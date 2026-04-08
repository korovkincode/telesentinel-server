from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IS_PROD: bool

    SUPERUSER_LOGIN: str
    SUPERUSER_PASSWORD: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str

    @property
    def DB_URL(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

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
