from django.http import HttpRequest
from ninja.security import HttpBearer
from ninja_jwt.authentication import JWTAuth
from users.models import User


# ── Guardas de role ────────────────────────────────────────────────────────

def require_church(user: User) -> bool:
    """Levanta 403 se o usuário não for uma Igreja."""
    return user.role == User.UserRole.CHURCH


def require_member(user: User) -> bool:
    """Levanta 403 se o usuário não for um Membro."""
    return user.role == User.UserRole.MEMBER


def require_superuser(user: User) -> bool:
    """Levanta 403 se o usuário não for superuser (admin do sistema)."""
    return user.is_superuser


# ── Decorador de permissão para endpoints ─────────────────────────────────
# Uso nos endpoints:
#
#   @router.get("/algo")
#   def endpoint(request):
#       check_permission(request.auth, require_church)
#       ...

def check_permission(user: User, *checks) -> None:
    from users.exceptions import PermissionDenied
    for check in checks:
        if not check(user):
            raise PermissionDenied()