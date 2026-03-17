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

- Уменьшить размер Docker образа (с >12ГБ до ~100-200МБ)
- Улучшить точность распознавания
- Снизить требования к ресурсам

### Поддерживаемые API

#### 1. **Edamam Nutrition Analysis API** (рекомендуется, ключи уже настроены)
   - Бесплатно: 1000 запросов в месяц
   - API ключи: APP_ID=b803dc99, APP_KEY=50ba16cca84c4a5932779cc7c2a7e2e6
   - Документация: https://developer.edamam.com/edamam-docs-nutrition-api

#### 2. **Google Cloud Vision API**
   - Бесплатно: 1000 единиц в месяц
   - Регистрация: https://cloud.google.com/vision

#### 3. **Microsoft Azure Computer Vision**
   - Бесплатно: 5000 транзакций в месяц
   - Регистрация: https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/

### API Эндпоинты

#### Edamam API (рекомендуемый)
- `POST /api/vision/recognize-edamam` - Распознавание еды с изображением
- `POST /api/vision/analyze-nutrition` - Анализ нутриентов по текстовому описанию
- `GET /api/vision/food-database` - Поиск продуктов в базе данных
- `GET /api/vision/available-apis-edamam` - Информация о доступных API

#### Google Cloud Vision API
- `POST /api/vision/recognize-google` - Распознавание еды через Google Vision
- `GET /api/vision/available-apis-google` - Информация о Google Vision API

#### Google Cloud Vision API
- `POST /api/vision/recognize-google` - Распознавание еды через Google Vision
- `GET /api/vision/available-apis-google` - Информация о Google Vision API

### Примеры использования

#### Распознавание еды с изображением (Edamam)
```bash
curl -X POST "http://localhost:8000/api/vision/recognize-edamam" \
  -H "Authorization: Bearer ваш_токен" \
  -F "image=@путь/к/изображению.jpg"
```

#### Анализ нутриентов по тексту (Edamam)
```bash
curl -X POST "http://localhost:8000/api/vision/analyze-nutrition" \
  -H "Authorization: Bearer ваш_токен" \
  -H "Content-Type: application/json" \
  -d '{"text": "1 medium apple"}'
```

#### Поиск в базе данных (Edamam)
```bash
curl "http://localhost:8000/api/vision/food-database?query=apple" \
  -H "Authorization: Bearer ваш_токен"
```

#### Распознавание через Google Vision
```bash
curl -X POST "http://localhost:8000/api/vision/recognize-google" \
  -H "Authorization: Bearer ваш_токен" \
  -F "image=@путь/к/изображению.jpg"
```

### Настройка

#### Edamam API
API ключи уже настроены в `.env` файле:
```
EDAMAM_APP_ID=b803dc99
EDAMAM_APP_KEY=50ba16cca84c4a5932779cc7c2a7e2e6
```

#### Google Cloud Vision API
1. Зарегистрируйтесь в Google Cloud Console: https://console.cloud.google.com/
2. Создайте проект и активируйте Cloud Vision API
3. Получите API ключ
4. Установите переменную окружения:
   ```bash
   export GOOGLE_VISION_API_KEY=ваш_ключ_здесь
   ```

Подробная инструкция по настройке API находится в файлах:
- [FOOD_RECOGNITION_SETUP.md](./FOOD_RECOGNITION_SETUP.md) - общая инструкция
- [GOOGLE_VISION_SETUP.md](./GOOGLE_VISION_SETUP.md) - инструкция для Google Cloud Vision

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
  - `vision.py` - Оригинальный vision API
  - `vision_google.py` - Google Cloud Vision API
  - `vision_edamam.py` - Edamam API
- `app/core/` - Конфигурация, база данных, безопасность
- `app/models/` - SQLAlchemy модели
- `app/schemas/` - Pydantic схемы
- `app/services/` - Бизнес-логика
- `tests/` - Тесты

## База данных

По умолчанию используется SQLite. Для продакшена настройте PostgreSQL в `.env`.

## Тестирование

```bash
# Тест Edamam API
python3 test_edamam_nutrition.py

# Тест Google Cloud Vision API
python3 test_google_vision.py

# Тест доступности API
python3 test_api_access.py

# Запуск всех тестов
pytest tests/
```

## Docker

```bash
docker build -t ai-dieta-backend .
docker run -p 8000:8000 ai-dieta-backend
```

## Документация

- [CHANGES_SUMMARY.md](./CHANGES_SUMMARY.md) - Полный обзор изменений
- [QUICK_START.md](./QUICK_START.md) - Быстрый старт
- [FOOD_RECOGNITION_SETUP.md](./FOOD_RECOGNITION_SETUP.md) - Настройка API
- [GOOGLE_VISION_SETUP.md](./GOOGLE_VISION_SETUP.md) - Настройка Google Cloud Vision

## Преимущества решения

✅ **Малый размер Docker образа** (100-200МБ вместо >12ГБ)  
✅ **Высокая точность распознавания** (профессиональные API)  
✅ **Низкие требования к ресурсам** (не нужен GPU)  
✅ **Автоматическое обновление** (API обновляются провайдерами)  
✅ **Бесплатное использование** (достаточно для большинства приложений)  

## Поддержка

Если возникнут вопросы:
1. Проверьте файлы документации в директории backend
2. Запустите тестовые скрипты для диагностики
3. Обратитесь к исходному коду в `app/api/vision*.py`

Готово! 🎉 Теперь у вас есть полностью рабочее приложение AI-Dieta с онлайн распознаванием еды!