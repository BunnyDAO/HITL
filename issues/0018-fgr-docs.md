---
id: 0018
title: SOP domain-example section + kit/checklist table updates for FGR
type: AFK
status: open
blocked_by: [0017]
parent: docs/prd/fgr-uniformity-domain-example.md
---

## What to build

Pure narrative documentation, no code or test impact. Makes the FGR example discoverable and explains it as the canonical Iron-flavored domain example so a teammate reading the SOP understands the pattern in their own vocabulary.

End-state: a reader of `docs/sop.md` finds a section presenting FGR uniformity as the first real domain example (vs. the toy vision primitives), the kit/primitive reference tables list the two new primitives and the `fgr` pattern, and the manual walkthrough checklist includes a `make demo-fgr` step.

## Acceptance criteria

- [ ] `docs/sop.md` gains a domain-example section presenting `fgr-uniformity` (what it measures, why it's the canonical Iron example, the cross-ROI uniformity metric in prose, pointing at `CONTEXT.md` as the terminology authority)
- [ ] The SOP's primitives/kit table(s) list `tile_rois` and `assert_roi_uniformity` with their variable contracts, and `fgr` as a `pattern_capture` `display_pattern` option
- [ ] The SOP manual-walkthrough checklist gains a `make demo-fgr` step (pass) plus the tight-variant fail check
- [ ] Non-programmer-facing wording stays in the friendly register established for the unified SOP; no Jinja/AST/frontmatter jargon in the engineer-facing portions
- [ ] `CONTEXT.md` is referenced, not duplicated (it remains the single glossary)
- [ ] `docs/deck.md` left unchanged (explicitly deferred in the PRD)
- [ ] Full test suite still passes (doc-only changes shouldn't touch tests, but verify)

## Blocked by

- 0017
