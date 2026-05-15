"""
Users router — endpoints autenticados de perfil.
Registrado em config/api.py como: api.add_router("/users/", ...)
"""
from ninja import Router, File, UploadedFile
from ninja_jwt.authentication import JWTAuth

from users import services, repositories
from users.schemas import UserOut, UserUpdateIn, MessageOut
from users.exceptions import UserAlreadyExists
from users.validators import validate_image_file
from django.core.exceptions import ValidationError as DjangoValidationError

router = Router(auth=JWTAuth())  # todas as rotas deste router exigem JWT


# ── Perfil ────────────────────────────────────────────────────────────────────

@router.get(
    "/me",
    response=UserOut,
    summary="Meu perfil",
)
def get_me(request):
    """Retorna os dados do usuário autenticado."""
    return request.auth


@router.patch(
    "/me",
    response={200: UserOut, 409: MessageOut},
    summary="Atualizar perfil",
)
def update_me(request, payload: UserUpdateIn):
    """
    Atualização parcial — envie apenas os campos que deseja alterar.
    """
    try:
        user = services.update_user_profile(request.auth, payload)
        return 200, user
    except UserAlreadyExists as e:
        return 409, {"detail": str(e)}


# ── Foto ──────────────────────────────────────────────────────────────────────

@router.post(
    "/me/photo",
    response={200: UserOut, 400: MessageOut},
    summary="Fazer upload de foto de perfil",
)
def upload_photo(request, photo: UploadedFile = File(...)):
    """
    Substitui a foto de perfil no MinIO.
    Formatos aceitos: jpg, jpeg, png. Máx: 5 MB.
    """
    try:
        validate_image_file(photo)          # reutiliza o validator já existente
    except DjangoValidationError as e:
        return 400, {"detail": str(e.message)}

    user = repositories.set_user_photo(request.auth, photo)
    return 200, user


@router.delete(
    "/me/photo",
    response={200: MessageOut},
    summary="Remover foto de perfil",
)
def remove_photo(request):
    """Volta a foto de perfil para a imagem padrão."""
    repositories.remove_user_photo(request.auth)
    return 200, {"detail": "Foto removida com sucesso."}