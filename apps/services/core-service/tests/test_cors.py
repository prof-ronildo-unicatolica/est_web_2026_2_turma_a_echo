from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import app

# Sem o bloco `with`, o TestClient nao dispara o lifespan (seed do MongoDB):
# a rota raiz nao toca em banco, entao basta para exercitar o middleware.
client = TestClient(app)

ORIGEM_FRONTEND = "http://localhost:5173"


def test_origem_permitida_recebe_cabecalho_cors():
    resposta = client.get("/", headers={"Origin": ORIGEM_FRONTEND})

    assert resposta.headers["access-control-allow-origin"] == ORIGEM_FRONTEND
    assert resposta.headers["access-control-allow-credentials"] == "true"


def test_origem_desconhecida_nao_recebe_cabecalho_cors():
    resposta = client.get("/", headers={"Origin": "https://site-qualquer.example"})

    assert "access-control-allow-origin" not in resposta.headers


def test_preflight_de_origem_desconhecida_e_recusado():
    resposta = client.options(
        "/api/v1/hoteis",
        headers={
            "Origin": "https://site-qualquer.example",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert resposta.status_code == 400


def test_cors_origins_aceita_lista_separada_por_virgula():
    config = Settings(CORS_ORIGINS=" http://a.example , http://b.example ,")

    assert config.cors_origins_list == ["http://a.example", "http://b.example"]
