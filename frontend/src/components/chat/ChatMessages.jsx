import React, { useEffect, useRef } from 'react';
import UserBubble from './UserBubble';
import AdviceBubble from './AdviceBubble';
import TypingIndicator from './TypingIndicator';

const ChatMessages = ({ messages, isSending, onSelectSuggested }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isSending]);


  return (
    <div className="flex-1 overflow-y-auto custom-scrollbar p-4 sm:p-6 bg-transparent">
      <div className="max-w-4xl mx-auto flex flex-col">
        {messages.map((msg) => {
          if (msg.role === 'user') {
            return <UserBubble key={msg.id} message={msg.content} timestamp={msg.timestamp} />;
          } else {
            return (
              <AdviceBubble 
                key={msg.id} 
                advice={msg.advice} 
                rawContent={msg.content} 
                timestamp={msg.timestamp} 
              />
            );
          }
        })}
        {isSending && (
          <div className="flex w-full justify-start mb-6">
            <TypingIndicator />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatMessages;
