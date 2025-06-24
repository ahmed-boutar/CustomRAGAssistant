import React, { useState } from 'react';
import { useAuth } from '../../../hooks/useAuth';
import Button from '../../common/Button/Button';
import Input from '../../common/Input/Input';
import styles from './RegisterForm.module.css';

interface RegisterFormProps {
  onSwitchToLogin: () => void;
}

const RegisterForm: React.FC<RegisterFormProps> = ({ onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
  });
  const [error, setError] = useState('');
  const { register, isLoading } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      await register({
        email: formData.email,
        password: formData.password,
        first_name: formData.first_name,
        last_name: formData.last_name,
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Sign Up</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.nameRow}>
          <Input
            type="text"
            name="first_name"
            label="First Name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
          <Input
            type="text"
            name="last_name"
            label="Last Name"
            value={formData.last_name}
            onChange={handleChange}
            required
          />
        </div>
        <Input
          type="email"
          name="email"
          label="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <Input
          type="password"
          name="password"
          label="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <Input
          type="password"
          name="confirmPassword"
          label="Confirm Password"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
        {error && <div className={styles.error}>{error}</div>}
        <Button type="submit" isLoading={isLoading}>
          Sign Up
        </Button>
      </form>
      <p className={styles.switchText}>
        Already have an account?{' '}
        <button type="button" onClick={onSwitchToLogin} className={styles.switchButton}>
          Sign In
        </button>
      </p>
    </div>
  );
};

export default RegisterForm;