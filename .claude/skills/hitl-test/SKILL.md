# /hitl-test — interrogate the engineer, render a HITL test

A Claude Code skill that walks an engineer through generating a HITL test
from one of the templates in `templates/`. The engineer never writes Python.

## What this skill does

1. Discovers available templates in `templates/*.py.j2` and asks which one to use.
2. Reads the chosen template's YAML frontmatter, then asks one structured
   `AskUserQuestion` per `required_variables` entry (with sensible options
   plus the implicit "Other" free-text path).
3. Renders the answers through `sc-compose render` as a subprocess.
4. If render fails, surfaces sc-compose's stderr verbatim — the engineer sees
   the contract violation directly, not a paraphrase.
5. Writes the result to `tests/generated/test_<test_name>.py`.
6. Offers to run pytest on the generated file and reports the outcome.

It does not validate variables itself. The single source of truth on what
counts as a valid set of inputs is sc-compose's frontmatter contract.

## Entry preflight

Before doing anything else, run:

```bash
command -v sc-compose && test -d templates && test -d .venv && echo "ready"
```

If that prints `ready`, proceed. Otherwise stop and tell the engineer:

> "I can't run /hitl-test from here — sc-compose, the templates dir, or
> the Python venv is missing. Open the repo root (where `Makefile` lives)
> and run `make demo` once to confirm the toolchain is wired up."

## Step 1 — discover templates and pick one

List all `templates/*.py.j2` files. For each one, read the YAML frontmatter
(everything between the first `---` and the next `---`) and extract:

- the filename stem (e.g. `vision-centroid`)
- `metadata.purpose` — the one-line description

Present them via `AskUserQuestion`. Each option's `label` is the stem; the
`description` is the `metadata.purpose` value.

`vision-centroid` is the Recommended option when present (it's the demo's
wow-moment template); otherwise fall back to the first template in
alphabetical order.

## Step 2 — walk the variables

Open the chosen template's frontmatter. For each name in `required_variables`,
ask one structured `AskUserQuestion`.

**Scalar variables** (everything not obviously a list): one question, options
should include sensible defaults for the variable's apparent type, plus the
implicit "Other" path. Coerce numeric answers to int when feeding sc-compose.

**Parallel-list variables** (you see two or more list-typed required vars
that obviously go together, like `assertion_kinds` + `assertion_kwargs`):
treat them as a single "configure N items" loop. Per iteration:

1. Ask one question per list (e.g. "what kind of assertion?" then "what kwargs
   for that assertion?"). The kwargs answer is a free-text Python kwargs
   fragment like `target=(100, 100), tolerance_px=5`.
2. After the iteration, ask `AskUserQuestion`: "add another?" with options
   `Yes — add another` and `No — done`.

When done, build each list in order. Both lists must end up the same length.

**Singleton list variables**: same shape but only one entry is collected.

### Variable defaults for known templates

These hints help you offer the right Recommended option, but the engineer can
always pick "Other" and type anything:

- `test_name` — snake_case the answer
- `display_pattern` — `dot_grid` (default), `checkerboard`, `single_dot`, `horizontal_lines`
- `target_x`, `target_y` — `100` (image center; image is 200×200)
- `tolerance_px` — `5` (passes with default `dot_grid` jitter); `1` to demonstrate failure
- `assertion_kinds` — `centroid_within`, `pixel_intensity_above`
- `assertion_kwargs` — e.g. `target=(100, 100), tolerance_px=5`, `threshold=100`
- `intensity_threshold` — `100` (typical sanity check that the display rendered something visible)

## Step 3 — render

Write the answers to a temp JSON file. Run:

```bash
sc-compose render --mode file \
  --file templates/<template-stem>.py.j2 \
  --var-file <tmp.json> \
  --output tests/generated/test_<test_name>.py
```

If exit code is non-zero, show the engineer:

> "sc-compose render failed. Its complaint was:
> ```
> <stderr verbatim>
> ```"

Then stop. Do not retry, do not paraphrase, do not guess at fixes — the
engineer needs to see the contract violation in sc-compose's own words.

If exit code is zero, tell the engineer:

> "Rendered tests/generated/test_<test_name>.py."

Then show them the rendered file so they can see what was produced.

## Step 4 — offer to run pytest

Ask one final `AskUserQuestion`:

> "Run pytest on this file now?"

Options:
- `Yes — run it` (Recommended)
- `No — I'll run it later`

If yes, run:

```bash
.venv/bin/pytest tests/generated/test_<test_name>.py -v
```

Show the engineer the output verbatim — including the failure diagnostic
from `assertions.centroid_within` (or whatever assertion failed) if the test
didn't pass. The point of this skill is that the engineer sees the real
outcome, not a curated summary.

If no, exit with:

> "Done. File is at `tests/generated/test_<test_name>.py`. Run it with
> `pytest tests/generated/test_<test_name>.py` when ready."

## What this skill is NOT for

- **Authoring new templates** — that's a different workflow. This skill only consumes templates.
- **Real hardware** — the fixture library is mocked. There is no production-hardware story in this repo.

## When the engineer asks you to "just write the test for me"

Push back gently. The reason this skill exists is to enforce the contract
that sc-compose templates declare. A test engineer who can describe what they
want in five answers is closer to a test that runs in CI than a test engineer
who hand-writes Python the agent will then have to interpret. Walk them
through the questions.

If they're stuck on a value, suggest the Recommended default and tell them
they can re-run the skill with a different choice — `/hitl-test` is fast
to repeat.
