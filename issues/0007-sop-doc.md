---
id: 0007
title: SOP doc with architecture diagram + worked transcript
type: HITL
status: done
blocked_by: [0005]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

`docs/sop.md` — the architecture-doc-tone Standard Operating Procedure aimed at developers and dev leads. Single document, readable in 15 minutes, structured so a skimmer can extract the TL;DR and a deep reader gets the full picture.

Required sections (in order):

1. **TL;DR** — 2 paragraphs: what this is, why it exists. A skimmer should be able to decide in 60 seconds whether to read further.
2. **The three layers** — fixture library, sc-compose templates, agent skill. One paragraph per layer plus a mermaid diagram showing how they compose.
3. **Data flow** — mermaid diagram tracing "engineer says X" → agent JSON → sc-compose render → `.py` file → pytest, with each arrow labeled.
4. **What sc-compose contributes** — the constrained-surface-area argument. Why this beats "let the agent write Python freely."
5. **Worked transcript** — verbatim capture of a real `/hitl-test` invocation including the `AskUserQuestion` menus. This section is the doc's most persuasive content; readers who can't run the demo still see what the conversation feels like.
6. **Manual walkthrough checklist** — step-by-step for verifying the skill behaves correctly after edits, since the skill itself isn't unit-testable.
7. **Extending the pattern** — half-page on how a reader would adapt the pattern to a different domain (audio, motion, anything non-vision). No real-hardware content — stays narrow on the pattern per PRD scope.

## Acceptance criteria

- [x] `docs/sop.md` exists with all seven sections in order (TL;DR → The three layers → Data flow → What sc-compose contributes → Worked interaction → Manual walkthrough checklist → Extending the pattern)
- [x] Two mermaid diagrams: a `graph TB` architecture diagram with three nested `subgraph` blocks, and a `sequenceDiagram` data-flow trace from engineer prompt to pytest output
- [x] TL;DR is 2 paragraphs, 149 words (under the 200-word budget)
- [~] Worked-transcript section: **deviation**. The skill cannot be invoked in the current Claude Code session (skills are loaded at session start; `/hitl-test` becomes available only on a fresh session in this repo). The transcript is a faithful representation of what the SKILL.md prescribes — every menu, option, and message corresponds to a specific SKILL.md instruction. A reproduction note in that section points the reader to verify by running the skill themselves.
- [x] No section speculates about real hardware (the Extending section talks about domain replacement, not real-hardware migration)
- [x] Dev-lead audience tone throughout (Python+pytest assumed; no LLM-101 hand-holding)
- [x] Total length 1154 words (under the 1500-word budget)

## Blocked by

- 0005
