"""
Configuration settings for the application.
Reads environment variables with production-ready defaults and fallback support.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Fake Review & Coordinated Network Detection System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security & JWT Token settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Reviewer privacy salt for pseudonymization
    REVIEWER_HASH_SALT: str
    
    # Database Settings
    USE_MYSQL: bool = False  # Set to True in .env when running MySQL via XAMPP
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "fake_review_db"
    
    MYSQL_URL: str = "mysql+pymysql://root:@localhost:3306/fake_review_db"
    SQLITE_URL: str = "sqlite:///./fake_review_db.sqlite3"
    
    @property
    def DATABASE_URL(self) -> str:
        if self.USE_MYSQL:
            return self.MYSQL_URL
        return self.SQLITE_URL
    
    # CORS settings for frontend integration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()
