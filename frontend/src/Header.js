import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header style={headerStyle}>
      <div>
        <h1 style={{ margin: '0', fontSize: '2.5rem' }}>RecruitIQ</h1>
        <h2 style={{ margin: '5px 0 0', fontWeight: 'normal' }}>Welcome back HRs!</h2>
      </div>
      <nav style={navStyle}>
       <Link to="/Main" style={linkStyle}>Home</Link>
        <Link to="/Profile" style={linkStyle}>Profile</Link>
  <Link
  to="/login"
  style={linkStyle}
  onClick={() => localStorage.removeItem('isAuthenticated')}
>
  Logout
</Link>
      </nav>
    </header>
  );
};

// Styles
const headerStyle = {
  backgroundColor: '#008080',
  padding: '20px',
  color: 'white',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
};

const navStyle = {
  display: 'flex',
  gap: '40px',
};

const linkStyle = {
  color: 'white',
  textDecoration: 'none',
  fontSize: '18px',
  fontWeight: 'bold',
  padding: '3px 6px',
  borderRadius: '2px',
  transition: 'background-color 0.3s ease',
};

export default Header;
