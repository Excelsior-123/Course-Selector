import React, { useState, useEffect } from 'react';
import InputSection from './components/InputSection';
import ScheduleGrid from './components/ScheduleGrid';
import CourseList from './components/CourseList';
import LoadingState from './components/LoadingState';
import api from './services/api';

function App() {
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (input) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.post('/recommend', { input });
      if (response.data.success) {
        setRecommendation(response.data.data);
      } else {
        setError(response.data.error || '获取推荐失败');
      }
    } catch (err) {
      setError(err.response?.data?.error || '网络错误，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen pb-20">
      {/* Header */}
      <header className="glass sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-400 to-purple-600 flex items-center justify-center animate-float">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">智能选课助手</h1>
                <p className="text-xs text-white/70">AI-powered Course Selection</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 pt-6">
        {/* Input Section */}
        <InputSection onSubmit={handleSubmit} loading={loading} />

        {/* Error Message */}
        {error && (
          <div className="mt-6 p-4 rounded-2xl bg-red-500/20 border border-red-400/30 text-red-100 animate-fade-in">
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && <LoadingState />}

        {/* Results */}
        {recommendation && !loading && (
          <div className="mt-6 space-y-6 animate-slide-up">
            {/* AI Summary */}
            <div className="glass-card rounded-2xl p-5">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h2 className="text-lg font-bold text-gray-800">AI 推荐总结</h2>
              </div>
              <p className="text-gray-600 leading-relaxed">{recommendation.summary}</p>
              
              {/* Stats */}
              <div className="mt-4 grid grid-cols-4 gap-3">
                <div className="text-center p-3 bg-blue-50 rounded-xl">
                  <p className="text-2xl font-bold text-blue-600">{recommendation.schedule.stats.courseCount}</p>
                  <p className="text-xs text-gray-500">门课程</p>
                </div>
                <div className="text-center p-3 bg-purple-50 rounded-xl">
                  <p className="text-2xl font-bold text-purple-600">{recommendation.schedule.stats.totalCredits}</p>
                  <p className="text-xs text-gray-500">总学分</p>
                </div>
                <div className="text-center p-3 bg-green-50 rounded-xl">
                  <p className="text-2xl font-bold text-green-600">{recommendation.schedule.stats.averageRating.toFixed(1)}</p>
                  <p className="text-xs text-gray-500">平均评分</p>
                </div>
                <div className="text-center p-3 bg-orange-50 rounded-xl">
                  <p className="text-2xl font-bold text-orange-600">{recommendation.schedule.stats.averageDifficulty.toFixed(1)}</p>
                  <p className="text-xs text-gray-500">平均难度</p>
                </div>
              </div>
            </div>

            {/* Schedule Grid */}
            <ScheduleGrid grid={recommendation.grid} courses={recommendation.schedule.courses} />

            {/* Course List */}
            <CourseList courses={recommendation.schedule.courses} />
          </div>
        )}

        {/* Empty State */}
        {!recommendation && !loading && (
          <div className="mt-12 text-center">
            <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-white/20 backdrop-blur flex items-center justify-center">
              <svg className="w-12 h-12 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">开始智能选课</h3>
            <p className="text-white/70 max-w-md mx-auto">
              用自然语言描述你的选课需求，例如："我对计算机网络感兴趣，希望上午上课，同时选一门给分高的体育课"
            </p>
            
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              {['想选给分高的水课', '周二周四晚上有课', 'AI相关课程', '作业少好拿A'].map((example) => (
                <button
                  key={example}
                  onClick={() => handleSubmit(example)}
                  className="px-4 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white/80 text-sm transition-all"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;