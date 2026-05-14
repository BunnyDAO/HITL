---
id: 0013
title: Primitive + composition lint tests + /hitl-test default-template tweak
type: AFK
status: open
blocked_by: [0012]
parent: docs/prd/primitives-kit-and-hitl-author.md
---

## What to build

Two new test files that lock down the kit's contracts, plus a one-line UX fix to `/hitl-test`.

`tests/test_primitives.py` — for each `.j2` file under `templates/primitives/`, asserts the primitive has parseable YAML frontmatter, declares at least one variable (in `required_variables` or `defaults`), and renders to a non-empty fragment when given a known-valid mini-var-set.

`tests/test_composition.py` — for each refactored top-level template, asserts that the render output parses as valid Python (via `ast.parse`) AND that running pytest against it with the existing example var files succeeds. Acts as the explicit post-refactor regression net.

`/hitl-test`'s SKILL.md template-picker rule: change "first alphabetical is Recommended" to "vision-centroid is Recommended when present, otherwise alphabetical-first." Surfaced as a real piece of UX feedback during the slice 0009 end-to-end walkthrough.

## Acceptance criteria

- [ ] `tests/test_primitives.py` exists, parametrized across all 4 primitives, with assertions on frontmatter parseability, variable declaration, and non-empty render output
- [ ] `tests/test_composition.py` exists, parametrized across the 3 refactored top-level templates, asserting `ast.parse` cleanliness and pytest exit-code 0 for each
- [ ] `.claude/skills/hitl-test/SKILL.md` Step 1 instruction updated: vision-centroid is Recommended when present
- [ ] `tests/test_skill_doc.py`'s template-discovery test still passes after the SKILL.md change (no fields lost)
- [ ] Full test suite (now ~32 tests) passes
- [ ] Both new test files run in under 5 seconds total

## Blocked by

- 0012
