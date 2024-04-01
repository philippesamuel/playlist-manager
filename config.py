from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    user_id: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()