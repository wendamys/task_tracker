# ARCHITECTURE.md

# Архитектура проекта

## Общая информация

Task Tracker — веб-приложение для управления внутренними задачами компании.

Проект реализован по принципу разделения ответственности (Separation of Concerns), где каждый слой отвечает только за свою область.

Основной стек:

* Python 3.12
* FastAPI
* SQLAlchemy 2.0
* Pydantic v2
* SQLite

---

# Архитектурная схема

```text
Frontend
    │
    ▼
Routers (API Layer)
    │
    ▼
Services (Business Logic)
    │
    ▼
Models (ORM)
    │
    ▼
SQLite Database
```

---

# Структура проекта

```text
backend/
│
├── app/
│   │
│   ├── database/
│   ├── enums/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
└── requirements.txt
```

---

# Назначение директорий

## app/main.py

Точка входа приложения.

Отвечает за:

* создание FastAPI приложения;
* регистрацию роутеров;
* создание таблиц базы данных;
* запуск API.

---

## database/

Содержит настройки работы с базой данных.

### base.py

Создаёт базовый класс SQLAlchemy Base.

Все ORM-модели наследуются от него.

### db.py

Настройка подключения к SQLite.

Содержит:

* Engine;
* SessionLocal;
* создание таблиц.

### dependencies.py

FastAPI Dependency Injection.

Позволяет получать объект Session через:

```python
db: Session = Depends(get_db)
```

---

## enums/

Содержит перечисления проекта.

### task_status.py

Набор допустимых статусов задач:

```text
new
in_progress
done
cancelled
```

Используется одновременно в:

* ORM моделях;
* Pydantic схемах;
* API.

---

## models/

ORM-модели SQLAlchemy.

### user.py

Модель пользователя.

Поля:

```text
id
name
email
```

---

### task.py

Модель задачи.

Поля:

```text
id
title
description
status
requester
assignee_id
created_at
updated_at
```

Содержит связь:

```python
Task -> User
```

через внешний ключ:

```python
ForeignKey("users.id")
```

---

## schemas/

Pydantic схемы.

Используются для:

* валидации входящих данных;
* сериализации ответов API.

### task.py

Содержит:

* TaskCreate
* TaskUpdate
* TaskResponse
* DeleteResponse

### user.py

Содержит схемы пользователей.

---

## routers/

HTTP слой приложения.

Роутеры содержат только обработку запросов и вызов бизнес-логики.

### task_router.py

CRUD операции над задачами.

### user_router.py

Получение списка пользователей.

---

## services/

Бизнес-логика приложения.

### task_service.py

Содержит операции:

* создание задачи;
* получение задачи;
* обновление задачи;
* удаление задачи;
* проверка существования задачи.

### task_mapper.py

Преобразует ORM объекты в Response схемы.

---

# Принципы проектирования

При разработке использовались следующие подходы:

* Separation of Concerns
* Dependency Injection
* Service Layer Pattern
* Data Validation через Pydantic
* ORM через SQLAlchemy 2.0

Это позволяет упростить поддержку и расширение проекта.
