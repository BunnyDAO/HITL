---
id: 0013
title: Primitive + composition lint tests + /hitl-test default-template tweak
type: AFK
status: done
blocked_by: [0012]
parent: docs/prd/primitives-kit-and-hitl-author.md
---

## What to build

Two new test files that lock down the kit's contracts, plus a one-line UX fix to `/hitl-test`.

`tests/test_primitives.py` — for each `.j2` file under `templates/primitives/`, asserts the primitive has parseable YAML frontmatter, declares at least one variable (in `required_variables` or `defaults`), and renders to a non-empty fragment when given a known-valid mini-var-set.

`tests/test_composition.py` — for each refactored top-level template, asserts that the render output parses as valid Python (via `ast.parse`) AND that running pytest against it with the existing example var files succeeds. Acts as the explicit post-refactor regression net.

`/hitl-test`'s SKILL.md template-picker rule: change "first alphabetical is Recommended" to "vision-centroid is Recommended when present, otherwise alphabetical-first." Surfaced as a real piece of UX feedback during the slice 0009 end-to-end walkthrough.

## Acceptance criteria

- [x] `tests/test_primitives.py` is parametrized across all 4 primitives (extended progressively through #0010–#0012; final entries: setup_preamble, pattern_capture, assert_centroid, assert_intensity). Contract test passes for each; render test skipped via documented include-confinement workaround.
- [x] `tests/test_composition.py` exists, parametrized across the 3 refactored top-level templates, asserting `ast.parse` cleanliness AND pytest exit-code 0 for each
- [x] Bonus test: `test_all_primitives_referenced_by_at_least_one_top_level_template` catches orphaned primitives in the kit
- [x] `.claude/skills/hitl-test/SKILL.md` Step 1 instruction updated: vision-centroid is Recommended when present, otherwise alphabetical-first
- [x] `tests/test_skill_doc.py` still passes after the SKILL.md change
- [x] Full test suite is 36 passing (32 from slices 0010–0012 + 4 new composition tests); 4 render-mode primitive tests skipped due to include-confinement
- [x] All new tests run in under 1s combined

## Blocked by

- 0012
