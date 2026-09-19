# Task Manager

Веб-приложение для управления задачами. Позволяет ставить задачи, назначать исполнителей, менять статусы, помечать метками и фильтровать список.

[![hexlet-check](https://github.com/artemcherepanov2357/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/artemcherepanov2357/python-project-52/actions)

## Демо
https://python-project-52-747b.onrender.com/

## Стек

- **Python 3.14**, [uv](https://github.com/astral-sh/uv)
- **Django** — ORM, шаблоны, формы, аутентификация
- **PostgreSQL** — продакшен, **SQLite** — локально
- **django-tailwind-cli** + **@tailwindcss/forms** — стилизация
- **Whitenoise** — раздача статики
- **Gunicorn** — WSGI-сервер
- **Render.com** — хостинг, PostgreSQL
- **python-dotenv**, **dj-database-url** — переменные окружения

## Локальный запуск

```bash
# Установка зависимостей
uv sync

# Переменные окружения — создай файл .env
cp .env.example .env
# заполни SECRET_KEY, DEBUG=True, DATABASE_URL=sqlite:///db.sqlite3

# Сборка стилей
uv run python manage.py tailwind build

# Миграции
uv run python manage.py migrate

# Запуск
uv run python manage.py runserver

# Тесты
uv run python manage.py test apps
```