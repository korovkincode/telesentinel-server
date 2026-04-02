from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    RABBITMQ_URL: str
    JWT_ALGORITHM: str
    SECRET_KEY: str
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
