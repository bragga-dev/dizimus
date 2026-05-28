# dizimus/apps/users/tests/repositories/conftest.py

import pytest
from dizimus.apps.users.models import User, Church, Member
from dizimus.apps.users.repositories.user import create_user
from dizimus.apps.users.repositories.church import create_church_profile
from dizimus.apps.users.repositories.member import create_member_profile


@pytest.fixture
def user_factory(db):
    """Factory para criar usuários"""
    def _create_user(**kwargs):
        defaults = {
            "email": "teste@teste.com",
            "password": "SenhaForte123!",
            "username": "testuser",
            "first_name": "Teste",
            "last_name": "User",
            "role": "member",
            "phone": "+5511999998888",  # <-- ADICIONAR PHONE
        }
        defaults.update(kwargs)
        return create_user(**defaults)
    return _create_user


@pytest.fixture
def member_user(db, user_factory):
    """Cria um usuário do tipo member com seu perfil"""
    user = user_factory(
        email="membro@teste.com",
        username="membro",
        first_name="João",
        last_name="Silva",
        role="member",
        phone="+5511999998888"
    )
    member = create_member_profile(user)
    return user


@pytest.fixture
def church_user(db, user_factory):
    """Cria um usuário do tipo church com seu perfil"""
    user = user_factory(
        email="igreja@teste.com",
        username="igreja",
        first_name="Igreja",
        last_name="Teste",
        role="church",
        phone="+5511988887777"
    )
    church = create_church_profile(user)
    return user