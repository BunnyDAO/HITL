---
id: 0005
title: Smoke-test template + @<path> include fragment
type: AFK
status: done
blocked_by: [0004]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

Add the third template, `smoke-test.py.j2`, which exists to demonstrate sc-compose's `@<path>` include mechanism — the feature that makes a multi-template catalog scale because templates can share fragments.

End-to-end behavior: the engineer picks `smoke-test` in the skill's template picker, answers a single required variable (`test_name`), and the rendered output is a minimal "device alive" test that imports + uses the fixture via a shared `_shared_setup.j2` fragment referenced with sc-compose's `@<path>` syntax.

The point of this template is the include, not the test logic. The test itself can be trivially shallow (just confirm `hitl_fixture` initializes).

## Acceptance criteria

- [x] `templates/_shared_setup.j2` exists, 3 lines, contains the imports any HITL test needs (`pytest`, `assertions as hitl_assert`, `camera`, `display`). **Note**: original spec said "imports + fixture parameter declaration", but the test function signature varies per test (different `test_name`s) so it can't live in the shared fragment; the `hitl_fixture` parameter is declared in the using-template's `def` line instead.
- [x] `templates/smoke-test.py.j2` exists, declares `test_name` as the only required variable, and uses sc-compose's `@<path>` syntax to include `_shared_setup.j2`
- [x] Rendering `smoke-test` produces a valid Python test file with the fragment's content inlined where the `@<_shared_setup.j2>` reference appeared (verified — fragment's 3 import lines appear inline)
- [x] The generated test passes when run via pytest (`make demo-smoke`)
- [x] Skill's template picker lists all three templates by discovering `templates/*.py.j2` dynamically; `_shared_setup.j2` is excluded by underscore-prefix convention
- [x] No regression: vision-centroid and vision-multi-assert still render and pass (full suite 24 tests green)
- [x] Crucial finding documented in PRD: the include directive is `@<path>` with **literal angle brackets** (parser at `crates/sc-composer/src/include.rs:parse_include_directive` requires `starts_with("@<") && ends_with(">")`). The README's prose example reads ambiguously.

## Blocked by

- 0004
