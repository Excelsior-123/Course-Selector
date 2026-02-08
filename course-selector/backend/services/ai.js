import Anthropic from '@anthropic-ai/sdk';
import dotenv from 'dotenv';

dotenv.config();

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || 'sk-api-nNHt79hIL5GSXj5DBHSGEhIPsNilUJQBORmHk7vMbLQ0Pkd7MBGluf36N_mix9gl-18cStiunbpljKGYE_tsVLjSVYKA8-FGe-5xZM4HT6QMiCnj4G1bkl4',
  baseURL: process.env.ANTHROPIC_BASE_URL || 'https://api.minimaxi.com/anthropic',
});

const SYSTEM_PROMPT = `你是一个智能选课助手，帮助大学生解析选课需求并推荐最优课程组合。

你的任务是：
1. 解析用户的自然语言选课需求
2. 提取关键信息：
   - 感兴趣的课程类型/名称
   - 时间偏好（如"上午9点到下午6点"、"周二周四晚上"）
   - 难度偏好（如"考核简单"、"给分高"、"水课"）
   - 工作量偏好（如"作业少"）
   - 必选的课程
   - 想避开的课程

3. 返回结构化的JSON格式：
{
  "preferences": {
    "interests": ["计算机网络", "篮球"],
    "timeConstraints": {
      "preferredDays": [1, 2, 3, 4, 5],
      "preferredTimeRanges": [{"start": "09:00", "end": "18:00"}],
      "avoidEvening": false
    },
    "difficultyPreference": "easy",
    "workloadPreference": "light",
    "gradePreference": "high",
    "requiredCourses": [],
    "avoidCourses": [],
    "maxCourses": 6,
    "priorities": ["给分高", "作业少", "感兴趣"]
  },
  "reasoning": "用户想要选择计算机网络相关的专业课，同时选篮球课作为体育课..."
}

注意：
- 周一=1, 周二=2, 周三=3, 周四=4, 周五=5, 周六=6, 周日=7
- difficultyPreference: "easy", "medium", "hard", "any"
- workloadPreference: "light", "medium", "heavy", "any"
- gradePreference: "high", "medium", "any"
- 只返回JSON，不要其他文字`;

export async function parseUserRequirements(userInput) {
  try {
    const response = await anthropic.messages.create({
      model: 'MiniMax-M2.1',
      max_tokens: 2000,
      system: SYSTEM_PROMPT,
      messages: [
        { role: 'user', content: userInput }
      ]
    });

    const content = response.content[0].text;
    
    // Extract JSON from response
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      return parsed;
    }
    
    throw new Error('无法解析AI响应');
  } catch (error) {
    console.error('AI解析错误:', error);
    // Return default preferences on error
    return {
      preferences: {
        interests: [],
        timeConstraints: {
          preferredDays: [1, 2, 3, 4, 5],
          preferredTimeRanges: [],
          avoidEvening: false
        },
        difficultyPreference: 'any',
        workloadPreference: 'any',
        gradePreference: 'any',
        requiredCourses: [],
        avoidCourses: [],
        maxCourses: 6,
        priorities: []
      },
      reasoning: '使用默认偏好设置'
    };
  }
}

export async function generateRecommendationSummary(selectedCourses, userInput, preferences) {
  try {
    const coursesInfo = selectedCourses.map(c => ({
      name: c.name,
      code: c.code,
      instructor: c.instructor,
      rating: c.rating,
      difficulty: c.difficulty,
      schedule: c.schedule
    }));

    const prompt = `基于用户的选课需求："${userInput}"

已推荐以下课程：
${JSON.stringify(coursesInfo, null, 2)}

请生成一段友好的推荐总结，说明：
1. 为什么推荐这些课程
2. 课程组合的优点
3. 可能的注意事项

用中文回复，语气友好，像是一个贴心的学长/学姐在给出建议。`;

    const response = await anthropic.messages.create({
      model: 'MiniMax-M2.1',
      max_tokens: 1000,
      messages: [
        { role: 'user', content: prompt }
      ]
    });

    return response.content[0].text;
  } catch (error) {
    console.error('生成总结错误:', error);
    return '已为您生成最优课程组合，请查看下方课表。';
  }
}