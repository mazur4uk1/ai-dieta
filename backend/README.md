# AI-Dieta Backend

Полнофункциональный backend для мобильного приложения AI-Dieta на FastAPI.

## Функциональность

- **Авторизация**: Email/Password, SMS, Telegram OAuth
- **Управление пользователями**: Профиль, подписки
- **Питание**: Приёмы пищи, планы питания, шопинг-листы
- **Статистика**: Аналитика потребления
- **AI-распознавание еды**: Загрузка изображений для анализа
- **Подписки**: Тарифные планы

## Запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Документация API: http://localhost:8000/docs

## Структура проекта

- `app/api/` - Эндпоинты FastAPI
- `app/core/` - Конфигурация, база данных, безопасность
- `app/models/` - SQLAlchemy модели
- `app/schemas/` - Pydantic схемы
- `app/services/` - Бизнес-логика
- `tests/` - Тесты

## База данных

По умолчанию используется SQLite. Для продакшена настройте PostgreSQL в `.env`.

## Тестирование

```bash
pytest tests/
```

## Docker

```bash
docker build -t ai-dieta-backend .
docker run -p 8000:8000 ai-dieta-backend
```