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

## Current — Repo-Native Memory Infrastructure

- Adding `docs/context/` AI memory files
- Adding `.ai/context-index.md` and skill procedures
- Adding `tools/context_pack.py` for context bundling
- Preparing for Week 5 CLI workflow (not started yet)

## Upcoming

- **Week 5:** Local, deterministic, typed CLI workflow
- **Later phases:** FastAPI, LLMs, evaluation harness (see README roadmap)
