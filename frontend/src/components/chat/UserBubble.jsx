import React from 'react';
import { User } from 'lucide-react';

const UserBubble = ({ message, timestamp }) => {
  return (
    <div className="flex w-full justify-end mb-6">
      <div className="flex flex-col items-end max-w-[85%] sm:max-w-[75%]">
        <div className="bg-secondary border border-border-color text-text rounded-2xl rounded-tr-none px-5 py-3.5 shadow-sm">
          <p className="whitespace-pre-wrap text-sm leading-relaxed">{message}</p>
        </div>
        {timestamp && (
          <span className="text-[10px] text-text-muted mt-1 mr-1">
            {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        )}
      </div>
    </div>
  );
};

export default UserBubble;
