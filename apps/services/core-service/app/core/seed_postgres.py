from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.repositories.usuario_repository import UsuarioRepository


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


if __name__ == "__main__":
    seed_admin_user()