import uuid

from app.models.hotel import Cidade
from app.repositories.hotel_repository import (
    CidadeRepository as HotelCidadeRepository,
)


class CidadeRepository(HotelCidadeRepository):
    """Compatibilidade temporaria com o service antigo de Cidade."""

    def listar(self) -> list[Cidade]:
        return self.list()

    def buscar_por_id(self, cidade_id: uuid.UUID) -> Cidade | None:
        return self.get_by_id(cidade_id)

    def criar(self, nome: str) -> Cidade:
        return self.create(nome)


__all__ = ["CidadeRepository"]