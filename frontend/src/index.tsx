// frontend/src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Auth0Provider } from '@auth0/auth0-react';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

// Auth0 configuration
const auth0Domain = process.env.REACT_APP_AUTH0_DOMAIN;
const auth0ClientId = process.env.REACT_APP_AUTH0_CLIENT_ID;
const auth0Audience = process.env.REACT_APP_AUTH0_AUDIENCE;

if (!auth0Domain || !auth0ClientId) {
  root.render(
    <div style={{ padding: '50px', textAlign: 'center', color: 'red' }}>
      <h2>Configuration Error</h2>
      <p>Please configure Auth0 in your .env file:</p>
      <pre style={{ textAlign: 'left', background: '#f5f5f5', padding: '20px' }}>
        REACT_APP_AUTH0_DOMAIN=your-domain.auth0.com<br/>
        REACT_APP_AUTH0_CLIENT_ID=your-client-id<br/>
        REACT_APP_AUTH0_AUDIENCE=your-api-audience
      </pre>
    </div>
  );
} else {
  root.render(
    <React.StrictMode>
      <Auth0Provider
        domain={auth0Domain}
        clientId={auth0ClientId}
        authorizationParams={{
          redirect_uri: window.location.origin,
          audience: auth0Audience,
          scope: "openid profile email"
        }}
        cacheLocation="localstorage"
        useRefreshTokens={true}
      >
        <App />
      </Auth0Provider>
    </React.StrictMode>
  );
}