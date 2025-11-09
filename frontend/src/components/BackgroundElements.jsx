import React from 'react';
import '@styles/components/BackgroundElements.css';

const BackgroundElements = () => {
  return (
    <div className="background-elements">
      <div className='relative size-full'>
        {/* 3D Pixel Sequences */}
        {Array.from({length: 2}, (_, index) => (
          <div key={index} className={`pixel-sequence pixel-sequence-${index + 1}`}>
            <div className="pixel-grid">
              {Array.from({length: 256}, (_, i) => (
                <div key={i} className="pixel"></div>
              ))}
            </div>
          </div>
        ))}

        {/* 3D Image Representations */}
        {Array.from({length: 2}, (_, index) => (
          <div key={index} className={`floating-image image-${index + 1}`}></div>
        ))}
      </div>
    </div>
  );
};

export default React.memo(BackgroundElements);
