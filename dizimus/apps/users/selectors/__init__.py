"""
Selectors — apenas leitura do banco.
Nenhuma escrita acontece aqui.
"""
from .user import (
    get_user_by_id,
    get_user_by_email,
    get_user_by_slug,
    email_exists,
    username_exists,
    get_active_users,
    get_users_by_role,
)

# Opcional: descomente se criar o profile.py
# from .profile import (
#     get_church_by_cnpj,
#     get_member_by_cpf,
#     get_church_by_user_id,
#     get_member_by_user_id,
# )

__all__ = [
    # User
    "get_user_by_id",
    "get_user_by_email",
    "get_user_by_slug",
    "email_exists",
    "username_exists",
    "get_active_users",
    "get_users_by_role",
    # Profile 
     "get_church_by_cnpj",
     "get_member_by_cpf",
     "get_church_by_user_id",
     "get_member_by_user_id",
]