---
id: 0012
title: assert_intensity primitive + refactor vision-multi-assert (preserves Jinja loop)
type: AFK
status: done
blocked_by: [0011]
parent: docs/prd/primitives-kit-and-hitl-author.md
---

## What to build

Ship the fourth and final starter-kit primitive (`assert_intensity`) and refactor `templates/vision-multi-assert.py.j2`. This template's `{% for %}` loop over `assertion_kinds` + `assertion_kwargs` is structural — it stays in the composing template body. What changes is that the loop body now uses primitive-derived call shapes rather than inline ones.

End-to-end behavior: `make demo-multi` continues to render the multi-assert template and the generated test continues to pass — two assertion calls in sequence, both using `hitl_assert.<kind>(image, <kwargs>)`. After this slice, all three existing top-level templates compose from the kit; the kit is proven against every shape the repo ships.

## Acceptance criteria

- [x] `templates/primitives/assert_intensity.j2` exists, declares `intensity_threshold` required
- [x] `assert_intensity.j2` body emits the single `hitl_assert.pixel_intensity_above(image, threshold=...)` call
- [x] `vision-multi-assert.py.j2` refactored: setup + capture from primitives; `{% for %}` loop body keeps the inline `hitl_assert.<kind>(image, <kwargs>)` call shape per the parallel-arrays sc-compose workaround
- [x] `make demo-multi` succeeds (two-assertion sequence renders + passes)
- [x] Full test suite passes (32 tests now — 4 primitive contract tests + the rest)
- [x] Composing template bodies are now tiny: vision-centroid = 3 lines, smoke-test = 3 lines, vision-multi-assert = 4 lines + small loop
- [x] **Bonus scope**: `smoke-test.py.j2` ALSO refactored to use `pattern_capture` + `assert_intensity` primitives (was partial after #0010). All three top-level templates now compose entirely from the kit — fulfills the PRD's "kit proves itself against every shape we ship" promise.

## Blocked by

- 0011
