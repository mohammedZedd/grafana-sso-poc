# backend/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Auth0
    auth0_domain: str = ""
    auth0_api_audience: str = ""
    auth0_client_id: str = ""
    auth0_client_secret: str = ""
    
    # Security
    secret_key: str = "change-this-secret-key"
    
    # Grafana
    grafana_url: str = "http://localhost:3000"
    grafana_admin_user: str = "admin"
    grafana_admin_password: str = "admin"
    
    # CORS
    allowed_origins: list = ["http://localhost:3001", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()