from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True, env_file=".env")

    PROJECT_NAME: str = "Sistema de Reservas - Core Service"
    API_V1_STR: str = "/api/v1"

    # Origens que o navegador pode usar para chamar a API, separadas por virgula.
    # Com credenciais (allow_credentials) o CORS nao aceita "*".
    CORS_ORIGINS: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origem.strip() for origem in self.CORS_ORIGINS.split(",") if origem.strip()
        ]

    # Configuracoes de autenticacao JWT
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuracoes do usuario administrador inicial
    ADMIN_NAME: str = "Administrador"
    ADMIN_EMAIL: str = "admin@hotel.com"
    ADMIN_PASSWORD: str

    # Configuracoes do PostgreSQL
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "hotel_db_dev"
    POSTGRES_PORT: str = "5432"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Configuracoes do MongoDB
    MONGODB_URL: str
    MONGODB_DB: str = "hotel_mongo_dev"

    # Configuracoes do RabbitMQ
    RABBITMQ_URL: str


settings = Settings()
