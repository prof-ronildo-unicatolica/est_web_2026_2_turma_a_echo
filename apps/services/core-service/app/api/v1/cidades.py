import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.hotel import CidadeCreateSchema, CidadeResponseSchema
from app.services.cidade_service import CidadeJaExisteError, CidadeService

router = APIRouter(prefix="/cidades", tags=["Cidades"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=CidadeResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma cidade",
    responses={
        status.HTTP_409_CONFLICT: {"description": "Cidade com mesmo nome ja cadastrada"},
    },
)
def criar_cidade(
    payload: CidadeCreateSchema,
    db: DbSession,
):
    service = CidadeService(db)

    try:
        return service.criar(nome=payload.nome)
    except CidadeJaExisteError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[CidadeResponseSchema],
    summary="Lista as cidades em ordem alfabetica",
)
def listar_cidades(db: DbSession):
    return CidadeService(db).listar()


@router.get(
    "/{cidade_id}",
    response_model=CidadeResponseSchema,
    summary="Busca uma cidade pelo identificador",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Cidade nao encontrada"},
    },
)
def buscar_cidade_por_id(
    cidade_id: uuid.UUID,
    db: DbSession,
):
    cidade = CidadeService(db).buscar_por_id(cidade_id)
    if cidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cidade nao encontrada",
        )
    return cidade
