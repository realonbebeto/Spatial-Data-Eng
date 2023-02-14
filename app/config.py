from pydantic import BaseSettings


class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_host: str
    database_port: str
    database_name: str

    class Config:
        env_file = "~/Documents/kazispaces/desrc/Spatial-Data-Eng/.env"


settings = Settings()
