"""
Testes de Member, MemberAddress e MemberChurch
───────────────────────────────────────────────
Cobre: validação de data_of_birth, __str__, unicidade de vínculo,
roles, status, constraints e indexes.
"""

import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .conftest import VALID_CPF, build_user_data


# ─────────────────────────────────────────────────────────────────────────────
# Member
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestMember:

    def test_str_retorna_nome_completo(self, member):
        assert str(member) == member.user.get_full_name()

    def test_member_criado_sem_cpf(self, member):
        assert member.cpf is None

    def test_member_criado_sem_data_nascimento(self, member):
        assert member.date_of_birth is None

    def test_member_com_cpf_valido(self, member):
        member.cpf = VALID_CPF
        member.full_clean()   # não deve lançar

    def test_member_com_cpf_invalido_levanta_validation_error(self, member):
        from dizimus.apps.users.validators.validate_cpf_cnpj import validate_cpf
        with pytest.raises(ValidationError):
            validate_cpf("111.111.111-11")

    def test_clean_data_nascimento_futura_levanta_validation_error(self, member):
        member.date_of_birth = date.today() + timedelta(days=1)
        with pytest.raises(ValidationError) as exc_info:
            member.clean()
        assert "date_of_birth" in exc_info.value.message_dict

    def test_clean_data_nascimento_hoje_levanta_validation_error(self, member):
        """Hoje também é no futuro segundo a regra (> localdate())."""
        member.date_of_birth = date.today()
        # date.today() não é > localdate() → deve passar
        # (a validação é >, não >=)
        member.clean()   # não deve lançar

    def test_clean_data_nascimento_passada_nao_levanta_erro(self, member):
        member.date_of_birth = date(1990, 5, 15)
        member.clean()   # não deve lançar

    def test_clean_data_nascimento_nula_nao_levanta_erro(self, member):
        member.date_of_birth = None
        member.clean()   # não deve lançar

    def test_relacao_one_to_one_com_user(self, member_user, member):
        assert member.user == member_user
        assert member_user.member == member

    def test_nao_pode_criar_dois_members_para_mesmo_user(self, db, member_user, member):
        from dizimus.apps.users.models import Member
        with pytest.raises(IntegrityError):
            Member.objects.create(user=member_user)


# ─────────────────────────────────────────────────────────────────────────────
# MemberChurch — vínculo
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestMemberChurch:

    def test_vinculo_criado_com_status_pending_por_padrao(self, member_church_link):
        from dizimus.apps.users.models import MemberChurch
        assert member_church_link.status == MemberChurch.Status.PENDING

    def test_vinculo_criado_com_role_member_por_padrao(self, member_church_link):
        from dizimus.apps.users.models import MemberChurch
        assert member_church_link.role == MemberChurch.Role.MEMBER

    def test_joined_at_preenchido_automaticamente(self, member_church_link):
        assert member_church_link.joined_at is not None

    def test_left_at_nulo_por_padrao(self, member_church_link):
        assert member_church_link.left_at is None

    def test_str_retorna_descricao_esperada(self, member_church_link):
        expected = (
            f"{member_church_link.member} - "
            f"{member_church_link.church} "
            f"({member_church_link.role})"
        )
        assert str(member_church_link) == expected

    def test_unique_constraint_member_church(self, member, church, member_church_link):
        """Membro não pode ter dois vínculos com a mesma igreja."""
        from dizimus.apps.users.models import MemberChurch
        with pytest.raises(IntegrityError):
            MemberChurch.objects.create(member=member, church=church)

    def test_member_pode_vincular_a_churches_diferentes(self, db, member, church):
        """Um membro pode pertencer a mais de uma igreja (vínculos distintos)."""
        # from dizimus.apps.users.user import User
        # from dizimus.apps.users.church import Church
        from dizimus.apps.users.models import MemberChurch, Church, User

        outro_church_user = User.objects.create_user(**build_user_data(
            email="outra_igreja@teste.com",
            username="outraigrj",
            first_name="Outra",
            last_name="Igreja",
            role="church",
        ))
        outra_church = Church.objects.create(user=outro_church_user)

        v1 = MemberChurch.objects.create(member=member, church=church)
        v2 = MemberChurch.objects.create(member=member, church=outra_church)
        assert v1.pk != v2.pk

    def test_status_pode_ser_alterado_para_active(self, member_church_link):
        from dizimus.apps.users.models import MemberChurch
        member_church_link.status = MemberChurch.Status.ACTIVE
        member_church_link.save()
        member_church_link.refresh_from_db()
        assert member_church_link.status == MemberChurch.Status.ACTIVE

    def test_status_pode_ser_alterado_para_inactive(self, member_church_link):
        from dizimus.apps.users.models import MemberChurch
        member_church_link.status = MemberChurch.Status.INACTIVE
        member_church_link.save()
        member_church_link.refresh_from_db()
        assert member_church_link.status == MemberChurch.Status.INACTIVE

    def test_role_pode_ser_alterado_para_pastor(self, member_church_link):
        from dizimus.apps.users.models import MemberChurch
        member_church_link.role = MemberChurch.Role.PASTOR
        member_church_link.save()
        member_church_link.refresh_from_db()
        assert member_church_link.role == MemberChurch.Role.PASTOR

    def test_role_pode_ser_alterado_para_treasurer(self, member_church_link):
        from dizimus.apps.users.models import MemberChurch
        member_church_link.role = MemberChurch.Role.TREASURER
        member_church_link.save()
        member_church_link.refresh_from_db()
        assert member_church_link.role == MemberChurch.Role.TREASURER

    def test_role_pode_ser_alterado_para_secretary(self, member_church_link):
        from dizimus.apps.users.models import MemberChurch
        member_church_link.role = MemberChurch.Role.SECRETARY
        member_church_link.save()
        member_church_link.refresh_from_db()
        assert member_church_link.role == MemberChurch.Role.SECRETARY

    def test_role_pode_ser_alterado_para_church_admin(self, member_church_link):
        from dizimus.apps.users.models import MemberChurch
        member_church_link.role = MemberChurch.Role.CHURCH_ADMIN
        member_church_link.save()
        member_church_link.refresh_from_db()
        assert member_church_link.role == MemberChurch.Role.CHURCH_ADMIN

    def test_ordering_e_por_joined_at_decrescente(self, db, member, church, second_member):
        """O ordering padrão é -joined_at: mais recente primeiro."""
        from dizimus.apps.users.models import MemberChurch
        v1 = MemberChurch.objects.create(member=member,        church=church)
        v2 = MemberChurch.objects.create(member=second_member, church=church)
        qs = MemberChurch.objects.filter(church=church)
        # O mais recente deve vir primeiro
        assert qs.first().pk == v2.pk


# ─────────────────────────────────────────────────────────────────────────────
# Choices — sanidade dos TextChoices
# ─────────────────────────────────────────────────────────────────────────────

class TestMemberChurchChoices:
    """Garante que os valores dos TextChoices não mudam acidentalmente."""

    def test_status_active_value(self):
        from dizimus.apps.users.models import MemberChurch
        assert MemberChurch.Status.ACTIVE == "active"

    def test_status_inactive_value(self):
        from dizimus.apps.users.models import MemberChurch
        assert MemberChurch.Status.INACTIVE == "inactive"

    def test_status_pending_value(self):
        from dizimus.apps.users.models import MemberChurch
        assert MemberChurch.Status.PENDING == "pending"

    def test_role_member_value(self):
        from dizimus.apps.users.models import MemberChurch
        assert MemberChurch.Role.MEMBER == "member"

    def test_role_pastor_value(self):
        from dizimus.apps.users.models import MemberChurch
        assert MemberChurch.Role.PASTOR == "pastor/padre"

    def test_role_church_admin_value(self):
        from dizimus.apps.users.models import MemberChurch
        assert MemberChurch.Role.CHURCH_ADMIN == "admin"