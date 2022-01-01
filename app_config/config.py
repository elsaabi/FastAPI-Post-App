from pydantic import BaseSettings

class Settings(BaseSettings):
# class Settings():
    database_hostname: str = "localhost"
    database_port: int  = 8000
    database_name: str = "FastAPIDB"
    database_username: str  = "postgres"
    database_password: str = "admin"
    
    secret_key: str  = "23449a762a0d35dfa45d4cb2e208c7aa09a2e839617d732d79bcef1f0d77c6a7"
    algorithm: str  = "HS256"
    access_token_expires_minutes: int  = 60
    
    class Config:
        env_file = ".env"
        
settings = Settings()

# print(settings.database_username)