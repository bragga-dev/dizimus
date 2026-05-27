import uuid
from typing import Optional
from ninja import Schema, Field
from validate_docbr import CNPJ
from dizimus.apps.users.schemas import AddressIn, AddressOut, UserOut
from pydantic import field_validator

_cnpj = CNPJ()


class ChurchOut(Schema):
    id:          uuid.UUID
    user:        UserOut
    is_verified: bool
    cnpj:        Optional[str]
    banner_url:  str
    

    @staticmethod
    def resolve_banner_url(obj) -> str:
        return obj.banner_url  # property com fallback seguro


class ChurchUpdateIn(Schema):
    cnpj: Optional[str] = None

    @field_validator("cnpj")  # type: ignore[name-defined]
    @classmethod
    def cnpj_valid(cls, v: Optional[str]) -> Optional[str]:
        from pydantic import field_validator  # noqa — só para o type checker
        if v and not _cnpj.validate(v):
            raise ValueError("CNPJ inválido.")
        return v


class ChurchAddressIn(AddressIn):
    """Endereço de Igreja — igual ao base."""
    pass


class ChurchAddressOut(AddressOut):
    church_id: uuid.UUID


# ── re-export para facilitar importação nos routers ──────────────────────────
__all__ = [
    "ChurchOut",
    "ChurchUpdateIn",
    "ChurchAddressIn",
    "ChurchAddressOut",
]