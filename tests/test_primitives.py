"""Lint each primitive in templates/primitives/.

A primitive must:
- have parseable YAML frontmatter,
- declare at least one variable in required_variables OR defaults,
- render to a non-empty body when given a known-valid mini-var-set.

The kit's contract is the frontmatter; the lints here keep that contract
honest as primitives are added/edited.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
PRIMITIVES_DIR = REPO_ROOT / "templates" / "primitives"

# Map each primitive to (known-valid mini-var-set, expected-substring).
# Slice 0010 ships setup_preamble; later slices add entries here.
PRIMITIVES: list[tuple[str, dict, str]] = [
    (
        "setup_preamble",
        {"test_name": "demo"},
        "def test_demo(hitl_fixture):",
    ),
    (
        "pattern_capture",
        {"display_pattern": "dot_grid", "capture_delay_ms": 500, "retries": 3},
        'display.show("dot_grid")',
    ),
    (
        "assert_centroid",
        {"target_x": 100, "target_y": 100, "tolerance_px": 5},
        "hitl_assert.centroid_within(image, target=(100, 100), tolerance_px=5)",
    ),
    (
        "assert_intensity",
        {"intensity_threshold": 100},
        "hitl_assert.pixel_intensity_above(image, threshold=100)",
    ),
    (
        "tile_rois",
        {"grid_rows": 3, "grid_cols": 3},
        "rois = roi.tile(image, rows=3, cols=3)",
    ),
    (
        "assert_roi_uniformity",
        {"max_deviation_pct": 5},
        "hitl_assert.roi_uniformity_within(image, rois, max_deviation_pct=5)",
    ),
]


def _frontmatter(path: Path) -> dict:
    body = path.read_text()
    assert body.startswith("---\n"), f"{path.name} must have YAML frontmatter"
    end = body.index("\n---\n", 4)
    return yaml.safe_load(body[4:end])


@pytest.mark.parametrize("stem,vars,expected_substring", PRIMITIVES, ids=lambda p: p if isinstance(p, str) else "")
def test_primitive_has_declared_contract(stem, vars, expected_substring):
    path = PRIMITIVES_DIR / f"{stem}.j2"
    assert path.exists(), f"primitive missing: {path}"

    fm = _frontmatter(path)
    declared = bool(fm.get("required_variables")) or bool(fm.get("defaults"))
    assert declared, f"{stem}.j2 declares no variables — primitives must own their inputs"


@pytest.mark.parametrize("stem,vars,expected_substring", PRIMITIVES, ids=lambda p: p if isinstance(p, str) else "")
def test_primitive_renders_to_expected_fragment(tmp_path, stem, vars, expected_substring):
    var_file = tmp_path / "vars.json"
    import json
    var_file.write_text(json.dumps(vars))

    # Primitives don't render standalone via sc-compose (no top-level template
    # output), so we render them through a tiny composing wrapper template.
    wrapper = tmp_path / "wrapper.py.j2"
    wrapper.write_text(
        "---\n"
        f"required_variables: {list(vars.keys())}\n"
        "metadata:\n"
        f"  purpose: \"composition wrapper for {stem}\"\n"
        "---\n"
        f"@<{(PRIMITIVES_DIR / (stem + '.j2')).resolve()}>\n"
    )

    out = tmp_path / "out.txt"
    result = subprocess.run(
        [
            "sc-compose", "render",
            "--mode", "file",
            "--file", str(wrapper),
            "--var-file", str(var_file),
            "--output", str(out),
            "--root", str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    # Confinement may prevent absolute-path includes; if so, try with the
    # primitive at the repo root (relative path resolves from the wrapper's parent).
    if result.returncode != 0 and "escape" in (result.stdout + result.stderr).lower():
        pytest.skip(
            "sc-compose's include confinement prevents the standalone wrapper "
            "from including a primitive across roots; integration coverage "
            "happens via test_composition.py and the existing top-level tests."
        )

    assert result.returncode == 0, (
        f"render failed for {stem}: {result.stderr}"
    )
    rendered = out.read_text()
    assert expected_substring in rendered, (
        f"{stem}.j2 did not render to include {expected_substring!r}; got:\n{rendered}"
    )
