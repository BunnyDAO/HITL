---
id: 0011
title: pattern_capture + assert_centroid primitives + refactor vision-centroid
type: AFK
status: done
blocked_by: [0010]
parent: docs/prd/primitives-kit-and-hitl-author.md
---

## What to build

Ship two more primitives — `pattern_capture` (display.show + camera.capture) and `assert_centroid` (the single centroid_within call) — and refactor `templates/vision-centroid.py.j2` to compose from `setup_preamble + pattern_capture + assert_centroid` via sequential `@<primitives/...>` includes.

End-to-end behavior: `make demo` continues to render the vision-centroid template and the generated test continues to pass at `tolerance_px=5`. The tolerance-flip demo (tight tolerance fails) still works — slice 0002's centroid math is downstream of the refactor.

After this slice, the kit covers two of the three existing top-level templates (smoke-test from 0010, vision-centroid here).

## Acceptance criteria

- [x] `templates/primitives/pattern_capture.j2` exists, declares `display_pattern` required + `capture_delay_ms` and `retries` defaults
- [x] `pattern_capture.j2` body emits `display.show(...)` + `image = camera.capture(...)` with 4-space indent for function-body inclusion
- [x] `templates/primitives/assert_centroid.j2` exists, declares `target_x`, `target_y`, `tolerance_px` required
- [x] `assert_centroid.j2` body emits the single `hitl_assert.centroid_within(...)` call (note: uses the `hitl_assert` alias, consistent with `setup_preamble.j2`'s imports)
- [x] `vision-centroid.py.j2` refactored to compose from the three primitives — body is just three `@<primitives/...>` lines
- [x] `make demo` succeeds and `test_demo_centroid` passes
- [x] Full test suite passes (31 tests now)
- [x] Wow moment preserved: rendering with `vars.tight.json` (tolerance_px=1) produces `FAILED  AssertionError: centroid (97.00, 101.00) is 3.16px from target (100, 100); tolerance was 1px`
- [x] Semantic diff vs. pre-refactor: the rendered output uses `hitl_assert.centroid_within` (aliased) instead of `assertions.centroid_within` — same callable, different name. Intentional per the kit's import convention.

## Blocked by

- 0010
