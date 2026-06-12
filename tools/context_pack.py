"""Bundle Ticket-Triage AI context files for session handover."""

from pathlib import Path

CONTEXT_FILES = [
    "docs/context/project.md",
    "docs/context/instructions.md",
    "docs/context/decisions.md",
    "docs/context/technical-truths.md",
    "docs/context/constraints.md",
    "docs/context/progress.md",
    "docs/context/next.md",
    "docs/context/recovery.md",
]

BUNDLE_HEADER = """\
================================================================================
Ticket-Triage AI Context Bundle
================================================================================
Generated from repo-native project memory. Read top to bottom for full context.
For the canonical read order, see .ai/context-index.md
================================================================================
"""


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _read_context_file(root: Path, relative_path: str) -> str:
    path = root / relative_path
    if not path.is_file():
        return f"[MISSING: {relative_path}]\n"
    return path.read_text(encoding="utf-8")


def main() -> None:
    root = _repo_root()
    print(BUNDLE_HEADER)
    for relative_path in CONTEXT_FILES:
        print(f"# FILE: {relative_path}")
        print("-" * 80)
        content = _read_context_file(root, relative_path)
        print(content, end="" if content.endswith("\n") else "\n")
        print()


if __name__ == "__main__":
    main()
