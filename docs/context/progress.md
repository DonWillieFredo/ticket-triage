# Progress

Weekly milestones and what has shipped.

## Week 1 — Project Direction Established

- Repository initialized with Python, uv, pytest, ruff
- Project identity and roadmap defined
- Local-first Build-and-Learn approach chosen

## Week 2 — Sample Data and Training Console

- Sample maintenance work orders added (`src/triage/samples.py`)
- Training console dashboard (`tools/training-console.html`)
- Learning log structure in `docs/learning/`

## Week 3 — Deterministic Filters and Tests

- Filter functions: by trade, by priority, safety-related, vague/incomplete
- Counter-based aggregation: `count_by_trade`, `count_by_priority`
- Full pytest coverage for filters
- Pydantic models and validation (`src/triage/models.py`)

## Week 5 — CLI Ingestion and Validation

- `src/triage/cli.py` — argparse `validate` command for JSON/JSONL files
- Validates records through existing `WorkOrder` Pydantic model
- Exit codes and human-readable summary with source locations for errors
- Full pytest coverage in `tests/test_cli.py`
- Learning log: `docs/learning/week-05.md`

## Week 6 — CLI Filter and Count Commands

- Extended `src/triage/cli.py` with `filter` and `count` subcommands
- Reuses `load_records()`, `validate_records()`, and `src/triage/filters.py`
- Filter by trade, priority, safety, or incomplete; count by trade or priority
- Validates files before querying; exit 1 on load, validation, or argument errors
- 12 additional CLI tests in `tests/test_cli.py`
- Learning log: `docs/learning/week-06.md`

## Upcoming

- **Week 7+:** Additional CLI commands, evaluation fixtures, or Phase 2 FastAPI
- **Later phases:** LLMs, evaluation harness
