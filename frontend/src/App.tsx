// frontend/src/App.tsx
import React, { useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import LoginButton from './components/LoginButton';
import Profile from './components/Profile';
import GrafanaButton from './components/GrafnaButton';
import './App.css';

const App: React.FC = () => {
  const { isLoading, isAuthenticated, error } = useAuth0();

  useEffect(() => {
    if (error) {
      console.error('Auth0 Error:', error);
    }
  }, [error]);

  if (error) {
    return (
      <div className="App">
        <div style={{ padding: '50px', textAlign: 'center', color: 'red' }}>
          <h2>Authentication Error</h2>
          <p>{error.message}</p>
          <p style={{ fontSize: '14px', marginTop: '20px' }}>
            Check your Auth0 configuration in .env file
          </p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="App">
        <div style={{ padding: '50px', textAlign: 'center' }}>
          <h2>Loading...</h2>
          <div className="spinner">⏳</div>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header style={{ 
        backgroundColor: '#282c34', 
        padding: '20px', 
        color: 'white',
        textAlign: 'center'
      }}>
        <h1>🚀 Grafana SSO Portal</h1>
        <p>Single Sign-On with Auth0</p>
      </header>

      <main style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
        {/* Login/Logout Button */}
        <div style={{ textAlign: 'right', marginBottom: '20px' }}>
          <LoginButton />
        </div>

        {/* Status */}
        <div style={{ 
          padding: '15px', 
          backgroundColor: isAuthenticated ? '#d4edda' : '#f8d7da',
          color: isAuthenticated ? '#155724' : '#721c24',
          borderRadius: '5px',
          marginBottom: '20px',
          textAlign: 'center'
        }}>
          Status: {isAuthenticated ? '✅ Authenticated' : '❌ Not authenticated'}
        </div>

        {/* Main Content */}
        <div style={{ display: 'grid', gap: '20px' }}>
          {/* Grafana Button */}
          <section style={{ 
            padding: '20px', 
            backgroundColor: '#fff', 
            borderRadius: '10px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}>
            <h2>Grafana Access</h2>
            <GrafanaButton />
          </section>

          {/* User Profile */}
          {isAuthenticated && (
            <section>
              <Profile />
            </section>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;