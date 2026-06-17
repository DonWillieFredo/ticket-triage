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

from triage.filters import (
    count_by_priority,
    count_by_trade,
    get_safety_related_work_orders,
    get_vague_or_incomplete_work_orders,
    get_work_orders_by_priority,
    get_work_orders_by_trade,
)
from triage.models import WorkOrder
from triage.samples import WorkOrderSample


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


def load_validated_work_orders(
    path: Path,
) -> tuple[ValidationSummary | None, list[WorkOrderSample]]:
    records = load_records(path)
    summary = validate_records(records)
    if summary.invalid > 0:
        return summary, []
    return None, [record for _, record in records]


def apply_filter(
    work_orders: Iterable[WorkOrderSample],
    *,
    trade: str | None = None,
    priority: str | None = None,
    safety: bool = False,
    incomplete: bool = False,
) -> list[WorkOrderSample]:
    if trade is not None:
        return get_work_orders_by_trade(work_orders, trade)
    if priority is not None:
        return get_work_orders_by_priority(work_orders, priority)
    if safety:
        return get_safety_related_work_orders(work_orders)
    if incomplete:
        return get_vague_or_incomplete_work_orders(work_orders)
    raise ValueError("no filter specified")


def _print_filter_results(
    total: int,
    filter_label: str,
    matches: list[WorkOrderSample],
) -> None:
    print(f"Loaded {total} work order(s).")
    print(f"Filter: {filter_label}")
    print(f"Matches: {len(matches)}")
    for work_order in sorted(matches, key=lambda item: item["id"]):
        print(f"- {work_order['id']}")


def _print_count_results(
    total: int,
    by: str,
    counts: dict[str, int],
) -> None:
    print(f"Loaded {total} work order(s).")
    print(f"Count by: {by}")
    for key in sorted(counts):
        print(f"{key}: {counts[key]}")


def _handle_load_or_validation_failure(
    path: Path,
) -> tuple[int, list[WorkOrderSample]]:
    try:
        summary, work_orders = load_validated_work_orders(path)
    except LoadError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1, []

    if summary is not None:
        _print_summary(summary)
        return 1, []

    return 0, work_orders


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

    filter_parser = subparsers.add_parser(
        "filter",
        help="Filter validated work-order records from a JSON or JSONL file",
    )
    filter_parser.add_argument(
        "path",
        type=Path,
        help="Path to a .json or .jsonl work-order file",
    )
    filter_group = filter_parser.add_mutually_exclusive_group(required=True)
    filter_group.add_argument(
        "--trade",
        metavar="TRADE",
        help="Filter by expected trade (electrical, general, hvac, plumbing)",
    )
    filter_group.add_argument(
        "--priority",
        metavar="PRIORITY",
        help="Filter by expected priority (emergency, urgent, high, medium)",
    )
    filter_group.add_argument(
        "--safety",
        action="store_true",
        help="Filter to work orders with safety notes",
    )
    filter_group.add_argument(
        "--incomplete",
        action="store_true",
        help="Filter to work orders missing location or asset",
    )

    count_parser = subparsers.add_parser(
        "count",
        help="Count validated work-order records from a JSON or JSONL file",
    )
    count_parser.add_argument(
        "path",
        type=Path,
        help="Path to a .json or .jsonl work-order file",
    )
    count_parser.add_argument(
        "--by",
        required=True,
        choices=["trade", "priority"],
        help="Group counts by trade or priority",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code in (0, None) else 1

    if args.command == "validate":
        try:
            records = load_records(args.path)
        except LoadError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        summary = validate_records(records)
        _print_summary(summary)
        return 0 if summary.invalid == 0 else 1

    if args.command == "filter":
        exit_code, work_orders = _handle_load_or_validation_failure(args.path)
        if exit_code != 0:
            return exit_code

        if args.trade is not None:
            filter_label = f"trade={args.trade}"
            matches = apply_filter(work_orders, trade=args.trade)
        elif args.priority is not None:
            filter_label = f"priority={args.priority}"
            matches = apply_filter(work_orders, priority=args.priority)
        elif args.safety:
            filter_label = "safety"
            matches = apply_filter(work_orders, safety=True)
        else:
            filter_label = "incomplete"
            matches = apply_filter(work_orders, incomplete=True)

        _print_filter_results(len(work_orders), filter_label, matches)
        return 0

    if args.command == "count":
        exit_code, work_orders = _handle_load_or_validation_failure(args.path)
        if exit_code != 0:
            return exit_code

        if args.by == "trade":
            counts = count_by_trade(work_orders)
        else:
            counts = count_by_priority(work_orders)

        _print_count_results(len(work_orders), args.by, counts)
        return 0

    parser.error(f"unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
