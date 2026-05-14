# Test Engineer's Guide

You don't write Python. You don't read Jinja. You know what your tests should verify, and you want a way to express that without learning a programming language. This guide is for you.

## What this project does

This repository ships two tools you talk to inside Claude Code:

- **`/hitl-test`** — you pick an existing test "shape" and answer a few questions; a real test file gets created and run.
- **`/hitl-author`** — you design a brand-new test "shape" by combining the available building blocks; a developer reviews what you produced, and once it's merged everyone can use it via `/hitl-test`.

Behind the scenes there's mocked hardware (a fake camera, a fake display) so everything runs on a laptop without any physical rig. The patterns, the variables you pick, the pass/fail outcomes — those are real.

## What a "primitive" is

A primitive is a **building block** for a test. Each one does one specific thing:

| Primitive | What it does |
|---|---|
| `setup_preamble` | Sets up the test — like saying "open a notebook and label the page." |
| `pattern_capture` | Shows a pattern on the display and snaps a picture with the camera. |
| `assert_centroid` | Checks that the bright spot in the picture is near where you expected it. |
| `assert_intensity` | Checks that the picture isn't blank — at least one pixel is bright enough. |

You assemble these in order to describe what your test does. Think of it like a sequence of steps:

> Setup → take a picture → check 1 → check 2 → ...

That sequence becomes a real test. You never see Python; the system handles the assembly.

## How to run an existing test — `/hitl-test`

In a Claude Code session, type `/hitl-test`. The skill:

1. Lists every test shape (template) that already exists. You pick one.
2. Asks you a few questions — what pattern to show, what tolerance to use, etc. Each question has a recommended answer; you can pick it or type your own.
3. Writes a real test file and (if you want) runs it. You see whether it passed.

If it failed, the message tells you *why*. For example:

> `AssertionError: centroid (97.00, 101.00) is 3.16px from target (100, 100); tolerance was 1px`

That means: the bright spot you were looking for landed at position (97, 101), 3.16 pixels away from where you said it should be (100, 100), and you only allowed 1 pixel of slack. So the test failed. Re-run with a tolerance of 5 and it'll pass.

## How to design a new test — `/hitl-author`

Use `/hitl-author` when no existing test shape fits what you want to verify. The skill:

1. Asks you for a name and a one-sentence description of the test.
2. Shows you the available building blocks (the primitives table above). You pick which ones you need — usually `setup_preamble` plus a `pattern_capture` plus one or more assertion blocks. Order matters: setup first, then capture, then checks.
3. Asks for the values each building block needs (target position, tolerance, etc.).
4. Writes a real reusable test file.
5. Offers to run it immediately so you see it work.

**Important — your new test needs developer review before it's permanent.** The skill writes the file with a comment block at the top recording what you said you wanted, which blocks you picked, and the date. A developer reads that, confirms the file matches your intent, and merges it. After that, anyone can run your new test shape via `/hitl-test`.

## What if the kit doesn't have what I need?

If your test needs a building block that doesn't exist yet — say, "check the LED color is red" or "measure how long a beep lasts" — tell `/hitl-author` "none of these fit." The skill writes a **primitive request** file describing what you needed. A developer picks it up, adds the missing building block to the kit, and tells you when it's ready. Re-run `/hitl-author` once it lands; your shape is now expressible.

This is on purpose. The kit stays small and reliable; new building blocks get the same review as any code change. Vague "the agent will figure it out" is exactly what this project is built to avoid.

## Reading the test result

When the test runs, pytest prints one of two things:

- **PASSED** — the test verified what it claimed to verify. You're done.
- **FAILED** — followed by an `AssertionError` that tells you *which check failed and what the actual measurement was*. The number you typed (tolerance, threshold, target position) appears in the error message so you can change it and re-run.

A failing test isn't a problem; it's information. The tolerance you picked was too tight, or the pattern is misaligned. Adjust and try again.

## A worked example

You want to verify that when you show a dot grid, the camera sees the centroid within 5 pixels of (100, 100). You type `/hitl-test`, pick `vision-centroid`, accept the recommended answers, and:

```
test_grid_centroid_alignment PASSED
```

You then re-run with a tolerance of 1, and:

```
test_grid_centroid_alignment FAILED
  AssertionError: centroid (97.00, 101.00) is 3.16px from target (100, 100);
  tolerance was 1px
```

The bright spot is real, the math is real, the failure tells you exactly why. The only thing that's fake is the hardware: in production this would be a real camera looking at a real display.

## When to ask a developer

- The kit doesn't cover your test shape → `/hitl-author` will write a primitive request. Tell the dev team to look in `issues/primitive-requests/`.
- A primitive seems to be doing the wrong thing → file an issue describing what you saw vs. what you expected.
- A new test shape you authored doesn't make sense to the reviewer → re-walk `/hitl-author` and adjust your intent description.

Always link to the test file or the primitive name when you ask for help — that's enough context for a developer to pick up.

## Where to read more

- [`README.md`](../README.md) — project front door, install instructions.
- [`docs/sop.md`](sop.md) — what your colleagues on the developer side are reading. You don't need it, but it's there if you're curious how the underlying machinery works.
