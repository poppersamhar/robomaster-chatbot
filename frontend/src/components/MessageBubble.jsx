import React from 'react';

function MessageBubble({ message, isUser }) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-[80%] px-4 py-2 rounded-2xl ${
          isUser
            ? 'bg-blue-500 text-white rounded-br-md'
            : 'bg-gray-100 text-gray-800 rounded-bl-md'
        }`}
      >
        <p className="text-sm whitespace-pre-wrap">{message}</p>
      </div>
    </div>
  );
}

export default MessageBubble;
