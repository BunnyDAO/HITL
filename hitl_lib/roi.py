"""Deterministic ROI grid tiling.

Splits an image into a `rows x cols` grid of regions of interest. Each
ROI is an `(x, y, w, h)` tuple. The grid covers every pixel exactly once;
pixels left over from non-even division are absorbed into the last row
and/or last column (so a 200px / 3-row split is 66, 66, 68).

If `rows` (or `cols`) exceeds the image's pixel extent, it is clamped so
every region is at least 1px — asking for more bands than pixels yields
one band per pixel rather than zero-height regions or an error.

See CONTEXT.md for the canonical definition of ROI.
"""
from __future__ import annotations

import numpy as np

ROI = tuple[int, int, int, int]  # (x, y, w, h)


def tile(image: np.ndarray, rows: int, cols: int) -> list[ROI]:
    h, w = image.shape[:2]
    rows = max(1, min(rows, h))
    cols = max(1, min(cols, w))

    base_h, rem_h = divmod(h, rows)
    base_w, rem_w = divmod(w, cols)

    regions: list[ROI] = []
    y = 0
    for r in range(rows):
        rh = base_h + (rem_h if r == rows - 1 else 0)
        x = 0
        for c in range(cols):
            rw = base_w + (rem_w if c == cols - 1 else 0)
            regions.append((x, y, rw, rh))
            x += rw
        y += rh
    return regions
