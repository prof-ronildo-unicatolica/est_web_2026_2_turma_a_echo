import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.models.tutorial import Disciplina, Linguagem, Stack, Tecnologia
from app.repositories.tutorial_repository import TutorialRepository
from app.services.tutorial_service import TutorialService


def _professor(db_session):
    return TutorialRepository(db_session).create_professor(
        nome="Ronildo Silva",
        email="ronildo@unicatolica.edu.br",
        sala="Sala 07",
        biografia="Professor",
    )


def test_sobre_sem_professor_devolve_estrutura_vazia(db_session):
    dados = TutorialService(db_session).get_sobre_data()

    assert dados["equipe"] == "Echo"
    assert dados["professor"] is None
    assert dados["disciplinas"] == []
    assert dados["stacks"] == []


def test_sobre_traz_professor_e_disciplinas_com_tecnologias(db_session):
    prof = _professor(db_session)
    backend = Stack(nome="Backend")
    fastapi = Tecnologia(nome="FastAPI", stack=backend)
    db_session.add(
        Disciplina(
            nome="Web",
            ano=2026,
            semestre=2,
            professor_id=prof.id,
            tecnologias=[fastapi],
        )
    )
    db_session.commit()

    dados = TutorialService(db_session).get_sobre_data()

    assert dados["professor"]["nome"] == "Ronildo Silva"
    assert dados["professor"]["sala"] == "Sala 07"
    assert dados["disciplinas"] == [
        {"nome": "Web", "ano": 2026, "semestre": 2, "tecnologias": ["FastAPI"]}
    ]


def test_sobre_traz_stacks_com_tecnologias_e_linguagens(db_session):
    python = Linguagem(nome="Python")
    db_session.add(
        Stack(
            nome="Backend",
            tecnologias=[Tecnologia(nome="FastAPI", linguagens=[python])],
        )
    )
    db_session.commit()

    dados = TutorialService(db_session).get_sobre_data()

    assert dados["stacks"] == [
        {
            "nome": "Backend",
            "tecnologias": [{"nome": "FastAPI", "linguagens": ["Python"]}],
        }
    ]


@patch("app.services.tutorial_service.publish_event", new_callable=AsyncMock)
def test_criar_disciplina_publica_evento_de_auditoria(mock_publish, db_session):
    prof = _professor(db_session)
    payload = SimpleNamespace(nome="Redes", ano=2026, semestre=1, professor_id=prof.id)

    disciplina = asyncio.run(TutorialService(db_session).create_disciplina(payload))

    fila, evento = mock_publish.await_args.args
    assert fila == "audit.logs"
    assert evento == {
        "evento": "disciplina.criada",
        "disciplina_id": str(disciplina.id),
        "nome": "Redes",
        "ano": 2026,
        "semestre": 1,
        "professor_id": str(prof.id),
    }
