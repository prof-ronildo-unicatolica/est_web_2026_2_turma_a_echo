import uuid

from sqlalchemy.orm import Session

from app.models.hotel import Hotel

class HotelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, hotel: Hotel) -> Hotel:
        self.db.add(hotel)
        self.db.commit()
        self.db.refresh(hotel)

        return hotel

    def list(self) -> list[Hotel]:
        return (
            self.db.query(Hotel)
            .order_by(Hotel.nome)
            .all()
        )

    def get_by_id(self, hotel_id: uuid.UUID) -> Hotel | None:
        return (
            self.db.query(Hotel)
            .filter(Hotel.id == hotel_id)
            .first()
        )

    def update(self, hotel: Hotel) -> Hotel:
        self.db.commit()
        self.db.refresh(hotel)

        return hotel

    def delete(self, hotel: Hotel) -> None:
        self.db.delete(hotel)
        self.db.commit()