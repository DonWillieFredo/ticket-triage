# Project Identity & Goal

## What Ticket-Triage Is

Ticket-Triage is a **local-first Build-and-Learn Applied AI Engineering project** that models real-world maintenance work-order triage. It ingests messy maintenance tickets, applies deterministic rules and (eventually) AI classification, and routes work with safety-first thinking.

The domain is facilities and maintenance operations — work orders, trades, priorities, safety notes, and human-in-the-loop review for ambiguous cases.

## Why It Exists

This project serves three purposes:

1. **Portfolio** — Build a recruiter-friendly, end-to-end AI engineering project grounded in a domain the author knows deeply from 20+ years in facilities and maintenance operations.
2. **Learning** — Follow a Build-and-Learn curriculum: small, testable increments with visible weekly progress.
3. **Honesty** — Model what good triage looks like: deterministic safety rules first, measurable outcomes, and clear human escalation paths.

## Current Foundation

The project is in its **deterministic Python foundation** phase:

- Typed functions and data models
- pytest test coverage
- Sample maintenance work orders
- Filtering and counting logic
- Pydantic validation and CLI workflow coming next

**Not yet in scope:** FastAPI, databases, LLMs, agents, MCP, or cloud services.

## Long-Term Vision

Eventually, Ticket-Triage will classify free-text tickets, extract structured fields, apply safety rules, route uncertain cases to human review, and measure performance with an evaluation harness. That vision starts with a solid, testable, local-first Python core — not premature framework sprawl.
