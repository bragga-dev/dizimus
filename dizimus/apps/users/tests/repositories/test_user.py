# dizimus/apps/users/tests/repositories/test_user.py

import pytest
from django.core.exceptions import ValidationError
from dizimus.apps.users.repositories.user import create_user, update_user, activate_user


@pytest.mark.django_db
class TestUserRepository:

    def test_create_user_success(self, db):
        user = create_user(
            email="joao@teste.com",
            password="SenhaForte123!",
            username="joaosilva",
            first_name="João",
            last_name="Silva",
            role="member",
            phone="+5511999998888"  # <-- Adicionar phone
        )
        
        assert user.id is not None
        assert user.email == "joao@teste.com"
        assert user.phone == "+5511999998888"

    def test_create_user_without_phone(self, db):
        """Deve criar usuário sem telefone (usando string vazia)"""
        user = create_user(
            email="maria@teste.com",
            password="SenhaForte123!",
            username="mariasilva",
            first_name="Maria",
            last_name="Silva",
            role="member",
            phone=None  # <-- Deve ser convertido para ""
        )
        
        assert user.id is not None
        assert user.phone == ""  # <-- Espera string vazia

    def test_create_church_user(self, db):
        user = create_user(
            email="igreja@teste.com",
            password="SenhaForte123!",
            username="igrejaamor",
            first_name="Igreja Amor",
            last_name="",
            role="church",
            phone="+5511988887777"  # <-- Adicionar phone
        )
        
        assert user.role == "church"
        assert user.is_active is False

    def test_update_user_success(self, member_user):  # <-- Agora member_user existe
        updated_user = update_user(
            member_user,
            first_name="Carlos",
            last_name="Ferreira",
        )
        
        assert updated_user.first_name == "Carlos"
        assert updated_user.last_name == "Ferreira"

    def test_update_user_partial(self, member_user):
        original_email = member_user.email
        updated_user = update_user(member_user, first_name="Roberto")
        
        assert updated_user.first_name == "Roberto"
        assert updated_user.email == original_email

    def test_update_user_with_none_values(self, member_user):
        original_first_name = member_user.first_name
        updated_user = update_user(member_user, first_name=None, last_name="Novo")
        
        assert updated_user.first_name == original_first_name
        assert updated_user.last_name == "Novo"

    def test_activate_user(self, member_user):
        assert member_user.is_active is False
        assert member_user.is_trusty is False
        
        activated_user = activate_user(member_user)
        
        assert activated_user.is_active is True
        assert activated_user.is_trusty is True

    def test_activate_already_active_user(self, db):
        user = create_user(
            email="ativo@teste.com",
            password="SenhaForte123!",
            username="ativo",
            first_name="Ativo",
            last_name="User",
            role="member",
            phone="+5511999998888"  # <-- Adicionar phone
        )
        activate_user(user)
        activate_user(user)  # segunda vez não deve dar erro
        
        assert user.is_active is True
        assert user.is_trusty is True