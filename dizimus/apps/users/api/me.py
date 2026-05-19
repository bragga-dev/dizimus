"""
Users router — endpoints de perfil base e foto.
"""
import uuid
from typing import List

from django.core.exceptions import ValidationError as DjangoValidationError
from ninja import File, Router, UploadedFile

from dizimus.apps.users import repositories, services
from dizimus.apps.users.exceptions import UserAlreadyExists
from dizimus.apps.users.schemas.users_schemas import MessageOut, UserOut, UserUpdateIn
from dizimus.apps.users.validators.validate_image_file import validate_image_file

router = Router()

# ═══════════════════════════════════════════════════════════════════════════════
# PERFIL BASE (User)
# ═══════════════════════════════════════════════════════════════════════════════

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
    summary="Atualizar dados base",
    description=(
        "Atualiza campos do usuário base: `username`, `first_name`, `last_name`, `phone`. "
        "Para campos específicos do perfil (CNPJ, CPF, etc.) use `PATCH /me/profile`."
    ),
)
def update_me(request, payload: UserUpdateIn):
    try:
        user = services.update_user_profile(request.auth, payload)
        return 200, user
    except UserAlreadyExists as e:
        return 409, {"detail": str(e)}


# ── Foto ──────────────────────────────────────────────────────────────────────

@router.post(
    "/me/photo",
    response={200: UserOut, 400: MessageOut},
    summary="Upload de foto de perfil",
)
def upload_photo(request, photo: UploadedFile = File(...)):
    """Formatos aceitos: jpg, jpeg, png, webp. Máx: 5 MB."""
    try:
        validate_image_file(photo)
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
    """Restaura a imagem padrão."""
    repositories.remove_user_photo(request.auth)
    return 200, {"detail": "Foto removida com sucesso."}