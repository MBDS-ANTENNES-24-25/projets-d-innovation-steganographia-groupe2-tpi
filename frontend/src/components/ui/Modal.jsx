import React from 'react';
import { createPortal } from 'react-dom';
import '@styles/components/ui/Modal.css';

const Modal = ({ 
  isOpen, 
  onClose, 
  children, 
  title, 
  size = 'md',
  showCloseButton = true,
  closeOnOverlayClick = true,
  backdrop = 'default', // 'default', 'static'
  className = ''
}) => {
  const handleOverlayClick = (e) => {
    if (backdrop === 'static') {
      // Add shake animation for static backdrop
      const modalContainer = e.currentTarget.querySelector('.modal-container');
      if (modalContainer) {
        modalContainer.classList.add('modal-shake');
        setTimeout(() => {
          modalContainer.classList.remove('modal-shake');
        }, 300);
      }
      return;
    }
    
    if (closeOnOverlayClick && e.target === e.currentTarget) {
      onClose();
    }
  };

  React.useEffect(() => {
    const handleEscapeKey = (e) => {
      if (e.key === 'Escape' && backdrop !== 'static') {
        onClose();
      } else if (e.key === 'Escape' && backdrop === 'static') {
        // Add shake animation for static backdrop
        const modalContainer = document.querySelector('.modal-container');
        if (modalContainer) {
          modalContainer.classList.add('modal-shake');
          setTimeout(() => {
            modalContainer.classList.remove('modal-shake');
          }, 300);
        }
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscapeKey);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose, backdrop]);

  if (!isOpen) return null;

  const modalContent = (
    <div 
      className="modal-overlay"
      onClick={handleOverlayClick}
    >
      <div 
        className={`modal-container glassmorphic-card ${`w-${size}`} ${className}`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        {(title || showCloseButton) && (
          <div className="modal-header">
            {title && (
              <h2 className="modal-title">
                {title}
              </h2>
            )}
            <button
              onClick={onClose}
              className="modal-close-button"
              aria-label="Close modal"
            >
              <svg 
                className="modal-close-icon" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M6 18L18 6M6 6l12 12" 
                />
              </svg>
            </button>
          </div>
        )}

        {/* Content */}
        <div className="modal-content">
          {children}
        </div>
      </div>
    </div>
  );

  return createPortal(modalContent, document.body);
};

export default Modal;
