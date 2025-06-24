import { apiService } from './api';
import { LoginRequest, RegisterRequest, AuthResponse, User } from '../types/auth';

export const authService = {
  login: (credentials: LoginRequest): Promise<AuthResponse> =>
    apiService.post<AuthResponse>('/auth/login', credentials).then(res => res.data),

  register: (userData: RegisterRequest): Promise<User> =>
    apiService.post<User>('/auth/register', userData).then(res => res.data),

  getCurrentUser: (): Promise<User> =>
    apiService.get<User>('/auth/me').then(res => res.data),

  logout: (refreshToken: string): Promise<void> =>
    apiService.post('/auth/logout', { refresh_token: refreshToken }).then(() => {}),
};