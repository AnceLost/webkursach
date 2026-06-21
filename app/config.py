from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "user"
    DB_PASS: str = "secret"
    DB_NAME: str = "db_name"
    
    SQLITE_DB_URI: str = "sqlite:///:memory:"
    
    FLASK_SECRET_KEY: str = "default-secret-key"
    
    TESTING: bool = False
    USING_SQLITE: bool = False
    WTF_CSRF_ENABLED: bool = True      
    
    @property
    def SECRET_KEY(self):
        return self.FLASK_SECRET_KEY

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.TESTING:
            return "sqlite:///:memory:"
        if self.USING_SQLITE:
            return self.SQLITE_DB_URI
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="app/.env")
    
# class TestingSettings(Settings):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
#     WTF_CSRF_ENABLED = False   # отключаем CSRF для удобства тестирования форм
#     SERVER_NAME = 'localhost'  # для url_for в тестах