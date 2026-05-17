"""Unit tests for hitl_lib.roi — deterministic ROI grid tiling.

roi.tile is the deep module behind the FGR-uniformity primitive. It must
produce a grid that covers the whole image with no overlap, absorbing
remainder pixels (from non-even division) into the last row/column.
"""
from __future__ import annotations

import numpy as np

from hitl_lib import roi


def _img(h: int, w: int) -> np.ndarray:
    return np.zeros((h, w), dtype=np.uint8)


def test_tile_returns_rows_times_cols_regions():
    rois = roi.tile(_img(200, 200), rows=3, cols=4)
    assert len(rois) == 12


def test_tile_regions_are_xywh_tuples_within_bounds():
    img = _img(200, 200)
    for (x, y, w, h) in roi.tile(img, rows=3, cols=3):
        assert 0 <= x < 200 and 0 <= y < 200
        assert w > 0 and h > 0
        assert x + w <= 200 and y + h <= 200


def test_tile_covers_every_pixel_with_no_overlap():
    img = _img(200, 200)
    coverage = np.zeros((200, 200), dtype=int)
    for (x, y, w, h) in roi.tile(img, rows=4, cols=5):
        coverage[y : y + h, x : x + w] += 1
    assert coverage.min() == 1 and coverage.max() == 1, (
        "every pixel must be covered exactly once"
    )


def test_tile_absorbs_remainder_into_last_row_and_col():
    # 200 / 3 = 66 r 2  →  first two rows 66px, last row 68px (66+2).
    img = _img(200, 200)
    rois = roi.tile(img, rows=3, cols=3)
    # Group by row band via y coordinate.
    ys = sorted({y for (_, y, _, _) in rois})
    heights_by_band = {
        y: next(h for (_, yy, _, h) in rois if yy == y) for y in ys
    }
    bands = [heights_by_band[y] for y in ys]
    assert bands[:-1] == [66, 66] and bands[-1] == 68, (
        f"remainder must land in the last band; got {bands}"
    )


def test_tile_one_by_one_returns_whole_image():
    rois = roi.tile(_img(120, 90), rows=1, cols=1)
    assert rois == [(0, 0, 90, 120)]


def test_tile_more_rows_than_pixels_does_not_raise_or_produce_empty_regions():
    # 5 rows over a 3px-tall image: must not crash, must not emit zero-height ROIs.
    rois = roi.tile(_img(3, 10), rows=5, cols=2)
    assert all(w > 0 and h > 0 for (_, _, w, h) in rois)
