import React from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import '@styles/pages/Dashboard.css';

const Dashboard = () => {

  return (
    <DashboardLayout
      title="Welcome to SteganographIA"
      titleDescription="Your secure platform for digital steganography and hidden message management."
    >
        <div className="glassmorphic-card" style={{ height: '9000px' }}>
        </div>
    </DashboardLayout>
  );
};

export default React.memo(Dashboard);
