import json
import logging
import os
import requests

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

    # The prompt should be strictly JSON.
    prompt = f"""
    Given the task title '{title}' and description '{description}', please suggest:
    - priority (LOW, MEDIUM, or HIGH)
    - a reasonable deadline in days from today (integer)
    - 3 actionable subtasks (list of strings)

    Return ONLY valid JSON with keys: "priority", "deadline_days", "subtasks".
    """
    
    # Simulating LLM response for demonstration if no API key is provided, or we can use a mock
    # In a real scenario, we'd use requests.post to OpenAI or similar with the prompt.
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.info("No AI key found, using simulated AI response based on length heuristics.")
        priority = "HIGH" if "urgent" in title.lower() or (description and "urgent" in description.lower()) else "MEDIUM"
        return {
            "priority": priority,
            "deadline_days": 3,
            "subtasks": [f"Understand {title}", "Implement solution", "Review and test"]
        }

    try:
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

def _validate_ai_response(data: dict) -> dict:
    try:
        priority = data.get("priority", "MEDIUM").upper()
        if priority not in ["LOW", "MEDIUM", "HIGH"]:
            priority = "MEDIUM"
            
        deadline_days = int(data.get("deadline_days", 3))
        if deadline_days < 0:
            deadline_days = 0
            
        subtasks = data.get("subtasks", [])
        if not isinstance(subtasks, list):
            subtasks = []

        return {
            "priority": priority,
            "deadline_days": deadline_days,
            "subtasks": [str(s) for s in subtasks][:3]
        }
    except Exception as e:
        logger.error(f"Failed to parse AI output: {e}")
        return _fallback_response()

def _fallback_response() -> dict:
    return {
        "priority": "MEDIUM",
        "deadline_days": 7,
        "subtasks": ["Analyze requirement", "Create implementation plan", "Execute plan"]
    }
