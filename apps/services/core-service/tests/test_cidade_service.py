import uuid

import pytest

from app.services import cidade_service, hotel_service
from app.services.cidade_service import CidadeService
from app.services.excecoes import (
    CidadeJaExisteError,
    CidadeNaoEncontradaError,
    RegraDeNegocioError,
)
from app.services.hotel_service import HotelService


def test_hotel_e_cidade_service_lancam_a_mesma_cidade_nao_encontrada():
    assert cidade_service.CidadeNaoEncontradaError is CidadeNaoEncontradaError
    assert hotel_service.CidadeNaoEncontradaError is CidadeNaoEncontradaError


def test_erro_do_hotel_service_e_capturado_pela_excecao_do_cidade_service(
    db_session,
):
    with pytest.raises(cidade_service.CidadeNaoEncontradaError):
        HotelService(db_session).criar("Hotel A", uuid.uuid4(), 3)


def test_excecoes_de_dominio_herdam_da_mesma_base():
    assert issubclass(CidadeJaExisteError, RegraDeNegocioError)
    assert issubclass(CidadeNaoEncontradaError, RegraDeNegocioError)


def test_criar_cidade_duplicada_informa_o_nome_na_mensagem(db_session):
    service = CidadeService(db_session)
    service.criar("Crato")

    with pytest.raises(CidadeJaExisteError, match="Crato"):
        service.criar("  Crato ")


def test_buscar_cidade_inexistente_retorna_none(db_session):
    assert CidadeService(db_session).buscar_por_id(uuid.uuid4()) is None


def test_listar_sem_cidades_retorna_lista_vazia(db_session):
    assert CidadeService(db_session).listar() == []
