---
id: 0005
title: Smoke-test template + @<path> include fragment
type: AFK
status: open
blocked_by: [0004]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

Add the third template, `smoke-test.py.j2`, which exists to demonstrate sc-compose's `@<path>` include mechanism — the feature that makes a multi-template catalog scale because templates can share fragments.

End-to-end behavior: the engineer picks `smoke-test` in the skill's template picker, answers a single required variable (`test_name`), and the rendered output is a minimal "device alive" test that imports + uses the fixture via a shared `_shared_setup.j2` fragment referenced with sc-compose's `@<path>` syntax.

The point of this template is the include, not the test logic. The test itself can be trivially shallow (just confirm `hitl_fixture` initializes).

## Acceptance criteria

- [ ] `templates/_shared_setup.j2` exists, ~10 lines max, contains imports + fixture parameter declaration
- [ ] `templates/smoke-test.py.j2` exists, declares `test_name` as the only required variable, and uses sc-compose's `@<path>` syntax to include `_shared_setup.j2`
- [ ] Rendering `smoke-test` produces a valid Python test file with the fragment's content inlined where the `@<path>` reference appeared
- [ ] The generated test passes when run via pytest
- [ ] Skill's template picker lists all three templates; each with its `metadata.purpose` shown
- [ ] No regression: vision-centroid and vision-multi-assert still render and pass

## Blocked by

- 0004
