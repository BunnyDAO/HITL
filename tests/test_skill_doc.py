"""Lint test for .claude/skills/hitl-test/SKILL.md.

The skill is LLM-mediated and not unit-testable in a useful way. But it
*can* drift from the template it's supposed to interrogate the engineer
about — e.g. someone adds a required variable to the template and forgets
to add a question for it in SKILL.md. This test catches that.
"""
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
SKILL_FILE = REPO_ROOT / ".claude" / "skills" / "hitl-test" / "SKILL.md"
TEMPLATE_FILE = REPO_ROOT / "templates" / "vision-centroid.py.j2"


def _template_required_variables() -> list[str]:
    body = TEMPLATE_FILE.read_text()
    assert body.startswith("---\n"), "template must have YAML frontmatter"
    end = body.index("\n---\n", 4)
    frontmatter = yaml.safe_load(body[4:end])
    return frontmatter["required_variables"]


def test_skill_doc_exists():
    assert SKILL_FILE.exists(), f"missing skill doc: {SKILL_FILE}"


def test_skill_doc_mentions_every_required_template_variable():
    doc = SKILL_FILE.read_text()
    for var in _template_required_variables():
        assert var in doc, (
            f"required template variable {var!r} not mentioned in SKILL.md — "
            "the skill will not collect it from the engineer"
        )


def test_skill_doc_references_the_correct_template_path():
    doc = SKILL_FILE.read_text()
    assert "templates/vision-centroid.py.j2" in doc, (
        "SKILL.md must reference the exact template path so its render "
        "subprocess works from the repo root"
    )


def test_skill_doc_uses_ask_user_question():
    doc = SKILL_FILE.read_text()
    assert "AskUserQuestion" in doc, (
        "SKILL.md must instruct the agent to use AskUserQuestion — "
        "free-text fallback is the wrong UX for this skill"
    )


def test_skill_doc_writes_to_tests_generated():
    doc = SKILL_FILE.read_text()
    assert "tests/generated/" in doc, (
        "SKILL.md must instruct the agent to write rendered output into "
        "tests/generated/ — anywhere else and pytest discovery breaks"
    )


def test_skill_doc_short_enough_to_read_quickly():
    doc = SKILL_FILE.read_text()
    word_count = len(doc.split())
    # ~1000 words is roughly a 4–5 minute read. Aim for under that.
    assert word_count < 1200, (
        f"SKILL.md is {word_count} words — over the 5-minute-read budget. "
        "Trim before committing."
    )
