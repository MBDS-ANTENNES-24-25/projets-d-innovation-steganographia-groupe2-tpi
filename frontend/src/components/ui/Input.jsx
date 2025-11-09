import React, { forwardRef } from 'react';
import '@styles/components/ui/Input.css';

const Input = forwardRef(({ 
  type = 'text', 
  label, 
  placeholder = '', 
  value, 
  onChange, 
  disabled = false, 
  required = false,
  id,
  name,
  className = '',
  options = [], // For select, radio, checkbox groups
  multiple = false, // For select multiple
  rows = 4, // For textarea
  cols = 50, // For textarea
  checked, // For radio and checkbox
  errorMessage = '', // Error message to display
  ...props 
}, ref) => {
  const inputId = id || name || label?.toLowerCase().replace(/\s+/g, '-');

  const renderInput = () => {
    switch (type) {
      case 'select':
        return (
          <select
            ref={ref}
            name={name}
            value={value}
            onChange={onChange}
            disabled={disabled}
            required={required}
            multiple={multiple}
            className={`input-field select-field ${errorMessage && 'error'}`}
            {...props}
          >
            {placeholder && <option value="" disabled>{placeholder}</option>}
            {options.map((option, index) => (
              <option 
                key={option.value || index} 
                value={option.value || option}
              >
                {option.label || option}
              </option>
            ))}
          </select>
        );

      case 'textarea':
        return (
          <textarea
            ref={ref}
            name={name}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            disabled={disabled}
            required={required}
            rows={rows}
            cols={cols}
            className={`input-field textarea-field ${errorMessage && 'error'}`}
            {...props}
          />
        );

      case 'radio':
        return (
          <div className="radio-group">
            {options.map((option, index) => {
              const { checked: _checked, onChange: _onChange, ...restProps } = props;
              return (
                <div key={option.value || index} className="radio-item">
                  <input
                    type="radio"
                    name={name}
                    value={option.value || option}
                    checked={value === (option.value || option)}
                    onChange={onChange || (() => {})}
                    disabled={disabled}
                    required={required}
                    className="radio-input"
                    {...restProps}
                  />
                  <label className="radio-label">
                    {option.label || option}
                  </label>
                </div>
              );
            })}
          </div>
        );

      case 'checkbox':
        if (options.length > 0) {
          // Multiple checkboxes
          return (
            <div className="checkbox-group">
              {options.map((option, index) => {
                const isChecked = Array.isArray(value) 
                  ? value.includes(option.value || option)
                  : false;
                
                return (
                  <div key={option.value || index} className="checkbox-item">
                    <input
                      type="checkbox"
                      name={name}
                      value={option.value || option}
                      checked={isChecked}
                      onChange={(e) => {
                        if (!onChange) return;
                        const currentValue = Array.isArray(value) ? value : [];
                        const optionValue = option.value || option;
                        
                        if (e.target.checked) {
                          onChange({
                            ...e,
                            target: {
                              ...e.target,
                              value: [...currentValue, optionValue]
                            }
                          });
                        } else {
                          onChange({
                            ...e,
                            target: {
                              ...e.target,
                              value: currentValue.filter(v => v !== optionValue)
                            }
                          });
                        }
                      }}
                      disabled={disabled}
                      className="checkbox-input"
                      {...props}
                    />
                    <label className="checkbox-label">
                      {option.label || option}
                    </label>
                  </div>
                );
              })}
            </div>
          );
        } else {
          // Single checkbox
          return (
            <div className="checkbox-item">
              <input
                type="checkbox"
                id={inputId}
                name={name}
                checked={checked || value}
                onChange={onChange}
                disabled={disabled}
                required={required}
                className="checkbox-input"
                {...props}
              />
              <label htmlFor={inputId} className="checkbox-label">
                {placeholder || 'Check this box'}
              </label>
            </div>
          );
        }

      default:
        // Standard input types: text, email, password, number, date, etc.
        return (
          <input
            ref={ref}
            type={type}
            name={name}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            disabled={disabled}
            required={required}
            className={`input-field ${errorMessage && 'error'}`}
            {...props}
          />
        );
    }
  };

  return (
    <div className={`input-group ${type}-group ${className}`}>
      {label && (type !== 'radio' && type !== 'checkbox' || options.length === 0) && (
        <label className="input-label">
          {label}
          {required && <span className="required-asterisk">*</span>}
        </label>
      )}
      {(type === 'radio' || (type === 'checkbox' && options.length > 0)) && label && (
        <fieldset className="fieldset">
          <legend className="input-label">
            {label}
            {required && <span className="required-asterisk">*</span>}
          </legend>
          {renderInput()}
        </fieldset>
      )}
      {(type !== 'radio' && (type !== 'checkbox' || options.length === 0)) && renderInput()}
      {errorMessage && (
        <span className="error-message">
          {errorMessage}
        </span>
      )}
    </div>
  );
});

Input.displayName = 'Input';

export default React.memo(Input);
