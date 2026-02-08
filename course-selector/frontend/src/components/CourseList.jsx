import React, { useState } from 'react';

function CourseList({ courses }) {
  const [expandedCourse, setExpandedCourse] = useState(null);

  const getDifficultyColor = (difficulty) => {
    if (difficulty <= 2) return 'text-green-500';
    if (difficulty <= 3) return 'text-yellow-500';
    if (difficulty <= 4) return 'text-orange-500';
    return 'text-red-500';
  };

  const getWorkloadColor = (workload) => {
    if (workload <= 1) return 'bg-green-100 text-green-700';
    if (workload <= 2) return 'bg-blue-100 text-blue-700';
    if (workload <= 3) return 'bg-yellow-100 text-yellow-700';
    return 'bg-red-100 text-red-700';
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <svg
        key={i}
        className={`w-4 h-4 ${i < Math.floor(rating) ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}`}
        viewBox="0 0 20 20"
      >
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
      </svg>
    ));
  };

  return (
    <div className="glass-card rounded-2xl p-5">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-400 to-teal-500 flex items-center justify-center">
          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
        </div>
        <h2 className="text-lg font-bold text-gray-800">推荐课程</h2>
        <span className="text-sm text-gray-500">共 {courses.length} 门</span>
      </div>
      
      <div className="space-y-4">
        {courses.map((course, index) => (
          <div
            key={course.id}
            className="rounded-xl border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            {/* Course Header */}
            <div
              className="p-4 cursor-pointer bg-white"
              onClick={() => setExpandedCourse(expandedCourse === course.id ? null : course.id)}
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-bold text-gray-800">{course.name}</h3>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">
                      {course.code}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500 mt-1">{course.department} · {course.instructor}</p>
                  
                  <div className="flex items-center gap-4 mt-3">
                    <div className="flex items-center gap-1">
                      {renderStars(course.rating)}
                      <span className="text-sm text-gray-600 ml-1">{course.rating}</span>
                    </div>
                    
                    <div className={`text-xs px-2 py-1 rounded-full ${getWorkloadColor(course.workload)}`}>
                      工作量: {['极少', '较少', '适中', '较多', '极多'][course.workload - 1] || course.workload}
                    </div>
                    
                    <div className={`text-sm font-medium ${getDifficultyColor(course.difficulty)}`}>
                      难度: {course.difficulty.toFixed(1)}
                    </div>
                  </div>
                </div>
                
                <svg
                  className={`w-5 h-5 text-gray-400 transition-transform ${expandedCourse === course.id ? 'rotate-180' : ''}`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
              
              {/* Tags */}
              <div className="flex flex-wrap gap-2 mt-3">
                {course.tags.map((tag) => (
                  <span
                    key={tag}
                    className="text-xs px-2 py-1 rounded-full bg-blue-50 text-blue-600"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
            
            {/* Expanded Details */}
            {expandedCourse === course.id && (
              <div className="px-4 pb-4 bg-gray-50 border-t border-gray-100 animate-fade-in">
                <div className="pt-4 space-y-4">
                  {/* Schedule */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">课程时间</h4>
                    <div className="space-y-1">
                      {course.schedule.map((slot, i) => (
                        <div key={i} className="text-sm text-gray-600 flex items-center gap-2">
                          <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          周{['一', '二', '三', '四', '五', '六', '日'][slot.day - 1]} {slot.startTime}-{slot.endTime} · {slot.location}
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {/* Description */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-1">课程简介</h4>
                    <p className="text-sm text-gray-600">{course.description}</p>
                  </div>
                  
                  {/* Grade Distribution */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">成绩分布</h4>
                    <div className="flex h-6 rounded-lg overflow-hidden">
                      <div className="bg-green-400 flex items-center justify-center text-xs text-white" style={{ width: `${course.gradeDistribution.A}%` }}>
                        {course.gradeDistribution.A >= 15 && `A ${course.gradeDistribution.A}%`}
                      </div>
                      <div className="bg-blue-400 flex items-center justify-center text-xs text-white" style={{ width: `${course.gradeDistribution.B}%` }}>
                        {course.gradeDistribution.B >= 15 && `B ${course.gradeDistribution.B}%`}
                      </div>
                      <div className="bg-yellow-400 flex items-center justify-center text-xs text-white" style={{ width: `${course.gradeDistribution.C}%` }}>
                        {course.gradeDistribution.C >= 15 && `C ${course.gradeDistribution.C}%`}
                      </div>
                      <div className="bg-red-400 flex items-center justify-center text-xs text-white" style={{ width: `${course.gradeDistribution.D}%` }}>
                        {course.gradeDistribution.D >= 10 && `D ${course.gradeDistribution.D}%`}
                      </div>
                    </div>
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>A: {course.gradeDistribution.A}%</span>
                      <span>B: {course.gradeDistribution.B}%</span>
                      <span>C: {course.gradeDistribution.C}%</span>
                      <span>D: {course.gradeDistribution.D}%</span>
                    </div>
                  </div>
                  
                  {/* Reviews */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">学生评价</h4>
                    <div className="space-y-2">
                      {course.reviews.slice(0, 3).map((review, i) => (
                        <div key={i} className="bg-white p-3 rounded-lg border border-gray-100">
                          <div className="flex items-center justify-between">
                            <span className="text-xs text-gray-500">{review.author}</span>
                            <div className="flex">
                              {Array.from({ length: review.rating }, (_, j) => (
                                <svg key={j} className="w-3 h-3 text-yellow-400 fill-yellow-400" viewBox="0 0 20 20">
                                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                              ))}
                            </div>
                          </div>
                          <p className="text-sm text-gray-600 mt-1">{review.content}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default CourseList;