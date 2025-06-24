export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const CHAT_MODELS = {
  'claude-instant': 'claude',
  'titan-text-g1': 'titan'
};

export const DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant.";

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user'
} as const;