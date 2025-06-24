import { useState } from 'react';
import { useChat as useChatContext } from '../context/ChatContext';
import { chatService } from '../services/chat';
import { CHAT_MODELS, DEFAULT_SYSTEM_PROMPT } from '../utils/constants';
import { generateSessionTitle } from '../utils/helpers';

export const useChat = () => {
  const context = useChatContext();
//   const [selectedModel, setSelectedModel] = useState<keyof typeof CHAT_MODELS>('claude-instant');

  const sendMessage = async (message: string) => {
    if (!context.currentSessionId) return;

    const userMessage = {
      role: 'user' as const,
      content: message,
      timestamp: new Date(),
    };

    context.addMessage(userMessage);
    context.setLoading(true);

    const backendModel = CHAT_MODELS[context.selectedModel];
    console.log('SELECTED IN HOOK:', context.selectedModel);
    console.log('Backend model:', backendModel);

    try {
      const response = await chatService.sendMessage({
        model: backendModel,
        system_prompt: DEFAULT_SYSTEM_PROMPT,
        session_id: context.currentSessionId,
        user_input: message,
        enable_rag: context.ragEnabled,
      });

      const assistantMessage = {
        role: 'assistant' as const,
        content: response.response,
        timestamp: new Date(),
      };

      context.addMessage(assistantMessage);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      context.setLoading(false);
    }
  };

  const createNewSession = async (firstMessage?: string) => {
    try {
      const title = firstMessage ? generateSessionTitle(firstMessage) : 'New Chat';
      const session = await chatService.createSession(title);

      // Add to sessions list
      const updatedSessions = [...context.sessions, session];
      context.setSessions(updatedSessions);

      context.setCurrentSession(session.id);
      context.setMessages([]);

      return session;
    } catch (error) {
      console.error('Error creating session:', error);
      throw error;
    }
  };

  const loadSessionMessages = async (sessionId: number) => {
    try {
      context.setLoading(true);
      const messages = await chatService.getSessionMessages(sessionId);
      
      // Convert backend message format to frontend format
      const formattedMessages = messages.map((msg : any) => ({
        role: msg.role,
        content: msg.content,
        timestamp: new Date(msg.created_at),
      }));
      
      context.setMessages(formattedMessages);
      context.setCurrentSession(sessionId);
    } catch (error) {
      console.error('Error loading session messages:', error);
      throw error;
    } finally {
      context.setLoading(false);
    }
  };

  const switchToSession = async (sessionId: number) => {
    // Don't reload if already on this session
    if (context.currentSessionId === sessionId) {
      return;
    }

    await loadSessionMessages(sessionId);
  };

  const toggleRag = () => {
    context.setRagEnabled(!context.ragEnabled);
  };

  const deleteSession = async (sessionId: number) => {
    try {
      await chatService.deleteSession(sessionId);

      // Remove from sessions list
      const updatedSessions = context.sessions.filter(session => session.id !== sessionId);
      context.setSessions(updatedSessions);

      // If we deleted the current session, switch to another session or clear
      if (context.currentSessionId === sessionId) {
        if (updatedSessions.length > 0) {
          // Switch to the most recent session
          const mostRecentSession = updatedSessions[0];
          await loadSessionMessages(mostRecentSession.id);
        } else {
          // No sessions left, clear everything
          context.setCurrentSession(null);
          context.setMessages([]);
        }
      }
    } catch (error) {
      console.error('Error deleting session:', error);
      throw error;
    }
  };

  return {
    ...context,
    // selectedModel,
    // setSelectedModel,
    sendMessage,
    deleteSession,
    createNewSession,
    loadSessionMessages,
    switchToSession,
    toggleRag
  };
};