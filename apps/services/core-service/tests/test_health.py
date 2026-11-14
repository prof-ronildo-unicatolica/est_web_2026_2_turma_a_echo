import pytest

from app.core.database import get_mongo_db
from app.main import app

HEALTH = "/api/v1/health"


class MongoFalso:
    def __init__(self, erro=None):
        self.erro = erro

    async def command(self, nome):
        if self.erro:
            raise self.erro
        return {"ok": 1}


@pytest.fixture
def usar_mongo(client):
    def _usar(mongo):
        app.dependency_overrides[get_mongo_db] = lambda: mongo

    return _usar


def test_health_com_bancos_de_pe_retorna_200(client, usar_mongo):
    usar_mongo(MongoFalso())

    resposta = client.get(HEALTH)

    assert resposta.status_code == 200
    assert resposta.json() == {
        "status": "healthy",
        "postgres": "healthy",
        "mongodb": "healthy",
    }


def test_health_com_mongo_fora_retorna_503_sem_vazar_o_erro(client, usar_mongo):
    usar_mongo(MongoFalso(ConnectionError("mongodb://admin:segredo@db recusou")))

    resposta = client.get(HEALTH)

    assert resposta.status_code == 503
    assert resposta.json()["detail"] == {
        "status": "unhealthy",
        "postgres": "healthy",
        "mongodb": "unhealthy",
    }
    assert "segredo" not in resposta.text
