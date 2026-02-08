import React from 'react';

function LoadingState() {
  return (
    <div className="mt-6 glass-card rounded-2xl p-8 animate-fade-in">
      <div className="flex flex-col items-center justify-center py-8">
        <div className="relative">
          {/* Outer ring */}
          <div className="w-20 h-20 rounded-full border-4 border-blue-200 animate-pulse"></div>
          
          {/* Inner spinning ring */}
          <div className="absolute inset-0 w-20 h-20 rounded-full border-4 border-transparent border-t-blue-500 animate-spin"></div>
          
          {/* Center icon */}
          <div className="absolute inset-0 flex items-center justify-center">
            <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
        </div>
        
        <div className="mt-6 text-center">
          <h3 className="text-lg font-semibold text-gray-800">AI正在分析您的需求...</h3>
          <div className="mt-4 space-y-2">
            <div className="flex items-center gap-3 text-sm text-gray-600">
              <div className="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center">
                <svg className="w-3 h-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span>解析选课偏好</span>
            </div>
            <div className="flex items-center gap-3 text-sm text-gray-600">
              <div className="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center animate-pulse">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              </div>
              <span>筛选匹配课程</span>
            </div>
            <div className="flex items-center gap-3 text-sm text-gray-400">
              <div className="w-5 h-5 rounded-full bg-gray-100 flex items-center justify-center">
                <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
              </div>
              <span>生成最优课表</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoadingState;