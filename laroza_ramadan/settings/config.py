from pydantic_settings import BaseSettings, SettingsConfigDict
from fake_useragent import UserAgent
ua = UserAgent()

headers = {
    "User-Agent": f"{ua.random}"
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    # WeCima_Config
    LAROZA_SITE_NAME: str
    LAROZA_SITE_URL: str
    LAROZA_SITE_Series_List_URL: str
    

def get_settings():
    return Settings()

settings = get_settings()