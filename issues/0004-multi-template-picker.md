---
id: 0004
title: Multi-template support + template picker
type: AFK
status: open
blocked_by: [0003]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

Extend the skill to support multiple templates. Add the second template (`vision-multi-assert`) which demonstrates Jinja `{% for %}` loops via an `assertions` list.

End-to-end behavior: engineer types `/hitl-test`. The skill discovers templates in `templates/` by reading their frontmatter, lists them via `AskUserQuestion` with each template's `metadata.purpose` as the option description. Engineer picks one. The rest of the flow proceeds as in slice 3, against whichever template was picked.

`vision-multi-assert` lets the engineer build a structured list of assertions during the interrogation — at least one assertion required, with a "add another?" loop until the engineer says stop.

## Acceptance criteria

- [ ] Skill auto-discovers templates by scanning `templates/*.py.j2` and reading frontmatter
- [ ] First user-facing question is "which template?" with options derived from `metadata.purpose`
- [ ] `templates/vision-multi-assert.py.j2` exists with frontmatter declaring `assertions: list` as a required variable
- [ ] Skill's variable-walker handles list-type variables: prompts to add the first item's fields, then loops "add another?" until the engineer declines
- [ ] Rendering `vision-multi-assert` with a 2-item assertions list produces a valid Python file with two assertion calls in sequence
- [ ] All slice 3 acceptance criteria still pass for the original `vision-centroid` template

## Blocked by

- 0003
