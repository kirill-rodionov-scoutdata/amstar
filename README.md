# Amstar

FastAPI + Clean Architecture. MySQL, async SQLAlchemy, dependency injection, JWT. Ready to extend.

---

## Prerequisites

| Tool | Version |
|------|---------|
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | latest |
| Docker + Docker Compose | latest |

---

## Run with Docker (recommended)

```bash
# 1. Clone and enter the project
git clone <repo-url> && cd amstar

# 2. Start everything (builds image, runs migrations, starts server)
make start
```

App is live at **http://localhost:8200**  
Swagger UI at **http://localhost:8200/docs**

```bash
# Stop
make stop
```

---

## Run locally (without Docker)

```bash
# 1. Install dependencies
uv sync

# 2. Copy and edit env (point DB__URL to your running MySQL)
cp .env_defaults .env

# 3. Run migrations
make migrate

# 4. Start the server
uv run python app/manage.py run-server
```

---

## Environment

All config lives in `.env_defaults` (committed defaults) and `.env` (local overrides, gitignored).

| Variable | Default | Description |
|----------|---------|-------------|
| `DB__URL` | `mysql+aiomysql://app:password@db:3306/amstar_db` | MySQL DSN |
| `DB__POOL_SIZE` | `10` | SQLAlchemy pool size |
| `API__PORT` | `8200` | HTTP port |
| `API__DOCS_ENABLED` | `true` | Enable Swagger/ReDoc |
| `JWT__SECRET` | `dev-secret-change-me` | **Change in production** |
| `JWT__ALGO` | `HS256` | JWT algorithm |
| `JWT__TTL` | `86400` | Token lifetime (seconds) |

Override any value by adding it to `.env`:
```bash
JWT__SECRET=my-real-secret
```

---

## Makefile Commands

```bash
make start    # docker compose up --build -d
make stop     # docker compose down
make migrate  # alembic upgrade head
make fmt      # ruff format + fix
make lint     # ruff check
make test     # pytest tests/
```

---

## Creating a Migration

```bash
uv run alembic revision --autogenerate -m "your message"
make migrate
```

---

## Project Structure

```
app/
├── config.py              # Pydantic settings (env-driven)
├── main.py                # FastAPI app + lifespan
├── manage.py              # CLI entry point (typer)
├── containers.py          # DI container (dependency-injector)
│
├── api/rest/internal/v1/
│   └── items/api.py       # HTTP controllers (@inject + Depends)
│
├── app_layer/
│   ├── interfaces/        # Abstract base classes (ABC)
│   │   ├── repositories/
│   │   ├── services/
│   │   └── unit_of_work/
│   ├── services/          # Concrete business logic
│   └── providers/jwt.py   # JWT issue/decode
│
├── domain/items/          # Entities, DTOs, enums, exceptions
│
└── infra/
    ├── db/                # Engine, ORM models, mixins
    ├── repositories/      # SQLAlchemy implementations
    └── unit_of_work/      # Session + transaction management

alembic/                   # Async migrations
tests/                     # pytest
```

**Request flow:** `HTTP → Controller → Service (via UoW) → Repository → MySQL`

---

## Example API Call

```bash
curl -X POST http://localhost:8200/api/internal/v1/items \
  -H "Content-Type: application/json" \
  -d '{"title": "My first item", "description": "optional"}'
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "My first item",
  "description": "optional",
  "created_at": "2026-04-06T12:00:00Z"
}
```

---

## Adding a New Domain

1. **Domain** — add entity/DTO/enum in `app/domain/<name>/`
2. **Interface** — add abstract repo in `app/app_layer/interfaces/repositories/`
3. **Service** — add concrete service in `app/app_layer/services/<name>/`
4. **Infra** — add SQLAlchemy repo in `app/infra/repositories/<name>/alchemy.py`
5. **ORM** — add model to `app/infra/db/models.py`, generate migration
6. **Container** — register new providers in `app/containers.py`
7. **API** — add router in `app/api/rest/internal/v1/<name>/api.py`, include in `controllers.py`
