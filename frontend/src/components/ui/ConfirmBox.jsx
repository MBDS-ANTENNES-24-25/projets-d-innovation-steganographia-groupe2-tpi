import React from 'react';
import { Modal, Spinner } from '@components';
import '@styles/components/ui/ConfirmBox.css';

const ConfirmBox = ({
  isOpen,
  onClose,
  onConfirm,
  title = 'Confirm Action',
  message = 'Are you sure you want to proceed?',
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  type = 'default', // 'default', 'danger', 'warning', 'success'
  size = 'sm',
  isLoading = false,
  backdrop = 'default' // 'default', 'static'
}) => {
  const handleConfirm = () => {
    onConfirm();
    if (!isLoading) {
      onClose();
    }
  };

  const getTypeClass = () => {
    switch (type) {
      case 'danger':
        return 'confirm-box-danger';
      case 'warning':
        return 'confirm-box-warning';
      case 'success':
        return 'confirm-box-success';
      default:
        return 'confirm-box-default';
    }
  };

  const getIconByType = () => {
    switch (type) {
      case 'danger':
        return (
          <svg className="confirm-box-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        );
      case 'warning':
        return (
          <svg className="confirm-box-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'success':
        return (
          <svg className="confirm-box-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      default:
        return (
          <svg className="confirm-box-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      size={size}
      closeOnOverlayClick={backdrop !== 'static' && !isLoading}
      showCloseButton={backdrop !== 'static' && !isLoading}
      backdrop={backdrop === 'static' || isLoading ? 'static' : 'default'}
      className="confirm-box-modal"
    >
      <div className="confirm-box-content">
        <div className={`confirm-box-header ${getTypeClass()}`}>
          <div className="confirm-box-icon-container">
            {getIconByType()}
          </div>
        </div>
        
        <div className="confirm-box-body">
          <p className="confirm-box-message">
            {message}
          </p>
        </div>

        <div className="confirm-box-actions">
          <button
            onClick={onClose}
            disabled={isLoading}
            className="btn btn-secondary"
          >
            {cancelText}
          </button>
          <button
            onClick={handleConfirm}
            disabled={isLoading}
            className={`btn ${type === 'default' ? 'btn-primary' : `btn-${type}`}`}
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <Spinner
                  size={4}
                  className="me-2"
                  animate={true}
                />
                Loading...
              </div>
            ) : (
              confirmText
            )}
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default React.memo(ConfirmBox);
