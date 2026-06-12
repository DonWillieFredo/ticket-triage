# Recovery Notes

Use this when tests fail, lint breaks, or an AI session has drifted from project scope.

## Standard Recovery Commands

Run these first, in order:

```bash
git status --short
uv run ruff check .
uv run pytest
```

## Ruff Failures

1. Read the ruff output — note file and rule (e.g., `F401`, `I001`)
2. Fix only what ruff reports unless the fix reveals a real bug
3. Re-run `uv run ruff check .` until clean
4. Do not disable rules or add `# noqa` unless there is a documented reason

## Pytest Failures

1. Run the failing test in isolation: `uv run pytest tests/test_filters.py::test_name -v`
2. Read the assertion message — compare expected vs actual
3. Determine whether the test or the implementation is wrong
4. Apply the **smallest change** that makes the test pass correctly
5. Re-run full suite: `uv run pytest`

## AI Adding Premature Complexity

If an AI session introduced excluded technology or over-engineered a solution:

1. Check `git status --short` and `git diff` to see what changed
2. Re-read `docs/context/instructions.md` and `docs/context/constraints.md`
3. Revert or simplify changes that violate project rules
4. Re-run ruff and pytest
5. Update `docs/context/decisions.md` if a new boundary was clarified

## Rebuilding Context

When starting a fresh AI session or after a long break:

```bash
uv run python tools/context_pack.py
```

This prints the full Ticket-Triage AI Context Bundle. Paste or reference it at session start, or point the AI to `.ai/context-index.md` for the canonical read order.

## Smallest-Change Repair Principle

When fixing failures:

- Change one thing at a time
- Prefer fixing the implementation over weakening tests
- Do not refactor unrelated code during recovery
- Confirm green status before moving on
