from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.hotel import HotelCreateSchema, HotelResponseSchema, HotelUpdateSchema
from app.services.hotel_service import (
    CidadeNaoEncontradaError,
    HotelNaoEncontradoError,
    HotelService,
)

router = APIRouter(prefix="/hoteis", tags=["Hotéis"])


@router.post(
    "",
    response_model=HotelResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um hotel",
)
def criar_hotel(
    payload: HotelCreateSchema,
    db: Session = Depends(get_db),
):
    service = HotelService(db)

    try:
        return service.criar(
            nome=payload.nome,
            cidade_id=payload.cidade_id,
            estrelas=payload.estrelas,
        )
    except CidadeNaoEncontradaError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[HotelResponseSchema],
    summary="Lista os hotéis",
)
def listar_hoteis(db: Session = Depends(get_db)):
    return HotelService(db).listar()


@router.get(
    "/{hotel_id}",
    response_model=HotelResponseSchema,
    summary="Busca um hotel pelo ID",
)
def buscar_hotel(
    hotel_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return HotelService(db).buscar_por_id(hotel_id)
    except HotelNaoEncontradoError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{hotel_id}",
    response_model=HotelResponseSchema,
    summary="Atualiza um hotel",
)
def atualizar_hotel(
    hotel_id: UUID,
    payload: HotelUpdateSchema,
    db: Session = Depends(get_db),
):
    service = HotelService(db)

    try:
        return service.atualizar(
            hotel_id=hotel_id,
            nome=payload.nome,
            cidade_id=payload.cidade_id,
            estrelas=payload.estrelas,
        )
    except HotelNaoEncontradoError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CidadeNaoEncontradaError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{hotel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Exclui um hotel",
)
def excluir_hotel(
    hotel_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        HotelService(db).excluir(hotel_id)
    except HotelNaoEncontradoError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc