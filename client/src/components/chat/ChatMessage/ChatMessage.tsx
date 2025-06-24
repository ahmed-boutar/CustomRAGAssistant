import React from 'react';
import { User, Bot } from 'lucide-react';
import { ChatMessage as ChatMessageType } from '../../../types/chat';
import { formatDate } from '../../../utils/helpers';
import styles from './ChatMessage.module.css';

interface ChatMessageProps {
  message: ChatMessageType;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`${styles.message} ${isUser ? styles.user : styles.assistant}`}>
      <div className={styles.avatar}>
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      <div className={styles.content}>
        <div className={styles.text}>
          {message.content}
        </div>
        <div className={styles.timestamp}>
          {formatDate(message.timestamp)}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;