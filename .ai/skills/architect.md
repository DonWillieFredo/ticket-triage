# Skill: Architect

Use this procedure **before** complex or multi-file implementation work.

## Prerequisites

Read project memory in order (see `.ai/context-index.md`):

1. `docs/context/project.md`
2. `docs/context/instructions.md`
3. `docs/context/decisions.md`
4. `docs/context/technical-truths.md`
5. `docs/context/constraints.md`
6. `docs/context/progress.md`
7. `docs/context/next.md`

## Output Template

Produce a written plan with these sections:

### 1. Feature Goal

What specific outcome does this work achieve? Tie it to maintenance triage if applicable.

### 2. Current Project Phase

Which week/phase are we in? What is already built vs. not yet started?

### 3. Constraints

List relevant constraints from `constraints.md` and `instructions.md` (local-first, no excluded tech, tests must pass, etc.).

### 4. Affected Files

Which files will be created or modified? List paths explicitly.

### 5. Implementation Plan

Numbered steps, smallest increment first. Each step should be independently verifiable.

### 6. Testing Plan

What tests will be added or updated? What commands confirm success (`pytest`, `ruff`)?

### 7. Risks

What could go wrong? Scope creep, breaking changes, premature complexity?

### 8. Non-Goals

What is explicitly out of scope for this work?

### 9. Definition of Done

Concrete checklist — e.g., "ruff clean, pytest green, memory files updated if needed."

## When to Skip

Single-file fixes, typo corrections, or changes explicitly scoped by the user do not require a full architect pass. Use judgment.
