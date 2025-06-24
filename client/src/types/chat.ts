export interface ChatMessage {
  id?: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatSession {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ChatRequest {
  model: string;
  system_prompt?: string;
  session_id: number;
  user_input: string;
  enable_rag?: boolean;
}

export interface ChatResponse {
  response: string;
}