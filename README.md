# Amstar

FastAPI + Clean Architecture. MySQL, async SQLAlchemy, dependency injection. Ready to extend.

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
---

## Makefile Commands

```bash
make start    # docker compose up --build -d
make stop     # docker compose down
make migrate  # alembic upgrade head
make lint     # ruff check
make test     # pytest tests/
```

---

## Testing

The project uses `pytest` for unit testing with `pytest-asyncio` for asynchronous tests. Coverage is measured using `pytest-cov`.

### Running Tests
To run all unit tests:
```bash
uv run pytest tests/unit
```

### Coverage Report
Coverage is configured by default in `pyproject.toml`. After running tests, you can see the report:
- **Terminal**: A summary is printed automatically after execution.
- **HTML Report**: A detailed line-by-line report is generated in `htmlcov/index.html`.

### Test Data
Tests are data-driven and utilize JSON files located in `tests/data/` for consistent and reproducible test cases.

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
│   └── bookings/api.py       # HTTP controllers (@inject + Depends)
│
├── app_layer/
│   ├── interfaces/        # Abstract base classes (ABC)
│   │   ├── repositories/
│   │   ├── services/
│   │   └── unit_of_work/
│   └──── services/          # Concrete business logic
│
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

## Examples of input data

1. POST create booking {
  "passenger_name": "Ivan Ivanov",
  "flight_number": "PRD83",
  "pickup_time": "2027-01-01T10:00:00Z",
  "pickup_location": "Amsterdam",
  "dropoff_location": "Bangkok"
}

2. UPDATE booking by id with new status {
  "booking_ids": [
    "8e1382c4-a362-4290-9e2c-e033c48874f7"
  ],
  "action": "next" /or/ "cancel"
}

3. GET booking by ID 92e67dd1-1327-4cef-8c71-1814488594b3

4. GET by date 2027-01-01

5. GET history by ID 92e67dd1-1327-4cef-8c71-1814488594b3
