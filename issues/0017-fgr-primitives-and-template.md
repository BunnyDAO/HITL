---
id: 0017
title: tile_rois + assert_roi_uniformity primitives + fgr-uniformity template, wired end-to-end
type: AFK
status: open
blocked_by: [0016]
parent: docs/prd/fgr-uniformity-domain-example.md
---

## What to build

The full agentic path for FGR uniformity, end-to-end demoable. Builds on 0016's measurement substrate.

End-to-end behavior: a first-class `fgr-uniformity` template composes `setup_preamble → pattern_capture (display_pattern=fgr) → tile_rois → assert_roi_uniformity`. `make demo-fgr` renders it with `vars.fgr.json` and the generated pytest passes. A tight variant (`max_deviation_pct=2`) renders to a test that fails with the deviation-naming diagnostic — the same tunable wow moment the centroid slice established. Both skills can offer the new shape and its variables.

Only two new primitives. `pattern_capture` is reused unchanged with `display_pattern=fgr` (it is not a third new primitive).

## Acceptance criteria

- [ ] `templates/primitives/tile_rois.j2` declares `grid_rows`, `grid_cols`; emits `rois = roi.tile(image, rows=..., cols=...)`
- [ ] `templates/primitives/assert_roi_uniformity.j2` declares `max_deviation_pct`; emits `hitl_assert.roi_uniformity_within(image, rois, max_deviation_pct=...)`
- [ ] `templates/fgr-uniformity.py.j2` is a first-class template composing the four includes; frontmatter declares the union of required variables (explicit, consistent with other top-level templates)
- [ ] `vars.fgr.json` (e.g. `grid_rows=3`, `grid_cols=3`, `max_deviation_pct=5`) renders to a PASSING test via `make demo-fgr`
- [ ] A tight variant (`max_deviation_pct=2`) renders to a FAILING test whose message names the observed cross-ROI deviation
- [ ] `make demo-fgr` target added to the Makefile
- [ ] `tests/test_primitives.py` extended with parametrized entries for `tile_rois` and `assert_roi_uniformity` (same contract checks as the existing four)
- [ ] `tests/test_composition.py` extended: `fgr-uniformity` renders to valid Python and passes pytest with `vars.fgr.json`
- [ ] Both SKILL.md hint sections (`.claude/skills/hitl-test/SKILL.md`, `.claude/skills/hitl-author/SKILL.md`) learn `grid_rows`, `grid_cols`, `max_deviation_pct`, and `fgr` as a `display_pattern` option
- [ ] `tests/test_skill_doc.py` and `tests/test_hitl_author_doc.py` drift-lints pass (they go red if the SKILL.md hints above are missing — this is why the hint updates are in THIS slice, not the docs slice)
- [ ] Full suite green at the slice boundary (45 prior + new)

## Blocked by

- 0016
