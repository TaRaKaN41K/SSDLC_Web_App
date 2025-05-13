import os
from pathlib import Path
from pydantic import BaseModel, root_validator, Field
from pydantic_settings import BaseSettings
from fastapi.security import HTTPBearer
from typing import List
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

load_dotenv(BASE_DIR / ".env")

# Получаем строку с CORS_ORIGINS
cors_origins_raw = os.getenv("CORS_ORIGINS", "")

# Преобразуем строку в список
if cors_origins_raw:
    cors_origins = [origin.strip() for origin in cors_origins_raw.split(",") if origin.strip()]
else:
    cors_origins = []  # Если переменная не задана, то список пустой.

UPLOAD_DIR = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

http_bearer = HTTPBearer(auto_error=False)


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt_private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt_public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 3


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
