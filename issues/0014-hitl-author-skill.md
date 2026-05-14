---
id: 0014
title: /hitl-author skill v0 (incl. no-fit case → issues/primitive-requests/)
type: HITL
status: open
blocked_by: [0013]
parent: docs/prd/primitives-kit-and-hitl-author.md
---

## What to build

The new Claude Code skill that lets a non-programmer test engineer author a NEW top-level template by picking from the primitives kit. Lives at `.claude/skills/hitl-author/SKILL.md`. Single-stage interrogator (no stage machinery), parallel in shape to `/hitl-test`.

End-to-end behavior: engineer types `/hitl-author`. The skill walks them through:

1. Preflight (sc-compose, `templates/primitives/`, `.venv` exist)
2. Pick a snake_case `test_name` for the new test shape (becomes the new template's filename stem)
3. Describe the test's intent in one line (free text, becomes part of the authoring-trail comment block)
4. Multi-select which primitives the test needs (1–4 picked from the kit)
5. For each variable the picked primitives declare as required (union across all picked primitives, deduplicated), one structured `AskUserQuestion`
6. Skill writes the new template to `templates/<test_name>.py.j2` containing: YAML frontmatter (required_variables union, metadata.purpose from the intent), an authoring-trail comment block at the top (timestamp, author email, intent, primitives picked in order), and a body that is `@<primitives/...>` includes in conventional order (setup → capture → assertions)
7. Offer to render the new template immediately via the same flow `/hitl-test` would use; show the engineer the rendered output and pytest result

No-fit case: if the engineer indicates none of the offered primitives match their intent (via "Other" → "none of these fit"), the skill writes `issues/primitive-requests/<test_name>-<YYYY-MM-DD>.md` describing the engineer's intent, what primitives were available, and what API surface would be needed. Exits cleanly without writing a template.

A lint test guards drift between SKILL.md and the primitives kit, parallel to `tests/test_skill_doc.py`.

## Acceptance criteria

- [ ] `.claude/skills/hitl-author/SKILL.md` exists, readable end-to-end in under 5 minutes (lint enforced under 1200 words)
- [ ] SKILL.md instructs the agent on the 7-step flow described above
- [ ] SKILL.md mentions every primitive in the kit by stem (lint-enforced)
- [ ] SKILL.md describes the authoring-trail comment block format and the conventional primitive ordering
- [ ] SKILL.md describes the no-fit case and the `issues/primitive-requests/` write
- [ ] A new template authored end-to-end by simulating `/hitl-author` lands in `templates/`, is discoverable by `/hitl-test`, and renders+passes via existing flow
- [ ] An engineer-authored template's authoring-trail comment block survives sc-compose rendering (the comment block appears at the top of the rendered Python output)
- [ ] `tests/test_hitl_author_doc.py` exists with parallel structure to `tests/test_skill_doc.py` — asserts SKILL.md mentions each primitive, references the `issues/primitive-requests/` path, instructs `AskUserQuestion`, and stays under the read budget
- [ ] Full test suite passes (now ~35 tests)
- [ ] No regression: `/hitl-test` flow continues to work for the three existing templates plus any engineer-authored template

## Blocked by

- 0013
