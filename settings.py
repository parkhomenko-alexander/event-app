from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationSettings(BaseSettings):
    
    APPLICATION_LOGGER_PATH: str = ""
    APPLICATION_LOGGER_FILENAME: str = ""

    APPLICATION_HOST: str = ""  
    APPLICATION_PORT: int = 0 
    APPLICATION_LOG_LEVEL: str = "" 
    APPLICATION_DEBUG: bool = False
    APPLICATION_PREFIX_BEHIND_PROXY: str = "" 
    APPLICATION_API_PREFIX: str = "" 

    DB_URI: str = "" 
    DB_ECHO: bool = False 

    KAFKA_SERVICE_URL: str = "" 
    KAFKA_SERVICE_PORT: str = "" 

    model_config = SettingsConfigDict(env_file=".env")
  
config = ApplicationSettings()
