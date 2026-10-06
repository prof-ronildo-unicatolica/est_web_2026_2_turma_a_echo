import uuid

from pydantic import BaseModel, ConfigDict, Field


class CidadeCreateSchema(BaseModel):
    """O que o cliente envia em POST /cidades."""

    nome: str = Field(min_length=1, max_length=100)


class CidadeResponseSchema(BaseModel):
    """O que a API devolve."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str

class HotelCreateSchema(BaseModel):
    """Dados necessários para criar um hotel."""

    nome: str = Field(min_length=1, max_length=100)
    cidade_id: uuid.UUID
    estrelas: int = Field(ge=1, le=5)


class HotelUpdateSchema(BaseModel):
    """Dados permitidos para atualizar um hotel."""

    nome: str | None = Field(default=None, min_length=1, max_length=100)
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