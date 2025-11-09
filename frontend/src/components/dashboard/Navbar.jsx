import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { Logo, ConfirmBox } from '@components';
import { useAtom } from 'jotai';
import { logout } from '@api/authApi';
import { userInfoAtom, logoutAtom } from '@atoms/authAtoms';
import '@styles/components/dashboard/Navbar.css';

const Navbar = () => {
  const [, setLogout] = useAtom(logoutAtom);
  const [userInfo] = useAtom(userInfoAtom);
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const navigate = useNavigate();

  const handleConfirmLogout = async () => {
    await logout();
    setLogout();
    setIsModalOpen(false);
    navigate('/login');
  };

  const handleLogoutClick = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Logo size={2} />
        <div className="navbar-menu">
          <div className="navbar-user">
            <span className="user-name">{userInfo?.username}</span>
            <div className="user-avatar">
              <Link to="/profile" className="user-profile-link">
                  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="16" cy="12" r="5" fill="rgba(128, 128, 128, 0.6)"/>
                    <path d="M6 28c0-5.5 4.5-10 10-10s10 4.5 10 10 L26 38 L6 38 Z" fill="rgba(128, 128, 128, 0.6)"/>
                  </svg>
              </Link>
            </div>
            <button className="btn btn-primary" onClick={handleLogoutClick}>Logout</button>
          </div>
        </div>
      </div>
      <ConfirmBox
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        size="lg"
        title="Confirm Logout"
        type="danger"
        confirmText="Logout"
        message="Are you sure you want to logout?"
        onConfirm={handleConfirmLogout}
      />
    </nav>
  );
};

export default React.memo(Navbar);
