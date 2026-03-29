from app.models.task import db, Task

def test_create_task_valid(test_client):
    data = {
        "title": "Buy groceries",
        "description": "Apples, milk, bread",
        "priority": "HIGH"
    }
    response = test_client.post("/api/tasks", json=data)
    assert response.status_code == 201
    assert response.json["title"] == "Buy groceries"
    assert response.json["priority"] == "HIGH"
    assert "id" in response.json

def test_create_task_invalid(test_client):
    data = {"description": "No title provided"}
    response = test_client.post("/api/tasks", json=data)
    assert response.status_code == 400
    assert "title" in response.json["details"]

def test_get_tasks(test_client):
    data = {"title": "Task 1"}
    test_client.post("/api/tasks", json=data)
    response = test_client.get("/api/tasks")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_update_task(test_client):
    post_resp = test_client.post("/api/tasks", json={"title": "Old Title"})
    task_id = post_resp.json["id"]

    update_resp = test_client.put(f"/api/tasks/{task_id}", json={"title": "New Title", "status": "DONE"})
    assert update_resp.status_code == 200
    assert update_resp.json["title"] == "New Title"
    assert update_resp.json["status"] == "DONE"

def test_delete_task(test_client):
    post_resp = test_client.post("/api/tasks", json={"title": "To be deleted"})
    task_id = post_resp.json["id"]

    del_resp = test_client.delete(f"/api/tasks/{task_id}")
    assert del_resp.status_code == 200

    get_resp = test_client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 404
