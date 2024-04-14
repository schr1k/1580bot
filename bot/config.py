from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Config class to validate and store all the environment variables
    """
    # Telegram
    TOKEN: str
    IDEAS_GROUP_ID: str
    APPROVED_IDEAS_GROUP_ID: str
    BUGS_GROUP_ID: str

    # Paths
    PROJECT_PATH: str
    SCHEDULE_PATH: str
    TEACHERS_PATH: str
    POPPLER_PATH: str | None

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    class Config:
        env_file = ".docker.env"


config: Config()
