# Dizimus

> Sistema de gestão de igrejas

![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DD0031?style=flat&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=flat&logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)

---

## Stack

| Camada | Tecnologias |
|--------|------------|
| **Backend** | Django · Django Ninja · Pydantic · Celery |
| **Banco de Dados** | PostgreSQL |
| **Cache / Fila** | Redis |
| **Armazenamento** | MinIO (S3 Compatible) |
| **Infraestrutura** | Docker · Docker Compose · Nginx · Gunicorn · Whitenoise |

---

## Arquitetura do Projeto

### Estrutura de Diretórios

```
dizimus/
│
├── .env
├── .env.example
├── .gitignore
├── manage.py
├── Dockerfile
├── docker-compose.dev.yml
└── docker-compose.prod.yml
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
|   ├── celery.py
│   ├── wsgi.py
│   ├── urls.py
│   ├── api.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       ├── prod.py
│       └── test.py
│
├── apps/
│   ├── core/
│   ├── churches/
│   ├── users/
│   ├── members/
│   ├── contributions/
│   ├── payments/
│   ├── receipts/
│   ├── reports/
│   ├── dashboards/
│   ├── webhooks/
│   └── integrations/
│       └── asaas/
│
├── docker/
│   ├── django/
│   │   └── entrypoint.sh
│   ├── nginx/
│   │   └── default.conf
│   ├── postgres/
│   └── redis/
│
├── minio/
│   └── data/
│
├── templates/
├── static/
├── media/
├── logs/
└── scripts/
```

---

### Estrutura Interna dos Apps

Cada app segue uma arquitetura baseada em separação de responsabilidades:

```
apps/users/
│
├── admin/
│   ├── user_admin.py
│   ├── group_admin.py
│   └── __init__.py
│
├── api/
│   ├── auth.py
│   ├── profile.py
│   ├── verification.py
│   ├── password_reset.py
│   ├── sessions.py
│   └── __init__.py
│
├── schemas/
│   ├── auth.py
│   ├── profile.py
│   ├── verification.py
│   ├── password_reset.py
│   ├── common.py
│   └── __init__.py
│
├── models/
│   ├── user.py
│   ├── profile.py
│   ├── session.py
│   ├── security_event.py
│   └── __init__.py
│
├── services/
│   ├── auth/
│   │   ├── login.py
│   │   ├── register.py
│   │   ├── refresh_token.py
│   │   ├── logout.py
│   │   └── change_password.py
│   │
│   ├── profile/
│   │   ├── update_profile.py
│   │   ├── upload_avatar.py
│   │   └── remove_avatar.py
│   │
│   ├── verification/
│   │   ├── send_email.py
│   │   ├── verify_email.py
│   │   └── resend_email.py
│   │
│   ├── password_reset/
│   │   ├── request_reset.py
│   │   ├── confirm_reset.py
│   │   └── validate_token.py
│   │
│   └── __init__.py
│
├── selectors/
│   ├── users.py
│   ├── profiles.py
│   ├── sessions.py
│   └── __init__.py
│
├── repositories/
│   ├── users.py
│   ├── profiles.py
│   ├── sessions.py
│   └── __init__.py
│
├── tasks/
│   ├── emails.py
│   ├── cleanup.py
│   ├── security.py
│   └── __init__.py
│
├── tokens/
│   ├── email_verification.py
│   ├── password_reset.py
│   ├── jwt.py
│   └── __init__.py
│
├── permissions/
│   ├── roles.py
│   ├── auth.py
│   ├── ownership.py
│   └── __init__.py
│
├── validators/
│   ├── password.py
│   ├── username.py
│   ├── image.py
│   └── __init__.py
│
├── exceptions/
│   ├── auth.py
│   ├── verification.py
│   ├── profile.py
│   └── __init__.py
│
├── constants/
│   ├── roles.py
│   ├── auth.py
│   ├── limits.py
│   └── __init__.py
│
├── filters/
│   ├── users.py
│   └── __init__.py
│
├── signals/
│   ├── auth.py
│   ├── profile.py
│   └── __init__.py
│
├── utils/
│   ├── slug.py
│   ├── ip.py
│   ├── device.py
│   └── __init__.py
│
├── tests/
│   ├── factories/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── __init__.py
│
├── migrations/
│
├── apps.py
├── urls.py
└── __init__.py
```

---

## Responsabilidade dos Arquivos

| Arquivo | Camada | Responsabilidade |
|---------|--------|-----------------|
| `models.py` | Dados | Modelos do banco de dados |
| `repositories.py` | Dados | Persistência e acesso ao banco |
| `selectors.py` | Dados | Queries e leitura de dados |
| `schemas.py` | API | Schemas do Django Ninja / Pydantic |
| `api.py` | API | Endpoints da API |
| `filters.py` | API | Filtros de consulta |
| `permissions.py` | API | Controle de permissões |
| `services.py` | Negócio | Regras de negócio |
| `tasks.py` | Negócio | Tarefas assíncronas do Celery |
| `signals.py` | Negócio | Eventos do Django |
| `constants.py` | Infra | Constantes do domínio |
| `exceptions.py` | Infra | Exceções customizadas |

---

## Ambientes

### Desenvolvimento

```bash
cp .env.example .env
docker compose -f docker-compose.dev.yml up --build
```

### Produção

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

---

## Comandos Úteis

```bash
# Migrações
docker compose exec web python manage.py migrate

# Superusuário
docker compose exec web python manage.py createsuperuser

# Celery worker
celery -A config worker -l info
```

---

## MinIO

| Interface | URL |
|-----------|-----|
| Painel Administrativo | `http://localhost:9001` |
| Endpoint S3 | `http://localhost:9000` |

---

## Objetivos da Arquitetura

- **Alta escalabilidade** — estrutura modular preparada para crescimento
- **Separação de responsabilidades** — cada arquivo tem um papel claro
- **Fácil manutenção** — organização previsível em todos os apps
- **Preparação para microsserviços** — apps independentes e desacoplados
- **Infraestrutura pronta para produção** — Docker, Nginx, Gunicorn e Whitenoise configurados

# 🧪 Testes

O projeto utiliza:

* `pytest`
* `pytest-django`
* `pytest-cov`

---

# Instalação

## Pip

```bash
pip install pytest pytest-django pytest-cov
```

## Poetry

```bash
poetry add --group dev pytest pytest-django pytest-cov
```

---

# Rodando os testes

## Rodar todos os testes

```bash
pytest
```

---

## Rodar testes com coverage

```bash
pytest --cov=dizimus --cov-report=term-missing
```

---

## Rodar testes de um app específico

### Users

```bash
pytest dizimus/apps/users/tests/
```

### Community

```bash
pytest dizimus/apps/community/tests/
```

---

## Rodar testes de um diretório específico

### Schemas

```bash
pytest dizimus/apps/users/tests/schemas/
```

### Models

```bash
pytest dizimus/apps/users/tests/models/
```

### Services

```bash
pytest dizimus/apps/users/tests/services/
```

---

# Coverage por módulo

## Schemas

```bash
pytest dizimus/apps/users/tests/schemas/ \
    --cov=dizimus.apps.users.schemas \
    --cov-report=term-missing
```

---

## Models

```bash
pytest dizimus/apps/users/tests/models/ \
    --cov=dizimus.apps.users.models \
    --cov-report=term-missing
```

---

## Validators

```bash
pytest dizimus/apps/users/tests/validators/ \
    --cov=dizimus.apps.users.validators \
    --cov-report=term-missing
```

---

## Services

```bash
pytest dizimus/apps/users/tests/services/ \
    --cov=dizimus.apps.users.services \
    --cov-report=term-missing
```

---

# Flags úteis

## Verbose

```bash
pytest -vv
```

---

## Mostrar prints/logs

```bash
pytest -s
```

---

## Parar no primeiro erro

```bash
pytest -x
```

---

## Reexecutar apenas testes que falharam

```bash
pytest --lf
```

---

## Executar um teste específico

```bash
pytest path/to/test_file.py
```

Exemplo:

```bash
pytest dizimus/apps/users/tests/models/test_user.py
```

---

## Executar uma classe específica

```bash
pytest path/to/test_file.py::TestClassName
```

Exemplo:

```bash
pytest dizimus/apps/users/tests/models/test_user.py::TestUserModel
```

---

## Executar um método específico

```bash
pytest path/to/test_file.py::TestClassName::test_method_name
```

Exemplo:

```bash
pytest dizimus/apps/users/tests/models/test_user.py::TestUserModel::test_create_user
```

---

# Coverage HTML

Gerar relatório HTML:

```bash
pytest --cov=dizimus --cov-report=html
```

Abrir relatório:

```bash
xdg-open htmlcov/index.html
```

---

# Configuração recomendada do Coverage

Adicionar no `pyproject.toml`:

```toml
[tool.coverage.run]
omit = [
    "*/migrations/*",
    "*/config/*",
]
```

---

# Estrutura recomendada de testes

```text
apps/
└── users/
    └── tests/
        ├── models/
        ├── schemas/
        ├── services/
        ├── validators/
        ├── api/
        └── conftest.py
```

---

# Boas práticas

* Testar regras de negócio antes de testar interface/admin.
* Priorizar testes de:

  * services
  * validators
  * models
  * autenticação
  * permissões
* Utilizar factories e fixtures reutilizáveis.
* Evitar testes frágeis baseados em textos HTML.
* Manter coverage acima de 80%.
