import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.hotel import Cidade, Hotel


class CidadeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, nome: str) -> Cidade:
        cidade = Cidade(nome=nome.strip())

        self.db.add(cidade)
        self.db.commit()
        self.db.refresh(cidade)

        return cidade

    def list(self) -> list[Cidade]:
        return self.db.query(Cidade).order_by(Cidade.nome).all()

    def list_with_hoteis(self) -> list[Cidade]:
        return (
            self.db.query(Cidade)
            .options(joinedload(Cidade.hoteis).joinedload(Hotel.cidade))
            .order_by(Cidade.nome)
            .all()
        )

    def get_by_id(self, cidade_id: uuid.UUID) -> Cidade | None:
        return self.db.query(Cidade).filter(Cidade.id == cidade_id).first()

    def get_with_hoteis(self, cidade_id: uuid.UUID) -> Cidade | None:
        return (
            self.db.query(Cidade)
            .options(joinedload(Cidade.hoteis).joinedload(Hotel.cidade))
            .filter(Cidade.id == cidade_id)
            .first()
        )

    def get_by_nome(self, nome: str) -> Cidade | None:
        return self.db.query(Cidade).filter(Cidade.nome == nome).first()

    def get_by_nome_case_insensitive(self, nome: str) -> Cidade | None:
        nome_limpo = nome.strip().lower()
        return (
            self.db.query(Cidade)
            .filter(func.lower(Cidade.nome) == nome_limpo)
            .first()
        )

    def count_hoteis(self, cidade_id: uuid.UUID) -> int:
        total = (
            self.db.query(func.count(Hotel.id))
            .filter(Hotel.cidade_id == cidade_id)
            .scalar()
        )
        return int(total or 0)

    def delete(self, cidade: Cidade) -> None:
        self.db.delete(cidade)
        self.db.commit()
