# Сервис уведомлений

[![CI](https://github.com/annaputilovskaya/NotificationService/actions/workflows/ci.yml/badge.svg)](https://github.com/annaputilovskaya/NotificationService/actions/workflows/ci.yml)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/annaputilovskaya/097e2cc0afbb6ee7fdbfb4d2d67bb87d/raw/coverage.json)](https://github.com/annaputilovskaya/NotificationService/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)

API для надёжной доставки уведомлений пользователям по нескольким каналам — Email, SMS и Telegram — с автоматическим переключением между каналами при сбое.

[English version](README.md)

## Возможности

- **Пользователи** — регистрация по email и паролю, получение и обновление JWT-токена авторизации.

  <img width="1283" height="181" alt="Пользователи" src="https://github.com/user-attachments/assets/7e4815d7-6b3d-4df3-8355-7259a6694f6e" />

- **Получатели** — создание, просмотр, изменение и удаление получателей.

  <img width="1285" height="324" alt="Получатели" src="https://github.com/user-attachments/assets/0b7015b5-3b83-481f-9e83-4d3cc3b31d81" />

- **Уведомления** — создание уведомления, просмотр одного уведомления и списка.

  <img width="1283" height="177" alt="Уведомления" src="https://github.com/user-attachments/assets/4724f16d-c9ef-469c-bcaf-f63bb1f97a3d" />

- **Надёжная доставка (failover)** — при создании уведомления ставится задача Celery. Стратегии перебираются по порядку **Email → Telegram → SMS**: если канал не сработал, используется следующий. Если ни одна стратегия не сработала для части получателей, попытка повторяется для этих получателей через заданный интервал.
- **Пагинация** — эндпоинты списков отдают постраничный ответ `{"count": ..., "results": [...]}` (параметр `?page=`).
- **Логирование** — логи отправки пишутся в консоль и сохраняются в файл.
- Сервис ориентирован на разовые уведомления; поддержка повторяющихся уведомлений — возможная доработка.

## Стек

- Python 3.12
- Django REST Framework (Django ORM)
- PostgreSQL 17
- Celery + RabbitMQ
- drf-yasg (Swagger/Redoc)

## Архитектура

```mermaid
flowchart LR
    Client[Клиент] --> API[Django REST API]
    API -->|создание уведомления| Task[Celery: send_notification]
    Task --> Email[Email strategy]
    Email -->|fail| Telegram[Telegram strategy]
    Telegram -->|fail| SMS[SMS strategy]
    Email --> SMTP[(SMTP)]
    Telegram --> TG[(Telegram API)]
    SMS --> SMSAPI[(sms.ru)]
    Task --> DB[(PostgreSQL)]
```

## Модель данных

<img width="1189" height="757" alt="Схема базы данных" src="https://github.com/user-attachments/assets/7cfac615-f570-4744-85db-69e529d4a3b6" />

## Начало работы

### Требования

- Docker и Docker Compose

### Конфигурация

Скопируйте `.env.example` в `.env` и заполните значения:

```bash
cp .env.example .env
```

| Переменная | Описание | Пример |
|---|---|---|
| `SECRET_KEY` | Секретный ключ Django | `django-insecure-...` |
| `DEBUG` | Режим отладки | `False` |
| `ALLOWED_HOSTS` | Разрешённые хосты (через запятую) | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Разрешённые CORS-origins | `http://localhost:8000` |
| `POSTGRES_*` | Параметры подключения к БД | `POSTGRES_DB=notifications` |
| `CELERY_BROKER_URL` | URL брокера Celery (RabbitMQ) | `amqp://user:pass@rabbitmq:5672//` |
| `EMAIL_*` | Настройки почтового сервера | `EMAIL_HOST=smtp.example.com` |
| `TELEGRAM_TOKEN` | Токен Telegram-бота | `123456:ABC` |
| `SMS_API_KEY` / `SMS_SENDER` | Доступ к sms.ru | `SMS_SENDER=Service` |
| `SMS_TEST` | Тестовый режим sms.ru (не отправляет СМС) | `0` |

### Установка и запуск

Склонируйте репозиторий и запустите сервисы:

```bash
git clone https://github.com/annaputilovskaya/NotificationService.git
cd NotificationService
docker compose up -d --build
```

Проверка версии Docker (если не установлен — [инструкция](https://www.docker.com/)):

```bash
docker --version
```

Интерактивная документация API (Swagger): http://localhost:8000/swagger/

## Тесты

Тесты запускаются на PostgreSQL. Поднимите БД и выполните:

```bash
docker compose up -d db
python -m pytest --cov
```

Внешние сервисы (SMTP, Telegram, sms.ru) в тестах замоканы. Ранее проект проверялся вручную через Postman; теперь добавлены автоматизированные тесты ядра и smoke.

## Структура проекта

```
config/           # настройки Django, Celery, urls
notifications/    # уведомления: модель, стратегии, задача Celery
recipients/       # получатели
users/            # пользователи, JWT
conftest.py       # общие фикстуры pytest
pyproject.toml    # конфиг ruff/pytest/coverage
```

## Лицензия

Проект распространяется под лицензией MIT — см. [LICENSE](LICENSE).
