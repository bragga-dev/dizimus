"""
User Selectors — queries de leitura para User.
Nenhuma escrita acontece aqui.
"""
import uuid
from typing import Optional

from dizimus.apps.users.models import User


def get_user_by_id(user_id: uuid.UUID) -> Optional[User]:
    """Busca usuário por ID."""
    return User.objects.filter(pk=user_id).first()


def get_user_by_email(email: str) -> Optional[User]:
    """Busca usuário por email (case insensitive)."""
    return User.objects.filter(email__iexact=email).first()


def get_user_by_slug(slug: str) -> Optional[User]:
    """Busca usuário por slug."""
    return User.objects.filter(slug=slug).first()


def email_exists(email: str, exclude_id: uuid.UUID = None) -> bool:
    """
    Verifica se email já existe.
    Opcionalmente exclui um ID específico (para updates).
    """
    qs = User.objects.filter(email__iexact=email)
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)
    return qs.exists()


def username_exists(username: str, exclude_id: uuid.UUID = None) -> bool:
    """
    Verifica se username já existe.
    Opcionalmente exclui um ID específico (para updates).
    """
    qs = User.objects.filter(username__iexact=username)
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)
    return qs.exists()


def get_active_users() -> list[User]:
    """Retorna todos os usuários ativos."""
    return list(User.objects.filter(is_active=True))


def get_users_by_role(role: str) -> list[User]:
    """Retorna usuários por role (church/member)."""
    return list(User.objects.filter(role=role))