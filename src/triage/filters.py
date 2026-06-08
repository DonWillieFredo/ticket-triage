from collections import Counter
from collections.abc import Iterable

from triage.samples import WorkOrderSample


def get_work_orders_by_trade(
    work_orders: Iterable[WorkOrderSample],
    trade: str,
) -> list[WorkOrderSample]:
    normalized_trade = trade.casefold()

    return [
        work_order
        for work_order in work_orders
        if work_order["expected_trade"].casefold() == normalized_trade
    ]


def get_work_orders_by_priority(
    work_orders: Iterable[WorkOrderSample],
    priority: str,
) -> list[WorkOrderSample]:
    normalized_priority = priority.casefold()

    return [
        work_order
        for work_order in work_orders
        if work_order["expected_priority"].casefold() == normalized_priority
    ]


def get_safety_related_work_orders(
    work_orders: Iterable[WorkOrderSample],
) -> list[WorkOrderSample]:
    return [
        work_order
        for work_order in work_orders
        if len(work_order["safety_notes"]) > 0
    ]


def get_vague_or_incomplete_work_orders(
    work_orders: Iterable[WorkOrderSample],
) -> list[WorkOrderSample]:
    return [
        work_order
        for work_order in work_orders
        if not work_order["location"].strip()
        or not work_order["asset"].strip()
    ]


def count_by_trade(
    work_orders: Iterable[WorkOrderSample],
) -> dict[str, int]:
    return dict(
        Counter(
            work_order["expected_trade"]
            for work_order in work_orders
        )
    )


def count_by_priority(
    work_orders: Iterable[WorkOrderSample],
) -> dict[str, int]:
    return dict(
        Counter(
            work_order["expected_priority"]
            for work_order in work_orders
        )
    )
