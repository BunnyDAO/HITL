# /hitl-author — design a new HITL test shape from the primitives kit

A Claude Code skill that lets a non-programmer test engineer **author a new
top-level template** by picking primitives from the kit. Parallel in shape to
`/hitl-test` (which *renders* existing templates) — same single-stage
interrogator pattern, same `AskUserQuestion`-driven walk.

The engineer never writes Python. They never see Jinja. They pick from a
finite catalog of primitives, answer the variables those primitives need,
and the skill writes a new `templates/<name>.py.j2` for them.

## What this skill does

1. **Preflight** — confirm `sc-compose`, `templates/primitives/`, `.venv` all exist.
2. **Test name** — ask the engineer for a snake_case name for the new shape.
3. **Intent** — ask the engineer to describe the test in one line (free text).
4. **Pick primitives** — multi-select from the catalog (1–4 primitives).
5. **Walk variables** — for each variable the picked primitives require (the union, deduplicated), one `AskUserQuestion`. Re-uses `/hitl-test`'s variable-walking spec — same options, same coercions; do not duplicate the logic.
6. **Author the template** — write `templates/<test_name>.py.j2` with frontmatter, an authoring-trail comment block, and `@<primitives/...>` includes in conventional order (setup → capture → assertions).
7. **Optional render** — offer to render the new template immediately via `/hitl-test`'s flow so the engineer sees their shape produce a passing test.

The skill **never emits Python directly**. It only writes:
- a YAML frontmatter block,
- a comment block,
- a sequence of `@<...>` include lines.

The Python comes from rendering the primitives.

## Entry preflight

```bash
command -v sc-compose && test -d templates/primitives && test -d .venv && echo "ready"
```

If not ready: stop. Tell the engineer to run `make demo` in the repo root once to confirm setup.

## Step 1 — test name

```
What should we call this test? (snake_case; becomes the new template's filename)
```

Coerce to snake_case (lowercase, spaces → underscores, strip punctuation).

## Step 2 — intent

```
Describe what this test does, in one sentence. This goes in the new template's
metadata.purpose and in the authoring-trail comment block for the reviewer.
```

Free text. Keep it under 200 characters.

## Step 3 — pick primitives

List every `.j2` in `templates/primitives/`. For each, read its frontmatter
and present its `metadata.purpose` as the option's description.

Present as a single multi-select `AskUserQuestion`. The engineer picks 1–4.

If the engineer answers "none of these fit" (via the "Other" path or an
explicit refusal), GO TO the no-primitive-fits case below.

## Step 4 — walk variables

For each primitive picked, read its frontmatter and union the
`required_variables`. Deduplicate. Then ask one `AskUserQuestion` per
variable — same UX as `/hitl-test`'s Step 2 (see `.claude/skills/hitl-test/SKILL.md`).

Hints for the kit's known variables (mirror `/hitl-test`):

- `test_name` — already collected in Step 1; do not re-ask
- `display_pattern` — recommend `dot_grid`; offer `checkerboard`, `single_dot`, `horizontal_lines`
- `target_x`, `target_y` — recommend `100`
- `tolerance_px` — recommend `5`
- `intensity_threshold` — recommend `100`

## Step 5 — author the template

Sort the picked primitives into conventional order:

1. `setup_preamble` (always first if picked — emits imports + def line)
2. `pattern_capture` (after setup, before any assertion)
3. `assert_centroid`, `assert_intensity`, ... (assertions in pick order)

Write `templates/<test_name>.py.j2` with this structure:

```
---
required_variables:
  - <union of picked primitives' required vars, sorted alphabetically>
defaults:
  <union of picked primitives' defaults, with the composing template winning on conflict>
metadata:
  purpose: "<engineer's intent from Step 2>"
---
# ────────────────────────────────────────────────────────────────────
# Authored via /hitl-author on YYYY-MM-DD by <engineer email if known>
# Intent: <engineer's intent from Step 2>
# Primitives: <picked primitives joined by " → ">
# Review: PR before merging into templates/
# ────────────────────────────────────────────────────────────────────
@<primitives/setup_preamble.j2>
@<primitives/pattern_capture.j2>
@<primitives/assert_centroid.j2>
```

(Substituting the actually-picked primitives in conventional order.)

Tell the engineer:

> "Wrote `templates/<test_name>.py.j2`. Open a PR before merging — a developer
> should review that this matches what you described."

## Step 6 — optional render

Ask:

> "Render and run this new template now to confirm it works?"

If yes: invoke `/hitl-test`'s render flow against the new template using the
variables the engineer just supplied. Show the rendered file path and the
pytest result.

If no: exit cleanly.

## No-primitive-fits case

If the engineer indicates no available primitive matches their intent:

1. Do NOT write a template.
2. Write `issues/primitive-requests/<test_name>-YYYY-MM-DD.md` with this shape:

```markdown
---
id: primitive-request-<test_name>
status: open
requested_by: <engineer email if known>
requested_on: YYYY-MM-DD
---

## Intent

<engineer's Step 2 intent>

## What's missing

<engineer's description of the API surface they needed and what primitives
they wished existed>

## Available primitives at request time

- setup_preamble — <purpose>
- pattern_capture — <purpose>
- assert_centroid — <purpose>
- assert_intensity — <purpose>
- ...

## Suggested next steps for a developer

1. Decide whether the requested capability becomes a new primitive or fits inside an existing one.
2. Author the primitive (`templates/primitives/<verb>_<noun>.j2`) with its own YAML frontmatter contract.
3. Add a parametrized entry to `tests/test_primitives.py`.
4. Update `.claude/skills/hitl-author/SKILL.md`'s "Hints for the kit's known variables" section if the primitive introduces new variables.
5. Close this request file once the new primitive ships.
```

Tell the engineer:

> "None of the current primitives match this. I've written
> `issues/primitive-requests/<test_name>-YYYY-MM-DD.md` describing what you
> needed. A developer will pick this up and add a primitive — re-run
> `/hitl-author` once that lands."

Then exit cleanly.

## What this skill is NOT for

- **Authoring primitives.** Primitives are a developer concept. Engineers compose from them; engineers don't write them. Primitive-request files exist so developers know what to build.
- **One-shot tests.** Use `/hitl-test` if you just want to render an existing template once.
- **Editing engineer-authored templates.** If your shape changes, re-run `/hitl-author` with a new name. The previous template stays valid.

## Push-back on "just write it for me"

If the engineer asks the agent to "just generate the Python directly", refuse politely. The whole point of the kit is that engineer-authored templates are constructed from primitives that have already been reviewed. Free-form Python defeats the review story. Walk them through the catalog instead.
