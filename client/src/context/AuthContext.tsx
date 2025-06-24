import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { User, AuthState, LoginRequest, RegisterRequest } from '../types/auth';
import { authService } from '../services/auth';
import { storage } from '../utils/storage';
import { STORAGE_KEYS } from '../utils/constants';

interface AuthContextType extends AuthState {
  login: (credentials: LoginRequest) => Promise<void>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

type AuthAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_USER'; payload: User }
  | { type: 'CLEAR_USER' };

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
      };
    case 'CLEAR_USER':
      return {
        user: null,
        isAuthenticated: false,
        isLoading: false,
      };
    default:
      return state;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    isAuthenticated: false,
    isLoading: true,
  });

  useEffect(() => {
    const initializeAuth = async () => {
      const token = storage.get(STORAGE_KEYS.ACCESS_TOKEN);
      const userData = storage.get(STORAGE_KEYS.USER);

      if (token && userData) {
        try {
          const user = JSON.parse(userData);
          dispatch({ type: 'SET_USER', payload: user });
        } catch {
          storage.clear();
          dispatch({ type: 'CLEAR_USER' });
        }
      } else {
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    initializeAuth();
  }, []);

  const login = async (credentials: LoginRequest) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const authResponse = await authService.login(credentials);
      storage.set(STORAGE_KEYS.ACCESS_TOKEN, authResponse.access_token);
      storage.set(STORAGE_KEYS.REFRESH_TOKEN, authResponse.refresh_token);

      const user = await authService.getCurrentUser();
      storage.set(STORAGE_KEYS.USER, JSON.stringify(user));
      dispatch({ type: 'SET_USER', payload: user });
    } catch (error) {
      dispatch({ type: 'SET_LOADING', payload: false });
      throw error;
    }
  };

  const register = async (userData: RegisterRequest) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      await authService.register(userData);
      await login({ email: userData.email, password: userData.password });
    } catch (error) {
      dispatch({ type: 'SET_LOADING', payload: false });
      throw error;
    }
  };

  const logout = () => {
    const refreshToken = storage.get(STORAGE_KEYS.REFRESH_TOKEN);
    if (refreshToken) {
      authService.logout(refreshToken).catch(() => {});
    }
    storage.clear();
    dispatch({ type: 'CLEAR_USER' });
  };

  return (
    <AuthContext.Provider value={{ ...state, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
