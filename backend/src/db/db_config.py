import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from config import BASE_DIR

load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings(
    DB_USER=os.getenv("DB_USER"),
    DB_PASSWORD=os.getenv("DB_PASSWORD"),
    DB_HOST=os.getenv("DB_HOST"),
    DB_PORT=os.getenv("DB_PORT"),
    DB_NAME=os.getenv("DB_NAME"),
)
