---
id: 0008
title: Marp deck (≤12 slides, ≥2 mermaid diagrams)
type: HITL
status: open
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

- [ ] `docs/deck.md` exists with Marp frontmatter (`marp: true`, theme set)
- [ ] At most 12 slides total (count separator lines)
- [ ] At least 2 mermaid diagrams that render natively in Marp
- [ ] No slide is text-only with > 60 words — each slide carries either a diagram, a code snippet, or a tight bullet list
- [ ] `marp docs/deck.md --pdf` produces a clean PDF with no rendering errors
- [ ] Code snippets on slides are real, not pseudocode — copied or trimmed from the actual repo
- [ ] Deck length is presentable in 10 minutes at a normal pace

## Blocked by

- 0007
