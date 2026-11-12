from fastapi import APIRouter, HTTPException, status

from app.api.deps import AdminDep, SessaoDep, UsuarioAtualDep
from app.schemas.usuario import (
    LoginRequest,
    RegisterRequest,
    Token,
    UsuarioPublic,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

RESPOSTAS_AUTENTICADO = {
    status.HTTP_401_UNAUTHORIZED: {"description": "Token inválido ou expirado"},
    status.HTTP_403_FORBIDDEN: {"description": "Token ausente"},
}


@router.post(
    "/register",
    response_model=UsuarioPublic,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {"description": "E-mail já cadastrado"}},
)
def register(payload: RegisterRequest, db: SessaoDep):
    usuario = AuthService(db).register(
        nome=payload.nome,
        email=payload.email,
        senha=payload.senha,
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail ja cadastrado",
        )

    return usuario


@router.post(
    "/login",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "E-mail ou senha incorretos"}
    },
)
def login(payload: LoginRequest, db: SessaoDep):
    access_token = AuthService(db).login(
        email=payload.email,
        senha=payload.senha,
    )

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )

    return Token(access_token=access_token)


@router.get("/me", response_model=UsuarioPublic, responses=RESPOSTAS_AUTENTICADO)
def get_me(usuario_atual: UsuarioAtualDep):
    """Rota protegida: retorna o perfil do usuario autenticado."""
    return usuario_atual


@router.get(
    "/admin/verificacao",
    responses={
        **RESPOSTAS_AUTENTICADO,
        status.HTTP_403_FORBIDDEN: {
            "description": "Token ausente ou usuário sem perfil de administrador"
        },
    },
)
def somente_admin(admin: AdminDep):
    """Rota administrativa de exemplo."""
    return {"mensagem": f"Acesso administrativo concedido para {admin.nome}"}
