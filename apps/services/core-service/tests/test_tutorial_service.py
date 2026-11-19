import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.models.tutorial import Disciplina, Linguagem, Professor, Stack, Tecnologia
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
    assert dados["ano"] == 2026
    assert dados["semestre"] == 2
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


def test_sobre_traz_professor_sem_detalhe_cadastrado(db_session):
    prof = Professor(nome="Docente Sem Detalhe", email="docente@unicatolica.edu.br")
    db_session.add(prof)
    db_session.commit()

    dados = TutorialService(db_session).get_sobre_data()

    assert dados["professor"]["nome"] == "Docente Sem Detalhe"
    assert dados["professor"]["sala"] == ""
    assert dados["professor"]["biografia"] == ""
    assert dados["professor"]["biografia_mapa"] is None


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


def test_get_professor_by_id_encontrado_e_inexistente(db_session):
    prof = _professor(db_session)
    service = TutorialService(db_session)

    encontrado = service.get_professor_by_id(str(prof.id))
    assert encontrado is not None
    assert encontrado["nome"] == "Ronildo Silva"
    assert encontrado["email"] == "ronildo@unicatolica.edu.br"
    assert encontrado["sala"] == "Sala 07"

    assert service.get_professor_by_id(uuid.uuid4()) is None
    assert service.get_professor_by_id("uuid-invalido") is None


def test_create_professor_normaliza_campos_e_valida_obrigatorios(db_session):
    service = TutorialService(db_session)
    payload = SimpleNamespace(
        nome="  Maria Oliveira  ",
        email="  maria@unicatolica.edu.br  ",
        sala="  Lab 03  ",
        biografia="Pesquisadora",
        biografia_mapa={"lattes": "https://lattes.cnpq.br"},
    )

    criado = service.create_professor(payload)

    assert criado["nome"] == "Maria Oliveira"
    assert criado["email"] == "maria@unicatolica.edu.br"
    assert criado["sala"] == "Lab 03"
    assert criado["biografia_mapa"] == {"lattes": "https://lattes.cnpq.br"}

    invalido = SimpleNamespace(nome="   ", email="a@b.com", sala="Sala 1")
    with pytest.raises(ValueError):
        service.create_professor(invalido)


@patch("app.services.tutorial_service.publish_event", new_callable=AsyncMock)
def test_criar_disciplina_publica_evento_de_auditoria(mock_publish, db_session):
    prof = _professor(db_session)
    payload = SimpleNamespace(
        nome="  Redes  ", ano=2026, semestre=1, professor_id=prof.id
    )

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


@patch("app.services.tutorial_service.publish_event", new_callable=AsyncMock)
def test_criar_disciplina_recusa_nome_em_branco(mock_publish, db_session):
    prof = _professor(db_session)
    payload = SimpleNamespace(nome="   ", ano=2026, semestre=1, professor_id=prof.id)

    with pytest.raises(ValueError):
        asyncio.run(TutorialService(db_session).create_disciplina(payload))

    mock_publish.assert_not_awaited()
