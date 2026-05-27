# dizimus/apps/users/tests/schemas/conftest.py

import pytest
from datetime import date
from dizimus.apps.users.models import User


@pytest.fixture
def member_user(db):
    """
    User com role='member' + perfil Member criado explicitamente.
    (Não há signal que crie o Member automaticamente.)
    """
    from dizimus.apps.users.models.member import Member  # ajuste o path se necessário

    user = User.objects.create_user(
        username="membro_teste",
        first_name="João",
        last_name="Silva",
        email="membro@teste.com",
        password="SenhaForte123!",
        role=User.UserRole.MEMBER,
    )
    Member.objects.create(
        user=user,
        cpf="529.982.247-25",
        date_of_birth=date(1990, 6, 15),
    )
    return user


@pytest.fixture
def church_user(db):
    """
    User com role='church' + perfil Church criado explicitamente.
    (Não há signal que crie o Church automaticamente.)
    """
    from dizimus.apps.users.models.church import Church  # ajuste o path se necessário

    user = User.objects.create_user(
        username="igreja_teste",
        first_name="Igreja Teste",
        email="igreja@teste.com",
        password="SenhaForte123!",
        role=User.UserRole.CHURCH,
    )
    Church.objects.create(
        user=user,
        cnpj="11.222.333/0001-81",
    )
    return user