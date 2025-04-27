from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DOMAIN_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
