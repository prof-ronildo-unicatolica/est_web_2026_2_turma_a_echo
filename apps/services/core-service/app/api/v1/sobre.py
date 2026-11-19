import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.tutorial import (
    DisciplinaCreateSchema,
    DisciplinaResponseSimpleSchema,
    ProfessorBaseSchema,
    SobreResponseSchema,
    StackResponseSchema,
)
from app.services.tutorial_service import TutorialService

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]


@router.get(
    "/sobre",
    response_model=SobreResponseSchema,
    summary="Retorna dados institucionais da equipe, professor, disciplinas e stacks",
)
def get_sobre(db: DbSession):
    service = TutorialService(db)
    return service.get_sobre_data()


@router.get(
    "/sobre/stacks",
    response_model=list[StackResponseSchema],
    summary="Lista as stacks tecnologicas e suas respectivas linguagens",
)
def get_sobre_stacks(db: DbSession):
    service = TutorialService(db)
    dados = service.get_sobre_data()
    return dados["stacks"]


@router.get(
    "/sobre/professores/{professor_id}",
    response_model=ProfessorBaseSchema,
    summary="Busca professor pelo identificador",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Professor nao encontrado"},
    },
)
def get_professor_por_id(
    professor_id: uuid.UUID,
    db: DbSession,
):
    service = TutorialService(db)
    prof = service.get_professor_by_id(professor_id)
    if not prof:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor nao encontrado",
        )
    return prof


@router.post(
    "/sobre/disciplinas",
    response_model=DisciplinaResponseSimpleSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra uma nova disciplina e publica evento de auditoria",
)
async def criar_disciplina(
    payload: DisciplinaCreateSchema,
    db: DbSession,
):
    service = TutorialService(db)
    return await service.create_disciplina(payload)


@router.get("/debug/error")
def trigger_error():
    raise RuntimeError("Erro imprevisto de conexao com gateway ou hardware.")
