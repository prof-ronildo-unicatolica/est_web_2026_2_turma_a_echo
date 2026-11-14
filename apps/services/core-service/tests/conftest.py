from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.core.security import hash_password
from app.main import app
from app.models.tutorial import Base
from app.models.usuario import Usuario

# Banco SQLite em memoria. O StaticPool reaproveita uma unica conexao, entao
# todas as sessoes enxergam o mesmo banco e nenhum arquivo test.db fica no disco.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# O bcrypt e lento de proposito (~0,25 s por hash). Calcular uma vez por sessao
# de testes, e nao duas vezes por teste, corta segundos da suite inteira.
SENHA_HASH_CLIENTE = hash_password("cliente123")
SENHA_HASH_ADMIN = hash_password("admin123")


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        db.add(
            Usuario(
                nome="Cliente de Teste",
                email="cliente@hotel.com",
                senha_hash=SENHA_HASH_CLIENTE,
                is_admin=False,
            )
        )

        db.add(
            Usuario(
                nome="Administrador de Teste",
                email="admin@hotel.com",
                senha_hash=SENHA_HASH_ADMIN,
                is_admin=True,
            )
        )

        db.commit()

        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session, monkeypatch):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # O lifespan da aplicacao semeia o MongoDB. Sem um Mongo de pe, cada
    # TestClient esperava o timeout de selecao de servidor (~30 s) antes de
    # seguir. O seed tem teste proprio; aqui ele vira um duplo.
    monkeypatch.setattr("app.main.seed_mongo_users", AsyncMock())

    app.dependency_overrides[get_db] = override_get_db
    # Desativamos raise_server_exceptions para validar retornos de erro 500
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
