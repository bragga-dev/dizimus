"""
Profile Selectors — queries de leitura para Church e Member.
"""
from typing import Optional
import uuid

from dizimus.apps.users.models import Church, Member


def get_church_by_cnpj(cnpj: str) -> Optional[Church]:
    """Busca igreja por CNPJ."""
    return Church.objects.filter(cnpj=cnpj).first()


def get_member_by_cpf(cpf: str) -> Optional[Member]:
    """Busca membro por CPF."""
    return Member.objects.filter(cpf=cpf).first()


def get_church_by_user_id(user_id: uuid.UUID) -> Optional[Church]:
    """Busca perfil da igreja pelo user_id."""
    return Church.objects.filter(user_id=user_id).first()


def get_member_by_user_id(user_id: uuid.UUID) -> Optional[Member]:
    """Busca perfil do membro pelo user_id."""
    return Member.objects.filter(user_id=user_id).first()