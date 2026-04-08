.PHONY: lint format fix test build up down logs shell migration

DC = docker-compose
EXEC_API = $(DC) exec api

# ---------- Local Tasks (Fast & Clean) ----------
lint:
	poetry run ruff check .

format:
	poetry run ruff format .

fix:
	poetry run ruff check --fix .
	poetry run ruff format .

# ---------- Docker Tasks (Infrastructure) ----------
build:
	$(DC) build

up:
	$(DC) up -d

down:
	$(DC) down

logs:
	$(DC) logs -f api

shell:
	$(EXEC_API) /bin/bash

# ---------- Database & Migrations ----------
migration: # Usage: make migration m="add_users_table"
	$(EXEC_API) alembic revision --autogenerate -m "$(m)"

migrate:
	$(EXEC_API) alembic upgrade head

# ---------- Testing ----------
test:
	$(EXEC_API) pytest -v