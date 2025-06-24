import React, { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import LoginForm from '../../components/auth/LoginForm/LoginForm';
import RegisterForm from '../../components/auth/RegisterForm/RegisterForm';
import Button from '../../components/common/Button/Button';
import styles from './AuthPage.module.css';

const AuthPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h1 className={styles.title}>
            {isLogin ? 'Welcome Back' : 'Create Account'}
          </h1>
          <p className={styles.subtitle}>
            {isLogin
              ? 'Sign in to your AI assistant'
              : 'Join us and create your personalized AI assistant'
            }
          </p>
        </div>

        <div className={styles.form}>
          {isLogin ? <LoginForm /> : <RegisterForm />}
        </div>

        <div className={styles.footer}>
          <p className={styles.switchText}>
            {isLogin ? "Don't have an account?" : 'Already have an account?'}
          </p>
          <Button
            variant="ghost"
            onClick={() => setIsLogin(!isLogin)}
            className={styles.switchButton}
          >
            {isLogin ? 'Sign up' : 'Sign in'}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;