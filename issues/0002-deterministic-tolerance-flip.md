---
id: 0002
title: Deterministic pass/fail by tolerance_px — the demo's central beat
type: AFK
status: done
blocked_by: [0001]
parent: docs/prd/agentic-hitl-test-generator.md
---

## What to build

Make the camera's jitter and the assertion's centroid math real enough that changing one variable — `tolerance_px` — flips the generated test between pass and fail in a way the demo audience can feel.

End-to-end behavior: render the `vision-centroid` template twice. With `tolerance_px=5`, pytest passes. With `tolerance_px=1`, pytest fails. The numbers and jitter magnitude are tuned so the difference is unambiguous and reproducible (seeded PRNG — no flakiness).

This slice replaces slice 1's stubs with real numpy-backed implementations. The "wow moment" beat of the demo is created here.

## Acceptance criteria

- [x] `hitl_lib.camera.capture()` returns a numpy 2D grayscale array with a synthetic dot pattern derived from `display.current()`
- [x] Camera jitter is seeded PRNG-driven (deterministic across runs) with magnitude ~3 pixels (md5-derived seed → `np.random.default_rng`, sigma=3.0)
- [x] `hitl_lib.assertions.centroid_within()` computes the real image-moments centroid (numpy directly via `np.indices`) and raises `AssertionError` with the observed centroid, distance, and tolerance in the message
- [x] `hitl_lib.display.show()`/`current()` track the current pattern in module-level state; fixture resets state between tests (from #0001)
- [x] `tests/test_assertions.py` unit-tests `centroid_within` against known synthetic arrays (9 cases: zero distance, pass-within-tolerance, fail-outside-tolerance, exactly-at-boundary, just-outside, multi-pixel centroid, blank image, non-array, message format)
- [x] `tests/test_camera.py` unit-tests the camera (determinism, shape, expected offset range, pattern-keyed seed, error when display not set)
- [x] Demonstrated manually: `vars.example.json` (tolerance_px=5) renders to a PASSING test; `vars.tight.json` (tolerance_px=1) renders to a FAILING test with message `centroid (97.00, 101.00) is 3.16px from target (100, 100); tolerance was 1px`
- [x] PRNG seed scheme (md5(pattern_name)[:4]) and sigma=3.0 are documented in `hitl_lib/camera.py` module docstring

## Blocked by

- 0001
