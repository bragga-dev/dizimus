"""
Member Repository — persistência de perfil Membro.
"""
from dizimus.apps.users.models import User, Member


def create_member_profile(user: User) -> Member:
    return Member.objects.create(user=user)


def update_member_profile(member: Member, **fields) -> Member:
    for attr, value in fields.items():
        setattr(member, attr, value)
    member.full_clean()   # dispara validação do model (date_of_birth no futuro, etc.)
    member.save()
    return member