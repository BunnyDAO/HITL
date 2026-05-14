---
id: 0007
title: SOP doc with architecture diagram + worked transcript
type: HITL
status: open
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

- [ ] `docs/sop.md` exists with all seven sections in order
- [ ] At least two mermaid diagrams (architecture + data flow); both render in standard markdown previewers
- [ ] TL;DR section is exactly 2 paragraphs, under 200 words total
- [ ] Worked-transcript section is captured verbatim from an actual `/hitl-test` run — not paraphrased or fictionalized
- [ ] No section speculates about real hardware, pluggable backends, or productionization (PRD scope says stay narrow)
- [ ] Dev-lead audience tone throughout: assumes Python+pytest knowledge, doesn't over-explain LLM concepts
- [ ] Total length under 1500 words

## Blocked by

- 0005
