import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)


async def seed_mongo_users(db: AsyncIOMotorDatabase):
    try:
        users_collection = db["users"]
        existing_user = await users_collection.find_one(
            {"email": settings.ADMIN_EMAIL}
        )

        if not existing_user:
            hashed_password = pwd_context.hash(settings.ADMIN_PASSWORD)

            admin_user = {
                "username": "admin",
                "email": settings.ADMIN_EMAIL,
                "password_hash": hashed_password,
                "role": "admin_master",
                "active": True,
            }

            await users_collection.insert_one(admin_user)
            logger.info("MongoDB seed user created successfully.")
        else:
            logger.info("MongoDB seed user already exists.")

    except Exception as e:
        logger.error(f"Error seeding MongoDB: {str(e)}")