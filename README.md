# Agentic HITL Test Generator — worked example

A teaching repo that demonstrates how four moving parts — a mock fixture library, a kit of sc-compose template primitives, and two Claude Code skills (`/hitl-test` and `/hitl-author`) — let non-programmer test engineers both **run** and **design** real Python tests through a constrained conversation. Runs end-to-end on a laptop with no real hardware.

## Pick your path

- **You write code** (developer, dev lead, maintainer) → **[`docs/sop.md`](docs/sop.md)** — the architecture doc. ~20 minutes.
- **You don't write code** (test engineer, QA, anyone using `/hitl-test` or `/hitl-author`) → **[`docs/test-engineer-guide.md`](docs/test-engineer-guide.md)** — the user manual. ~10 minutes.
- **You're presenting this to a team** → **[`docs/deck.md`](docs/deck.md)** — Marp slide deck, ~10 minutes to present.

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

To use the agentic flows: open this directory in Claude Code, start a fresh session, and type `/hitl-test` or `/hitl-author`. See [`docs/test-engineer-guide.md`](docs/test-engineer-guide.md) for what each skill does.

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
  sop.md                      Developer/architecture doc.
  test-engineer-guide.md      Non-programmer user manual.
  deck.md                     Marp slide deck.
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
