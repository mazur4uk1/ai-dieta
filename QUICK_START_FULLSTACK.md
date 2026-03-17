# Быстрый старт: AI-Dieta Fullstack

Простой способ запустить приложение на любом компьютере.

## 🚀 Вариант 1: Backend в Docker + Frontend локально (рекомендуется)

### 1. Запустите Backend в Docker
```bash
cd стол/App/backend
sudo docker run -p 8000:8000 \
  -e EDAMAM_APP_ID=b803dc99 \
  -e EDAMAM_APP_KEY=50ba16cca84c4a5932779cc7c2a7e2e6 \
  ai-dieta-backend
```

### 2. Запустите Frontend локально
```bash
cd стол/App/frontend
npm install
npm run dev
```

### 3. Откройте приложение
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🐳 Вариант 2: Только Backend в Docker

Если не нужен frontend:

```bash
cd стол/App/backend
sudo docker run -p 8000:8000 \
  -e EDAMAM_APP_ID=b803dc99 \
  -e EDAMAM_APP_KEY=50ba16cca84c4a5932779cc7c2a7e2e6 \
  ai-dieta-backend
```

API будет доступно по адресу: http://localhost:8000

## 📱 Вариант 3: Mobile App (если есть)

Если у вас есть React Native приложение:

1. Запустите backend как в варианте 1
2. В настройках мобильного приложения укажите URL: `http://localhost:8000`
3. Запустите мобильное приложение

## 🔧 Проверка работы

### Проверьте Backend
```bash
curl http://localhost:8000/api/vision/available-apis-edamam
```

### Проверьте Frontend
Откройте в браузере: http://localhost:3000

### Пример API запроса
```bash
# Анализ нутриентов
curl -X POST "http://localhost:8000/api/vision/analyze-nutrition" \
  -H "Content-Type: application/json" \
  -d '{"text": "1 medium apple"}'
```

## 🚨 Возможные проблемы

### 1. Docker не запускается
**Решение**: Убедитесь, что Docker установлен и запущен

### 2. Frontend не может подключиться к backend
**Проверка**: 
```bash
curl http://localhost:8000/health
```
**Решение**: Убедитесь, что backend запущен на порту 8000

### 3. npm install падает
**Решение**: 
```bash
cd стол/App/frontend
rm -rf node_modules package-lock.json
npm install
```

### 4. API Edamam не работает
**Проверка**: 
```bash
curl "http://localhost:8000/api/vision/food-database?query=apple"
```
**Решение**: Проверьте API ключи в переменных окружения

## 💡 Советы

1. **Backend работает стабильно** - он уже протестирован и работает
2. **Frontend может требовать доработки** - это нормально для frontend части
3. **API полностью функционально** - все эндпоинты работают
4. **Edamam API ключи активны** - можно сразу тестировать распознавание еды

## 🎉 Готово!

Теперь у вас есть работающее приложение AI-Dieta! Backend в Docker, frontend локально - это надежная и простая конфигурация для запуска на любом компьютере.