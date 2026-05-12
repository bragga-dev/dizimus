from pathlib import Path

import environ


# =========================================================
# BASE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# =========================================================
# ENV
# =========================================================

env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")


# =========================================================
# CORE
# =========================================================

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# =========================================================
# DJANGO APPS
# =========================================================

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# =========================================================
# THIRD PARTY APPS
# =========================================================

THIRD_PARTY_APPS = [
    "ninja",
    "ninja_simple_jwt",
]


# =========================================================
# LOCAL APPS
# =========================================================

LOCAL_APPS = [
    # "apps.core",
    # "apps.users",
    # "apps.churches",
    # "apps.members",
    # "apps.contributions",
    # "apps.payments",
    # "apps.receipts",
    # "apps.reports",
    # "apps.dashboards",
    # "apps.webhooks",
]


# =========================================================
# INSTALLED APPS
# =========================================================

INSTALLED_APPS = (
    DJANGO_APPS
    + THIRD_PARTY_APPS
    + LOCAL_APPS
)


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URLS
# =========================================================

ROOT_URLCONF = "config.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# WSGI / ASGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


# =========================================================
# DATABASE
# =========================================================

DATABASES = {
    "default": env.db()
}


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# SECURITY
# =========================================================

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])


# =========================================================
# REDIS / CELERY
# =========================================================

REDIS_URL = env("REDIS_URL",  default="redis://localhost:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL


# =========================================================
# LOGGING
# =========================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": (
                "[{asctime}] "
                "{levelname} "
                "{name} "
                "{message}"
            ),
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },

        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django.log",
            "formatter": "verbose",
        },
    },

    "root": {
        "handlers": [
            "console",
            "file",
        ],
        "level": "INFO",
    },

    "loggers": {
        "django.core.mail": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        }
    }
}


# =========================================================
# ASAAS
# =========================================================
ASAAS_API_KEY = env("ASAAS_API_KEY")
ASAAS_BASE_URL = env("ASAAS_BASE_URL", default="https://api-sandbox.asaas.com/v3")


# =========================================================
# EMAIL
# =========================================================
EMAIL_BACKEND = ("django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="bragawebdevelopment@gmail.com")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = "[Dizimus]"
ADMINS = [("Admin", env("ADMIN_EMAIL")),]
EMAIL_TIMEOUT = 30
EMAIL_USE_LOCALTIME = True
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
DEFAULT_CHARSET = "utf-8"
DEFAULT_REPLY_TO_EMAIL = env("DEFAULT_REPLY_TO_EMAIL", default=DEFAULT_FROM_EMAIL)

# =========================================================
# JWT
# =========================================================

NINJA_SIMPLE_JWT = {"USE_STATELESS_AUTH": False,}