"""Structural validation for the Domain 1 subsection mini-quizzes.

Domain 1 previously offered only one summative practice-question set at the
very end of the document (15-20 questions). This meant learners had no way
to self-check their understanding incrementally while working through each
major numbered section. This test asserts that every one of the seven major
numbered sections ("## 1." through "## 7.") now contains a short formative
"Mini-quiz" checkpoint -- 2 to 4 multiple-choice questions, each with at
least four options and an inline answer explanation -- placed *within* that
section (i.e. before the section ends), so a future edit that drops a
mini-quiz, strips its explanations, or moves it out of its section is
caught automatically.

Run with:
    python3 -m unittest tests/test_domain_1_subsection_mini_quizzes.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-1-fundamentals-of-ai-and-ml.md"
)

MIN_QUIZ_QUESTIONS = 2
MAX_QUIZ_QUESTIONS = 4


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _numbered_sections(text):
    """Return (heading, body) pairs for each "## 1." through "## 7."
    top-level section, mirroring tests/test_domain_1_study_guide.py."""
    sections = re.findall(r"\n## ([1-7]\. .*?)\n(.*?)(?=\n## |\Z)", text, re.S)
    return sections


class TestDomain1SubsectionMiniQuizzes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.sections = _numbered_sections(cls.text)

    def test_found_all_seven_numbered_sections(self):
        self.assertEqual(
            len(self.sections),
            7,
            "expected exactly 7 numbered topic sections in Domain 1",
        )

    def test_every_numbered_section_has_a_mini_quiz_heading(self):
        for heading, body in self.sections:
            with self.subTest(section=heading):
                self.assertRegex(
                    body,
                    r"#### Mini-quiz: Test your understanding of",
                    f"section {heading!r} is missing a subsection mini-quiz",
                )

    def test_mini_quiz_sits_before_the_next_top_level_divider(self):
        # The mini-quiz heading must appear before the "---" divider that
        # closes out the section, i.e. it belongs to *this* section, not
        # dangling after it / before the next "## " heading.
        for heading, body in self.sections:
            with self.subTest(section=heading):
                quiz_match = re.search(
                    r"#### Mini-quiz: Test your understanding of", body
                )
                self.assertIsNotNone(quiz_match)
                divider_match = re.search(r"\n---\n", body)
                self.assertIsNotNone(
                    divider_match,
                    f"section {heading!r} should end with a '---' divider",
                )
                self.assertLess(
                    quiz_match.start(),
                    divider_match.start(),
                    f"mini-quiz in section {heading!r} should appear before "
                    "the section's closing divider",
                )

    def test_mini_quiz_has_two_to_four_questions_with_four_options_each(self):
        for heading, body in self.sections:
            quiz_match = re.search(
                r"#### Mini-quiz: Test your understanding of.*?(?=\n---\n|\Z)",
                body,
                re.S,
            )
            self.assertIsNotNone(quiz_match, f"no mini-quiz found in {heading!r}")
            quiz_text = quiz_match.group(0)
            question_numbers = re.findall(r"^(\d+)\.\s", quiz_text, re.M)
            with self.subTest(section=heading):
                self.assertEqual(
                    [int(n) for n in question_numbers],
                    list(range(1, len(question_numbers) + 1)),
                    f"mini-quiz questions in {heading!r} must be "
                    "sequentially numbered starting at 1",
                )
                self.assertGreaterEqual(
                    len(question_numbers),
                    MIN_QUIZ_QUESTIONS,
                    f"mini-quiz in {heading!r} should have at least "
                    f"{MIN_QUIZ_QUESTIONS} questions",
                )
                self.assertLessEqual(
                    len(question_numbers),
                    MAX_QUIZ_QUESTIONS,
                    f"mini-quiz in {heading!r} should have at most "
                    f"{MAX_QUIZ_QUESTIONS} questions",
                )

            blocks = re.split(r"\n(?=\d+\.\s)", quiz_text.strip())
            blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
            for block in blocks:
                qnum = block.split(".", 1)[0]
                with self.subTest(section=heading, question=qnum):
                    options = re.findall(r"^\s*[A-E]\.\s", block, re.M)
                    self.assertGreaterEqual(
                        len(options),
                        4,
                        f"mini-quiz question {qnum} in {heading!r} should "
                        "have at least 4 answer options",
                    )
                    self.assertRegex(
                        block,
                        r"\*\*Answer:\s*[A-E]\*\*\s*[—-]\s*\S",
                        f"mini-quiz question {qnum} in {heading!r} should "
                        "state the correct option with a brief explanation "
                        "(e.g. '**Answer: B** — ...')",
                    )

    def test_mini_quiz_topics_match_their_parent_section(self):
        # Sanity-check the mini-quiz titles line up 1:1 with the sections
        # they follow, e.g. "Test your understanding of the ML lifecycle"
        # directly after "## 2. The ML development lifecycle".
        expected_topic_fragment = {
            "1": "AI/ML/DL terminology",
            "2": "the ML lifecycle",
            "3": "types of learning",
            "4": "common AI/ML use cases",
            "5": "AWS managed AI/ML services",
            "6": "model evaluation",
            "7": "overfitting, underfitting, and bias",
        }
        for heading, body in self.sections:
            section_num = heading.split(".", 1)[0]
            with self.subTest(section=heading):
                quiz_heading_match = re.search(
                    r"#### Mini-quiz: (Test your understanding of .*)", body
                )
                self.assertIsNotNone(quiz_heading_match)
                self.assertIn(
                    expected_topic_fragment[section_num].lower(),
                    quiz_heading_match.group(1).lower(),
                )


if __name__ == "__main__":
    unittest.main()
