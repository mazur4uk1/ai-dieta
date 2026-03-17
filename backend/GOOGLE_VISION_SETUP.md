# Настройка Google Cloud Vision API

Google Cloud Vision API - это надежный и мощный сервис для распознавания изображений, включая еду.

## Преимущества Google Cloud Vision API

✅ **Высокая точность распознавания**  
✅ **1000 бесплатных запросов в месяц**  
✅ **Поддержка множества типов анализа**  
✅ **Надежная инфраструктура Google**  
✅ **Простая настройка**  

## Шаг 1: Регистрация в Google Cloud

1. **Перейдите на Google Cloud Console**
   - https://console.cloud.google.com/
   - Войдите с вашим Google аккаунтом

2. **Создайте новый проект**
   - Нажмите "Select a project" в верхней панели
   - Нажмите "New Project"
   - Введите имя проекта (например, "AI-Dieta Vision")
   - Нажмите "Create"

## Шаг 2: Активация Vision API

1. **Перейдите в библиотеку API**
   - В меню слева выберите "APIs & Services" → "Library"
   - Найдите "Cloud Vision API"
   - Нажмите "Cloud Vision API"
   - Нажмите "Enable"

2. **Создайте учетные данные**
   - В меню слева выберите "APIs & Services" → "Credentials"
   - Нажмите "Create Credentials" → "API key"
   - Скопируйте созданный API ключ

## Шаг 3: Настройка переменных окружения

```bash
# Установите переменную окружения (временно)
export GOOGLE_VISION_API_KEY=ваш_ключ_здесь

# Для постоянной настройки добавьте в ~/.bashrc
echo 'export GOOGLE_VISION_API_KEY=ваш_ключ_здесь' >> ~/.bashrc
source ~/.bashrc
```

## Шаг 4: Тестирование API

```bash
# Перейдите в директорию backend
cd /home/user/Рабочий стол/App/стол/App/backend

# Запустите тест Google Vision API
python3 test_google_vision.py
```

## Ограничения бесплатного тарифа

- **1000 запросов в месяц** бесплатно
- **10 запросов в секунду** (лимит скорости)
- **Поддержка изображений до 4MB**
- **Поддержка JPEG, PNG, GIF, BMP, WebP, RAW, ICO форматов**

## Типы анализа, поддерживаемые API

1. **LABEL_DETECTION** - Обнаружение меток и описаний
2. **WEB_DETECTION** - Поиск веб-ссылок и схожих изображений
3. **TEXT_DETECTION** - Обнаружение текста на изображениях
4. **FACE_DETECTION** - Обнаружение лиц
5. **LANDMARK_DETECTION** - Обнаружение достопримечательностей
6. **LOGO_DETECTION** - Обнаружение логотипов

## Пример использования

```python
# Загрузка изображения
curl -X POST "http://localhost:8000/api/vision/recognize-google" \
  -H "Authorization: Bearer ваш_токен" \
  -F "image=@путь/к/изображению.jpg"
```

## Пример ответа

```json
{
  "recognized_foods": [
    {
      "name": "Apple",
      "calories": 95,
      "confidence": 0.95
    },
    {
      "name": "Fruit",
      "calories": 50,
      "confidence": 0.85
    }
  ],
  "source": "Google Cloud Vision"
}
```

## Альтернативные API

Если Google Cloud Vision не подходит, используйте:

### 1. Microsoft Azure Computer Vision
- **5000 транзакций/месяц бесплатно**
- Регистрация: https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/

### 2. Clarifai API
- **5000 предсказаний/месяц бесплатно**
- Регистрация: https://www.clarifai.com/

## Troubleshooting

### API ключ не работает
```bash
# Проверьте, что переменная установлена
echo $GOOGLE_VISION_API_KEY

# Проверьте ограничения в Google Cloud Console
# Убедитесь, что API активирован для вашего проекта
```

### Ошибка квоты
- Проверьте использование квот в Google Cloud Console
- При необходимости запросите увеличение квоты

### Ошибка формата изображения
- Убедитесь, что изображение в поддерживаемом формате
- Проверьте размер изображения (не более 4MB)

## Стоимость после бесплатного лимита

- **LABEL_DETECTION**: $1.50 за 1000 запросов
- **WEB_DETECTION**: $1.50 за 1000 запросов
- **TEXT_DETECTION**: $1.50 за 1000 запросов

Для большинства приложений бесплатного лимита более чем достаточно!

## Интеграция с приложением

Приложение автоматически:
1. Попробует Google Cloud Vision API (если ключ настроен)
2. Переключится на fallback-режим при ошибках
3. Вернет распознанные продукты с калорийностью

Готово! 🎉 Теперь у вас есть надежное решение для распознавания еды!