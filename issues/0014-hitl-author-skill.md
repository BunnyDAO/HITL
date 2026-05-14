---
id: 0014
title: /hitl-author skill v0 (incl. no-fit case → issues/primitive-requests/)
type: HITL
status: done
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

- [x] `.claude/skills/hitl-author/SKILL.md` exists, under the 1200-word read budget (lint enforced)
- [x] SKILL.md instructs the 7-step flow (preflight → name → intent → pick primitives → walk variables → author → optional render)
- [x] SKILL.md mentions every primitive in the kit by stem (lint enforced — drift-protected)
- [x] SKILL.md describes the authoring-trail comment block format and the conventional setup → capture → assertions ordering
- [x] SKILL.md describes the no-fit case and the `issues/primitive-requests/` write
- [x] Engineer-authored template landed end-to-end: `templates/centroid-with-intensity.py.j2` simulates `/hitl-author`'s output with the full authoring-trail comment block, composes 4 primitives, ships `vars.centroid-with-intensity.json`, runs via `make demo-authored`, and is discoverable by `/hitl-test`'s dynamic template-listing
- [x] Authoring-trail comment block survives sc-compose rendering (visible at the top of the rendered Python — confirmed by inspecting `tests/generated/test_authored.py`)
- [x] `tests/test_hitl_author_doc.py` exists with 8 lint tests parallel to `test_skill_doc.py` — covers primitive mentions, request-path mention, AskUserQuestion, conventional order, authoring-trail format, word budget, and cross-reference to `/hitl-test`'s SKILL.md for shared variable-walking spec
- [x] **Drift surfaced + fixed**: the engineer-authored template introduced `intensity_threshold` as a required variable; the existing `test_skill_doc.py` lint caught that `/hitl-test`'s SKILL.md didn't mention it. Added a hint line; lint passes
- [x] Full test suite passes (45 tests + 4 documented skips)
- [x] No regression: `/hitl-test` flow continues to render all four top-level templates (3 original + 1 engineer-authored)

## Blocked by

- 0013
