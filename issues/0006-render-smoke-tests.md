---
id: 0006
title: Render-smoke tests for all templates
type: AFK
status: open
blocked_by: [0005]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

Add `tests/test_template_render.py` covering all three templates. For each template, render with a known-valid var set and confirm the output is syntactically valid Python (via `ast.parse`). This catches template-level mistakes (unbalanced braces, malformed Jinja, missing imports) without needing to execute the generated test.

End-to-end behavior: running `pytest tests/test_template_render.py` produces three passing checks — one per template. If anyone edits a template and breaks its rendering, `pytest` fails immediately with a clear error.

## Acceptance criteria

- [ ] `tests/test_template_render.py` exists with one test function per template (parametrized is fine)
- [ ] Each test invokes `sc-compose render` as a subprocess with a known-valid JSON var file, captures stdout, parses it with `ast.parse`
- [ ] A failing case is also covered: rendering with a known-missing required variable raises a clear error from sc-compose, and the test asserts the non-zero exit + the expected stderr substring
- [ ] Test fixtures (the known-valid var sets) live in `tests/fixtures/` as JSON files, not inline in the test code
- [ ] `pytest tests/` (the whole suite, not just `generated/`) exits 0
- [ ] Render-smoke tests run in under 5 seconds total

## Blocked by

- 0005
