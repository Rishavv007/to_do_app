# Developer Coding Standards

Guidelines for maintaining a production-grade, layered codebase.

## Functional Standards
- **Function Responsibility**: Every function must follow the Single Responsibility Principle (SRP).
- **Max Function Length**: Functions should not exceed 30 lines. If they do, refactor into smaller private helpers.
- **No Logic in Routes**: Routes must only:
  1. Extract parameters.
  2. Call a Service method.
  3. Return a JSON response with the appropriate status code.

## Consistency & Safety
- **Schema-First**: No data should enter the business logic without being processed by `Schema.load()`.
- **Error Handling Format**: All API errors must return a consistent JSON structure:
  `{"error": "Type", "message": "Details", "details": {OptionalValidationErrors}}`
- **Observability**: Every failed AI request or Validation error must be logged with `logger.warning` or `logger.error` including the trace ID or Task ID.
