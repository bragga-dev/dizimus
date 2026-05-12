from .base import *


# =========================================================
# CORE
# =========================================================

DEBUG = True

SECRET_KEY = env(
    "SECRET_KEY",
    default="dev-secret-key"
)

ALLOWED_HOSTS = [
    "*",
]


# =========================================================
# DATABASE
# =========================================================

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=(
            "postgres://postgres:"
            "123456@localhost:5432/dizimus"
        )
    )
}


# =========================================================
# STATIC / MEDIA
# =========================================================

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"


# =========================================================
# EMAIL
# =========================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)

# SMTP REAL (descomentar quando precisar)
#
# EMAIL_BACKEND = (
#     "django.core.mail.backends.smtp.EmailBackend"
# )
#
# EMAIL_HOST = env("EMAIL_HOST")
# EMAIL_PORT = env.int("EMAIL_PORT", default=587)
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = True


# =========================================================
# CACHE
# =========================================================

CACHES = {
    "default": {
        "BACKEND": (
            "django.core.cache.backends.locmem."
            "LocMemCache"
        ),
    }
}


# =========================================================
# SESSION
# =========================================================

SESSION_ENGINE = (
    "django.contrib.sessions.backends.db"
)


# =========================================================
# SECURITY (DEV)
# =========================================================

CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False


# =========================================================
# DJANGO NINJA
# =========================================================

NINJA_PAGINATION_CLASS = (
    "ninja.pagination.LimitOffsetPagination"
)

NINJA_PAGINATION_PER_PAGE = 20


# =========================================================
# CORS (FUTURO FRONTEND SEPARADO)
# =========================================================

CORS_ALLOW_ALL_ORIGINS = True

# =========================================================
# CELERY
# =========================================================

CELERY_TASK_ALWAYS_EAGER = False

CELERY_TASK_EAGER_PROPAGATES = True


# =========================================================
# DEBUG TOOLBAR
# =========================================================

INTERNAL_IPS = [
    "127.0.0.1",
]