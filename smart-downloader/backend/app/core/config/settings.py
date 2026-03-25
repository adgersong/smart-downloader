from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    # Core application settings
    APP_NAME: str = "SmartDownloader"
    DEBUG: bool = False

    # Database (PostgreSQL) – fallback to SQLite for local dev
    DATABASE_URL: str = "sqlite:///./data/app.db"

    # JWT settings
    JWT_SECRET_KEY: str = "CHANGE_ME_SECRET"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Notification channels
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "user@example.com"
    SMTP_PASSWORD: str = "password"
    SMTP_FROM: str = "no-reply@example.com"
    DINGTALK_WEBHOOK_URL: str = ""
    WECHAT_WEBHOOK_URL: str = ""

    # Ollama AI service
    OLLAMA_HOST: str = "http://host.docker.internal:11434"
    OLLAMA_MODEL: str = "Qwen-VL"

    # File storage – "local" or "minio"
    FILE_STORAGE: Literal["local", "minio"] = "local"
    LOCAL_FILE_PATH: str = "./data/files"
    MINIO_ENDPOINT: str = "http://minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "smart-files"
    MINIO_USE_SSL: bool = False

    # Monitoring / tracing
    OTEL_EXPORTER_JAEGER_ENDPOINT: str = "http://jaeger:14268/api/traces"
    LOKI_ENDPOINT: str = "http://loki:3100/loki/api/v1/push"

    # Backup configuration
    BACKUP_STORAGE_PATH: str = "/backup"
    BACKUP_FREQUENCY: Literal["daily", "weekly", "monthly"] = "daily"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    class Config:
        case_sensitive = True
