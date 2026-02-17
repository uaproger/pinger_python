# Pinger Pro System

Система асинхронного моніторингу доступності веб-сервісів.

## Технологічний стек:
- **Backend**: Django 5, DRF (Class Based Views, Permissions).
- **Frontend**: Vue 3, Vite, Bootstrap 5.
- **Async Logic**: Celery & Redis.
- **Infrastructure**: Docker & Docker Compose.

## Особливості:
- Реєстрація та JWT авторизація.
- Кожен користувач керує лише власними сервісами (Owner-based permissions).
- Автоматична перевірка статусів кожні 5 хвилин через Celery Beat.
- Повна контейнеризація всіх сервісів.

@AlexProger 2026