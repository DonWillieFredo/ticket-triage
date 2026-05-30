# ticket-triage

**AI-powered triage for maintenance work orders — classify, extract, route, and prove it works.**

> **Status:** In active development · Phase 1 of 7 (Modern Python Foundations) · See [Roadmap](#roadmap).

---

## What this is

`ticket-triage` is an AI workflow system for operational teams that run on work orders. It ingests free-text maintenance tickets, classifies them (trade, priority, category), extracts structured fields, applies hard safety rules drawn from real facilities operations, routes uncertain cases to human review, and is measured by an evaluation harness with per-class metrics — not vibes.

It is built to be honest about what it gets right, what it gets wrong, and where humans must stay in the loop.

## The problem

A maintenance team receives a queue of work orders every day. They arrive as messy free text:

> *"Toilet over flowing on 2nd floor near elevator, water everywhere. Pretty bad."*

Before anyone can act, someone has to read it, decide it's plumbing, decide it's urgent, decide if it's safety-related, find the right tech, and route it. That triage step is repetitive, error-prone, and expensive — and the cost of getting it wrong on the *safety-related* dimension is real.

`ticket-triage` automates the routine cases, flags the ambiguous ones for human review, and never auto-routes anything that trips a safety rule.

## How it works

```
incoming ticket (free text)
         │
         ▼
   [ Pydantic validation ]
         │
         ▼
   [ LLM classifier ]        ──▶  trade, priority, confidence
         │
         ▼
   [ LLM field extractor ]   ──▶  location, asset, costs, urgency signals
         │
         ▼
   [ Safety rule engine ]    ──▶  deterministic checks from facilities ops
         │
         ▼
   [ Router ]
      ├──▶  high confidence + safe   →  auto-route to trade
      ├──▶  low confidence           →  human review queue
      └──▶  safety flagged           →  escalate
         │
         ▼
   [ Persistence + audit trail ]
```

Every step's output is a validated Pydantic model. Every decision is logged. Every classification is measurable.

## Tech stack

| Layer            | Tool                                          |
| ---------------- | --------------------------------------------- |
| Language         | Python 3.13+                                  |
| Package manager  | [uv](https://github.com/astral-sh/uv)         |
| Lint & format    | [ruff](https://docs.astral.sh/ruff/)          |
| Type checking    | Pylance / Pyright                             |
| Data modeling    | Pydantic v2                                   |
| Web framework    | FastAPI                                       |
| Persistence      | SQLModel + SQLite (Postgres later)            |
| Testing          | pytest                                        |
| LLM              | Anthropic Claude (tool calling for structured output) |
| Container        | Docker                                        |
| Deployment       | Fly.io                                        |

## Roadmap

Built over 52 weeks across 7 phases:

| Phase | Weeks  | Focus                                | Status            |
| ----- | ------ | ------------------------------------ | ----------------- |
| 1     | 1–8    | Modern Python foundations            | **▶ in progress** |
| 2     | 9–16   | FastAPI backend                      | planned           |
| 3     | 17–24  | LLM, structured output, agent patterns | planned         |
| 4     | 25–36  | Flagship end-to-end                  | planned           |
| 5     | 37–40  | Evaluation harness & reliability     | planned           |
| 6     | 41–44  | Polish, deploy, document             | planned           |
| 7     | 45–52  | Production-readiness                 | planned           |

## Quick start

> Nothing runnable yet — Phase 1 is in progress. The first usable CLI ships at the end of Week 8.

When the time comes:

```bash
git clone git@github.com:DonWillieFredo/ticket-triage.git
cd ticket-triage
uv sync
uv run triage --help
```

## Repository structure

```
ticket-triage/
├── pyproject.toml      # project + dependency declaration
├── uv.lock             # locked exact dependency versions
├── .python-version     # Python version pin
├── main.py             # placeholder (replaced by src/ layout in Week 5)
└── README.md
```

This grows into a proper `src/triage/` package layout in Phase 1 as the data models, ingestion, and CLI come together.

## Why I'm building this

I spent 20+ years in maintenance and facilities operations before transitioning into engineering. I've seen what good and bad work-order triage look like at 6am on a holiday shift with a flooded mechanical room.

Most AI tools in this space are built by engineers who have never carried a radio. This one is built by someone who has — and who understands that *safety-related* is not just another classification label.

The point of this project is not to replace operators. It's to give them better tools, faster, with a system that knows when to ask for help.

## License

MIT (LICENSE file to follow).

## Author

Built by **Will** ([@DonWillieFredo](https://github.com/DonWillieFredo)) as the flagship project of a 12-month transition into AI workflow systems engineering.
