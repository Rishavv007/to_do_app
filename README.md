# AI Task Manager

A production-grade, fault-tolerant task management system featuring an AI-assisted suggestion engine. This project demonstrates a clean, layered architecture designed for maintainability, strict interface safety, and resilience against unreliable external services (AI).

## Project Overview

The AI Task Manager allows users to manage their workflow with the assistance of a "suggestion engine." Unlike traditional task apps, this system treats AI as an **unreliable external actor**, ensuring that all AI-generated content is strictly validated, coerced into valid types, and handled with safe fallbacks before it ever interacts with the application state.

## Architecture

The system follows a **Clean Layered Architecture** to enforce separation of concerns:

- **Frontend (React + HeroUI + Tailwind v4)**: A modern, reactive UI that handles user interaction and input sanitization.
- **Routes Layer (HTTP)**: Thin controllers that manage request parsing and response formatting. They contain zero business logic.
- **Service Layer (Business Logic)**: The core of the application. Orchestrates data flow between models, schemas, and external AI services.
- **Schema Layer (Validation/Serialization)**: Uses Marshmallow to protect system boundaries. It ensures that both user input and AI output conform to strict types (e.g., date objects, specific enums).
- **Model Layer (Persistence)**: Uses SQLAlchemy with SQLite to manage the task lifecycle. Designed to be easily swap-able for PostgreSQL.

## AI Safety Design
The AI integration (managed in `ai_service.py`) operates under a strict **Zero Trust Policy**. AI is treated as an unreliable, non-deterministic external actor.
1. **Contract Enforcement**: The AI is instructed via System Prompts to return strictly formatted JSON.
2. **Defensive Parsing**: If the AI returns malformed JSON, hallucinates extra fields, or times out, the system catches the error at the service boundary.
3. **Safe Fallback**: When the AI fails, the system logs the failure and returns a pre-defined "Safe Default" object, ensuring the user experience remains fully uninterrupted.

## Validation Strategy
- **Centralized Validation**: Marshmallow enforces strict Data Transfer Object (DTO) contracts at system boundaries.
- **AI Output Validation**: All AI responses are intercepted and piped through the `AIResponseSchema` before being processed by the system.
- **Safe Coercion**: If standard forms or integrations bypass Enum bounds (e.g. invalid string representations), the `_coerce_enums` utility safely catches `ValueErrors` and dynamically assigns logical defaults (e.g., `Priority.MEDIUM`) rather than allowing the backend to crash with a 500 Internal Server Error.

## System Guarantees
- **AI is Unreliable**: The backend never trusts the AI.
- **Zero Direct DB Access**: Routes and AI services have zero direct access to the database engine.
- **100% Validated State**: All data (from humans or AI) entering the core service layer guarantees conformity to strict schemas.

## Key Technical Decisions

- **Flask + Blueprint**: Enables modular routing and prevents the "God Object" app pattern.
- **Marshmallow Schemas**: Centralizes validation logic. If a field like `priority` is added, it only needs to be updated in the schema to protect the entire API.
- **Service Layer Pattern**: By keeping business logic out of routes, we ensure the system is **Change Resilient**. Adding Authentication or a different DB requires zero changes to the routing logic.
- **SQLite for Simplicity**: Chosen for portability in evaluation, but wrapped in SQLAlchemy to ensure production-readiness for larger relational databases.

## Folder Structure

```text
backend/
├── app/
│   ├── models/     # Persistence Layer (SQLAlchemy)
│   ├── routes/     # HTTP/API Layer (Blueprints)
│   ├── schemas/    # Validation Layer (Marshmallow)
│   ├── services/   # Business & AI Service Logic
│   └── utils/      # Shared Helpers
├── tests/          # Pytest suite
└── run.py          # Entry point
frontend/
├── src/
│   ├── components/ # Higher-order UI components
│   ├── pages/      # Route-level components
│   └── services/   # API bridge (Fetch wrappers)
ai/                 # Formal AI Governance and Standards
```

## Setup & Execution

### Backend
1. `cd backend`
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python run.py` (Server runs on port 5001)

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev` (Access at http://localhost:5173)

### Verification
Run `pytest` in the `backend/` directory to verify the API logic, schema validation, and AI fallback mechanisms.
