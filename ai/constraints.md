# AI System Constraints

These constraints define the safety boundaries between the AI Suggestion Engine and the Core Application.

## Boundary Integrity
- **Zero Trust**: The application never trusts AI output. All LLM responses must pass through `TaskSchema` before being processed.
- **Read-Only Context**: The AI service has no access to the Database. It only receives strings (title/description) as input.
- **Isolation**: Interaction with OpenAI/LLM providers must strictly live within `ai_service.py`.

## Logic Constraints
- **No Direct DB Writes**: AI output can never trigger a `db.session.commit()` directly. It only populates a transient "Suggestion" object for user review.
- **Enum Coercion**: Any variation of priority (e.g., "Very High") must be coerced to the closest valid Enum member (`HIGH`) or rejected for a default.
- **Input Sanitization**: User inputs are stripped of HTML/Script tags before being sent to the AI to prevent prompt injection.
