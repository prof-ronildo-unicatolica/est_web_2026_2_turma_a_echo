import uuid

import pytest
from pydantic import ValidationError

from app.schemas.hotel import (
    CidadeCreateSchema,
    HotelCreateSchema,
    HotelUpdateSchema,
)


def test_nome_de_cidade_so_com_espacos_e_recusado():
    with pytest.raises(ValidationError):
        CidadeCreateSchema(nome="   ")


def test_nome_de_cidade_chega_sem_espacos_nas_pontas():
    assert CidadeCreateSchema(nome="  Crato ").nome == "Crato"


def test_nome_de_hotel_so_com_espacos_e_recusado_na_criacao():
    with pytest.raises(ValidationError):
        HotelCreateSchema(nome="   ", cidade_id=uuid.uuid4(), estrelas=3)


def test_nome_de_hotel_so_com_espacos_e_recusado_na_atualizacao():
    with pytest.raises(ValidationError):
        HotelUpdateSchema(nome="   ")


def test_atualizacao_sem_campos_e_valida():
    payload = HotelUpdateSchema()

    assert (payload.nome, payload.cidade_id, payload.estrelas) == (None, None, None)


@pytest.mark.parametrize("estrelas", [0, 6])
def test_estrelas_fora_de_1_a_5_sao_recusadas(estrelas):
    with pytest.raises(ValidationError):
        HotelCreateSchema(nome="Hotel", cidade_id=uuid.uuid4(), estrelas=estrelas)


def test_post_cidade_com_nome_so_de_espacos_retorna_422(client):
    resposta = client.post("/api/v1/cidades", json={"nome": "   "})

    assert resposta.status_code == 422
    assert client.get("/api/v1/cidades").json() == []
