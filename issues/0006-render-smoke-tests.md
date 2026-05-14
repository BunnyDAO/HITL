---
id: 0006
title: Render-smoke tests for all templates
type: AFK
status: done
blocked_by: [0005]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

Add `tests/test_template_render.py` covering all three templates. For each template, render with a known-valid var set and confirm the output is syntactically valid Python (via `ast.parse`). This catches template-level mistakes (unbalanced braces, malformed Jinja, missing imports) without needing to execute the generated test.

End-to-end behavior: running `pytest tests/test_template_render.py` produces three passing checks — one per template. If anyone edits a template and breaks its rendering, `pytest` fails immediately with a clear error.

## Acceptance criteria

- [x] `tests/test_template_render.py` exists, parametrized across all three renderable templates
- [x] Each test invokes `sc-compose render` as a subprocess with a known-valid JSON var file and parses the output with `ast.parse`
- [x] A failing case is also covered: omits `target_x` from vision-centroid's vars + uses `--strict`; asserts non-zero exit and that stderr mentions `target_x`
- [x] **Deviation from spec**: the JSON var files live at the repo root (`vars.example.json`, `vars.multi-assert.json`, `vars.smoke.json`) rather than `tests/fixtures/`. Reason: they're the same files used by `make demo*` targets; duplicating them would let demo and test reality drift. The test's docstring explains this.
- [x] `pytest tests/` exits 0 (28 tests pass)
- [x] Render-smoke tests run in 0.05s on their own, full suite in 0.18s — well under the 5s budget

## Blocked by

- 0005
