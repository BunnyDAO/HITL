---
id: 0002
title: Deterministic pass/fail by tolerance_px — the demo's central beat
type: AFK
status: open
blocked_by: [0001]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

Make the camera's jitter and the assertion's centroid math real enough that changing one variable — `tolerance_px` — flips the generated test between pass and fail in a way the demo audience can feel.

End-to-end behavior: render the `vision-centroid` template twice. With `tolerance_px=5`, pytest passes. With `tolerance_px=1`, pytest fails. The numbers and jitter magnitude are tuned so the difference is unambiguous and reproducible (seeded PRNG — no flakiness).

This slice replaces slice 1's stubs with real numpy-backed implementations. The "wow moment" beat of the demo is created here.

## Acceptance criteria

- [ ] `hitl_lib.camera.capture()` returns a numpy 2D grayscale array with a synthetic dot pattern derived from `display.current()`
- [ ] Camera jitter is seeded PRNG-driven (deterministic across runs) with magnitude ~3 pixels
- [ ] `hitl_lib.assertions.centroid_within()` computes the real image-moments centroid (e.g. via scipy.ndimage or numpy directly) and raises `AssertionError` with an informative message
- [ ] `hitl_lib.display.show()`/`current()` track the current pattern in module-level state; fixture resets state between tests
- [ ] `tests/test_assertions.py` unit-tests `centroid_within` against known synthetic arrays — covers the pass case, the fail case, and an edge case at exactly the tolerance boundary
- [ ] Demonstrated manually: rendering with `tolerance_px=5` produces a passing test, `tolerance_px=1` produces a failing test, every time
- [ ] PRNG seed is documented in the camera module so future maintainers can reproduce

## Blocked by

- 0001
