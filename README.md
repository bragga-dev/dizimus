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
apps/members/
│
├── migrations/
│
├── models.py          # Modelos do banco de dados
├── schemas/           # Schemas do Django Ninja / Pydantic
├── api.py             # Endpoints da API
├── services.py        # Regras de negócio
├── selectors.py       # Queries e leitura de dados
├── repositories.py    # Persistência e acesso ao banco
├── tasks.py           # Tarefas assíncronas do Celery
├── permissions.py     # Controle de permissões
├── filters.py         # Filtros de consulta
├── signals.py         # Eventos do Django
├── constants.py       # Constantes do domínio
├── exceptions.py      # Exceções customizadas
├── apps.py
├── urls.py
│
└── tests/
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