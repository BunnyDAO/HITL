"""Unit tests for hitl_lib.assertions.centroid_within.

The assertion is the load-bearing math for the demo: if the centroid
calculation is correct and the threshold check is correct, generated
tests do the right thing and the tolerance_px variable has the meaning
its name implies. These tests pin down both responsibilities.
"""
import numpy as np
import pytest

from hitl_lib import assertions


def _single_pixel_image(y: int, x: int, size: int = 200) -> np.ndarray:
    img = np.zeros((size, size), dtype=np.uint8)
    img[y, x] = 255
    return img


def test_centroid_at_target_passes_zero_tolerance():
    img = _single_pixel_image(100, 100)
    assertions.centroid_within(img, target=(100, 100), tolerance_px=0)


def test_centroid_three_pixels_off_passes_tolerance_five():
    img = _single_pixel_image(100, 103)
    assertions.centroid_within(img, target=(100, 100), tolerance_px=5)


def test_centroid_three_pixels_off_fails_tolerance_one():
    img = _single_pixel_image(100, 103)
    with pytest.raises(AssertionError, match="centroid"):
        assertions.centroid_within(img, target=(100, 100), tolerance_px=1)


def test_centroid_exactly_at_tolerance_passes():
    # Distance is exactly 5; tolerance 5 should pass (inclusive boundary).
    img = _single_pixel_image(100, 105)
    assertions.centroid_within(img, target=(100, 100), tolerance_px=5)


def test_centroid_just_outside_tolerance_fails():
    img = _single_pixel_image(100, 106)
    with pytest.raises(AssertionError):
        assertions.centroid_within(img, target=(100, 100), tolerance_px=5)


def test_centroid_of_multiple_bright_pixels_is_their_mean():
    # Two equal-intensity pixels at (98,100) and (102,100) → centroid (100,100).
    img = np.zeros((200, 200), dtype=np.uint8)
    img[98, 100] = 255
    img[102, 100] = 255
    assertions.centroid_within(img, target=(100, 100), tolerance_px=0.5)


def test_centroid_blank_image_raises():
    img = np.zeros((200, 200), dtype=np.uint8)
    with pytest.raises(AssertionError, match="zero|blank|empty"):
        assertions.centroid_within(img, target=(100, 100), tolerance_px=5)


def test_centroid_non_array_raises():
    with pytest.raises(AssertionError, match="ndarray"):
        assertions.centroid_within([1, 2, 3], target=(100, 100), tolerance_px=5)


def test_assertion_message_includes_observed_centroid():
    img = _single_pixel_image(100, 110)
    with pytest.raises(AssertionError) as exc:
        assertions.centroid_within(img, target=(100, 100), tolerance_px=1)
    # The diagnostic must say where the centroid actually was, not just
    # "it failed". A test engineer reading the failure needs both numbers.
    msg = str(exc.value)
    assert "100" in msg and "110" in msg, f"diagnostic must mention observed centroid; got: {msg}"


def test_pixel_intensity_above_passes_when_max_exceeds_threshold():
    img = _single_pixel_image(100, 100)  # one pixel at 255
    assertions.pixel_intensity_above(img, threshold=200)


def test_pixel_intensity_above_fails_when_max_below_threshold():
    img = np.full((200, 200), 50, dtype=np.uint8)
    with pytest.raises(AssertionError, match="intensity"):
        assertions.pixel_intensity_above(img, threshold=100)


def test_pixel_intensity_above_message_includes_observed_max():
    img = np.full((200, 200), 73, dtype=np.uint8)
    with pytest.raises(AssertionError) as exc:
        assertions.pixel_intensity_above(img, threshold=200)
    assert "73" in str(exc.value) and "200" in str(exc.value)
