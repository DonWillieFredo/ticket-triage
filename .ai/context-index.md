# AI Context Index — Start Here

**Every AI assistant working in Ticket-Triage must read this file first.**

## Read Order

Load project context in this sequence before planning or implementing:

1. [`docs/context/project.md`](../docs/context/project.md) — Identity, goal, current phase
2. [`docs/context/instructions.md`](../docs/context/instructions.md) — Rules and excluded technologies
3. [`docs/context/decisions.md`](../docs/context/decisions.md) — Durable decisions log
4. [`docs/context/technical-truths.md`](../docs/context/technical-truths.md) — Current codebase facts
5. [`docs/context/constraints.md`](../docs/context/constraints.md) — Hard boundaries
6. [`docs/context/progress.md`](../docs/context/progress.md) — What has shipped
7. [`docs/context/next.md`](../docs/context/next.md) — Immediate next step

## Debugging & Recovery

Read [`docs/context/recovery.md`](../docs/context/recovery.md) when:

- Tests or lint fail
- Scope has drifted
- You need standard recovery commands

## Operating Rules

- **Do not add excluded technologies** — No FastAPI, database, LLMs, agents, MCP, or cloud services unless explicitly allowed.
- **Plan before complex implementation** — Use [`.ai/skills/architect.md`](skills/architect.md) before multi-file or architectural work.
- **Update memory after durable changes** — Use [`.ai/skills/remember.md`](skills/remember.md) when progress, decisions, or technical facts change.

## Skills

| Skill | When to use |
| ----- | ----------- |
| [`architect.md`](skills/architect.md) | Before complex implementation |
| [`review.md`](skills/review.md) | After implementation |
| [`recover.md`](skills/recover.md) | When tests, lint, or scope drift |
| [`remember.md`](skills/remember.md) | After meaningful progress |

## Context Bundle

To print all memory files as one bundle:

```bash
uv run python tools/context_pack.py
```
