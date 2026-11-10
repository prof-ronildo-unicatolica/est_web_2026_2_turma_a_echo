import uuid

import pytest

from app.services.cidade_service import (
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


def test_cidade_service_cria_cidade(db_session):
    service = CidadeService(db_session)

    cidade = service.criar("Fortaleza")
    cidade_id = cidade.id
    db_session.expire_all()

    cidade_salva = service.buscar_por_id(cidade_id)

    assert cidade_salva is not None
    assert cidade_salva.nome == "Fortaleza"


def test_hotel_service_cria_hotel(db_session):
    cidade = CidadeService(db_session).criar("Fortaleza")
    service = HotelService(db_session)

    hotel = service.criar("   Hotel A   ", cidade.id, 5)
    hotel_id = hotel.id
    db_session.expire_all()

    hotel_salvo = service.buscar_por_id(hotel_id)

    assert hotel_salvo.nome == "Hotel A"
    assert hotel_salvo.cidade_id == cidade.id
    assert hotel_salvo.estrelas == 5


def test_hotel_service_barra_criacao_com_cidade_inexistente(db_session):
    service = HotelService(db_session)

    with pytest.raises(CidadeNaoEncontradaError):
        service.criar("Hotel A", uuid.uuid4(), 5)

    assert service.listar() == []


def test_hotel_service_lista_hoteis(db_session):
    cidades = CidadeService(db_session)
    fortaleza = cidades.criar("Fortaleza")
    sobral = cidades.criar("Sobral")
    service = HotelService(db_session)
    service.criar("Hotel Z", fortaleza.id, 4)
    service.criar("Hotel A", sobral.id, 5)

    hoteis = service.listar()

    assert [hotel.nome for hotel in hoteis] == ["Hotel A", "Hotel Z"]
    assert [hotel.cidade.nome for hotel in hoteis] == ["Sobral", "Fortaleza"]


def test_hotel_service_lista_hoteis_por_cidade(db_session):
    cidades = CidadeService(db_session)
    fortaleza = cidades.criar("Fortaleza")
    sobral = cidades.criar("Sobral")
    service = HotelService(db_session)
    service.criar("Hotel Z", fortaleza.id, 4)
    service.criar("Hotel B", sobral.id, 3)
    service.criar("Hotel A", fortaleza.id, 5)

    hoteis = service.listar(cidade_id=fortaleza.id)

    assert [hotel.nome for hotel in hoteis] == ["Hotel A", "Hotel Z"]
    assert all(hotel.cidade_id == fortaleza.id for hotel in hoteis)


def test_hotel_service_lista_cidade_sem_hoteis(db_session):
    cidade = CidadeService(db_session).criar("Fortaleza")
    service = HotelService(db_session)

    assert service.listar(cidade_id=cidade.id) == []


def test_hotel_service_barra_filtro_com_cidade_inexistente(db_session):
    service = HotelService(db_session)

    with pytest.raises(CidadeNaoEncontradaError):
        service.listar(cidade_id=uuid.uuid4())


def test_hotel_service_busca_por_id(db_session):
    cidade = CidadeService(db_session).criar("Fortaleza")
    service = HotelService(db_session)
    hotel = service.criar("Hotel A", cidade.id, 5)

    encontrado = service.buscar_por_id(hotel.id)

    assert encontrado.id == hotel.id
    assert encontrado.nome == "Hotel A"
    assert encontrado.cidade.nome == "Fortaleza"


def test_hotel_service_busca_hotel_inexistente(db_session):
    service = HotelService(db_session)

    with pytest.raises(HotelNaoEncontradoError):
        service.buscar_por_id(uuid.uuid4())


def test_hotel_service_atualiza_hotel(db_session):
    cidades = CidadeService(db_session)
    fortaleza = cidades.criar("Fortaleza")
    sobral = cidades.criar("Sobral")
    service = HotelService(db_session)
    hotel = service.criar("Hotel A", fortaleza.id, 3)
    hotel_id = hotel.id

    service.atualizar(hotel_id, nome="   Hotel B   ", cidade_id=sobral.id, estrelas=5)
    db_session.expire_all()
    atualizado = service.buscar_por_id(hotel_id)

    assert atualizado.nome == "Hotel B"
    assert atualizado.cidade_id == sobral.id
    assert atualizado.estrelas == 5


def test_hotel_service_atualiza_apenas_nome(db_session):
    cidade = CidadeService(db_session).criar("Fortaleza")
    service = HotelService(db_session)
    hotel = service.criar("Hotel A", cidade.id, 3)

    atualizado = service.atualizar(hotel.id, nome="Hotel B")

    assert atualizado.nome == "Hotel B"
    assert atualizado.cidade_id == cidade.id
    assert atualizado.estrelas == 3


def test_hotel_service_barra_atualizacao_com_cidade_inexistente(db_session):
    cidade = CidadeService(db_session).criar("Fortaleza")
    service = HotelService(db_session)
    hotel = service.criar("Hotel A", cidade.id, 3)

    with pytest.raises(CidadeNaoEncontradaError):
        service.atualizar(hotel.id, cidade_id=uuid.uuid4())

    db_session.expire_all()
    assert service.buscar_por_id(hotel.id).cidade_id == cidade.id


def test_hotel_service_atualiza_hotel_inexistente(db_session):
    service = HotelService(db_session)

    with pytest.raises(HotelNaoEncontradoError):
        service.atualizar(uuid.uuid4(), nome="Hotel B")


def test_hotel_service_exclui_hotel(db_session):
    cidade = CidadeService(db_session).criar("Fortaleza")
    service = HotelService(db_session)
    hotel = service.criar("Hotel A", cidade.id, 3)
    hotel_id = hotel.id

    service.excluir(hotel_id)

    assert service.listar() == []
    with pytest.raises(HotelNaoEncontradoError):
        service.buscar_por_id(hotel_id)
    assert CidadeService(db_session).buscar_por_id(cidade.id) is not None


def test_hotel_service_exclui_hotel_inexistente(db_session):
    service = HotelService(db_session)

    with pytest.raises(HotelNaoEncontradoError):
        service.excluir(uuid.uuid4())
