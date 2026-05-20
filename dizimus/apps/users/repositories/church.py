"""
Church Repository — persistência de perfil Igreja.
"""
from dizimus.apps.users.models import User, Church


def create_church_profile(user: User) -> Church:
    return Church.objects.create(user=user)


def update_church_profile(church: Church, **fields) -> Church:
    for attr, value in fields.items():
        setattr(church, attr, value)
    church.save()
    return church