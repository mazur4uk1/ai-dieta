# AI-Dieta Backend

Полнофункциональный backend для мобильного приложения AI-Dieta на FastAPI.

## Функциональность

- **Авторизация**: Email/Password, SMS, Telegram OAuth
- **Управление пользователями**: Профиль, подписки
- **Питание**: Приёмы пищи, планы питания, шопинг-листы
- **Статистика**: Аналитика потребления
- **AI-распознавание еды**: Загрузка изображений для анализа через бесплатные онлайн API
- **Подписки**: Тарифные планы

## Распознавание еды

Приложение использует бесплатные онлайн API для распознавания еды вместо локальных нейросетевых моделей. Это позволяет:

- Уменьшить размер Docker образа
- Улучшить точность распознавания
- Снизить требования к ресурсам

### Поддерживаемые API

1. **Edamam Food Detection API** (рекомендуется)
   - Бесплатно: 1000 запросов в месяц
   - Регистрация: https://developer.edamam.com/

2. **Google Cloud Vision API**
   - Бесплатно: 1000 единиц в месяц
   - Регистрация: https://cloud.google.com/vision

3. **Microsoft Azure Computer Vision**
   - Бесплатно: 5000 транзакций в месяц
   - Регистрация: https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/

### Настройка

Подробная инструкция по настройке API находится в файле [FOOD_RECOGNITION_SETUP.md](./FOOD_RECOGNITION_SETUP.md).

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