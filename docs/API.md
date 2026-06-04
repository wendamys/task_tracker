# API.md

# API Documentation

Базовый адрес API:

```text
http://127.0.0.1:8000
```

Полная интерактивная документация доступна по адресу:

```text
http://127.0.0.1:8000/docs
```

---

# Users

## Получить список пользователей

### Запрос

```http
GET /users
```

### Ответ

```json
[
  {
    "id": 1,
    "name": "Alex",
    "email": "alex@example.ru"
  }
]
```

---

# Tasks

## Создание задачи

### Запрос

```http
POST /tasks
```

### Тело запроса

```json
{
  "title": "Fix bug",
  "description": "Login page issue",
  "requester": "Alex",
  "assignee_id": 1
}
```

### Ответ

```json
{
  "id": 1,
  "title": "Fix bug",
  "description": "Login page issue",
  "status": "new",
  "requester": "Alex",
  "assignee_name": "John",
  "created_at": "2026-06-04T10:00:00",
  "updated_at": "2026-06-04T10:00:00"
}
```

---

## Получить список задач

### Запрос

```http
GET /tasks
```

### Фильтрация

```http
GET /tasks?status=new
GET /tasks?status=in_progress
GET /tasks?status=done
GET /tasks?status=cancelled
```

---

## Получить задачу по ID

### Запрос

```http
GET /tasks/{id}
```

---

## Обновить задачу

### Запрос

```http
PUT /tasks/{id}
```

### Тело запроса

```json
{
  "status": "done",
  "assignee_id": 2
}
```

Обновление любого поля является необязательным.

---

## Удалить задачу

### Запрос

```http
DELETE /tasks/{id}
```

### Ответ

```json
{
  "id": 1,
  "message": "Task deleted"
}
```

---

# Ошибки

## 404

Задача не найдена

```json
{
  "detail": "Task not found"
}
```

## 400

Пользователь не найден

```json
{
  "detail": "User not found"
}
```
