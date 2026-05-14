"""Pytest fixture wiring camera + display + assertions for generated tests."""
from types import SimpleNamespace

import pytest

from hitl_lib import assertions, camera, display


@pytest.fixture
def hitl_fixture():
    display.reset()
    yield SimpleNamespace(camera=camera, display=display, assertions=assertions)
    display.reset()
