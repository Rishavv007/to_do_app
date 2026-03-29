import json
import logging
import os
import requests
from marshmallow import ValidationError
from app.schemas.task_schema import AIResponseSchema

logger = logging.getLogger(__name__)

def evaluate_task_with_ai(title: str, description: str) -> dict:
    """
    Simulates or calls an AI service to extract task priority, deadline days, and subtasks.
    Returns:
        {
            "priority": "HIGH" | "MEDIUM" | "LOW",
            "deadline_days": int,
            "subtasks": ["...", "...", "..."]
        }
    """
    # Validate input
    if not title:
        return _fallback_response()

    from datetime import datetime
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    
    # The prompt should be strictly JSON.
    prompt = f"""
    Given the task title '{title}' and description '{description}', please suggest:
    - priority (LOW, MEDIUM, or HIGH)
    - 3 actionable subtasks (list of strings)

    Return ONLY valid JSON with keys: "priority", "subtasks".
    """
    
    # Simulating LLM response for demonstration if no API key is provided, or we can use a mock
    # In a real scenario, we'd use requests.post to OpenAI or similar with the prompt.
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.info("No AI key found, using simulated AI response based on length heuristics.")
        priority = "HIGH" if "urgent" in title.lower() or (description and "urgent" in description.lower()) else "MEDIUM"
        simulated_data = {
            "priority": priority,
            "deadline_days": 3 if priority == "HIGH" else 7,
            "subtasks": [f"Understand {title}", "Implement solution", "Review and test"]
        }
        return _validate_ai_response(simulated_data)

    try:
        logger.info(f"Calling OpenAI API for task suggestions: '{title}'")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that only outputs strictly valid JSON matching the schema."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"}
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        parsed = json.loads(content)
        return _validate_ai_response(parsed)
    except Exception as e:
        logger.error(f"AI Service error: {e}")
        return _fallback_response()

def _calculate_heuristic_deadline(priority: str) -> int:
    """Python native heuristic logic to calculate deadline rather than asking the LLM."""
    if priority == "HIGH":
        return 2  # 2 days strict SLA
    elif priority == "MEDIUM":
        return 7  # 1 week SLA
    elif priority == "LOW":
        return 14 # 2 weeks SLA
    return 7

def _validate_ai_response(data: dict) -> dict:
    """Uses Marshmallow to strictly validate AI output and sanitize."""
    schema = AIResponseSchema()
    try:
        validated_data = schema.load(data)
        # Compute days algorithmically in python per user request
        validated_data["deadline_days"] = _calculate_heuristic_deadline(validated_data.get("priority", "MEDIUM"))
        logger.info("AI response successfully validated and deadline mathematically generated.")
        return validated_data
    except ValidationError as err:
        logger.error(f"AI Schema validation failed: {err.messages}. Falling back.")
        return _fallback_response()
    except Exception as e:
        logger.error(f"Unexpected error validating AI output: {e}")
        return _fallback_response()

def _fallback_response() -> dict:
    logger.warning("Using AI Safe-Fallback response.")
    return {
        "priority": "MEDIUM",
        "deadline_days": 7,
        "subtasks": ["Analyze requirement", "Create implementation plan", "Execute plan"]
    }
