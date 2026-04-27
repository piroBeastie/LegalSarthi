import React, { useState } from 'react';
import { ChevronDown, ChevronUp, BookOpen, CheckCircle, ShieldAlert } from 'lucide-react';
import CategoryBadge from './CategoryBadge';
import SourceBadge from './SourceBadge';
import { Scale } from 'lucide-react';

const AdviceBubble = ({ advice, timestamp, rawContent }) => {
  const [lawsExpanded, setLawsExpanded] = useState(false);

  // If no advice object (e.g., fallback or parsing failed), render raw content
  if (!advice) {
    return (
      <div className="flex w-full justify-start mb-10">
        <div className="flex flex-col items-start w-full max-w-3xl">
          <p className="whitespace-pre-wrap text-[15px] leading-relaxed text-text">
            {rawContent}
          </p>
        </div>
      </div>
    );
  }

  const { category, summary, steps = [], relevant_laws = [], disclaimer, source } = advice;

  return (
    <div className="flex w-full justify-start mb-10">
      <div className="flex flex-col items-start w-full max-w-3xl space-y-6">
        
        {/* Header Badges */}
        <div className="flex items-center flex-wrap gap-3">
          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-accent/20 border border-accent/30 text-accent mr-2">
            <Scale className="w-4 h-4" />
          </div>
          <CategoryBadge category={category} />
          <SourceBadge source={source} />
        </div>

        {/* Summary */}
        <div className="w-full">
          <p className="text-text text-[15px] leading-relaxed whitespace-pre-wrap">
            {summary}
          </p>
        </div>

        {/* Actionable Steps */}
        {steps && steps.length > 0 && (
          <div className="w-full mt-2">
            <h4 className="text-[15px] font-semibold text-text mb-4 flex items-center">
              Recommended Steps
            </h4>
            <div className="space-y-4 pl-1">
              {steps.map((step, idx) => (
                <div key={idx} className="flex items-start group">
                  <span className="flex-shrink-0 text-text-muted font-mono text-sm mr-4 mt-0.5 w-4 text-right">
                    {idx + 1}.
                  </span>
                  <p className="text-[15px] text-text-muted leading-relaxed">{step}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Relevant Laws (Collapsible) */}
        {relevant_laws && relevant_laws.length > 0 && (
          <div className="w-full pt-2">
            <button 
              onClick={() => setLawsExpanded(!lawsExpanded)}
              className="flex items-center text-sm font-medium text-text-muted hover:text-text transition-colors"
            >
              <BookOpen className="w-4 h-4 mr-2" />
              Relevant Indian Laws Cited
              {lawsExpanded ? <ChevronUp className="w-4 h-4 ml-2" /> : <ChevronDown className="w-4 h-4 ml-2" />}
            </button>
            
            {lawsExpanded && (
              <div className="mt-4 pl-6 border-l-2 border-border-color">
                <ul className="space-y-3">
                  {relevant_laws.map((law, idx) => (
                    <li key={idx} className="flex items-start text-sm text-text-muted leading-relaxed">
                      <Scale className="w-3.5 h-3.5 mr-3 mt-1 flex-shrink-0 text-accent/70" />
                      <span>{law}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Disclaimer Footer */}
        {disclaimer && (
          <div className="w-full mt-6 pt-4 border-t border-border-color/50">
            <div className="flex items-start">
              <ShieldAlert className="w-4 h-4 text-accent mt-0.5 mr-3 flex-shrink-0 opacity-80" />
              <p className="text-sm text-text-muted italic leading-relaxed">
                {disclaimer}
              </p>
            </div>
          </div>
        )}

        {/* Timestamp */}
        {timestamp && (
          <div className="w-full text-left pt-2">
            <span className="text-xs text-text-muted/50 font-medium">
              {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>
        )}

      </div>
    </div>
  );
};

export default AdviceBubble;
