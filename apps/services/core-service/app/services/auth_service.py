from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository


class AuthService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def register(
        self,
        nome: str,
        email: str,
        senha: str,
    ) -> Usuario | None:
        if self.repository.email_exists(email):
            return None

        senha_hash = hash_password(senha)

        return self.repository.create(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            is_admin=False,
        )

    def login(
        self,
        email: str,
        senha: str,
    ) -> str | None:
        usuario = self.repository.get_by_email(email)

        if usuario is None:
            return None

        if not verify_password(senha, usuario.senha_hash):
            return None

        return create_access_token(subject=usuario.email)