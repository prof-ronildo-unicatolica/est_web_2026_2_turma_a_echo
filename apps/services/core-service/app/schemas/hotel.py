import uuid
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CidadeCreateSchema(BaseModel):
    """O que o cliente envia em POST /cidades."""

    nome: str = Field(min_length=1, max_length=100)


class CidadeResponseSchema(BaseModel):
    """O que a API devolve para uma cidade."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class HotelCreateSchema(BaseModel):
    """Dados necessarios para criar um hotel.

    A cidade entra como ID para evitar ambiguidade entre reutilizar uma cidade
    existente ou criar uma nova.
    """

    nome: str = Field(min_length=1, max_length=100)
    cidade_id: uuid.UUID
    estrelas: int = Field(ge=1, le=5)


class HotelUpdateSchema(BaseModel):
    """Dados permitidos para atualizar um hotel."""

    nome: str | None = Field(default=None, min_length=1, max_length=100)
    cidade_id: uuid.UUID | None = None
    estrelas: int | None = Field(default=None, ge=1, le=5)


class HotelResumoSchema(BaseModel):
    """Representacao compacta de hotel sem repetir o objeto cidade."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    estrelas: int


class HotelResponseSchema(BaseModel):
    """Dados retornados pela API de hoteis com a cidade aninhada."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    cidade_id: uuid.UUID
    estrelas: int
    cidade: CidadeResponseSchema


class CidadeComHoteisSchema(CidadeResponseSchema):
    """Cidade com a lista de hoteis aninhada (Issue #11).

    Usada onde a listagem de hoteis da cidade for solicitada explicitamente.
    """

    hoteis: List[HotelResponseSchema] = Field(default_factory=list)
