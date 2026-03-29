import json
import logging
import os
import requests
from marshmallow import ValidationError
from app.schemas.task_schema import AIResponseSchema

logger = logging.getLogger(__name__)

def evaluate_task_with_ai(title: str, description: str, deadline=None) -> dict:
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
        return _fallback_response(deadline)

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
        return _validate_ai_response(simulated_data, deadline)

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
        return _validate_ai_response(parsed, deadline)
    except Exception as e:
        logger.error(f"AI Service error: {e}")
        return _fallback_response(deadline)

def _calculate_heuristic_deadline(priority: str, deadline=None) -> int:
    """Python native heuristic logic to calculate deadline mathematically."""
    if deadline:
        from datetime import date
        # deadline is a datetime.date object from marshmallow
        delta = (deadline - date.today()).days
        return delta if delta >= 0 else 0

    if priority == "HIGH":
        return 1  # 1 day strict SLA
    elif priority == "MEDIUM":
        return 3  # 3 days SLA
    elif priority == "LOW":
        return 7   # 1 week SLA
    return 3

def _validate_ai_response(data: dict, deadline=None) -> dict:
    """Uses Marshmallow to strictly validate AI output and sanitize."""
    schema = AIResponseSchema()
    try:
        validated_data = schema.load(data)
        # Compute exact days mathematically in python from user's explicit deadline
        validated_data["deadline_days"] = _calculate_heuristic_deadline(validated_data.get("priority", "MEDIUM"), deadline)
        logger.info("AI response successfully validated and exact deadline generated.")
        return validated_data
    except ValidationError as err:
        logger.error(f"AI Schema validation failed: {err.messages}. Falling back.")
        return _fallback_response(deadline)
    except Exception as e:
        logger.error(f"Unexpected error validating AI output: {e}")
        return _fallback_response(deadline)

def _fallback_response(deadline=None) -> dict:
    logger.warning("Using AI Safe-Fallback response.")
    days = 7
    if deadline:
        from datetime import date
        delta = (deadline - date.today()).days
        days = delta if delta >= 0 else 0

    return {
        "priority": "MEDIUM",
        "deadline_days": days,
        "subtasks": ["Analyze requirement", "Create implementation plan", "Execute plan"]
    }
