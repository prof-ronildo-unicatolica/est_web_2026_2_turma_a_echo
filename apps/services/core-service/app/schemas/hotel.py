import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

# Remove os espacos das pontas ANTES de medir o tamanho: assim "   " vira ""
# e cai no min_length, em vez de passar na validacao e gravar um nome vazio.
Nome = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]


class CidadeCreateSchema(BaseModel):
    """O que o cliente envia em POST /cidades."""

    nome: Nome


class CidadeResponseSchema(BaseModel):
    """O que a API devolve."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class HotelCreateSchema(BaseModel):
    """Dados necessários para criar um hotel."""

    nome: Nome
    cidade_id: uuid.UUID
    estrelas: int = Field(ge=1, le=5)


class HotelUpdateSchema(BaseModel):
    """Dados permitidos para atualizar um hotel."""

    nome: Nome | None = None
    cidade_id: uuid.UUID | None = None
    estrelas: int | None = Field(default=None, ge=1, le=5)


class HotelResponseSchema(BaseModel):
    """Dados retornados pela API de hotéis."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    cidade_id: uuid.UUID
    estrelas: int
    cidade: CidadeResponseSchema
