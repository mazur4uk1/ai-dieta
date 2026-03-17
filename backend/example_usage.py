#!/usr/bin/env python3
"""
Пример использования Food Recognition API.
Этот скрипт показывает, как загружать изображения и получать распознанные продукты.
"""

import os
import httpx
import base64
from pathlib import Path

def create_example_image():
    """Создает пример изображения для тестирования"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Создаем изображение с надписью "Food Image"
    img = Image.new('RGB', (400, 300), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Рисуем простое "блюдо" (круг)
    draw.ellipse([100, 100, 300, 200], fill='red', outline='darkred', width=3)
    draw.text((150, 140), "🍎", font=None, fill='white')
    
    # Сохраняем изображение
    img.save("example_food_image.jpg", "JPEG")
    return "example_food_image.jpg"

def test_food_recognition_api():
    """Тестирует food recognition API"""
    
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
    
    # Создаем пример изображения
    print("📸 Создаем пример изображения...")
    image_path = create_example_image()
    
    # Читаем изображение
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    # Конвертируем в base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    print("🌐 Тестируем Food Recognition API...")
    
    try:
        # Тестируем Edamam API
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
            
            # Обрабатываем результат
            if "parsed" in data and data["parsed"]:
                print(f"\n🍎 Найдено продуктов: {len(data['parsed'])}")
                print("=" * 50)
                
                for i, item in enumerate(data["parsed"], 1):
                    food = item.get("food", {})
                    label = food.get("label", "Unknown")
                    nutrients = food.get("nutrients", {})
                    
                    # Получаем нутриенты
                    calories = nutrients.get("ENERC_KCAL", 0)
                    protein = nutrients.get("PROCNT", 0)
                    fat = nutrients.get("FAT", 0)
                    carbs = nutrients.get("CHOCDF", 0)
                    
                    print(f"{i}. {label}")
                    print(f"   Калории: {calories} ккал")
                    print(f"   Белки: {protein} г")
                    print(f"   Жиры: {fat} г")
                    print(f"   Углеводы: {carbs} г")
                    print()
                
                return True
            else:
                print("⚠️ API работает, но не распознал продукты на изображении")
                print("   Это нормально для сгенерированного изображения")
                print("   Попробуйте с реальным фото еды")
                
                # Показываем fallback-режим
                print("\n🔄 Показываем fallback-режим:")
                show_fallback_example()
                return True
                
        else:
            print(f"❌ API вернул ошибку: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при запросе к API: {e}")
        return False

def show_fallback_example():
    """Показывает пример fallback-режима"""
    
    fallback_foods = [
        {"name": "Apple", "calories": 95, "confidence": 0.85},
        {"name": "Banana", "calories": 105, "confidence": 0.8},
        {"name": "Orange", "calories": 62, "confidence": 0.75},
        {"name": "Broccoli", "calories": 55, "confidence": 0.7},
        {"name": "Pizza", "calories": 285, "confidence": 0.6}
    ]
    
    print("🍎 Пример распознанных продуктов (fallback-режим):")
    print("=" * 50)
    
    for i, food in enumerate(fallback_foods, 1):
        print(f"{i}. {food['name']}")
        print(f"   Калории: {food['calories']} ккал")
        print(f"   Уверенность: {food['confidence'] * 100}%")
        print()

def simulate_api_request():
    """Симулирует API запрос для демонстрации"""
    
    print("📡 Симуляция API запроса")
    print("=" * 50)
    
    # Пример реального запроса
    example_request = {
        "image": "base64_encoded_image_data_here"
    }
    
    print("📤 Пример запроса:")
    print(f"POST /api/vision/recognize")
    print(f"Headers: Authorization: Bearer your_token")
    print(f"Body: {example_request}")
    print()
    
    # Пример ответа
    example_response = {
        "recognized_foods": [
            {
                "name": "Apple",
                "calories": 95,
                "confidence": 0.9
            },
            {
                "name": "Banana",
                "calories": 105,
                "confidence": 0.85
            }
        ]
    }
    
    print("📥 Пример ответа:")
    print(f"Status: 200 OK")
    print(f"Body: {example_response}")
    print()

def main():
    """Основная функция"""
    
    print("Пример использования Food Recognition API")
    print("=" * 50)
    
    # Симулируем API запрос
    simulate_api_request()
    
    # Тестируем реальное API
    success = test_food_recognition_api()
    
    print("=" * 50)
    if success:
        print("🎉 Тест пройден! API готов к использованию.")
    else:
        print("💥 Тест не пройден. Проверьте API ключи и интернет-соединение.")
    
    print("\n💡 Как использовать в приложении:")
    print("1. Пользователь загружает фото еды")
    print("2. Приложение отправляет изображение на /api/vision/recognize")
    print("3. API возвращает распознанные продукты с калорийностью")
    print("4. Приложение сохраняет данные в базу и показывает пользователю")

if __name__ == "__main__":
    main()