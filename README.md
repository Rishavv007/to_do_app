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

## AI Integration Design

The AI integration is isolated within `ai_service.py`. It follows three defensive principles:
1. **Contract Enforcement**: The AI is instructed via System Prompts to return strictly formatted JSON.
2. **Defensive Parsing**: If the AI returns malformed JSON or unexpected fields, the system catches the error at the service boundary.
3. **Safe Fallback**: When the AI fails, the system returns a pre-defined "Safe Default" object, ensuring the user experience remains uninterrupted.

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
