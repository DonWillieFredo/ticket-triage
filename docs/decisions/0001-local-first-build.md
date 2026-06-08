# ADR 0001: Local-First Build

## Decision

This project will be built locally first using Python, uv, pytest, ruff, and GitHub.

## Reason

The goal is to learn production-style applied AI engineering without introducing cloud complexity too early.

## Consequence

All core logic must run locally before adding hosted deployment.
