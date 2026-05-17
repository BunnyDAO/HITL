---
id: 0018
title: SOP domain-example section + kit/checklist table updates for FGR
type: AFK
status: done
blocked_by: [0017]
parent: docs/prd/fgr-uniformity-domain-example.md
---

## What to build

Pure narrative documentation, no code or test impact. Makes the FGR example discoverable and explains it as the canonical Iron-flavored domain example so a teammate reading the SOP understands the pattern in their own vocabulary.

End-state: a reader of `docs/sop.md` finds a section presenting FGR uniformity as the first real domain example (vs. the toy vision primitives), the kit/primitive reference tables list the two new primitives and the `fgr` pattern, and the manual walkthrough checklist includes a `make demo-fgr` step.

## Acceptance criteria

- [x] `docs/sop.md` gains a "Domain example — FGR cross-ROI uniformity" section (what it measures, the metric in prose, why it's the canonical display-metrology example, points at `CONTEXT.md`)
- [x] SOP "What a primitive is" table + the primitives-kit mermaid both list `tile_rois` and `assert_roi_uniformity` with their variable contracts; `fgr` documented as a `display_pattern` option (SKILL.md hints already landed in 0017)
- [x] SOP manual-walkthrough checklist gains a `make demo-fgr` step plus the `vars.fgr-tight.json` fail check; test-count line updated to 62/6
- [x] Friendly register preserved; the engineer-facing portions explain FGR/ROI/uniformity in prose without Jinja/AST/frontmatter jargon
- [x] `CONTEXT.md` referenced ("see `CONTEXT.md` for the canonical glossary"), not duplicated
- [x] `docs/deck.md` left unchanged (PRD-deferred)
- [x] Full suite still passes — **62 passed, 6 skipped**, unchanged by doc edits
- [x] Bonus consistency fix (in scope for a docs slice): README repo-layout updated — adds `fgr-uniformity.py.j2`, the two new primitives, `make demo-fgr`, corrects "4 sub-template fragments"→6 and the stale 45→62 test counts; SOP Layer-2 paragraph and worked-interaction transcript updated four→five templates

## Blocked by

- 0017
