# dizimus/apps/users/tests/repositories/test_address.py

import pytest
import uuid
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from dizimus.apps.users.repositories.address import (
    get_church_addresses,
    get_church_address_by_id,
    create_church_address,
    update_church_address,
    delete_church_address,
    get_member_addresses,
    get_member_address_by_id,
    create_member_address,
    update_member_address,
    delete_member_address,
)
from dizimus.apps.users.models import ChurchAddress, MemberAddress, Church, Member


# =============================================================================
# Church Address Tests
# =============================================================================

@pytest.mark.django_db
class TestChurchAddressRepository:
    """Testes dos endereços de igreja"""

    def test_create_church_address_success(self, church_user):
        """Deve criar endereço para igreja"""
        church = church_user.church
        
        address = create_church_address(
            church,
            cep="01001-000",
            road="Praça da Sé",
            number="100",
            district="Sé",
            city="São Paulo",
            state="SP",
            principal=True
        )
        
        assert address.id is not None
        assert address.church == church
        assert address.cep == "01001-000"
        assert address.road == "Praça da Sé"
        assert address.principal is True
        assert address.slug is not None

    def test_create_church_address_with_complement(self, church_user):
        """Deve criar endereço com complemento"""
        church = church_user.church
        
        address = create_church_address(
            church,
            cep="01001-000",
            road="Praça da Sé",
            number="100",
            district="Sé",
            city="São Paulo",
            state="SP",
            complement="Apto 101",
            principal=False
        )
        
        assert address.complement == "Apto 101"
        assert address.principal is False

    def test_create_church_address_invalid_cep_raises_error(self, church_user):
        """Deve lançar erro ao criar com CEP inválido"""
        church = church_user.church
        
        with pytest.raises(ValidationError):
            create_church_address(
                church,
                cep="12345678",  # formato inválido
                road="Rua A",
                number="123",
                district="Centro",
                city="São Paulo",
                state="SP"
            )

    def test_create_church_address_invalid_state_raises_error(self, church_user):
        """Deve lançar erro ao criar com estado inválido"""
        church = church_user.church
        
        with pytest.raises(ValidationError):
            create_church_address(
                church,
                cep="01001-000",
                road="Rua A",
                number="123",
                district="Centro",
                city="São Paulo",
                state="XX"  # Estado inválido
            )

    def test_get_church_addresses_empty(self, church_user):
        """Deve retornar lista vazia quando não há endereços"""
        church = church_user.church
        addresses = get_church_addresses(church)
        
        assert len(addresses) == 0

    def test_get_church_addresses_ordered(self, church_user):
        """Deve retornar endereços ordenados (principal primeiro, depois por rua)"""
        church = church_user.church
        
        # Criar endereços
        addr1 = create_church_address(church, cep="01001-000", road="Rua Principal", number="1", district="Centro", city="SP", state="SP", principal=True)
        addr2 = create_church_address(church, cep="02002-000", road="Avenida Secundária", number="2", district="Vila", city="SP", state="SP", principal=False)
        addr3 = create_church_address(church, cep="03003-000", road="Rua Terciária", number="3", district="Centro", city="SP", state="SP", principal=False)
        
        addresses = get_church_addresses(church)
        
        assert len(addresses) == 3
        assert addresses[0].principal is True  # Principal primeiro
        # Os não-principais ordenados por road
        assert addresses[1].road == "Avenida Secundária"
        assert addresses[2].road == "Rua Terciária"

    def test_get_church_address_by_id_found(self, church_user):
        """Deve encontrar endereço por ID"""
        church = church_user.church
        created = create_church_address(church, cep="01001-000", road="Rua Teste", number="123", district="Centro", city="SP", state="SP")
        
        found = get_church_address_by_id(church, created.id)
        
        assert found is not None
        assert found.id == created.id

    def test_get_church_address_by_id_not_found(self, church_user):
        """Deve retornar None quando endereço não existe"""
        church = church_user.church
        fake_id = uuid.uuid4()
        
        found = get_church_address_by_id(church, fake_id)
        
        assert found is None

    def test_get_church_address_by_id_wrong_church(self, church_user, user_factory):
        """Deve retornar None quando endereço pertence a outra igreja"""
        church1 = church_user.church
        
        # Criar outra igreja
        other_user = user_factory(email="outra@igreja.com", username="outraigreja", role="church", phone="+5511988887777")
        from dizimus.apps.users.repositories.church import create_church_profile
        church2 = create_church_profile(other_user)
        
        # Criar endereço para church1
        address = create_church_address(church1, cep="01001-000", road="Rua Teste", number="123", district="Centro", city="SP", state="SP")
        
        # Buscar endereço de church1 usando church2
        found = get_church_address_by_id(church2, address.id)
        
        assert found is None

    def test_update_church_address_success(self, church_user):
        """Deve atualizar endereço da igreja"""
        church = church_user.church
        address = create_church_address(church, cep="01001-000", road="Rua Antiga", number="100", district="Centro", city="SP", state="SP")
        
        updated = update_church_address(address, road="Rua Nova", number="200", complement="Apto 1")
        
        assert updated.road == "Rua Nova"
        assert updated.number == "200"
        assert updated.complement == "Apto 1"
        assert updated.cep == "01001-000"  # não alterado

    def test_update_church_address_partial(self, church_user):
        """Deve atualizar apenas campos fornecidos"""
        church = church_user.church
        address = create_church_address(church, cep="01001-000", road="Rua A", number="100", district="Centro", city="SP", state="SP")
        
        updated = update_church_address(address, number="999")
        
        assert updated.number == "999"
        assert updated.road == "Rua A"

    def test_update_church_address_with_none_values(self, church_user):
        """Deve ignorar campos com valor None"""
        church = church_user.church
        address = create_church_address(church, cep="01001-000", road="Rua A", number="100", district="Centro", city="SP", state="SP")
        original_road = address.road
        
        updated = update_church_address(address, road=None, number="999")
        
        assert updated.road == original_road  # não alterado
        assert updated.number == "999"

    def test_update_church_address_invalid_data_raises_error(self, church_user):
        """Deve lançar erro ao atualizar com dados inválidos"""
        church = church_user.church
        address = create_church_address(church, cep="01001-000", road="Rua A", number="100", district="Centro", city="SP", state="SP")
        
        with pytest.raises(ValidationError):
            update_church_address(address, state="XX")  # Estado inválido

    def test_delete_church_address(self, church_user):
        """Deve deletar endereço da igreja"""
        church = church_user.church
        address = create_church_address(church, cep="01001-000", road="Rua Delete", number="1", district="Centro", city="SP", state="SP")
        
        address_id = address.id
        delete_church_address(address)
        
        assert ChurchAddress.objects.filter(id=address_id).count() == 0

    def test_delete_church_address_nonexistent(self, church_user):
        """Deve deletar sem erro se endereço não existe (deve ser silencioso)"""
        church = church_user.church
        address = ChurchAddress(church=church, cep="01001-000", road="Rua Fake", number="1", district="Centro", city="SP", state="SP")
        address.id = uuid.uuid4()  # ID fake
        
        # Deve não lançar exceção
        delete_church_address(address)


# =============================================================================
# Member Address Tests
# =============================================================================

@pytest.mark.django_db
class TestMemberAddressRepository:
    """Testes dos endereços de membro"""

    def test_create_member_address_success(self, member_user):
        """Deve criar endereço para membro"""
        member = member_user.member
        
        address = create_member_address(
            member,
            cep="01001-000",
            road="Rua das Flores",
            number="42",
            district="Jardim",
            city="São Paulo",
            state="SP",
            principal=True
        )
        
        assert address.id is not None
        assert address.member == member
        assert address.cep == "01001-000"
        assert address.principal is True

    def test_create_member_address_with_complement(self, member_user):
        """Deve criar endereço com complemento"""
        member = member_user.member
        
        address = create_member_address(
            member,
            cep="01001-000",
            road="Rua Secundária",
            number="100",
            district="Centro",
            city="SP",
            state="SP",
            complement="Bloco B",
            principal=False
        )
        
        assert address.complement == "Bloco B"
        assert address.principal is False

    def test_create_member_address_invalid_cep_raises_error(self, member_user):
        """Deve lançar erro ao criar com CEP inválido"""
        member = member_user.member
        
        with pytest.raises(ValidationError):
            create_member_address(
                member,
                cep="12345678",
                road="Rua A",
                number="123",
                district="Centro",
                city="SP",
                state="SP"
            )

    def test_get_member_addresses_empty(self, member_user):
        """Deve retornar lista vazia quando não há endereços"""
        member = member_user.member
        addresses = get_member_addresses(member)
        
        assert len(addresses) == 0

    def test_get_member_addresses_ordered(self, member_user):
        """Deve retornar endereços do membro ordenados"""
        member = member_user.member
        
        addr1 = create_member_address(member, cep="01001-000", road="Rua Principal", number="1", district="Centro", city="SP", state="SP", principal=True)
        addr2 = create_member_address(member, cep="02002-000", road="Avenida Secundária", number="2", district="Vila", city="SP", state="SP", principal=False)
        addr3 = create_member_address(member, cep="03003-000", road="Rua Terciária", number="3", district="Centro", city="SP", state="SP", principal=False)
        
        addresses = get_member_addresses(member)
        
        assert len(addresses) == 3
        assert addresses[0].principal is True
        assert addresses[1].road == "Avenida Secundária"
        assert addresses[2].road == "Rua Terciária"

    def test_get_member_address_by_id_found(self, member_user):
        """Deve encontrar endereço do membro por ID"""
        member = member_user.member
        created = create_member_address(member, cep="01001-000", road="Rua Teste", number="123", district="Centro", city="SP", state="SP")
        
        found = get_member_address_by_id(member, created.id)
        
        assert found is not None
        assert found.id == created.id

    def test_get_member_address_by_id_not_found(self, member_user):
        """Deve retornar None quando endereço não existe"""
        member = member_user.member
        fake_id = uuid.uuid4()
        
        found = get_member_address_by_id(member, fake_id)
        
        assert found is None

    def test_get_member_address_by_id_wrong_member(self, member_user, user_factory):
        """Deve retornar None quando endereço pertence a outro membro"""
        member1 = member_user.member
        
        # Criar outro membro
        other_user = user_factory(email="outro@membro.com", username="outromembro", role="member", phone="+5511999998888")
        from dizimus.apps.users.repositories.member import create_member_profile
        member2 = create_member_profile(other_user)
        
        # Criar endereço para member1
        address = create_member_address(member1, cep="01001-000", road="Rua Teste", number="123", district="Centro", city="SP", state="SP")
        
        # Buscar endereço de member1 usando member2
        found = get_member_address_by_id(member2, address.id)
        
        assert found is None

    def test_update_member_address_success(self, member_user):
        """Deve atualizar endereço do membro"""
        member = member_user.member
        address = create_member_address(member, cep="01001-000", road="Rua Velha", number="10", district="Centro", city="SP", state="SP")
        
        updated = update_member_address(address, road="Rua Nova", complement="Casa 2", number="20")
        
        assert updated.road == "Rua Nova"
        assert updated.complement == "Casa 2"
        assert updated.number == "20"

    def test_update_member_address_partial(self, member_user):
        """Deve atualizar apenas campos fornecidos"""
        member = member_user.member
        address = create_member_address(member, cep="01001-000", road="Rua A", number="100", district="Centro", city="SP", state="SP")
        original_road = address.road
        
        updated = update_member_address(address, number="999")
        
        assert updated.number == "999"
        assert updated.road == original_road

    def test_update_member_address_with_none_values(self, member_user):
        """Deve ignorar campos com valor None"""
        member = member_user.member
        address = create_member_address(member, cep="01001-000", road="Rua A", number="100", district="Centro", city="SP", state="SP")
        original_road = address.road
        
        updated = update_member_address(address, road=None, number="999")
        
        assert updated.road == original_road
        assert updated.number == "999"

    def test_update_member_address_invalid_data_raises_error(self, member_user):
        """Deve lançar erro ao atualizar com dados inválidos"""
        member = member_user.member
        address = create_member_address(member, cep="01001-000", road="Rua A", number="100", district="Centro", city="SP", state="SP")
        
        with pytest.raises(ValidationError):
            update_member_address(address, state="XX")

    def test_delete_member_address(self, member_user):
        """Deve deletar endereço do membro"""
        member = member_user.member
        address = create_member_address(member, cep="01001-000", road="Rua Delete", number="1", district="Centro", city="SP", state="SP")
        
        address_id = address.id
        delete_member_address(address)
        
        assert MemberAddress.objects.filter(id=address_id).count() == 0

    def test_delete_member_address_nonexistent(self, member_user):
        """Deve deletar sem erro se endereço não existe"""
        member = member_user.member
        address = MemberAddress(member=member, cep="01001-000", road="Rua Fake", number="1", district="Centro", city="SP", state="SP")
        address.id = uuid.uuid4()
        
        # Deve não lançar exceção
        delete_member_address(address)


# =============================================================================
# Extra: Testes de integração para principal logic
# =============================================================================

@pytest.mark.django_db
class TestPrincipalLogic:
    """Testa a lógica de endereço principal (deve ser testada no model, não no repo)"""

    def test_first_address_becomes_principal_by_default(self, church_user):
        """Primeiro endereço criado deve ser principal por padrão"""
        church = church_user.church
        
        address = create_church_address(
            church,
            cep="01001-000",
            road="Rua Principal",
            number="1",
            district="Centro",
            city="SP",
            state="SP"
            # principal não especificado, deve ser True por padrão
        )
        
        assert address.principal is True

    def test_multiple_principal_addresses_handled_by_model(self, church_user):
        """Múltiplos endereços principal deve ser tratado pelo model.save()
        O repositório apenas chama save(), a lógica está no model"""
        church = church_user.church
        
        addr1 = create_church_address(church, cep="01001-000", road="Rua A", number="1", district="Centro", city="SP", state="SP", principal=True)
        addr2 = create_church_address(church, cep="02002-000", road="Rua B", number="2", district="Vila", city="SP", state="SP", principal=True)
        
        # O model deve garantir que apenas um principal existe
        # Refresh para pegar o estado atualizado pelo model
        addr1.refresh_from_db()
        addr2.refresh_from_db()
        
        # Apenas um deles deve ser principal (o último salvo)
        assert (addr1.principal or addr2.principal) is True
        assert (addr1.principal and addr2.principal) is False