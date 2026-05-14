---
id: 0015
title: Docs reorganization — README front door + test-engineer-guide + SOP kit sections
type: HITL
status: open
blocked_by: [0014]
parent: docs/prd/primitives-kit-and-hitl-author.md
---

## What to build

Three coordinated documentation changes so that each audience reads a doc tuned to their vocabulary, and so the entire system (originally three layers; now three layers + primitives kit + two skills) is explained coherently.

`README.md` — rewritten as a short front door. First paragraph names the two audience docs explicitly ("developers, start here; test engineers, start here") and gives the elevator-pitch one-liner. Getting Started section trimmed to a single copy-pasteable block that works for both audiences. No architecture content — that lives in the SOP.

`docs/test-engineer-guide.md` — new document, written entirely in non-programmer language. Audience: a test engineer who has Claude Code installed and the repo cloned but does not read Python. Sections: what this is (one paragraph, no Python jargon), what a primitive is (explained operationally, not mechanically), how to use `/hitl-test` to run an existing test shape, how to use `/hitl-author` to design a new one, what to do when the kit doesn't fit (the request file), how to know your test ran correctly (pass/fail output, the centroid-distance diagnostic in plain English). Pick a single user-facing synonym for "primitive" and stick with it (the PRD suggests "primitives" if explained well, or "building blocks" / "steps" as softer alternatives).

`docs/sop.md` — extended with new sections covering: the primitives kit (what it is, mechanics of `@<primitives/...>` composition, sc-compose's FR-3a merge rule), the `/hitl-author` skill flow + the no-fit case, the review story (PR review described as the operational gate, not enforced in-repo), and a new bullet in the manual walkthrough checklist for verifying `/hitl-author` after edits. Word budget grows from 1154 to ~1700 — still well under any sensible cap.

`docs/deck.md` — unchanged this slice per the PRD's Out of Scope. A follow-up could add one slide for the kit if needed.

## Acceptance criteria

- [ ] `README.md` rewritten: under 80 lines, opens with one elevator-pitch sentence and a two-link "audience? read this" paragraph. Old content moved or removed; no architecture content remains
- [ ] `docs/test-engineer-guide.md` exists, written in non-programmer language throughout — no mentions of Jinja, pytest fixtures, ast.parse, frontmatter syntax, sc-compose CLI flags. Vocabulary picked once and used consistently
- [ ] `docs/sop.md` extended with the four sections above; existing sections preserved
- [ ] The SOP's manual walkthrough checklist gains a step for verifying `/hitl-author` after edits
- [ ] All three audience docs link to each other appropriately — the test-engineer guide links to the SOP for developers reading along, the SOP links to the guide for "what your test engineers see"
- [ ] No internal links break (no references to files that don't exist or paths that moved)
- [ ] Existing `docs/deck.md` is unchanged
- [ ] Full test suite still passes (docs changes shouldn't touch tests, but verify)

## Blocked by

- 0014
