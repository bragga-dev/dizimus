from django.utils.translation import gettext_lazy as _


class UserAlreadyExists(Exception):
    def __init__(self, field: str = "email"):
        self.field = field
        super().__init__(_(f"Já existe um usuário com este {field}."))


class InvalidCredentials(Exception):
    def __init__(self):
        super().__init__(_("E-mail ou senha inválidos."))


class UserNotFound(Exception):
    def __init__(self):
        super().__init__(_("Usuário não encontrado."))


class InvalidPassword(Exception):
    def __init__(self):
        super().__init__(_("Senha atual incorreta."))


class InvalidToken(Exception):
    def __init__(self):
        super().__init__(_("Token inválido ou expirado."))


class PermissionDenied(Exception):
    def __init__(self, msg: str = "Você não tem permissão para realizar esta ação."):
        super().__init__(_(msg))