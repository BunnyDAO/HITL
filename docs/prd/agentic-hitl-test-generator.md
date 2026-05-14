# Agentic HITL Test Generator — Worked Example

## Problem Statement

A dev lead wants to evaluate the pattern of using a deterministic text-generator (sc-compose) plus a Claude Code skill (Valkyrie-style interrogator) plus a domain-specific fixture library to let non-programmers — specifically test engineers — generate real, runnable test code from natural-language conversation.

They don't have a worked example to show their team. The available material is conceptual (the sc-compose README, the Valkyrie skill source). A team meeting where someone says "imagine if…" is unconvincing; a 5-minute laptop demo that ends with `pytest` showing a real pass/fail mix is convincing. The dev lead needs the second thing.

## Solution

A self-contained repository that demonstrates the full pattern end-to-end on a laptop, with mocked camera/display hardware so nothing physical is required. A dev lead can clone it, run `pip install -r requirements.txt`, invoke `/hitl-test` inside Claude Code, answer a handful of conversational prompts, and watch a real `.py` test file get rendered and executed — with the test's pass/fail outcome correlating directly to a `tolerance_px` value they typed in.

Alongside the runnable example, an architecture-doc SOP and a Marp slide deck explain how the three layers (fixture library, sc-compose templates, agent skill) fit together, so the dev lead can walk a team or stakeholder through the pattern in 10 minutes.

The pattern itself stays narrow — no real-hardware migration story, no productionizing appendix. The reader should grok the *shape* and imagine the migration for themselves.

## User Stories

1. As a **dev lead evaluating the pattern**, I want to clone the repo, run one install command, and have a working environment, so that I can demo the pattern in a meeting without preflight friction.
2. As a **dev lead in a meeting**, I want to invoke `/hitl-test` and have it list the available templates clearly, so that the audience sees the constrained surface area before any code is generated.
3. As a **dev lead**, I want the skill to ask me one structured question at a time (using AskUserQuestion), so that the audience sees the agent doing focused interrogation rather than open-ended chat.
4. As a **dev lead**, I want the skill to refuse to render if I omit a required variable, so that I can demonstrate sc-compose's "fail loud, fail early" contract live.
5. As a **dev lead**, I want the generated test file to be saved to a predictable location (`tests/generated/`), so that I can `cat` it on screen and then run `pytest` against it without hunting.
6. As a **dev lead**, I want `pytest` on the generated file to produce a *meaningful* pass/fail outcome — not a canned result — so that the audience sees the demo is real, not a mockumentary.
7. As a **dev lead**, I want to be able to re-run `/hitl-test` with a tighter `tolerance_px` and watch the test flip from pass to fail, so that I can demonstrate how the agent-supplied variable propagates all the way to runtime behavior.
8. As a **dev lead reading the SOP**, I want a single-page architecture diagram showing the three layers and the data flow between them, so that I have a printable artifact to send to skeptics.
9. As a **dev lead reading the SOP**, I want a verbatim transcript of a `/hitl-test` invocation embedded in the doc, so that someone who can't run the demo can still see what the conversation looks like.
10. As a **dev lead presenting the Marp deck**, I want fewer than 12 slides and at least 2 mermaid diagrams, so that I can deliver the pitch in 10 minutes with no slide feeling content-thin.
11. As a **dev reviewing the skill source**, I want the `SKILL.md` to be readable end-to-end in five minutes, so that I can adapt the pattern to my own domain (audio tests, motion tests, etc.) without reverse-engineering anything clever.
12. As a **dev reviewing the templates**, I want at least one template to demonstrate the `@<path>` include mechanism, so that I can see the multi-template scaling story rather than just one-off generation.
13. As a **dev reviewing the fixture library**, I want the centroid math to be real numpy code — not a stub returning a hardcoded boolean — so that I trust the "mock at the hardware boundary, real everywhere else" framing.
14. As a **dev**, I want `pip install -r requirements.txt` to pin sc-compose to a specific commit SHA, so that an upstream API change doesn't silently break the demo six months from now.
15. As a **future maintainer**, I want a `README.md` at the repo root that says "start here → docs/sop.md," so that new arrivals don't waste time excavating the layout.

## Implementation Decisions

### Modules

- **`hitl_lib.camera`** — Mock camera. Exposes `capture(delay_ms: int = 500, retries: int = 3) -> np.ndarray`. Reads the current pattern from `hitl_lib.display`, renders a synthetic grayscale image with the appropriate dot pattern and deterministic jitter (seeded PRNG). Jitter magnitude is tunable so the same template can produce tests that pass at `tolerance_px=5` and fail at `tolerance_px=1`.
- **`hitl_lib.display`** — Logging-only "display" that holds the currently-shown pattern in module-level state. Exposes `show(pattern: str)` and `current() -> str`. No graphics — the camera reads `current()` to know what to "see."
- **`hitl_lib.assertions`** — Real assertion functions on numpy arrays. `centroid_within(image, target, tolerance_px)` computes the image moments-based centroid and raises `AssertionError` if the distance exceeds tolerance. `pixel_intensity_above(image, threshold)` does the obvious thing. Both raise informative messages so generated tests fail readably.
- **`hitl_lib.fixtures`** — Pytest fixture `hitl_fixture` that resets `display` state, seeds the camera PRNG, and yields a namespace exposing the three submodules. Generated tests take `hitl_fixture` as their only parameter.

### Templates (`templates/`)

All three templates have sc-compose frontmatter declaring `required_variables` and `defaults`. The skill validates against this contract before rendering.

- **`vision-centroid.py.j2`** — Single test: show pattern → capture → assert centroid within tolerance. Required vars: `test_name`, `display_pattern`, `target_x`, `target_y`, `tolerance_px`. Optional: `capture_delay_ms` (default 500), `retries` (default 3).
- **`vision-multi-assert.py.j2`** — Same shape, but loops over an `assertions` list of `{kind, params}` dicts. Demonstrates the `{% for %}` mechanism and how the agent can build structured lists from conversation.
- **`smoke-test.py.j2`** — Minimal "device alive" test. Uses sc-compose's `@<path>` include to pull in `_shared_setup.j2` (imports + fixture call). Required vars: `test_name` only. The point is to show fragment reuse, not to be a serious smoke test.
- **`_shared_setup.j2`** — The included fragment. Just the imports block and the fixture parameter declaration. Demonstrates how templates would share a common preamble across a family.

### `/hitl-test` skill (`.claude/skills/hitl-test/SKILL.md`)

Single-stage. On invocation:

1. List the three templates by name + one-line description from each frontmatter's `metadata.purpose`. Ask the engineer to pick one (`AskUserQuestion` with the three options).
2. Read the picked template's frontmatter. For each entry in `required_variables`, ask one structured question. Use `defaults` for hint text. Free-text responses are coerced to the right type (ints get parsed; strings stay strings).
3. After the last question, render the variables to a JSON file in a tempdir, then invoke `sc-compose render <template> --var-file <json>` as a subprocess. If sc-compose's exit code is non-zero, surface stderr verbatim (so the user sees the "missing required variable: foo" message live — this is part of the demo).
4. Write the rendered output to `tests/generated/test_<test_name>.py`.
5. Ask whether to run `pytest tests/generated/test_<test_name>.py` now. If yes, run and show output. If no, exit cleanly with the file path.

The skill does *not* implement its own validation logic — sc-compose is the single source of truth on the contract. The skill just feeds it inputs.

### Dependencies

sc-compose is a Rust CLI (binary), not a Python package — confirmed by reading the upstream README at https://github.com/randlee/sc-compose. It cannot be installed via `pip`. The README documents `brew install randlee/tap/sc-compose` as a prerequisite (macOS), `winget install randlee.sc-compose` on Windows, or `cargo install --path crates/sc-compose` from source. The repo pins to whatever version brew currently serves (v1.0.0 at time of writing); the README mentions the version and tells future maintainers how to pin if reproducibility ever bites.

`requirements.txt` covers only the Python deps:
- `numpy>=1.26,<3`
- `pytest>=8,<9`

Marp-cli is a dev-tool dep, not a runtime dep — documented in the SOP but not in `requirements.txt`.

### CLI surface

The verified sc-compose invocation for our case (`--mode file`, since we author templates in `templates/` not as agent profiles):

```
sc-compose render --mode file --file templates/vision-centroid.py.j2 \
                  --var-file vars.example.json \
                  --output tests/generated/test_demo.py
```

`--mode profile` exists for agent/skill/command profiles resolved through runtime search chains; we don't use it.

### Layout

```
HITL/
  hitl_lib/
    __init__.py
    camera.py
    display.py
    assertions.py
    fixtures.py
  templates/
    vision-centroid.py.j2
    vision-multi-assert.py.j2
    smoke-test.py.j2
    _shared_setup.j2
  .claude/skills/hitl-test/
    SKILL.md
  docs/
    sop.md
    deck.md
    prd/agentic-hitl-test-generator.md
  tests/
    test_assertions.py        # unit tests on centroid math
    test_template_render.py   # render-smoke tests
    generated/                # gitignored; demo output lands here
  requirements.txt
  README.md
  conftest.py                 # registers hitl_fixture
  pyproject.toml              # python>=3.11, package config
  .gitignore
```

## Testing Decisions

Three test layers, each testing **external behavior** of the corresponding deep module:

1. **`tests/test_assertions.py`** — unit tests on `hitl_lib.assertions`. Feed in known numpy arrays (synthetic dot at known position), confirm `centroid_within` raises or doesn't raise according to the tolerance. This is the *one* place we test "is the math right" — if this passes, generated tests can trust the assertion layer.
2. **`tests/test_template_render.py`** — render-smoke tests. For each of the three templates, render with a known-valid var set and confirm the output is syntactically valid Python (compile via `ast.parse`). Catches template-level mistakes (unbalanced braces, malformed Jinja) without needing to execute the generated test.
3. **`tests/generated/test_*.py`** — the demo output. Not pre-committed; produced by the skill. Run via `pytest` as the closing beat of the demo. The "wow moment" is that these tests are real and their pass/fail outcome maps to the `tolerance_px` value the user typed.

The skill itself is LLM-mediated and not unit-testable in a useful way. The SOP includes a manual walkthrough checklist for verifying it behaves correctly after edits.

Prior art: this is structurally the same pattern as `to-issues` testing in Valkyrie — the deep modules (template rendering, assertion math) get real tests; the LLM-driven orchestration gets a manual checklist.

## Out of Scope

- **Real hardware support.** No pluggable backend, no `RealCamera` skeleton, no comments speculating about it. Stay narrow on the pattern.
- **Multiple modalities.** No audio or motion templates. Three vision-flavored templates is the catalog.
- **CI workflow.** No GitHub Actions, no `pre-commit` config. The demo is laptop-only.
- **Multi-runtime parity.** Skill is Claude Code only. No Codex profile, no agent-runtime abstraction. Mentioned in the SOP as a future direction but not implemented.
- **Test execution beyond pytest.** No HTML reports, no JUnit XML, no allure. Plain pytest output.
- **License + copyright headers.** TODO left in README; can be added later.
- **`pyproject.toml` as an installable package.** It exists so editable-mode `pip install -e .` works during development, but we're not publishing to PyPI.

## Further Notes

- The deck (Marp) should have at most ~12 slides. Two mermaid diagrams minimum: (1) the three-layer architecture, (2) the data flow from "engineer says X" through the agent → JSON → sc-compose → `.py` file → pytest. A third "what sc-compose actually contributes" slide is high-value if space allows.
- The SOP should open with a 2-paragraph TL;DR ("what this is, why it exists") so a dev lead can skim and decide if it's worth reading further.
- The SOP's worked-transcript section should reproduce a real `/hitl-test` interaction verbatim, including the AskUserQuestion menus. This is the doc's most persuasive section — readers who don't run the demo still see what the conversation feels like.
- The `vision-centroid` template should be tuned so the **default** `tolerance_px=2` produces a *failing* test (jitter magnitude ~3px), and `tolerance_px=5` produces a passing one. This gives the demo its central "watch me change one number and see the test flip" beat.
- All templates and fixture code target Python 3.11+. `from __future__ import annotations` not needed.
- `_shared_setup.j2` should be ~10 lines max. Its purpose is to show the mechanism, not to be a serious shared library.
