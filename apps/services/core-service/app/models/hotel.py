import uuid
from typing import List

from sqlalchemy import String, ForeignKey, Integer, Float, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tutorial import Base


class Cidade(Base):
    __tablename__ = "cidades"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    hoteis: Mapped[List["Hotel"]] = relationship(
        "Hotel", back_populates="cidade", cascade="all, delete-orphan"
    )


class Hotel(Base):
    __tablename__ = "hoteis"

    __table_args__ = (
        UniqueConstraint(
            "fonte",
            "external_id",
            name="uq_hoteis_fonte_external_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    cidade_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cidades.id", ondelete="CASCADE"),
        nullable=False,
    )
    estrelas: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

   
    external_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    
    fonte: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    endereco: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    telefone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    imagem_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    cidade: Mapped["Cidade"] = relationship(
        "Cidade",
        back_populates="hoteis",
    )
