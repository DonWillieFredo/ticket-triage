from collections.abc import Iterable
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from triage.samples import WorkOrderSample


class WorkOrderTrade(StrEnum):
    ELECTRICAL = "electrical"
    GENERAL = "general"
    HVAC = "hvac"
    PLUMBING = "plumbing"


class WorkOrderPriority(StrEnum):
    EMERGENCY = "emergency"
    HIGH = "high"
    MEDIUM = "medium"
    URGENT = "urgent"


class WorkOrder(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    raw_text: str
    reported_by: str
    location: str
    asset: str
    created_at: datetime
    expected_trade: WorkOrderTrade
    expected_priority: WorkOrderPriority
    safety_notes: list[str] = Field(default_factory=list)

    @field_validator("id", "raw_text", "reported_by")
    @classmethod
    def required_text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("field must not be blank")
        return value

    @field_validator("expected_trade", "expected_priority", mode="before")
    @classmethod
    def normalize_enum_text(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.casefold()
        return value


def validate_work_orders(
    work_orders: Iterable[WorkOrderSample],
) -> list[WorkOrder]:
    return [WorkOrder.model_validate(work_order) for work_order in work_orders]
