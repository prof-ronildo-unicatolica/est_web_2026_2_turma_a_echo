import uuid

import pytest

from app.models.hotel import Cidade, Hotel

BASE = "/api/v1/hoteis"


def _headers(client, email, senha):
    resposta = client.post("/api/v1/auth/login", json={"email": email, "senha": senha})
    return {"Authorization": f"Bearer {resposta.json()['access_token']}"}


@pytest.fixture
def admin(client):
    return _headers(client, "admin@hotel.com", "admin123")


@pytest.fixture
def cliente(client):
    return _headers(client, "cliente@hotel.com", "cliente123")


@pytest.fixture
def fortaleza(db_session):
    cidade = Cidade(nome="Fortaleza")
    db_session.add(cidade)
    db_session.commit()
    return cidade


@pytest.fixture
def hotel(db_session, fortaleza):
    hotel = Hotel(nome="Hotel Beira-Mar", cidade_id=fortaleza.id, estrelas=4)
    db_session.add(hotel)
    db_session.commit()
    return hotel


# --- Leitura: publica -------------------------------------------------------


def test_listar_hoteis_sem_token_traz_cidade_aninhada(client, hotel):
    resposta = client.get(BASE)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [h["nome"] for h in corpo] == ["Hotel Beira-Mar"]
    assert corpo[0]["cidade"]["nome"] == "Fortaleza"


def test_listar_hoteis_filtra_por_cidade(client, db_session, hotel):
    sobral = Cidade(nome="Sobral")
    db_session.add(sobral)
    db_session.commit()
    db_session.add(Hotel(nome="Hotel Sobral", cidade_id=sobral.id, estrelas=3))
    db_session.commit()

    resposta = client.get(BASE, params={"cidade_id": str(sobral.id)})

    assert resposta.status_code == 200
    assert [h["nome"] for h in resposta.json()] == ["Hotel Sobral"]


def test_listar_hoteis_de_cidade_inexistente_retorna_404(client):
    resposta = client.get(BASE, params={"cidade_id": str(uuid.uuid4())})

    assert resposta.status_code == 404


def test_buscar_hotel_inexistente_retorna_404(client):
    resposta = client.get(f"{BASE}/{uuid.uuid4()}")

    assert resposta.status_code == 404


# --- Escrita: somente administrador ------------------------------------------


def test_criar_hotel_sem_token_e_bloqueado(client, fortaleza):
    resposta = client.post(
        BASE, json={"nome": "Hotel X", "cidade_id": str(fortaleza.id), "estrelas": 3}
    )

    assert resposta.status_code in (401, 403)
    assert client.get(BASE).json() == []


def test_criar_hotel_como_cliente_retorna_403(client, cliente, fortaleza):
    resposta = client.post(
        BASE,
        json={"nome": "Hotel X", "cidade_id": str(fortaleza.id), "estrelas": 3},
        headers=cliente,
    )

    assert resposta.status_code == 403
    assert client.get(BASE).json() == []


def test_criar_hotel_como_admin_retorna_201(client, admin, fortaleza):
    resposta = client.post(
        BASE,
        json={"nome": "Hotel X", "cidade_id": str(fortaleza.id), "estrelas": 3},
        headers=admin,
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Hotel X"
    assert corpo["cidade"] == {"id": str(fortaleza.id), "nome": "Fortaleza"}


def test_criar_hotel_com_cidade_inexistente_retorna_404(client, admin):
    resposta = client.post(
        BASE,
        json={"nome": "Hotel X", "cidade_id": str(uuid.uuid4()), "estrelas": 3},
        headers=admin,
    )

    assert resposta.status_code == 404


def test_atualizar_hotel_como_cliente_retorna_403(client, cliente, hotel):
    resposta = client.put(f"{BASE}/{hotel.id}", json={"estrelas": 1}, headers=cliente)

    assert resposta.status_code == 403
    assert client.get(f"{BASE}/{hotel.id}").json()["estrelas"] == 4


def test_atualizar_hotel_como_admin(client, admin, hotel):
    resposta = client.put(f"{BASE}/{hotel.id}", json={"estrelas": 5}, headers=admin)

    assert resposta.status_code == 200
    assert resposta.json()["estrelas"] == 5


def test_excluir_hotel_sem_token_e_bloqueado(client, hotel):
    resposta = client.delete(f"{BASE}/{hotel.id}")

    assert resposta.status_code in (401, 403)
    assert client.get(f"{BASE}/{hotel.id}").status_code == 200


def test_excluir_hotel_como_admin_retorna_204(client, admin, hotel):
    resposta = client.delete(f"{BASE}/{hotel.id}", headers=admin)

    assert resposta.status_code == 204
    assert client.get(f"{BASE}/{hotel.id}").status_code == 404


def test_excluir_hotel_inexistente_retorna_404(client, admin):
    resposta = client.delete(f"{BASE}/{uuid.uuid4()}", headers=admin)

    assert resposta.status_code == 404
