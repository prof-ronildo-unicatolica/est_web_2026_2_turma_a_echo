import uuid
from unittest.mock import AsyncMock, patch

from app.repositories.tutorial_repository import TutorialRepository

DISCIPLINAS = "/api/v1/sobre/disciplinas"


def test_criar_disciplina_sem_professor_id_retorna_422(client):
    resposta = client.post(
        DISCIPLINAS, json={"nome": "Web", "ano": 2026, "semestre": 2}
    )

    assert resposta.status_code == 422
    assert resposta.json()["detail"][0]["loc"] == ["body", "professor_id"]


def test_criar_disciplina_com_professor_id_que_nao_e_uuid_retorna_422(client):
    resposta = client.post(
        DISCIPLINAS,
        json={"nome": "Web", "ano": 2026, "semestre": 2, "professor_id": "abc"},
    )

    assert resposta.status_code == 422


@patch("app.services.tutorial_service.publish_event", new_callable=AsyncMock)
def test_criar_disciplina_devolve_ids_como_uuid(mock_publish, client, db_session):
    prof = TutorialRepository(db_session).create_professor(
        nome="Prof", email="prof@unicatolica.edu.br", sala="Sala 1"
    )

    resposta = client.post(
        DISCIPLINAS,
        json={"nome": "Web", "ano": 2026, "semestre": 2, "professor_id": str(prof.id)},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert uuid.UUID(corpo["id"])
    assert corpo["professor_id"] == str(prof.id)
