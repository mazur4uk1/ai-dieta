#!/usr/bin/env python3
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
