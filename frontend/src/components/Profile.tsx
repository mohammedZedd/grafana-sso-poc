// frontend/src/components/Profile.tsx
import React, { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import apiService from '../services/api.service';
import { User } from '../types';

const Profile: React.FC = () => {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [apiData, setApiData] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!isAuthenticated) return;
      
      try {
        setLoading(true);
        setError(null);
        const token = await getAccessTokenSilently();
        apiService.setToken(token);
        
        const data = await apiService.getMe();
        setApiData(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch user data');
        console.error('Profile fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [isAuthenticated, getAccessTokenSilently]);

  if (!isAuthenticated) {
    return <div>Please login to see your profile</div>;
  }

  return (
    <div style={{ padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '10px' }}>
      <h2>User Profile</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <h3>Auth0 User Info:</h3>
        {user?.picture && (
          <img 
            src={user.picture} 
            alt={user.name || 'User'} 
            style={{ width: '100px', borderRadius: '50%' }} 
          />
        )}
        <p><strong>Name:</strong> {user?.name || 'N/A'}</p>
        <p><strong>Email:</strong> {user?.email || 'N/A'}</p>
        <p><strong>Sub:</strong> {user?.sub || 'N/A'}</p>
      </div>

      <div>
        <h3>Backend API Response:</h3>
        {loading && <p>Loading API data...</p>}
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}
        {apiData && (
          <pre style={{ backgroundColor: '#fff', padding: '10px', borderRadius: '5px' }}>
            {JSON.stringify(apiData, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
};

export default Profile;