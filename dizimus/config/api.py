from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth
from ninja.errors import ValidationError, AuthenticationError
from django.http import HttpRequest
from django.http import JsonResponse

api = NinjaAPI(
    title="DIZIMUS API",
    version="1.0.0",
    description="API para gerenciamento de igrejas e membros.",
    auth=JWTAuth(),  # todas as rotas protegidas por padrão
    urls_namespace="api",
)

# ── Routers ───────────────────────────────────────────────────────────────────
# auth=False nas rotas de auth pois login/registro são públicos
api.add_router("/auth/",     "dizimus.apps.users.routers.auth_router",    tags=["Auth"])
api.add_router("/users/",    "dizimus.apps.users.routers.users_router",   tags=["Users"])
api.add_router("/churches/", "dizimus.apps.churches.routers.router",      tags=["Churches"])
api.add_router("/members/",  "dizimus.apps.members.routers.router",       tags=["Members"])


# ── Handlers de erro globais ──────────────────────────────────────────────────

@api.exception_handler(ValidationError)
def validation_error(request: HttpRequest, exc: ValidationError):
    return api.create_response(
        request,
        {"detail": exc.errors},
        status=422,
    )


@api.exception_handler(AuthenticationError)
def auth_error(request: HttpRequest, exc: AuthenticationError):
    return JsonResponse(
        {"detail": "Credenciais inválidas ou token expirado."},
        status=401,
    )