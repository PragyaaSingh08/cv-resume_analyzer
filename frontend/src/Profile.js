import react from 'react';
import { useLocation } from 'react-router-dom';
const Profile = () =>{
      const user = {
    name: 'Pragya Singh',
    email: 'hr@recruitiq.com',
    company: 'RecruitIQ',
    role: 'HR Manager',
    joined: 'March 2024'
  };
  //can add total resumes analyzed
    return(
    <div style={containerStyle}>
      <h2 style={headingStyle}>My Profile</h2>
      <div style={cardStyle}>
        <p><strong>Name:</strong> {user.name}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Company:</strong> {user.company}</p>
        <p><strong>Role:</strong> {user.role}</p>
        <p><strong>Member Since:</strong> {user.joined}</p>
      </div>
    </div>
  );
};

// Styles
const containerStyle = {
  padding: '40px',
  backgroundColor: '#f9f9f9',
  minHeight: '80vh',
};

const headingStyle = {
  fontSize: '2rem',
  marginBottom: '20px',
};

const cardStyle = {
  backgroundColor: '#fff',
  padding: '20px',
  borderRadius: '10px',
  boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
  maxWidth: '400px',
  lineHeight: '1.6',
};

export default Profile;


    
