"""Assertion helpers operating on numpy image arrays."""
from __future__ import annotations

import math

import numpy as np


def centroid_within(
    image: np.ndarray,
    target: tuple[float, float],
    tolerance_px: float,
) -> None:
    """Assert that the intensity-weighted centroid of `image` lies within
    `tolerance_px` of `target`. `target` is `(x, y)` in pixel coordinates,
    where x is the column index and y is the row index.

    Centroid is computed via the standard image-moments formula:

        cx = sum(x * I(x,y)) / sum(I(x,y))
        cy = sum(y * I(x,y)) / sum(I(x,y))

    A blank image (sum == 0) raises immediately — no centroid is defined.
    """
    if not isinstance(image, np.ndarray):
        raise AssertionError(
            f"expected numpy.ndarray, got {type(image).__name__}"
        )

    total = float(image.sum())
    if total == 0.0:
        raise AssertionError("image is uniformly zero — no centroid to compute")

    ys, xs = np.indices(image.shape)
    cx = float((image * xs).sum() / total)
    cy = float((image * ys).sum() / total)

    tx, ty = target
    distance = math.hypot(cx - tx, cy - ty)

    if distance > tolerance_px:
        raise AssertionError(
            f"centroid ({cx:.2f}, {cy:.2f}) is {distance:.2f}px from "
            f"target ({tx}, {ty}); tolerance was {tolerance_px}px"
        )


def pixel_intensity_above(image: np.ndarray, threshold: float) -> None:
    """Assert that at least one pixel in `image` has intensity greater than
    `threshold`. Useful as a sanity check that the display actually rendered
    something visible to the camera."""
    if not isinstance(image, np.ndarray):
        raise AssertionError(
            f"expected numpy.ndarray, got {type(image).__name__}"
        )
    observed_max = float(image.max())
    if observed_max <= threshold:
        raise AssertionError(
            f"max pixel intensity was {observed_max:.0f}; "
            f"expected something above {threshold}"
        )
