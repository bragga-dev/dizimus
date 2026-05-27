# dizimus/apps/users/tests/schemas/test_users_schemas.py

import pytest
from datetime import datetime
from pydantic import ValidationError
from dizimus.apps.users.schemas.users_schemas import (
    RegisterIn,
    LoginIn,
    TokenOut,
    RefreshIn,
    ChangePasswordIn,
    PasswordResetRequestIn,
    PasswordResetConfirmIn,
    UserOut,
    UserUpdateIn,
    AddressIn,
    AddressOut,
    MessageOut,
)
from dizimus.apps.users.models import User


class TestRegisterIn:
    """Testes do schema de registro"""

    def test_valid_member_registration(self):
        data = {
            "username": "joaosilva",
            "first_name": "João",
            "last_name": "Silva",
            "email": "joao@teste.com",
            "password": "SenhaForte123!",
            "password2": "SenhaForte123!",
            "role": "member",
            "phone": "+5511999998888"
        }
        schema = RegisterIn(**data)
        assert schema.username == "joaosilva"
        assert schema.first_name == "João"
        assert schema.last_name == "Silva"

    def test_valid_church_registration_without_last_name(self):
        data = {
            "username": "igrejaamor",
            "first_name": "Igreja Amor",
            "last_name": None,
            "email": "contato@igrejaamor.com",
            "password": "SenhaForte123!",
            "password2": "SenhaForte123!",
            "role": "church",
        }
        schema = RegisterIn(**data)
        assert schema.role == "church"
        assert schema.last_name is None

    def test_member_requires_last_name(self):
        data = {
            "username": "joaosilva",
            "first_name": "João",
            "last_name": None,
            "email": "joao@teste.com",
            "password": "SenhaForte123!",
            "password2": "SenhaForte123!",
            "role": "member",
        }
        with pytest.raises(ValidationError) as exc_info:
            RegisterIn(**data)
        assert "Sobrenome é obrigatório para membros" in str(exc_info.value)

    def test_passwords_must_match(self):
        data = {
            "username": "joaosilva",
            "first_name": "João",
            "last_name": "Silva",
            "email": "joao@teste.com",
            "password": "SenhaForte123!",
            "password2": "SenhaDiferente456!",
            "role": "member",
        }
        with pytest.raises(ValidationError) as exc_info:
            RegisterIn(**data)
        assert "senhas não coincidem" in str(exc_info.value).lower()

    def test_weak_password_raises_error(self):
        data = {
            "username": "joaosilva",
            "first_name": "João",
            "last_name": "Silva",
            "email": "joao@teste.com",
            "password": "123",
            "password2": "123",
            "role": "member",
        }
        with pytest.raises(ValidationError) as exc_info:
            RegisterIn(**data)
        assert "password" in str(exc_info.value).lower()

    def test_invalid_email_format(self):
        data = {
            "username": "joaosilva",
            "first_name": "João",
            "last_name": "Silva",
            "email": "email_invalido",
            "password": "SenhaForte123!",
            "password2": "SenhaForte123!",
            "role": "member",
        }
        with pytest.raises(ValidationError):
            RegisterIn(**data)

    def test_username_with_invalid_characters(self):
        data = {
            "username": "joao@silva!",
            "first_name": "João",
            "last_name": "Silva",
            "email": "joao@teste.com",
            "password": "SenhaForte123!",
            "password2": "SenhaForte123!",
            "role": "member",
        }
        with pytest.raises(ValidationError) as exc_info:
            RegisterIn(**data)
        assert "Username inválido" in str(exc_info.value)


class TestLoginIn:
    def test_valid_login_data(self):
        data = {"email": "user@teste.com", "password": "senha123"}
        schema = LoginIn(**data)
        assert schema.email == "user@teste.com"
        assert schema.password == "senha123"


class TestTokenOut:
    def test_token_output(self):
        data = {"access": "token_access_123", "refresh": "token_refresh_456"}
        schema = TokenOut(**data)
        assert schema.access == "token_access_123"
        assert schema.refresh == "token_refresh_456"


class TestRefreshIn:
    def test_refresh_input(self):
        data = {"refresh": "refresh_token_123"}
        schema = RefreshIn(**data)
        assert schema.refresh == "refresh_token_123"


class TestChangePasswordIn:
    def test_valid_password_change(self):
        data = {
            "old_password": "SenhaAntiga123!",
            "new_password": "SenhaNova456!",
            "new_password2": "SenhaNova456!"
        }
        schema = ChangePasswordIn(**data)
        assert schema.old_password == "SenhaAntiga123!"
        assert schema.new_password == "SenhaNova456!"

    def test_passwords_must_match(self):
        data = {
            "old_password": "SenhaAntiga123!",
            "new_password": "SenhaNova456!",
            "new_password2": "SenhaDiferente789!"
        }
        with pytest.raises(ValidationError) as exc_info:
            ChangePasswordIn(**data)
        assert "senhas não coincidem" in str(exc_info.value).lower()

    def test_weak_new_password(self):
        data = {
            "old_password": "SenhaAntiga123!",
            "new_password": "123",
            "new_password2": "123"
        }
        with pytest.raises(ValidationError):
            ChangePasswordIn(**data)


class TestPasswordResetRequestIn:
    def test_valid_request(self):
        data = {"email": "user@teste.com"}
        schema = PasswordResetRequestIn(**data)
        assert schema.email == "user@teste.com"


class TestPasswordResetConfirmIn:
    def test_valid_confirmation(self):
        data = {
            "uid": "abc123",
            "token": "token_xyz",
            "new_password": "NovaSenha123!",
            "new_password2": "NovaSenha123!"
        }
        schema = PasswordResetConfirmIn(**data)
        assert schema.uid == "abc123"
        assert schema.token == "token_xyz"

    def test_passwords_must_match(self):
        data = {
            "uid": "abc123",
            "token": "token_xyz",
            "new_password": "Senha123!",
            "new_password2": "Senha456!"
        }
        with pytest.raises(ValidationError):
            PasswordResetConfirmIn(**data)


class TestUserOut:
    def test_user_output_serialization(self, member_user):
        """Testa a serialização do UserOut a partir de um model User"""
        data = UserOut.from_orm(member_user)
        assert data.id == member_user.id
        assert data.username == member_user.username
        assert data.email == member_user.email
        assert data.role == member_user.role
        assert data.photo_url == member_user.photo_url

    def test_resolve_phone_without_phone(self, member_user):
        member_user.phone = None
        data = UserOut.from_orm(member_user)
        assert data.phone is None


class TestUserUpdateIn:
    def test_partial_update_with_first_name_only(self):
        data = {"first_name": "Carlos"}
        schema = UserUpdateIn(**data)
        assert schema.first_name == "Carlos"
        assert schema.last_name is None
        assert schema.username is None

    def test_partial_update_with_multiple_fields(self):
        data = {"first_name": "Carlos", "last_name": "Silva", "phone": "+5511988887777"}
        schema = UserUpdateIn(**data)
        assert schema.first_name == "Carlos"
        assert schema.last_name == "Silva"
        assert schema.phone == "+5511988887777"

    def test_empty_update_is_valid(self):
        schema = UserUpdateIn()
        assert schema.first_name is None
        assert schema.last_name is None
        assert schema.username is None


class TestAddressIn:
    def test_valid_address(self):
        data = {
            "cep": "12345-678",
            "road": "Rua das Flores",
            "number": "123",
            "district": "Centro",
            "city": "São Paulo",
            "state": "SP",
            "principal": True
        }
        schema = AddressIn(**data)
        assert schema.cep == "12345-678"
        assert schema.state == "SP"

    def test_invalid_cep_format(self):
        data = {
            "cep": "12345678",
            "road": "Rua das Flores",
            "number": "123",
            "district": "Centro",
            "city": "São Paulo",
            "state": "SP",
        }
        with pytest.raises(ValidationError):
            AddressIn(**data)


class TestMessageOut:
    def test_message_output(self):
        data = {"detail": "Operação realizada com sucesso"}
        schema = MessageOut(**data)
        assert schema.detail == "Operação realizada com sucesso"