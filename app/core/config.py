from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IS_PROD: bool

    SUPERUSER_LOGIN: str
    SUPERUSER_PASSWORD: str

    DB_URL: str
    RABBITMQ_URL: str

    JWT_ALGORITHM: str
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRES_MINUTES: int
    REFRESH_TOKEN_EXPIRES_DAYS: int
    REFRESH_TOKEN_COOKIE_NAME: str

    OPENAI_API_KEY: str

    @property
    def REFRESH_TOKEN_MAX_AGE(self) -> int:
        return self.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60

    class Config:
        env_file = ".env"


settings = Settings()
