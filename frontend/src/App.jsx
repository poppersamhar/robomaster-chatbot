import React from 'react';
import ChatBot from './components/ChatBot';

function App() {
  return (
    <div className="min-h-screen bg-gray-900">
      {/* 模拟直播页面背景 */}
      <div className="flex items-center justify-center h-screen">
        <div className="text-center text-white">
          <h1 className="text-4xl font-bold mb-4">RoboMaster 机甲大师赛</h1>
          <p className="text-gray-400">直播页面示例 - 点击右下角小粉助手开始对话</p>
        </div>
      </div>

      {/* AI 问答机器人 */}
      <ChatBot />
    </div>
  );
}

export default App;
