import React, { useEffect, useRef } from 'react';
import { useChat } from '../../../hooks/useChat';
import ChatMessage from '../ChatMessage/ChatMessage';
import ChatInput from '../ChatInput/ChatInput';
import RAGToggle from '../RAGToggle/RAGToggle';
import { MessageCircle } from 'lucide-react';
import styles from './ChatInterface.module.css';

const ChatInterface: React.FC = () => {
  const {
    messages,
    isLoading,
    ragEnabled,
    toggleRag,
    sendMessage,
    currentSessionId
  } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    await sendMessage(message);
  };

  if (!currentSessionId) {
    return (
      <div className={styles.emptyState}>
        <MessageCircle size={48} className={styles.emptyIcon} />
        <h2 className={styles.emptyTitle}>No Chat Session Selected</h2>
        <p className={styles.emptyDescription}>
          Create a new chat session to start a conversation with your AI assistant.
        </p>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <RAGToggle
          enabled={ragEnabled}
          onToggle={toggleRag}
        />
      </div>

      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div className={styles.welcomeMessage}>
            <MessageCircle size={32} className={styles.welcomeIcon} />
            <p className={styles.welcomeText}>
              Start a conversation with your AI assistant. 
              {ragEnabled && " RAG is enabled - your documents will be used to enhance responses."}
            </p>
          </div>
        ) : (
          <div className={styles.messagesList}>
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                message={message}
                // isLast={index === messages.length - 1}
              />
            ))}
            {isLoading && (
              <div className={styles.typingIndicator}>
                <div className={styles.typingDots}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <ChatInput
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        placeholder="Ask me anything..."
      />
    </div>
  );
};

export default ChatInterface;