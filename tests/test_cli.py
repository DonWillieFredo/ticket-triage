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
