#!/usr/bin/env python3
"""
Тест Google Cloud Vision API.
"""

import os
import httpx
import base64
import json
from io import BytesIO
from PIL import Image

async def test_google_vision_api():
    """Тестирует Google Cloud Vision API"""
    
    # Проверка наличия API ключей
    api_key = os.getenv("GOOGLE_VISION_API_KEY")
    
    if not api_key:
        print("❌ Google Cloud Vision API ключ не найден!")
        print("Пожалуйста, установите переменную окружения:")
        print("export GOOGLE_VISION_API_KEY=ваш_ключ_здесь")
        return False
    
    print("✓ Google Cloud Vision API ключ найден")
    print(f"API Key: {api_key[:10]}...")
    
    # Создаем тестовое изображение
    print("📸 Создаем тестовое изображение...")
    
    # Создаем изображение с надписью "Food"
    img = Image.new('RGB', (400, 300), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Рисуем простое "яблоко"
    draw.ellipse([100, 100, 300, 200], fill='red', outline='darkred', width=3)
    draw.text((150, 140), "🍎", font=None, fill='white')
    draw.text((180, 220), "Food Image", font=None, fill='black')
    
    # Сохраняем изображение в буфер
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    image_bytes = buffer.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    print("🌐 Тестируем Google Cloud Vision API...")
    
    try:
        # Формируем запрос к Google Cloud Vision API
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        
        # Google Cloud Vision request body
        request_body = {
            "requests": [
                {
                    "image": {
                        "content": image_base64
                    },
                    "features": [
                        {
                            "type": "LABEL_DETECTION",
                            "maxResults": 10
                        },
                        {
                            "type": "WEB_DETECTION",
                            "maxResults": 10
                        }
                    ]
                }
            ]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=request_body,
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Google Cloud Vision API работает!")
                print(f"Статус: {response.status_code}")
                
                # Парсим ответ
                responses = data.get("responses", [])
                if responses:
                    response_data = responses[0]
                    
                    # Получаем метки
                    labels = response_data.get("labelAnnotations", [])
                    web_detection = response_data.get("webDetection", {})
                    web_entities = web_detection.get("webEntities", [])
                    
                    print(f"\n🏷️ Найдено меток: {len(labels)}")
                    print(f"🌐 Найдено веб-сущностей: {len(web_entities)}")
                    
                    # Показываем метки
                    if labels:
                        print("\n📋 Топ-5 меток:")
                        for i, label in enumerate(labels[:5], 1):
                            description = label.get("description", "Unknown")
                            score = label.get("score", 0)
                            print(f"  {i}. {description} (уверенность: {score:.2f})")
                    
                    # Показываем веб-сущности
                    if web_entities:
                        print("\n🌐 Топ-5 веб-сущностей:")
                        for i, entity in enumerate(web_entities[:5], 1):
                            description = entity.get("description", "Unknown")
                            score = entity.get("score", 0)
                            print(f"  {i}. {description} (уверенность: {score:.2f})")
                    
                    # Проверяем, есть ли еда среди распознанного
                    food_items = []
                    for label in labels:
                        description = label.get("description", "").lower()
                        score = label.get("score", 0)
                        if is_food_item(description):
                            food_items.append({
                                "name": description.title(),
                                "confidence": score
                            })
                    
                    for entity in web_entities:
                        description = entity.get("description", "").lower()
                        score = entity.get("score", 0)
                        if is_food_item(description):
                            food_items.append({
                                "name": description.title(),
                                "confidence": score
                            })
                    
                    if food_items:
                        print(f"\n🍎 Найдено продуктов: {len(food_items)}")
                        for i, food in enumerate(food_items[:5], 1):
                            print(f"  {i}. {food['name']} (уверенность: {food['confidence']:.2f})")
                    else:
                        print("\n⚠️ Еда не распознана на тестовом изображении")
                        print("   Это нормально для сгенерированного изображения")
                        print("   Попробуйте с реальным фото еды")
                    
                    return True
                else:
                    print("⚠️ API вернул пустой ответ")
                    return True
            else:
                print(f"❌ API вернул ошибку: {response.status_code}")
                print(f"Текст ошибки: {response.text[:500]}")
                return False
                
    except Exception as e:
        print(f"❌ Ошибка при запросе к API: {e}")
        return False

def is_food_item(description: str) -> bool:
    """Check if description is likely a food item"""
    food_keywords = [
        "apple", "banana", "orange", "broccoli", "carrot", "potato", "tomato",
        "pizza", "burger", "sandwich", "salad", "pasta", "rice", "bread", "cheese",
        "chicken", "fish", "egg", "milk", "cake", "pie", "cookie", "donut", "candy",
        "fruit", "vegetable", "food", "meal", "dish"
    ]
    
    return any(keyword in description for keyword in food_keywords)

def main():
    """Основная функция"""
    
    print("Тест Google Cloud Vision API")
    print("=" * 40)
    
    import asyncio
    success = asyncio.run(test_google_vision_api())
    
    print("=" * 40)
    if success:
        print("🎉 Тест пройден! Google Cloud Vision API готов к использованию.")
    else:
        print("💥 Тест не пройден. Проверьте API ключ и интернет-соединение.")
    
    print("\n💡 Как использовать:")
    print("1. Зарегистрируйтесь в Google Cloud Console")
    print("2. Создайте проект и активируйте Vision API")
    print("3. Получите API ключ")
    print("4. Установите переменную окружения GOOGLE_VISION_API_KEY")
    print("5. Используйте эндпоинт /api/vision/recognize-google")

if __name__ == "__main__":
    main()