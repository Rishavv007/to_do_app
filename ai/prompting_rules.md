# AI Prompting Rules

To ensure system stability, all interactions with the LLM must follow these deterministic rules. The AI is a component, not a conversationalist.

## Rules for Response Generation
1. **Strict JSON Output**: The response must be a single JSON object. No markdown blocks (```json```), no preamble, and no conversational text.
2. **Schema Enforcement**: Output must contain exactly three keys:
    - `"priority"`: String (MUST be one of: `LOW`, `MEDIUM`, `HIGH`).
    - `"deadline_days"`: Integer (Positive integer only).
    - `"subtasks"`: List of Strings (Exactly 3 items).
3. **Zero Hallucination**: Do not add keys such as `reasoning`, `notes`, or `tags`.
4. **Deterministic Values**: If the title is vague, default to `MEDIUM` priority and `7` days.

## Example Good Response
```json
{
  "priority": "HIGH",
  "deadline_days": 3,
  "subtasks": ["Initial research", "Core implementation", "Final testing"]
}
```

## Example Bad Response (REJECTED)
"I think this task is high priority. Here is your JSON:
```json
{
  "priority": "High",
  "days": 3,
  "tasks": [...]
}
```"
*Reason: Contains natural language, non-standard Enum case ("High" vs "HIGH"), and incorrect keys ("days" vs "deadline_days").*
