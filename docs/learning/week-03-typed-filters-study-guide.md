# Week 3 Learning Module — Typed Filters

> **Project:** Ticket-Triage (facilities-maintenance work-order triage)
> **Goal of the week:** Turn static sample data into *queryable, tested triage logic* using small, typed, deterministic functions.
> **Build target:** `src/triage/filters.py`, `tests/test_filters.py`, `docs/learning/week-03.md`

---

## How to use this guide

Read it top to bottom **before** you write `filters.py`. Each concept builds on the one before it. When you reach the build section, you'll already understand *why* every line looks the way it does — which is the whole point of treating this as an apprenticeship instead of a copy-paste session.

There's a 60-second summary right below if you just need a refresher.

---

## TL;DR (60-second version)

This week you write seven small functions that answer real operational questions about maintenance tickets:

| Question | Function |
|---|---|
| Show me all *plumbing* tickets | `get_work_orders_by_trade` |
| Show me all *urgent* tickets | `get_work_orders_by_priority` |
| Show me tickets with *safety* concerns | `get_safety_related_work_orders` |
| Show me tickets too *vague* to route | `get_vague_or_incomplete_work_orders` |
| How many tickets per *trade*? | `count_by_trade` |
| How many tickets per *priority*? | `count_by_priority` |

Each function is **typed** (clear inputs/outputs), **deterministic** (same input → same output, no AI, no randomness), and **tested** (a matching test proves it works). These are the boring, reliable bricks the rest of the project gets built on.

---

## 1. What you're learning

By the end of the week you should be able to:

- Write **single-responsibility functions** that do one clear job.
- Annotate them with **type hints** so your intent is obvious to your editor, your teammates, and your future self.
- Choose the **smallest interface that works** (`Iterable` over `list`).
- Compare messy human text **safely** with `casefold()`.
- Express filtering compactly with **list comprehensions**.
- Summarize data with **`Counter`**.
- Separate **safety-related** and **vague/incomplete** tickets into their own lanes — the seed of safe AI engineering.
- Prove all of it with **tests**.

---

## 2. The big picture

You are moving one rung up a ladder:

```
raw sample data   →   queryable triage logic   →   intelligent routing
  (Week 2)                  (Week 3, here)            (later weeks)
```

`WORK_ORDERS` already exists: a static list of realistic maintenance tickets. On its own, that's just data sitting in a file. This week you give it a *query surface* — functions that can ask and answer operational questions.

Why do this **before** the interesting AI parts? Because every later feature — Pydantic validation, CLI ingestion, a database, an API, LLM-assisted routing — leans on a stable, predictable core. If the deterministic layer is solid and tested, you can add probabilistic AI on top of it with confidence. If it's shaky, every layer above inherits the wobble.

> **Mental model:** deterministic functions are the *spine*. The AI is *muscle* you attach later. You build the spine first.

---

## 3. Concept breakdown

### Concept 1 — Functions as small production tools

A function should do **one clear job**.

```python
def get_work_orders_by_trade(work_orders, trade):
    ...
```

One responsibility: given some work orders and a trade name, return only the matching ones. Writing it once — instead of scattering filter logic across the project — makes it **reusable, testable, debuggable, and stable**. In production, small boring functions are an asset. They reduce chaos.

> **Rule of thumb:** if you struggle to name a function in a few words, it's probably doing too much.

---

### Concept 2 — Type hints

```python
def get_work_orders_by_trade(
    work_orders: Iterable[WorkOrderSample],
    trade: str,
) -> list[WorkOrderSample]:
```

Read this as:

- `work_orders` is something you can loop over, and each item looks like a `WorkOrderSample`.
- `trade` is a string.
- The function returns a **list** of `WorkOrderSample` items.

Type hints don't catch *every* bug, but they make your intent legible to **you, your editor, future teammates, test tools, AI coding assistants, and recruiters reading your code**. For a portfolio, this is the difference between "writing scripts" and "doing typed Python engineering."

> **Tooling note:** type hints become enforceable when you run a checker like `mypy` or `pyright`. Hints alone are documentation; a checker turns them into guardrails.

---

### Concept 3 — `Iterable` vs `list`

You *could* write `work_orders: list[WorkOrderSample]`. Instead use:

```python
work_orders: Iterable[WorkOrderSample]
```

`Iterable` means **"anything Python can loop over"** — a list, a tuple, a generator, and eventually database rows or streamed records. The function shouldn't care *where* the work orders came from, only that it can iterate them.

That's a real engineering habit: **depend on the smallest interface you need.** It keeps the function flexible and decoupled from its callers.

> **Caveat:** a generator can only be consumed once. If a function needs to loop over the input twice, materialize it first (`work_orders = list(work_orders)`) or keep the parameter typed as `Iterable` but be aware of the trade-off. Our filters loop exactly once, so `Iterable` is safe.

---

### Concept 4 — `casefold()` for safer string comparison

Human-entered data is messy. The same trade might arrive as `Plumbing`, `PLUMBING`, or `plumbing`.

Fragile:

```python
work_order["expected_trade"] == trade
```

Robust:

```python
work_order["expected_trade"].casefold() == trade.casefold()
```

`casefold()` normalizes text for **case-insensitive comparison** (and is more aggressive than `lower()` for some non-English characters, which is why it's the preferred choice). In maintenance triage, messy input is the norm, so we build functions that tolerate small variations instead of breaking on them.

> **Going further:** real input also has stray whitespace. Pairing `.strip().casefold()` is a common, cheap defense. This guide keeps `casefold()` to match the build, but `.strip()` is a reasonable addition.

---

### Concept 5 — List comprehensions

```python
return [
    work_order
    for work_order in work_orders
    if work_order["expected_trade"].casefold() == normalized_trade
]
```

Read it as: *"build a new list of each work order whose trade matches."* It's equivalent to the longer loop:

```python
results = []
for work_order in work_orders:
    if work_order["expected_trade"].casefold() == normalized_trade:
        results.append(work_order)
return results
```

Same logic, fewer lines. The comprehension is idiomatic Python and you'll see it everywhere — but you should be comfortable reading and writing **both** forms, because comprehensions stop being readable once the logic gets complicated.

> **When to prefer the loop:** if you'd need nested conditionals, side effects, or more than one `if`/`for`, write the explicit loop. Readability wins.

---

### Concept 6 — `Counter`

```python
from collections import Counter

Counter(["plumbing", "electrical", "plumbing"])
# Counter({'plumbing': 2, 'electrical': 1})
```

`Counter` tallies how often each value appears. In Ticket-Triage it answers *"how many plumbing tickets? how many urgent? how many routine?"* — and the same idea later powers dashboards, eval reports, and operational metrics.

> **Handy methods:** `Counter(...).most_common(3)` gives the top three, and two `Counter`s can be added together to merge tallies.

---

### Concept 7 — Safety-related filtering

```python
get_safety_related_work_orders()
```

This project's core rule:

> **Safety false negatives are the worst failure mode.**

- A **false positive** is annoying: the system flags a ticket as safety-related when it isn't.
- A **false negative** can be dangerous: the system *fails* to flag `"water leaking near electrical panel."`

So even before any LLM exists, we build the habit of pulling safety-related tickets into their **own lane**. The AI comes later; the safety *architecture* starts now. That ordering — safety structure first, intelligence second — is the heart of Applied AI Engineering.

---

### Concept 8 — Vague or incomplete tickets

```python
get_vague_or_incomplete_work_orders()
```

Real work orders often say things like *"It is broken,"* *"Bathroom issue,"* or *"Light not working"* — while missing the **location, asset name, urgency, safety details, or access instructions** needed to route them confidently.

This function teaches a workflow principle that matters enormously later:

> **Not every ticket should be auto-routed. Some need clarification or human review.**

That's the seed of **human-in-the-loop** design. A confident system that knows *when it shouldn't act* is safer than one that always acts.

---

## 4. Why it matters in production

- **Reusability** — one filter, many callers (CLI, API, reports).
- **Testability** — deterministic functions are trivial to assert against.
- **Debuggability** — when something's wrong, you can isolate one small function.
- **Composability** — later features call these instead of reinventing filtering.
- **Trust** — a tested deterministic core lets you add probabilistic AI without losing your footing.

---

## 5. How it connects to facilities maintenance

Maintenance shops live and die by **routing speed and accuracy**. A plumbing ticket sent to an electrician wastes a truck roll. A safety issue lost in the queue is a liability. These filters mirror the real triage desk:

- *By trade* → who gets dispatched.
- *By priority* → what gets done first.
- *Safety lane* → what jumps the queue and gets eyes on it.
- *Vague lane* → what gets a callback before anyone is dispatched.

You're encoding the judgment a good dispatcher already uses — just in a form you can test and scale.

---

## 6. How it prepares us for applied AI engineering

The progression is deliberate:

1. **Deterministic filters (now)** establish the safety and quality *lanes*.
2. **Pydantic models** will validate ticket shape so filters can trust their input.
3. **LLM routing** will later *suggest* a trade/priority — but its suggestions flow through the same safety and human-review lanes you're building today.
4. **Evals** will measure the LLM against the deterministic baseline you've already proven.

In other words: today's "boring" functions are tomorrow's **guardrails and ground truth.**

---

## 7. Files we are changing

| Path | Purpose |
|---|---|
| `src/triage/filters.py` | The seven typed filter/count functions |
| `tests/test_filters.py` | One test per behavior, proving the filters work |
| `docs/learning/week-03.md` | Your learning note (answers to the reflection questions) |

---

## 8. Reference implementation — `filters.py`

> Use this to **check your work** after you've attempted it yourself. Adjust the import for wherever `WorkOrderSample` and `WORK_ORDERS` live in your project. The exact keys (`expected_trade`, `priority`, `is_safety_related`, etc.) should match your Week 2 sample data — rename if yours differ.

```python
"""Typed, deterministic filters for the Ticket-Triage project.

These functions turn the static WORK_ORDERS sample data into queryable
triage logic. They are intentionally small, typed, and side-effect free so
they can serve as a stable foundation for later features (Pydantic models,
CLI ingestion, databases, APIs, and LLM-assisted routing).
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable

# Adjust this import to match your project layout.
from triage.data import WorkOrderSample


def get_work_orders_by_trade(
    work_orders: Iterable[WorkOrderSample],
    trade: str,
) -> list[WorkOrderSample]:
    """Return only the work orders whose expected trade matches `trade`."""
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
    """Return only the work orders whose priority matches `priority`."""
    normalized_priority = priority.casefold()
    return [
        work_order
        for work_order in work_orders
        if work_order["priority"].casefold() == normalized_priority
    ]


def get_safety_related_work_orders(
    work_orders: Iterable[WorkOrderSample],
) -> list[WorkOrderSample]:
    """Return work orders flagged as safety-related.

    Safety false negatives are the worst failure mode, so this lane is kept
    separate from ordinary trade/priority filtering.
    """
    return [
        work_order
        for work_order in work_orders
        if work_order.get("is_safety_related", False)
    ]


def get_vague_or_incomplete_work_orders(
    work_orders: Iterable[WorkOrderSample],
) -> list[WorkOrderSample]:
    """Return work orders that are too vague or incomplete to route confidently.

    These are candidates for clarification or human review rather than
    automatic routing.
    """
    return [
        work_order
        for work_order in work_orders
        if work_order.get("is_vague", False)
    ]


def count_by_trade(
    work_orders: Iterable[WorkOrderSample],
) -> Counter[str]:
    """Count how many work orders belong to each trade."""
    return Counter(
        work_order["expected_trade"].casefold()
        for work_order in work_orders
    )


def count_by_priority(
    work_orders: Iterable[WorkOrderSample],
) -> Counter[str]:
    """Count how many work orders belong to each priority."""
    return Counter(
        work_order["priority"].casefold()
        for work_order in work_orders
    )
```

> **Design note on the "vague" lane:** here it reads a precomputed `is_vague` flag from the sample data, which keeps the function deterministic and testable. If your Week 2 data doesn't carry that flag, a reasonable alternative is a heuristic (e.g. *missing location AND missing asset, or a description under N characters*). Keep the heuristic in one place so it's easy to swap for an LLM later.

---

## 9. Reference tests — `test_filters.py`

```python
"""Tests for the deterministic triage filters."""

from collections import Counter

from triage.filters import (
    count_by_priority,
    count_by_trade,
    get_safety_related_work_orders,
    get_vague_or_incomplete_work_orders,
    get_work_orders_by_priority,
    get_work_orders_by_trade,
)

# A small, explicit fixture so tests don't depend on the full sample set.
SAMPLE = [
    {"id": 1, "expected_trade": "Plumbing", "priority": "urgent",
     "is_safety_related": True, "is_vague": False},
    {"id": 2, "expected_trade": "plumbing", "priority": "routine",
     "is_safety_related": False, "is_vague": False},
    {"id": 3, "expected_trade": "Electrical", "priority": "URGENT",
     "is_safety_related": True, "is_vague": False},
    {"id": 4, "expected_trade": "HVAC", "priority": "routine",
     "is_safety_related": False, "is_vague": True},
]


def test_by_trade_is_case_insensitive():
    results = get_work_orders_by_trade(SAMPLE, "PLUMBING")
    assert [w["id"] for w in results] == [1, 2]


def test_by_trade_no_match_returns_empty():
    assert get_work_orders_by_trade(SAMPLE, "carpentry") == []


def test_by_priority_is_case_insensitive():
    results = get_work_orders_by_priority(SAMPLE, "urgent")
    assert {w["id"] for w in results} == {1, 3}


def test_safety_lane():
    results = get_safety_related_work_orders(SAMPLE)
    assert {w["id"] for w in results} == {1, 3}


def test_vague_lane():
    results = get_vague_or_incomplete_work_orders(SAMPLE)
    assert [w["id"] for w in results] == [4]


def test_count_by_trade():
    assert count_by_trade(SAMPLE) == Counter(
        {"plumbing": 2, "electrical": 1, "hvac": 1}
    )


def test_count_by_priority():
    assert count_by_priority(SAMPLE) == Counter(
        {"urgent": 2, "routine": 2}
    )


def test_filters_accept_any_iterable():
    # A generator is an Iterable but not a list — this proves we depend on
    # the smallest interface we need.
    gen = (w for w in SAMPLE)
    assert len(get_safety_related_work_orders(gen)) == 2
```

> **What these tests prove:** case-insensitivity works, empty results are handled, the safety and vague lanes select the right tickets, counts are correct, and the functions accept *any* iterable (not just lists). That last test is the one that earns the `Iterable` hint.

---

## 10. Commands to run

```bash
# Run the new tests (from the project root)
pytest tests/test_filters.py -v

# Run the whole suite
pytest -v

# Optional but recommended: type-check the filters
mypy src/triage/filters.py
# or
pyright src/triage/filters.py
```

If `pytest` can't find `triage`, make sure your package is importable — typically by installing the project in editable mode (`pip install -e .`) or setting `PYTHONPATH=src`.

---

## 11. Git workflow

Small, labeled commits tell the story of your learning — recruiters and future-you both benefit.

```bash
git checkout -b week-03-typed-filters

# after writing filters.py and test_filters.py
git add src/triage/filters.py tests/test_filters.py
git commit -m "Add typed deterministic triage filters with tests"

# after writing your learning note
git add docs/learning/week-03.md
git commit -m "Add Week 3 learning note: typed filters"

git push -u origin week-03-typed-filters
# open a pull request, let tests run, then merge
```

> **Habit to build:** never commit code without its test in the same (or the very next) commit. The test is what makes the function trustworthy.

---

## 12. Portfolio / README / learning-note update

When this lane is done, update three things:

1. **`docs/learning/week-03.md`** — your answers to the reflection questions, in your own words. This is your study artifact.
2. **README** — add a line to the project's feature list, e.g. *"Deterministic, typed filters for querying work orders by trade, priority, safety, and completeness."*
3. **Portfolio narrative** — one or two sentences you could say in an interview: *"Before adding any AI, I built a tested deterministic core that separates safety-related and ambiguous tickets into their own lanes, so later LLM routing inherits those guardrails."*

---

## 13. Reflection questions (with model answers)

Try to answer each in your own words **first**, then compare. The point is to be able to explain these out loud.

**Q1 — What does `Iterable[WorkOrderSample]` mean?**
It means the parameter is anything you can loop over (list, tuple, generator, future DB rows), where each item has the shape of a `WorkOrderSample`. It's chosen over `list` so the function doesn't care where the data came from — it depends on the smallest interface it needs.

**Q2 — Why `casefold()` instead of direct string comparison?**
Human input is inconsistent in case (`Plumbing`, `PLUMBING`, `plumbing`). `casefold()` normalizes both sides so comparisons are case-insensitive, which makes the filters tolerant of messy real-world data instead of brittle.

**Q3 — What does a list comprehension do?**
It builds a new list in one expression by looping over an iterable and optionally keeping only items that pass a condition. It's a concise, idiomatic equivalent of a `for` loop that appends to a results list.

**Q4 — Why does `get_safety_related_work_orders()` matter for this project?**
Because safety false negatives are the worst failure mode. Putting safety tickets in their own lane — before any AI exists — establishes the safety architecture early, so later automated routing can be layered on without risking missed hazards.

**Q5 — Why are vague/incomplete tickets important in a real triage workflow?**
They can't be routed confidently and would cause bad dispatches if auto-routed. Separating them sets up human-in-the-loop review: the system should know when *not* to act and ask for clarification instead.

**Q6 — What does `Counter` help us summarize?**
It tallies how many tickets fall into each category (per trade, per priority), which feeds operational summaries and later dashboards, metrics, and eval reports.

**Q7 — Why are deterministic filters useful before adding LLMs?**
They're predictable, testable, and reusable — a stable spine. They define the lanes and ground truth that probabilistic AI later plugs into, and they give you a baseline to evaluate the LLM against.

---

## 14. Glossary

- **Deterministic** — same input always produces the same output; no randomness, no AI.
- **Type hint** — an annotation declaring expected types; documentation that a checker can enforce.
- **`Iterable`** — anything you can loop over.
- **`casefold()`** — aggressive case-normalization for safe text comparison.
- **List comprehension** — concise syntax to build a list from a loop + optional filter.
- **`Counter`** — a dict subclass that tallies occurrences.
- **False negative** — the system misses something it should have flagged (the dangerous case here).
- **False positive** — the system flags something it shouldn't have (the annoying case here).
- **Human-in-the-loop** — design where uncertain cases are routed to a person instead of auto-handled.
- **Single responsibility** — one function does one clear job.

---

## 15. Common pitfalls

- **Forgetting to normalize *both* sides** of a comparison — normalize the input *and* the stored value.
- **Consuming a generator twice** — if you must iterate input more than once, call `list()` on it first.
- **Hard-coding `list`** when `Iterable` would do — couples the function to its callers unnecessarily.
- **Writing the function without a test** — an untested filter is an unproven claim.
- **Overstuffing one function** — if it filters *and* counts *and* formats, split it.
- **Testing against the full sample set** — prefer a tiny, explicit fixture so a test failure points to one behavior.

---

## 16. What's next (preview)

With the deterministic spine in place, the natural next lane is **Pydantic models**: replacing the loose `dict`/`TypedDict` shape with validated `WorkOrder` objects so the filters can trust their input. After that come CLI ingestion, persistence, and eventually LLM-assisted routing that flows through the very safety and review lanes you built this week.

---

## Operating agreement (reminder)

Ticket-Triage is a **guided engineering apprenticeship**, not a code-generation session. Each week provides: the learning material, the code steps, the production reasoning, the tests, the Git workflow, the portfolio documentation, and the next logical lane. External resources are optional supplements — **the project is the backbone.**
