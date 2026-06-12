"""Tests for domain sample work-order data."""

from triage.samples import REQUIRED_FIELDS, WORK_ORDERS


def test_work_orders_count() -> None:
    assert len(WORK_ORDERS) == 20


def test_required_fields_present() -> None:
    for order in WORK_ORDERS:
        for field in REQUIRED_FIELDS:
            assert field in order, f"{order['id']} missing field {field!r}"


def test_ids_are_unique() -> None:
    ids = [order["id"] for order in WORK_ORDERS]
    assert len(ids) == len(set(ids))


def test_at_least_five_have_safety_notes() -> None:
    with_notes = [o for o in WORK_ORDERS if o["safety_notes"]]
    assert len(with_notes) >= 5


def test_at_least_three_vague_or_incomplete() -> None:
    vague = [
        o
        for o in WORK_ORDERS
        if not o["location"].strip() or not o["asset"].strip()
    ]
    assert len(vague) >= 3
