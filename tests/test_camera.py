"""Unit tests for hitl_lib.camera — deterministic-jitter mock camera.

The camera is the *source* of the demo's wow moment: with the default
seed and pattern, the dot lands ~3 px from (100, 100), so tolerance=5
passes and tolerance=1 fails. These tests pin the determinism and the
observable offset; the assertion math is tested separately.
"""
import numpy as np

from hitl_lib import camera, display


def _centroid(img: np.ndarray) -> tuple[float, float]:
    total = float(img.sum())
    ys, xs = np.indices(img.shape)
    return float((img * xs).sum() / total), float((img * ys).sum() / total)


def test_capture_is_deterministic_for_same_pattern():
    display.reset()
    display.show("dot_grid")
    a = camera.capture()
    b = camera.capture()
    assert np.array_equal(a, b), "capture must be deterministic for repeat calls under the same pattern"


def test_capture_returns_numpy_array_with_expected_shape():
    display.reset()
    display.show("dot_grid")
    img = camera.capture()
    assert isinstance(img, np.ndarray)
    assert img.ndim == 2
    assert img.dtype == np.uint8
    assert img.shape == (200, 200)


def test_capture_dot_grid_centroid_is_offset_from_nominal():
    # The defining behavior for the demo: with dot_grid + default seed,
    # the dot lands a couple of pixels off (100, 100) — far enough that
    # tolerance_px=1 fails, close enough that tolerance_px=5 passes.
    display.reset()
    display.show("dot_grid")
    img = camera.capture()
    cx, cy = _centroid(img)
    dist = ((cx - 100) ** 2 + (cy - 100) ** 2) ** 0.5
    assert 1.5 < dist < 5.0, (
        f"dot_grid centroid distance from (100,100) was {dist:.2f}; "
        "must sit in (1.5, 5.0) so the demo's tolerance flip works"
    )


def test_capture_different_patterns_give_different_centroids():
    display.reset()
    display.show("dot_grid")
    a_centroid = _centroid(camera.capture())
    display.show("checkerboard")
    b_centroid = _centroid(camera.capture())
    assert a_centroid != b_centroid, (
        "different display patterns must seed the PRNG differently"
    )


def test_capture_without_display_show_raises():
    display.reset()
    import pytest
    with pytest.raises(RuntimeError, match="display.show"):
        camera.capture()
