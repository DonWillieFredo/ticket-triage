# Week 6 — CLI Filter and Count Commands

## What we built

This week extended the CLI so validated work-order files can be filtered and summarized from the command line.

Commands:

```bash
uv run python -m triage.cli filter path/to/work-orders.jsonl --trade electrical
uv run python -m triage.cli filter path/to/work-orders.jsonl --priority emergency
uv run python -m triage.cli filter path/to/work-orders.jsonl --safety
uv run python -m triage.cli filter path/to/work-orders.jsonl --incomplete

uv run python -m triage.cli count path/to/work-orders.jsonl --by trade
uv run python -m triage.cli count path/to/work-orders.jsonl --by priority
```

The existing `validate` command is unchanged.

## Big picture

Week 5 added the ingestion boundary: load a file, validate records, report errors.

Week 6 adds the first operational queries on top of that boundary. A facilities lead can now ask:

- Which tickets are electrical?
- Which are emergency priority?
- Which have safety notes?
- Which are vague or incomplete?
- How many tickets per trade or priority?

All answers come from the same deterministic filter logic already tested in `src/triage/filters.py`.

## Why this matters in production

Validation alone is not enough. Operators need to slice a queue before routing work.

In a real maintenance desk:

- electrical emergencies get a different on-call path than general medium-priority tickets
- safety-flagged tickets must not wait behind routine work
- vague tickets need human follow-up before dispatch

The CLI now exposes those operational questions locally, without a database or API.

## Command behavior

### `filter`

1. Load JSON or JSONL file
2. Validate every record through `WorkOrder`
3. Apply one filter: `--trade`, `--priority`, `--safety`, or `--incomplete`
4. Print human-readable summary and matching work-order IDs

Example output:

```text
Loaded 20 work order(s).
Filter: trade=electrical
Matches: 4
- WO-2024-0003
- WO-2024-0007
```

### `count`

1. Load and validate file
2. Group by `--by trade` or `--by priority`
3. Print sorted counts

Example output:

```text
Loaded 20 work order(s).
Count by: trade
electrical: 4
general: 6
hvac: 4
plumbing: 6
```

### Exit codes

- **0** — successful filter or count
- **1** — missing file, malformed JSON, invalid records, or bad CLI arguments

## What I learned

### Reuse over rewrite

`filter` and `count` call the same `load_records()` and `validate_records()` helpers as `validate`, then delegate to `src/triage/filters.py`. The CLI is a thin orchestration layer.

### Validate before query

Filter and count refuse to run on partially invalid files. That keeps behavior honest: you cannot silently query a corrupted batch.

### argparse subcommands scale cleanly

Adding `filter` and `count` subparsers kept Week 5 structure intact. Mutually exclusive filter flags prevent ambiguous queries.

### Testing without subprocesses

Tests call `main(["filter", str(path), "--trade", "electrical"])` directly with `tmp_path` fixtures, same pattern as Week 5.

## Files changed

- `src/triage/cli.py`
- `tests/test_cli.py`
- `docs/learning/week-06.md`

## Tests added

The new CLI tests verify:

- filter by trade, priority, safety, and incomplete
- count by trade and priority
- validation failures block filter/count
- missing files fail with exit 1
- missing required CLI arguments fail with exit 1

## Scope intentionally avoided

We did not add:

- FastAPI
- database persistence
- LLMs or agents
- JSON output mode
- new dependencies

## Portfolio positioning

I extended a local argparse CLI to filter and count validated maintenance work-order files using existing deterministic Python logic. The commands validate input first, report human-readable results, and use exit codes suitable for scripting.

## Reflection questions

1. Why should filter/count validate before querying?
2. What is the difference between `validate` and `filter` in the CLI architecture?
3. Why reuse `filters.py` instead of duplicating logic in the CLI?
4. When would an operator use `--safety` vs `--priority emergency`?
5. Why sort count output alphabetically?
6. What would break if filter ran on invalid records?
7. How does this CLI prepare for a future FastAPI layer?
8. What command might come next: export, route, or review-queue?
9. Why keep output human-readable instead of JSON for now?
10. How does Week 6 connect Week 3 filters to Week 5 file ingestion?

## What comes next

The project now has:

1. realistic sample data
2. deterministic filters
3. validated domain models
4. CLI validate, filter, and count

Next steps may include additional CLI commands, evaluation fixtures, or Phase 2 FastAPI ingestion.
