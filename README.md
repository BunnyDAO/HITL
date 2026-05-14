# Agentic HITL Test Generator — worked example

A teaching repo that demonstrates how four moving parts — a mock fixture library, a kit of sc-compose template primitives, and two Claude Code skills (`/hitl-test` and `/hitl-author`) — let non-programmer test engineers both **run** and **design** real Python tests through a constrained conversation. Runs end-to-end on a laptop with no real hardware.

## Pick your path

The full story lives in **[`docs/sop.md`](docs/sop.md)** — one doc, ordered so each audience can stop where they need to.

- **Test engineers / non-programmers** → read [What this project does](docs/sop.md#what-this-project-does) through [Reading test results](docs/sop.md#reading-test-results). ~10 minutes; no Python required.
- **Developers / maintainers** → continue past that into [How it works](docs/sop.md#how-it-works--the-three-layers) for the architecture, mermaid diagrams, and the manual walkthrough checklist. ~20 minutes total.
- **Presenters** → **[`docs/deck.md`](docs/deck.md)** is the Marp slide deck for a 10-minute team pitch.

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

# 4. Run the repo's own test suite (45 tests, ~1s).
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
  primitives/                 The kit (4 sub-template fragments)
    setup_preamble.j2          imports + def line
    pattern_capture.j2         display.show + camera.capture
    assert_centroid.j2         centroid_within call
    assert_intensity.j2        pixel_intensity_above call

.claude/skills/
  hitl-test/SKILL.md          Skill: render an existing template
  hitl-author/SKILL.md        Skill: author a new template from primitives

docs/
  sop.md                      The single reference doc — both audience paths.
  deck.md                     Marp slide deck for presentations.
  prd/                        Design history (PRDs).

issues/                      Implementation history (vertical slices 0001..0015)
                             plus issues/primitive-requests/ for kit-extension requests.

tests/                       45 tests; ~1s. Run with `make test`.
vars.*.json                  Example var sets — used by both `make demo*` and tests.
Makefile                     `make demo*`, `make test`.
```

## What this is not

- **Real-hardware code.** The fixture library is mocked. `camera.capture()` returns a seeded-jitter dot pattern, not a real image.
- **A production framework.** This is a worked example, not a library to depend on. Take the pattern, leave the code.
- **Coupled to vision.** Four vision-flavored templates ship as a teaching catalog. Adapting the pattern to audio, motion, or any other domain is a SOP section.

## License

TODO — add a LICENSE file before sharing externally.
