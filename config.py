from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    user_id: str
    client_id: str
    client_secret: str
    redirect_uri: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()