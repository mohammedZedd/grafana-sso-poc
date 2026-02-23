### 2. Crée & Configure tes .env (⚠️ Secrets privés → ne JAMAIS commiter !)

Crée `front/.env` 

#### Exemple Front : `front/.env`
REACT_APP_AUTH0_DOMAIN=YOUR_DOMAIN.auth0.com # Ex: dev-abc123.us.auth0.com
REACT_APP_AUTH0_CLIENT_ID=your-client-id-here # Auth0 > Applications > ton app
REACT_APP_AUTH0_AUDIENCE=your-api-audience # Ex: https://ton-api/
REACT_APP_AUTH0_REDIRECT_URI=http://localhost:3001/callback
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GRAFANA_URL=http://localhost # Via Nginx

