---
id: 0017
title: tile_rois + assert_roi_uniformity primitives + fgr-uniformity template, wired end-to-end
type: AFK
status: done
blocked_by: [0016]
parent: docs/prd/fgr-uniformity-domain-example.md
---

## What to build

The full agentic path for FGR uniformity, end-to-end demoable. Builds on 0016's measurement substrate.

End-to-end behavior: a first-class `fgr-uniformity` template composes `setup_preamble → pattern_capture (display_pattern=fgr) → tile_rois → assert_roi_uniformity`. `make demo-fgr` renders it with `vars.fgr.json` and the generated pytest passes. A tight variant (`max_deviation_pct=2`) renders to a test that fails with the deviation-naming diagnostic — the same tunable wow moment the centroid slice established. Both skills can offer the new shape and its variables.

Only two new primitives. `pattern_capture` is reused unchanged with `display_pattern=fgr` (it is not a third new primitive).

## Acceptance criteria

- [x] `templates/primitives/tile_rois.j2` declares `grid_rows`, `grid_cols`; emits `rois = roi.tile(image, rows=..., cols=...)`
- [x] `templates/primitives/assert_roi_uniformity.j2` declares `max_deviation_pct`; emits `hitl_assert.roi_uniformity_within(image, rois, max_deviation_pct=...)`
- [x] `templates/fgr-uniformity.py.j2` is a first-class template composing the four includes; frontmatter declares the union of required variables explicitly (consistent with vision-centroid)
- [x] `vars.fgr.json` (`grid_rows=3`, `grid_cols=3`, `max_deviation_pct=5`) renders to a PASSING test via `make demo-fgr`
- [x] `vars.fgr-tight.json` (`max_deviation_pct=2`) renders to a FAILING test: `cross-ROI uniformity deviation was 3.64% (brightest ROI mean 126.26, dimmest 121.66); tolerance was 2%`
- [x] `make demo-fgr` target added (+ `.PHONY` updated)
- [x] `tests/test_primitives.py` extended with `tile_rois` + `assert_roi_uniformity` entries (contract test passes; render test skipped per the documented include-confinement convention)
- [x] `tests/test_composition.py` extended: `fgr-uniformity` renders, ast.parses, pytest-passes with `vars.fgr.json`; the orphan-primitive check now sees both new primitives referenced
- [x] Both SKILL.md hint sections learn `grid_rows`, `grid_cols`, `max_deviation_pct`, and `fgr`; hitl-author also learns `tile_rois` in the conventional-order list
- [x] `test_skill_doc.py` + `test_hitl_author_doc.py` drift-lints pass
- [x] Full suite green: **62 passed, 6 skipped** (was 59/4 — +2 primitive contract tests, +1 composition; +2 skipped render tests per convention). Zero regressions.

## Blocked by

- 0016
