"""Lint test for .claude/skills/hitl-author/SKILL.md.

Mirrors tests/test_skill_doc.py but for the author skill. The skill is
LLM-mediated and not unit-testable in a useful way, but it *can* drift
from the primitives kit — someone adds a primitive and forgets to update
SKILL.md's hints. This catches that.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILL_FILE = REPO_ROOT / ".claude" / "skills" / "hitl-author" / "SKILL.md"
PRIMITIVES_DIR = REPO_ROOT / "templates" / "primitives"


def _primitive_stems() -> list[str]:
    return sorted(p.stem for p in PRIMITIVES_DIR.glob("*.j2"))


def test_skill_doc_exists():
    assert SKILL_FILE.exists(), f"missing skill doc: {SKILL_FILE}"


def test_skill_doc_mentions_every_primitive_in_the_kit():
    doc = SKILL_FILE.read_text()
    for stem in _primitive_stems():
        assert stem in doc, (
            f"primitive {stem!r} not mentioned in SKILL.md — engineers won't see "
            "it in the picker's catalog"
        )


def test_skill_doc_references_primitive_requests_path():
    doc = SKILL_FILE.read_text()
    assert "issues/primitive-requests/" in doc, (
        "SKILL.md must instruct writing to issues/primitive-requests/ for the "
        "no-fit case — that's the developer's input queue"
    )


def test_skill_doc_uses_ask_user_question():
    doc = SKILL_FILE.read_text()
    assert "AskUserQuestion" in doc, (
        "SKILL.md must instruct AskUserQuestion as the interrogation surface"
    )


def test_skill_doc_describes_conventional_primitive_order():
    doc = SKILL_FILE.read_text()
    assert "setup_preamble" in doc and "pattern_capture" in doc, (
        "SKILL.md must describe the conventional primitive ordering "
        "(setup → capture → assertions)"
    )


def test_skill_doc_describes_authoring_trail_comment_block():
    doc = SKILL_FILE.read_text()
    assert "Authored via /hitl-author" in doc, (
        "SKILL.md must describe the authoring-trail comment block that gets "
        "embedded in engineer-authored templates"
    )


def test_skill_doc_short_enough_to_read_quickly():
    doc = SKILL_FILE.read_text()
    word_count = len(doc.split())
    assert word_count < 1200, (
        f"SKILL.md is {word_count} words — over the 5-minute-read budget. Trim before committing."
    )


def test_skill_doc_cross_references_hitl_test_skill():
    doc = SKILL_FILE.read_text()
    assert "hitl-test/SKILL.md" in doc, (
        "SKILL.md should reference /hitl-test's SKILL.md for the variable-walking spec "
        "rather than duplicate it — single source of truth"
    )
