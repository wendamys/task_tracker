# DATABASE.md

# Database Structure

В проекте используется SQLite.

Файл базы данных:

```text
task_tracker.db
```

---

# Таблица users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL
);
```

### Описание полей

| Поле  | Тип     | Описание                   |
| ----- | ------- | -------------------------- |
| id    | INTEGER | Идентификатор пользователя |
| name  | VARCHAR | Имя сотрудника             |
| email | VARCHAR | Email сотрудника           |

---

# Таблица tasks

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    status VARCHAR(50) NOT NULL,
    requester VARCHAR(50) NOT NULL,
    assignee_id INTEGER,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
```

### Описание полей

| Поле        | Тип      | Описание                   |
| ----------- | -------- | -------------------------- |
| id          | INTEGER  | Идентификатор задачи       |
| title       | VARCHAR  | Название задачи            |
| description | VARCHAR  | Описание задачи            |
| status      | VARCHAR  | Статус выполнения          |
| requester   | VARCHAR  | Автор заявки               |
| assignee_id | INTEGER  | Исполнитель                |
| created_at  | DATETIME | Дата создания              |
| updated_at  | DATETIME | Дата последнего обновления |

---

# Связи

## User → Tasks

Один пользователь может быть назначен на множество задач.

```text
User (1)
    │
    └───────< Task (N)
```

SQLAlchemy relationship:

```python
User.tasks
Task.assignee
```

---

# Автоматические поля

## created_at

Заполняется автоматически при создании задачи.

## updated_at

Автоматически обновляется при каждом изменении записи.

---

# Начальные данные

При первом запуске создаются тестовые пользователи:

```text
Alex
alex@example.ru

John
john@yandex.ru
```

Они используются для назначения задач через интерфейс приложения.
