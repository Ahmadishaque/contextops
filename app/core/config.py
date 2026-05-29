from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ContextOps"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql://contextops:contextops@localhost:5432/contextops"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "contextops_chunks"
    redis_url: str = "redis://localhost:6379/0"

    openai_api_key: str = "replace_me"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
