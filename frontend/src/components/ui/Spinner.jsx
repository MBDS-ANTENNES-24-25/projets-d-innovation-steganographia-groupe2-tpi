import React from 'react';
import '@styles/components/ui/Spinner.css';

const Spinner = ({ size = 4, className = '', animate = true, style = {} }) => {
    return (
        <svg 
            className={`box-spinner me-2 !size-${size} ${animate ? 'animate-spin' : ''} ${className}`} 
            viewBox="0 0 24 24"
            style={style}
        >
            <circle 
                className="box-spinner-circle" 
                cx="12" 
                cy="12" 
                r="10" 
                stroke="currentColor" 
                strokeWidth="4"
                fill="none"
            />
            <path 
                className="box-spinner-path" 
                fill="currentColor" 
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
        </svg>
    );
};

export default React.memo(Spinner);
