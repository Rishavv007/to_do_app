# Agents Code Generation Rules

## Core Principles
* **Always validate inputs**: All incoming data from the API or user interaction must be validated before any processing.
* **Never bypass schema validation**: All data entering the business logic must pass through designated schema validation (e.g., Pydantic or Marshmallow).
* **Keep functions small and modular**: Limit a function to a single responsibility. This enhances testability and readability.
* **Avoid tight coupling**: Use dependency injection concepts and clearly defined interfaces between the controller (routes), service, and model layers.

## Backend Architecture
* Do not allow the `routes` directory to know about the database (`models`). Services act as the intermediary.
* Return appropriate HTTP status codes for every response:
  * 200/201 on success.
  * 400 on bad requests (validation errors).
  * 404 on not found.
  * 500 on internal server errors.
* Use centralized error handling within blueprints or the app factory.

## AI Service Guidelines
* The AI service layer (`ai_service.py`) must isolate third-party or LLM API calls.
* Always enforce structured JSON output from LLM responses and parse it safely.
* Implement a safe fallback: if the AI response is unparseable or violates schema, return a default graceful response rather than crashing the system.
