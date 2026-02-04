import React, { useState, useRef, useEffect } from 'react';
import FloatingButton from './FloatingButton';
import MessageBubble from './MessageBubble';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function ChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      text: '你好！我是小粉助手，RoboMaster机甲大师赛的AI问答机器人。有什么关于RoboMaster的问题可以问我哦！',
      isUser: false,
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setMessages((prev) => [...prev, { text: userMessage, isUser: true }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setMessages((prev) => [...prev, { text: data.reply, isUser: false }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { text: '抱歉，网络出现问题，请稍后再试。', isUser: false },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* 聊天窗口 */}
      <div
        className={`fixed bottom-24 right-5 w-96 h-[500px] bg-white rounded-2xl shadow-2xl
          flex flex-col overflow-hidden
          transition-all duration-300 ease-in-out origin-bottom-right
          ${isOpen ? 'scale-100 opacity-100' : 'scale-0 opacity-0 pointer-events-none'}`}
      >
        {/* 头部 */}
        <div className="bg-gradient-to-r from-pink-500 to-pink-600 px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
              <span className="text-pink-500 text-lg">🤖</span>
            </div>
            <span className="text-white font-semibold">小粉助手</span>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="text-white hover:bg-white/20 rounded-full p-1 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* 消息区域 */}
        <div className="flex-1 overflow-y-auto p-4 scrollbar-thin">
          {messages.map((msg, index) => (
            <MessageBubble key={index} message={msg.text} isUser={msg.isUser} />
          ))}
          {isLoading && (
            <div className="flex justify-start mb-3">
              <div className="bg-gray-100 px-4 py-2 rounded-2xl rounded-bl-md">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* 输入区域 */}
        <div className="border-t border-gray-200 p-3">
          <div className="flex gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="输入你的问题..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-full
                focus:outline-none focus:border-pink-500 focus:ring-1 focus:ring-pink-500
                text-sm"
              disabled={isLoading}
            />
            <button
              onClick={handleSend}
              disabled={isLoading || !inputValue.trim()}
              className="px-4 py-2 bg-pink-500 text-white rounded-full
                hover:bg-pink-600 transition-colors
                disabled:bg-gray-300 disabled:cursor-not-allowed
                flex items-center justify-center"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* 悬浮按钮 */}
      <FloatingButton onClick={() => setIsOpen(!isOpen)} isOpen={isOpen} />
    </>
  );
}

export default ChatBot;
