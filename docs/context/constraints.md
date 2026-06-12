# Current Constraints

Hard boundaries for the current project phase. Violating these requires explicit owner approval.

## Architecture

- **Local-first** — Everything must run from a fresh clone with `uv sync` and no external services.
- **Minimal dependencies** — Add packages only when they solve a concrete, current need.
- **No premature framework sprawl** — Resist adding FastAPI, ORMs, LLM SDKs, or cloud tooling before their scheduled phase.

## Quality

- **Tests must stay green** — No merging or committing broken pytest suites.
- **Lint must pass** — `uv run ruff check .` should succeed before work is considered done.
- **Understandable from a fresh clone** — A new developer (or AI session) should orient quickly using README, `docs/context/`, and `.ai/context-index.md`.

## Portfolio

- **Portfolio-readable** — Code, commits, and docs should tell a clear story of incremental, thoughtful engineering.
- **Domain-authentic** — Maintenance triage scenarios should feel real, not toy examples.
- **Honest scope** — Do not claim features (API, AI, deployment) that are not yet built.

## Process

- **One milestone at a time** — Finish memory infrastructure before Week 5 CLI work; finish CLI before web layer, etc.
- **Separate commits for infrastructure vs features** — Infrastructure milestones (like this memory system) commit separately from feature work.
