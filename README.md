# Agentic HITL Test Generator — worked example

A teaching repo that demonstrates how four layers — a mock fixture library (Layer 1), a kit of sc-compose template primitives (Layer 2), and two Claude Code skills (`/hitl-test` as Layer 3, `/hitl-author` as Layer 4) — let Non-Developer test engineers both **run** and **design** real Python tests through a constrained conversation. Runs end-to-end on a laptop with no real hardware.

## Pick your path

The full story lives in **[`docs/sop.md`](docs/sop.md)** — one doc, ordered so each audience can stop where they need to.

- **Test engineers / non-programmers** → read [What this project does](docs/sop.md#what-this-project-does) through [Reading test results](docs/sop.md#reading-test-results). ~10 minutes; no Python required.
- **Developers / maintainers** → continue past that into [How it works](docs/sop.md#how-it-works--the-three-layers) for the architecture, mermaid diagrams, and the manual walkthrough checklist. ~20 minutes total.
- **Presenters** → **[`docs/deck.md`](docs/deck.md)** is the Marp slide deck for a 10-minute team pitch.

## How it works — the four layers

The system has four main layers. Layers 3 and 4 are the Claude skills the user actually interacts with.

**Layer 1 — `hitl_lib/`** — Straight Python functions for system control: `camera.capture()`, `display.show(pattern)`, and so on. In a real deployment these would be replaced with real API calls or direct source-code calls into the device under test.

**Layer 2 — `templates/*.py.j2`** — sc-compose templates with YAML frontmatter declaring required variables and defaults. There are example templates in this repo (`smoke-test`, `vision-centroid`, `fgr-uniformity`, etc.). In practice a real deployment would have templates for things like POIs, FGR, and other domain-specific test shapes.

**Layer 3 — `/hitl-test`** — A Claude skill that the Non-Developer actually uses day-to-day. It picks an existing template from Layer 2, walks the user through that template's required variables one question at a time, writes a JSON file combining the variables with the user's answers, lets sc-compose verify the JSON against the template's contract, and renders a runnable pytest `.py` file. This is what a Non-Developer uses day-to-day once the right templates exist.

This accomplishes the **first goal**: spinning up a custom pytest `.py` on-the-fly from a pre-built template. For example — if a template called `fgr_roi_variance_check` exists, the Non-Developer runs `/hitl-test`, picks that template, answers a few questions ("What FGR method should be used for registering the pixels?", "Lv tolerance to find the pixels?", "Lv allowed variance % of the pixels?") that are the chosen template's variables, and out the other side is a runnable pytest `.py` that triggers the FGR, iterates the ROIs, runs the variance check on each, and reports pass/fail. No code written by the Non-Developer.

**Layer 4 — `/hitl-author`** (grouped with Layer 3 in [`docs/sop.md`](docs/sop.md)) — A second Claude skill for creating additional templates for Layer 2 from a collection of new primitives — or by mixing and matching primitives from previous templates to fit the current need. The SOP explains how to compose these.

This accomplishes the **second goal**: getting a template like `fgr_roi_variance_check` to exist in the first place — when no developer has hand-written it yet — is what Layer 4 (`/hitl-author`) is for. If the right primitives are in the kit (e.g. `fgr_trigger`, `roi_select`, `pixel_variance_check`), the Non-Developer can compose them into a new template via `/hitl-author` themselves. If those primitives don't exist yet, that's a developer task — and `/hitl-author` writes a structured request so the developer knows exactly what to add.

### Why two skills, not one

**Important distinction:** `/hitl-test` (Layer 3) only varies the *values* (tolerance, pattern, target coordinates, etc.) of an existing template. It cannot change the test's structure — which checks run, in what order, against what capture. If the Non-Developer needs a truly unique test — different primitives, different order, different combination of checks — `/hitl-author` (Layer 4) is the only path. That's the architectural reason there are two skills, not just two prompts.

### Scope going forward

The near-term focus is the templates (shapes) and the collection of primitives explicitly required for the first production deployment. In-progress functional-requirements work should identify the primitives needed, which can then be composed into an organized set of Layer 2 templates.

## Getting started

Prerequisites: macOS or Linux with [Homebrew](https://brew.sh), Python 3.11+, and [Claude Code](https://claude.com/claude-code).

```bash
# 1. Install sc-compose (the deterministic template renderer — a Rust CLI).
brew install randlee/tap/sc-compose

# 2. Set up the Python environment.
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# 3. Run the hand-rendered demos (no agent involved).
make demo            # vision-centroid: centroid alignment, passes
make demo-multi      # multi-assertion: loops over checks
make demo-smoke      # smoke-test: minimal device-alive
make demo-authored   # engineer-authored example template
make demo-fgr        # FGR cross-ROI uniformity (display-metrology example)

# 4. Run the repo's own test suite (62 tests + 6 skipped, ~1s).
make test
```

To use the agentic flows: open this directory in Claude Code, start a fresh session, and type `/hitl-test` or `/hitl-author`. See [Using `/hitl-test`](docs/sop.md#using-hitl-test--render-an-existing-test) and [Using `/hitl-author`](docs/sop.md#using-hitl-author--design-a-new-test) in the SOP for what each skill does.

## Repo layout

```
hitl_lib/                    Mock fixture library (camera, display, assertions).
                             Real numpy math on synthetic dot patterns.

templates/
  vision-centroid.py.j2       Centroid alignment test    (composes from kit)
  vision-multi-assert.py.j2   Multi-assertion sequence   (composes from kit + Jinja loop)
  smoke-test.py.j2            Device-alive check         (composes from kit)
  centroid-with-intensity.py.j2  Engineer-authored example
  fgr-uniformity.py.j2        FGR cross-ROI uniformity   (display-metrology domain example)
  primitives/                 The kit (6 sub-template fragments)
    setup_preamble.j2          imports + def line
    pattern_capture.j2         display.show + camera.capture
    assert_centroid.j2         centroid_within call
    assert_intensity.j2        pixel_intensity_above call
    tile_rois.j2               roi.tile into a grid of ROIs
    assert_roi_uniformity.j2   cross-ROI uniformity check

.claude/skills/
  hitl-test/SKILL.md          Skill: render an existing template
  hitl-author/SKILL.md        Skill: author a new template from primitives

docs/
  sop.md                      The single reference doc — both audience paths.
  deck.md                     Marp slide deck for presentations.
  prd/                        Design history (PRDs).

issues/                      Implementation history (vertical slices 0001..0018)
                             plus issues/primitive-requests/ for kit-extension requests.

tests/                       62 tests + 6 skipped; ~1s. Run with `make test`.
vars.*.json                  Example var sets — used by both `make demo*` and tests.
Makefile                     `make demo*`, `make test`.
```

## What this is not

- **Real-hardware code.** The fixture library is mocked. `camera.capture()` returns a seeded-jitter dot pattern, not a real image.
- **A production framework.** This is a worked example, not a library to depend on. Take the pattern, leave the code.
- **Coupled to vision.** The catalog is mostly vision-flavored toys (dot, centroid), but `fgr-uniformity` is a real display-metrology example precisely to show the pattern is domain-agnostic. Adapting it to audio, motion, or any other domain is a SOP section.

## License

TODO — add a LICENSE file before sharing externally.
