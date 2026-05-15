"""
Repositories — escrita no banco.
Toda persistência de User passa por aqui.
"""
import uuid
from typing import Optional
from django.core.files.uploadedfile import InMemoryUploadedFile

from users.models import User, Church, Member


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


def create_church_profile(user: User) -> Church:
    return Church.objects.create(user=user)


def create_member_profile(user: User) -> Member:
    return Member.objects.create(user=user)


def update_user(user: User, **fields) -> User:
    for attr, value in fields.items():
        if value is not None:
            setattr(user, attr, value)
    user.save()
    return user


def set_user_photo(user: User, photo: InMemoryUploadedFile) -> User:
    # Remove arquivo antigo do MinIO antes de substituir
    if user.photo and user.photo.name != "default/user_img.jpg":
        user.photo.delete(save=False)
    user.photo = photo
    user.save(update_fields=["photo"])
    return user


def remove_user_photo(user: User) -> User:
    if user.photo and user.photo.name != "default/user_img.jpg":
        user.photo.delete(save=False)
    user.photo = "default/user_img.jpg"
    user.save(update_fields=["photo"])
    return user


def activate_user(user: User) -> User:
    user.is_active = True
    user.is_trusty = True
    user.save(update_fields=["is_active", "is_trusty"])
    return user