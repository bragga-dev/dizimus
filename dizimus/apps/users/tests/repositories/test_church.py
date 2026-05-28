# dizimus/apps/users/tests/repositories/test_church.py

import pytest
from unittest.mock import patch
from dizimus.apps.users.repositories.church import create_church_profile, update_church_profile
from dizimus.apps.users.models import Church, User


@pytest.mark.django_db
class TestChurchRepository:
    """Testes do repositório de Church"""

    def test_create_church_profile_success(self, user_factory):
        """Deve criar perfil de igreja com sucesso"""
        user = user_factory(role="church")
        
        church = create_church_profile(user)
        
        assert church.id is not None
        assert church.user == user
        assert church.is_verified is False
        assert church.total_members == 0
        assert church.cnpj is None
        assert church.asaas_token is None

    def test_create_church_profile_only_once_per_user(self, user_factory):
        """Deve permitir apenas um perfil de igreja por usuário"""
        user = user_factory(role="church")
        
        church1 = create_church_profile(user)
        church2 = Church.objects.filter(user=user).first()
        
        assert church1.id == church2.id
        assert Church.objects.filter(user=user).count() == 1

    def test_update_church_profile_success(self, church_user):
        """Deve atualizar perfil da igreja"""
        church = church_user.church
        
        updated_church = update_church_profile(
            church,
            cnpj="12.345.678/0001-90",
            instagram="@igrejaamor",
            website="https://igrejaamor.com",
            about="Uma igreja acolhedora"
        )
        
        assert updated_church.cnpj == "12.345.678/0001-90"
        assert updated_church.instagram == "@igrejaamor"
        assert updated_church.website == "https://igrejaamor.com"
        assert updated_church.about == "Uma igreja acolhedora"

    def test_update_church_profile_partial(self, church_user):
        """Deve atualizar apenas campos fornecidos"""
        church = church_user.church
        original_cnpj = church.cnpj
        
        updated_church = update_church_profile(church, instagram="@novaigreja")
        
        assert updated_church.instagram == "@novaigreja"
        assert updated_church.cnpj == original_cnpj

    def test_update_church_profile_with_asaas_token(self, church_user):
        """Deve atualizar token do Asaas"""
        church = church_user.church
        
        updated_church = update_church_profile(church, asaas_token="tokentest123")
        
        assert updated_church.asaas_token == "tokentest123"

    def test_update_church_profile_returns_church_instance(self, church_user):
        """Deve retornar a instância da igreja atualizada"""
        church = church_user.church
        result = update_church_profile(church, instagram="@teste")
        
        assert isinstance(result, Church)
        assert result == church