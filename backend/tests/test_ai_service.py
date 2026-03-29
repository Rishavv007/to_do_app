import pytest
from app.services.ai_service import evaluate_task_with_ai

def test_ai_suggestion():
    # As we are doing integration and the AI uses a fallback when no prompt / key is given,
    # we can test the fallback directly or mocking if we wanted.
    response = evaluate_task_with_ai("Test title", "Test Description")
    assert "priority" in response
    assert "deadline_days" in response
    assert "subtasks" in response
    assert isinstance(response["subtasks"], list)
    assert response["priority"] in ["LOW", "MEDIUM", "HIGH"]

def test_ai_suggestion_no_title(test_client):
    response = test_client.post("/api/tasks/suggest", json={"description": "Missing title"})
    assert response.status_code == 400
    assert "title" in response.json["details"]

def test_ai_suggestion_valid(test_client):
    response = test_client.post("/api/tasks/suggest", json={"title": "Test Title"})
    assert response.status_code == 200
    assert "priority" in response.json
