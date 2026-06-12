# Skill: Remember

Use this procedure **after meaningful progress** to keep project memory accurate for future AI sessions.

## When to Update Memory

Update memory when work:

- Ships a visible milestone (new module, CLI, test suite expansion)
- Establishes or changes a durable decision
- Adds new technical facts (enums, functions, dependencies, layout)
- Changes the immediate next step
- Reveals a new recovery pattern

Do **not** update memory for trivial fixes (typos, formatting-only changes).

## Which File to Update

### `docs/context/progress.md`

Update when:

- A weekly milestone completes
- A significant feature ships (even within a week)
- Current phase status changes

Add dated entries. Keep historical weeks; append new ones.

### `docs/context/technical-truths.md`

Update when:

- New modules, functions, or enums are added
- Project layout changes
- Dependencies are added or removed
- Coding patterns or conventions evolve

Keep facts current — remove "not yet implemented" items once built.

### `docs/context/decisions.md`

Update when:

- A technology is explicitly included or excluded for a phase
- Architecture direction changes
- Process rules change (e.g., commit conventions)

Link to formal ADRs in `docs/decisions/` when appropriate.

### `docs/context/next.md`

Update when:

- The immediate next step completes
- Priorities shift
- A new milestone becomes the focus

Keep this file short — one current milestone, clear definition of done.

### `docs/context/recovery.md`

Update when:

- A new recurring failure pattern emerges
- Recovery commands change (e.g., new tooling)
- A useful debugging workflow is discovered

## Update Procedure

1. Read the current file before editing — do not duplicate existing entries
2. Write concise, factual updates — future AI sessions depend on accuracy
3. Do not update `project.md` or `instructions.md` unless identity or core rules change
4. After updates, optionally verify bundle: `uv run python tools/context_pack.py`

## Commit Guidance

Memory updates may ship in the same commit as the feature they describe, or in a follow-up commit. Infrastructure-only memory changes (like this milestone) commit separately from feature work.
