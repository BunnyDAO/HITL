"""Mock camera with deterministic-jitter dot patterns.

The camera reads the currently-displayed pattern from `hitl_lib.display`
and produces a single bright pixel near the nominal target (100, 100),
offset by jitter drawn from a PRNG seeded off the pattern name.

The seed is derived via a stable hash (md5) rather than Python's built-in
hash(), so output is reproducible across processes — required for a
demo whose entire point is "same inputs, same outputs."

Tuning: with sigma=3.0 and the current seed scheme, "dot_grid" lands
~3.16 px from (100, 100), so `tolerance_px=5` passes and `tolerance_px=1`
fails. Other patterns vary between ~1.4 and ~4.2 px. Change either
constant only if you're prepared to re-verify the demo's tolerance flip.
"""
from __future__ import annotations

import hashlib

import numpy as np

from hitl_lib import display

_IMAGE_SIZE = 200
_BASE_X = 100
_BASE_Y = 100
_JITTER_SIGMA = 3.0

# FGR (flat gray raster) field: a nominally-uniform mid-gray panel with a
# deterministic brightness fall-off away from the top-left corner. The
# fall-off magnitude is tuned so a 3x3 ROI tiling yields ~3-4% cross-ROI
# uniformity deviation — enough that `max_deviation_pct=5` passes and
# `max_deviation_pct=2` fails (the demo's tunable wow moment). No
# per-capture randomness: same pattern in, same field out, every time.
# Change these only if you re-verify the FGR uniformity flip.
_FGR_BASE_LV = 128
_FGR_HOTSPOT_DELTA = 7.0


def _seed_from_pattern(pattern: str) -> int:
    digest = hashlib.md5(pattern.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big")


def capture(delay_ms: int = 500, retries: int = 3) -> np.ndarray:
    pattern = display.current()
    if not pattern:
        raise RuntimeError(
            "camera.capture() requires display.show(pattern) to be called first"
        )

    if pattern == "fgr":
        return _fgr_field()

    rng = np.random.default_rng(_seed_from_pattern(pattern))
    jitter_x = int(round(rng.normal(0, _JITTER_SIGMA)))
    jitter_y = int(round(rng.normal(0, _JITTER_SIGMA)))

    img = np.zeros((_IMAGE_SIZE, _IMAGE_SIZE), dtype=np.uint8)
    img[_BASE_Y + jitter_y, _BASE_X + jitter_x] = 255
    return img


def _fgr_field() -> np.ndarray:
    """Mid-gray field with a deterministic brightness fall-off away from
    the top-left corner — a stand-in for real panel non-uniformity."""
    ys, xs = np.indices((_IMAGE_SIZE, _IMAGE_SIZE))
    norm = np.sqrt(xs**2 + ys**2) / np.sqrt(2 * (_IMAGE_SIZE - 1) ** 2)
    field = _FGR_BASE_LV - _FGR_HOTSPOT_DELTA * norm
    return np.clip(field, 0, 255).astype(np.uint8)
