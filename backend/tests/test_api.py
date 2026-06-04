def test_root_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json() or "status" in response.json()


def test_get_users(client, test_user):
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test User"
    assert data[0]["email"] == "test@example.com"


def test_create_task_success(client, test_user):
    payload = {
        "title": "Написать тесты",
        "description": "Покрыть API автотестами",
        "requester": "Team Lead",
        "assignee_id": test_user.id
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 200 
    data = response.json()
    assert data["title"] == "Написать тесты"
    assert data["status"] == "new"
    assert data["assignee_id"] == test_user.id


def test_create_task_validation_error(client):
    payload = {
        "title": "",  # Пустой заголовок должен вызвать ошибку валидации Pydantic
        "description": "Описание",
        "requester": "User"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_get_tasks_with_filter(client, test_user):
    # Создаем задачу
    client.post("/tasks", json={
        "title": "Важная задача",
        "description": "Описание",
        "requester": "Manager",
        "assignee_id": test_user.id
    })

    # Проверяем получение всех задач
    response_all = client.get("/tasks")
    assert response_all.status_code == 200
    assert len(response_all.json()) == 1

    # Проверяем фильтрацию по статусу
    response_filtered = client.get("/tasks?status=new")
    assert response_filtered.status_code == 200
    assert len(response_filtered.json()) == 1

    response_empty = client.get("/tasks?status=done")
    assert response_empty.status_code == 200
    assert len(response_empty.json()) == 0


def test_get_single_task(client, test_user):
    create_resp = client.post("/tasks", json={
        "title": "Тестовая задача",
        "description": "Для получения",
        "requester": "QA",
        "assignee_id": test_user.id
    })
    task_id = create_resp.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Тестовая задача"


def test_get_single_task_not_found(client):
    response = client.get("/tasks/99999")
    assert response.status_code == 404


def test_update_task(client, test_user):
    create_resp = client.post("/tasks", json={
        "title": "Старая задача",
        "description": "Описание",
        "requester": "User"
    })
    task_id = create_resp.json()["id"]

    update_payload = {
        "status": "in_progress",
        "assignee_id": test_user.id
    }
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["assignee_id"] == test_user.id
    # Проверка, что updated_at изменился (опционально, но полезно)
    assert data["updated_at"] != create_resp.json()["updated_at"]


def test_delete_task(client):
    create_resp = client.post("/tasks", json={
        "title": "Задача на удаление",
        "description": "Описание",
        "requester": "User"
    })
    task_id = create_resp.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # Проверяем, что задача действительно удалена
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404
