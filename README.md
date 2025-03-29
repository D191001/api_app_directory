# API App Directory

REST API сервис для управления справочником организаций, зданий и видов деятельности.

## Стек технологий

- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL
- Docker & Docker Compose
- Pydantic

## Быстрый старт

### Запуск через Docker

```bash
git clone <repository-url>
cd api_app_directory
cp .env.example .env  # Настройте переменные окружения
docker-compose up --build
```

API будет доступен по адресу: http://localhost:8000
Swagger UI: http://localhost:8000/docs

## API Endpoints

### Организации
- `GET /organizations` - список организаций
- `GET /organizations/{id}` - детали организации
- `GET /organizations/search` - поиск организаций
  - По названию: `?name=текст`
  - По координатам: `?latitude=X&longitude=Y&radius=Z`
- `POST /organizations` - создание организации

### Здания
- `GET /buildings` - список зданий
- `GET /buildings/{id}` - детали здания
- `GET /buildings/{id}/organizations` - организации в здании
- `POST /buildings` - создание здания

### Виды деятельности
- `GET /activities` - список видов деятельности
- `GET /activities/{id}` - детали вида деятельности
- `GET /activities/search?activity_name=name` - поиск по деятельности
- `POST /activities` - создание вида деятельности

## Аутентификация

Все запросы требуют заголовок `X-API-Key`:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/organizations
```

## Локальная разработка

1. Создание виртуального окружения:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
```

2. Установка зависимостей:
```bash
pip install -r requirements.txt
```

3. Настройка базы данных:
```bash
# Создание БД
psql -U postgres -c "CREATE DATABASE app_db"

# Применение миграций
alembic upgrade head
```

4. Запуск сервера разработки:
```bash
uvicorn app.main:app --reload
```

## Структура проекта

```
api_app_directory/
├── app/
│   ├── routes/          # API эндпоинты
│   ├── models.py        # SQLAlchemy модели
│   ├── schemas.py       # Pydantic схемы
│   ├── crud.py         # CRUD операции
│   ├── database.py     # Настройки БД
│   └── main.py         # Точка входа
├── alembic/            # Миграции
├── docker/             # Docker файлы
└── tests/             # Тесты
```

## Миграции

Создание новой миграции:
```bash
alembic revision --autogenerate -m "description"
```

Применение миграций:
```bash
alembic upgrade head
```

## Тестирование

```bash
pytest
```

## Переменные окружения

Необходимые переменные (`.env`):
- `POSTGRES_USER` - пользователь БД
- `POSTGRES_PASSWORD` - пароль БД
- `POSTGRES_DB` - имя БД
- `DATABASE_URL` - URL подключения к БД
- `API_KEY` - ключ API для аутентификации

## Лицензия

MIT