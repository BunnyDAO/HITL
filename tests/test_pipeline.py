"""End-to-end tracer bullet for slice 0001.

This test exercises the complete pipeline:

    template + vars → sc-compose render → .py file → pytest exits 0

If this test passes, the wire from sc-compose to our fixture library
is connected correctly. It is the single most important test in the
repo — every other slice deepens behavior behind this contract.
"""
import ast
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def test_render_and_run_vision_centroid(tmp_path):
    assert shutil.which("sc-compose"), (
        "sc-compose CLI not on PATH — install with "
        "`brew install randlee/tap/sc-compose`"
    )

    out_file = tmp_path / "test_generated.py"
    render = subprocess.run(
        [
            "sc-compose", "render",
            "--mode", "file",
            "--file", str(REPO_ROOT / "templates" / "vision-centroid.py.j2"),
            "--var-file", str(REPO_ROOT / "vars.example.json"),
            "--output", str(out_file),
        ],
        capture_output=True,
        text=True,
    )
    assert render.returncode == 0, (
        f"sc-compose render failed (exit {render.returncode})\n"
        f"stderr:\n{render.stderr}"
    )
    assert out_file.exists(), "render did not write --output file"

    ast.parse(out_file.read_text())

    pytest_run = subprocess.run(
        [sys.executable, "-m", "pytest", str(out_file), "-v"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert pytest_run.returncode == 0, (
        f"generated test failed under pytest (exit {pytest_run.returncode})\n"
        f"stdout:\n{pytest_run.stdout}\n"
        f"stderr:\n{pytest_run.stderr}"
    )
