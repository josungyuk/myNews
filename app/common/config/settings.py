import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    def vaildate(self):
        missing = [
            key for key, value in vars(self).items()
            if key.startswith("DB_") and value is None
        ]

        if missing:
            raise RuntimeError(f"Missing environment variables: {missing}")
        
settings = Settings()
settings.vaildate()