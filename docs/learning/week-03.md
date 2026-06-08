# Week 3 — Typed Filters and Python Fundamentals

## What we built

This week adds typed helper functions for querying the Week 2 maintenance work-order sample data.

New files:

- `src/triage/filters.py`
- `tests/test_filters.py`

## Why this matters

Before adding Pydantic, FastAPI, databases, or LLMs, the project needs simple deterministic logic over realistic domain data.

This is the first step from:

> static sample data

toward:

> testable triage logic

## What I learned

- How to write small Python functions
- How to use type hints with project data
- Why `Iterable` makes functions more flexible than requiring only `list`
- How list comprehensions can express filtering logic clearly
- How `Counter` can summarize work-order categories
- How to write tests for normal behavior and empty input behavior

## Functions added

- `get_work_orders_by_trade`
- `get_work_orders_by_priority`
- `get_safety_related_work_orders`
- `get_vague_or_incomplete_work_orders`
- `count_by_trade`
- `count_by_priority`

## Scope intentionally avoided

We did not add:

- Pydantic
- FastAPI
- SQLModel or database persistence
- LLM calls
- prompt workflows
- agents

The goal was to keep the project local-first, typed, tested, and understandable.

## Production lesson

In real facilities maintenance triage, filtering by trade, priority, safety notes, and incomplete data is basic but essential.

These helpers are small, but they model real operational questions:

- Which tickets belong to plumbing?
- Which tickets are high priority?
- Which tickets contain safety concerns?
- Which tickets are too vague to route confidently?

This supports the larger principle of the project:

> LLMs may suggest, but deterministic logic and safety rules must remain inspectable and testable.
