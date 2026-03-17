
# Регистрация в Edamam API

## Шаг 1: Регистрация аккаунта
1. Перейдите на https://developer.edamam.com/
2. Нажмите "Sign Up" или "Register"
3. Заполните форму регистрации (email, пароль)
4. Подтвердите email

## Шаг 2: Создание приложения
1. После входа в аккаунт перейдите в раздел "My Applications"
2. Нажмите "Create a new application"
3. Заполните поля:
   - Application Name: AI-Dieta Backend
   - Application Description: Food recognition API for diet tracking app
   - Website URL: http://localhost:8000 (или ваш домен)
4. Нажмите "Create"

## Шаг 3: Получение API ключей
После создания приложения вы увидите:
- **Application ID (APP_ID)**: строка из букв и цифр
- **Application Key (APP_KEY)**: длинная строка с символами

## Шаг 4: Настройка переменных окружения
Скопируйте полученные ключи и выполните команды:

```bash
# Для временной настройки (до перезагрузки терминала)
export EDAMAM_APP_ID=ваш_app_id_здесь
export EDAMAM_APP_KEY=ваш_app_key_здесь

# Для постоянной настройки (добавьте в ~/.bashrc или ~/.zshrc)
echo 'export EDAMAM_APP_ID=ваш_app_id_здесь' >> ~/.bashrc
echo 'export EDAMAM_APP_KEY=ваш_app_key_здесь' >> ~/.bashrc
source ~/.bashrc
```

## Шаг 5: Проверка API
После настройки переменных выполните:
```bash
python3 test_edamam_api.py
```

## Ограничения бесплатного тарифа
- 1000 запросов в месяц
- 1 запрос в секунду
- Доступ к базе данных продуктов и нутриентов

## Альтернативные провайдеры
Если Edamam не подходит, используйте:
1. Google Cloud Vision API: https://cloud.google.com/vision
2. Azure Computer Vision: https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/
3. Clarifai API: https://www.clarifai.com/
