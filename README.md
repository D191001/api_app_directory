# API App Directory

REST API для справочника организаций с поддержкой геолокации и поиска.

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone git@github.com:D191001/api_app_directory.git
cd api_app_directory
```

### 2. Настройка окружения
```bash
# Переименовать файл с переменными окружения
mv env.txt .env
```

### 3. Запуск с Docker Compose
```bash
# Сборка и запуск контейнеров
docker-compose up -d --build

# Проверка статуса контейнеров
docker-compose ps
```

### 4. Применение миграций
```bash
# Применение миграций для создания таблиц и PostGIS расширения
docker-compose exec app alembic upgrade head
```

### 5. Загрузка тестовых данных
```bash
# Запуск скрипта для загрузки тестовых данных
docker-compose exec app python -m app.data_loader
```

## Тестирование API

API доступно по адресу: http://localhost:8000

Swagger UI документация: http://localhost:8000/docs

### Основные эндпоинты:

- `GET /organizations` - список всех организаций
- `GET /organizations/search` - поиск организаций по параметрам
- `GET /buildings/nearest` - поиск ближайших зданий
- `GET /buildings/bounds` - поиск зданий в границах
- `GET /buildings/search/radius` - поиск зданий в радиусе
- `GET /activities` - список видов деятельности

### Примеры запросов:

1. Поиск ближайших зданий:
```bash
curl "http://localhost:8000/buildings/nearest?latitude=55.7648&longitude=37.6059&limit=5" \
-H "X-API-Key: your-super-secret-key"
```

2. Поиск организаций в радиусе:
```bash
curl "http://localhost:8000/buildings/search/radius?latitude=55.7648&longitude=37.6059&radius=1" \
-H "X-API-Key: your-super-secret-key"
```

3. Поиск зданий в границах:
```bash
curl "http://localhost:8000/buildings/bounds?min_lat=55&max_lat=57&min_lon=37&max_lon=61" \
-H "X-API-Key: your-super-secret-key"
```

## Лицензия

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



