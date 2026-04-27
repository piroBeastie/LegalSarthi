import React from 'react';
import { PlusCircle, MessageSquare, Trash2, X, LogOut, User, Scale } from 'lucide-react';
import CategoryBadge from './CategoryBadge';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

const ChatSidebar = ({ 
  conversations, 
  currentConversation, 
  onSelectConversation, 
  onNewChat, 
  onDeleteConversation,
  isOpen,
  setIsOpen
}) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/60 z-20 md:hidden backdrop-blur-sm"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed md:static inset-y-0 left-0 z-30 w-72 h-full bg-secondary border-r border-border-color transform transition-transform duration-300 ease-in-out flex flex-col ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
        
        {/* Header */}
        <div className="p-4 flex items-center justify-between border-b border-border-color">
          <div className="flex items-center space-x-2">
            <Scale className="w-6 h-6 text-accent" />
            <h2 className="text-xl font-bold text-white tracking-tight">LegalSarthi</h2>
          </div>
          <button 
            className="p-2 text-text-muted hover:text-white hover:bg-border-color rounded-md transition-all"
            onClick={() => setIsOpen(false)}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* New Chat Button */}
        <div className="px-4 py-2">
          <button 
            onClick={() => {
              onNewChat();
              if (window.innerWidth < 768) setIsOpen(false);
            }}
            className="w-full flex items-center justify-between bg-primary hover:bg-border-color border border-border-color text-text py-2.5 px-4 rounded-lg text-sm font-medium transition-all group"
          >
            <span>New Chat</span>
            <PlusCircle className="w-4 h-4 text-text-muted group-hover:text-accent transition-colors" />
          </button>
        </div>

        {/* Conversation List */}
        <div className="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-1 mt-2">
          <div className="text-xs font-semibold text-text-muted mb-3 px-2 uppercase tracking-wider">History</div>
          {conversations.length === 0 ? (
            <div className="text-center p-4 text-text-muted text-sm mt-4">
              No conversations yet
            </div>
          ) : (
            conversations.map((conv) => (
              <div 
                key={conv.id}
                className={`group flex items-center justify-between p-2.5 rounded-lg cursor-pointer transition-colors ${
                  currentConversation?.id === conv.id 
                    ? 'bg-border-color/50 text-text' 
                    : 'text-text-muted hover:bg-primary hover:text-text'
                }`}
                onClick={() => {
                  onSelectConversation(conv.id);
                  if (window.innerWidth < 768) setIsOpen(false);
                }}
              >
                <div className="flex items-center space-x-3 overflow-hidden flex-1">
                  <MessageSquare className={`w-4 h-4 shrink-0 ${currentConversation?.id === conv.id ? 'text-text' : 'text-text-muted group-hover:text-text'}`} />
                  <span className="text-sm font-medium truncate">
                    {conv.title || 'New Conversation'}
                  </span>
                </div>
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    if (window.confirm('Delete this conversation?')) {
                      onDeleteConversation(conv.id);
                    }
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 text-text-muted hover:text-red-400 transition-all shrink-0 ml-2"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))
          )}
        </div>

        {/* User Profile & Logout */}
        <div className="p-4 border-t border-border-color">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3 overflow-hidden">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0 border border-border-color">
                <User className="w-4 h-4 text-text-muted" />
              </div>
              <div className="truncate text-sm font-medium text-text">
                {user?.name || 'User'}
              </div>
            </div>
            <button 
              onClick={handleLogout}
              className="p-2 text-text-muted hover:text-red-400 hover:bg-primary rounded-md transition-colors"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChatSidebar;
