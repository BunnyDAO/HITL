---
id: 0016
title: hitl_lib FGR measurement support (roi.tile + camera fgr branch + roi_uniformity_within)
type: HITL
status: done
blocked_by: []
parent: docs/prd/fgr-uniformity-domain-example.md
---

## What to build

The measurement substrate for FGR uniformity — the riskiest, most novel part, built and proven before any template touches it. After this slice the repo can, in pure Python, simulate an FGR capture, tile it into ROIs, and compute cross-ROI uniformity, all unit-tested. No template, no primitive, no skill change beyond the one shared import.

End-to-end verifiable behavior (via new unit tests, not a rendered template yet):

- `hitl_lib.roi.tile(image, rows, cols)` returns `rows*cols` regions as `(x, y, w, h)` tuples that cover the image with no overlap; pixels left over from non-even division are absorbed into the last row/column.
- `hitl_lib.assertions.roi_uniformity_within(image, rois, max_deviation_pct)` computes each ROI's mean luminance, derives `uniformity = (max_mean - min_mean) / max_mean` as a percent (the canonical metric per `CONTEXT.md`), and raises `AssertionError` naming the observed deviation, the brightest/dimmest ROI means, and the threshold when it exceeds `max_deviation_pct`.
- `hitl_lib.camera.capture()` returns a deterministic ~mid-gray field with a documented corner hot-spot (~3–4% cross-ROI deviation) when `display.current() == "fgr"`. Every other `display.current()` value behaves exactly as before.
- `setup_preamble.j2` emits `from hitl_lib import roi` so later primitives (next slice) can call `roi.tile`.

This slice is HITL because it fixes interfaces every later slice inherits: the `roi.tile` signature, the ROI tuple shape, the remainder-pixel rule, the single home of the uniformity formula, and the FGR hot-spot constant.

## Acceptance criteria

- [x] `hitl_lib/roi.py` exists; `tile(image, rows, cols)` returns `rows*cols` `(x,y,w,h)` tuples, no overlap, full coverage, remainder pixels in the last row/col
- [x] `tile` handles degenerate inputs sanely (1×1; rows or cols exceeding image dimensions) — clamps so every region ≥1px
- [x] `hitl_lib.assertions.roi_uniformity_within(image, rois, max_deviation_pct)` implements the `CONTEXT.md` uniformity metric and raises a diagnostic-rich `AssertionError` (observed deviation %, brightest & dimmest ROI means, threshold)
- [x] `camera.capture()` returns a deterministic FGR field (mid-gray + documented corner hot-spot constant `_FGR_HOTSPOT_DELTA`, no per-capture randomness) when `display.current()=="fgr"`; constant carries a docstring like `_JITTER_SIGMA`
- [x] FGR cross-ROI deviation measured at **3.64%** on a 3×3 grid — inside the documented ~3–4% band and the (2,5) window so `max_deviation_pct=5` passes / `=2` fails
- [x] `setup_preamble.j2` gains `from hitl_lib import roi` (unconditional; documented harmless unused import in non-FGR templates); `hitl_lib/__init__.py` updated for consistency
- [x] New `tests/test_roi.py` — 6 tests: count, bounds, full-coverage/no-overlap, remainder rule, 1×1, degenerate over-tiling
- [x] `tests/test_assertions.py` extended — 4 tests: flat-field pass, gradient fail, exact-threshold boundary pass, message names deviation + extremes + threshold
- [x] `tests/test_camera.py` extended — 4 tests: deterministic FGR, mid-gray (not a dot), deviation in band, dot branch unchanged
- [x] All 45 pre-existing tests still pass — full suite now **59 passed, 4 skipped** (45 prior + 14 new); zero regressions

## Blocked by

None — can start immediately.
