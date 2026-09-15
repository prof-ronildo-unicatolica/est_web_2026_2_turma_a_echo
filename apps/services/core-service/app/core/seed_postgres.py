from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.repositories.usuario_repository import UsuarioRepository
from app.models.hotel import Cidade, Hotel


def seed_admin_user() -> None:
    db = SessionLocal()

    try:
        repository = UsuarioRepository(db)

        usuario = repository.get_by_email(settings.ADMIN_EMAIL)

        if usuario is not None:
            print("Usuario administrador ja existe.")
            return

        repository.create(
            nome=settings.ADMIN_NAME,
            email=settings.ADMIN_EMAIL,
            senha_hash=hash_password(settings.ADMIN_PASSWORD),
            is_admin=True,
        )

        print("Usuario administrador criado com sucesso.")

    finally:
        db.close()

def seed_cidades_e_hoteis() -> None:
    db = SessionLocal()

    try:
        if db.query(Cidade).count() > 0:
            print("Cidades e hoteis já existem.")
            return

        cidade1 = Cidade(nome="Fortaleza")
        cidade2 = Cidade(nome="Quixadá")
        cidade3 = Cidade(nome="Juazeiro do Norte")

        db.add_all([cidade1, cidade2, cidade3])
        db.flush()

        hoteis = [
            Hotel(
                nome="Hotel Resort",
                cidade_id=cidade1.id,
                estrelas=1,
            ),
            Hotel(
                nome="Hotel Aquiraz",
                cidade_id=cidade1.id,
                estrelas=2,
            ),
            Hotel(
                nome="Hotel Beira Mar",
                cidade_id=cidade2.id,
                estrelas=3,
            ),
            Hotel(
                nome="Hotel Paraíso",
                cidade_id=cidade2.id,
                estrelas=4,
            ),
            Hotel(
                nome="Hotel Premium",
                cidade_id=cidade3.id,
                estrelas=5,
            ),
        ]

        db.add_all(hoteis)
        db.commit()

        print("Cidades e hoteis criados com sucesso.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_admin_user()
    seed_cidades_e_hoteis()