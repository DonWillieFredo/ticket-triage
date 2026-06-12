# Key Decisions Log

Durable decisions that future sessions should treat as settled unless explicitly revisited.

| Decision | Rationale | Status |
| -------- | --------- | ------ |
| **Local-first foundation** | Learn production-style engineering without cloud complexity too early. All core logic runs locally first. | Active |
| **Deterministic logic before AI** | Safety rules and filters must be plain, testable Python before any LLM integration. | Active |
| **No FastAPI yet** | Web API comes in Phase 2 (Weeks 9–16). Current phase is Python foundations only. | Active |
| **No database yet** | Persistence comes later. Sample data and in-memory/dict structures suffice for now. | Active |
| **No LLMs yet** | Classification and extraction are future phases. Current work is typed models and filters. | Active |
| **Weekly visible progress** | Each week ships something demonstrable; learning logs live in `docs/learning/`. | Active |
| **Repo-native AI memory** | Project context lives in `docs/context/` and `.ai/` so any AI session can rebuild context from the repo. | Active (this milestone) |

## Related ADRs

Formal architecture decision records live in `docs/decisions/`:

- [0001-local-first-build.md](../decisions/0001-local-first-build.md) — Local-first build using Python, uv, pytest, ruff, and GitHub.

## When to Add a Decision Here

Record a decision when:

- It excludes or includes a technology for a meaningful period
- It changes how the project is structured or tested
- It affects what AI assistants should or should not do by default

Do not log transient implementation details — those belong in `technical-truths.md` or code comments.
