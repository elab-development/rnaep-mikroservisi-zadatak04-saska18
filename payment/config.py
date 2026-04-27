from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int

    INVENTORY_URL: str

    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()