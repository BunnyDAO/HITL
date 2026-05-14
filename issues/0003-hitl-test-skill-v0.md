---
id: 0003
title: /hitl-test skill v0 — one template, full interrogation flow
type: HITL
status: open
blocked_by: [0001]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

The first version of `/hitl-test` as a Claude Code skill. Hardcoded to the `vision-centroid` template for now — multi-template support comes in slice 4. This slice proves the agentic flow end-to-end.

End-to-end behavior: engineer types `/hitl-test` in Claude Code. The skill reads `vision-centroid.py.j2`'s frontmatter, walks `required_variables` one at a time using `AskUserQuestion`, validates by writing variables to a JSON file and invoking `sc-compose render` as a subprocess, writes the output to `tests/generated/test_<test_name>.py`, then asks whether to run pytest. If yes, runs and reports the result.

Failure modes are part of the demo: if sc-compose returns non-zero (e.g. the engineer's variables don't satisfy the contract), the skill surfaces stderr verbatim rather than wrapping the error.

## Acceptance criteria

- [ ] `.claude/skills/hitl-test/SKILL.md` exists and is readable end-to-end in under 5 minutes
- [ ] Skill is invokable via `/hitl-test`
- [ ] Skill uses `AskUserQuestion` for each variable (one structured question per variable, not free-text catch-all)
- [ ] Each question's options include the template's `defaults` value as the recommended option where applicable
- [ ] Free-text user responses for numeric fields are parsed (string `"5"` → int `5`); failures surface a clear message
- [ ] Skill invokes `sc-compose render` as a subprocess with a temp-file var-file
- [ ] Non-zero exit from sc-compose surfaces stderr verbatim to the user
- [ ] Generated file written to `tests/generated/test_<test_name>.py`
- [ ] Final step offers to run `pytest <generated-file>` and reports the result
- [ ] Skill does NOT re-implement sc-compose's validation — only sc-compose decides what's valid

## Blocked by

- 0001
