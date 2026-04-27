import { useState, useCallback } from 'react';
import client from '../api/client';
import toast from 'react-hot-toast';

export const useChat = () => {
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);

  const fetchConversations = useCallback(async () => {
    try {
      setIsLoading(true);
      const res = await client.get('/chat/conversations?skip=0&limit=50');
      setConversations(res.data);
    } catch (error) {
      toast.error('Failed to load conversations');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loadConversation = useCallback(async (id) => {
    try {
      setIsLoading(true);
      const res = await client.get(`/chat/conversations/${id}`);
      setCurrentConversation({
        id: res.data.id,
        title: res.data.title,
        category: res.data.category,
      });
      setMessages(res.data.messages || []);
    } catch (error) {
      toast.error('Failed to load conversation');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const startNewChat = useCallback(() => {
    setCurrentConversation(null);
    setMessages([]);
  }, []);

  const sendMessage = useCallback(async (text) => {
    if (!text.trim()) return;

    // Optimistic UI
    const tempId = Date.now().toString();
    const newUserMsg = {
      id: tempId,
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, newUserMsg]);
    setIsSending(true);

    try {
      const payload = { message: text };
      if (currentConversation?.id) {
        payload.conversation_id = currentConversation.id;
      }

      const res = await client.post('/chat/ask', payload);
      
      const assistantMsg = {
        id: res.data.message_id || Date.now().toString() + '-assistant',
        role: 'assistant',
        advice: res.data.advice,
        timestamp: res.data.timestamp,
      };

      setMessages((prev) => [...prev, assistantMsg]);

      // If it's a new conversation, set the current conversation and refresh list
      if (!currentConversation?.id && res.data.conversation_id) {
        setCurrentConversation({
          id: res.data.conversation_id,
          title: text.substring(0, 50) + (text.length > 50 ? '...' : ''),
        });
        fetchConversations();
      }

    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to send message');
      // Remove optimistic message on failure
      setMessages((prev) => prev.filter((msg) => msg.id !== tempId));
    } finally {
      setIsSending(false);
    }
  }, [currentConversation, fetchConversations]);

  const deleteConversation = useCallback(async (id) => {
    try {
      await client.delete(`/chat/conversations/${id}`);
      setConversations((prev) => prev.filter((c) => c.id !== id));
      if (currentConversation?.id === id) {
        startNewChat();
      }
      toast.success('Conversation deleted');
    } catch (error) {
      toast.error('Failed to delete conversation');
    }
  }, [currentConversation, startNewChat]);

  return {
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
  };
};
