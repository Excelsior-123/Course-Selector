/**
 * Schedule optimization algorithm
 * - Avoid time conflicts
 * - Maximize preferences
 * - Balance workload
 */

function timeToMinutes(time) {
  const [hours, minutes] = time.split(':').map(Number);
  return hours * 60 + minutes;
}

function hasConflict(course1, course2) {
  for (const slot1 of course1.schedule) {
    for (const slot2 of course2.schedule) {
      if (slot1.day !== slot2.day) continue;
      
      const start1 = timeToMinutes(slot1.startTime);
      const end1 = timeToMinutes(slot1.endTime);
      const start2 = timeToMinutes(slot2.startTime);
      const end2 = timeToMinutes(slot2.endTime);
      
      // Check overlap
      if (start1 < end2 && start2 < end1) {
        return true;
      }
    }
  }
  return false;
}

function hasAnyConflict(selectedCourses, newCourse) {
  return selectedCourses.some(c => hasConflict(c, newCourse));
}

function calculateWorkload(selectedCourses) {
  return selectedCourses.reduce((sum, c) => sum + c.workload, 0);
}

function calculateAverageRating(selectedCourses) {
  if (selectedCourses.length === 0) return 0;
  return selectedCourses.reduce((sum, c) => sum + c.rating, 0) / selectedCourses.length;
}

function calculateAverageDifficulty(selectedCourses) {
  if (selectedCourses.length === 0) return 0;
  return selectedCourses.reduce((sum, c) => sum + c.difficulty, 0) / selectedCourses.length;
}

function calculateScore(selectedCourses, preferences = {}) {
  let score = 0;
  
  // Rating score (0-50)
  score += calculateAverageRating(selectedCourses) * 10;
  
  // Difficulty preference
  const avgDifficulty = calculateAverageDifficulty(selectedCourses);
  if (preferences.preferEasy) {
    score += (5 - avgDifficulty) * 5;
  }
  
  // Workload preference
  const totalWorkload = calculateWorkload(selectedCourses);
  if (preferences.preferLightWorkload) {
    score += Math.max(0, 30 - totalWorkload * 2);
  }
  
  // Number of courses
  score += selectedCourses.length * 3;
  
  // Credit hours
  const totalCredits = selectedCourses.reduce((sum, c) => sum + c.credits, 0);
  score += totalCredits * 2;
  
  return score;
}

export function generateOptimalSchedule(availableCourses, preferences = {}, maxCourses = 6) {
  const { requiredCourses = [], preferredCourses = [], timeConstraints = [] } = preferences;
  
  // Start with required courses
  let selected = [...requiredCourses];
  
  // Filter out conflicting preferred courses
  const validPreferred = preferredCourses.filter(c => 
    !hasAnyConflict(selected, c) && !selected.find(s => s.id === c.id)
  );
  
  // Sort by rating and preference score
  validPreferred.sort((a, b) => {
    const scoreA = a.rating * 2 - a.difficulty;
    const scoreB = b.rating * 2 - b.difficulty;
    return scoreB - scoreA;
  });
  
  // Add preferred courses greedily
  for (const course of validPreferred) {
    if (selected.length >= maxCourses) break;
    if (!hasAnyConflict(selected, course)) {
      selected.push(course);
    }
  }
  
  // Fill remaining slots with highly-rated courses
  const remaining = availableCourses.filter(c => 
    !selected.find(s => s.id === c.id) && !hasAnyConflict(selected, c)
  );
  
  remaining.sort((a, b) => {
    // Prioritize by rating and ease
    const scoreA = a.rating * 2 + (5 - a.difficulty) + (5 - a.workload);
    const scoreB = b.rating * 2 + (5 - b.difficulty) + (5 - b.workload);
    return scoreB - scoreA;
  });
  
  for (const course of remaining) {
    if (selected.length >= maxCourses) break;
    selected.push(course);
  }
  
  // Calculate statistics
  const stats = {
    totalCredits: selected.reduce((sum, c) => sum + c.credits, 0),
    totalWorkload: calculateWorkload(selected),
    averageRating: calculateAverageRating(selected),
    averageDifficulty: calculateAverageDifficulty(selected),
    courseCount: selected.length,
    score: calculateScore(selected, preferences)
  };
  
  return {
    courses: selected,
    stats,
    conflicts: []
  };
}

export function generateScheduleGrid(courses) {
  const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
  const hours = Array.from({ length: 14 }, (_, i) => i + 8); // 8:00 - 21:00
  
  const grid = days.map((day, dayIndex) => ({
    day,
    slots: hours.map(hour => ({
      hour,
      time: `${hour.toString().padStart(2, '0')}:00`,
      course: null,
      isOccupied: false
    }))
  }));
  
  for (const course of courses) {
    for (const slot of course.schedule) {
      const dayIndex = slot.day - 1;
      if (dayIndex < 0 || dayIndex >= 7) continue;
      
      const startHour = parseInt(slot.startTime.split(':')[0]);
      const endHour = parseInt(slot.endTime.split(':')[0]);
      
      for (let h = startHour; h < endHour; h++) {
        const slotIndex = hours.indexOf(h);
        if (slotIndex >= 0) {
          grid[dayIndex].slots[slotIndex].course = course;
          grid[dayIndex].slots[slotIndex].isOccupied = true;
        }
      }
    }
  }
  
  return grid;
}