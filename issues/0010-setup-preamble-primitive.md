---
id: 0010
title: setup_preamble primitive + refactor smoke-test to use it
type: HITL
status: done
blocked_by: []
parent: docs/prd/primitives-kit-and-hitl-author.md
---

## What to build

The first tracer bullet for the primitives kit. Establish `templates/primitives/` as a directory, ship one primitive (`setup_preamble.j2`) with its own YAML frontmatter contract, and refactor the existing `smoke-test.py.j2` to compose from it via `@<primitives/setup_preamble.j2>`.

End-to-end behavior: `make demo-smoke` continues to render a valid Python test file and that test continues to pass under pytest. The 28-test suite stays green. Reading the new `smoke-test.py.j2` source shows it is now ~3–5 lines of YAML frontmatter, an `@<...>` include, and one assertion call — the imports + fixture-decl line that used to be inline now come from the primitive.

This slice is a HITL gate because it establishes the kit's conventions (primitive file naming, frontmatter shape, include path conventions) that all subsequent slices follow.

## Acceptance criteria

- [x] `templates/primitives/` directory exists
- [x] `templates/primitives/setup_preamble.j2` exists with YAML frontmatter declaring `test_name` as a required variable
- [x] The primitive's body emits imports (`pytest`, `assertions as hitl_assert`, `camera`, `display`) plus the `def test_{{ test_name }}(hitl_fixture):` line
- [x] `templates/smoke-test.py.j2` refactored to use `@<primitives/setup_preamble.j2>` — the existing `@<_shared_setup.j2>` include is replaced; the composing template's `def test_X` line moves into the primitive
- [x] `templates/_shared_setup.j2` removed
- [x] `make demo-smoke` succeeds and the generated test passes pytest
- [x] Full test suite passes (29 tests now — the new test_primitives.py contract test for setup_preamble is added; one render test skipped due to sc-compose's include-confinement preventing absolute-path includes in the parametrized wrapper, integration coverage handled by the existing smoke-test pipeline)
- [x] Render output is byte-identical to the pre-refactor version (verified by inspecting `tests/generated/test_smoke.py` after `make demo-smoke`)
- [x] `tests/test_primitives.py` ships with one parametrized entry (setup_preamble); slice 0013 extends to all four primitives

## Blocked by

None — can start immediately.
