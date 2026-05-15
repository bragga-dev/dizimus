"""
Services — regras de negócio.
Orquestra selectors, repositories e tasks. Nunca acessa request.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ninja_jwt.tokens import RefreshToken

from users.models import User
from users import selectors, repositories
from users.exceptions import (
    UserAlreadyExists,
    InvalidCredentials,
    UserNotFound,
    InvalidPassword,
    InvalidToken,
)

if TYPE_CHECKING:
    from users.schemas import RegisterIn, UserUpdateIn


# ── Auth ──────────────────────────────────────────────────────────────────────

def register_user(data: RegisterIn) -> dict:
    """
    Cria o User + perfil (Church ou Member) e dispara e-mail de verificação.
    Retorna os tokens JWT diretamente para o cliente já poder operar.
    """
    if selectors.email_exists(data.email):
        raise UserAlreadyExists("e-mail")
    if selectors.username_exists(data.username):
        raise UserAlreadyExists("username")

    user = repositories.create_user(
        email=data.email,
        password=data.password,
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role,
        phone=data.phone,
    )

    # Cria o perfil conforme o role escolhido
    if user.role == User.UserRole.CHURCH:
        repositories.create_church_profile(user)
    else:
        repositories.create_member_profile(user)

    # Dispara e-mail de verificação (Celery)
    from users.tasks import send_verification_email
    send_verification_email.delay(user.pk)

    return _make_tokens(user)


def login_user(email: str, password: str) -> dict:
    user = authenticate(username=email, password=password)
    if not user:
        raise InvalidCredentials()
    if not user.is_active:
        raise InvalidCredentials()
    return _make_tokens(user)


def logout_user(refresh_token: str) -> None:
    """Blacklista o refresh token (requer ninja_jwt.token_blacklist)."""
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        raise InvalidToken()


def refresh_access_token(refresh_token: str) -> dict:
    try:
        token = RefreshToken(refresh_token)
        return {"access": str(token.access_token)}
    except Exception:
        raise InvalidToken()


def change_password(user: User, old_password: str, new_password: str) -> None:
    if not user.check_password(old_password):
        raise InvalidPassword()
    user.set_password(new_password)
    user.save(update_fields=["password"])


# ── Reset de senha ────────────────────────────────────────────────────────────

def request_password_reset(email: str) -> None:
    """
    Sempre retorna sem erro mesmo que o e-mail não exista
    (evita enumeração de usuários).
    """
    user = selectors.get_user_by_email(email)
    if not user:
        return

    from users.tasks import send_password_reset_email
    uid   = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    send_password_reset_email.delay(user.pk, uid, token)


def confirm_password_reset(uidb64: str, token: str, new_password: str) -> None:
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        raise InvalidToken()

    if not default_token_generator.check_token(user, token):
        raise InvalidToken()

    user.set_password(new_password)
    user.save(update_fields=["password"])


# ── User ──────────────────────────────────────────────────────────────────────

def update_user_profile(user: User, data: UserUpdateIn) -> User:
    payload = data.model_dump(exclude_none=True)

    if "username" in payload and selectors.username_exists(payload["username"], exclude_id=user.pk):
        raise UserAlreadyExists("username")

    return repositories.update_user(user, **payload)


# ── Helpers internos ─────────────────────────────────────────────────────────

def _make_tokens(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        "access":  str(refresh.access_token),
        "refresh": str(refresh),
    }