import React from 'react';

const Footer = () => {
  return (
    <footer style={footerStyle}>
      <p style={{ margin: 0 }}>© {new Date().getFullYear()} RecruitIQ. All rights reserved.</p>
      <p style={{ margin: '5px 0' }}>Made for internal HR analysis</p>
    </footer>
  );
};

const footerStyle = {
  backgroundColor: '#008080',
  color: 'white',
  textAlign: 'center',
  padding: '10px',
  position: 'fixed',
  bottom: 0,
  width: '100%',
  height: '45px',
};

export default Footer;
