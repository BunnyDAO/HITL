---
id: 0008
title: Marp deck (≤12 slides, ≥2 mermaid diagrams)
type: HITL
status: done
blocked_by: [0007]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

`docs/deck.md` — a Marp markdown slide deck that distills the SOP into ~10 minutes of presentation. Source of truth is the SOP; the deck is the compressed version with visuals carrying more of the load.

Required slide arc (suggested ordering — adjust if a different order tells the story better):

1. Title — "Agentic HITL Test Generator"
2. The problem — "non-programmer test engineers can't write code, but they know what to test"
3. The naive approach — "let the agent write Python freely" + why it fails (drift, hidden assumptions, no auditability)
4. The pattern — three-layer architecture diagram (mermaid)
5. Layer 1 — the fixture library (code snippet + role)
6. Layer 2 — sc-compose templates (frontmatter + Jinja code snippet)
7. Layer 3 — the `/hitl-test` agent skill (conversation snippet)
8. Data flow — end-to-end mermaid diagram from engineer prompt to pytest output
9. The "wow moment" — same template, two values of `tolerance_px`, two outcomes
10. What you'd build to adapt this — three bullets, then "questions?"

## Acceptance criteria

- [x] `docs/deck.md` exists with Marp frontmatter (`marp: true`, theme: default, paginate: true)
- [x] 11 slides total — under the 12-slide budget
- [x] Two mermaid diagrams: the three-layer architecture (graph TB) and the data-flow sequence diagram
- [x] No text-only slide exceeds 60 words (max text-only: 60 words on the "domain adaptation" slide; all others under)
- [x] `marp docs/deck.md --pdf` produces a clean PDF with no rendering errors (verified — 11 sections render). **Caveat**: marp doesn't natively render Mermaid to SVG; the diagrams come through as code fences in the PDF. An HTML comment at the top of `docs/deck.md` documents the three viewing options (GitHub web view, marp+mermaid plugin, HTML in Chrome).
- [x] Code snippets are real — trimmed from `hitl_lib/assertions.py`, `templates/vision-centroid.py.j2`, and a faithful representation of `/hitl-test`'s SKILL.md-prescribed conversation
- [x] Deck length is presentable in ~10 minutes (11 slides at ~1 min each)

## Blocked by

- 0007
