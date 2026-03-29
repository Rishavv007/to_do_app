# AI System Constraints

This system is built using the Clean Architecture model, where Artificial Intelligence is treated as an unreliable third-party service rather than internal business logic.

## 1. Zero Trust Policy (Validation Required)
All AI output MUST be treated as user-input and validated before usage. The Marshmallow `AIResponseSchema` strictly intercepts API responses before the service layer proceeds. We expect the AI to lie, hallucinate, and break JSON. 

## 2. No Direct Database Access
- The AI service layer `ai_service.py` is fully sandboxed. It does not import `db` or SQLAlchemy models. 
- It has zero context on past tasks or other user rows. It is purely functional: `(Title, Description) -> Dict`.

## 3. Schema Enforcement
- Coercion mechanisms (e.g. `_coerce_enums`) handle unexpected values by safely assigning a default value (e.g. `Priority.MEDIUM`) rather than allowing backend exceptions `(ValueError)` to bubble up as 500 errors.
- Schema validation enforces strict lengths and types to guard against excessive token usage attacks.
