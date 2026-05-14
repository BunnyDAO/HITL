---
id: 0001
title: First tracer bullet — hand-rendered test runs end-to-end
type: HITL
status: done
blocked_by: []
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

A working pipeline from a hand-edited variables file → `sc-compose render` → `tests/generated/test_*.py` → `pytest` exit code 0. No Claude Code skill yet; this slice proves the wire is straight before anything agentic is layered on.

End-to-end behavior: from a clean clone, `pip install -r requirements.txt` succeeds. A maintainer runs a documented one-line command (sc-compose CLI with the `vision-centroid` template and a checked-in `vars.example.json`) and gets a syntactically valid Python test file in `tests/generated/`. Running `pytest tests/generated/` against that file passes.

Everything else (other templates, the skill, real assertion math, docs) is out of scope for this slice. The fixture library can be a one-liner that returns canned data — the point is to prove the pipeline, not exercise the assertions.

## Acceptance criteria

- [x] `pyproject.toml` declares Python 3.11+, package config for `hitl_lib`
- [x] `requirements.txt` pins Python deps only (`numpy`, `pytest`). sc-compose is a Rust binary installed via `brew install randlee/tap/sc-compose` — documented in the README, not in `requirements.txt`
- [x] `hitl_lib/{camera,display,assertions,fixtures}.py` exist with minimal stubs sufficient to import and run one passing test
- [x] `conftest.py` exposes a `hitl_fixture` pytest fixture (via `hitl_lib.fixtures` registered as a pytest11 entry point so generated tests outside the repo tree still discover it)
- [x] `templates/vision-centroid.py.j2` exists with sc-compose frontmatter (`required_variables`, `defaults`, `metadata.purpose`)
- [x] `vars.example.json` checked in alongside the template
- [x] One documented shell command produces `tests/generated/test_demo.py` — `make demo`, which wraps `sc-compose render --mode file --file templates/vision-centroid.py.j2 --var-file vars.example.json --output tests/generated/test_demo.py`
- [x] `pytest tests/generated/` exits 0 (demonstrated via `make demo`)
- [x] `.gitignore` excludes `tests/generated/` (and `.venv/`, `__pycache__/`, etc.)
- [x] A `tests/test_pipeline.py` integration test executes the full render-then-pytest sequence and asserts exit code 0 (tracer-bullet test; survives refactors)

## Blocked by

None — can start immediately.
