import React from 'react';

const ImageIcon = ({ width = 64, height = 64, color = 'currentColor' }) => (
  <svg width={width} height={height} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="3" y="3" width="18" height="18" rx="2" stroke={color} strokeWidth="1" fill="rgba(255,255,255,0.1)" />
    <circle cx="8.5" cy="8.5" r="1.5" fill={color} />
    <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" stroke={color} strokeWidth="1" />
  </svg>
);

export default React.memo(ImageIcon);
