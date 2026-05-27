import uuid
from datetime import date
from typing import Optional
from ninja import Schema, Field
from pydantic import field_validator
from validate_docbr import CPF
from dizimus.apps.users.schemas import AddressIn, AddressOut, UserOut

_cpf = CPF()


class MemberOut(Schema):
    id:            uuid.UUID
    user:          UserOut
    cpf:           Optional[str]
    date_of_birth: Optional[date]
    


class MemberUpdateIn(Schema):
    cpf:           Optional[str] = None
    date_of_birth: Optional[date] = None

    @field_validator("cpf")
    @classmethod
    def cpf_valid(cls, v: Optional[str]) -> Optional[str]:
        if v and not _cpf.validate(v):
            raise ValueError("CPF inválido.")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def birth_not_future(cls, v: Optional[date]) -> Optional[date]:
        if v and v > date.today():
            raise ValueError("Data de nascimento não pode ser no futuro.")
        return v


class MemberAddressIn(AddressIn):
    """Endereço de Membro — igual ao base."""
    pass


class MemberAddressOut(AddressOut):
    member_id: uuid.UUID


__all__ = [
    "MemberOut",
    "MemberUpdateIn",
    "MemberAddressIn",
    "MemberAddressOut",
]