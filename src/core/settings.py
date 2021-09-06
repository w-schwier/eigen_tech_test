from pydantic import BaseSettings


class Settings(BaseSettings):
    FOLDER_PATH: str

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    return Settings()
