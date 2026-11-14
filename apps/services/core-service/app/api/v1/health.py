import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.database import get_db, get_mongo_db

router = APIRouter()
logger = logging.getLogger(__name__)

SAUDAVEL = "healthy"
INDISPONIVEL = "unhealthy"


@router.get(
    "/health",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "PostgreSQL ou MongoDB indisponível"
        }
    },
)
async def health_check(
    db: Annotated[Session, Depends(get_db)],
    mongo_db: Annotated[AsyncIOMotorDatabase, Depends(get_mongo_db)],
):
    postgres_status = INDISPONIVEL
    mongo_status = INDISPONIVEL

    # A mensagem da excecao vai para o log, nunca para a resposta: a rota e
    # publica e o erro do driver pode trazer host, porta e usuario do banco.
    try:
        db.execute(text("SELECT 1"))
        postgres_status = SAUDAVEL
    except Exception:
        logger.exception("Health check: PostgreSQL indisponivel")

    try:
        await mongo_db.command("ping")
        mongo_status = SAUDAVEL
    except Exception:
        logger.exception("Health check: MongoDB indisponivel")

    corpo = {
        "status": SAUDAVEL,
        "postgres": postgres_status,
        "mongodb": mongo_status,
    }

    if INDISPONIVEL in (postgres_status, mongo_status):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={**corpo, "status": INDISPONIVEL},
        )

    return corpo
