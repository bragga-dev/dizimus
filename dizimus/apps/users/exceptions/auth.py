from django.utils.translation import gettext_lazy as _


class InvalidCredentials(Exception):
    def __init__(self):
        super().__init__(_("E-mail ou senha inválidos."))


class InvalidPassword(Exception):
    def __init__(self):
        super().__init__(_("Senha atual incorreta."))


class InvalidToken(Exception):
    def __init__(self):
        super().__init__(_("Token inválido ou expirado."))