import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    API_KEY: str = os.getenv("API_KEY")

settings = Settings()