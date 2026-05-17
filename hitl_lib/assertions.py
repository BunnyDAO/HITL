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


def roi_uniformity_within(
    image: np.ndarray,
    rois: list[tuple[int, int, int, int]],
    max_deviation_pct: float,
) -> None:
    """Assert cross-ROI luminance uniformity is within tolerance.

    For each ROI `(x, y, w, h)`, compute its mean luminance. Then:

        uniformity = (max_ROI_mean - min_ROI_mean) / max_ROI_mean * 100

    (the canonical metric — see CONTEXT.md). Raises `AssertionError`
    naming the observed deviation, the brightest and dimmest ROI means,
    and the threshold when uniformity exceeds `max_deviation_pct`.

    This is a cross-ROI metric (ROIs compared to each other), NOT a
    per-pixel or within-ROI spread.
    """
    if not isinstance(image, np.ndarray):
        raise AssertionError(
            f"expected numpy.ndarray, got {type(image).__name__}"
        )
    if not rois:
        raise AssertionError("no ROIs supplied — nothing to compare")

    means = [
        float(image[y : y + h, x : x + w].mean())
        for (x, y, w, h) in rois
    ]
    max_mean = max(means)
    min_mean = min(means)

    if max_mean == 0.0:
        raise AssertionError(
            "all ROIs are uniformly zero — no luminance to compare"
        )

    deviation_pct = (max_mean - min_mean) / max_mean * 100.0

    if deviation_pct > max_deviation_pct:
        raise AssertionError(
            f"cross-ROI uniformity deviation was {deviation_pct:.2f}% "
            f"(brightest ROI mean {max_mean:.2f}, dimmest {min_mean:.2f}); "
            f"tolerance was {max_deviation_pct}%"
        )
