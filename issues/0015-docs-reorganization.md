---
id: 0015
title: Docs reorganization — README front door + test-engineer-guide + SOP kit sections
type: HITL
status: done
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

- [x] `README.md` rewritten: 79 lines (under 80), opens with one-sentence pitch + a three-option "Pick your path" paragraph (developer, test engineer, presenter). No architecture content remains.
- [x] `docs/test-engineer-guide.md` exists (101 lines, ~1050 words), written in non-programmer language. Avoids Jinja, AST parsing, frontmatter syntax, sc-compose CLI flags. "Primitives = building blocks" introduced once and used consistently.
- [x] `docs/sop.md` extended with: "The primitives kit" (new section with composition mermaid diagram), "Authoring new shapes via /hitl-author" (new section), "The review story" (new section). Layer 2 paragraph updated to describe 4 templates composing from primitives. Word count: 1999.
- [x] SOP's manual walkthrough checklist now has 9 steps (was 6) covering `make demo-authored`, `/hitl-author` end-to-end, and the no-fit case landing in `issues/primitive-requests/`.
- [x] Cross-links: README → SOP + test-engineer-guide + deck; test-engineer-guide → README + SOP. All paths verified.
- [x] `docs/deck.md` unchanged.
- [x] Full test suite (45 tests + 4 documented skips) still passes — no test files touched.

## Blocked by

- 0014
