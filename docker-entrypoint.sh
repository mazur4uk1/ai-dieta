#!/bin/bash
set -e

echo "🚀 Запуск AI-Dieta Fullstack приложения..."

# Функция для проверки готовности сервиса
wait_for_service() {
    local service_name=$1
    local url=$2
    local max_attempts=60
    local attempt=1
    
    echo "⏳ Ожидание готовности $service_name..."
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s $url > /dev/null 2>&1; then
            echo "✅ $service_name готов!"
            return 0
        fi
        echo "⏳ Попытка $attempt/$max_attempts..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name не ответил за отведенное время"
    return 1
}

# Запускаем backend в фоне
echo "🐍 Запуск FastAPI backend..."
cd /app/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Ждем готовности backend
if ! wait_for_service "Backend" "http://localhost:8000/docs"; then
    echo "❌ Backend не запустился"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Запускаем frontend в фоне
echo "🌐 Запуск Next.js frontend..."
cd /app/frontend
npm run dev &
FRONTEND_PID=$!

# Ждем готовности frontend
if ! wait_for_service "Frontend" "http://localhost:3000"; then
    echo "❌ Frontend не запустился"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 1
fi

echo "🎉 AI-Dieta Fullstack приложение запущено!"
echo "📱 Backend: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo "📚 API Documentation: http://localhost:8000/docs"

# Функция для graceful shutdown
cleanup() {
    echo "🛑 Остановка сервисов..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    echo "✅ Все сервисы остановлены"
    exit 0
}

# Ловим сигналы для graceful shutdown
trap cleanup SIGTERM SIGINT

# Ждем, пока один из процессов не завершится
wait $BACKEND_PID $FRONTEND_PID