#!/usr/bin/env python3
"""
Скрипт для настройки Edamam API.
Этот скрипт поможет вам зарегистрироваться и настроить API ключи.
"""

import os
import json
from pathlib import Path

def create_edamam_registration_guide():
    """Создает руководство по регистрации в Edamam API"""
    
    guide_content = """
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
"""
    
    with open("EDAMAM_REGISTRATION_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✓ Руководство по регистрации создано: EDAMAM_REGISTRATION_GUIDE.md")

def create_env_template():
    """Создает шаблон .env файла"""
    
    env_template = """
# AI-Dieta Backend Environment Variables

# Database Configuration
DATABASE_URL=sqlite:///./ai_dieta.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Food Recognition API (Edamam)
# Получите ключи на https://developer.edamam.com/
EDAMAM_APP_ID=your_edamam_app_id_here
EDAMAM_APP_KEY=your_edamam_app_key_here

# Alternative APIs (optional)
# GOOGLE_VISION_API_KEY=your_google_api_key_here
# AZURE_CV_ENDPOINT=your_azure_endpoint_here
# AZURE_CV_KEY=your_azure_key_here
# CLARIFAI_API_KEY=your_clarifai_key_here

# Application Settings
DEBUG=true
"""
    
    with open(".env.template", "w", encoding="utf-8") as f:
        f.write(env_template.strip())
    
    print("✓ Шаблон .env файла создан: .env.template")

def create_test_script():
    """Создает скрипт для тестирования Edamam API"""
    
    test_script = '''#!/usr/bin/env python3
"""
Тестовый скрипт для проверки Edamam API.
"""

import os
import httpx
import base64
from io import BytesIO
from PIL import Image

def test_edamam_api():
    """Тестирует Edamam API с реальным изображением"""
    
    # Проверка наличия API ключей
    app_id = os.getenv("EDAMAM_APP_ID")
    app_key = os.getenv("EDAMAM_APP_KEY")
    
    if not app_id or not app_key:
        print("❌ API ключи не найдены!")
        print("Пожалуйста, установите переменные окружения:")
        print("export EDAMAM_APP_ID=ваш_app_id")
        print("export EDAMAM_APP_KEY=ваш_app_key")
        return False
    
    print("✓ API ключи найдены")
    
    # Создаем тестовое изображение (в реальности используйте реальное фото еды)
    print("📸 Создаем тестовое изображение...")
    img = Image.new('RGB', (200, 200), color='red')
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    image_bytes = buffer.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Тестируем API
    print("🌐 Тестируем Edamam API...")
    
    try:
        url = "https://api.edamam.com/api/food-detection-parser"
        
        response = httpx.post(
            url,
            params={
                "app_id": app_id,
                "app_key": app_key
            },
            data={
                "image": image_base64
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API работает!")
            print(f"Статус: {response.status_code}")
            
            # Проверяем ответ
            if "parsed" in data and data["parsed"]:
                print(f"Найдено продуктов: {len(data['parsed'])}")
                for item in data["parsed"][:3]:  # Показываем первые 3
                    food = item.get("food", {})
                    label = food.get("label", "Unknown")
                    nutrients = food.get("nutrients", {})
                    calories = nutrients.get("ENERC_KCAL", 0)
                    print(f"  - {label}: {calories} ккал")
            else:
                print("⚠️ API работает, но не распознал продукты на тестовом изображении")
                print("   Это нормально для сгенерированного изображения")
                print("   Попробуйте с реальным фото еды")
            
            return True
            
        else:
            print(f"❌ API вернул ошибку: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при запросе к API: {e}")
        return False

if __name__ == "__main__":
    print("Тестирование Edamam API")
    print("=" * 40)
    success = test_edamam_api()
    print("=" * 40)
    if success:
        print("🎉 Тест пройден! API готов к использованию.")
    else:
        print("💥 Тест не пройден. Проверьте API ключи и интернет-соединение.")
'''
    
    with open("test_edamam_api.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    # Делаем скрипт исполняемым
    os.chmod("test_edamam_api.py", 0o755)
    
    print("✓ Тестовый скрипт создан: test_edamam_api.py")

def main():
    """Основная функция настройки"""
    
    print("Настройка Edamam API для AI-Dieta")
    print("=" * 40)
    
    # Создаем необходимые файлы
    create_edamam_registration_guide()
    create_env_template()
    create_test_script()
    
    print("\n" + "=" * 40)
    print("Готово! Теперь выполните следующие шаги:")
    print()
    print("1. Прочитайте руководство: EDAMAM_REGISTRATION_GUIDE.md")
    print("2. Зарегистрируйтесь на https://developer.edamam.com/")
    print("3. Получите API ключи")
    print("4. Настройте переменные окружения:")
    print("   export EDAMAM_APP_ID=ваш_app_id")
    print("   export EDAMAM_APP_KEY=ваш_app_key")
    print("5. Протестируйте API:")
    print("   python3 test_edamam_api.py")
    print()
    print("💡 Совет: Для постоянной настройки добавьте export команды в ~/.bashrc")

if __name__ == "__main__":
    main()
