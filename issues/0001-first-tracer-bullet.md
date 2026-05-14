---
id: 0001
title: First tracer bullet — hand-rendered test runs end-to-end
type: HITL
status: open
blocked_by: []
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

A working pipeline from a hand-edited variables file → `sc-compose render` → `tests/generated/test_*.py` → `pytest` exit code 0. No Claude Code skill yet; this slice proves the wire is straight before anything agentic is layered on.

End-to-end behavior: from a clean clone, `pip install -r requirements.txt` succeeds. A maintainer runs a documented one-line command (sc-compose CLI with the `vision-centroid` template and a checked-in `vars.example.json`) and gets a syntactically valid Python test file in `tests/generated/`. Running `pytest tests/generated/` against that file passes.

Everything else (other templates, the skill, real assertion math, docs) is out of scope for this slice. The fixture library can be a one-liner that returns canned data — the point is to prove the pipeline, not exercise the assertions.

## Acceptance criteria

- [ ] `pyproject.toml` declares Python 3.11+, package config for `hitl_lib`
- [ ] `requirements.txt` pins `sc-compose` to a specific commit SHA (record the SHA in the file)
- [ ] `hitl_lib/{camera,display,assertions,fixtures}.py` exist with minimal stubs sufficient to import and run one passing test
- [ ] `conftest.py` exposes a `hitl_fixture` pytest fixture
- [ ] `templates/vision-centroid.py.j2` exists with sc-compose frontmatter (`required_variables`, `defaults`, `metadata.purpose`)
- [ ] `vars.example.json` checked in alongside the template
- [ ] One documented shell command produces `tests/generated/test_demo.py`
- [ ] `pytest tests/generated/` exits 0
- [ ] `.gitignore` excludes `tests/generated/` (the demo output should not be committed)

## Blocked by

None — can start immediately.
