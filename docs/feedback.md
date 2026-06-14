# User Feedback

ContextOps stores user feedback linked to individual agent execution traces.

## Endpoints

Submit feedback: `POST /api/v1/feedback`

Retrieve feedback: `GET /api/v1/feedback/{feedback_id}`

## Feedback Fields

- trace ID
- user email
- rating from 1 to 5
- optional comment
- optional label
- creation timestamp

## Example Labels

- helpful
- incorrect
- incomplete
- unsupported-claim
- wrong-source
- tool-error

## Ownership Validation

Feedback may only be submitted by the user who owns the associated agent trace.

## Why This Matters

User feedback creates a production improvement signal for evaluation datasets, failure analysis, prompt iteration, model comparison, and future retraining workflows.

## Future Improvements

- feedback analytics
- feedback-driven evaluation datasets
- unresolved feedback queues
- reviewer assignment
- feedback-triggered regression tests
- retraining and prompt-improvement triggers
