.PHONY: lint format fix test build up down logs


# ---------- Python Tasks ----------
lint:
	poetry run ruff check .

format:
	poetry run ruff format .

fix:
	poetry run ruff check --fix .
	poetry run ruff format .

test:
	poetry run pytest -v

run-server:
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


# ---------- Docker Tasks ----------
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f