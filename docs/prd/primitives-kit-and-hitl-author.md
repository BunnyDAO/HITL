# Primitives Kit + `/hitl-author` skill + audience-split docs

## Problem Statement

The current system (PRD: `agentic-hitl-test-generator.md`, slices 0001–0009) ships three top-level templates a test engineer can render via `/hitl-test`. If the engineer needs a *new* test shape — one not covered by the three — they have no path forward inside the system. Their options are: ask a developer to author a template by hand, or describe the test in free-form English and hope someone implements it correctly. Both bypass the "the contract is the template" property the rest of the system rests on.

Test engineers are non-programmers. They need an authoring path that is **as constrained as the consumption path** — they should not be exposed to free-form Python, and the agent should not freely emit Python on their behalf. Whatever they produce must be reviewable by a developer using the same "one template per PR" model the existing flow established.

A second, mostly orthogonal problem: the current `README.md` is dev-focused; the `docs/sop.md` is dev-focused. A test engineer who walks into the repo cold has no doc tuned to their vocabulary. The pitch "non-programmer test engineers can use this" is unsupported by any reading material aimed at non-programmers.

## Solution

Two coordinated changes:

**1. A primitives kit.** A small library of sub-template fragments at `templates/primitives/*.j2`, each declaring its own YAML frontmatter contract. Test engineers learn the kit's vocabulary directly (no "test shapes" abstraction layer in front of it). Top-level templates — both the three we already shipped and any new ones — compose from primitives via sc-compose's `@<path>` include directive, which merges required-variable declarations across the include graph per its FR-3a spec.

The existing three top-level templates (`vision-centroid`, `vision-multi-assert`, `smoke-test`) get refactored to use primitives, so the kit isn't a theoretical promise — it expresses every template we currently ship.

**2. A `/hitl-author` Claude Code skill.** Parallel in shape to `/hitl-test` but for *authoring* new top-level templates rather than rendering existing ones. The engineer answers structured `AskUserQuestion` prompts about which primitives their test needs and in what order; the skill composes a new `templates/<name>.py.j2` that `@<...>`-includes those primitives. The output is a real, reusable template file that goes into git, gets PR-reviewed like any other code change, and shows up in `/hitl-test`'s discovery list on next render.

When no primitive combination fits, the skill refuses politely and writes `issues/primitive-requests/<slug>.md` describing the missing primitive — turning vague "we should add more" gripes into actionable requests.

Documentation is reorganized so each audience reads a doc written in their vocabulary: `README.md` becomes a short front door pointing readers to the right doc; `docs/sop.md` stays as the developer/architecture doc; new `docs/test-engineer-guide.md` is a non-programmer's manual.

## User Stories

1. As a **test engineer**, I want to invoke `/hitl-author` and pick from a list of primitives in plain language, so I can describe a new test shape without writing or reading Python.
2. As a **test engineer**, I want the skill to explain in each primitive's menu entry what that primitive *does* in operational terms ("show a pattern on the display and capture an image", "check that a centroid lands within tolerance"), so I can choose without learning the underlying API.
3. As a **test engineer**, I want to compose primitives in an order I control (setup → capture → assertion), so the resulting test reads like the sequence of steps I'd describe to a colleague.
4. As a **test engineer**, I want the rendered template to be a real file in `templates/` that I (or a teammate) can re-render later with different variables via `/hitl-test`, so my work is reusable rather than one-shot.
5. As a **test engineer**, I want the skill to refuse politely when no primitive fits my description and write a request file describing what I needed, so I'm not left with an approximate test that silently does the wrong thing.
6. As a **test engineer**, I want a guide written in non-programmer language that explains what a primitive is, when to use `/hitl-test` vs `/hitl-author`, and what to do when the kit doesn't cover my case, so I can onboard without asking a developer.
7. As a **developer**, I want the new top-level templates to land in `templates/` with an embedded authoring-trail comment block (engineer's intent, primitives picked, timestamp), so PR review compares *intent* to *output* at a glance.
8. As a **developer**, I want each primitive to declare its own YAML frontmatter so sc-compose can merge required variables across the include graph automatically, so adding a primitive doesn't require touching any composing template.
9. As a **developer**, I want the existing three top-level templates refactored to use primitives, so the kit is proven against shapes we already ship — not just a theoretical promise.
10. As a **developer**, I want primitive-request files to land in `issues/primitive-requests/` with a predictable shape (the engineer's intent + the missing API surface), so I can pick up real demand on the next sprint instead of guessing what to add.
11. As a **developer reading the SOP**, I want a new section explaining the primitives kit, the composition mechanism, and the `/hitl-author` flow, so I understand the architecture as a whole rather than as the original three-layer model plus a bolted-on appendix.
12. As a **maintainer**, I want the existing 28-test suite to continue passing after the refactor, so the template-refactor work doesn't silently break what we already ship.
13. As a **maintainer**, I want lint tests on each primitive (frontmatter declares variables; primitive renders to a non-empty fragment) and on `/hitl-author`'s SKILL.md (similar pattern to `test_skill_doc.py`), so drift between SKILL.md, primitives, and the kit's actual capabilities is caught early.
14. As a **dev lead**, I want the README to act as a front door directing developers to `docs/sop.md` and test engineers to `docs/test-engineer-guide.md` in the first paragraph, so people don't waste minutes reading the wrong doc.
15. As a **dev lead**, I want a one-paragraph "what counts as a constraint violation" section in the SOP that explains why `/hitl-author` refuses certain requests, so I can defend the design when stakeholders push for "just let the agent do it".

## Implementation Decisions

### The primitives kit

Four primitives ship in the starter kit, all at `templates/primitives/<name>.j2` (note: `.j2`, not `.py.j2` — they're fragments, not standalone Python files):

- **`setup_preamble.j2`** — emits the Python imports every HITL test needs (`pytest`, `assertions as hitl_assert`, `camera`, `display`) plus the `def test_{{ test_name }}(hitl_fixture):` line. Declares `test_name` in its frontmatter.
- **`pattern_capture.j2`** — emits two indented lines: `display.show("{{ display_pattern }}")` followed by `image = camera.capture(delay_ms=..., retries=...)`. Declares `display_pattern` as required; provides defaults for `capture_delay_ms` and `retries`.
- **`assert_centroid.j2`** — emits one `hitl_assert.centroid_within(image, target=(...), tolerance_px=...)` call. Declares `target_x`, `target_y`, `tolerance_px`.
- **`assert_intensity.j2`** — emits one `hitl_assert.pixel_intensity_above(image, threshold=...)` call. Declares `intensity_threshold`.

Naming convention: `<verb>_<noun>.j2`. Primitives are **stateless about ordering** — composing `assert_centroid` before `pattern_capture` produces broken Python, but that's a composition-time concern; the primitives themselves don't enforce ordering. The `/hitl-author` skill knows the conventional order (setup → capture → assertions).

### Composition mechanism

sc-compose's literal `@<primitives/setup_preamble.j2>` directive. Per sc-compose's FR-3a, required-variable declarations from included files merge upward into the using template's required set, so the composing template doesn't need to repeat what each primitive already declared.

A new composing template's body is just a sequence of `@<primitives/X.j2>` lines plus an authoring-trail comment block at the top.

### `/hitl-author` skill

Lives at `.claude/skills/hitl-author/SKILL.md`. Same single-stage interrogator shape as `/hitl-test` (one SKILL.md, no stage machinery). Flow:

1. **Preflight** — confirm `sc-compose`, `templates/primitives/`, and `.venv` exist.
2. **Test name** — ask the engineer for a snake_case name for the new test shape. This becomes the new template's filename stem.
3. **Pick primitives** — present the four primitives as a multi-select `AskUserQuestion` (engineer can pick 1–4). The skill knows the conventional order; it sorts the picked primitives into setup → capture → assertions order automatically.
4. **Walk merged variables** — for each variable the composed primitive set declares as required, ask one `AskUserQuestion` (re-using `/hitl-test`'s walker — the variable-walking is shared logic, not duplicated). Engineers see only the variables their picked primitives need.
5. **Author the template** — write `templates/<test_name>.py.j2` with:
   - YAML frontmatter declaring `required_variables` (the union from all picked primitives, deduplicated) and `metadata.purpose` derived from the engineer's intent
   - An authoring-trail comment block at the top: who authored, when, the engineer's described intent, the chosen primitives
   - A body that is `@<primitives/X.j2>` lines in the conventional order
6. **No-primitive-fits case** — if the engineer indicates none of the primitives match their intent, the skill writes `issues/primitive-requests/<test_name>-<timestamp>.md` describing the intent and the missing API surface, and exits cleanly without writing a template.
7. **Optional render** — offer to immediately render the new template via `/hitl-test` so the engineer sees their shape execute. Decline = exit cleanly with the file path.

### Existing-template refactor

`vision-centroid.py.j2`, `vision-multi-assert.py.j2`, and `smoke-test.py.j2` are rewritten to use only primitive `@<...>` includes plus their own frontmatter declaring `metadata.purpose`. The rendered output of each must be byte-identical (modulo whitespace) to the pre-refactor version — the 28-test suite is the regression net.

`vision-multi-assert` is a slight exception: its Jinja `{% for %}` loop over `assertion_kinds`/`assertion_kwargs` still lives in the composing template body because the loop is structural, not snippet-level. The primitives the loop body emits are still kit-derived calls (e.g. `hitl_assert.{{ kind }}(image, {{ kwargs }})`).

### Documentation

- **`README.md`** — rewritten as a short front door. First paragraph names the two audience docs explicitly. Keep the Getting Started section (it works for both audiences), but trim the dev-flavored content and link out for depth.
- **`docs/sop.md`** — extended with new sections covering the primitives kit (what it is, how composition works), the `/hitl-author` flow, the review story, and the "no primitive fits" failure mode. Continues to be the developer/architecture doc.
- **`docs/test-engineer-guide.md`** — new. Audience: a non-programmer test engineer who has Claude Code installed and the repo cloned. Sections: what this is (in one paragraph, no Python jargon), what's a primitive, how to use `/hitl-test`, how to use `/hitl-author`, what to do when the kit doesn't fit, how to know your test ran correctly.
- **`docs/deck.md`** — unchanged. The 10-minute pitch already covers the constraint argument; adding the kit changes the architecture diagram but not the headline. (Listed under Out of Scope below for explicit deferral.)

### Skill recommendation tweak

A small note from the live test: `/hitl-test`'s template picker currently makes `smoke-test` the Recommended option (alphabetical first). That's a worse default than `vision-centroid` for a demo. Update SKILL.md's discovery rule to prefer `vision-centroid` when present, otherwise alphabetical-first.

## Testing Decisions

Three new test files, plus the existing 28-test suite as the regression net.

1. **`tests/test_primitives.py`** — for each `.j2` file in `templates/primitives/`:
   - parses frontmatter cleanly
   - declares at least one variable in `required_variables` OR declares a non-empty `defaults` map
   - renders to a non-empty fragment when given a known-valid mini-var-set
   - the fragment's Python (when sliced out of a context that supplies the surrounding `def`) parses with `ast.parse`

2. **`tests/test_composition.py`** — for each refactored top-level template:
   - renders successfully via `sc-compose render` with the existing `vars.*.json`
   - the rendered output parses with `ast.parse`
   - the existing `vars.example.json`/`vars.multi-assert.json`/`vars.smoke.json` still produce passing tests under pytest (this is the regression check — it's nearly the same as the existing `test_template_render.py` but adds the explicit "post-refactor still green" assertion)

3. **`tests/test_hitl_author_doc.py`** — mirrors `test_skill_doc.py`:
   - SKILL.md exists at `.claude/skills/hitl-author/SKILL.md`
   - SKILL.md mentions every primitive's filename stem
   - SKILL.md references the `issues/primitive-requests/` path for the no-fit case
   - SKILL.md instructs use of `AskUserQuestion`
   - SKILL.md is under the 1200-word read budget

The existing `tests/test_skill_doc.py` continues to lint `/hitl-test`'s SKILL.md unchanged; the existing `tests/test_template_render.py` continues to render-smoke the three top-level templates (which now happen to compose from primitives).

The `/hitl-author` skill's execution itself is LLM-mediated and not unit-testable in a useful way, same as `/hitl-test`. The SOP gets a new walkthrough-checklist step for verifying `/hitl-author` after edits.

## Out of Scope

- **Adding new primitives beyond the starter kit of four.** Adding `capture_with_retry`, time-series primitives, audio/motion modalities — all explicitly deferred. The starter kit is meant to prove the *pattern*, not be a comprehensive catalog. Real demand for new primitives flows through `issues/primitive-requests/`.
- **Updating `docs/deck.md`.** The deck already lands the constraint argument; the kit changes the architecture diagram but doesn't change the deck's headline. If the deck gets reused after this expansion, a single slide update can be a follow-up.
- **Mechanically enforcing PR review.** The SOP describes PR review as the operational gate; this repo doesn't have a remote configured, and we're not building a CI workflow to enforce it. That's a real-deployment concern.
- **A primitives catalog reference doc.** Each primitive's contract is visible in its own frontmatter; until the kit grows past ~6 primitives, a dedicated catalog doc is overhead. Defer.
- **Backwards compatibility shims.** The refactored templates produce equivalent (not byte-identical, modulo whitespace) output. We won't keep the old inline-imports versions around as fallbacks.
- **Migrating engineer-authored templates between primitive versions.** If a primitive's contract changes, engineer-authored templates may need updating — that's a real-life concern but not in scope for this round.

## Further Notes

- The `/hitl-author` skill should not become a second source of variable-walking logic; the variable-walking instructions in its SKILL.md should reference `/hitl-test`'s SKILL.md as the shared spec rather than re-state it. Both skills walk variables the same way.
- The authoring-trail comment block at the top of engineer-authored templates is the demo's central audit moment. Format suggested:
  ```
  # ────────────────────────────────────────────────────────────────────
  # Authored via /hitl-author on YYYY-MM-DD by <engineer@example.com>
  # Intent: <one-line description the engineer gave>
  # Primitives: setup_preamble → pattern_capture → assert_centroid
  # Review: PR before merging into templates/
  # ────────────────────────────────────────────────────────────────────
  ```
  The reviewing developer reads this *first*, then reads the body to confirm the body matches the intent.
- The `test-engineer-guide.md` should NOT explain the underlying mechanics (Jinja, sc-compose's include resolver, pytest fixtures). Test engineers don't need that. The SOP covers it for developers.
- The grilling session confirmed test engineers see "primitives" directly rather than going through a "test shapes" abstraction. The vocabulary in `docs/test-engineer-guide.md` should reflect this — "primitives" is fine if explained well; we don't need to invent softer language ("building blocks" / "steps" are reasonable synonyms but pick one and stick with it).
- The four starter primitives have asymmetric size: `setup_preamble` and `pattern_capture` are multi-line fragments, while the two `assert_*` primitives are single-line calls. This is fine — primitives are about *what concept they encapsulate*, not about line count.
