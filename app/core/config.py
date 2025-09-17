from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Conexión principal a la base de datos
    DATABASE_URL: str

    # Config Google Books
    GOOGLE_BOOKS_API_URL: str

    # Variables específicas de Postgres (útiles para inicializar el contenedor)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env"
        extra = "ignore"  # ignora cualquier variable adicional que no esté aquí

# Instancia global de settings
settings = Settings()
