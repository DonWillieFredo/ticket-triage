# Immediate Next Logical Step

## Current Milestone: Memory Infrastructure

1. Finish creating repo-native AI memory files (`docs/context/`, `.ai/`, `tools/context_pack.py`)
2. Run validation: `uv run ruff check .`, `uv run pytest`, `git status --short`
3. Commit infrastructure separately with message: **Add repo-native AI project memory**

## After Memory Infrastructure

Proceed to **Week 5 CLI workflow**:

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

## Definition of Done for Memory Milestone

- All context files exist with project-specific content
- `.ai/context-index.md` points AI sessions to the correct read order
- `tools/context_pack.py` bundles context successfully
- ruff and pytest pass
- Infrastructure committed before CLI feature work begins
