# Week 5 Learning Module — CLI Ingestion & Validation

> **Project:** Ticket-Triage (facilities-maintenance work-order triage)
> **Goal of the week:** Build the project's first *external system boundary* — a standard-library CLI that reads work-order files (JSON / JSONL) and validates them through the existing Pydantic `WorkOrder` model.
> **Build target:** `src/triage/cli.py`, `tests/test_cli.py`, `docs/learning/week-05.md`

```
uv run python -m triage.cli validate path/to/work-orders.jsonl
```

---

## How to use this guide

Read it top to bottom **before** you write `cli.py`. Each concept builds on the one before it, and by the build section you'll understand *why* the CLI is split the way it is and why exit codes matter. Same apprenticeship pattern as Weeks 3–4 — the project is the backbone.

There's a 60-second summary right below if you just need a refresher.

---

## TL;DR (60-second version)

Week 4 gave you a validation boundary (`WorkOrder`). This week you put a **door** in front of it: a CLI that loads a file, runs every record through the model, and reports the result in a way both humans *and* automation can act on.

| What | How |
|---|---|
| Read a work-order file | `load_records()` (handles `.json` object, `.json` array, `.jsonl`) |
| Validate each record | `validate_records()` (the Pydantic loop) |
| Define the command | `build_parser()` (argparse `validate` subcommand) |
| Wire it together | `main()` (orchestration + exit codes) |
| Tell the operator what happened | human-readable summary with line/record locations |
| Tell automation what happened | **exit code 0** = safe, **exit code 1** = stop and fix |

The theme: **bad files are caught at the door, deterministically, before anything downstream runs.**

---

## 1. What you're learning

By the end of the week you should be able to:

- Treat **file ingestion as a system boundary** and explain why.
- Structure a CLI with **`argparse` subcommands** using only the standard library.
- Apply **separation of concerns** (load / validate / parse / orchestrate).
- Distinguish a **load error** (bad file) from a **validation error** (bad record).
- Use **exit codes as a contract** that CI and automation can rely on.
- Report errors with **source locations** (`line 2`, `record 3`) plus Pydantic field detail.
- Test a CLI **without shelling out**, using `main([...])` and `capsys`.

---

## 2. The big picture

You're adding a *door* to the boundary you built last week:

```
files / exports / integrations  →  [ CLI DOOR ]  →  [ VALIDATION BOUNDARY ]  →  filters / routing / AI
                                    (Week 5, here)        (Week 4)               (Week 3 + later)
```

Real maintenance data arrives from CSV exports, integrations, mobile apps, and eventually LLM pipelines. Before any routing, filtering, or AI workflow runs, the system needs a **trusted ingestion path** that rejects malformed records early. The CLI is that first door — local, deterministic, and testable.

> **Mental model:** the Pydantic model decides if a *record* is valid; the CLI decides if a *file* is safe to process, and says so in a way a script can check.

---

## 3. Why it matters in production

In facilities operations, bad files are routine:

- a CSV export saved as JSON with the wrong shape
- one blank ticket description in a batch of fifty
- safety notes stored as a string instead of a list
- a truncated file with malformed JSON on line 47

A validation CLI gives operators and engineers a fast way to check a file **before** it enters the workflow. **Exit code 0** means the batch is structurally safe to process. **Exit code 1** means stop and fix the input. That single bit — safe or not — is what makes the tool usable in automation.

---

## 4. Supported input formats

| Format | Meaning |
|---|---|
| `.json` object | one work-order record |
| `.json` array | many work-order records |
| `.jsonl` | one JSON object per line |

---

## 5. CLI behavior (the contract)

- **Exit code 0** when every record validates.
- **Exit code 1** when any record is invalid.
- **Exit code 1** when the file is missing, malformed, unsupported, or contains non-object records.
- A human-readable summary:

```
Validated N work order(s).
Valid: X
Invalid: Y
```

- Invalid records report their **source location** (`line 2`, `record 3`) and the Pydantic field errors.

---

## 6. Concept breakdown

### Concept 1 — `argparse` subcommands

The CLI uses `argparse` with a `validate` subcommand. Subcommands keep the entry point small and leave room for future commands (`filter`, `count`, `ingest`) **without** pulling in Typer or Click. Standard library now; richer frameworks only if a real need appears.

---

### Concept 2 — Separation of concerns

Four functions, four jobs:

| Function | Responsibility |
|---|---|
| `load_records()` | file I/O and format detection |
| `validate_records()` | the Pydantic validation loop |
| `build_parser()` | the CLI definition |
| `main()` | orchestration and exit codes |

This is Week 3's single-responsibility lesson applied at a larger scale. Each piece is independently testable: you can test loading without validating, and validating without touching the filesystem.

---

### Concept 3 — Load errors vs validation errors

Two different failure categories that must not be confused:

- A **load error** means the *file* is wrong — missing, unreadable, malformed JSON, unsupported extension, or a non-object record. The data never even reaches the model.
- A **validation error** means a *record* is wrong — it parsed as JSON but failed the `WorkOrder` model (blank `raw_text`, bad enum, wrong `safety_notes` type, etc.).

Both end in exit code 1, but the messages differ, and keeping them separate keeps the error output honest about *what* went wrong and *where*.

---

### Concept 4 — Exit codes as a contract

Automation and CI rely on exit codes, not on reading prose. A validation failure must **not** surface as a Python traceback — that's an uncontrolled crash. Instead it's a controlled, readable result with a clean exit status. `0` and `1` become a stable promise other tools can build on.

---

### Concept 5 — Testing without shelling out

Tests call `main(["validate", str(path)])` directly and use pytest's `capsys` to capture stdout/stderr. No subprocess, no shell — which keeps tests **fast and deterministic** and lets them assert on both the exit code and the exact summary text.

---

## 7. How it connects to maintenance triage

Before triage logic runs, the system must answer:

- Is this ticket **structurally valid**?
- Does it have a **usable description**?
- Are **safety notes** in the expected shape?
- Are **trade and priority** values from the allowed set?

The CLI answers those questions for file-based batches — the *same* questions an API or LLM pipeline will need to answer later. You're building the muscle once, in the simplest possible context.

---

## 8. Reference implementation — `cli.py`

> Standard library + Pydantic only. Adjust the import to match your project. This follows the four-function split exactly.

```python
"""Command-line ingestion for Ticket-Triage.

Reads work-order records from local JSON or JSONL files and validates them
through the Pydantic WorkOrder model. This is the project's first external
system boundary: nothing downstream runs until a file passes here.

Usage:
    python -m triage.cli validate path/to/work-orders.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from triage.models import WorkOrder


class LoadError(Exception):
    """Raised when a file cannot be read or its shape is unusable.

    Distinct from a Pydantic ValidationError: a LoadError means we never got
    valid per-record data to hand to the model.
    """


def load_records(path: Path) -> list[tuple[str, dict]]:
    """Load (location_label, record) pairs from a JSON or JSONL file.

    - .json  -> a single object, or an array of objects
    - .jsonl -> one JSON object per line

    Raises LoadError for missing files, malformed JSON, unsupported
    extensions, or records that are not JSON objects.
    """
    if not path.exists():
        raise LoadError(f"File not found: {path}")

    suffix = path.suffix.casefold()

    if suffix == ".jsonl":
        records: list[tuple[str, dict]] = []
        for line_number, raw_line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            line = raw_line.strip()
            if not line:
                continue  # tolerate blank lines
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise LoadError(f"Malformed JSON on line {line_number}: {exc}")
            if not isinstance(obj, dict):
                raise LoadError(f"Line {line_number} is not a JSON object")
            records.append((f"line {line_number}", obj))
        return records

    if suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise LoadError(f"Malformed JSON: {exc}")

        if isinstance(data, dict):
            return [("record 1", data)]
        if isinstance(data, list):
            records = []
            for index, obj in enumerate(data, start=1):
                if not isinstance(obj, dict):
                    raise LoadError(f"Record {index} is not a JSON object")
                records.append((f"record {index}", obj))
            return records
        raise LoadError("Top-level JSON must be an object or an array")

    raise LoadError(f"Unsupported file type: {path.suffix}")


def validate_records(
    records: list[tuple[str, dict]],
) -> tuple[list[WorkOrder], list[tuple[str, ValidationError]]]:
    """Validate each record, returning (valid_orders, errors)."""
    valid: list[WorkOrder] = []
    errors: list[tuple[str, ValidationError]] = []
    for location, record in records:
        try:
            valid.append(WorkOrder(**record))
        except ValidationError as exc:
            errors.append((location, exc))
    return valid, errors


def build_parser() -> argparse.ArgumentParser:
    """Define the CLI. Subcommands leave room to grow without Typer/Click."""
    parser = argparse.ArgumentParser(
        prog="triage",
        description="Validate maintenance work-order files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a JSON or JSONL work-order file."
    )
    validate_parser.add_argument("path", type=Path, help="Path to the file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Orchestrate the run and return an exit code (0 = ok, 1 = stop)."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        try:
            records = load_records(args.path)
        except LoadError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        valid, errors = validate_records(records)
        total = len(valid) + len(errors)

        print(f"Validated {total} work order(s).")
        print(f"Valid: {len(valid)}")
        print(f"Invalid: {len(errors)}")

        for location, exc in errors:
            print(f"\n{location}:", file=sys.stderr)
            for err in exc.errors():
                field = ".".join(str(part) for part in err["loc"])
                print(f"  {field}: {err['msg']}", file=sys.stderr)

        return 1 if errors else 0

    return 1  # unreachable while 'validate' is the only subcommand


if __name__ == "__main__":
    raise SystemExit(main())
```

> **Design notes**
> - A dedicated `LoadError` keeps file problems cleanly separate from `ValidationError` — Concept 3 made concrete.
> - Empty/blank JSONL lines are skipped, so an empty file yields zero validated records (and exit code 0).
> - The summary goes to **stdout**; per-record errors go to **stderr**, which is friendlier for piping and logging.
> - `main()` takes `argv` so tests can call it directly instead of shelling out.

---

## 9. Reference tests — `test_cli.py`

```python
"""Tests for the work-order ingestion CLI."""

import json

from triage.cli import main

VALID_RECORD = {
    "id": "WO-1",
    "raw_text": "Leaking pipe under sink",
    "reported_by": "j.smith",
    "created_at": "2025-01-15T09:30:00",
    "expected_trade": "plumbing",
    "expected_priority": "high",
    "safety_notes": [],
}


def write(path, text):
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_jsonl_batch_passes(tmp_path, capsys):
    path = write(tmp_path / "wo.jsonl", json.dumps(VALID_RECORD) + "\n")
    assert main(["validate", str(path)]) == 0
    assert "Valid: 1" in capsys.readouterr().out


def test_invalid_jsonl_reports_line_number(tmp_path, capsys):
    bad = {**VALID_RECORD, "raw_text": "   "}
    path = write(
        tmp_path / "wo.jsonl",
        json.dumps(VALID_RECORD) + "\n" + json.dumps(bad) + "\n",
    )
    assert main(["validate", str(path)]) == 1
    assert "line 2" in capsys.readouterr().err


def test_valid_json_list_passes(tmp_path):
    path = write(tmp_path / "wo.json", json.dumps([VALID_RECORD, VALID_RECORD]))
    assert main(["validate", str(path)]) == 0


def test_valid_json_object_passes(tmp_path):
    path = write(tmp_path / "wo.json", json.dumps(VALID_RECORD))
    assert main(["validate", str(path)]) == 0


def test_malformed_json_fails(tmp_path, capsys):
    path = write(tmp_path / "wo.json", "{not valid json")
    assert main(["validate", str(path)]) == 1
    assert "Error" in capsys.readouterr().err


def test_missing_file_fails(tmp_path, capsys):
    path = tmp_path / "nope.jsonl"
    assert main(["validate", str(path)]) == 1
    assert "not found" in capsys.readouterr().err.casefold()


def test_unsupported_file_type_fails(tmp_path, capsys):
    path = write(tmp_path / "wo.csv", "id,raw_text\n1,broken")
    assert main(["validate", str(path)]) == 1
    assert "unsupported" in capsys.readouterr().err.casefold()


def test_wrong_safety_notes_type_fails(tmp_path):
    bad = {**VALID_RECORD, "safety_notes": "gas smell"}
    path = write(tmp_path / "wo.json", json.dumps(bad))
    assert main(["validate", str(path)]) == 1


def test_blank_raw_text_fails(tmp_path):
    bad = {**VALID_RECORD, "raw_text": ""}
    path = write(tmp_path / "wo.json", json.dumps(bad))
    assert main(["validate", str(path)]) == 1


def test_non_object_jsonl_line_fails(tmp_path, capsys):
    path = write(tmp_path / "wo.jsonl", json.dumps([1, 2, 3]) + "\n")
    assert main(["validate", str(path)]) == 1
    assert "not a json object" in capsys.readouterr().err.casefold()


def test_empty_jsonl_returns_zero_records(tmp_path, capsys):
    path = write(tmp_path / "wo.jsonl", "\n\n")
    assert main(["validate", str(path)]) == 0
    assert "Validated 0 work order(s)." in capsys.readouterr().out
```

> **What these tests prove:** valid JSONL/JSON-array/JSON-object all pass; an invalid record reports its line number; malformed JSON, a missing file, and an unsupported type all fail as *load* errors; wrong type and blank text fail as *validation* errors; a non-object line is rejected; and an empty file is a clean zero-record success. All without spawning a subprocess.

---

## 10. Commands to run

```bash
# Run it for real against a file
uv run python -m triage.cli validate path/to/work-orders.jsonl

# Check the exit code afterward (0 = safe, 1 = stop)
echo $?

# Run the CLI tests
pytest tests/test_cli.py -v

# Whole suite + type check
pytest -v
mypy src/triage/cli.py
```

---

## 11. Git workflow

```bash
git checkout -b week-05-cli-ingestion

git add src/triage/cli.py tests/test_cli.py
git commit -m "Add argparse CLI for JSON/JSONL work-order validation with tests"

git add docs/learning/week-05.md
git commit -m "Add Week 5 learning note: CLI ingestion and validation"

git push -u origin week-05-cli-ingestion
# open a pull request, let tests run, then merge
```

> **Habit to keep:** the CLI and its tests land together. Exit-code behavior is part of the contract, so it must be tested.

---

## 12. Scope intentionally avoided

To keep this lane focused, you did **not** add: FastAPI, database persistence, LLMs or agents, Typer or Click, or any new dependency. Restraint is a design decision — the standard library is enough for a local validation door, and saying "not yet" keeps the project legible.

---

## 13. Portfolio / README / learning-note update

1. **`docs/learning/week-05.md`** — your reflection answers in your own words.
2. **README** — e.g. *"A standard-library CLI validates JSON/JSONL work-order files through the Pydantic model, reporting record-level errors with source locations and returning automation-friendly exit codes."*
3. **Portfolio narrative** — *"I added a local argparse CLI that validates maintenance work-order files through Pydantic models before any API or AI layer exists. It supports JSON and JSONL ingestion, reports record-level validation errors with source locations, and uses exit codes suitable for automation."*

---

## 14. Reflection questions (with model answers)

Answer in your own words first, then compare.

**Q1 — Why is file ingestion a system boundary?**
Because it's where untrusted external data first enters the system. Everything after it can assume well-formed input only if the boundary rejects the rest.

**Q2 — Why use exit codes instead of only printing messages?**
Automation and CI can't reliably parse prose, but they can branch on an exit code. `0`/`1` is a stable machine-readable contract; messages are for humans.

**Q3 — What is the difference between a load error and a validation error?**
A load error means the file itself is wrong (missing, malformed, unsupported, non-object records) and never reaches the model. A validation error means a record parsed fine but failed the `WorkOrder` rules.

**Q4 — Why keep the CLI on the standard library for now?**
`argparse` covers the current need with zero new dependencies. Adding Typer or Click would be weight without benefit until the command surface grows.

**Q5 — How would this CLI fit into a CI pipeline for data imports?**
A pipeline step runs `validate` on the incoming file; exit code 0 lets the import proceed, exit code 1 fails the job and blocks bad data from entering downstream systems.

**Q6 — Why report `line 2` or `record 3` in error output?**
So an operator can find and fix the exact bad record in a large batch instead of guessing which of fifty tickets failed.

**Q7 — What happens when an LLM produces JSON that fails this same validation?**
It's rejected exactly like any malformed file — the same boundary that guards file input will guard AI output, so hallucinated or malformed fields can't slip through.

**Q8 — Why validate before filtering or routing?**
Filters and routers (Week 3) assume clean data. Validating first means they never have to defend against malformed records, keeping each layer simple.

**Q9 — What command would you add next: filter, count, or ingest?**
Any is reasonable; a `filter`/`count` command that runs Week 3's functions on a *validated* file is the most natural next step because it makes the validated data immediately useful.

**Q10 — How does this week connect Week 4 models to real external input?**
Week 4 defined the contract; Week 5 feeds real files into it. The CLI is the first place the validation boundary meets data it didn't create.

---

## 15. Glossary

- **System boundary** — the edge where external, untrusted data enters the system.
- **`argparse`** — the standard-library module for building command-line interfaces.
- **Subcommand** — a named action under one CLI (e.g. `validate`), allowing more later.
- **Load error** — a failure reading or shaping the file, before validation.
- **Validation error** — a record that parsed but failed the Pydantic model.
- **Exit code** — the integer a program returns; `0` = success, non-zero = failure.
- **JSONL** — JSON Lines: one JSON object per line.
- **`capsys`** — a pytest fixture that captures stdout/stderr for assertions.
- **Separation of concerns** — splitting work into focused, independently testable functions.

---

## 16. Common pitfalls

- **Letting a `ValidationError` escape as a traceback** — catch it and return exit code 1 with a readable message.
- **Conflating load and validation errors** — keep the two paths distinct so error output is honest.
- **Forgetting non-object records** — a JSON array of numbers, or a top-level array element that isn't an object, must fail.
- **Writing errors to stdout** — send the summary to stdout and per-record errors to stderr so piping stays clean.
- **Shelling out in tests** — call `main([...])` directly; it's faster and lets you assert on exit codes.
- **Not testing the empty file** — zero records is a valid, exit-code-0 outcome, not a crash.

---

## 17. What's next (preview)

The project now has four layers:

1. realistic sample data (Week 2)
2. deterministic filters (Week 3)
3. validated domain models (Week 4)
4. CLI file ingestion and validation (Week 5)

Natural next steps: add CLI commands that **run the Week 3 filters on a validated file** (`filter` / `count`), or begin moving toward **FastAPI ingestion** in a later phase. Either way, the validation boundary you've now wired to real input is the seam everything plugs into.

---

## Operating agreement (reminder)

Ticket-Triage is a **guided engineering apprenticeship**, not a code-generation session. Each week provides the learning material, the code steps, the production reasoning, the tests, the Git workflow, the portfolio documentation, and the next logical lane. External resources are optional supplements — **the project is the backbone.**
