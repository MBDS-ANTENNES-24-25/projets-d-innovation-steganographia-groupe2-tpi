import React, { useState, useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import ReactDOM from 'react-dom';
import { DropzoneContent, ImageIcon } from '@components';
import '@styles/components/ui/FileUpload.css';

const FileUpload = ({ 
  enableGlobalDrop = false,
  onFileSelect, 
  onError, 
  acceptedTypes = { '*/*': [] },
  maxFiles = 1,
  className = ""
}) => {
  const [isDragOverPage, setIsDragOverPage] = useState(false);
  const supportedFormats = Object.values(acceptedTypes).flat().join(', ');

  
  // Fonction appelée quand des fichiers sont déposés ou sélectionnés
  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    // Vérifier s'il y a des fichiers rejetés
    if (rejectedFiles.length > 0) {
      onError && onError(`Please select only supported file types (${supportedFormats})`);
      return;
    }

    // Vérifier s'il y a des fichiers acceptés
    if (acceptedFiles.length > 0) {
      if (maxFiles > 1) {
        onFileSelect && onFileSelect(acceptedFiles);
      } else {
        onFileSelect && onFileSelect(acceptedFiles[0]);
      }
    }
  }, [onError, supportedFormats, maxFiles, onFileSelect]);

  // Configuration de react-dropzone
  const {
    getRootProps,
    getInputProps,
    isDragActive
  } = useDropzone({
    onDrop,
    accept: acceptedTypes,
    maxFiles: maxFiles > 1 ? maxFiles : 1,
    multiple: maxFiles > 1
  });

  // Gestionnaires d'événements globaux pour le drag & drop sur toute la page
  useEffect(() => {
    if (!enableGlobalDrop) return;

    let dragCounter = 0;

    const handleDragEnter = (e) => {
      e.preventDefault();
      dragCounter++;
      if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
        setIsDragOverPage(true);
      }
    };

    const handleDragLeave = (e) => {
      e.preventDefault();
      dragCounter--;
      if (dragCounter === 0) {
        setIsDragOverPage(false);
      }
    };

    const handleDragOver = (e) => {
      e.preventDefault();
    };

    const handleDrop = (e) => {
      e.preventDefault();
      dragCounter = 0;
      setIsDragOverPage(false);
      
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        const files = Array.from(e.dataTransfer.files);
        const supportedFiles = files.filter(file => {
          return Object.keys(acceptedTypes).some(type => file.type === type);
        });
        const rejectedFiles = files.filter(file => {
          return !Object.keys(acceptedTypes).some(type => file.type === type);
        });
        
        onDrop(supportedFiles, rejectedFiles.map(file => ({ file })));
        e.dataTransfer.clearData();
      }
    };

    // Ajouter les événements globalement
    document.addEventListener('dragenter', handleDragEnter);
    document.addEventListener('dragleave', handleDragLeave);
    document.addEventListener('dragover', handleDragOver);
    document.addEventListener('drop', handleDrop);

    // Nettoyage des événements
    return () => {
      document.removeEventListener('dragenter', handleDragEnter);
      document.removeEventListener('dragleave', handleDragLeave);
      document.removeEventListener('dragover', handleDragOver);
      document.removeEventListener('drop', handleDrop);
    };
  }, [onDrop, acceptedTypes, enableGlobalDrop]);

  const getFileText = () => maxFiles > 1 ? 'files' : 'file';

  return (
    <>
      {/* Global overlay for drag & drop on the entire page */}
      {enableGlobalDrop && isDragOverPage &&
        ReactDOM.createPortal(
          <div className="global-drag-overlay">
            <DropzoneContent 
              UploadIconComponent={<ImageIcon width={100} height={100} />}
              animateIcon={true}
              dropzoneText={`Drop your ${getFileText()} anywhere on the page`}
              dropzoneSubtext={`Supported formats: ${supportedFormats}`}
            />
          </div>,
          document.body
        )}

      {/* Drag and drop zone */}
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'drag-active' : ''} ${className}`}
      >
        <input {...getInputProps()} />
        <DropzoneContent 
          UploadIconComponent={<ImageIcon width={80} height={80} />}
          animateIcon={isDragActive}
          dropzoneText={`${isDragActive ? 'Drop' : 'Drag & drop'} your ${getFileText()} here`}
          dropzoneSubtext={`Supported formats: ${supportedFormats}`}
        />
      </div>
    </>
  );
};

export default React.memo(FileUpload);
