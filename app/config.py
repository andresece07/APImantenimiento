from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Backend Mantenimiento"
    APP_ENV: str = "dev"

    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "app_user"
    DB_PASSWORD: str = "change_this"
    DB_NAME: str = "mantenimiento"

    JWT_SECRET: str = "please_change_me"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_TTL_MINUTES: int = 15  # corto; sesión total se gobierna con refresh TTL

    SINGLE_SESSION_PER_USER: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
