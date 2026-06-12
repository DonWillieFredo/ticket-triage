# Skill: Review

Use this procedure **after** implementation, before considering work complete.

## Review Checklist

### Scope

- [ ] Changes match the stated goal — no unrelated refactors or drive-by edits
- [ ] No excluded technologies added (FastAPI, database, LLMs, agents, MCP, cloud)
- [ ] Increment size is appropriate — not over-engineered

### Type Hints

- [ ] Public functions have type annotations
- [ ] `Iterable` used for input collections where appropriate
- [ ] Return types are explicit

### Deterministic Behavior

- [ ] Core logic is plain Python — no hidden side effects or non-deterministic calls
- [ ] String comparisons use `casefold()` where case-insensitivity is intended
- [ ] Filter/validation functions are pure given their inputs

### Tests

- [ ] New behavior has pytest coverage
- [ ] Edge cases considered (empty input, blank fields, case variants)
- [ ] `uv run pytest` passes

### Ruff

- [ ] `uv run ruff check .` passes
- [ ] No unjustified `# noqa` comments

### Docs

- [ ] Public API changes reflected in docstrings or context files if needed
- [ ] README or learning docs updated only if this change affects them

### Memory Updates

- [ ] If durable facts changed → update `technical-truths.md`
- [ ] If progress shipped → update `progress.md`
- [ ] If next step changed → update `next.md`
- [ ] If new decision made → update `decisions.md`
- [ ] Use `.ai/skills/remember.md` for guidance

### Decision Log Impact

- [ ] Does this work establish a new durable decision? If yes, record in `decisions.md` or `docs/decisions/`
- [ ] Does this work violate an existing decision? If yes, stop and confirm with the project owner

## Output

Summarize findings: pass/fail per section, any required fixes before merge or commit.
