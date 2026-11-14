import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.hotel import Cidade, Hotel
from app.repositories.usuario_repository import UsuarioRepository

logger = logging.getLogger(__name__)

# Cidade -> [(hotel, estrelas)]. O seed garante que cada par exista, sem
# duplicar o que ja estiver no banco.
CIDADES_E_HOTEIS: dict[str, list[tuple[str, int]]] = {
    "Fortaleza": [("Hotel Resort", 1), ("Hotel Aquiraz", 2)],
    "Quixadá": [("Hotel Beira Mar", 3), ("Hotel Paraíso", 4)],
    "Juazeiro do Norte": [("Hotel Premium", 5)],
}


def seed_admin_user(db: Session) -> bool:
    """Cria o administrador inicial. Devolve True se criou."""
    repository = UsuarioRepository(db)

    if repository.get_by_email(settings.ADMIN_EMAIL) is not None:
        logger.info("Usuario administrador ja existe.")
        return False

    repository.create(
        nome=settings.ADMIN_NAME,
        email=settings.ADMIN_EMAIL,
        senha_hash=hash_password(settings.ADMIN_PASSWORD),
        is_admin=True,
    )
    logger.info("Usuario administrador criado com sucesso.")
    return True


def seed_cidades_e_hoteis(db: Session) -> int:
    """Garante as cidades e hoteis de exemplo. Devolve quantos hoteis criou.

    Idempotente por nome: rodar de novo nao duplica, e uma cidade cadastrada
    antes do seed nao impede que os hoteis dela sejam criados.
    """
    criados = 0

    try:
        for nome_cidade, hoteis in CIDADES_E_HOTEIS.items():
            cidade = db.query(Cidade).filter(Cidade.nome == nome_cidade).first()

            if cidade is None:
                cidade = Cidade(nome=nome_cidade)
                db.add(cidade)
                db.flush()

            for nome_hotel, estrelas in hoteis:
                existe = (
                    db.query(Hotel.id)
                    .filter(Hotel.nome == nome_hotel, Hotel.cidade_id == cidade.id)
                    .first()
                )

                if existe is None:
                    db.add(
                        Hotel(nome=nome_hotel, cidade_id=cidade.id, estrelas=estrelas)
                    )
                    criados += 1

        db.commit()
    except Exception:
        db.rollback()
        raise

    logger.info("Seed de cidades e hoteis: %d hotel(is) criado(s).", criados)
    return criados


def main() -> None:
    db = SessionLocal()

    try:
        seed_admin_user(db)
        seed_cidades_e_hoteis(db)
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[seed_postgres] %(message)s")
    main()
