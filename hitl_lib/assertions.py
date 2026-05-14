"""Assertion helpers operating on numpy image arrays.

Slice 0001: stub implementations sufficient for the tracer-bullet test.
Slice 0002 replaces centroid_within with real image-moments math."""
from __future__ import annotations

import numpy as np


def centroid_within(
    image: np.ndarray,
    target: tuple[int, int],
    tolerance_px: float,
) -> None:
    if not isinstance(image, np.ndarray):
        raise AssertionError(f"expected numpy.ndarray, got {type(image).__name__}")
    if image.sum() == 0:
        raise AssertionError("image is uniformly zero — no centroid")
