"""Structural validation for the "Ensemble methods: bagging, boosting, and
voting" subsection added to docs/domain-1-fundamentals-of-ai-and-ml.md.

The gap this covers: Domain 1 Section 7 covers the bias-variance trade-off
and the two most commonly tested overfitting remedies (more data,
regularization), but never covered ensemble methods -- a natural third
remedy that reduces variance (bagging) or bias (boosting) by combining
multiple models. Before this subsection, "ensemble" appeared exactly once
in the whole documentation set, as a passing distractor term inside an
unrelated Domain 4 fairness-audit scenario, with no actual explanation of
bagging, boosting, or voting anywhere. These tests guard the new
subsection added to close that gap: it must exist inside "## 7.
Overfitting, underfitting, and the bias-variance trade-off", be linked
from the table of contents, define bagging/boosting/voting with their
canonical algorithms (Random Forest, Gradient Boosting), include a worked
example contrasting when bagging helps against when the problem instead
needs a different model architecture, and include an exam tip -- without
adding any new numbered section or extra mini-quiz block (this repo's
structural tests assert exact counts for both).

Mirrors the conventions established in
tests/test_domain_3_rlhf_subsection.py.

Run with:
    python3 -m unittest tests/test_domain_1_ensemble_methods_subsection.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-1-fundamentals-of-ai-and-ml.md"
)

HEADING = "### Ensemble methods: bagging, boosting, and voting"
TOC_LINK = (
    "[Ensemble methods: bagging, boosting, and voting]"
    "(#ensemble-methods-bagging-boosting-and-voting)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain1EnsembleMethodsSubsection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.subsection = _section(
            cls.text,
            re.escape(HEADING),
            r"\n#{1,3} |\n---\n",
        )

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_sits_inside_section_7_after_the_mini_quiz(self):
        # The subsection was added after Section 7's existing mini-quiz
        # (which must stay the section's only mini-quiz), but must still
        # land inside Section 7, before the next top-level heading begins.
        section_7 = _section(
            self.text,
            r"\n## 7\. Overfitting, underfitting, and the bias",
            r"\n## Worked example: end-to-end ML lifecycle",
        )
        heading_pos = section_7.index(HEADING)
        quiz_pos = section_7.index(
            "#### Mini-quiz: Test your understanding of overfitting"
        )
        self.assertGreater(
            heading_pos,
            quiz_pos,
            "Ensemble methods subsection should follow Section 7's "
            "existing mini-quiz",
        )

    def test_defines_bagging_boosting_and_voting_with_canonical_algorithms(self):
        for term in ["Bagging", "Boosting", "Voting"]:
            with self.subTest(term=term):
                self.assertRegex(
                    self.subsection,
                    rf"(?i)\*\*{term}",
                    f"subsection should define {term!r} as its own bullet",
                )
        self.assertRegex(
            self.subsection,
            r"(?i)Random Forest",
            "subsection should name Random Forest as the canonical "
            "bagging algorithm",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)Gradient Boosting",
            "subsection should name Gradient Boosting as the canonical "
            "boosting algorithm",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)XGBoost",
            "subsection should tie boosting back to SageMaker's built-in "
            "XGBoost algorithm",
        )

    def test_explains_bagging_reduces_variance_and_boosting_reduces_bias(self):
        self.assertRegex(
            self.subsection,
            r"(?i)bagging.{0,400}reduces?\s+variance|reduces?\s+variance.{0,400}bagging",
            "subsection should explain bagging's variance-reduction effect",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)boosting.{0,400}reduces?\s+bias|reduces?\s+bias.{0,400}boosting",
            "subsection should explain boosting's bias-reduction effect",
        )

    def test_appropriate_for_structured_tabular_data(self):
        self.assertRegex(
            self.subsection,
            r"(?i)structured|tabular",
            "subsection should scope ensembles to structured/tabular data",
        )

    def test_has_a_worked_example_contrasting_bagging_vs_different_architecture(self):
        self.assertRegex(
            self.subsection,
            r"(?i)Worked example",
            "subsection should include a worked example",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)different\s+(model\s+)?architecture",
            "worked example should call out needing a different model "
            "architecture instead of an ensemble for the wrong data type",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)convolutional neural network|CNN",
            "worked example should name a concrete alternative "
            "architecture (e.g. a CNN) for unstructured data",
        )

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-7]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            7,
            "Domain 1 must still have exactly 7 numbered sections",
        )
        section_7 = _section(
            self.text,
            r"\n## 7\. Overfitting, underfitting, and the bias",
            r"\n## Worked example: end-to-end ML lifecycle",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_7)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 7 must still contain exactly one mini-quiz heading",
        )

    def test_does_not_break_mini_quiz_question_numbering(self):
        # Regression guard: the ensemble-methods subsection sits between
        # Section 7's mini-quiz and the closing "---" divider, in the same
        # span the subsection-mini-quiz structural tests scan for numbered
        # quiz questions. Any numbered (markdown ordered) list re-introduced
        # into this subsection would corrupt that scan.
        section_7 = _section(
            self.text,
            r"\n## 7\. Overfitting, underfitting, and the bias",
            r"\n## Worked example: end-to-end ML lifecycle",
        )
        quiz_text_match = re.search(
            r"#### Mini-quiz: Test your understanding of.*?(?=\n---\n|\Z)",
            section_7,
            re.S,
        )
        self.assertIsNotNone(quiz_text_match)
        quiz_text = quiz_text_match.group(0)
        question_numbers = re.findall(r"^(\d+)\.\s", quiz_text, re.M)
        self.assertEqual(
            [int(n) for n in question_numbers],
            list(range(1, len(question_numbers) + 1)),
            "mini-quiz question numbering in Section 7 must stay "
            "sequential and uncorrupted by later subsection content",
        )

    def test_does_not_introduce_a_new_worked_example_heading(self):
        # The repo's DOCUMENTATION_STRUCTURE.md sync tests pin an exact
        # per-domain count of "##"/"###"/"####"-level "Worked example:"
        # headings. This subsection's worked example is deliberately an
        # inline bold paragraph, not a heading, so it must not add to
        # that count.
        heading_worked_examples = re.findall(
            r"(?m)^#{2,4} Worked examples?:", self.text
        )
        self.assertEqual(
            len(heading_worked_examples),
            3,
            "Domain 1 must still have exactly 3 heading-level 'Worked "
            "example' sections",
        )


if __name__ == "__main__":
    unittest.main()
