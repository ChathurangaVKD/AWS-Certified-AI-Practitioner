"""Structural validation for the "Choosing the right evaluation metric for
your use case" quick-reference table, the numeric "Worked interpretation
check", and the 4th mini-quiz question added to Domain 1's "6. Model
evaluation basics" section.

The gap this covers: Section 6 already had a decision *tree* (mermaid
flowchart) sorting metric choice by problem shape (regression vs.
classification, balanced vs. imbalanced), but no worked-through numeric
example of computing precision/recall from an actual confusion matrix, and
no lookup keyed by concrete, named exam-style scenarios (fraud detection,
spam filtering, medical screening, etc.). This test guards the new content
added to close that gap: it must live inside Section 6, before the
section's closing "---" divider (so it doesn't leak into Section 7), must
not add a new "##"/"###"/"####" heading (so it doesn't perturb the
worked-example or mini-quiz heading counts asserted elsewhere in this
repo's test suite), and the section's mini-quiz must still satisfy the
2-4-question, four-option, inline-answer contract asserted generically in
tests/test_domain_1_subsection_mini_quizzes.py.

Run with:
    python3 -m unittest tests/test_domain_1_model_evaluation_use_case_table.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-1-fundamentals-of-ai-and-ml.md"
)

SECTION_HEADING = "## 6. Model evaluation basics"
NEXT_SECTION_HEADING = "## 7. Overfitting"
TABLE_LEAD_IN = (
    "**Choosing the right evaluation metric for your use case:**"
)
WORKED_CHECK_LEAD_IN = "**Worked interpretation check:**"
MINI_QUIZ_HEADING = "#### Mini-quiz: Test your understanding of model evaluation"


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading, end_heading):
    start = text.index(start_heading)
    end = text.index(end_heading, start)
    return text[start:end]


class TestDomain1ModelEvaluationUseCaseTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, SECTION_HEADING, NEXT_SECTION_HEADING)

    def test_use_case_table_exists_within_section_6(self):
        self.assertIn(TABLE_LEAD_IN, self.section)

    def test_use_case_table_precedes_the_mini_quiz(self):
        table_pos = self.section.index(TABLE_LEAD_IN)
        quiz_pos = self.section.index(MINI_QUIZ_HEADING)
        self.assertLess(table_pos, quiz_pos)

    def test_use_case_table_covers_named_scenarios_and_recommended_metrics(self):
        for expected in [
            "Fraud detection",
            "Spam email filtering",
            "Medical disease screening",
            "Loan-default prediction",
            "**Recall**",
            "**Precision**",
            "**F1**",
            "**Accuracy**",
            "**RMSE / MAE**",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_use_case_table_cross_links_the_loan_default_worked_example(self):
        self.assertIn(
            "#worked-example-end-to-end-ml-lifecycle-for-a-loan-default-predictor",
            self.section,
        )

    def test_worked_interpretation_check_exists_and_precedes_the_mini_quiz(self):
        self.assertIn(WORKED_CHECK_LEAD_IN, self.section)
        check_pos = self.section.index(WORKED_CHECK_LEAD_IN)
        quiz_pos = self.section.index(MINI_QUIZ_HEADING)
        self.assertLess(check_pos, quiz_pos)

    def test_worked_interpretation_check_shows_the_confusion_matrix_arithmetic(self):
        for expected in ["TP = 32", "FP = 18", "FN = 8", "64%", "80%", "0.71"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_new_content_does_not_add_a_new_heading(self):
        # The new material is body prose/tables, not a new "##"/"###"/"####"
        # heading, so it must not perturb worked-example or mini-quiz
        # heading counts asserted elsewhere in this repo's test suite.
        headings = re.findall(r"(?m)^#{2,4} .*$", self.section)
        self.assertEqual(
            headings,
            [SECTION_HEADING, MINI_QUIZ_HEADING],
            "Section 6 should still contain exactly its own heading and "
            "one mini-quiz heading -- no new headings were expected",
        )

    def test_mini_quiz_now_has_a_fourth_question_on_the_worked_check(self):
        quiz_text = self.section[self.section.index(MINI_QUIZ_HEADING) :]
        question_numbers = re.findall(r"(?m)^(\d+)\.\s", quiz_text)
        self.assertEqual([int(n) for n in question_numbers], [1, 2, 3, 4])
        self.assertIn("recall", quiz_text.lower())
        self.assertIn("**Answer: C**", quiz_text)


if __name__ == "__main__":
    unittest.main()
