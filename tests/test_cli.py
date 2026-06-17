"""Tests for the ticket-triage CLI."""

import json

import pytest

from triage.cli import main
from triage.samples import WORK_ORDERS


def _sample_record() -> dict[str, object]:
    return dict(WORK_ORDERS[0])


def test_validate_valid_jsonl(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.jsonl"
    path.write_text(
        json.dumps(_sample_record()) + "\n" + json.dumps(_sample_record()) + "\n",
        encoding="utf-8",
    )

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Validated 2 work order(s)." in captured.out
    assert "Valid: 2" in captured.out
    assert "Invalid: 0" in captured.out


def test_validate_invalid_jsonl_record(tmp_path, capsys) -> None:
    valid = _sample_record()
    invalid = dict(_sample_record())
    invalid["raw_text"] = "   "

    path = tmp_path / "work-orders.jsonl"
    path.write_text(
        json.dumps(valid) + "\n" + json.dumps(invalid) + "\n",
        encoding="utf-8",
    )

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Validated 2 work order(s)." in captured.out
    assert "Valid: 1" in captured.out
    assert "Invalid: 1" in captured.out
    assert "line 2: raw_text:" in captured.out


def test_validate_valid_json_list(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.json"
    path.write_text(
        json.dumps([_sample_record(), _sample_record()]),
        encoding="utf-8",
    )

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Validated 2 work order(s)." in captured.out
    assert "Valid: 2" in captured.out


def test_validate_valid_json_object(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.json"
    path.write_text(json.dumps(_sample_record()), encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Validated 1 work order(s)." in captured.out
    assert "Valid: 1" in captured.out


def test_validate_malformed_json(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.json"
    path.write_text("{not valid json", encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error:" in captured.err
    assert "malformed JSON" in captured.err


def test_validate_missing_file(tmp_path, capsys) -> None:
    path = tmp_path / "missing.jsonl"

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error:" in captured.err
    assert "file not found" in captured.err


def test_validate_unsupported_file_type(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.txt"
    path.write_text("plain text", encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error:" in captured.err
    assert "unsupported file type" in captured.err


def test_validate_wrong_safety_notes_type(tmp_path, capsys) -> None:
    record = dict(_sample_record())
    record["safety_notes"] = "slip hazard near panel"

    path = tmp_path / "work-orders.jsonl"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Invalid: 1" in captured.out
    assert "line 1: safety_notes:" in captured.out


def test_validate_blank_raw_text(tmp_path, capsys) -> None:
    record = dict(_sample_record())
    record["raw_text"] = "   "

    path = tmp_path / "work-orders.json"
    path.write_text(json.dumps(record), encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "record 1: raw_text:" in captured.out


def test_validate_jsonl_non_object_record(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.jsonl"
    path.write_text('["not", "an", "object"]\n', encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "expected JSON object" in captured.err


def test_validate_malformed_jsonl_line(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.jsonl"
    path.write_text("{bad json\n", encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "malformed JSON on line 1" in captured.err


def test_validate_empty_jsonl(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.jsonl"
    path.write_text("", encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Validated 0 work order(s)." in captured.out


@pytest.mark.parametrize(
    ("suffix", "payload"),
    [
        (".json", "[1, 2, 3]"),
        (".json", '"just a string"'),
    ],
)
def test_validate_non_object_json_content(
    tmp_path,
    capsys,
    suffix: str,
    payload: str,
) -> None:
    path = tmp_path / f"work-orders{suffix}"
    path.write_text(payload, encoding="utf-8")

    exit_code = main(["validate", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error:" in captured.err


def _write_jsonl(path, records: list[dict[str, object]]) -> None:
    path.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )


def test_filter_by_trade(tmp_path, capsys) -> None:
    electrical = dict(WORK_ORDERS[2])
    plumbing = dict(WORK_ORDERS[0])
    path = tmp_path / "work-orders.jsonl"
    _write_jsonl(path, [electrical, plumbing, electrical])

    exit_code = main(["filter", str(path), "--trade", "electrical"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Loaded 3 work order(s)." in captured.out
    assert "Filter: trade=electrical" in captured.out
    assert "Matches: 2" in captured.out
    assert f"- {electrical['id']}" in captured.out
    assert f"- {plumbing['id']}" not in captured.out


def test_filter_by_priority(tmp_path, capsys) -> None:
    emergency = dict(WORK_ORDERS[1])
    urgent = dict(WORK_ORDERS[0])
    path = tmp_path / "work-orders.jsonl"
    _write_jsonl(path, [emergency, urgent])

    exit_code = main(["filter", str(path), "--priority", "emergency"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Filter: priority=emergency" in captured.out
    assert "Matches: 1" in captured.out
    assert f"- {emergency['id']}" in captured.out


def test_filter_by_safety(tmp_path, capsys) -> None:
    with_notes = dict(WORK_ORDERS[0])
    without_notes = dict(WORK_ORDERS[8])
    path = tmp_path / "work-orders.jsonl"
    _write_jsonl(path, [with_notes, without_notes])

    exit_code = main(["filter", str(path), "--safety"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Filter: safety" in captured.out
    assert "Matches: 1" in captured.out
    assert f"- {with_notes['id']}" in captured.out


def test_filter_by_incomplete(tmp_path, capsys) -> None:
    incomplete = dict(WORK_ORDERS[8])
    complete = dict(WORK_ORDERS[0])
    path = tmp_path / "work-orders.jsonl"
    _write_jsonl(path, [incomplete, complete])

    exit_code = main(["filter", str(path), "--incomplete"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Filter: incomplete" in captured.out
    assert "Matches: 1" in captured.out
    assert f"- {incomplete['id']}" in captured.out


def test_filter_invalid_record(tmp_path, capsys) -> None:
    valid = _sample_record()
    invalid = dict(_sample_record())
    invalid["raw_text"] = "   "
    path = tmp_path / "work-orders.jsonl"
    _write_jsonl(path, [valid, invalid])

    exit_code = main(["filter", str(path), "--trade", "plumbing"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Invalid: 1" in captured.out


def test_filter_missing_file(tmp_path, capsys) -> None:
    path = tmp_path / "missing.jsonl"

    exit_code = main(["filter", str(path), "--trade", "plumbing"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "file not found" in captured.err


def test_filter_missing_filter_option(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.jsonl"
    _write_jsonl(path, [_sample_record()])

    exit_code = main(["filter", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.err


def test_count_by_trade(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.jsonl"
    _write_jsonl(
        path,
        [dict(WORK_ORDERS[0]), dict(WORK_ORDERS[2]), dict(WORK_ORDERS[2])],
    )

    exit_code = main(["count", str(path), "--by", "trade"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Loaded 3 work order(s)." in captured.out
    assert "Count by: trade" in captured.out
    assert "electrical: 2" in captured.out
    assert "plumbing: 1" in captured.out


def test_count_by_priority(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.json"
    path.write_text(
        json.dumps([dict(WORK_ORDERS[0]), dict(WORK_ORDERS[1])]),
        encoding="utf-8",
    )

    exit_code = main(["count", str(path), "--by", "priority"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Count by: priority" in captured.out
    assert "emergency: 1" in captured.out
    assert "urgent: 1" in captured.out


def test_count_invalid_record(tmp_path, capsys) -> None:
    record = dict(_sample_record())
    record["safety_notes"] = "not a list"
    path = tmp_path / "work-orders.jsonl"
    _write_jsonl(path, [record])

    exit_code = main(["count", str(path), "--by", "trade"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Invalid: 1" in captured.out


def test_count_missing_by_option(tmp_path, capsys) -> None:
    path = tmp_path / "work-orders.jsonl"
    _write_jsonl(path, [_sample_record()])

    exit_code = main(["count", str(path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.err


def test_count_missing_file(tmp_path, capsys) -> None:
    path = tmp_path / "missing.json"

    exit_code = main(["count", str(path), "--by", "priority"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "file not found" in captured.err
