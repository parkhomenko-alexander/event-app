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

    DB_DIALECT: str = ""
    DB_DRIVER: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""
    DB_DBNAME: str = ""
    DB_ECHO: bool = False 

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
        return f"{self.DB_DIALECT}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DBNAME}"
    
    def get_redis_buildings_cache_uri(self) -> str:
        return f"redis://{self.REDIS_AMELIA_CACHE_HOST}:{self.REDIS_AMELIA_CACHE_PORT}/{self.REDIS_AMELIA_CACHE_DB}"

    def get_self_redis_uri(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
config = ApplicationSettings()
