import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Bot } from 'lucide-react';
import { useChat } from '../../../hooks/useChat';
import { CHAT_MODELS } from '../../../utils/constants';
import styles from './ModelSelector.module.css';

interface Model {
  id: keyof typeof CHAT_MODELS;
  name: string;
  displayName: string;
}

const AVAILABLE_MODELS: Model[] = [
  {
    id: 'claude-instant',
    name: 'claude-instant',
    displayName: 'Claude Instant'
  },
  {
    id: 'titan-text-g1',
    name: 'titan-text-g1',
    displayName: 'Amazon Titan'
  }
];

const ModelSelector: React.FC = () => {
  const { selectedModel, setSelectedModel } = useChat();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  console.log('\nselectedModel in ModelSelector:', selectedModel);
  console.log('Backend model will be:', CHAT_MODELS[selectedModel]);

  const currentModel = AVAILABLE_MODELS.find(model => 
    model.id === selectedModel
  ) || AVAILABLE_MODELS[0];

  const handleModelSelect = (model: Model) => {
    setSelectedModel(model.id);
    setIsOpen(false);
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className={styles.container} ref={dropdownRef}>
      <button
        className={styles.trigger}
        onClick={toggleDropdown}
        type="button"
      >
        <Bot size={16} />
        <span className={styles.modelName}>{currentModel.displayName}</span>
        <ChevronDown 
          size={14} 
          className={`${styles.chevron} ${isOpen ? styles.chevronOpen : ''}`}
        />
      </button>

      {isOpen && (
        <div className={styles.dropdown}>
          {AVAILABLE_MODELS.map((model) => (
            <button
              key={model.id}
              className={`${styles.option} ${
                currentModel.id === model.id ? styles.selected : ''
              }`}
              onClick={() => handleModelSelect(model)}
              type="button"
            >
              <Bot size={14} />
              <span>{model.displayName}</span>
              {currentModel.id === model.id && (
                <div className={styles.selectedIndicator}>●</div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default ModelSelector;