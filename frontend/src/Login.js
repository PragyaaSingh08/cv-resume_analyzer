import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const hardcodedUser = {
    email: 'hr@recruitiq.com',
    password: 'recruit123',
  };

  const handleLogin = (e) => {
    e.preventDefault();

    if (email === hardcodedUser.email && password === hardcodedUser.password) {
      setError('');
      localStorage.setItem('isAuthenticated', 'true');
      navigate('/main'); // Redirect after login
    } else {
      setError('Invalid email or password');
    }
  };

  return (
    <div style={containerStyle}>
      <h2 style={headingStyle}>RecruitIQ Login</h2>
      <form onSubmit={handleLogin} style={formStyle}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={inputStyle}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={inputStyle}
        />
        {error && <p style={errorStyle}>{error}</p>}
        <button type="submit" style={buttonStyle}>Login</button>
      </form>
    </div>
  );
};

// Styles
const containerStyle = {
  padding: '50px',
  maxWidth: '400px',
  margin: '100px auto',
  backgroundColor: '#f0f0f0',
  borderRadius: '8px',
  boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
};

const headingStyle = {
  textAlign: 'center',
  marginBottom: '30px',
};

const formStyle = {
  display: 'flex',
  flexDirection: 'column',
  gap: '15px',
};

const inputStyle = {
  padding: '10px',
  fontSize: '16px',
  borderRadius: '4px',
  border: '1px solid #ccc',
};

const buttonStyle = {
  padding: '10px',
  fontSize: '16px',
  borderRadius: '4px',
  backgroundColor: '#008080',
  color: 'white',
  border: 'none',
  cursor: 'pointer',
};

const errorStyle = {
  color: 'red',
  fontSize: '14px',
};

export default Login;
