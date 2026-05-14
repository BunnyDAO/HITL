"""Logging-only mock display. Tracks the current pattern in module state
so the camera can correlate captured imagery with what's being shown."""
import logging

_log = logging.getLogger(__name__)
_current: str = ""


def show(pattern: str) -> None:
    global _current
    _current = pattern
    _log.info("display.show(%r)", pattern)


def current() -> str:
    return _current


def reset() -> None:
    global _current
    _current = ""
