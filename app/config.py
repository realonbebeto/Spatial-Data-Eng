from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_username: str = Field(default="")
    database_password: str = Field(default="")
    database_host: str = Field(default="")
    database_port: str = Field(default="")
    database_name: str = Field(default="")

    class Config:
        env_file = "~/Documents/kazispaces/desrc/Spatial-Data-Eng/.env"


settings = Settings()
