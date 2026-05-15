"""
Selectors — apenas leitura do banco.
Nenhuma escrita acontece aqui.
"""
import uuid
from typing import Optional
from users.models import User


def get_user_by_id(user_id: uuid.UUID) -> Optional[User]:
    return User.objects.filter(pk=user_id).first()


def get_user_by_email(email: str) -> Optional[User]:
    return User.objects.filter(email__iexact=email).first()


def get_user_by_slug(slug: str) -> Optional[User]:
    return User.objects.filter(slug=slug).first()


def email_exists(email: str, exclude_id: uuid.UUID = None) -> bool:
    qs = User.objects.filter(email__iexact=email)
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)
    return qs.exists()


def username_exists(username: str, exclude_id: uuid.UUID = None) -> bool:
    qs = User.objects.filter(username__iexact=username)
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)
    return qs.exists()