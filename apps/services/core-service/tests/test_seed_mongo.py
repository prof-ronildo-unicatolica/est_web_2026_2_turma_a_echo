import asyncio
import logging
from unittest.mock import AsyncMock

from app.core.config import settings
from app.core.seed_mongo import pwd_context, seed_mongo_users


def _banco_com(users):
    return {"users": users}


def test_seed_mongo_cria_admin_quando_nao_existe():
    users = AsyncMock()
    users.find_one.return_value = None

    asyncio.run(seed_mongo_users(_banco_com(users)))

    users.insert_one.assert_awaited_once()
    documento = users.insert_one.await_args.args[0]
    assert documento["email"] == settings.ADMIN_EMAIL
    assert documento["role"] == "admin_master"
    assert documento["password_hash"] != settings.ADMIN_PASSWORD
    assert pwd_context.verify(settings.ADMIN_PASSWORD, documento["password_hash"])


def test_seed_mongo_nao_duplica_admin_existente():
    users = AsyncMock()
    users.find_one.return_value = {"email": settings.ADMIN_EMAIL}

    asyncio.run(seed_mongo_users(_banco_com(users)))

    users.insert_one.assert_not_awaited()


def test_seed_mongo_registra_falha_com_stack_trace_sem_derrubar(caplog):
    users = AsyncMock()
    users.find_one.side_effect = ConnectionError("mongo fora do ar")

    with caplog.at_level(logging.ERROR, logger="app.core.seed_mongo"):
        asyncio.run(seed_mongo_users(_banco_com(users)))

    assert caplog.records[0].exc_info is not None
    users.insert_one.assert_not_awaited()
