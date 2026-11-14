import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.schemas.hotel import HotelCreateSchema, HotelResponseSchema, HotelUpdateSchema
from app.services.hotel_service import (
    CidadeNaoEncontradaError,
    HotelNaoEncontradoError,
    HotelService,
)

router = APIRouter(prefix="/hoteis", tags=["Hotéis"])

SessaoDep = Annotated[Session, Depends(get_db)]

# Escrita de hotel e area administrativa: a leitura continua publica.
SOMENTE_ADMIN = [Depends(get_current_admin)]

RESPOSTA_NAO_ENCONTRADO = {
    status.HTTP_404_NOT_FOUND: {"description": "Hotel ou cidade não encontrado"},
}
RESPOSTAS_ADMIN = {
    status.HTTP_401_UNAUTHORIZED: {"description": "Token inválido ou expirado"},
    status.HTTP_403_FORBIDDEN: {
        "description": "Token ausente ou usuário sem perfil de administrador",
    },
}


def _nao_encontrado(exc: Exception) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post(
    "",
    response_model=HotelResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um hotel",
    dependencies=SOMENTE_ADMIN,
    responses={**RESPOSTA_NAO_ENCONTRADO, **RESPOSTAS_ADMIN},
)
def criar_hotel(payload: HotelCreateSchema, db: SessaoDep):
    try:
        return HotelService(db).criar(
            nome=payload.nome,
            cidade_id=payload.cidade_id,
            estrelas=payload.estrelas,
        )
    except CidadeNaoEncontradaError as exc:
        raise _nao_encontrado(exc) from exc


@router.get(
    "",
    response_model=list[HotelResponseSchema],
    summary="Lista os hotéis, opcionalmente filtrados por cidade",
    responses=RESPOSTA_NAO_ENCONTRADO,
)
def listar_hoteis(
    db: SessaoDep,
    cidade_id: Annotated[
        uuid.UUID | None,
        Query(description="Filtra os hotéis de uma cidade específica"),
    ] = None,
):
    try:
        return HotelService(db).listar(cidade_id=cidade_id)
    except CidadeNaoEncontradaError as exc:
        raise _nao_encontrado(exc) from exc


@router.get(
    "/{hotel_id}",
    response_model=HotelResponseSchema,
    summary="Busca um hotel pelo ID",
    responses=RESPOSTA_NAO_ENCONTRADO,
)
def buscar_hotel(hotel_id: uuid.UUID, db: SessaoDep):
    try:
        return HotelService(db).buscar_por_id(hotel_id)
    except HotelNaoEncontradoError as exc:
        raise _nao_encontrado(exc) from exc


@router.put(
    "/{hotel_id}",
    response_model=HotelResponseSchema,
    summary="Atualiza um hotel",
    dependencies=SOMENTE_ADMIN,
    responses={**RESPOSTA_NAO_ENCONTRADO, **RESPOSTAS_ADMIN},
)
def atualizar_hotel(hotel_id: uuid.UUID, payload: HotelUpdateSchema, db: SessaoDep):
    try:
        return HotelService(db).atualizar(
            hotel_id=hotel_id,
            nome=payload.nome,
            cidade_id=payload.cidade_id,
            estrelas=payload.estrelas,
        )
    except (HotelNaoEncontradoError, CidadeNaoEncontradaError) as exc:
        raise _nao_encontrado(exc) from exc


@router.delete(
    "/{hotel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Exclui um hotel",
    dependencies=SOMENTE_ADMIN,
    responses={**RESPOSTA_NAO_ENCONTRADO, **RESPOSTAS_ADMIN},
)
def excluir_hotel(hotel_id: uuid.UUID, db: SessaoDep):
    try:
        HotelService(db).excluir(hotel_id)
    except HotelNaoEncontradoError as exc:
        raise _nao_encontrado(exc) from exc
