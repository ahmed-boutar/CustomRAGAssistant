import React from 'react';
import Layout from '../../components/layout/Layout/Layout';
import DocumentUpload from '../../components/upload/DocumentUpload/DocumentUpload';
import styles from './UploadPage.module.css';

const UploadPage: React.FC = () => {
  return (
    <Layout>
      <div className={styles.container}>
        <DocumentUpload />
      </div>
    </Layout>
  );
};

export default UploadPage;