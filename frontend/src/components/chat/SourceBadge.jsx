import React from 'react';
import { Database, Sparkles, Bot } from 'lucide-react';

const SourceBadge = ({ source }) => {
  let label = 'Mock AI';
  let color = 'bg-primary text-text-muted border-border-color';
  let Icon = Bot;

  if (source === 'rules_engine') {
    label = 'Rules Engine';
    color = 'bg-primary text-emerald-400 border-emerald-900/50';
    Icon = Database;
  } else if (source === 'gemini_ai') {
    label = 'Gemini AI';
    color = 'bg-primary text-purple-400 border-purple-900/50';
    Icon = Sparkles;
  }

  return (
    <div className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium border ${color}`}>
      <Icon className="mr-1 h-3 w-3" />
      {label}
    </div>
  );
};

export default SourceBadge;
