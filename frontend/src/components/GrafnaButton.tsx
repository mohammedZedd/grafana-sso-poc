// frontend/src/components/GrafanaButton.tsx
import React, { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import apiService from '../services/api.service';

const GrafanaButton: React.FC = () => {
  const { isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const openGrafana = async (): Promise<void> => {
  if (!isAuthenticated) {
    setError('Please login first');
    return;
  }

  setLoading(true);
  setError(null);

  try {
    const token = await getAccessTokenSilently();
    
    // Ouvrir via notre endpoint backend
    const url = `http://localhost:8000/open-grafana?token=${encodeURIComponent(token)}`;
    window.open(url, '_blank');
    
  } catch (err: any) {
    setError(err.message || 'Failed to open Grafana');
  } finally {
    setLoading(false);
  }
};

  return (
    <div style={{ margin: '20px 0' }}>
      <button
        onClick={openGrafana}
        disabled={loading || !isAuthenticated}
        style={{
          padding: '15px 30px',
          backgroundColor: isAuthenticated ? '#28a745' : '#6c757d',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: isAuthenticated ? 'pointer' : 'not-allowed',
          fontSize: '16px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}
      >
        {loading ? (
          <>⏳ Opening Grafana...</>
        ) : (
          <>📊 Open Grafana Dashboard</>
        )}
      </button>
      
      {error && (
        <div style={{ 
          marginTop: '10px', 
          padding: '10px', 
          backgroundColor: '#f8d7da', 
          color: '#721c24',
          borderRadius: '5px' 
        }}>
          ⚠️ {error}
        </div>
      )}

      {!isAuthenticated && (
        <p style={{ marginTop: '10px', color: '#6c757d' }}>
          Please login to access Grafana
        </p>
      )}
    </div>
  );
};

export default GrafanaButton;