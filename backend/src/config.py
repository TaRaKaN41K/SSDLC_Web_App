from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from fastapi.security import HTTPBearer

BASE_DIR = Path(__file__).parent.parent.parent

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
