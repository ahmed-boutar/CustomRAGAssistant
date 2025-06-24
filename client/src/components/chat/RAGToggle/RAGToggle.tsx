import React from 'react';
import { Database } from 'lucide-react';
import { useChat } from '../../../hooks/useChat';
import Modal from '../../common/Modal/Modal';
import Button from '../../common/Button/Button';
import styles from './RAGToggle.module.css';

interface RAGToggleProps {
  enabled?: boolean;
  onToggle?: () => void;
}

const RAGToggle: React.FC<RAGToggleProps> = ({ enabled, onToggle }) => {
  const { ragEnabled: hookRagEnabled, setRagEnabled } = useChat();
  const [showModal, setShowModal] = React.useState(false);

  // Use props if provided, otherwise fall back to hook values
  const ragEnabled = enabled !== undefined ? enabled : hookRagEnabled;
  const toggleRag = onToggle || (() => setRagEnabled(!ragEnabled));

  const handleToggle = () => {
    if (!ragEnabled) {
      setShowModal(true);
    } else {
      if (onToggle) {
        onToggle();
      } else {
        setRagEnabled(false);
      }
    }
  };

  const confirmEnableRAG = () => {
    if (onToggle) {
      onToggle();
    } else {
      setRagEnabled(true);
    }
    setShowModal(false);
  };

  const cancelModal = () => {
    setShowModal(false);
  };

  return (
    <>
      <div className={styles.container}>
        <div 
          className={`${styles.toggle} ${ragEnabled ? styles.enabled : ''}`}
          onClick={handleToggle}
        >
          <Database size={16} />
          <span>RAG</span>
          <div className={`${styles.switch} ${ragEnabled ? styles.switchEnabled : ''}`}>
            <div className={styles.switchThumb}></div>
          </div>
        </div>

        {ragEnabled && (
          <div className={styles.status}>
            Document search enabled
          </div>
        )}
      </div>

      <Modal
        isOpen={showModal}
        onClose={cancelModal}
        title="Enable RAG"
      >
        <div className={styles.modalContent}>
          <div className={styles.description}>
            <p>
              Enabling RAG (Retrieval-Augmented Generation) will allow the AI to search
              through your uploaded documents to provide more accurate and contextual responses.
            </p>
          </div>

          <div className={styles.note}>
            <p>
              Note: Make sure you have uploaded documents first for RAG to be effective.
            </p>
          </div>

          <div className={styles.modalActions}>
            <Button onClick={cancelModal} variant="secondary">
              Cancel
            </Button>
            <Button onClick={confirmEnableRAG} variant="primary">
              Enable RAG
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
};

export default RAGToggle;