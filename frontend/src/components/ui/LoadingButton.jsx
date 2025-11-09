import React, {useState, useEffect, useRef } from 'react';
import Spinner from './Spinner';

const LoadingButton = ({ 
  loading = false, 
  loadingText = "Loading...", 
  defaultText = "Submit",
  className = "", 
  disabled = false,
  spinnerSize = 4,
  type = "button",
  ...props 
}) => {

    const buttonElement = useRef(null);
    const [textColor, setTextColor] = useState("");

    useEffect(() => {
        if (buttonElement.current) {
            const styles = window.getComputedStyle(buttonElement.current);
            setTextColor(styles.color);
        }
    }, [className, loading]);

return (
    <button 
        type={type}
        className={`${loading ? "opacity-80" : ""} ${className}`}
        disabled={loading || disabled}
        {...props}
        ref={buttonElement}
    >
        {loading ? (
            <div className="flex items-center justify-center">
                <Spinner size={spinnerSize} className={`me-2`} animate style={{ color: textColor }} />
                {loadingText}
            </div>
        ) : (
            defaultText
        )}
    </button>
);
};

export default React.memo(LoadingButton);
