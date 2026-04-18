from pydantic_settings import BaseSettings, SettingsConfigDict

__name__ = 'config'

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    FLASK_SECRET_KEY: str
    
    @property
    def get_db_uri(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"
    
    @property
    def get_secret_key(self):
        return self.FLASK_SECRET_KEY
    
    model_config = SettingsConfigDict(env_file="app/.env")