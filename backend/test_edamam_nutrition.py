#!/usr/bin/env python3
"""
Тест Edamam Nutrition Analysis API.
"""

import os
import httpx
import json

async def test_edamam_nutrition_api():
    """Тестирует Edamam Nutrition Analysis API"""
    
    # Проверка наличия API ключей
    app_id = os.getenv("EDAMAM_APP_ID")
    app_key = os.getenv("EDAMAM_APP_KEY")
    
    if not app_id or not app_key:
        print("❌ Edamam API ключи не найдены!")
        print("Проверьте переменные окружения:")
        print(f"EDAMAM_APP_ID: {app_id}")
        print(f"EDAMAM_APP_KEY: {app_key}")
        return False
    
    print("✓ Edamam API ключи найдены")
    print(f"APP_ID: {app_id}")
    print(f"APP_KEY: {app_key[:10]}...")
    
    print("🌐 Тестируем Edamam Nutrition Analysis API...")
    
    try:
        # Тестируем Nutrition Analysis API
        url = "https://api.edamam.com/api/nutrition-data"
        
        # Тестовые запросы
        test_foods = [
            "1 medium apple",
            "1 banana",
            "100g chicken breast",
            "1 slice pizza"
        ]
        
        for food in test_foods:
            print(f"🧪 Тестируем: {food}")
            
            params = {
                "app_id": app_id,
                "app_key": app_key,
                "ingr": food
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Извлекаем нутриенты
                    calories = data.get("ENERC_KCAL", 0)
                    protein = data.get("PROCNT", 0)
                    fat = data.get("FAT", 0)
                    carbs = data.get("CHOCDF", 0)
                    
                    print(f"  ✅ {food}: {calories} ккал, {protein}г белка, {fat}г жиров, {carbs}г углеводов")
                    
                else:
                    print(f"  ❌ Ошибка для {food}: {response.status_code}")
                    print(f"  📊 Ответ: {response.text[:200]}...")
        
        print("\n🔍 Тестируем Food Database API...")
        
        # Тестируем Food Database API
        url = "https://api.edamam.com/api/food-database/v2/parser"
        
        test_queries = ["apple", "banana", "chicken"]
        
        for query in test_queries:
            print(f"🔎 Поиск: {query}")
            
            params = {
                "app_id": app_id,
                "app_key": app_key,
                "ingr": query
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    foods = data.get("hints", [])
                    
                    print(f"  ✅ Найдено {len(foods)} вариантов")
                    for i, food in enumerate(foods[:3], 1):
                        food_data = food.get("food", {})
                        name = food_data.get("label", "Unknown")
                        category = food_data.get("category", "Unknown")
                        print(f"    {i}. {name} ({category})")
                        
                else:
                    print(f"  ❌ Ошибка для {query}: {response.status_code}")
                    print(f"  📊 Ответ: {response.text[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при запросе к API: {e}")
        return False

def main():
    """Основная функция"""
    
    print("Тест Edamam Nutrition Analysis API")
    print("=" * 50)
    
    import asyncio
    success = asyncio.run(test_edamam_nutrition_api())
    
    print("=" * 50)
    if success:
        print("🎉 Тест пройден! Edamam API готов к использованию.")
        print("\n💡 Доступные эндпоинты:")
        print("1. /api/vision/recognize-edamam - Распознавание еды (с изображением)")
        print("2. /api/vision/analyze-nutrition - Анализ нутриентов (по тексту)")
        print("3. /api/vision/food-database - Поиск в базе данных еды")
    else:
        print("💥 Тест не пройден. Проверьте API ключи и интернет-соединение.")
    
    print("\n📝 Примечание:")
    print("Edamam API предоставляет:")
    print("- Nutrition Analysis API для анализа нутриентов")
    print("- Food Database API для поиска продуктов")
    print("- Recipe Search API для поиска рецептов")

if __name__ == "__main__":
    main()