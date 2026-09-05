"""Structural validation for the "Decision table: Ground Truth vs.
synthetic data generation vs. active learning vs. weak supervision" table
added to the "Amazon SageMaker Ground Truth: data labeling and when NOT to
use it" subsection of docs/domain-1-fundamentals-of-ai-and-ml.md.

The gap this covers: the existing Ground Truth subsection already compared
Ground Truth against manual labeling, SageMaker Data Wrangler, and
synthetic data generation, but active learning was only mentioned as an
internal Ground Truth mechanism and weak supervision was never mentioned at
all -- even though both are exam-relevant labeling/data-generation
strategies in their own right. These tests guard the new decision table
that closes that gap: it must live inside the existing Ground Truth
subsection (no new numbered section, mini-quiz, or worked-example heading),
name all four strategies as an actual markdown table, describe active
learning and weak supervision as standalone strategies (not just as part of
how Ground Truth works internally), and include an exam tip tying each
strategy to the scenario constraint that makes it the correct answer.

Run with:
    python3 -m unittest tests/test_domain_1_ground_truth_alternatives_decision_table.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-1-fundamentals-of-ai-and-ml.md"
)

HEADING = (
    "### Amazon SageMaker Ground Truth: data labeling and when NOT to use it"
)
TABLE_INTRO = (
    "**Decision table: Ground Truth vs. synthetic data generation vs. "
    "active learning vs. weak supervision**"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain1GroundTruthAlternativesDecisionTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.subsection = _section(
            cls.text,
            re.escape(HEADING),
            r"\n#{1,3} |\n---\n",
        )

    def test_decision_table_intro_present_inside_ground_truth_subsection(self):
        self.assertIn(TABLE_INTRO, self.subsection)

    def test_decision_table_is_an_actual_markdown_table(self):
        table_text = self.subsection[self.subsection.index(TABLE_INTRO):]
        self.assertRegex(table_text, r"\|---\|---\|---\|---\|")

    def test_decision_table_covers_all_four_strategies(self):
        table_text = self.subsection[self.subsection.index(TABLE_INTRO):]
        for term in [
            "SageMaker Ground Truth",
            "Active learning",
            "Weak supervision",
            "Synthetic data generation",
        ]:
            with self.subTest(term=term):
                self.assertIn(
                    term,
                    table_text,
                    f"decision table should include a row for {term!r}",
                )

    def test_active_learning_described_as_a_standalone_strategy(self):
        # Distinguish it from the pre-existing mention of active learning
        # as merely an internal Ground Truth mechanism: it should also be
        # described as its own train/query/label/retrain loop.
        self.assertRegex(
            self.subsection,
            r"(?i)standalone.{0,40}active learning",
            "decision table should frame active learning as a standalone "
            "strategy distinct from Ground Truth's internal use of it",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)retrain",
            "decision table should describe the iterative retrain loop "
            "underpinning standalone active learning",
        )

    def test_weak_supervision_described_with_its_mechanism(self):
        self.assertRegex(
            self.subsection,
            r"(?i)weak supervision",
            "decision table should introduce weak supervision by name",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)heuristics|rules|labeling functions",
            "decision table should describe weak supervision's rule/"
            "heuristic-based labeling mechanism",
        )

    def test_has_decision_table_exam_tip_naming_all_four_strategies(self):
        tip_match = re.search(
            r"> \*\*Exam tip:\*\* When Ground Truth, active learning, "
            r"weak\nsupervision, and\nsynthetic data.*",
            self.subsection,
        )
        self.assertIsNotNone(
            tip_match,
            "expected a follow-up exam tip covering all four decision-"
            "table strategies together",
        )

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-7]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            7,
            "Domain 1 must still have exactly 7 numbered sections",
        )
        section_5 = _section(
            self.text,
            r"\n## 5\. AWS managed AI/ML services \(conceptual overview\)",
            r"\n## 6\. Model evaluation basics",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_5)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 5 must still contain exactly one mini-quiz heading",
        )

    def test_does_not_introduce_a_new_worked_example_heading(self):
        heading_worked_examples = re.findall(
            r"(?m)^#{2,4} Worked examples?:", self.text
        )
        self.assertEqual(
            len(heading_worked_examples),
            3,
            "Domain 1 must still have exactly 3 heading-level 'Worked "
            "example' sections",
        )

    def test_does_not_break_mini_quiz_question_numbering(self):
        section_5 = _section(
            self.text,
            r"\n## 5\. AWS managed AI/ML services \(conceptual overview\)",
            r"\n## 6\. Model evaluation basics",
        )
        quiz_text_match = re.search(
            r"#### Mini-quiz: Test your understanding of.*?(?=\n---\n|\Z)",
            section_5,
            re.S,
        )
        self.assertIsNotNone(quiz_text_match)
        quiz_text = quiz_text_match.group(0)
        question_numbers = re.findall(r"^(\d+)\.\s", quiz_text, re.M)
        self.assertEqual(
            [int(n) for n in question_numbers],
            list(range(1, len(question_numbers) + 1)),
            "mini-quiz question numbering in Section 5 must stay "
            "sequential and uncorrupted by the new decision table",
        )


if __name__ == "__main__":
    unittest.main()
