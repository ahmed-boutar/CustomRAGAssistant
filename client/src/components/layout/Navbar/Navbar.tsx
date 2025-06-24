import React from 'react';
import { useAuth } from '../../../hooks/useAuth';
import { LogOut, Menu, Upload } from 'lucide-react';
import Button from '../../common/Button/Button';
import ModelSelector from '../../chat/ModelSelector/ModelSelector';
import styles from './Navbar.module.css';

interface NavbarProps {
  onToggleSidebar: () => void;
  onNavigateToUpload: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onToggleSidebar, onNavigateToUpload }) => {
  const { user, logout } = useAuth();

  return (
    <nav className={styles.navbar}>
      <div className={styles.left}>
        <button onClick={onToggleSidebar} className={styles.menuButton}>
          <Menu size={20} />
        </button>
        <h1 className={styles.title}>RAG Assistant</h1>
      </div>
      
      <div className={styles.center}>
        <ModelSelector />
      </div>
      
      <div className={styles.right}>
        <Button variant="ghost" size="sm" onClick={onNavigateToUpload}>
          <Upload size={16} />
          Upload
        </Button>
        <span className={styles.userInfo}>
          {user?.first_name} {user?.last_name}
        </span>
        <Button variant="ghost" size="sm" onClick={logout}>
          <LogOut size={16} />
          Sign Out
        </Button>
      </div>
    </nav>
  );
};

export default Navbar;