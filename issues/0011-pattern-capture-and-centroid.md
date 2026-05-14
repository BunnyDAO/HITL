---
id: 0011
title: pattern_capture + assert_centroid primitives + refactor vision-centroid
type: AFK
status: open
blocked_by: [0010]
parent: docs/prd/primitives-kit-and-hitl-author.md
---

## What to build

Ship two more primitives — `pattern_capture` (display.show + camera.capture) and `assert_centroid` (the single centroid_within call) — and refactor `templates/vision-centroid.py.j2` to compose from `setup_preamble + pattern_capture + assert_centroid` via sequential `@<primitives/...>` includes.

End-to-end behavior: `make demo` continues to render the vision-centroid template and the generated test continues to pass at `tolerance_px=5`. The tolerance-flip demo (tight tolerance fails) still works — slice 0002's centroid math is downstream of the refactor.

After this slice, the kit covers two of the three existing top-level templates (smoke-test from 0010, vision-centroid here).

## Acceptance criteria

- [ ] `templates/primitives/pattern_capture.j2` exists with frontmatter declaring `display_pattern` required, `capture_delay_ms` and `retries` as defaults
- [ ] `templates/primitives/pattern_capture.j2` body emits `display.show("{{ display_pattern }}")` and `image = camera.capture(delay_ms={{ capture_delay_ms }}, retries={{ retries }})` with appropriate indentation for inclusion inside a function body
- [ ] `templates/primitives/assert_centroid.j2` exists with frontmatter declaring `target_x`, `target_y`, `tolerance_px` required
- [ ] `templates/primitives/assert_centroid.j2` body emits a single `hitl_assert.centroid_within(image, target=(...), tolerance_px=...)` call
- [ ] `templates/vision-centroid.py.j2` refactored to compose from the three primitives via `@<primitives/...>` includes (no inline assertion calls)
- [ ] `make demo` succeeds and the generated test passes pytest
- [ ] Full test suite passes
- [ ] Re-running with `vars.tight.json` (tolerance_px=1) still produces a FAILING test with the centroid-distance diagnostic — the refactor preserves the wow moment

## Blocked by

- 0010
