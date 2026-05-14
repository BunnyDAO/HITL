---
id: 0009
title: README + pyproject.toml polish
type: AFK
status: open
blocked_by: [0008]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

The closing-polish slice. Top-level `README.md` that points a new arrival at the SOP within 30 seconds of opening the repo, plus minor pyproject/gitignore cleanup so `pip install -e .` works cleanly and the demo output never accidentally lands in git.

End-to-end behavior: a developer who has never seen this repo before can open `README.md`, follow three commands (clone, install, invoke `/hitl-test`), and have a working demo. They then know to go to `docs/sop.md` for depth.

## Acceptance criteria

- [ ] `README.md` exists at repo root
- [ ] README opens with a 3-line description ("what this is, what it demonstrates, why you'd care")
- [ ] README contains a "Getting started" section with the install + invoke commands as copy-pasteable blocks
- [ ] README links to `docs/sop.md` as the next read, and `docs/deck.md` as the 10-minute version
- [ ] README has a "Repo layout" section pointing at `hitl_lib/`, `templates/`, `.claude/skills/hitl-test/`, `docs/`, and noting `tests/generated/` is the demo output
- [ ] `pyproject.toml` declares the project metadata; `pip install -e .` succeeds from a clean venv
- [ ] `.gitignore` excludes `tests/generated/`, `__pycache__/`, `*.egg-info/`, `.pytest_cache/`, `.venv/`
- [ ] Total README length under 250 lines

## Blocked by

- 0008
