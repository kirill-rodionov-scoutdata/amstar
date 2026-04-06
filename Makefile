start:
	docker compose up --build -d

stop:
	docker compose down

lint:
	uv run ruff check . && uv run ruff format --check .

fmt:
	uv run ruff format . && uv run ruff check --fix .

test:
	uv run pytest tests/

migrate:
	uv run alembic upgrade head
