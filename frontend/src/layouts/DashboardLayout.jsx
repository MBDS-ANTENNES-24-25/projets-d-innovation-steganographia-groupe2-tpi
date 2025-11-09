import React from 'react';
import Navbar from '../components/dashboard/Navbar';
import BackgroundElements from '../components/BackgroundElements';
import MenuNavigation from '../components/dashboard/MenuNavigation';
import { useLocation } from 'react-router-dom';
import '@styles/layouts/DashboardLayout.css';

const DashboardLayout = ({ children, title, titleDescription }) => {
  const location = useLocation();

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', path: '/dashboard' },
    { id: 'sign-image', label: 'Sign Image', path: '/sign-image' },
    { id: 'verify-image', label: 'Verify Image', path: '/verify-image' },
    { id: 'my-signatures', label: 'My Signatures', path: '/my-signatures' },
    { id: 'my-verifications', label: 'My Verifications', path: '/my-verifications' }
  ];

  const activeMenuItem = menuItems.find(item => item.path === location.pathname)?.id;

  return (
    <>
    <div className='size-full fixed overflow-hidden'>
      <BackgroundElements />
    </div>
    <div className='size-full fixed overflow-y-auto z-1'>
      <div className="dashboard-layout">
        <div className="dashboard-header">
          <Navbar />
          <MenuNavigation 
            menuItems={menuItems} 
            activeMenu={activeMenuItem}
          />
        </div>
        <main className="dashboard-content">
          <div className="page-title">
            <h1>{ title }</h1>
            <p>{ titleDescription }</p>
          </div>
          {children}
        </main>
      </div>
    </div>
    </>
  );
};

export default React.memo(DashboardLayout);
