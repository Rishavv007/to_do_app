# AI Usage & Guarantees

This document outlines how the AI (OpenAI `gpt-4o-mini`) is integrated securely into the Task Manager Application.

## Usage Overview
The AI provides predictive inputs for a task before the user commits to creating it. When a user fills out a Title and Description, they can press "Get AI Suggestions".
The service will pass this to OpenAI to map the text to:
1. An Actionable Priority scale (`LOW`, `MEDIUM`, `HIGH`)
2. A realistic integer deadline (`deadline_days`)
3. Three actionable subtasks that break down complex jobs.

## Identified Risks
1. **Hallucination**: The LLM might invent fields, priority values, or return Python dictionary syntax instead of valid JSON.
2. **Invalid Output**: Non-integer deadlines or malformed lists.
3. **Latency**: OpenAI endpoints can time out, causing the UI to hang.

## Mitigations
1. **Validation Pipeline**: Responses are piped through python's `json.loads()` and Marshmallow's `AIResponseSchema` strictly stripping unpredictable payload artifacts.
2. **System Fallback**: If the LLM throws a Timeout, a validation crash, or keys are missing, the system catches the `Exception` seamlessly, logs it, and falls back to a deterministic heuristic model without the user ever receiving a 500 Error.
3. **Safe Coercion**: Any invalid string enums assigned via API are mapped back securely to `.MEDIUM` priority without crashing the Flask `db.session` transaction.
