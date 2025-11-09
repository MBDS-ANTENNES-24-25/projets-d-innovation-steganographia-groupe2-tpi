import React from 'react';
import '@styles/components/ui/DropzoneContent.css';

const DropzoneContent = ({
  UploadIconComponent,
  dropzoneText = null,
  dropzoneSubtext = null,
  animateIcon = false
}) => (
  <div>
    <div className={`upload-icon ${animateIcon ? 'animate' : ''}`}>
      {UploadIconComponent && UploadIconComponent}
    </div>
    <div>
      {dropzoneText && (
        <p className="dropzone-text">
          {dropzoneText}
        </p>
      )}
      {dropzoneSubtext && (
        <p className="dropzone-subtext">
          {dropzoneSubtext}
        </p>
      )}
    </div>
  </div>
);

export default React.memo(DropzoneContent);
