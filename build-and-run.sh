#!/bin/bash
set -e

echo "🚀 Сборка и запуск AI-Dieta Fullstack приложения..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Имя образа
IMAGE_NAME="ai-dieta-fullstack"
CONTAINER_NAME="ai-dieta-app"

# Останавливаем и удаляем существующий контейнер, если он есть
echo "🛑 Остановка существующего контейнера..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Собираем Docker образ
echo "🔨 Сборка Docker образа..."
sudo docker build -f Dockerfile.fullstack -t $IMAGE_NAME .

# Запускаем контейнер
echo "🚀 Запуск контейнера..."
docker run -d \
    --name $CONTAINER_NAME \
    -p 8000:8000 \
    -p 3000:3000 \
    -e EDAMAM_APP_ID=${EDAMAM_APP_ID:-b803dc99} \
    -e EDAMAM_APP_KEY=${EDAMAM_APP_KEY:-50ba16cca84c4a5932779cc7c2a7e2e6} \
    -e DATABASE_URL=${DATABASE_URL:-sqlite:///./ai_dieta.db} \
    -e SECRET_KEY=${SECRET_KEY:-your-secret-key-here} \
    -e DEBUG=${DEBUG:-false} \
    $IMAGE_NAME

# Ждем запуска контейнера
echo "⏳ Ожидание запуска приложения..."
sleep 10

# Проверяем статус контейнера
if docker ps | grep -q $CONTAINER_NAME; then
    echo "✅ Приложение успешно запущено!"
    echo ""
    echo "📱 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🌐 Frontend: http://localhost:3000"
    echo ""
    echo "💡 Для просмотра логов выполните: docker logs $CONTAINER_NAME"
    echo "💡 Для остановки выполните: docker stop $CONTAINER_NAME"
else
    echo "❌ Контейнер не запустился. Проверьте логи:"
    docker logs $CONTAINER_NAME
    exit 1
fi