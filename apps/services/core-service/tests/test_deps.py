from datetime import timedelta

from app.core.security import create_access_token
from app.models.usuario import Usuario

ME = "/api/v1/auth/me"


def _bearer(token):
    return {"Authorization": f"Bearer {token}"}


def test_token_malformado_retorna_401(client):
    resposta = client.get(ME, headers=_bearer("isto-nao-e-um-jwt"))

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Token invalido ou expirado"
    assert resposta.headers["www-authenticate"] == "Bearer"


def test_token_expirado_retorna_401(client):
    token = create_access_token("cliente@hotel.com", timedelta(seconds=-1))

    resposta = client.get(ME, headers=_bearer(token))

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Token invalido ou expirado"


def test_token_de_usuario_removido_retorna_401(client, db_session):
    token = create_access_token("cliente@hotel.com")
    db_session.query(Usuario).filter(Usuario.email == "cliente@hotel.com").delete()
    db_session.commit()

    resposta = client.get(ME, headers=_bearer(token))

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Usuario nao encontrado"


def test_token_sem_subject_retorna_401(client):
    token = create_access_token("")

    resposta = client.get(ME, headers=_bearer(token))

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Token invalido"


def test_register_cria_usuario_e_recusa_email_repetido(client):
    payload = {"nome": "Ana", "email": "ana@hotel.com", "senha": "segredo1"}

    primeira = client.post("/api/v1/auth/register", json=payload)
    segunda = client.post("/api/v1/auth/register", json=payload)

    assert primeira.status_code == 201
    assert primeira.json() == {
        "email": "ana@hotel.com",
        "nome": "Ana",
        "is_admin": False,
    }
    assert segunda.status_code == 409
