import asyncio
import json
import logging
from datetime import datetime, timezone
from functools import partial

import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.core.config import settings

FILA_AUDITORIA = "audit.logs"

logger = logging.getLogger(__name__)


async def registrar_evento(collection: AsyncIOMotorCollection, corpo: bytes) -> dict:
    """Converte a mensagem da fila em documento de auditoria e grava no Mongo."""
    dados = json.loads(corpo.decode("utf-8"))
    documento = {**dados, "timestamp": datetime.now(timezone.utc).isoformat()}
    await collection.insert_one(documento)
    return documento


async def process_message(
    collection: AsyncIOMotorCollection,
    message: AbstractIncomingMessage,
) -> None:
    async with message.process():
        try:
            documento = await registrar_evento(collection, message.body)
            logger.info("Evento de auditoria registrado: %s", documento.get("evento"))
        except Exception:
            # A mensagem e confirmada mesmo assim (message.process): um corpo
            # invalido reprocessado para sempre travaria a fila.
            logger.exception("Erro ao processar mensagem de auditoria")


async def main() -> None:
    # Um cliente por processo: o Motor mantem um pool de conexoes, e abrir um
    # cliente novo a cada mensagem criava um pool novo por evento.
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    collection = mongo_client[settings.MONGODB_DB]["logs_auditoria"]

    # Nunca registrar settings.RABBITMQ_URL: ela carrega usuario e senha.
    logger.info("Conectando ao RabbitMQ")
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        # Define prefetch count para balancear carga
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(FILA_AUDITORIA, durable=True)

        logger.info("Aguardando mensagens na fila '%s'", FILA_AUDITORIA)
        await queue.consume(partial(process_message, collection))

        # Mantem o loop rodando indefinidamente
        await asyncio.Future()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[Worker] %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Parado pelo usuario.")
