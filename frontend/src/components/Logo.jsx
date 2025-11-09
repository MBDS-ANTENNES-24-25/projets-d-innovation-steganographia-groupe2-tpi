import React from 'react';

const Logo = ({ size = 2 }) => (
  <div className={`steganographia-logo text-${ size }xl`}>
    <p>SteganographIA</p>
  </div>
);

export default React.memo(Logo);
