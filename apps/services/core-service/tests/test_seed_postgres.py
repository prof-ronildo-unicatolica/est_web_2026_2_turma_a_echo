from app.core.config import settings
from app.core.security import verify_password
from app.core.seed_postgres import (
    CIDADES_E_HOTEIS,
    seed_admin_user,
    seed_cidades_e_hoteis,
)
from app.models.hotel import Cidade, Hotel
from app.models.usuario import Usuario

TOTAL_HOTEIS = sum(len(hoteis) for hoteis in CIDADES_E_HOTEIS.values())


def test_seed_admin_cria_administrador_com_senha_da_configuracao(
    db_session, monkeypatch
):
    monkeypatch.setattr(settings, "ADMIN_EMAIL", "novo-admin@hotel.com")
    monkeypatch.setattr(settings, "ADMIN_PASSWORD", "senha-do-env")

    assert seed_admin_user(db_session) is True

    admin = (
        db_session.query(Usuario).filter(Usuario.email == "novo-admin@hotel.com").one()
    )
    assert admin.is_admin is True
    assert verify_password("senha-do-env", admin.senha_hash)


def test_seed_admin_nao_duplica_administrador_existente(db_session, monkeypatch):
    monkeypatch.setattr(settings, "ADMIN_EMAIL", "admin@hotel.com")
    antes = db_session.query(Usuario).count()

    assert seed_admin_user(db_session) is False
    assert db_session.query(Usuario).count() == antes


def test_seed_cidades_e_hoteis_cria_todos_os_pares(db_session):
    assert seed_cidades_e_hoteis(db_session) == TOTAL_HOTEIS

    assert db_session.query(Cidade).count() == len(CIDADES_E_HOTEIS)
    assert db_session.query(Hotel).count() == TOTAL_HOTEIS


def test_seed_cidades_e_hoteis_e_idempotente(db_session):
    seed_cidades_e_hoteis(db_session)

    assert seed_cidades_e_hoteis(db_session) == 0
    assert db_session.query(Cidade).count() == len(CIDADES_E_HOTEIS)
    assert db_session.query(Hotel).count() == TOTAL_HOTEIS


def test_cidade_cadastrada_antes_do_seed_nao_impede_os_hoteis(db_session):
    db_session.add(Cidade(nome="Fortaleza"))
    db_session.commit()

    assert seed_cidades_e_hoteis(db_session) == TOTAL_HOTEIS

    fortaleza = db_session.query(Cidade).filter(Cidade.nome == "Fortaleza").one()
    nomes = sorted(hotel.nome for hotel in fortaleza.hoteis)
    assert nomes == sorted(nome for nome, _ in CIDADES_E_HOTEIS["Fortaleza"])
