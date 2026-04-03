from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPERUSER_LOGIN: str
    SUPERUSER_PASSWORD: str

    DB_URL: str
    RABBITMQ_URL: str

    JWT_ALGORITHM: str
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRES_MINUTES: int
    REFRESH_TOKEN_EXPIRES_DAYS: int

    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
