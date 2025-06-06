## Сервис покупки товаров для авторизованных пользователей.

Микросервис для управления пользователями, товарами и корзиной покупок

### 🛠 Технологический стек
Backend: FastAPI

База данных: PostgreSQL

Миграции: Alembic

Аутентификация: FastapiUsers, JWT

Документация: Swagger/ReDoc

### 🚀 Быстрый старт

### Установка
1. Клонировать репозиторий:
```
mkdir some_name
cd some_name
git clone git@github.com:sofxcknboring/auth-store-api.git .
```
2. Настроить окружение:
```
cp .env.example .env
```
3. Запуск.

На этапе сборки:
- создает суперюзера по переменным из .env
```
docker-compose up --build -d
```

### 📚 Документация API
После запуска доступно:

Swagger UI: http://0.0.0.0:8000/docs

ReDoc: http://0.0.0.0:8000/redoc


### 🗂 Структура проекта
```
├── migrations/           # Миграции Alembic
├── src/
│   ├── commands/         # Скрипты
│   │   └── csu.py        # Создание суперпользователя
│   ├── core/             # Ядро приложения
│   │   ├── auth/         # Логика авторизации
│   │   ├── config.py     # Конфигурация
│   │   └── database.py   # Работа с БД
│   ├── models/           # SQLAlchemy модели
│   ├── routers/          # Эндпоинты API
│   │   └── dependencies/ # Зависимости
│   ├── schemas/          # Pydantic схемы
│   └── services/         # Бизнес-логика
└── docker-compose.yml    # Конфигурация Docker
```

### 🔒 Особенности реализации
- Валидация пароля:
  - Минимум 8 символов
  - Обязательно: 1 заглавная буква и 1 спецсимвол ($%&!:)
- Валидация телефона: формат +7XXXXXXXXXX
- JWT аутентификация
- Автоматическое создание корзины при регистрации

### 🐳 Управление Docker
- Запустить: ```docker-compose up -d```
- Остановить: ```docker-compose down -v```
- Просмотреть логи: ```docker-compose logs -f app```
- Пересоздать базу: ```docker-compose down -v && docker-compose up -d```



