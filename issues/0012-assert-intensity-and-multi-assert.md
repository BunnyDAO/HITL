---
id: 0012
title: assert_intensity primitive + refactor vision-multi-assert (preserves Jinja loop)
type: AFK
status: open
blocked_by: [0011]
parent: docs/prd/primitives-kit-and-hitl-author.md
---

## What to build

Ship the fourth and final starter-kit primitive (`assert_intensity`) and refactor `templates/vision-multi-assert.py.j2`. This template's `{% for %}` loop over `assertion_kinds` + `assertion_kwargs` is structural — it stays in the composing template body. What changes is that the loop body now uses primitive-derived call shapes rather than inline ones.

End-to-end behavior: `make demo-multi` continues to render the multi-assert template and the generated test continues to pass — two assertion calls in sequence, both using `hitl_assert.<kind>(image, <kwargs>)`. After this slice, all three existing top-level templates compose from the kit; the kit is proven against every shape the repo ships.

## Acceptance criteria

- [ ] `templates/primitives/assert_intensity.j2` exists with frontmatter declaring `intensity_threshold` required
- [ ] `templates/primitives/assert_intensity.j2` body emits a single `hitl_assert.pixel_intensity_above(image, threshold={{ intensity_threshold }})` call
- [ ] `templates/vision-multi-assert.py.j2` refactored: setup + capture come from primitive includes; the `{% for %}` loop body emits the same `hitl_assert.{{ kind }}(image, {{ kwargs }})` call shape; structurally still uses the parallel-array workaround for sc-compose's scalar-only var-file
- [ ] `make demo-multi` succeeds and the generated test passes pytest
- [ ] Full test suite passes — the existing render-smoke test for vision-multi-assert continues to pass
- [ ] The new template body is readable end-to-end in under a screen — the three primitive includes plus a small loop is the entire body

## Blocked by

- 0011
