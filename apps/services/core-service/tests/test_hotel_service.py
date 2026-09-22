import pytest

from app.services.hotel_service import (
    CidadeJaExisteError,
    CidadeService,
)


def test_cidade_service_barra_nome_duplicado(db_session):
    service = CidadeService(db_session)

    service.criar("Fortaleza")

    with pytest.raises(CidadeJaExisteError):
        service.criar("Fortaleza")


def test_cidade_service_normaliza_espacos_do_nome(db_session):
    service = CidadeService(db_session)

    cidade = service.criar("   Fortaleza   ")

    assert cidade.nome == "Fortaleza"

    with pytest.raises(CidadeJaExisteError):
        service.criar("Fortaleza")


def test_cidade_service_lista_cidades(db_session):
    service = CidadeService(db_session)

    service.criar("Sobral")
    service.criar("Fortaleza")
    service.criar("Quixada")

    cidades = service.listar()

    assert [cidade.nome for cidade in cidades] == [
        "Fortaleza",
        "Quixada",
        "Sobral",
    ]