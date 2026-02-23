// frontend/src/components/LoginButton.tsx
import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const LoginButton: React.FC = () => {
  const { loginWithRedirect, logout, isAuthenticated, isLoading, error } = useAuth0();

  if (isLoading) {
    return <button disabled>Loading...</button>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (isAuthenticated) {
    return (
      <button 
        onClick={() => logout({ logoutParams: { returnTo: window.location.origin }})}
        style={{
          padding: '10px 20px',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
      >
        Logout
      </button>
    );
  }

  return (
    <button 
      onClick={() => loginWithRedirect()}
      style={{
        padding: '10px 20px',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer'
      }}
    >
      Login with Auth0
    </button>
  );
};

export default LoginButton;