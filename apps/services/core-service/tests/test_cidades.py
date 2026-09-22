from app.models.hotel import Cidade

BASE = "/api/v1/cidades"


def test_criar_cidade_retorna_201(client, db_session):
    response = client.post(
        BASE,
        json={"nome": "Sobral"},
    )

    assert response.status_code == 201

    body = response.json()

    assert body["id"]
    assert body["nome"] == "Sobral"

    cidade = (
        db_session.query(Cidade)
        .filter(Cidade.nome == "Sobral")
        .first()
    )

    assert cidade is not None


def test_criar_cidade_duplicada_retorna_409(client):
    primeira = client.post(
        BASE,
        json={"nome": "Fortaleza"},
    )

    assert primeira.status_code == 201

    segunda = client.post(
        BASE,
        json={"nome": "Fortaleza"},
    )

    assert segunda.status_code == 409


def test_criar_cidade_com_nome_vazio_retorna_422(client):
    response = client.post(
        BASE,
        json={"nome": ""},
    )

    assert response.status_code == 422


def test_listar_cidades_retorna_ordem_alfabetica(client, db_session):
    db_session.add_all(
        [
            Cidade(nome="Sobral"),
            Cidade(nome="Fortaleza"),
            Cidade(nome="Quixada"),
        ]
    )
    db_session.commit()

    response = client.get(BASE)

    assert response.status_code == 200

    body = response.json()

    assert [cidade["nome"] for cidade in body] == [
        "Fortaleza",
        "Quixada",
        "Sobral",
    ]