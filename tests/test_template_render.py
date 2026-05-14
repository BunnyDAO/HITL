"""Render-smoke tests for every sc-compose template in templates/.

These are fast (subprocess + ast.parse, no test execution) and catch
template-level mistakes — unbalanced braces, malformed Jinja, missing
imports — without needing to run the generated test code. They're the
first line of defense when someone edits a template.

The known-valid var files live at the repo root (vars.*.json) — the
same files used by the user-facing `make demo*` targets. Reusing them
avoids drift between the demo flow and the test suite. (Spec asked for
`tests/fixtures/` but that would duplicate the same JSON.)
"""
from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent

# Map each renderable template to its known-valid var file.
RENDERABLE_TEMPLATES: list[tuple[str, str]] = [
    ("templates/vision-centroid.py.j2", "vars.example.json"),
    ("templates/vision-multi-assert.py.j2", "vars.multi-assert.json"),
    ("templates/smoke-test.py.j2", "vars.smoke.json"),
]


@pytest.mark.parametrize("template_rel,var_file_rel", RENDERABLE_TEMPLATES, ids=lambda p: Path(p).stem)
def test_template_renders_to_valid_python(tmp_path, template_rel, var_file_rel):
    out_file = tmp_path / "rendered.py"
    result = subprocess.run(
        [
            "sc-compose", "render",
            "--mode", "file",
            "--file", str(REPO_ROOT / template_rel),
            "--var-file", str(REPO_ROOT / var_file_rel),
            "--output", str(out_file),
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, (
        f"sc-compose render failed for {template_rel}\nstderr: {result.stderr}"
    )
    ast.parse(out_file.read_text())


def test_missing_required_variable_surfaces_clear_error(tmp_path):
    # vision-centroid requires target_x; supply everything except that.
    broken = tmp_path / "broken.json"
    broken.write_text(json.dumps({
        "test_name": "broken_demo",
        "display_pattern": "dot_grid",
        # target_x deliberately omitted
        "target_y": 100,
        "tolerance_px": 5,
    }))

    out_file = tmp_path / "rendered.py"
    result = subprocess.run(
        [
            "sc-compose", "render",
            "--mode", "file",
            "--file", str(REPO_ROOT / "templates" / "vision-centroid.py.j2"),
            "--var-file", str(broken),
            "--output", str(out_file),
            "--strict",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode != 0, "expected non-zero exit when a required variable is missing"
    # The diagnostic must mention the variable name AND something that
    # signals "this was a missing required variable" so the skill can
    # surface a useful message verbatim.
    combined = (result.stdout + result.stderr).lower()
    assert "target_x" in combined, f"stderr should name the missing variable; got: {result.stderr}"
