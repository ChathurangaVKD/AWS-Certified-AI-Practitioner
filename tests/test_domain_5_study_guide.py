"""Structural validation for the shared-responsibility diagram added to
docs/domain-5-security-compliance-governance.md.

Domain 5 has no broader structural test suite yet (unlike Domains 1-4);
this file only covers the new diagram added for the Section 5 shared
responsibility model, mirroring the `_section` helper convention used in
tests/test_domain_1_study_guide.py.

Run with:
    python3 -m unittest tests/test_domain_5_study_guide.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain5StudyGuideExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(DOC_PATH.is_file(), f"expected study guide at {DOC_PATH}")


class TestDomain5PracticeQuestionDifficultyTags(unittest.TestCase):
    """Domain 5 has no broader practice-question test suite yet (see module
    docstring), but its practice questions must still carry difficulty tags
    like Domains 1-4, so this class covers that one requirement directly."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.questions_section = _section(
            cls.text, r"\n## Practice questions", r"\n## Answer key"
        )

    def test_every_question_is_tagged_with_a_difficulty_level(self):
        blocks = re.split(r"\n(?=\d+\.\s)", self.questions_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
        levels_seen = set()
        for block in blocks:
            qnum = block.split(".", 1)[0]
            with self.subTest(question=qnum):
                match = re.match(
                    r"^\d+\.\s\*\*\[(Beginner|Intermediate|Advanced)\]\*\*\s",
                    block,
                )
                self.assertTrue(
                    match,
                    f"question {qnum} should start with a "
                    f"**[Beginner|Intermediate|Advanced]** difficulty tag",
                )
                if match:
                    levels_seen.add(match.group(1))
        self.assertEqual(
            levels_seen,
            {"Beginner", "Intermediate", "Advanced"},
            "practice questions should include all three difficulty levels",
        )


class TestDomain5SharedResponsibilityDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_shared_responsibility_section_has_a_boundary_diagram(self):
        section = _section(
            self.text,
            r"\n## 5\. AWS shared responsibility model applied to AI/ML services",
        )
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "shared responsibility section should include a boundary diagram",
        )
        diagram = "\n".join(fences)
        for term in [
            "Bedrock",
            "SageMaker",
            "CUSTOMER",
            "in the cloud",
            "of the cloud",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)


if __name__ == "__main__":
    unittest.main()
