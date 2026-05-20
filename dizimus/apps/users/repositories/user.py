"""
User Repository — persistência de User.
"""
from typing import Optional

from dizimus.apps.users.models import User


def create_user(
    *,
    email: str,
    password: str,
    username: str,
    first_name: str,
    last_name: str,
    role: str,
    phone: Optional[str] = None,
) -> User:
    user = User.objects.create_user(
        email=email,
        password=password,
        username=username,
        first_name=first_name,
        last_name=last_name,
        role=role,
        phone=phone,
    )
    return user


def update_user(user: User, **fields) -> User:
    for attr, value in fields.items():
        if value is not None:
            setattr(user, attr, value)
    user.save()
    return user


def activate_user(user: User) -> User:
    user.is_active = True
    user.is_trusty = True
    user.save(update_fields=["is_active", "is_trusty"])
    return user