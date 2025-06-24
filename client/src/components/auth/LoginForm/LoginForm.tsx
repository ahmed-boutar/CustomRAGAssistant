import React, { useState } from 'react';
import { useAuth } from '../../../hooks/useAuth';
import Button from '../../common/Button/Button';
import Input from '../../common/Input/Input';
import styles from './LoginForm.module.css';

interface LoginFormProps {
  onSwitchToRegister: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onSwitchToRegister }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, isLoading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await login({ email, password });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Sign In</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <Input
          type="email"
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Input
          type="password"
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <div className={styles.error}>{error}</div>}
        <Button type="submit" isLoading={isLoading}>
          Sign In
        </Button>
      </form>
      <p className={styles.switchText}>
        Don't have an account?{' '}
        <button type="button" onClick={onSwitchToRegister} className={styles.switchButton}>
          Sign Up
        </button>
      </p>
    </div>
  );
};

export default LoginForm;