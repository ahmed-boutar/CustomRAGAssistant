import { apiService } from './api';
import { ChatRequest, ChatResponse, ChatSession, ChatMessage } from '../types/chat';

export const chatService = {
  sendMessage: (request: ChatRequest): Promise<ChatResponse> =>
    apiService.post<ChatResponse>('/chat/', request).then(res => res.data),

  getSessions: (): Promise<ChatSession[]> =>
    apiService.get<ChatSession[]>('/sessions/').then(res => res.data),

  createSession: (title: string): Promise<ChatSession> =>
    apiService.post<ChatSession>('/sessions/', { title }).then(res => res.data),

  getSessionMessages: (sessionId: number): Promise<ChatMessage[]> =>
    apiService.get<ChatMessage[]>(`/sessions/${sessionId}/messages/`).then(res => res.data),

  deleteSession: (sessionId: number): Promise<void> =>
    apiService.delete<void>(`/sessions/${sessionId}/`).then(() => {}),
};