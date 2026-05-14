"""Mock camera.

Slice 0001: returns a trivially-centered single-pixel image so the
tracer-bullet pipeline can run end-to-end without real math.
Slice 0002 replaces this body with deterministic-jitter dot patterns
keyed off display.current()."""
import numpy as np


def capture(delay_ms: int = 500, retries: int = 3) -> np.ndarray:
    img = np.zeros((200, 200), dtype=np.uint8)
    img[100, 100] = 255
    return img
