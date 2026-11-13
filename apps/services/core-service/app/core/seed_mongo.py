import asyncio
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)


async def seed_mongo_users(db: AsyncIOMotorDatabase) -> None:
    try:
        users_collection = db["users"]
        existing_user = await users_collection.find_one({"email": settings.ADMIN_EMAIL})

        if existing_user:
            logger.info("MongoDB seed user already exists.")
            return

        admin_user = {
            "username": "admin",
            "email": settings.ADMIN_EMAIL,
            "password_hash": pwd_context.hash(settings.ADMIN_PASSWORD),
            "role": "admin_master",
            "active": True,
        }

        await users_collection.insert_one(admin_user)
        logger.info("MongoDB seed user created successfully.")

    except Exception:
        # Nao derruba a subida da API: o lifespan tambem chama este seed.
        logger.exception("Error seeding MongoDB")


async def main() -> None:
    # Import tardio: o modulo de banco abre os clientes ao ser importado, e os
    # testes importam este arquivo sem precisar deles.
    from app.core.database import get_mongo_db

    await seed_mongo_users(get_mongo_db())


if __name__ == "__main__":
    # O docker-compose roda `python -m app.core.seed_mongo`; sem este bloco o
    # comando importava o modulo e saia sem semear nada.
    logging.basicConfig(level=logging.INFO, format="[seed_mongo] %(message)s")
    asyncio.run(main())
