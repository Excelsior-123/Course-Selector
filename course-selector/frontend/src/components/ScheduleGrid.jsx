import React from 'react';

function ScheduleGrid({ grid, courses }) {
  const hours = Array.from({ length: 14 }, (_, i) => i + 8);
  const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
  
  const getCourseColor = (course) => {
    if (!course) return '';
    if (course.code.startsWith('CS')) return 'bg-gradient-to-br from-blue-400 to-cyan-400';
    if (course.code.startsWith('MATH')) return 'bg-gradient-to-br from-pink-400 to-yellow-400';
    if (course.code.startsWith('PE')) return 'bg-gradient-to-br from-teal-400 to-indigo-600';
    if (course.code.startsWith('ART')) return 'bg-gradient-to-br from-purple-400 to-pink-400';
    if (course.code.startsWith('ENG')) return 'bg-gradient-to-br from-blue-400 to-cyan-400';
    return 'bg-gradient-to-br from-indigo-400 to-purple-500';
  };

  return (
    <div className="glass-card rounded-2xl p-5 overflow-hidden">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-400 to-indigo-500 flex items-center justify-center">
          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <h2 className="text-lg font-bold text-gray-800">课程时间表</h2>
      </div>
      
      <div className="overflow-x-auto">
        <div className="min-w-[800px]">
          {/* Header */}
          <div className="grid grid-cols-8 gap-1">
            <div className="text-center py-2 text-sm font-medium text-gray-500">时间</div>
            {days.map((day) => (
              <div key={day} className="text-center py-2 text-sm font-medium text-gray-700 bg-gray-50 rounded-lg">
                {day}
              </div>
            ))}
          </div>
          
          {/* Grid */}
          <div className="mt-1 space-y-1">
            {hours.map((hour) => (
              <div key={hour} className="grid grid-cols-8 gap-1">
                <div className="text-center py-2 text-xs text-gray-500 flex items-center justify-center">
                  {hour}:00
                </div>
                {grid.map((dayGrid, dayIndex) => {
                  const slot = dayGrid.slots.find(s => s.hour === hour);
                  const course = slot?.course;
                  
                  return (
                    <div
                      key={dayIndex}
                      className={`
                        min-h-[50px] rounded-lg p-1 text-xs
                        ${course 
                          ? `${getCourseColor(course)} text-white shadow-md` 
                          : 'bg-gray-50'
                        }
                      `}
                    >
                      {course && (
                        <div className="h-full flex flex-col justify-center">
                          <p className="font-semibold truncate">{course.name}</p>
                          <p className="opacity-80 truncate">{course.location}</p>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Legend */}
      <div className="mt-4 flex flex-wrap gap-3 text-xs">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-gradient-to-br from-blue-400 to-cyan-400"></div>
          <span className="text-gray-600">计算机</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-gradient-to-br from-pink-400 to-yellow-400"></div>
          <span className="text-gray-600">数学</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-gradient-to-br from-teal-400 to-indigo-600"></div>
          <span className="text-gray-600">体育</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-gradient-to-br from-purple-400 to-pink-400"></div>
          <span className="text-gray-600">人文</span>
        </div>
      </div>
    </div>
  );
}

export default ScheduleGrid;