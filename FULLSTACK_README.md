# AI-Dieta Fullstack Docker

Полноценное веб-приложение AI-Dieta, запускаемое одним Docker контейнером.

## 🚀 Быстрый старт

### Требования
- Docker и Docker Compose
- Интернет-соединение (для API Edamam)

### Запуск приложения

1. **Скачайте репозиторий**
   ```bash
   git clone <repository-url>
   cd стол/App
   ```

2. **Запустите сборку и запуск**
   ```bash
   ./build-and-run.sh
   ```

3. **Откройте приложение в браузере**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📋 Что включено

### Backend (FastAPI)
- **Аутентификация**: Email/Password, SMS, Telegram OAuth
- **Питание**: Приёмы пищи, планы питания, шопинг-листы
- **Статистика**: Аналитика потребления
- **AI-распознавание еды**: Edamam API, Google Cloud Vision
- **Подписки**: Тарифные планы

### Frontend (Next.js)
- **Адаптивный интерфейс**
- **Интеграция с backend API**
- **Формы аутентификации**
- **Управление питанием**
- **Статистика и аналитика**

## 🔧 Архитектура

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (Next.js)     │◄──►│   (FastAPI)     │
│   Port: 3000    │    │   Port: 8000    │
└─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Edamam API    │
                       │   (Food AI)     │
                       └─────────────────┘
```

## 📦 Docker образ

### Размеры
- **Backend только**: ~100-200МБ
- **Fullstack**: ~300-500МБ
- **Исходный (с YOLOv8)**: >12ГБ ❌

### Слои
1. **Frontend Builder**: Сборка Next.js приложения
2. **Backend Builder**: Установка Python зависимостей
3. **Final Image**: Финальный образ с обоими сервисами

## ⚙️ Конфигурация

### Переменные окружения
```bash
# Edamam API (уже настроены по умолчанию)
EDAMAM_APP_ID=b803dc99
EDAMAM_APP_KEY=50ba16cca84c4a5932779cc7c2a7e2e6

# База данных
DATABASE_URL=sqlite:///./ai_dieta.db

# Безопасность
SECRET_KEY=your-secret-key-here
DEBUG=false
```

### Порты
- **Frontend**: 3000
- **Backend**: 8000
- **Health Check**: 8000/health

## 🛠️ Разработка

### Локальная разработка (раздельно)
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Локальная разработка (в Docker)
```bash
# Сборка образа
docker build -f Dockerfile.fullstack -t ai-dieta-fullstack .

# Запуск контейнера
docker run -p 8000:8000 -p 3000:3000 ai-dieta-fullstack
```

## 🚨 Возможные проблемы

### 1. Frontend не загружается
**Причина**: Frontend не может подключиться к backend
**Решение**: Проверьте, что backend запущен на порту 8000

### 2. API Edamam не работает
**Причина**: Неправильные API ключи или лимит запросов
**Решение**: Проверьте переменные окружения EDAMAM_APP_ID и EDAMAM_APP_KEY

### 3. Docker build падает
**Причина**: Недостаточно памяти или проблема с зависимостями
**Решение**: 
```bash
# Очистите кэш Docker
docker system prune -a

# Пересоберите с нуля
docker build --no-cache -f Dockerfile.fullstack -t ai-dieta-fullstack .
```

### 4. Приложение медленно запускается
**Причина**: Frontend и backend запускаются последовательно
**Решение**: Это нормально для первого запуска, последующие запуски будут быстрее

## 📊 Мониторинг

### Health Check
```bash
# Проверка состояния backend
curl http://localhost:8000/health

# Проверка состояния frontend
curl http://localhost:3000
```

### Логи
```bash
# Просмотр логов контейнера
docker logs ai-dieta-app

# Просмотр логов в реальном времени
docker logs -f ai-dieta-app
```

## 🔄 Обновление

### Обновление кода
1. Внесите изменения в исходный код
2. Пересоберите образ: `./build-and-run.sh`
3. Контейнер перезапустится с новыми изменениями

### Обновление зависимостей
1. Обновите `requirements.txt` (backend) или `package.json` (frontend)
2. Пересоберите образ: `./build-and-run.sh`

## 🚀 Production

### Рекомендации
1. **Используйте production базу данных** (PostgreSQL вместо SQLite)
2. **Настройте HTTPS** с помощью reverse proxy (nginx, traefik)
3. **Настройте мониторинг** и логирование
4. **Используйте secrets** для хранения API ключей

### Environment для production
```bash
# Production база данных
DATABASE_URL=postgresql://user:password@db:5432/ai_dieta

# Production секреты
SECRET_KEY=your-production-secret-key
DEBUG=false

# Production API ключи
EDAMAM_APP_ID=your-production-app-id
EDAMAM_APP_KEY=your-production-app-key
```

## 📞 Поддержка

Если возникнут проблемы:
1. Проверьте логи: `docker logs ai-dieta-app`
2. Проверьте состояние сервисов: `docker ps`
3. Перезапустите контейнер: `docker restart ai-dieta-app`
4. Обратитесь к документации в папке `backend/`

## 🎉 Готово!

Теперь у вас есть полностью рабочее fullstack приложение AI-Dieta, которое можно запустить на любом компьютере с Docker!