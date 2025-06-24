import React, { useState, useEffect } from 'react';
import { useChat } from '../../hooks/useChat';
import Layout from '../../components/layout/Layout/Layout';
import ChatInterface from '../../components/chat/ChatInterface/ChatInterface';
import { chatService } from '../../services/chat';
import styles from './ChatPage.module.css';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const ChatPage: React.FC = () => {
    const { sessionId } = useParams<{ sessionId?: string }>();
    const navigate = useNavigate();
    const { setSessions, sessions, currentSessionId, switchToSession } = useChat();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const loadSessions = async () => {
        try {
            const sessionsData = await chatService.getSessions();
            setSessions(sessionsData);

            // If we have a sessionId in URL but no sessions loaded yet, wait for them
            if (sessionId && sessionsData.length > 0) {
            const targetSessionId = parseInt(sessionId);
            const sessionExists = sessionsData.find(s => s.id === targetSessionId);
            
            if (sessionExists) {
                await switchToSession(targetSessionId);
            } else {
                // Session doesn't exist, redirect to chat page without session
                navigate('/chat');
            }
            } else if (!sessionId && sessionsData.length > 0) {
            // No session in URL, redirect to the first session
            navigate(`/chat/${sessionsData[0].id}`);
            }
        } catch (error) {
            console.error('Error loading sessions:', error);
        } finally {
            setIsLoading(false);
        }
        };

        loadSessions();
    }, []);

    useEffect(() => {
    if (sessionId && sessions.length > 0) {
      const targetSessionId = parseInt(sessionId);
      
      // Only switch if it's different from current session
      if (currentSessionId !== targetSessionId) {
        const sessionExists = sessions.find(s => s.id === targetSessionId);
        if (sessionExists) {
          switchToSession(targetSessionId);
        }
      }
    }
  }, [sessionId, sessions, currentSessionId, switchToSession]);

  if (isLoading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.spinner} />
        <p className={styles.loadingText}>Loading your conversations...</p>
      </div>
    );
  }

  return (
    <Layout>
      <ChatInterface />
    </Layout>
  );
};

export default ChatPage;