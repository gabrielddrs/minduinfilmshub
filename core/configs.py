from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):

    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://gabriel:argo@localhost:5432/minduinfilmeshub'
    DBBaseModel = declarative_base()

    class Configs:
        case_sensitive = True


settings = Settings()
