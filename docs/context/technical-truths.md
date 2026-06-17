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
├── cli.py         # argparse CLI: validate JSON/JSONL work-order files
├── models.py      # WorkOrder, enums, validate_work_orders()
├── samples.py     # Sample work order data
└── filters.py     # Deterministic filter and count functions
tests/
├── test_cli.py
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
- `safety_notes: list[str]` on both `WorkOrder` and `WorkOrderSample` (empty list when none)
- Blank-field validation on `id`, `raw_text`, `reported_by`
- Enum normalization via `casefold()` in validators
- `validate_work_orders()` accepts `Iterable[WorkOrderSample]`, returns `list[WorkOrder]`

### CLI (`src/triage/cli.py`)

- `uv run python -m triage.cli validate <path>` — validate JSON/JSONL work-order files
- `uv run python -m triage.cli filter <path> --trade|--priority|--safety|--incomplete` — filter validated records
- `uv run python -m triage.cli count <path> --by trade|priority` — count validated records by category
- Supports `.json` (object or array) and `.jsonl` (one object per line)
- `filter` and `count` validate all records before querying; refuse partially invalid files
- Exit 0 on success; exit 1 on load, validation, or argument errors
- Human-readable output with work-order IDs for filter matches and sorted counts

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

- FastAPI, database, LLMs, agents, MCP
