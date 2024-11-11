import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.getcwd(), ".env")

class ApplicationSettings(BaseSettings):
    
    APPLICATION_LOGGER_PATH: str = ""
    APPLICATION_LOGGER_FILENAME: str = ""

    APPLICATION_HOST: str = ""  
    APPLICATION_PORT: int = 0 
    APPLICATION_LOG_LEVEL: str = "" 
    APPLICATION_DEBUG: bool = False
    APPLICATION_PREFIX_BEHIND_PROXY: str = "" 
    APPLICATION_API_PREFIX: str = "" 

    POSTGRES_DIALECT: str = ""
    POSTGRES_DRIVER: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: int = 0
    POSTGRES_DB: str = ""
    POSTGRES_ECHO: bool = False 

    REDIS_HOST: str = ""
    REDIS_PORT: int = 0
    REDIS_DB: int = 0 

    REDIS_AMELIA_CACHE_HOST: str = ""
    REDIS_AMELIA_CACHE_PORT: int = 0
    REDIS_AMELIA_CACHE_DB: int = 0

    KAFKA_SERVICE_URL: str = ""
    KAFKA_SERVICE_PORT: str = ""
    KAFKA_TOPIC_NAME_EVENTS: str = ""

    model_config = SettingsConfigDict(env_file=DOTENV)

    def get_db_uri(self) -> str:
        return f"{self.POSTGRES_DIALECT}+{self.POSTGRES_DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_redis_buildings_cache_uri(self) -> str:
        return f"redis://{self.REDIS_AMELIA_CACHE_HOST}:{self.REDIS_AMELIA_CACHE_PORT}/{self.REDIS_AMELIA_CACHE_DB}"

    def get_self_redis_uri(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
config = ApplicationSettings()
