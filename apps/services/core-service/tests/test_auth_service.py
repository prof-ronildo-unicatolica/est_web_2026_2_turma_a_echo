from app.core.security import decode_access_token, verify_password
from app.services.auth_service import AuthService


def test_register_cria_usuario_comum_com_senha_em_hash(db_session):
    usuario = AuthService(db_session).register(
        nome="Maria", email="maria@hotel.com", senha="segredo1"
    )

    assert usuario is not None
    assert usuario.email == "maria@hotel.com"
    assert usuario.is_admin is False
    assert usuario.senha_hash != "segredo1"
    assert verify_password("segredo1", usuario.senha_hash)


def test_register_com_email_existente_retorna_none(db_session):
    service = AuthService(db_session)

    resultado = service.register(
        nome="Outro", email="cliente@hotel.com", senha="qualquer"
    )

    assert resultado is None


def test_login_valido_devolve_token_com_email_no_sub(db_session):
    token = AuthService(db_session).login(email="cliente@hotel.com", senha="cliente123")

    assert token is not None
    assert decode_access_token(token)["sub"] == "cliente@hotel.com"


def test_login_com_senha_errada_retorna_none(db_session):
    token = AuthService(db_session).login(email="cliente@hotel.com", senha="errada")

    assert token is None


def test_login_com_email_inexistente_retorna_none(db_session):
    token = AuthService(db_session).login(email="ninguem@hotel.com", senha="x")

    assert token is None
