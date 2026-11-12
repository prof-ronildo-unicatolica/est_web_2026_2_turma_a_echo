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
)
from app.services.tutorial_service import TutorialService

router = APIRouter()

SessaoDep = Annotated[Session, Depends(get_db)]


@router.get("/sobre", response_model=SobreResponseSchema)
def get_sobre(db: SessaoDep):
    return TutorialService(db).get_sobre_data()


@router.get(
    "/sobre/professores/{professor_id}",
    response_model=ProfessorBaseSchema,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Professor não encontrado"}},
)
def get_professor_por_id(professor_id: uuid.UUID, db: SessaoDep):
    prof = TutorialService(db).get_professor_by_id(professor_id)
    if not prof:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Professor nao encontrado"
        )
    return prof


@router.post(
    "/sobre/disciplinas",
    response_model=DisciplinaResponseSimpleSchema,
    status_code=status.HTTP_201_CREATED,
)
async def criar_disciplina(payload: DisciplinaCreateSchema, db: SessaoDep):
    return await TutorialService(db).create_disciplina(payload)


@router.get("/debug/error")
def trigger_error():
    raise RuntimeError("Erro imprevisto de conexao com gateway ou hardware.")
