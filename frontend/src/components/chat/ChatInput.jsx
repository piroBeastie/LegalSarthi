import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

const ChatInput = ({ onSendMessage, isSending, isCentered = false }) => {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);
  const MAX_CHARS = 2000;

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [text]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    if (text.trim() && !isSending && text.length <= MAX_CHARS) {
      onSendMessage(text);
      setText('');
      // Reset height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const remainingChars = MAX_CHARS - text.length;

  return (
    <div className={`p-4 ${isCentered ? '' : 'bg-primary'}`}>
      <div className={`max-w-4xl mx-auto relative flex items-end bg-secondary border ${isCentered ? 'border-border-color shadow-lg' : 'border-border-color shadow-sm'} rounded-2xl focus-within:ring-1 focus-within:ring-accent focus-within:border-accent transition-all`}>
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe your legal situation..."
          className="w-full max-h-[150px] py-4 pl-5 pr-14 bg-transparent border-none text-text placeholder-text-muted focus:ring-0 resize-none custom-scrollbar text-base"
          rows={1}
          disabled={isSending}
        />
        
        <button
          onClick={handleSubmit}
          disabled={!text.trim() || isSending || text.length > MAX_CHARS}
          className="absolute right-2 bottom-2 p-2.5 rounded-xl text-primary bg-accent hover:bg-amber-400 disabled:bg-border-color disabled:text-text-muted transition-colors"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
      
      <div className="max-w-4xl mx-auto mt-2 flex justify-between px-2">
        <p className="text-[11px] text-text-muted">
          Press Enter to send, Shift + Enter for new line
        </p>
        <p className={`text-[11px] ${remainingChars < 100 ? 'text-red-400' : 'text-text-muted'}`}>
          {text.length}/{MAX_CHARS}
        </p>
      </div>
    </div>
  );
};

export default ChatInput;
