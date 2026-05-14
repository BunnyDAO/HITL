---
id: 0004
title: Multi-template support + template picker
type: AFK
status: done
blocked_by: [0003]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

Extend the skill to support multiple templates. Add the second template (`vision-multi-assert`) which demonstrates Jinja `{% for %}` loops via an `assertions` list.

End-to-end behavior: engineer types `/hitl-test`. The skill discovers templates in `templates/` by reading their frontmatter, lists them via `AskUserQuestion` with each template's `metadata.purpose` as the option description. Engineer picks one. The rest of the flow proceeds as in slice 3, against whichever template was picked.

`vision-multi-assert` lets the engineer build a structured list of assertions during the interrogation — at least one assertion required, with a "add another?" loop until the engineer says stop.

## Acceptance criteria

- [x] Skill auto-discovers templates by scanning `templates/*.py.j2` and reading frontmatter (SKILL.md Step 1)
- [x] First user-facing question is "which template?" with options derived from `metadata.purpose`
- [x] `templates/vision-multi-assert.py.j2` exists with frontmatter declaring list variables. **Note**: sc-compose 1.0.1's var-file format only accepts scalars or scalar arrays — no nested objects. The "list of assertions" is therefore split into two parallel scalar arrays: `assertion_kinds` (list of strings) and `assertion_kwargs` (list of strings, each a Python kwargs fragment). The template uses `loop.index0` to pair them. Workaround documented in the template's `metadata.purpose`.
- [x] Skill's variable-walker handles list-type variables: SKILL.md describes the "parallel-list variables" case where two related lists are collected together via an "add another?" loop
- [x] Rendering `vision-multi-assert` with a 2-item kinds/kwargs pair produces a valid Python file with two assertion calls in sequence — demonstrated via `make demo-multi`
- [x] All slice 3 acceptance criteria still pass for the original `vision-centroid` template — full test suite (24 cases) is green
- [x] Lint test `test_skill_doc_mentions_every_required_variable_across_all_templates` enforces SKILL.md ↔ all templates alignment going forward
- [x] `hitl_lib.assertions.pixel_intensity_above()` added (with 3 unit tests) so the multi-assert template has more than one assertion kind to exercise

## Blocked by

- 0003
