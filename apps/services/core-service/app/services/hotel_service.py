import uuid

from sqlalchemy.orm import Session

from app.models.hotel import Hotel
from app.repositories.cidade_repository import CidadeRepository
from app.repositories.hotel_repository import HotelRepository


class RegraDeNegocioError(Exception):
    """Base das excecoes de negocio deste modulo."""


class HotelNaoEncontradoError(RegraDeNegocioError):
    pass


class CidadeNaoEncontradaError(RegraDeNegocioError):
    pass


class HotelService:
    def __init__(self, db: Session):
        self.repository = HotelRepository(db)
        self.cidade_repository = CidadeRepository(db)

    def criar(
        self,
        nome: str,
        cidade_id: uuid.UUID,
        estrelas: int,
    ) -> Hotel:
        nome = nome.strip()

        cidade = self.cidade_repository.get_by_id(cidade_id)

        if cidade is None:
            raise CidadeNaoEncontradaError(
                f"Cidade com id '{cidade_id}' não encontrada."
            )

        hotel = Hotel(
            nome=nome,
            cidade_id=cidade_id,
            estrelas=estrelas,
        )

        return self.repository.create(hotel)

    def listar(self) -> list[Hotel]:
        return self.repository.list()

    def buscar_por_id(self, hotel_id: uuid.UUID) -> Hotel:
        hotel = self.repository.get_by_id(hotel_id)

        if hotel is None:
            raise HotelNaoEncontradoError(
                f"Hotel com id '{hotel_id}' não encontrado."
            )

        return hotel

    def atualizar(
        self,
        hotel_id: uuid.UUID,
        nome: str | None = None,
        cidade_id: uuid.UUID | None = None,
        estrelas: int | None = None,
    ) -> Hotel:
        hotel = self.buscar_por_id(hotel_id)

        if nome is not None:
            hotel.nome = nome.strip()

        if cidade_id is not None:
            cidade = self.cidade_repository.get_by_id(cidade_id)

            if cidade is None:
                raise CidadeNaoEncontradaError(
                    f"Cidade com id '{cidade_id}' não encontrada."
                )

            hotel.cidade_id = cidade_id

        if estrelas is not None:
            hotel.estrelas = estrelas

        return self.repository.update(hotel)

    def excluir(self, hotel_id: uuid.UUID) -> None:
        hotel = self.buscar_por_id(hotel_id)
        self.repository.delete(hotel)