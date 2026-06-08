from triage.filters import (
    count_by_priority,
    count_by_trade,
    get_safety_related_work_orders,
    get_vague_or_incomplete_work_orders,
    get_work_orders_by_priority,
    get_work_orders_by_trade,
)
from triage.samples import WORK_ORDERS


def test_get_work_orders_by_trade_filters_matching_trade() -> None:
    first_work_order = WORK_ORDERS[0]
    trade = first_work_order["expected_trade"]

    results = get_work_orders_by_trade(WORK_ORDERS, trade.upper())

    assert first_work_order in results
    assert all(
        work_order["expected_trade"].casefold() == trade.casefold()
        for work_order in results
    )


def test_get_work_orders_by_priority_filters_matching_priority() -> None:
    first_work_order = WORK_ORDERS[0]
    priority = first_work_order["expected_priority"]

    results = get_work_orders_by_priority(WORK_ORDERS, priority.upper())

    assert first_work_order in results
    assert all(
        work_order["expected_priority"].casefold() == priority.casefold()
        for work_order in results
    )


def test_get_safety_related_work_orders_returns_only_safety_items() -> None:
    results = get_safety_related_work_orders(WORK_ORDERS)

    assert len(results) >= 5
    assert all(work_order["safety_notes"] for work_order in results)


def test_get_vague_or_incomplete_work_orders_returns_missing_location_or_asset() -> None:
    results = get_vague_or_incomplete_work_orders(WORK_ORDERS)

    assert len(results) >= 3
    assert all(
        not work_order["location"].strip()
        or not work_order["asset"].strip()
        for work_order in results
    )


def test_count_by_trade_counts_all_work_orders() -> None:
    results = count_by_trade(WORK_ORDERS)

    assert sum(results.values()) == len(WORK_ORDERS)
    assert all(isinstance(trade, str) for trade in results)
    assert all(isinstance(count, int) for count in results.values())


def test_count_by_priority_counts_all_work_orders() -> None:
    results = count_by_priority(WORK_ORDERS)

    assert sum(results.values()) == len(WORK_ORDERS)
    assert all(isinstance(priority, str) for priority in results)
    assert all(isinstance(count, int) for count in results.values())


def test_filter_functions_handle_empty_input() -> None:
    assert get_work_orders_by_trade([], "plumbing") == []
    assert get_work_orders_by_priority([], "urgent") == []
    assert get_safety_related_work_orders([]) == []
    assert get_vague_or_incomplete_work_orders([]) == []
    assert count_by_trade([]) == {}
    assert count_by_priority([]) == {}
