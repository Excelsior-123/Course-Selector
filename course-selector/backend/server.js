import express from 'express';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';
import { courses, getAllCourses, getCourseById } from './data/courses.js';
import { generateOptimalSchedule, generateScheduleGrid } from './services/scheduler.js';
import { parseUserRequirements, generateRecommendationSummary } from './services/ai.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Get all courses
app.get('/api/courses', (req, res) => {
  const { department, tag, search } = req.query;
  let result = [...courses];
  
  if (department) {
    result = result.filter(c => c.department.includes(department));
  }
  
  if (tag) {
    result = result.filter(c => c.tags.includes(tag));
  }
  
  if (search) {
    const searchLower = search.toLowerCase();
    result = result.filter(c => 
      c.name.toLowerCase().includes(searchLower) ||
      c.nameEn.toLowerCase().includes(searchLower) ||
      c.code.toLowerCase().includes(searchLower) ||
      c.instructor.toLowerCase().includes(searchLower)
    );
  }
  
  res.json({
    success: true,
    count: result.length,
    courses: result
  });
});

// Get course by ID
app.get('/api/courses/:id', (req, res) => {
  const course = getCourseById(req.params.id);
  
  if (!course) {
    return res.status(404).json({
      success: false,
      error: '课程不存在'
    });
  }
  
  res.json({
    success: true,
    course
  });
});

// Get schedule grid for selected courses
app.post('/api/schedule/grid', (req, res) => {
  const { courseIds } = req.body;
  
  if (!courseIds || !Array.isArray(courseIds)) {
    return res.status(400).json({
      success: false,
      error: '请提供课程ID列表'
    });
  }
  
  const selectedCourses = courseIds
    .map(id => getCourseById(id))
    .filter(Boolean);
  
  const grid = generateScheduleGrid(selectedCourses);
  
  res.json({
    success: true,
    grid,
    courses: selectedCourses
  });
});

// Main recommendation endpoint
app.post('/api/recommend', async (req, res) => {
  try {
    const { input, selectedCourseIds = [] } = req.body;
    
    if (!input) {
      return res.status(400).json({
        success: false,
        error: '请提供选课需求描述'
      });
    }
    
    console.log('收到选课请求:', input);
    
    // Step 1: Parse user requirements with AI
    const aiResult = await parseUserRequirements(input);
    const preferences = aiResult.preferences;
    
    console.log('解析的偏好:', JSON.stringify(preferences, null, 2));
    
    // Step 2: Filter courses based on preferences
    let availableCourses = [...courses];
    
    // Filter by interests
    if (preferences.interests && preferences.interests.length > 0) {
      const interestMatches = availableCourses.filter(c => 
        preferences.interests.some(interest => 
          c.name.includes(interest) || 
          c.tags.some(t => t.includes(interest)) ||
          c.description.includes(interest)
        )
      );
      
      if (interestMatches.length > 0) {
        availableCourses = interestMatches;
      }
    }
    
    // Filter by difficulty preference
    if (preferences.difficultyPreference === 'easy') {
      availableCourses = availableCourses.filter(c => c.difficulty <= 2.5);
    } else if (preferences.difficultyPreference === 'hard') {
      availableCourses = availableCourses.filter(c => c.difficulty >= 4);
    }
    
    // Filter by workload preference
    if (preferences.workloadPreference === 'light') {
      availableCourses = availableCourses.filter(c => c.workload <= 2);
    }
    
    // Filter by grade preference
    if (preferences.gradePreference === 'high') {
      availableCourses = availableCourses.filter(c => 
        c.gradeDistribution.A >= 30 || c.gradeDistribution.A + c.gradeDistribution.B >= 70
      );
    }
    
    // Remove avoided courses
    if (preferences.avoidCourses && preferences.avoidCourses.length > 0) {
      availableCourses = availableCourses.filter(c => 
        !preferences.avoidCourses.some(avoid => 
          c.name.includes(avoid) || c.code.includes(avoid)
        )
      );
    }
    
    // Step 3: Generate optimal schedule
    const scheduleResult = generateOptimalSchedule(
      availableCourses,
      {
        requiredCourses: preferences.requiredCourses || [],
        preferredCourses: availableCourses.filter(c => 
          preferences.interests.some(i => c.name.includes(i) || c.tags.includes(i))
        ),
        preferEasy: preferences.difficultyPreference === 'easy',
        preferLightWorkload: preferences.workloadPreference === 'light',
        maxCourses: preferences.maxCourses || 6
      }
    );
    
    // Step 4: Generate AI summary
    const summary = await generateRecommendationSummary(
      scheduleResult.courses,
      input,
      preferences
    );
    
    // Step 5: Generate schedule grid
    const grid = generateScheduleGrid(scheduleResult.courses);
    
    res.json({
      success: true,
      data: {
        preferences,
        reasoning: aiResult.reasoning,
        summary,
        schedule: scheduleResult,
        grid
      }
    });
    
  } catch (error) {
    console.error('推荐失败:', error);
    res.status(500).json({
      success: false,
      error: '生成推荐时出错，请稍后重试'
    });
  }
});

// Get available filters/departments
app.get('/api/filters', (req, res) => {
  const departments = [...new Set(courses.map(c => c.department))];
  const tags = [...new Set(courses.flatMap(c => c.tags))];
  
  res.json({
    success: true,
    departments,
    tags
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    error: '服务器内部错误'
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`📚 Loaded ${courses.length} courses`);
});

export default app;