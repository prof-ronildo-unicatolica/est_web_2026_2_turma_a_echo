from datetime import timedelta

import jwt
import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_nao_guarda_a_senha_em_texto():
    senha_hash = hash_password("minha-senha")

    assert senha_hash != "minha-senha"
    assert senha_hash.startswith("$2")


def test_hash_password_usa_sal_diferente_a_cada_chamada():
    assert hash_password("minha-senha") != hash_password("minha-senha")


def test_verify_password_aceita_a_senha_certa_e_recusa_a_errada():
    senha_hash = hash_password("minha-senha")

    assert verify_password("minha-senha", senha_hash) is True
    assert verify_password("outra-senha", senha_hash) is False


def test_token_carrega_o_subject():
    token = create_access_token(subject="ana@hotel.com")

    assert decode_access_token(token)["sub"] == "ana@hotel.com"


def test_token_expirado_e_recusado():
    token = create_access_token(
        subject="ana@hotel.com", expires_delta=timedelta(seconds=-1)
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_token_assinado_com_outra_chave_e_recusado():
    forjado = jwt.encode(
        {"sub": "admin@hotel.com"},
        "chave-de-quem-nao-devia-assinar-0000",
        algorithm="HS256",
    )

    with pytest.raises(jwt.InvalidSignatureError):
        decode_access_token(forjado)
