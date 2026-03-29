# AI Usage and Safety Strategy

## Implementation Context
AI is utilized within the **Task Creation/Editing** flow to reduce cognitive load for the user. It derives metadata (priority/deadlines/subtasks) from unstructured text.

## Risk Assessment
| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| **Hallucination** | Low | Strict Schema validation and user-in-the-loop review. |
| **Invalid JSON** | Medium | `try/except` block at the service layer with immediate fallback to a safe default. |
| **Latency** | Medium | Asynchronous front-end UI (loading states) and optimized models. |
| **Non-deterministic Enum** | Low | Programmatic coercion inside `ai_service.py` to match internal Enums. |

## Request Lifecycle
1. **Frontend**: Captures title/description.
2. **Backend (Service)**: Wraps input in a strict system prompt.
3. **LLM**: Generates JSON.
4. **Backend (Defensive Parser)**: 
    - Attempt to parse JSON.
    - Validate against `TaskSchema`.
    - If valid, return to user.
    - If invalid or timeout, return `_fallback_response()` (safe defaults).
5. **Frontend**: Displays suggestions; user has the final authority to "Apply" or discard.
