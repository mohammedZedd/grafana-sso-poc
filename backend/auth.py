# backend/auth.py
from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional, Dict
import httpx
import logging
from functools import lru_cache
from config import settings

logger = logging.getLogger(__name__)

# Security scheme pour Swagger UI
security = HTTPBearer()

class Auth0:
    def __init__(self):
        self.domain = settings.auth0_domain
        self.audience = settings.auth0_api_audience
        self.client_id = settings.auth0_client_id
        self.issuer = f"https://{self.domain}/"
        self.jwks_uri = f"https://{self.domain}/.well-known/jwks.json"
        self._jwks_client = None
    
    @property
    @lru_cache()
    def jwks_client(self):
        """Lazy loading du JWKS client"""
        if not self._jwks_client:
            import jwt as pyjwt
            from jwt import PyJWKClient
            self._jwks_client = PyJWKClient(self.jwks_uri)
        return self._jwks_client
    
    async def verify_token(self, token: str) -> Dict:
        """Vérifie et décode le token JWT Auth0"""
        try:
            # Récupérer la clé de signature
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            
            # Décoder et vérifier le token
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer
            )
            
            return payload
            
        except JWTError as e:
            logger.error(f"JWT Error: {e}")
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
    
    async def get_user_info(self, token: str) -> Dict:
        """Récupère les infos utilisateur depuis Auth0"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://{self.domain}/userinfo",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Auth0 userinfo error: {response.text}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Could not get user info"
                    )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise HTTPException(
                status_code=503,
                detail="Auth0 service unavailable"
            )

# Instance globale
auth0 = Auth0()

# ====================
# DEPENDENCY INJECTIONS
# ====================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict:
    """Dependency pour obtenir l'utilisateur actuel depuis le token"""
    token = credentials.credentials
    
    # Vérifier le token
    payload = await auth0.verify_token(token)
    
    # Enrichir avec les infos utilisateur si nécessaire
    # user_info = await auth0.get_user_info(token)
    
    return {
        "sub": payload.get("sub"),
        "email": payload.get("email", ""),
        "name": payload.get("name", ""),
        "picture": payload.get("picture", ""),
        "token": token  # On garde le token pour Grafana
    }

async def get_optional_user(
    request: Request
) -> Optional[Dict]:
    """Dependency pour obtenir l'utilisateur si token présent (optionnel)"""
    auth_header = request.headers.get("Authorization", "")
    
    if not auth_header.startswith("Bearer "):
        return None
    
    try:
        token = auth_header.split(" ")[1]
        payload = await auth0.verify_token(token)
        return {
            "sub": payload.get("sub"),
            "email": payload.get("email", ""),
            "token": token
        }
    except:
        return None