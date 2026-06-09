# Week 4 — Pydantic Models and Validation

## What we built

This week added Pydantic validation models for maintenance work-order samples.

The project moved from plain dictionaries to validated domain objects.

## Big picture

Raw operational data should not be trusted automatically.

Maintenance tickets may come from forms, emails, CSV files, mobile apps, APIs, or eventually LLM output. Before the rest of the system processes a ticket, the ticket should pass through a validation boundary.

Pydantic gives us that boundary.

## Why this matters in production

In a real facilities environment, bad input can create bad routing decisions.

Examples:

- missing ticket ID
- blank work description
- malformed timestamp
- wrong priority value
- safety notes stored as a plain string instead of a list
- unexpected fields entering the system

Validation catches malformed data early before it spreads into filters, routing, persistence, APIs, or AI workflows.

## What I learned

### Pydantic BaseModel

A `BaseModel` defines what valid data looks like.

Unlike a `TypedDict`, which mainly helps the editor and type checker, a Pydantic model validates data at runtime.

### Required fields

Fields such as `id`, `raw_text`, `reported_by`, `created_at`, `expected_trade`, and `expected_priority` are required.

If they are missing, validation fails.

### Field types

Pydantic checks and converts fields where appropriate.

For example, `created_at` is converted from a string into a Python `datetime`.

### Enums

Trades and priorities are constrained to known values.

Current allowed trades:

- electrical
- general
- hvac
- plumbing

Current allowed priorities:

- emergency
- high
- medium
- urgent

This prevents accidental values from entering the system.

### Validators

Validators enforce business rules.

This week, `id`, `raw_text`, and `reported_by` are not allowed to be blank.

### Validation helper

The `validate_work_orders` helper converts the Week 2 sample dictionaries into validated `WorkOrder` objects.

This creates a bridge from raw sample data to validated domain models.

## How this connects to maintenance triage

A maintenance triage system needs to know whether a ticket is structurally valid before it tries to classify, route, escalate, or store it.

A vague location may be allowed because vague tickets happen in real life.

A blank work description should fail because the system cannot triage nothing.

Safety notes remain explicit structured data because safety signals must not be buried in free text.

## How this prepares the project for applied AI

Before using LLMs, the system needs a trusted output shape.

Later, when an LLM extracts fields from messy text, its output can be validated with these models.

This is how we prevent AI output from silently corrupting the workflow.

Good AI-assisted systems are built on good boring engineering first.

## Files changed

- `src/triage/models.py`
- `tests/test_models.py`
- `docs/learning/week-04.md`

## Tests added

The model tests verify:

- all sample work orders validate
- timestamps become `datetime` objects
- trade values become `WorkOrderTrade` enums
- priority values become `WorkOrderPriority` enums
- missing required fields fail
- blank `raw_text` fails
- wrong `safety_notes` type fails
- validation helper returns the expected count
- uppercase enum input is normalized
- unexpected fields are rejected

## Portfolio positioning

I added Pydantic validation models for realistic maintenance work-order samples. This moved Ticket-Triage from plain dictionaries to validated domain objects, enforcing required fields, field types, enum constraints, and business validation before any API, database, or LLM layer was introduced.

## Reflection questions

1. What problem does Pydantic solve?
2. How is a Pydantic `BaseModel` different from a `TypedDict`?
3. Why is validation a boundary?
4. Why should raw work-order data not be trusted automatically?
5. What fields should be required in a maintenance ticket?
6. Why do we preserve safety notes as structured data?
7. What kinds of invalid data should fail fast?
8. Why are Pydantic models useful before FastAPI?
9. Why are Pydantic models useful before LLM structured output?
10. How does this help the project become production-style?

## What comes next

The next logical step is CLI ingestion.

The project now has:

1. realistic sample data
2. deterministic filters
3. validated domain models

Next, we can build a small command-line ingestion path that reads raw JSON or JSONL input and validates it through the Pydantic model.
