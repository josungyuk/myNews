from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Use Neon (or another hosted PostgreSQL) with one complete URL when set.
    # The individual DB_* fields remain available for local development.
    DATABASE_URL: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_NAME: str | None = None

    llm_api_key: str
    llm_model: str
    llm_fallback_model: str | None = None
    llm_max_output_tokens: int = 512
    embedding_model: str = "gemini-embedding-001"
    embedding_dimension: int = 768
    rag_top_k: int = 3
    rag_max_context_chars: int = 6000
    
    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            if self.DATABASE_URL.startswith("postgresql://"):
                return "postgresql+psycopg://" + self.DATABASE_URL.removeprefix(
                    "postgresql://"
                )
            return self.DATABASE_URL

        local_values = (
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )
        if any(value is None for value in local_values):
            raise ValueError(
                "Set DATABASE_URL or all DB_USER, DB_PASSWORD, DB_HOST, "
                "DB_PORT, and DB_NAME values"
            )

        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    class Config:
        env_file = ".env"
        
settings = Settings()
