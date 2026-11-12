from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository

bearer_scheme = HTTPBearer(description="Use o token retornado por POST /auth/login")

CredenciaisDep = Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]
SessaoDep = Annotated[Session, Depends(get_db)]


def _nao_autorizado(detalhe: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detalhe,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(credentials: CredenciaisDep, db: SessaoDep) -> Usuario:
    """Retorna o usuario autenticado a partir de um JWT valido."""

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.InvalidTokenError as exc:
        raise _nao_autorizado("Token invalido ou expirado") from exc

    email = payload.get("sub")

    if not email:
        raise _nao_autorizado("Token invalido")

    usuario = UsuarioRepository(db).get_by_email(email)

    if usuario is None:
        raise _nao_autorizado("Usuario nao encontrado")

    return usuario


UsuarioAtualDep = Annotated[Usuario, Depends(get_current_user)]


def get_current_admin(usuario: UsuarioAtualDep) -> Usuario:
    """Permite acesso somente a usuarios administradores."""

    if not usuario.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )

    return usuario


AdminDep = Annotated[Usuario, Depends(get_current_admin)]
