---
id: 0009
title: README + pyproject.toml polish
type: AFK
status: done
blocked_by: [0008]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

The closing-polish slice. Top-level `README.md` that points a new arrival at the SOP within 30 seconds of opening the repo, plus minor pyproject/gitignore cleanup so `pip install -e .` works cleanly and the demo output never accidentally lands in git.

End-to-end behavior: a developer who has never seen this repo before can open `README.md`, follow three commands (clone, install, invoke `/hitl-test`), and have a working demo. They then know to go to `docs/sop.md` for depth.

## Acceptance criteria

- [x] `README.md` exists at repo root, 82 lines (under the 250-line budget)
- [x] Opens with a 3-line description ("what this is, what it demonstrates, runs on a laptop")
- [x] "Getting started" section with copy-pasteable `brew install`, venv setup, `pip install -e .`, and `make demo` commands
- [x] Links to `docs/sop.md` (full version) and `docs/deck.md` (10-minute version) in the top paragraph
- [x] "Repo layout" section pointing at `hitl_lib/`, `templates/`, `.claude/skills/hitl-test/`, `docs/`, `issues/`, `tests/`, and noting `tests/generated/` is gitignored demo output
- [x] `pyproject.toml` works — verified by creating a clean venv with `python3.13 -m venv .venv2 && .venv2/bin/pip install -e .` (succeeds; import works; full suite passes)
- [x] `.gitignore` excludes `tests/generated/`, `__pycache__/`, `*.egg-info/`, `.pytest_cache/`, `.venv/`, plus `.DS_Store`, sc-compose's log dir, and the PromptMaxxing stage markers

## Blocked by

- 0008
