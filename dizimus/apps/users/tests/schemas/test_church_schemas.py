# dizimus/apps/users/tests/schemas/test_church_schemas.py

import pytest
import uuid
from pydantic import ValidationError
from dizimus.apps.users.schemas.church_schemas import (
    ChurchOut,
    ChurchUpdateIn,
    ChurchAddressIn,
    ChurchAddressOut,
)


class TestChurchOut:
    """Testes do schema de saída da igreja"""

    def test_church_out_serialization(self, church_user):
        church = church_user.church
        data = ChurchOut.from_orm(church)
        assert data.id == church.id
        assert data.user.id == church_user.id
        assert data.is_verified == church.is_verified
        assert data.cnpj == church.cnpj
        assert data.banner_url == church.banner_url


class TestChurchUpdateIn:
    """Testes do schema de atualização de igreja (versão church_schemas)"""

    def test_valid_cnpj(self):
        data = {"cnpj": "12.345.678/0001-95"}
        schema = ChurchUpdateIn(**data)
        assert schema.cnpj == "12.345.678/0001-95"

    def test_invalid_cnpj(self):
        data = {"cnpj": "12.345.678/0001-96"}
        with pytest.raises(ValidationError) as exc_info:
            ChurchUpdateIn(**data)
        assert "CNPJ inválido" in str(exc_info.value)

    def test_none_cnpj_is_valid(self):
        data = {"cnpj": None}
        schema = ChurchUpdateIn(**data)
        assert schema.cnpj is None


class TestChurchAddressIn:
    """Testes do schema de endereço de igreja"""

    def test_valid_address(self):
        data = {
            "cep": "01001-000",
            "road": "Praça da Sé",
            "number": "100",
            "district": "Sé",
            "city": "São Paulo",
            "state": "SP",
            "principal": True
        }
        schema = ChurchAddressIn(**data)
        assert schema.cep == "01001-000"
        assert schema.road == "Praça da Sé"


class TestChurchAddressOut:
    """Testes do schema de saída de endereço de igreja"""

    def test_address_out_serialization(self, church_user):
        from dizimus.apps.users.models.church import ChurchAddress
        address = ChurchAddress.objects.filter(church=church_user.church).first()
        if address:
            data = ChurchAddressOut.from_orm(address)
            assert data.id == address.id
            assert data.church_id == address.church_id
            assert data.cep == address.cep