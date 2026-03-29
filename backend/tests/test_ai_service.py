import pytest
from unittest.mock import patch
from app.services.ai_service import evaluate_task_with_ai, _validate_ai_response

def test_ai_suggestion():
    # Integration test hitting the heuristical fallback since no key is matched internally
    response = evaluate_task_with_ai("Test title", "Test Description")
    assert "priority" in response
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

@patch('app.services.ai_service.requests.post')
def test_ai_fallback_scenario_mock_failure(mock_post):
    # Simulate a timeout or network crash
    mock_post.side_effect = Exception("OpenAI servers down!")
    # Make sure we supply an API KEY in the environment to trigger the API path
    import os
    os.environ["OPENAI_API_KEY"] = "fake-key-to-force-api"
    response = evaluate_task_with_ai("Urgent DB Fix", "Fix schema")
    
    # Assert fallback handles it gracefully
    assert response["priority"] == "MEDIUM"
    assert "Analyze requirement" in response["subtasks"]
    del os.environ["OPENAI_API_KEY"]

def test_ai_response_validation():
    # Test our schema handles bad AI payload internally
    bad_payload = {
        "priority": "CRITICAL", # Invalid Enum
        # missing subtasks
    }
    response = _validate_ai_response(bad_payload)
    
    # Ensure it rejected parsing and returned the safe fallback
    assert response["priority"] == "MEDIUM"
    assert "Execute plan" in response["subtasks"]
