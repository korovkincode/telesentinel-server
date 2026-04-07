# TeleSentinel

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-6F42C1?style=flat&logo=celery&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FF6600?style=flat&logo=sqlalchemy&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-4B0082?style=flat&logo=python&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-F4A261?style=flat&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-FFD700?style=flat&logo=pytest&logoColor=black)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=flat&logo=rabbitmq&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-FFDD00?style=flat&logo=github&logoColor=black)  

TeleSentinel-Server is a backend service for monitoring Telegram chats, analyzing messages using LLMs, and collecting users based on semantic filters.

## 🚀 Features

- Telegram channel parsing via user accounts (Telethon)
- Message analysis using LLM (score 1–100)
- Flexible task scheduling (one-time & recurring)
- Scalable background processing with Celery
- REST API with authentication (JWT)
- PostgreSQL as the single source of truth

---

## 🏗 Architecture

- **API**: FastAPI
- **Workers**: Celery
- **Queue Broker**: RabbitMQ
- **Database**: PostgreSQL
- **Telegram Client**: Telethon
- **LLM Provider**: OpenAI API (or compatible)
- **Scheduler**: Celery Beat
- **Containerization**: Docker

---

## 📦 Project Structure

```

app/
   api/            # FastAPI routers
   core/           # config, settings, security
   exc/            # app exceptions
   execution/      # execution logic
   models/         # SQLAlchemy models
   repositories/   # DB access layer
   schemas/        # Pydantic
   services/       # business logic
   tasks/          # Celery Setup (worker.py, celery_app.py)
      jobs/        # Celery Tasks (run_task.py, scheduler.py)
   utils/          # helpers

migrations/        # Alembic
docker/            # Docker configs

```

---

## ⚙️ Setup

### 1. Clone repository

```bash
git clone <repo_url>
cd telesentinel
```

### 2. Environment variables

Create `.env` file:

```env
IS_PROD=0

SUPERUSER_LOGIN=superuser_login
SUPERUSER_PASSWORD=superuser_password

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/telesentinel
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672//

JWT_ALGORITHM=HS256
SECRET_KEY=your_secret

ACCESS_TOKEN_EXPIRES_MINUTES=60
REFRESH_TOKEN_EXPIRES_DAYS=7
REFRESH_TOKEN_COOKIE_NAME=your_cookie_name

OPENAI_API_KEY=your_key
```

---

### 3. Run with Docker

```bash
make build
make up  
```

---

## 🔁 Services

* `api` – FastAPI app
* `worker` – Celery worker
* `beat` – Celery scheduler
* `db` – PostgreSQL
* `rabbitmq` – message broker

---

## 🔄 Core Flow

1. Scheduler creates `TaskRun`
2. Task is sent to Celery
3. Worker:
   * fetches Telegram messages
   * sends to LLM
   * filters by threshold
   * saves results
4. Updates `TaskRun` status

---

## 🧠 Key Design Decisions

* No Celery result backend → PostgreSQL is the source of truth
* Idempotent tasks
* Retry with exponential backoff
* Clear separation: API / Services / Repositories / Tasks

---

## ⚠️ Notes

* Telegram rate limits must be respected
* LLM usage should be optimized (cost & latency)
* Deduplication is required for messages
* Data retention: 14 days (cleanup job required)

---

## 🛠 Roadmap

* [ ] Auth & user management
* [ ] Telegram account integration
* [ ] Task management API
* [ ] Parsing worker
* [ ] LLM integration
* [ ] Result storage & querying
* [ ] Cleanup jobs

---