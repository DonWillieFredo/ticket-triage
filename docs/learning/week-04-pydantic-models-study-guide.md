# Week 4 Learning Module — Pydantic Models & Validation

> **Project:** Ticket-Triage (facilities-maintenance work-order triage)
> **Goal of the week:** Move from plain dictionaries to *validated domain objects* by putting a Pydantic validation boundary in front of every work order.
> **Build target:** `src/triage/models.py`, `tests/test_models.py`, `docs/learning/week-04.md`

---

## How to use this guide

Read it top to bottom **before** you write `models.py`. Each concept builds on the one before it, and by the build section you'll understand *why* every field, enum, and validator exists. This continues the apprenticeship pattern from Week 3 — the project is the backbone, not a copy-paste session.

There's a 60-second summary right below if you just need a refresher.

---

## TL;DR (60-second version)

Last week you built **deterministic filters** that *trusted* their input. This week you make that trust earned: every ticket passes through a **Pydantic `BaseModel`** that validates it at runtime before anything else touches it.

| What | How |
|---|---|
| Define what a valid ticket looks like | `WorkOrder(BaseModel)` |
| Require core fields | `id`, `raw_text`, `reported_by`, `created_at`, `expected_trade`, `expected_priority` |
| Constrain trades & priorities | `WorkOrderTrade` / `WorkOrderPriority` enums |
| Convert types | `created_at` string → `datetime` |
| Enforce business rules | validators reject blank `id`, `raw_text`, `reported_by` |
| Keep safety signals structured | `safety_notes` is a **list**, not free text |
| Reject surprises | unexpected fields are forbidden |
| Bridge Week 2 data → models | `validate_work_orders` helper |

The theme: **bad input is caught at the boundary, before it can corrupt filters, routing, persistence, APIs, or AI.**

---

## 1. What you're learning

By the end of the week you should be able to:

- Explain the difference between a **`TypedDict`** (editor-time hints) and a **Pydantic `BaseModel`** (runtime validation).
- Define **required fields** and **typed fields** that auto-convert (string → `datetime`).
- Constrain values with **enums** and normalize messy input (uppercase → canonical).
- Write **validators** that enforce business rules (no blank text).
- Keep safety data **structured** rather than buried in prose.
- **Reject unexpected fields** so the system fails loud instead of silent.
- Build a **validation helper** that turns raw sample dicts into trusted domain objects.
- Prove all of it with **tests**.

---

## 2. The big picture

You're adding a *gate* to the ladder you've been climbing:

```
raw data   →   [ VALIDATION BOUNDARY ]   →   filters / routing / storage / AI
 (Week 2)            (Week 4, here)              (Week 3 + later weeks)
```

Maintenance tickets arrive from forms, emails, CSV files, mobile apps, APIs, and eventually LLM output. None of those sources are trustworthy by default. Before the rest of the system processes a ticket, it should pass through **one place** that decides whether the ticket is even well-formed. Pydantic is that place.

> **Mental model:** the model is a *turnstile*. Malformed tickets don't get past it, so nothing downstream ever has to wonder whether its input is sane.

---

## 3. Why it matters in production

In a real facilities environment, bad input produces bad routing — and bad routing wastes truck rolls or, worse, drops a safety issue. Validation catches malformed data **early**, before it spreads. Things that should be caught at the boundary:

- a missing ticket ID
- a blank work description (you can't triage *nothing*)
- a malformed timestamp
- an out-of-range priority value
- safety notes stored as a plain string instead of a list
- unexpected fields sneaking into the system

Catching these here means filters, routing, persistence, the API, and later the AI never have to defend against them individually.

---

## 4. Concept breakdown

### Concept 1 — Pydantic `BaseModel`

A `BaseModel` declares what valid data looks like **and enforces it at runtime**. You construct one from a dict (or keyword args); if the data doesn't fit, Pydantic raises a `ValidationError` describing exactly what's wrong.

```python
from pydantic import BaseModel

class WorkOrder(BaseModel):
    id: str
    raw_text: str
    ...
```

---

### Concept 2 — `BaseModel` vs `TypedDict`

This is the key distinction this week:

| | `TypedDict` | Pydantic `BaseModel` |
|---|---|---|
| When it helps | editing / type-checking | **runtime** |
| Validates real data? | No | **Yes** |
| Converts types? | No | Yes (e.g. `str` → `datetime`) |
| Enforces business rules? | No | Yes (validators) |
| Rejects bad input? | No | Yes (raises `ValidationError`) |

A `TypedDict` is a *promise* about a dict's shape that nothing enforces. A `BaseModel` is a *checkpoint* that actually inspects the data. Week 3's filters assumed clean dicts; Week 4 guarantees them.

---

### Concept 3 — Required fields & typed fields

Fields such as `id`, `raw_text`, `reported_by`, `created_at`, `expected_trade`, and `expected_priority` are **required** — omit one and validation fails. Pydantic also **coerces** types where it's safe: `created_at` arrives as a string and comes out as a Python `datetime`, so the rest of the system works with real datetimes instead of parsing strings everywhere.

---

### Concept 4 — Enums

Trades and priorities are constrained to known values so a typo or a creative entry can't slip in.

```python
class WorkOrderTrade(str, Enum):
    ELECTRICAL = "electrical"
    GENERAL = "general"
    HVAC = "hvac"
    PLUMBING = "plumbing"

class WorkOrderPriority(str, Enum):
    EMERGENCY = "emergency"
    HIGH = "high"
    MEDIUM = "medium"
    URGENT = "urgent"
```

Anything outside these sets is rejected. We also **normalize uppercase input** (`"PLUMBING"` → `plumbing`) so the model tolerates messy casing — the same defensive instinct as Week 3's `casefold()`, applied at the boundary instead of in every filter.

> **Verify against your data:** Week 3 referred to priorities like `urgent`/`routine`, while this module's allowed set is `emergency`/`high`/`medium`/`urgent`. Make sure your enum matches the priority strings actually present in your Week 2 samples, or the helper will reject valid tickets.

---

### Concept 5 — Validators

Type checks alone don't capture *business* rules. A `raw_text` of `""` is a valid string but a useless ticket. Validators close that gap:

```python
@field_validator("id", "raw_text", "reported_by")
@classmethod
def not_blank(cls, value: str) -> str:
    if not value.strip():
        raise ValueError("must not be blank")
    return value
```

This week, `id`, `raw_text`, and `reported_by` may not be blank.

---

### Concept 6 — Structured safety notes

Safety signals must never be buried in free text where a filter or model can't see them. So `safety_notes` is a **list of strings**, not a paragraph:

```python
safety_notes: list[str] = Field(default_factory=list)
```

A plain string passed here **fails validation**. This keeps safety an explicit, queryable field — the runtime enforcement of Week 3's "safety gets its own lane" principle.

---

### Concept 7 — Rejecting unexpected fields

By default Pydantic ignores extra keys. We turn that off so surprises fail loudly:

```python
model_config = ConfigDict(extra="forbid")
```

If a ticket arrives with a field the model doesn't know about, that's a signal something changed upstream — better to halt and notice than to silently drop data.

---

### Concept 8 — The validation helper

`validate_work_orders` is the **bridge** from raw Week 2 sample dicts to validated `WorkOrder` objects:

```python
def validate_work_orders(raw_orders):
    return [WorkOrder(**raw) for raw in raw_orders]
```

One call turns untrusted data into a list of trusted domain objects — the seam every later input path (CLI, API, LLM) will plug into.

---

## 5. How it connects to maintenance triage

A triage system must know a ticket is **structurally valid** before it tries to classify, route, escalate, or store it. The model encodes real-world judgment:

- A **vague location** is *allowed* — vague tickets genuinely happen, and Week 3's "vague lane" exists to handle them.
- A **blank work description** *fails* — you can't triage nothing.
- **Safety notes stay structured** — because safety must not be hidden in prose.

So the model isn't pedantic strictness for its own sake; it allows the messiness that's real and rejects the messiness that's dangerous.

---

## 6. How it prepares us for applied AI

Before any LLM is involved, the system gains a **trusted output shape**. Later, when an LLM extracts fields from messy ticket text, its output is fed through these same models. If the LLM hallucinates a field, returns the wrong type, or invents a priority, **validation catches it** — the AI cannot silently corrupt the workflow.

> Good AI-assisted systems are built on good boring engineering first. The model you write this week is the contract the LLM will later be held to.

---

## 7. Files we are changing

| Path | Purpose |
|---|---|
| `src/triage/models.py` | The `WorkOrder` model, enums, validators, and helper |
| `tests/test_models.py` | Tests proving valid data passes and invalid data fails |
| `docs/learning/week-04.md` | Your learning note (answers to the reflection questions) |

---

## 8. Reference implementation — `models.py`

> Written for **Pydantic v2**. Use it to check your own attempt. Adjust field names to match your Week 2 sample keys (this module names them `expected_trade` / `expected_priority`; confirm yours agree).

```python
"""Pydantic validation models for Ticket-Triage work orders.

This module is the validation boundary: raw, untrusted ticket data is turned
into validated WorkOrder domain objects before any filter, router, store,
API, or LLM step touches it.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WorkOrderTrade(str, Enum):
    ELECTRICAL = "electrical"
    GENERAL = "general"
    HVAC = "hvac"
    PLUMBING = "plumbing"


class WorkOrderPriority(str, Enum):
    EMERGENCY = "emergency"
    HIGH = "high"
    MEDIUM = "medium"
    URGENT = "urgent"


class WorkOrder(BaseModel):
    # Reject any field the model doesn't explicitly declare.
    model_config = ConfigDict(extra="forbid")

    id: str
    raw_text: str
    reported_by: str
    created_at: datetime  # a string like "2025-01-15T09:30:00" is coerced here
    expected_trade: WorkOrderTrade
    expected_priority: WorkOrderPriority

    # Optional: vague tickets happen in real life, so location may be missing.
    location: str | None = None

    # Safety signals stay structured, never buried in free text.
    safety_notes: list[str] = Field(default_factory=list)

    @field_validator("id", "raw_text", "reported_by")
    @classmethod
    def not_blank(cls, value: str) -> str:
        """Required text fields must contain non-whitespace characters."""
        if not value.strip():
            raise ValueError("must not be blank")
        return value

    @field_validator("expected_trade", "expected_priority", mode="before")
    @classmethod
    def normalize_enum_case(cls, value):
        """Normalize messy casing (e.g. 'PLUMBING') before enum coercion."""
        if isinstance(value, str):
            return value.strip().casefold()
        return value


def validate_work_orders(raw_orders) -> list[WorkOrder]:
    """Convert raw sample dictionaries into validated WorkOrder objects.

    This is the bridge from Week 2 sample data to validated domain models.
    Any malformed ticket raises a ValidationError here, at the boundary.
    """
    return [WorkOrder(**raw) for raw in raw_orders]
```

> **Design notes**
> - `safety_notes` defaults to an empty list, but a *plain string* passed in still fails — exactly the behavior we want.
> - `location` is optional on purpose; it's the model-level expression of Week 3's "vague tickets are allowed."
> - The `mode="before"` validator runs *before* enum coercion, which is what lets uppercase input normalize cleanly.

---

## 9. Reference tests — `test_models.py`

```python
"""Tests for the Pydantic work-order models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from triage.models import (
    WorkOrder,
    WorkOrderPriority,
    WorkOrderTrade,
    validate_work_orders,
)


def make_raw(**overrides):
    """A minimal valid raw ticket; override individual fields per test."""
    base = {
        "id": "WO-1",
        "raw_text": "Leaking pipe under sink",
        "reported_by": "j.smith",
        "created_at": "2025-01-15T09:30:00",
        "expected_trade": "plumbing",
        "expected_priority": "high",
        "safety_notes": [],
    }
    base.update(overrides)
    return base


def test_valid_work_order_passes():
    wo = WorkOrder(**make_raw())
    assert wo.id == "WO-1"


def test_timestamp_becomes_datetime():
    wo = WorkOrder(**make_raw())
    assert isinstance(wo.created_at, datetime)


def test_trade_becomes_enum():
    wo = WorkOrder(**make_raw())
    assert wo.expected_trade is WorkOrderTrade.PLUMBING


def test_priority_becomes_enum():
    wo = WorkOrder(**make_raw())
    assert wo.expected_priority is WorkOrderPriority.HIGH


def test_uppercase_enum_is_normalized():
    wo = WorkOrder(**make_raw(expected_trade="PLUMBING"))
    assert wo.expected_trade is WorkOrderTrade.PLUMBING


def test_missing_required_field_fails():
    raw = make_raw()
    del raw["raw_text"]
    with pytest.raises(ValidationError):
        WorkOrder(**raw)


def test_blank_raw_text_fails():
    with pytest.raises(ValidationError):
        WorkOrder(**make_raw(raw_text="   "))


def test_wrong_safety_notes_type_fails():
    with pytest.raises(ValidationError):
        WorkOrder(**make_raw(safety_notes="gas smell"))  # string, not list


def test_unexpected_field_is_rejected():
    with pytest.raises(ValidationError):
        WorkOrder(**make_raw(surprise="???"))


def test_invalid_enum_value_fails():
    with pytest.raises(ValidationError):
        WorkOrder(**make_raw(expected_trade="carpentry"))


def test_validate_work_orders_returns_expected_count():
    raws = [make_raw(id="WO-1"), make_raw(id="WO-2")]
    result = validate_work_orders(raws)
    assert len(result) == 2
    assert all(isinstance(wo, WorkOrder) for wo in result)
```

> **What these tests prove:** valid data passes, types convert (`datetime`, enums), casing normalizes, every failure mode (missing field, blank text, wrong type, bad enum, unexpected field) raises `ValidationError`, and the helper returns the right count of real `WorkOrder` objects.

---

## 10. Commands to run

```bash
# Run the new model tests
pytest tests/test_models.py -v

# Run the whole suite
pytest -v

# Type-check the models
mypy src/triage/models.py
# or
pyright src/triage/models.py
```

If `pydantic` isn't installed yet: `pip install pydantic` (and add it to your project's dependencies / `pyproject.toml`).

---

## 11. Git workflow

```bash
git checkout -b week-04-pydantic-models

git add src/triage/models.py tests/test_models.py
git commit -m "Add Pydantic WorkOrder model with validation and tests"

git add docs/learning/week-04.md
git commit -m "Add Week 4 learning note: Pydantic models and validation"

git push -u origin week-04-pydantic-models
# open a pull request, let tests run, then merge
```

> **Habit to keep:** model and tests land together. A validation model without tests is an unproven contract.

---

## 12. Portfolio / README / learning-note update

1. **`docs/learning/week-04.md`** — your reflection answers in your own words.
2. **README** — e.g. *"Validated domain models (Pydantic) enforce required fields, types, enum constraints, and business rules at the system's input boundary."*
3. **Portfolio narrative** — *"I added Pydantic validation models that moved Ticket-Triage from plain dictionaries to validated domain objects, enforcing required fields, type coercion, enum constraints, and business rules before any API, database, or LLM layer existed — so AI output can later be validated against the same contract."*

---

## 13. Reflection questions (with model answers)

Answer in your own words first, then compare.

**Q1 — What problem does Pydantic solve?**
It validates and converts untrusted data at runtime, so malformed input is caught at the boundary instead of causing failures deep in the system.

**Q2 — How is a `BaseModel` different from a `TypedDict`?**
A `TypedDict` only informs the editor/type-checker and enforces nothing at runtime. A `BaseModel` actually validates real data, coerces types, runs business-rule validators, and raises on bad input.

**Q3 — Why is validation a boundary?**
Because it's the single place data must pass through before the rest of the system trusts it. Everything downstream can assume well-formed input precisely because the boundary rejected the rest.

**Q4 — Why should raw work-order data not be trusted automatically?**
It comes from many uncontrolled sources (forms, email, CSV, mobile, APIs, LLMs), any of which can produce missing, malformed, or unexpected values.

**Q5 — What fields should be required in a maintenance ticket?**
At minimum an identifier, the work description, who reported it, when, and the expected trade and priority — enough to route and act on the ticket.

**Q6 — Why preserve safety notes as structured data?**
So safety signals stay explicit and queryable rather than hidden inside free text, where a filter or router could miss them. Safety false negatives are the worst failure mode.

**Q7 — What kinds of invalid data should fail fast?**
Missing required fields, blank descriptions, malformed timestamps, out-of-range enum values, wrong types (e.g. string for a list field), and unexpected fields.

**Q8 — Why are Pydantic models useful before FastAPI?**
FastAPI uses Pydantic models as request/response schemas, so having the domain model defined and tested first means the API layer drops in with validation already solved.

**Q9 — Why are they useful before LLM structured output?**
An LLM's extracted fields can be validated against the same model, so hallucinated or malformed output is rejected instead of silently corrupting the workflow.

**Q10 — How does this help the project become production-style?**
It establishes a trusted data contract with runtime enforcement, the foundation every production system relies on before adding APIs, persistence, or AI.

---

## 14. Glossary

- **Pydantic** — a Python library that validates and coerces data against typed models at runtime.
- **`BaseModel`** — the Pydantic base class you subclass to define a validated schema.
- **`TypedDict`** — a typing construct describing a dict's shape; checked by tools, not at runtime.
- **Validation boundary** — the single gate untrusted data passes through before the system trusts it.
- **Validator** — a function attached to a model that enforces a business rule beyond simple typing.
- **Coercion** — automatic conversion of a value into the declared type (e.g. string → `datetime`).
- **Enum** — a fixed set of allowed values.
- **`extra="forbid"`** — config that makes unexpected fields raise an error.
- **`ValidationError`** — the exception Pydantic raises when data doesn't fit the model.

---

## 15. Common pitfalls

- **Confusing `TypedDict` with runtime validation** — only Pydantic actually checks data.
- **Leaving `extra` at its default** — unexpected fields get silently ignored unless you `forbid` them.
- **Validating type but not emptiness** — `""` is a valid string; use a validator to reject blanks.
- **Treating safety notes as text** — keep them a list so they stay queryable.
- **Enum mismatch with real data** — confirm your allowed trades/priorities match the actual sample strings.
- **Normalizing case in the wrong place** — use a `mode="before"` validator so it runs before enum coercion.
- **Shipping a model without tests** — an unproven contract is worse than no contract.

---

## 16. What's next (preview)

The next logical lane is **CLI ingestion**. The project now has three solid layers:

1. realistic sample data (Week 2)
2. deterministic filters (Week 3)
3. validated domain models (Week 4)

Next you'll build a small command-line ingestion path that reads raw JSON or JSONL input and runs it through `validate_work_orders` — the first time real external input meets the validation boundary you built this week.

---

## Operating agreement (reminder)

Ticket-Triage is a **guided engineering apprenticeship**, not a code-generation session. Each week provides the learning material, the code steps, the production reasoning, the tests, the Git workflow, the portfolio documentation, and the next logical lane. External resources are optional supplements — **the project is the backbone.**
