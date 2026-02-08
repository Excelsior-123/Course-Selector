import React, { useState } from 'react';

function InputSection({ onSubmit, loading }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input.trim());
    }
  };

  return (
    <div className="glass-card rounded-2xl p-5">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            描述你的选课需求
          </label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="例如：我对计算机网络感兴趣，希望上午9点到下午6点上课，考核简单作业少给分高；同时想选篮球课，周二到周四晚上..."
            className="w-full h-32 p-4 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 resize-none text-gray-700 placeholder-gray-400 transition-all"
            disabled={loading}
          />
        </div>
        
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              AI分析中...
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              生成推荐方案
            </>
          )}
        </button>
      </form>
      
      <div className="mt-4 flex flex-wrap gap-2">
        <span className="text-xs text-gray-500">热门标签：</span>
        {['水课推荐', '给分高', '专业课', '体育课', '通识课'].map((tag) => (
          <button
            key={tag}
            onClick={() => setInput(prev => prev ? prev + ' ' + tag : tag)}
            className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600 hover:bg-blue-100 hover:text-blue-600 transition-colors"
          >
            #{tag}
          </button>
        ))}
      </div>
    </div>
  );
}

export default InputSection;