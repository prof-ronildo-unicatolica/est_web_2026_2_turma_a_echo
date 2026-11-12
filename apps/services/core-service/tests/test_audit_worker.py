import asyncio
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from unittest.mock import AsyncMock

from app.workers.audit_worker import process_message, registrar_evento


class MensagemFalsa:
    """Duplo minimo de aio_pika.IncomingMessage: corpo + process()."""

    def __init__(self, corpo: bytes):
        self.body = corpo
        self.processada = False

    @asynccontextmanager
    async def process(self):
        yield
        self.processada = True


def test_registrar_evento_grava_dados_com_timestamp_utc():
    collection = AsyncMock()
    corpo = json.dumps({"evento": "disciplina.criada", "nome": "Web"}).encode()

    documento = asyncio.run(registrar_evento(collection, corpo))

    collection.insert_one.assert_awaited_once_with(documento)
    assert documento["evento"] == "disciplina.criada"
    assert documento["nome"] == "Web"
    assert (
        datetime.fromisoformat(documento["timestamp"]).utcoffset().total_seconds() == 0
    )


def test_process_message_confirma_e_grava_mensagem_valida():
    collection = AsyncMock()
    mensagem = MensagemFalsa(json.dumps({"evento": "x"}).encode())

    asyncio.run(process_message(collection, mensagem))

    collection.insert_one.assert_awaited_once()
    assert mensagem.processada is True


def test_process_message_com_corpo_invalido_registra_erro_e_nao_grava(caplog):
    collection = AsyncMock()
    mensagem = MensagemFalsa(b"isto nao e json")

    with caplog.at_level(logging.ERROR, logger="app.workers.audit_worker"):
        asyncio.run(process_message(collection, mensagem))

    collection.insert_one.assert_not_awaited()
    assert mensagem.processada is True
    assert caplog.records[0].exc_info is not None
