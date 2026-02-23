# backend/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# IMPORTANT: Cette ligne crée l'objet 'app'
app = FastAPI(
    title="Grafana SSO Backend",
    description="Backend pour l'authentification SSO Grafana avec Auth0",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================
# ENDPOINTS DE BASE
# ====================

@app.get("/")
async def root():
    """Endpoint de base pour vérifier que l'API fonctionne"""
    return {
        "message": "Grafana SSO Backend API",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "fastapi-backend",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/config")
async def get_config():
    """Retourne la configuration publique"""
    return {
        "auth0_domain": "your-domain.auth0.com",
        "grafana_url": "http://localhost:3000",
        "environment": "development"
    }

# ====================
# EVENTS
# ====================

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI Backend starting...")
    
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 FastAPI Backend shutting down...")




# backend/main.py - MISE À JOUR
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
from typing import Dict, Optional
import json

from config import settings
from auth import get_current_user, get_optional_user, auth0

# ... (garde le code existant du début)

# ====================
# ENDPOINTS PROTÉGÉS
# ====================

@app.get("/api/me")
async def get_me(user: Dict = Depends(get_current_user)):
    """Obtenir les infos de l'utilisateur connecté"""
    return {
        "user": user,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/protected")
async def protected_route(user: Dict = Depends(get_current_user)):
    """Exemple d'endpoint protégé"""
    return {
        "message": f"Hello {user.get('email', 'User')}!",
        "user_id": user.get('sub'),
        "timestamp": datetime.now().isoformat()
    }

# ====================
# GRAFANA SSO ENDPOINTS
# ====================

@app.post("/api/validate-token")
async def validate_token_for_grafana(
    request: Request,
    response: Response,
    user: Dict = Depends(get_current_user)
):
    """
    Endpoint utilisé par Nginx pour valider le token Auth0
    Retourne les headers nécessaires pour Grafana
    """
    email = user.get("email", "")
    name = user.get("name", email.split("@")[0] if email else "user")
    
    # Headers pour Nginx/Grafana
    response.headers["X-WEBAUTH-USER"] = name
    response.headers["X-WEBAUTH-EMAIL"] = email
    response.headers["X-WEBAUTH-NAME"] = name
    
    # On peut aussi stocker une session si besoin
    session_id = f"session_{user.get('sub', 'unknown')}"
    
    return {
        "authenticated": True,
        "user": name,
        "email": email,
        "session_id": session_id
    }

@app.get("/api/grafana-url")
async def get_grafana_url(user: Dict = Depends(get_current_user)):
    """
    Génère une URL Grafana authentifiée pour l'utilisateur
    """
    return {
        "url": settings.grafana_url,
        "user": user.get("email"),
        "method": "proxy_auth",
        "headers": {
            "X-WEBAUTH-USER": user.get("name", user.get("email", "").split("@")[0]),
            "X-WEBAUTH-EMAIL": user.get("email", "")
        }
    }

# Ajoute ceci dans backend/main.py après les autres endpoints

@app.get("/api/validate-token")
async def validate_token_for_grafana(
    request: Request,
    response: Response
):
    """Endpoint pour Nginx auth_request avec Auth0"""
    try:
        from config import settings
        import jwt
        from jwt import PyJWKClient
        
        auth_header = request.headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            response.status_code = 401
            return {"authenticated": False}
        
        token = auth_header.split(" ")[1]
        
        # Validation Auth0 réelle
        jwks_client = PyJWKClient(f"https://{settings.auth0_domain}/.well-known/jwks.json")
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.auth0_api_audience,
            issuer=f"https://{settings.auth0_domain}/"
        )
        
        # Extraire les infos utilisateur
        email = payload.get("email", "unknown@example.com")
        name = payload.get("name", email.split("@")[0])
        
        # Headers pour Grafana
        response.headers["X-WEBAUTH-USER"] = name or email.split("@")[0]
        response.headers["X-WEBAUTH-EMAIL"] = email
        
        return {"authenticated": True, "user": email}
        
    except Exception as e:
        print(f"Validation error: {e}")
        response.status_code = 401
        return {"authenticated": False, "error": str(e)}


from fastapi.responses import HTMLResponse

from fastapi.responses import RedirectResponse

@app.get("/grafana-redirect")
async def grafana_redirect(token: str, response: Response):
    """Redirige vers Grafana avec cookie de session"""
    # Créer un cookie de session
    response = RedirectResponse(url="http://localhost:3030/dashboards")
    response.set_cookie(
        key="auth_token",
        value=token,
        max_age=3600,
        httponly=True
    )
    return response

@app.get("/open-grafana")
async def open_grafana(token: str):
    """Endpoint pour ouvrir Grafana avec authentification"""
    from fastapi.responses import HTMLResponse
    
    # Valider le token d'abord (optionnel)
    # ... validation code ...
    
    # Page HTML qui fait la redirection avec le header
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Opening Grafana...</title>
    </head>
    <body>
        <h2>Redirecting to Grafana...</h2>
        <form id="grafanaForm" action="http://localhost:3030/dashboards" method="GET">
            <input type="hidden" name="auth_token" value="{token}">
        </form>
        <script>
            // Stocker le token dans localStorage
            localStorage.setItem('grafana_token', '{token}');
            
            // Créer un cookie
            document.cookie = "auth_token={token}; path=/; max-age=3600";
            
            // Rediriger
            setTimeout(() => {{
                window.location.href = 'http://localhost:3030/dashboards';
            }}, 100);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.post("/api/create-grafana-session")
async def create_grafana_session(
    response: Response,
    user: Dict = Depends(get_current_user)
):
    """
    Crée une session pour accès direct à Grafana
    """
    import secrets
    import hashlib
    
    # Créer un token de session
    session_token = secrets.token_urlsafe(32)
    session_id = hashlib.sha256(f"{user['sub']}:{session_token}".encode()).hexdigest()
    
    # Dans une vraie app, tu stockerais ça dans Redis/DB
    # Pour le test, on met dans un cookie
    response.set_cookie(
        key="grafana_session",
        value=session_id,
        max_age=3600,  # 1 heure
        httponly=True,
        samesite="lax"
    )
    
    return {
        "session_created": True,
        "session_id": session_id,
        "user": user.get("email"),
        "expires_in": 3600
    }

# ====================
# ENDPOINTS DE TEST
# ====================

@app.get("/api/test-auth")
async def test_auth(user: Optional[Dict] = Depends(get_optional_user)):
    """Test endpoint - montre l'état d'authentification"""
    if user:
        return {
            "authenticated": True,
            "user": user,
            "message": "Token valide"
        }
    else:
        return {
            "authenticated": False,
            "message": "Pas de token ou token invalide"
        }

# ====================
# GESTION DES ERREURS MISE À JOUR
# ====================

@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc):
    return JSONResponse(
        status_code=401,
        content={
            "error": "Unauthorized",
            "message": "Token invalide ou expiré",
            "timestamp": datetime.now().isoformat()
        }
    )




# Pour debug - vérifier que app existe
if __name__ == "__main__":
    print("✅ main.py loaded successfully")
    print(f"App type: {type(app)}")