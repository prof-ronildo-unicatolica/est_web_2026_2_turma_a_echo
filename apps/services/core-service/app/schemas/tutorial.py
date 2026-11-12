import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class ProfessorBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    email: str
    sala: str
    biografia: Optional[str] = None
    biografia_mapa: Optional[Dict[str, Any]] = None


class DisciplinaResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    ano: int
    semestre: int
    tecnologias: List[str]


class TecnologiaResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    linguagens: List[str]


class StackResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    tecnologias: List[TecnologiaResponseSchema]


class SobreResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    equipe: str
    ano: int
    semestre: int
    professor: Optional[ProfessorBaseSchema] = None
    disciplinas: List[DisciplinaResponseSchema]
    stacks: List[StackResponseSchema]


class ProfessorCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    email: str
    sala: str
    biografia: Optional[str] = None
    biografia_mapa: Optional[Dict[str, Any]] = None


class DisciplinaCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    ano: int
    semestre: int
    # Obrigatorio: sem ele a disciplina era atribuida em silencio ao professor
    # do seed.
    professor_id: uuid.UUID


class DisciplinaResponseSimpleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    ano: int
    semestre: int
    professor_id: uuid.UUID
