import React, { createContext, useContext, useReducer } from 'react';
import { ChatMessage, ChatSession } from '../types/chat';
import { CHAT_MODELS } from '../utils/constants';

interface ChatState {
  sessions: ChatSession[];
  currentSessionId: number | null;
  messages: ChatMessage[];
  isLoading: boolean;
  ragEnabled: boolean;
  selectedModel: keyof typeof CHAT_MODELS;
}

interface ChatContextType extends ChatState {
  setCurrentSession: (sessionId: number) => void;
  addMessage: (message: ChatMessage) => void;
  setSessions: (sessions: ChatSession[]) => void;
  setMessages: (messages: ChatMessage[]) => void;
  setLoading: (loading: boolean) => void;
  toggleRag: () => void;
  setRagEnabled: (enabled: boolean) => void;
  setSelectedModel: (model: keyof typeof CHAT_MODELS) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

type ChatAction =
  | { type: 'SET_CURRENT_SESSION'; payload: number }
  | { type: 'ADD_MESSAGE'; payload: ChatMessage }
  | { type: 'SET_SESSIONS'; payload: ChatSession[] }
  | { type: 'SET_MESSAGES'; payload: ChatMessage[] }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'TOGGLE_RAG' }
  | { type: 'SET_RAG_ENABLED'; payload: boolean }
  | { type: 'SET_SELECTED_MODEL'; payload: keyof typeof CHAT_MODELS };

const chatReducer = (state: ChatState, action: ChatAction): ChatState => {
  switch (action.type) {
    case 'SET_CURRENT_SESSION':
      return { ...state, currentSessionId: action.payload };
    case 'ADD_MESSAGE':
      return { ...state, messages: [...state.messages, action.payload] };
    case 'SET_SESSIONS':
      return { ...state, sessions: action.payload };
    case 'SET_MESSAGES':
      return { ...state, messages: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'TOGGLE_RAG':
      return { ...state, ragEnabled: !state.ragEnabled };
    case 'SET_RAG_ENABLED':
      return { ...state, ragEnabled: action.payload };
    case 'SET_SELECTED_MODEL':
      return { ...state, selectedModel: action.payload };
    default:
      return state;
  }
};

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, {
    sessions: [],
    currentSessionId: null,
    messages: [],
    isLoading: false,
    ragEnabled: false,
    selectedModel: 'claude-instant',
  });

  const setCurrentSession = (sessionId: number) => {
    dispatch({ type: 'SET_CURRENT_SESSION', payload: sessionId });
  };

  const addMessage = (message: ChatMessage) => {
    dispatch({ type: 'ADD_MESSAGE', payload: message });
  };

  const setSessions = (sessions: ChatSession[]) => {
    dispatch({ type: 'SET_SESSIONS', payload: sessions });
  };

  const setMessages = (messages: ChatMessage[]) => {
    dispatch({ type: 'SET_MESSAGES', payload: messages });
  };

  const setLoading = (loading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  };

  const toggleRag = () => {
    dispatch({ type: 'TOGGLE_RAG' });
  };

  const setRagEnabled = (enabled: boolean) => {
    dispatch({ type: 'SET_RAG_ENABLED', payload: enabled });
  };

  const setSelectedModel = (model: keyof typeof CHAT_MODELS) => {
    dispatch({ type: 'SET_SELECTED_MODEL', payload: model });
  };

  return (
    <ChatContext.Provider
      value={{
        ...state,
        setCurrentSession,
        addMessage,
        setSessions,
        setMessages,
        setLoading,
        toggleRag,
        setRagEnabled,
        setSelectedModel,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};