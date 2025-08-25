# Task Manager API

Простое REST API для управления задачами, построенное на FastAPI с PostgreSQL.

## Функциональность

- Создание, чтение, обновление и удаление задач
- Пагинация списка задач
- Статусы задач: CREATED, IN_PROGRESS, COMPLETED
- Автоматическая документация API (Swagger UI)

## Быстрый запуск

1. **Клонируйте репозиторий**:
```bash
git clone <your-repo-url>
cd task_manager
```

2. **Запустите приложение**:
```bash
docker-compose up -d
```

3. **Откройте в браузере**:
- API: http://localhost:8000
- Документация: http://localhost:8000/docs
- PostgreSQL: localhost:5432

## API Endpoints

- `GET /api/v1/tasks` - список задач
- `POST /api/v1/tasks` - создать задачу
- `GET /api/v1/tasks/{id}` - получить задачу
- `PATCH /api/v1/tasks/{id}` - обновить задачу
- `DELETE /api/v1/tasks/{id}` - удалить задачу

## Переменные окружения

Приложение использует настройки по умолчанию, но можно настроить через `.env`:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=task_manager
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## Миграции базы данных

Миграции применяются автоматически при запуске контейнера.