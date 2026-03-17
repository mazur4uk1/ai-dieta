#!/usr/bin/env python3
"""
Тест доступности Edamam API и проверка ключей.
"""

import os
import urllib.request
import urllib.parse

def test_api_access():
    """Тестирует доступность API и правильность ключей"""
    
    app_id = os.getenv("EDAMAM_APP_ID")
    app_key = os.getenv("EDAMAM_APP_KEY")
    
    if not app_id or not app_key:
        print("❌ API ключи не найдены!")
        return False
    
    print("✓ API ключи найдены")
    print(f"APP_ID: {app_id}")
    print(f"APP_KEY: {app_key[:10]}...")
    
    # Проверим доступность API через простой GET запрос
    print("🌐 Проверяем доступность API...")
    
    try:
        # Попробуем разные возможные URL
        test_urls = [
            "https://api.edamam.com/api/food-detection/v1",
            "https://api.edamam.com/api/food-detection/v2", 
            "https://api.edamam.com/api/food-detection-parser",
            "https://api.edamam.com/api/food-detection",
            "https://api.edamam.com/api/nutrition-details"
        ]
        
        for url in test_urls:
            print(f"Проверяем URL: {url}")
            
            try:
                # Простой GET запрос для проверки доступности
                params = {
                    'app_id': app_id,
                    'app_key': app_key,
                    'ingr': '1 apple'  # Простой тестовый ингредиент
                }
                
                query_string = urllib.parse.urlencode(params)
                full_url = f"{url}?{query_string}"
                
                req = urllib.request.Request(full_url, method='GET')
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    status = response.getcode()
                    print(f"  ✅ URL доступен: {status}")
                    
                    # Если URL доступен, попробуем POST запрос с изображением
                    if status == 200:
                        print(f"  📸 Тестируем POST запрос с изображением...")
                        test_image_post(url, app_id, app_key)
                        return True
                        
            except Exception as e:
                print(f"  ❌ URL недоступен: {e}")
        
        print("❌ Ни один из URL не работает")
        return False
        
    except Exception as e:
        print(f"❌ Ошибка при проверке API: {e}")
        return False

def test_image_post(url, app_id, app_key):
    """Тестирует POST запрос с изображением"""
    
    try:
        # Создаем простое изображение
        from PIL import Image
        import io
        import base64
        
        img = Image.new('RGB', (100, 100), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Формируем POST запрос
        data = {
            'image': image_base64
        }
        
        data_bytes = urllib.parse.urlencode(data).encode('utf-8')
        
        req = urllib.request.Request(url, data=data_bytes, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        req.add_header('app_id', app_id)
        req.add_header('app_key', app_key)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            status = response.getcode()
            response_data = response.read().decode('utf-8')
            
            if status == 200:
                print(f"  ✅ POST запрос успешен: {status}")
                print(f"  📊 Ответ: {response_data[:200]}...")
                return True
            else:
                print(f"  ❌ POST запрос неудачен: {status}")
                print(f"  📊 Ответ: {response_data[:200]}...")
                return False
                
    except Exception as e:
        print(f"  ❌ Ошибка POST запроса: {e}")
        return False

def main():
    """Основная функция"""
    
    print("Тест доступности Edamam API")
    print("=" * 40)
    
    success = test_api_access()
    
    print("=" * 40)
    if success:
        print("🎉 API доступен и работает!")
    else:
        print("💥 API недоступен или ключи не работают.")
        print("\n💡 Возможные причины:")
        print("1. Неправильный URL API")
        print("2. API ключи не активированы")
        print("3. Приложение не настроено для Food Detection API")
        print("4. Ограничения по IP или региону")
        print("\n🔍 Рекомендации:")
        print("1. Проверьте документацию Edamam API")
        print("2. Убедитесь, что приложение настроено для Food Detection")
        print("3. Попробуйте другие API провайдеры (Google Cloud Vision, Azure)")

if __name__ == "__main__":
    main()