# Immediate Next Logical Step

## Current Milestone: Green Baseline Before Week 5

1. Commit memory infrastructure: **Add repo-native AI project memory**
2. Commit `safety_notes` alignment fix (samples → `list[str]`, tests green)
3. Confirm: `uv run ruff check .` and `uv run pytest` pass

## Next: Week 5 CLI Workflow

- Local-only, no network dependencies
- Deterministic behavior (no LLMs)
- Fully typed public functions
- pytest coverage for CLI behavior
- Uses existing models, samples, and filters

## Week 5 Non-Goals

- No FastAPI
- No database
- No LLMs or agents
- No MCP
- No cloud deployment

## Definition of Done for Green Baseline

- Memory infrastructure committed
- `safety_notes` aligned as `list[str]` across samples, model, and tests
- ruff and pytest pass
- Ready for Week 5 CLI feature work
