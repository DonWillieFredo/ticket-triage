# Week 5 — CLI Ingestion and Validation

## What we built

This week added the first external system boundary: a small standard-library CLI that reads work-order records from local JSON or JSONL files and validates them through the existing Pydantic `WorkOrder` model.

Command:

```bash
uv run python -m triage.cli validate path/to/work-orders.jsonl
```

## Big picture

Real maintenance data arrives from exports, integrations, mobile apps, and eventually LLM pipelines. Before any routing, filtering, or AI workflow runs, the system needs a trusted ingestion path that rejects malformed records early.

The CLI is that first boundary — local, deterministic, and testable.

## Why this matters in production

In facilities operations, bad files are common:

- a CSV export saved as JSON with the wrong shape
- one blank ticket description in a batch of fifty
- safety notes stored as a string instead of a list
- a truncated file with malformed JSON on line 47

A validation CLI gives operators and engineers a fast way to check a file before it enters the workflow. Exit code 0 means the batch is structurally safe to process. Exit code 1 means stop and fix the input.

## Supported input formats

1. **`.json` object** — one work-order record
2. **`.json` array** — many work-order records
3. **`.jsonl`** — one JSON object per line

## CLI behavior

- Exit code **0** when every record validates
- Exit code **1** when any record is invalid
- Exit code **1** when the file is missing, malformed, unsupported, or contains non-object records
- Human-readable summary:

  ```text
  Validated N work order(s).
  Valid: X
  Invalid: Y
  ```

- Invalid records report source location (`line 2`, `record 3`) and Pydantic field errors

## What I learned

### argparse subcommands

The CLI uses `argparse` with a `validate` subcommand. This keeps the entry point small and leaves room for future commands without adding Typer or Click.

### Separation of concerns

- `load_records()` — file I/O and format detection
- `validate_records()` — Pydantic validation loop
- `build_parser()` — CLI definition
- `main()` — orchestration and exit codes

### Testing without shelling out

Tests call `main(["validate", str(path)])` directly and use `capsys` to inspect stdout/stderr. This keeps tests fast and deterministic.

### Exit codes as a contract

Automation and CI can rely on exit codes. A validation failure is not an Python traceback — it is a controlled, readable result.

## How this connects to maintenance triage

Before triage logic runs, the system must answer:

- Is this ticket structurally valid?
- Does it have a usable description?
- Are safety notes in the expected shape?
- Are trade and priority values from the allowed set?

The CLI answers those questions for file-based batches — the same questions an API or LLM pipeline will need later.

## Files changed

- `src/triage/cli.py`
- `tests/test_cli.py`
- `docs/learning/week-05.md`

## Tests added

The CLI tests verify:

- valid JSONL batch passes
- invalid JSONL record fails with line number in output
- valid JSON list passes
- valid JSON object passes
- malformed JSON fails
- missing file fails
- unsupported file type fails
- wrong `safety_notes` type fails
- blank `raw_text` fails
- non-object JSONL line fails
- empty JSONL returns zero validated records

## Scope intentionally avoided

We did not add:

- FastAPI
- database persistence
- LLMs or agents
- Typer or Click
- new dependencies

## Portfolio positioning

I added a local argparse CLI that validates maintenance work-order files through Pydantic models before any API or AI layer exists. The command supports JSON and JSONL ingestion, reports record-level validation errors with source locations, and uses exit codes suitable for automation.

## Reflection questions

1. Why is file ingestion a system boundary?
2. Why use exit codes instead of only printing messages?
3. What is the difference between a load error and a validation error?
4. Why keep the CLI on the standard library for now?
5. How would this CLI fit into a CI pipeline for data imports?
6. Why report `line 2` or `record 3` in error output?
7. What happens when an LLM produces JSON that fails this same validation?
8. Why validate before filtering or routing?
9. What command would you add next: `filter`, `count`, or `ingest`?
10. How does this week connect Week 4 models to real external input?

## What comes next

The project now has:

1. realistic sample data
2. deterministic filters
3. validated domain models
4. CLI file ingestion and validation

Next steps may include CLI commands that run filters on validated files, or moving toward FastAPI ingestion in a later phase.
