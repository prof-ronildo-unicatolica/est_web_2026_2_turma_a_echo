import uuid

from sqlalchemy.orm import Session

from app.models.hotel import Cidade
from app.repositories.cidade_repository import CidadeRepository


class RegraDeNegocioError(Exception):
    """Base das excecoes de negocio deste modulo."""


class CidadeJaExisteError(RegraDeNegocioError):
    pass


class CidadeNaoEncontradaError(RegraDeNegocioError):
    pass


class CidadeService:
    def __init__(self, db: Session):
        self.repository = CidadeRepository(db)

    def criar(self, nome: str) -> Cidade:
        nome = nome.strip()

        if self.repository.get_by_nome(nome):
            raise CidadeJaExisteError(
                f"Ja existe uma cidade chamada '{nome}'."
            )

        return self.repository.create(nome=nome)

    def listar(self) -> list[Cidade]:
        return self.repository.list()

    def buscar_por_id(self, cidade_id: uuid.UUID) -> Cidade | None:
        return self.repository.get_by_id(cidade_id)