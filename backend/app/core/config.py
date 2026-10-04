from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_nmae:str = "Enterprise ai pilot"
    app_version:str="0.1.0"
    redis_url: str
    database_url:str
    qdrant_url: str
    openai_api_key: str
    checkpoint_database_url: str
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    
settings = Settings()