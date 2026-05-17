"""Post-refactor regression net for the primitive-composed top-level templates.

Where `tests/test_template_render.py` asserts each template *renders* to valid
Python, this file goes one step further and asserts the rendered code actually
*passes pytest* with the standard example var files. After the primitives
refactor (slices 0010–0012), this is the explicit "no regression" guarantee.
"""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent

COMPOSED_TEMPLATES: list[tuple[str, str]] = [
    ("templates/vision-centroid.py.j2", "vars.example.json"),
    ("templates/vision-multi-assert.py.j2", "vars.multi-assert.json"),
    ("templates/smoke-test.py.j2", "vars.smoke.json"),
    # Engineer-authored example, produced by simulating /hitl-author end-to-end.
    ("templates/centroid-with-intensity.py.j2", "vars.centroid-with-intensity.json"),
    # FGR cross-ROI uniformity — the display-metrology domain example.
    ("templates/fgr-uniformity.py.j2", "vars.fgr.json"),
]


@pytest.mark.parametrize(
    "template_rel,var_file_rel", COMPOSED_TEMPLATES, ids=lambda p: Path(p).stem
)
def test_composed_template_renders_and_passes(tmp_path, template_rel, var_file_rel):
    out_file = tmp_path / "rendered.py"

    render = subprocess.run(
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
    assert render.returncode == 0, (
        f"sc-compose render failed for {template_rel}\nstderr:\n{render.stderr}"
    )

    rendered = out_file.read_text()
    ast.parse(rendered)

    pytest_run = subprocess.run(
        [sys.executable, "-m", "pytest", str(out_file), "-v"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert pytest_run.returncode == 0, (
        f"pytest failed on rendered output of {template_rel} (exit {pytest_run.returncode})\n"
        f"stdout:\n{pytest_run.stdout}\n"
        f"stderr:\n{pytest_run.stderr}"
    )


def test_all_primitives_referenced_by_at_least_one_top_level_template():
    """Every primitive in the kit should be used by at least one top-level
    template. Catches dead code in the kit if a primitive gets orphaned."""
    primitives_dir = REPO_ROOT / "templates" / "primitives"
    primitive_stems = {p.stem for p in primitives_dir.glob("*.j2")}

    referenced = set()
    for template_rel, _ in COMPOSED_TEMPLATES:
        body = (REPO_ROOT / template_rel).read_text()
        for stem in primitive_stems:
            if f"@<primitives/{stem}.j2>" in body:
                referenced.add(stem)

    orphans = primitive_stems - referenced
    assert not orphans, (
        f"primitives not referenced by any top-level template: {sorted(orphans)}. "
        "Either compose them into a template or remove them from the kit."
    )
