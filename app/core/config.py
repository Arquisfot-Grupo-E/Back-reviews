from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Conexión a MongoDB
    MONGODB_URL: str
    MONGO_DB_NAME: str

    # Config Google Books
    GOOGLE_BOOKS_API_URL: str
    
    # Variables para inicializar el contenedor de Mongo (leídas por docker-compose)
    MONGO_USER: str
    MONGO_PASSWORD: str

    class Config:
        env_file = ".env"
        extra = "ignore"
        
    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        extra = "ignore"

# Instancia global de settings
settings = Settings()