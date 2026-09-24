from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    app_env: str = "development"
    secret_key: str = "changeme"

    class Config:
        env_file = ".env"


settings = Settings()
