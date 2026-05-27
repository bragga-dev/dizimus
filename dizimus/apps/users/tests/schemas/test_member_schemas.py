# dizimus/apps/users/tests/schemas/test_member_schemas.py

import pytest
from datetime import date, timedelta
from pydantic import ValidationError
from dizimus.apps.users.schemas.member_schemas import (
    MemberOut,
    MemberUpdateIn,
    MemberAddressIn,
    MemberAddressOut,
)


class TestMemberOut:
    """Testes do schema de saída do membro"""

    def test_member_out_serialization(self, member_user):
        member = member_user.member
        data = MemberOut.from_orm(member)
        assert data.id == member.id
        assert data.user.id == member_user.id
        assert data.cpf == member.cpf
        assert data.date_of_birth == member.date_of_birth


class TestMemberUpdateIn:
    """Testes do schema de atualização de membro (versão member_schemas)"""

    def test_valid_cpf(self):
        data = {"cpf": "529.982.247-25"}
        schema = MemberUpdateIn(**data)
        assert schema.cpf == "529.982.247-25"

    def test_invalid_cpf(self):
        data = {"cpf": "111.111.111-11"}
        with pytest.raises(ValidationError) as exc_info:
            MemberUpdateIn(**data)
        assert "CPF inválido" in str(exc_info.value)

    def test_valid_date_of_birth(self):
        data = {"date_of_birth": date(1990, 1, 1)}
        schema = MemberUpdateIn(**data)
        assert schema.date_of_birth == date(1990, 1, 1)

    def test_future_date_of_birth(self):
        future_date = date.today() + timedelta(days=1)
        data = {"date_of_birth": future_date}
        with pytest.raises(ValidationError) as exc_info:
            MemberUpdateIn(**data)
        assert "futuro" in str(exc_info.value).lower()


class TestMemberAddressIn:
    """Testes do schema de endereço de membro"""

    def test_valid_address(self):
        data = {
            "cep": "01001-000",
            "road": "Praça da Sé",
            "number": "100",
            "district": "Sé",
            "city": "São Paulo",
            "state": "SP",
            "complement": "Apto 101",
            "principal": True
        }
        schema = MemberAddressIn(**data)
        assert schema.cep == "01001-000"
        assert schema.complement == "Apto 101"


class TestMemberAddressOut:
    """Testes do schema de saída de endereço de membro"""

    def test_address_out_serialization(self, member_user):
        from dizimus.apps.users.models import MemberAddress
        address = MemberAddress.objects.filter(member=member_user.member).first()
        if address:
            data = MemberAddressOut.from_orm(address)
            assert data.id == address.id
            assert data.member_id == address.member_id
            assert data.cep == address.cep
            assert data.slug == address.slug