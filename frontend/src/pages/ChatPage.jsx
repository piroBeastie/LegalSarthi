import React, { useEffect, useState } from 'react';
import { Menu } from 'lucide-react';
import { useChat } from '../hooks/useChat';
import ChatSidebar from '../components/chat/ChatSidebar';
import ChatMessages from '../components/chat/ChatMessages';
import ChatInput from '../components/chat/ChatInput';

const ChatPage = () => {
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    const saved = localStorage.getItem('sidebarOpen');
    return saved !== null ? JSON.parse(saved) : true;
  });

  const {
    conversations,
    currentConversation,
    messages,
    isLoading,
    isSending,
    fetchConversations,
    loadConversation,
    startNewChat,
    sendMessage,
    deleteConversation,
  } = useChat();

  useEffect(() => {
    fetchConversations();
  }, [fetchConversations]);

  useEffect(() => {
    localStorage.setItem('sidebarOpen', JSON.stringify(sidebarOpen));
  }, [sidebarOpen]);

  const isEmpty = !currentConversation || messages.length === 0;

  return (
    <div className="w-full h-screen flex overflow-hidden bg-primary relative">
      <div className={`${sidebarOpen ? 'w-72' : 'w-0'} h-full transition-all duration-300 ease-in-out overflow-hidden shrink-0`}>
        <ChatSidebar 
          conversations={conversations}
          currentConversation={currentConversation}
          onSelectConversation={loadConversation}
          onNewChat={startNewChat}
          onDeleteConversation={deleteConversation}
          isOpen={sidebarOpen}
          setIsOpen={setSidebarOpen}
        />
      </div>
      
      <div className="flex-1 flex flex-col h-full bg-primary relative overflow-hidden">
        {/* Sidebar Toggle Button (Floating when sidebar is closed) */}
        {!sidebarOpen && (
          <div className="absolute top-4 left-4 z-10 hidden md:block">
            <button 
              onClick={() => setSidebarOpen(true)}
              className="p-2 text-text-muted hover:text-white transition-colors bg-secondary border border-border-color rounded-lg"
            >
              <Menu className="w-5 h-5" />
            </button>
          </div>
        )}

        {/* Mobile Top Navbar */}
        <div className="h-16 flex items-center justify-between px-4 z-20 md:hidden bg-primary/80 backdrop-blur-md border-b border-border-color shrink-0">
          <h2 className="text-xl tracking-tighter cursor-default select-none flex items-baseline">
            <span className="font-light text-text-muted mr-1">Legal</span>
            <span className="font-bold text-text uppercase">Sarthi</span>
          </h2>
          <button 
            onClick={() => setSidebarOpen(true)}
            className="p-2 text-text-muted hover:text-white transition-colors"
          >
            <Menu className="w-6 h-6" />
          </button>
        </div>
        
        <div className="flex-1 flex flex-col h-full overflow-hidden">
          {isEmpty ? (
            <div className="flex-1 flex flex-col h-full py-8">
              {/* Center Quote */}
              <div className="flex-1 flex items-center justify-center px-4">
                <h1 className="text-3xl md:text-5xl font-semibold text-text text-center max-w-2xl opacity-70 tracking-widest font-quote leading-tight">
                  "The law is reason, free from passion."
                </h1>
              </div>
              
              {/* Bottom Search Bar */}
              <div className="w-full px-4 max-w-4xl mx-auto mt-auto pb-6">
                <ChatInput 
                  onSendMessage={sendMessage} 
                  isSending={isSending} 
                  isCentered={true}
                />
              </div>
            </div>
          ) : (
            <div className="flex-1 flex flex-col h-full overflow-hidden">
              <div className="flex-1 overflow-y-auto">
                <ChatMessages 
                  messages={messages} 
                  isSending={isSending} 
                  onSelectSuggested={sendMessage} 
                />
              </div>
              <div className="shrink-0 pb-6 px-4 w-full max-w-4xl mx-auto">
                <ChatInput 
                  onSendMessage={sendMessage} 
                  isSending={isSending} 
                  isCentered={false}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
