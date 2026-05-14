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
TEMPLATES_DIR = REPO_ROOT / "templates"


def _required_variables(template_path: Path) -> list[str]:
    body = template_path.read_text()
    assert body.startswith("---\n"), f"{template_path} must have YAML frontmatter"
    end = body.index("\n---\n", 4)
    frontmatter = yaml.safe_load(body[4:end])
    return frontmatter.get("required_variables", [])


def _all_templates() -> list[Path]:
    # Excludes underscore-prefixed include fragments.
    return sorted(p for p in TEMPLATES_DIR.glob("*.py.j2") if not p.name.startswith("_"))


def test_skill_doc_exists():
    assert SKILL_FILE.exists(), f"missing skill doc: {SKILL_FILE}"


def test_skill_doc_mentions_every_required_variable_across_all_templates():
    doc = SKILL_FILE.read_text()
    for template in _all_templates():
        for var in _required_variables(template):
            assert var in doc, (
                f"required variable {var!r} from {template.name} not mentioned "
                f"in SKILL.md — the skill will not collect it from the engineer"
            )


def test_skill_doc_does_not_hardcode_one_template_path():
    # v0 referenced `templates/vision-centroid.py.j2` literally. After slice
    # 0004, the skill discovers templates dynamically and should reference
    # them by stem only.
    doc = SKILL_FILE.read_text()
    assert "templates/<template-stem>.py.j2" in doc or "templates/*.py.j2" in doc, (
        "SKILL.md should describe template discovery, not hardcode a single template path"
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
