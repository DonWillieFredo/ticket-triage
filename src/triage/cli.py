"""Command-line interface for ticket-triage."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from triage.models import WorkOrder


class LoadError(Exception):
    """Raised when a work-order file cannot be loaded."""


@dataclass
class ValidationSummary:
    total: int = 0
    valid: int = 0
    invalid: int = 0
    error_lines: list[str] = field(default_factory=list)


def load_records(path: Path) -> list[tuple[str, dict[str, Any]]]:
    if not path.is_file():
        raise LoadError(f"file not found: {path}")

    suffix = path.suffix.casefold()
    if suffix == ".jsonl":
        return _load_jsonl_records(path)
    if suffix == ".json":
        return _load_json_records(path)

    raise LoadError(f"unsupported file type: {path.suffix or '(no extension)'}")


def _load_jsonl_records(path: Path) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    text = path.read_text(encoding="utf-8")

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue

        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise LoadError(
                f"malformed JSON on line {line_number}: {exc.msg}"
            ) from exc

        if not isinstance(parsed, dict):
            raise LoadError(f"line {line_number}: expected JSON object")

        records.append((f"line {line_number}", parsed))

    return records


def _load_json_records(path: Path) -> list[tuple[str, dict[str, Any]]]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise LoadError(f"malformed JSON: {exc.msg}") from exc

    if isinstance(parsed, dict):
        return [("record 1", parsed)]

    if isinstance(parsed, list):
        records: list[tuple[str, dict[str, Any]]] = []
        for index, item in enumerate(parsed, start=1):
            if not isinstance(item, dict):
                raise LoadError(f"record {index}: expected JSON object")
            records.append((f"record {index}", item))
        return records

    raise LoadError("expected JSON object or array of objects")


def _format_validation_errors(source: str, exc: ValidationError) -> list[str]:
    lines: list[str] = []
    for error in exc.errors():
        field_path = ".".join(str(part) for part in error["loc"])
        lines.append(f"{source}: {field_path}: {error['msg']}")
    return lines


def validate_records(
    records: Iterable[tuple[str, dict[str, Any]]],
) -> ValidationSummary:
    summary = ValidationSummary()

    for source, record in records:
        summary.total += 1
        try:
            WorkOrder.model_validate(record)
        except ValidationError as exc:
            summary.invalid += 1
            summary.error_lines.extend(_format_validation_errors(source, exc))
        else:
            summary.valid += 1

    return summary


def _print_summary(summary: ValidationSummary) -> None:
    print(f"Validated {summary.total} work order(s).")
    print(f"Valid: {summary.valid}")
    print(f"Invalid: {summary.invalid}")
    for line in summary.error_lines:
        print(line)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="triage")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate work-order records from a JSON or JSONL file",
    )
    validate_parser.add_argument(
        "path",
        type=Path,
        help="Path to a .json or .jsonl work-order file",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        try:
            records = load_records(args.path)
        except LoadError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        summary = validate_records(records)
        _print_summary(summary)
        return 0 if summary.invalid == 0 else 1

    parser.error(f"unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
