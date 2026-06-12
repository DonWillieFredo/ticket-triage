# Skill: Recover

Use this procedure when tests fail, lint breaks, or an AI session has drifted from project scope.

## Step 1 — Assess State

Run standard recovery commands:

```bash
git status --short
uv run ruff check .
uv run pytest
```

Record what failed and where.

## Step 2 — Classify the Failure

| Symptom | Likely cause | First action |
| ------- | ------------ | ------------ |
| Ruff errors | Style, imports, unused vars | Fix reported issues only |
| Pytest failure | Logic bug or outdated test | Run failing test in isolation |
| Scope drift | AI added excluded tech | Revert or simplify; re-read `instructions.md` |
| Missing context | Stale session | Run `uv run python tools/context_pack.py` |

## Step 3 — Smallest-Change Repair

1. Fix **one problem at a time**
2. Prefer fixing implementation over weakening tests
3. Do not refactor unrelated code during recovery
4. Re-run the failing check after each fix

## Step 4 — Confirm Green

```bash
uv run ruff check .
uv run pytest
git status --short
```

All must pass before continuing feature work.

## Step 5 — Prevent Recurrence

If the failure was caused by scope drift:

- Re-read `docs/context/instructions.md` and `docs/context/constraints.md`
- Update `decisions.md` if a new boundary was clarified
- Note the incident in `recovery.md` if a new recovery pattern emerged

## Reference

Full recovery guidance: [`docs/context/recovery.md`](../../docs/context/recovery.md)
