# Core Project Instructions

These rules apply to all work in Ticket-Triage unless the project owner explicitly overrides them.

## Build Principles

1. **Small, testable increments** — Ship one focused change at a time. Each increment should be reviewable and verifiable.
2. **Deterministic logic before AI** — Safety rules, filters, validation, and routing heuristics must be plain Python first. LLMs come later, after the core is trustworthy.
3. **Type hints and tests** — Public functions need type annotations. Behavior changes need pytest coverage.
4. **Build-and-Learn teaching style** — Explain trade-offs, connect code to real maintenance triage scenarios, and favor readable code over clever abstractions.

## Excluded Technologies (Unless Explicitly Allowed)

Do **not** add these without explicit approval:

- FastAPI or other web frameworks
- Databases (SQLite, Postgres, ORMs)
- LLMs or agent frameworks
- MCP servers or external API integrations
- Cloud services or deployment tooling
- UI frameworks beyond the existing training console

## Domain Connection

When implementing logic, tie it to real maintenance triage:

- Trades: electrical, general, HVAC, plumbing
- Priorities: emergency, urgent, high, medium
- Safety notes and vague/incomplete ticket detection reflect real operational risk
- Human-in-the-loop is a design requirement, not an afterthought

## Code Quality

- Use **uv** for dependency and script execution
- Run **ruff** before considering work done
- Keep **pytest** green
- Match existing conventions in `src/triage/`
- Prefer `Iterable` over `list` for function parameters when accepting collections
- Use `casefold()` for case-insensitive string comparisons

## Memory Maintenance

After durable project changes, update the appropriate files under `docs/context/` (see `.ai/skills/remember.md`).
