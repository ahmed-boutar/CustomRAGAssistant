import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../Navbar/Navbar';
import Sidebar from '../Sidebar/Sidebar';
import styles from './Layout.module.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  const navigateToUpload = () => {
    navigate('/upload');
  };

  return (
    <div className={styles.layout}>
      <Navbar onToggleSidebar={toggleSidebar} onNavigateToUpload={navigateToUpload} />
      <div className={styles.content}>
        <Sidebar isOpen={sidebarOpen} onClose={closeSidebar} />
        <main className={styles.main}>
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;