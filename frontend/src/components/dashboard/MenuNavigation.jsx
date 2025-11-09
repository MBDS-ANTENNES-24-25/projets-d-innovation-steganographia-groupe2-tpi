import React from 'react';
import { Link } from 'react-router-dom';
import '@styles/components/dashboard/MenuNavigation.css';

const MenuNavigation = ({ menuItems, activeMenu }) => {
    return (
        <div className="menu-navigation">
            <div className="menu-container">
                {menuItems.map((menu) => (
                    <Link
                        key={menu.id}
                        to={menu.path}
                        className={`menu-item ${activeMenu === menu.id ? 'active' : ''}`}
                    >
                        <span className="menu-label">{menu.label}</span>
                    </Link>
                ))}
            </div>
        </div>
    );
};

export default React.memo(MenuNavigation);
