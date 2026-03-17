#!/usr/bin/env python3
"""
Простой тест без внешних зависимостей для проверки Edamam API.
"""

import os
import base64
import urllib.request
import urllib.parse
import json

def test_edamam_api_simple():
    """Простой тест Edamam API без httpx"""
    
    # Проверка наличия API ключей
    app_id = os.getenv("EDAMAM_APP_ID")
    app_key = os.getenv("EDAMAM_APP_KEY")
    
    if not app_id or not app_key:
        print("❌ API ключи не найдены!")
        print("Проверьте переменные окружения:")
        print(f"EDAMAM_APP_ID: {app_id}")
        print(f"EDAMAM_APP_KEY: {app_key}")
        return False
    
    print("✓ API ключи найдены")
    print(f"APP_ID: {app_id}")
    print(f"APP_KEY: {app_key[:10]}...")
    
    # Создаем простое тестовое изображение
    print("📸 Создаем тестовое изображение...")
    
    # Создаем простое изображение (красный квадрат)
    from PIL import Image
    import io
    
    img = Image.new('RGB', (200, 200), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    image_bytes = buffer.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    print("🌐 Тестируем Edamam API...")
    
    try:
        # Формируем URL
        url = "https://api.edamam.com/api/food-detection/v2"
        
        # Формируем параметры
        params = {
            'app_id': app_id,
            'app_key': app_key
        }
        
        # Формируем данные
        data = {
            'image': image_base64
        }
        
        # Кодируем параметры
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        # Кодируем данные
        data_bytes = urllib.parse.urlencode(data).encode('utf-8')
        
        # Создаем запрос
        req = urllib.request.Request(full_url, data=data_bytes, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        # Отправляем запрос
        with urllib.request.urlopen(req, timeout=30) as response:
            status_code = response.getcode()
            response_data = response.read().decode('utf-8')
            
            if status_code == 200:
                try:
                    json_data = json.loads(response_data)
                    print("✅ API работает!")
                    print(f"Статус: {status_code}")
                    
                    # Проверяем ответ
                    if "parsed" in json_data and json_data["parsed"]:
                        print(f"Найдено продуктов: {len(json_data['parsed'])}")
                        for item in json_data["parsed"][:3]:  # Показываем первые 3
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
                    
                except json.JSONDecodeError:
                    print(f"❌ Ошибка парсинга JSON: {response_data[:200]}...")
                    return False
            else:
                print(f"❌ API вернул ошибку: {status_code}")
                print(f"Текст ошибки: {response_data[:500]}")
                return False
                
    except Exception as e:
        print(f"❌ Ошибка при запросе к API: {e}")
        return False

def main():
    """Основная функция"""
    
    print("Простой тест Edamam API (без внешних зависимостей)")
    print("=" * 60)
    
    success = test_edamam_api_simple()
    
    print("=" * 60)
    if success:
        print("🎉 Тест пройден! API готов к использованию.")
    else:
        print("💥 Тест не пройден. Проверьте API ключи и интернет-соединение.")

if __name__ == "__main__":
    main()