from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    #  ------------- elasticsearch settings --------
    ES_HOST: str = 'localhost'
    ES_PORT: int = 9200
    ES_USER: str = 'elastic'
    ES_PASSWORD: str = ''

    #  ------------- debug mode settings --------
    DEBUG: bool = False


load_dotenv()
settings = Settings()
