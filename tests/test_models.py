from datetime import datetime

import pytest
from pydantic import ValidationError

from triage.models import (
    WorkOrder,
    WorkOrderPriority,
    WorkOrderTrade,
    validate_work_orders,
)
from triage.samples import WORK_ORDERS


def test_all_sample_work_orders_validate() -> None:
    validated = validate_work_orders(WORK_ORDERS)

    assert len(validated) == len(WORK_ORDERS)
    assert all(isinstance(work_order, WorkOrder) for work_order in validated)


def test_created_at_is_parsed_as_datetime() -> None:
    work_order = WorkOrder.model_validate(WORK_ORDERS[0])

    assert isinstance(work_order.created_at, datetime)


def test_expected_trade_is_work_order_trade_enum() -> None:
    work_order = WorkOrder.model_validate(WORK_ORDERS[0])

    assert isinstance(work_order.expected_trade, WorkOrderTrade)


def test_expected_priority_is_work_order_priority_enum() -> None:
    work_order = WorkOrder.model_validate(WORK_ORDERS[0])

    assert isinstance(work_order.expected_priority, WorkOrderPriority)


def test_missing_required_field_fails_validation() -> None:
    sample = dict(WORK_ORDERS[0])
    del sample["id"]

    with pytest.raises(ValidationError):
        WorkOrder.model_validate(sample)


def test_blank_raw_text_fails_validation() -> None:
    sample = dict(WORK_ORDERS[0])
    sample["raw_text"] = "   "

    with pytest.raises(ValidationError):
        WorkOrder.model_validate(sample)


def test_wrong_safety_notes_type_fails_validation() -> None:
    sample = dict(WORK_ORDERS[0])
    sample["safety_notes"] = "water near electrical panel"

    with pytest.raises(ValidationError):
        WorkOrder.model_validate(sample)


def test_validation_helper_returns_same_count_as_input() -> None:
    validated = validate_work_orders(WORK_ORDERS)

    assert len(validated) == len(WORK_ORDERS)


def test_enum_normalization_handles_uppercase_values() -> None:
    sample = dict(WORK_ORDERS[0])
    sample["expected_trade"] = "HVAC"
    sample["expected_priority"] = "HIGH"

    work_order = WorkOrder.model_validate(sample)

    assert work_order.expected_trade == WorkOrderTrade.HVAC
    assert work_order.expected_priority == WorkOrderPriority.HIGH


def test_extra_fields_fail_validation() -> None:
    sample = dict(WORK_ORDERS[0])
    sample["unexpected_field"] = "should not be accepted"

    with pytest.raises(ValidationError):
        WorkOrder.model_validate(sample)
