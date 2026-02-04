import React from 'react';

function FloatingButton({ onClick, isOpen }) {
  return (
    <button
      onClick={onClick}
      className={`fixed bottom-5 right-5 w-16 h-16
        flex items-center justify-center
        transition-all duration-300 ease-in-out
        hover:scale-110
        focus:outline-none
        ${isOpen ? 'opacity-70' : ''}`}
      aria-label={isOpen ? '关闭聊天' : '打开聊天'}
    >
      {isOpen ? (
        <div className="relative">
          <img
            src="/mascot.png"
            alt="小粉助手"
            className="w-16 h-16 object-contain drop-shadow-lg"
          />
          <div className="absolute -top-1 -right-1 w-5 h-5 bg-pink-500 rounded-full flex items-center justify-center">
            <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        </div>
      ) : (
        <img
          src="/mascot.png"
          alt="小粉助手"
          className="w-16 h-16 object-contain drop-shadow-lg animate-bounce-slow"
        />
      )}
    </button>
  );
}

export default FloatingButton;
