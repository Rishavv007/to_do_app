# AI Prompting Rules

When interacting with the system's LLM, the following rules MUST be strictly adhered to:

## 1. Strict JSON Format Requirement
- The AI must return **strict JSON only**.
- Do not include markdown codeblocks (e.g., ````json \n {...} \n ````) unless properly stripped by the backend. Use `"response_format": {"type": "json_object"}` natively via the OpenAI API parameters.

## 2. No Natural Language
- Never include conversational filler (e.g., "Here is your task assessment...").
- Output should start with `{` and end with `}` immediately.

## 3. Strict Schema Mapping (No Extra Fields)
- The JSON output MUST ONLY contain the fields explicitly defined in the `AIResponseSchema`:
  - `priority`: Must be exactly `"LOW"`, `"MEDIUM"`, or `"HIGH"`.
  - `subtasks`: Must be a list of strings containing exactly 3 actionable steps. No objects, no nested lists.
- Any extra fields injected by hallucination will either be stripped or fail Marshmallow schema validation.
