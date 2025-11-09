import React from 'react';
import DashboardLayout from '../layouts/DashboardLayout';

const Profile = () => {
  
  return (
    <DashboardLayout
      title="Profile Settings"
      titleDescription="Manage your account information and preferences"
    >
      <div className="glassmorphic-card">

      </div>
    </DashboardLayout>
  );
};

export default React.memo(Profile);
