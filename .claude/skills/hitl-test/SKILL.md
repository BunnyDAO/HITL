# /hitl-test — interrogate the engineer, render a HITL test

A Claude Code skill that walks an engineer through generating a vision-centroid
HITL test, without them ever writing Python. This is the v0 — hardcoded to
the single `vision-centroid` template. Multi-template support is a follow-up.

## What this skill does

1. Asks the engineer five structured questions, one variable at a time, using
   `AskUserQuestion` (each with sensible options plus an "Other" free-text
   path).
2. Renders the answers through `sc-compose render` as a subprocess.
3. If render fails, surfaces sc-compose's stderr verbatim — the engineer sees
   the contract violation directly, not a paraphrase.
4. Writes the result to `tests/generated/test_<test_name>.py`.
5. Offers to run pytest on the generated file and reports the outcome.

It does not validate variables itself. The single source of truth on what
counts as a valid set of inputs is sc-compose's frontmatter contract.

## Entry

Before doing anything else, confirm the prerequisites are in place. Run:

```bash
command -v sc-compose && test -f templates/vision-centroid.py.j2 && \
  test -d .venv && echo "ready"
```

If that prints `ready`, proceed. If not, stop and tell the engineer:

> "I can't run /hitl-test from here — sc-compose, the template, or the
> Python venv is missing. Open the repo root (where `Makefile` lives) and
> run `make demo` once to confirm the toolchain is wired up, then try
> again."

## Step 1 — collect the five required variables

Ask these five `AskUserQuestion` calls IN ORDER. Do not batch them — one
question, wait for answer, next question. The engineer's answers feed
directly into the sc-compose var file.

### Q1 — test_name

> "What should we call this test? It becomes the function name, so use snake_case."

Options:
- `grid_centroid_alignment` (Recommended) — descriptive default
- `centroid_within_tolerance`
- `quick_smoke`

The "Other" path lets them type anything; coerce to snake_case if it isn't
already (lowercase, spaces→underscores, strip non-alphanumeric-underscore).

### Q2 — display_pattern

> "Which pattern should the display show before capture?"

Options:
- `dot_grid` (Recommended) — the demo's default; lands ~3px off (100, 100)
- `checkerboard` — lands ~1.4px off
- `single_dot` — lands ~4.2px off (use to demonstrate a tight tolerance failing)
- `horizontal_lines` — lands ~2.2px off

### Q3 — target_x

> "What x-coordinate should the centroid land at? (Image is 200×200, centered at 100.)"

Options:
- `100` (Recommended) — image center
- `50`
- `150`

### Q4 — target_y

> "What y-coordinate should the centroid land at?"

Options:
- `100` (Recommended) — image center
- `50`
- `150`

### Q5 — tolerance_px

> "How many pixels can the centroid be off before the test fails?"

Options:
- `5` (Recommended) — passes with the default `dot_grid` jitter (~3px)
- `2` — tight; will fail for `dot_grid` and `single_dot`
- `1` — very tight; fails for every pattern
- `10` — loose; passes everything

## Step 2 — render

Write the five answers to a temp JSON file (use `tempfile.NamedTemporaryFile`
or equivalent). Coerce numeric answers (`target_x`, `target_y`, `tolerance_px`)
to integers; leave string answers as strings.

Run:

```bash
sc-compose render --mode file \
  --file templates/vision-centroid.py.j2 \
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

And read the rendered file so they can see what was produced (or `cat` it
into the conversation).

## Step 3 — offer to run pytest

Ask one final `AskUserQuestion`:

> "Run pytest on this file now?"

Options:
- `Yes — run it` (Recommended)
- `No — I'll run it myself later`

If yes, run:

```bash
.venv/bin/pytest tests/generated/test_<test_name>.py -v
```

Show the engineer the output verbatim — including the failure diagnostic
from `assertions.centroid_within` if the centroid was outside tolerance.
The point of this skill is that the engineer sees the real outcome, not
a curated summary.

If no, exit with:

> "Done. File is at `tests/generated/test_<test_name>.py`. Run it with
> `pytest tests/generated/test_<test_name>.py` when ready."

## What this skill is NOT for

- **Multi-template selection** — slice 0004 adds that. For now, vision-centroid only.
- **Authoring new templates** — that's a different workflow. This skill only consumes templates.
- **Real hardware** — the fixture library is mocked. There is no production-hardware story in this repo.

## When the engineer asks you to "just write the test for me"

Push back gently. The reason this skill exists is to enforce the contract
that sc-compose templates declare. A test engineer who can describe what they
want in five answers is closer to a test that runs in CI than a test engineer
who hand-writes Python the agent will then have to interpret. Walk them
through the five questions.

If they're stuck on a value, suggest the Recommended default and tell them
they can re-run the skill with a different choice — `/hitl-test` is fast
to repeat.
