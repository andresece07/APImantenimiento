# config.py (Versión Corregida)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Valores que no son secretos pueden tener un default
    APP_NAME: str = "Backend Mantenimiento"
    APP_ENV: str = "dev"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_TTL_MINUTES: int = 15
    SINGLE_SESSION_PER_USER: bool = False

    # --- VALORES SENSIBLES ---
    # No les ponemos valor por defecto para obligar
    # a que se lean desde el archivo .env
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    JWT_SECRET: str
    MASTER_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
