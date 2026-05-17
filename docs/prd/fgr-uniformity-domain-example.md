# FGR-Uniformity — first Iron-flavored domain example

## Problem Statement

The repo proves the agentic-HITL pattern works, but every primitive and template ships with *toy vision* semantics (a jittered dot, a centroid check). A teammate evaluating this for Iron can't see the pattern expressed in their own domain (display/optical metrology). The honest framing in the team message is "here's the machinery on stub primitives — Iron-specific primitives don't exist yet." This PRD closes that gap with one concrete, end-to-end display-metrology example so the repo demonstrates the pattern in the language Iron actually uses (FGR, ROI, Lv, uniformity), not just abstract vision toys.

## Solution

Add a first-class `fgr-uniformity` template and the two new primitives it needs, plus the `hitl_lib` support to make the measurement real. A test engineer can then pick `fgr-uniformity` in `/hitl-test` (or compose the same shape in `/hitl-author`), answer `grid_rows`, `grid_cols`, `max_deviation_pct`, and get a runnable pytest that tiles a captured FGR field into ROIs and asserts cross-ROI luminance uniformity. The same tunable pass/fail "wow moment" the centroid slice established carries over: loosening or tightening one threshold flips the test, with a diagnostic that names the observed deviation.

All terminology is governed by `CONTEXT.md` (written during the grill): FGR, ROI, Lv (uint8 grayscale as luminance proxy), Uniformity (the cross-ROI metric), Within-ROI spread (explicitly *not* implemented), Mura.

## User Stories

1. As a **teammate evaluating this for Iron**, I want to see the pattern expressed with FGR/ROI/uniformity vocabulary, so I can judge fit against real Iron tests instead of extrapolating from a dot demo.
2. As a **test engineer**, I want to pick `fgr-uniformity` in `/hitl-test`, answer grid size and tolerance, and get a runnable uniformity test, so I never touch pixel coordinates or Python.
3. As a **test engineer**, I want the failure message to name the observed uniformity deviation and which threshold I set, so a failing run tells me whether to adjust the spec or the rig.
4. As a **developer**, I want ROI tiling to be a deep module with a one-function interface (`roi.tile`), so the grid math is unit-tested in isolation and the primitive stays a thin include.
5. As a **developer**, I want the `"fgr"` camera behavior added alongside the existing dot behavior (not replacing it), so all 45 existing tests stay green.
6. As a **developer**, I want the uniformity metric defined once in `CONTEXT.md` and computed in exactly one place (`assertions.roi_uniformity_within`), so "uniformity" can't drift into meaning three different things.
7. As a **maintainer**, I want both SKILL.md hint sections to learn the new variables and the `fgr` pattern, enforced by the existing drift-lint tests, so `/hitl-test` and `/hitl-author` don't silently fail to offer them.
8. As a **dev lead**, I want this shipped as a first-class template (peer of `vision-centroid`), so the repo's canonical domain example isn't buried in the engineer-authored-example slot.
9. As a **test engineer using `/hitl-author`**, I want `tile_rois` and `assert_roi_uniformity` to appear in the primitive picker, so I can compose other uniformity-style shapes without a developer.

## Implementation Decisions

- **Metric (canonical, per `CONTEXT.md`)**: `uniformity = (max_ROI_mean_Lv − min_ROI_mean_Lv) / max_ROI_mean_Lv`, as a percentage. Cross-ROI only. Per-pixel / within-ROI spread is explicitly out (named in `CONTEXT.md` solely to keep the distinction sharp).
- **`hitl_lib/roi.py`** — new deep module. Interface: `tile(image, rows, cols) -> list[ROI]` where `ROI` is a 4-tuple `(x, y, w, h)`. Pure deterministic geometry over image dimensions; remainder pixels from non-even division are absorbed into the last row/column (documented behavior, unit-tested).
- **`assertions.roi_uniformity_within(image, rois, max_deviation_pct)`** — computes each ROI's mean Lv, the cross-ROI uniformity, raises `AssertionError` if it exceeds `max_deviation_pct`. The message names the observed deviation %, the brightest and dimmest ROI means, and the threshold — same diagnostic-richness bar as `centroid_within`.
- **`camera.capture()` gains an `"fgr"` branch** keyed off `display.current()=="fgr"`. Returns a ~mid-gray field plus a deterministic corner hot-spot sized to produce ~3–4% cross-ROI deviation. The hot-spot magnitude is a named module constant with a docstring, exactly like the existing jitter-sigma constant. No per-capture randomness — same inputs, same field, every time. Existing dot/centroid branch is untouched.
- **`setup_preamble.j2` gains `from hitl_lib import roi`** unconditionally. Primitives emit into the function body after `setup_preamble` has already written top-level imports, so a later primitive cannot add an import; the only clean place is `setup_preamble`. Dot/centroid templates carry one unused import as a result — harmless (no linter in the suite; Python/pytest don't care), and it keeps all imports in one reviewed primitive, consistent with how `hitl_assert` already works.
- **Two new primitives**: `tile_rois.j2` (declares `grid_rows`, `grid_cols`; emits `rois = roi.tile(image, rows=..., cols=...)`) and `assert_roi_uniformity.j2` (declares `max_deviation_pct`; emits `hitl_assert.roi_uniformity_within(image, rois, max_deviation_pct=...)`). `pattern_capture` is reused unchanged with `display_pattern=fgr`.
- **`templates/fgr-uniformity.py.j2`** — first-class template composing `setup_preamble → pattern_capture → tile_rois → assert_roi_uniformity`. Its frontmatter declares the union of required variables (kept explicit for `test_skill_doc.py` compatibility, consistent with the other top-level templates).
- **Naming**: the assertion primitive is `assert_roi_uniformity`. The earlier-floated `assert_pixel_variance` was rejected during the grill as a misnomer (it would name a metric the code doesn't compute).
- **Var-file shape** stays scalar-only: `grid_rows`, `grid_cols`, `max_deviation_pct`, `test_name`, `display_pattern`. No nested objects — honors sc-compose's `ERR_CONFIG_VARFILE` constraint without a parallel-array workaround, because the grid is fully determined by two scalars plus the image size.
- **Both SKILL.md hint sections** (`/hitl-test`, `/hitl-author`) learn `grid_rows`, `grid_cols`, `max_deviation_pct`, and `fgr` as a `display_pattern` option. Enforced by the existing `test_skill_doc.py` / `test_hitl_author_doc.py` drift-lints.

## Testing Decisions

Test external behavior, not internals — consistent with the existing suite.

- **`tests/test_roi.py`** (new): `tile()` returns `rows*cols` ROIs; they cover the image without overlap; remainder pixels land in the last row/col; degenerate inputs (1×1, rows>height) behave sanely. This is the deep module — the one place tiling correctness is pinned.
- **`tests/test_assertions.py`** (extend): `roi_uniformity_within` passes on a flat field, fails on a field with a known injected gradient, the boundary case sits exactly at the threshold, and the failure message contains the observed deviation. Mirrors the existing `centroid_within` test structure.
- **`tests/test_camera.py`** (extend): with `display.show("fgr")`, `capture()` returns a field whose cross-ROI deviation lands in the documented ~3–4% band, and is byte-identical across two calls (determinism). Existing dot-pattern tests must remain unchanged and green.
- **`tests/test_primitives.py`** (extend): two new parametrized entries (`tile_rois`, `assert_roi_uniformity`) — same contract checks as the existing four (frontmatter declares variables; renders to the expected fragment).
- **`tests/test_composition.py`** (extend): `fgr-uniformity` renders to valid Python and passes pytest with `vars.fgr.json`.
- **Regression net**: all 45 existing tests stay green. They are the guarantee that adding the `fgr` branch and the `roi` import didn't disturb dot/centroid behavior.
- **The wow moment** is verified by `make demo-fgr` (passes at `max_deviation_pct=5`) plus a tight variant rendered at `max_deviation_pct=2` that fails with the deviation-naming diagnostic — the same manual check pattern as the centroid slice.

## Out of Scope

- **Within-ROI / per-pixel variance.** Named in `CONTEXT.md` only to keep the metric distinction sharp. Not implemented; a future primitive-request if ever needed.
- **Irregular / overlapping / hand-placed ROIs.** Only regular grid tiling (`grid_rows × grid_cols`). Explicit-bounds ROIs were considered and deferred during the grill.
- **Real photometry.** `uint8` grayscale stays the luminance proxy. No real Lv units, no photometer model, no gamma.
- **Other display metrics** (chromaticity, contrast ratio, defect/dead-pixel detection, response time, mura-as-its-own-metric). This PRD ships exactly one domain metric end-to-end.
- **Deck update.** `docs/deck.md` may later gain one FGR slide; deferred — not required for this slice.
- **Real-hardware wiring.** Layer 1 stays mocked; this PRD does not touch the mock/real boundary.

## Further Notes

- **Deferred ADR**: the choice of cross-ROI uniformity over within-ROI spread, and `uint8`-as-luminance-proxy, is borderline ADR-worthy (genuine fork, mildly hard to reverse, future-reader-surprising). `CONTEXT.md` records the *what*; an ADR would record the *why*. Not created — offer it again at implementation time if the rationale feels worth freezing.
- `CONTEXT.md` was authored during the grill and is the terminology authority for all downstream issues and code. Any drift between code and `CONTEXT.md` during TDD should correct the code or update `CONTEXT.md` deliberately — not silently diverge.
- This is most naturally **one vertical slice** (hitl_lib support → primitives → template → docs), but the issue-breakdown step may split it tracer-first (e.g. `roi.tile` + camera fgr branch + assertion as the tracer, then primitives, then template+docs). That decision belongs to `to-issues`.
- The unused `roi` import in non-FGR templates is a deliberate, documented trade-off (see Implementation Decisions). If a linter is ever added to the suite, it must be configured to permit it in generated output, or `setup_preamble` revisited.
