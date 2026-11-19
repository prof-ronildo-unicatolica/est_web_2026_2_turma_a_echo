import uuid
from unittest.mock import patch

from app.models.hotel import Cidade
from app.models.tutorial import Disciplina, Linguagem, Stack, Tecnologia
from app.repositories.tutorial_repository import TutorialRepository


def test_get_sobre_returns_200(client, db_session):
    repo = TutorialRepository(db_session)
    repo.create_professor(
        nome="Ronildo Silva",
        email="ronildo@ufc.br",
        sala="Sala 07",
        biografia="Professor",
    )

    response = client.get("/api/v1/sobre")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["equipe"] == "Echo"
    assert json_data["professor"]["nome"] == "Ronildo Silva"


def test_get_sobre_inclui_stacks_e_disciplinas(client, db_session):
    repo = TutorialRepository(db_session)
    prof = repo.create_professor(
        nome="Docente Echo",
        email="docente.echo@unicatolica.edu.br",
        sala="Bloco A",
        biografia="Pesquisador Web",
    )
    python = Linguagem(nome="Python")
    stack = Stack(
        nome="Backend",
        tecnologias=[Tecnologia(nome="FastAPI", linguagens=[python])],
    )
    db_session.add(stack)
    db_session.add(
        Disciplina(
            nome="Desenvolvimento Web",
            ano=2026,
            semestre=2,
            professor_id=prof.id,
        )
    )
    db_session.commit()

    response = client.get("/api/v1/sobre")
    assert response.status_code == 200
    body = response.json()
    assert len(body["stacks"]) == 1
    assert body["stacks"][0]["nome"] == "Backend"
    assert len(body["disciplinas"]) == 1
    assert body["disciplinas"][0]["nome"] == "Desenvolvimento Web"


def test_get_professor_inexistente_returns_404(client):
    id_fake = uuid.uuid4()
    response = client.get(f"/api/v1/sobre/professores/{id_fake}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Professor nao encontrado"


@patch("app.services.tutorial_service.publish_event")
def test_criar_disciplina_returns_201(mock_publish, client, db_session):
    repo = TutorialRepository(db_session)
    prof = repo.create_professor(
        nome="Ronildo Silva",
        email="ronildo@ufc.br",
        sala="Sala 07",
        biografia="Professor",
    )
    payload = {
        "nome": "Inteligencia Artificial",
        "ano": 2026,
        "semestre": 2,
        "professor_id": str(prof.id),
    }
    response = client.post("/api/v1/sobre/disciplinas", json=payload)
    assert response.status_code == 201
    assert response.json()["nome"] == "Inteligencia Artificial"
    mock_publish.assert_called_once()


def test_criar_disciplina_com_dados_invalidos_returns_422(client):
    payload = {
        "nome": "Disciplina Sem Ano",
        "semestre": 2,
    }
    response = client.post("/api/v1/sobre/disciplinas", json=payload)
    assert response.status_code == 422


def test_buscar_cidade_por_id_returns_200_e_404(client, db_session):
    cidade = Cidade(nome="Quixada")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    resp_ok = client.get(f"/api/v1/cidades/{cidade.id}")
    assert resp_ok.status_code == 200
    assert resp_ok.json()["nome"] == "Quixada"

    resp_404 = client.get(f"/api/v1/cidades/{uuid.uuid4()}")
    assert resp_404.status_code == 404
    assert resp_404.json()["detail"] == "Cidade nao encontrada"


def test_trigger_server_error_returns_500(client):
    response = client.get("/api/v1/debug/error")
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
