from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).parent / '.env'

class Settings(BaseSettings):
    user_id: str
    client_id: str
    client_secret: str
    redirect_uri: str
    spotify_auth_token: str
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8')


settings = Settings()