import React from 'react';
import { Plus, MessageCircle, Trash2 } from 'lucide-react';
import { useChat } from '../../../hooks/useChat';
import Button from '../../common/Button/Button';
import { formatDate } from '../../../utils/helpers';
import styles from './Sidebar.module.css';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const { sessions, currentSessionId, setCurrentSession, createNewSession, deleteSession } = useChat();

    const handleNewChat = async () => {
        try {
            const newSession = await createNewSession();
            navigate(`/chat/${newSession.id}`);
        } catch (error) {
        console.error('Failed to create new chat:', error);
        }
    };

    const handleSessionClick = (sessionId: number) => {
        setCurrentSession(sessionId);
        navigate(`/chat/${sessionId}`);
        onClose();
    };

    const formatSessionTitle = (session: any) => {
        // If session has a custom title, use it, otherwise use "Chat #ID"
        if (session.title && session.title !== 'New Chat') {
        return session.title;
        }
        return `Chat #${session.id}`;
    };

    const formatSessionDate = (createdAt: string) => {
        const date = new Date(createdAt);
        const now = new Date();
        const diffTime = Math.abs(now.getTime() - date.getTime());
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) {
        return 'Today';
        } else if (diffDays === 2) {
        return 'Yesterday';
        } else if (diffDays <= 7) {
        return `${diffDays - 1} days ago`;
        } else {
        return date.toLocaleDateString();
        }
    };

    const handleDeleteSession = async (e: React.MouseEvent, sessionId: number) => {
        // Prevent event bubbling to avoid triggering session click
        e.stopPropagation();
        
        try {
            await deleteSession(sessionId);
            
            // If we deleted the current session and no sessions remain, navigate to home
            if (currentSessionId === sessionId && sessions.length === 1) {
                navigate('/');
            }
            // If we deleted the current session but other sessions exist, 
            // the useChat hook will automatically switch to another session
            // and we should navigate to that session
            else if (currentSessionId === sessionId && sessions.length > 1) {
                // Find the next session to navigate to (this will be handled by useChat hook)
                // We'll navigate after the deletion is complete
                setTimeout(() => {
                    const remainingSessions = sessions.filter(s => s.id !== sessionId);
                    if (remainingSessions.length > 0) {
                        navigate(`/chat/${remainingSessions[0].id}`);
                    }
                }, 100);
            }
        } catch (error) {
            console.error('Failed to delete session:', error);
            // You might want to show a toast notification here
        }
    };

    return (
        <>
        {isOpen && <div className={styles.overlay} onClick={onClose} />}
        <div className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}>
            <div className={styles.header}>
            <Button onClick={handleNewChat} className={styles.newChatButton}>
                <Plus size={16} />
                New Chat
            </Button>
            </div>
            
            <div className={styles.sessions}>
                {sessions.map((session) => (
                    <div
                    key={session.id}
                    className={`${styles.session} ${
                        currentSessionId === session.id ? styles.active : ''
                    }`}
                    onClick={() => handleSessionClick(session.id)}
                    >
                    <div className={styles.sessionContent}>
                        <MessageCircle size={16} />
                        <div className={styles.sessionInfo}>
                            <div className={styles.sessionTitle}>
                                {formatSessionTitle(session)}
                            </div>
                            <div className={styles.sessionDate}>
                            {formatSessionDate(session.created_at)}
                            </div>
                        </div>
                    </div>
                    <button 
                    className={styles.deleteButton}
                    onClick={(e) => handleDeleteSession(e, session.id)}
                    title="Delete chat"
                    >
                        <Trash2 size={14} />
                    </button>
                    </div>
                ))}
            </div>
        </div>
        </>
    );
};

export default Sidebar;
