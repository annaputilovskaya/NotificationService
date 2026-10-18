# Notification Service

[![CI](https://github.com/annaputilovskaya/NotificationService/actions/workflows/ci.yml/badge.svg)](https://github.com/annaputilovskaya/NotificationService/actions/workflows/ci.yml)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/annaputilovskaya/097e2cc0afbb6ee7fdbfb4d2d67bb87d/raw/coverage.json)](https://github.com/annaputilovskaya/NotificationService/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)

An API for reliable delivery of notifications to users across multiple channels — Email, SMS, and Telegram — with automatic failover between channels.

[Русская версия](README.ru.md)

## Features

- **Users** — email/password sign-up, issuing and refreshing JWT access tokens.

  <img width="1283" height="181" alt="Users" src="https://github.com/user-attachments/assets/7e4815d7-6b3d-4df3-8355-7259a6694f6e" />

- **Recipients** — create, view, update, and delete recipients.

  <img width="1285" height="324" alt="Recipients" src="https://github.com/user-attachments/assets/0b7015b5-3b83-481f-9e83-4d3cc3b31d81" />

- **Notifications** — create a notification, view a single notification and a list.

  <img width="1077" height="153" alt="Notifications" src="https://github.com/user-attachments/assets/ffaec4e6-269d-45a7-94ec-140b19d542f5" />

- **Reliable delivery (failover)** — creating a notification enqueues a Celery task. Strategies are tried in order **Email → Telegram → SMS**: when a channel fails, the next one is used. If no strategy succeeds for some recipients, delivery to those recipients is retried after a delay.
- **Pagination** — list endpoints return a paginated `{"count": ..., "results": [...]}` payload (the `?page=` parameter).
- **Logging** — delivery logs go to the console and to a file.
- The service targets one-off notifications; recurring notifications are a possible extension.

## Stack

- Python 3.12
- Django REST Framework (Django ORM)
- PostgreSQL 17
- Celery + RabbitMQ
- drf-yasg (Swagger/Redoc)

## Architecture

```mermaid
flowchart LR
    Client["Client"] --> API["Django REST API"]
    API -->|create notification| Task["Celery: send_notification"]
    Task --> Email["Email strategy"]
    Email -->|fail| Telegram["Telegram strategy"]
    Telegram -->|fail| SMS["SMS strategy"]
    Email --> SMTP[("SMTP")]
    Telegram --> TG[("Telegram API")]
    SMS --> SMSAPI[("sms.ru")]
    Task --> DB[("PostgreSQL")]
```

## Data model

<img width="1189" height="757" alt="Database schema" src="https://github.com/user-attachments/assets/7cfac615-f570-4744-85db-69e529d4a3b6" />

## Getting started

### Prerequisites

- Docker and Docker Compose

### Configuration

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts (comma-separated) | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | `http://localhost:8000` |
| `POSTGRES_*` | Database connection settings | `POSTGRES_DB=notifications` |
| `CELERY_BROKER_URL` | Celery broker URL (RabbitMQ) | `amqp://user:pass@rabbitmq:5672//` |
| `EMAIL_*` | Mail server settings | `EMAIL_HOST=smtp.example.com` |
| `TELEGRAM_TOKEN` | Telegram bot token | `123456:ABC` |
| `SMS_API_KEY` / `SMS_SENDER` | sms.ru credentials | `SMS_SENDER=Service` |
| `SMS_TEST` | sms.ru test mode (does not send SMS) | `0` |

### Install & run

Clone the repository and start the services:

```bash
git clone https://github.com/annaputilovskaya/NotificationService.git
cd NotificationService
docker compose up -d --build
```

Verify Docker is installed (otherwise follow the [official instructions](https://www.docker.com/)):

```bash
docker --version
```

Interactive API documentation (Swagger): http://localhost:8000/swagger/

## Tests

Tests run against PostgreSQL. Start the database and run:

```bash
docker compose up -d db
python -m pytest --cov
```

External services (SMTP, Telegram, sms.ru) are mocked. The project was originally checked manually via Postman; automated core and smoke tests are now in place.

## Project structure

```
config/           # Django settings, Celery, urls
notifications/    # notifications: model, strategies, Celery task
recipients/       # recipients
users/            # users, JWT
conftest.py       # shared pytest fixtures
pyproject.toml    # ruff/pytest/coverage config
```

## License

Released under the MIT License — see [LICENSE](LICENSE).
