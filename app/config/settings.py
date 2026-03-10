from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Voice Reminder API"
    admin_email: str = "admin@example.com"
    items_per_user: int = 50
    
    class Config:
        env_file = ".env"

settings = Settings()
