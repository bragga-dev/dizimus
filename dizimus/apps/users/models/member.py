from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from dizimus.apps.users.validators.validate_cpf_cnpj import validate_cpf
from .user import User
from .base_address import BaseAddress


class Member(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="member",
    )
    cpf = models.CharField(
        max_length=14, unique=True, null=True, blank=True,
        validators=[validate_cpf],
        help_text=_('Formato: 000.000.000-00.'),
    )
    date_of_birth = models.DateField(
        _('Data de nascimento'), null=True, blank=True,
        help_text=_('Formato: DD/MM/AAAA.'),
    )

    class Meta:
        verbose_name        = "Membro"
        verbose_name_plural = "Membros"

    def __str__(self):
        return self.user.get_full_name()

    def clean(self):
        if self.date_of_birth and self.date_of_birth > timezone.localdate():
            raise ValidationError(
                {'date_of_birth': _('Data de nascimento não pode ser no futuro.')}
            )


class MemberAddress(BaseAddress):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='addresses',
    )

    def save(self, *args, **kwargs):
        if self.principal:
            MemberAddress.objects.filter(
                member=self.member, principal=True,
            ).exclude(pk=self.pk).update(principal=False)
        super().save(*args, **kwargs)


