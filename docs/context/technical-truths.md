# Technical Truths

Current technical facts about the codebase. Update when the implementation changes.

## Stack

| Tool | Role |
| ---- | ---- |
| Python 3.13+ | Language |
| uv | Package manager and script runner |
| pytest | Test runner |
| ruff | Lint and format |
| Pydantic v2 | Data validation (models in progress) |

## Project Layout

```
src/triage/
├── __init__.py
├── models.py      # WorkOrder, enums, validate_work_orders()
├── samples.py     # Sample work order data
└── filters.py     # Deterministic filter and count functions
tests/
├── test_models.py
└── test_filters.py
tools/
├── training-console.html
└── context_pack.py   # Bundles AI context files for handover
```

## Domain Enums

**Trades:** `electrical`, `general`, `hvac`, `plumbing`

**Priorities:** `emergency`, `urgent`, `high`, `medium`

## Implemented Logic

### Models (`src/triage/models.py`)

- `WorkOrderTrade` and `WorkOrderPriority` StrEnums
- `WorkOrder` Pydantic model with `extra="forbid"`
- Blank-field validation on `id`, `raw_text`, `reported_by`
- Enum normalization via `casefold()` in validators
- `validate_work_orders()` accepts `Iterable[WorkOrderSample]`, returns `list[WorkOrder]`

### Filters (`src/triage/filters.py`)

- `get_work_orders_by_trade()` — case-insensitive trade filter
- `get_work_orders_by_priority()` — case-insensitive priority filter
- `get_safety_related_work_orders()` — tickets with non-empty `safety_notes`
- `get_vague_or_incomplete_work_orders()` — missing location or asset
- `count_by_trade()` / `count_by_priority()` — `Counter`-based aggregation

## Coding Themes Established

- Type hints on public functions
- `Iterable` for input collections, `list` for return types
- `casefold()` for case-insensitive comparisons
- List comprehensions for filtering
- `collections.Counter` for counting
- Deterministic, side-effect-free filter functions
- Safety-first filtering (safety notes, incomplete ticket detection)
- Human-in-the-loop thinking (vague ticket flagging)

## Not Yet Implemented

- CLI entry point (Week 5 target)
- FastAPI, database, LLMs, agents, MCP
