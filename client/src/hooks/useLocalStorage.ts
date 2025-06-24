import { useState } from 'react';
import { storage } from '../utils/storage';

export const useLocalStorage = <T>(key: string, initialValue: T): [T, (value: T) => void] => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = storage.get(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    try {
      setStoredValue(value);
      storage.set(key, JSON.stringify(value));
    } catch {
      // Silently fail
    }
  };

  return [storedValue, setValue];
};