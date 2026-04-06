start:
	docker compose up --build -d

stop:
	docker compose down

lint:
	uv run ruff check . && uv run ruff format --check .

test:
	uv run pytest tests/

migrate:
	uv run alembic upgrade head
