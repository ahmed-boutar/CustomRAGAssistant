import React, { useState, useRef } from 'react';
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react';
import Button from '../../common/Button/Button';
import { uploadService } from '../../../services/upload';
import styles from './DocumentUpload.module.css';

interface UploadedFile {
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  error?: string;
}

const DocumentUpload: React.FC = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const acceptedTypes = ['.txt', '.pdf', '.docx'];
  const maxFileSize = 10 * 1024 * 1024; // 10MB

  const validateFile = (file: File): string | null => {
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!acceptedTypes.includes(extension)) {
      return `File type not supported. Please upload ${acceptedTypes.join(', ')} files.`;
    }
    if (file.size > maxFileSize) {
      return 'File size must be less than 10MB.';
    }
    return null;
  };

  const handleFileSelect = (selectedFiles: FileList | null) => {
    if (!selectedFiles) return;

    const newFiles: UploadedFile[] = Array.from(selectedFiles).map(file => {
      const error = validateFile(file);
      return {
        file,
        status: error ? 'error' : 'pending',
        error: error || undefined
      };
    });

    setFiles(prev => [...prev, ...newFiles]);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const uploadFile = async (index: number) => {
    const file = files[index];
    if (file.status !== 'pending') return;

    setFiles(prev =>
      prev.map((f, i) =>
        i === index ? { ...f, status: 'uploading' } : f
      )
    );

    try {
      await uploadService.uploadDocument(file.file);
      setFiles(prev =>
        prev.map((f, i) =>
          i === index ? { ...f, status: 'success' } : f
        )
      );
    } catch (error) {
      setFiles(prev =>
        prev.map((f, i) =>
          i === index
            ? {
                ...f,
                status: 'error',
                error: error instanceof Error ? error.message : 'Upload failed'
              }
            : f
        )
      );
    }
  };

  const uploadAllFiles = async () => {
    const pendingFiles = files
      .map((file, index) => ({ file, index }))
      .filter(({ file }) => file.status === 'pending');

    await Promise.all(
      pendingFiles.map(({ index }) => uploadFile(index))
    );
  };

  const getStatusIcon = (status: UploadedFile['status']) => {
    switch (status) {
      case 'success':
        return <CheckCircle size={16} className={styles.successIcon} />;
      case 'error':
        return <AlertCircle size={16} className={styles.errorIcon} />;
      case 'uploading':
        return <div className={styles.spinner} />;
      default:
        return <File size={16} className={styles.fileIcon} />;
    }
  };

  const pendingCount = files.filter(f => f.status === 'pending').length;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>Upload Documents</h2>
        <p className={styles.description}>
          Upload your documents to enhance your AI assistant with relevant context.
          Supported formats: {acceptedTypes.join(', ')}
        </p>
      </div>

      <div
        className={`${styles.dropzone} ${isDragOver ? styles.dragOver : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <Upload size={48} className={styles.uploadIcon} />
        <p className={styles.dropzoneText}>
          <span className={styles.dropzoneAction}>Click to upload</span> or drag and drop
        </p>
        <p className={styles.dropzoneSubtext}>
          {acceptedTypes.join(', ')} files up to 10MB
        </p>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept={acceptedTypes.join(',')}
        onChange={(e) => handleFileSelect(e.target.files)}
        className={styles.hiddenInput}
      />

      {files.length > 0 && (
        <div className={styles.filesList}>
          <div className={styles.filesHeader}>
            <h3 className={styles.filesTitle}>Selected Files ({files.length})</h3>
            {pendingCount > 0 && (
              <Button
                onClick={uploadAllFiles}
                variant="primary"
                size="sm"
              >
                Upload All ({pendingCount})
              </Button>
            )}
          </div>

          <div className={styles.files}>
            {files.map((uploadedFile, index) => (
              <div key={index} className={styles.fileItem}>
                <div className={styles.fileInfo}>
                  {getStatusIcon(uploadedFile.status)}
                  <div className={styles.fileDetails}>
                    <span className={styles.fileName}>{uploadedFile.file.name}</span>
                    <span className={styles.fileSize}>
                      {(uploadedFile.file.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>
                </div>

                <div className={styles.fileActions}>
                  {uploadedFile.status === 'pending' && (
                    <Button
                      onClick={() => uploadFile(index)}
                      variant="secondary"
                      size="sm"
                    >
                      Upload
                    </Button>
                  )}
                  <button
                    onClick={() => removeFile(index)}
                    className={styles.removeButton}
                  >
                    <X size={16} />
                  </button>
                </div>

                {uploadedFile.error && (
                  <div className={styles.errorMessage}>
                    {uploadedFile.error}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;