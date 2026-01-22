from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    '''model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )'''

    ENVIRONMENT: str = "development"

    # Paths
    DATA_DIR: Path = Path("data")
    VECTOR_DB_PATH: Path = Path("vector_store")

    # Vector DB: Qdrant
    QDRANT_COLLECTION: str = "documents"

    # Embeddings / LLM
    GEMINI_API_KEY: str
    GEMINI_LLM_MODEL: str = "models/gemini-2.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "models/text-embedding-004"

    # Security
    API_KEY: str

    # Límites
    MAX_FILE_SIZE_MB: int = 10
    MAX_TOP_K: int = 20

    class Config:
        env_file = ".env"


settings = Settings()
