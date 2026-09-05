"""Structural validation for the "Amazon SageMaker Ground Truth: data
labeling and when NOT to use it" subsection added to
docs/domain-1-fundamentals-of-ai-and-ml.md.

The gap this covers: SageMaker Ground Truth appears in this repo's mock
exam (docs/mock-exam.md) as both a plausible correct answer and a
distractor, but before this subsection no domain guide ever explained
what it does, when to reach for it, or how it differs from manual
labeling, SageMaker Data Wrangler, or synthetic data generation. These
tests guard the new subsection added to close that gap: it must exist
inside "## 5. AWS managed AI/ML services (conceptual overview)", be
linked from the table of contents, describe Ground Truth as a
human-in-the-loop labeling service (not an inference service), include a
comparison table covering Ground Truth vs. manual labeling vs. Data
Wrangler vs. synthetic data generation, include concrete use-case
scenarios illustrating scale thresholds (a 100K-image dataset vs. a
50-image dataset), and include an exam tip distinguishing when Ground
Truth is the correct exam answer versus a distractor -- without adding
any new numbered section or extra mini-quiz block (this repo's
structural tests assert exact counts for both).

Mirrors the conventions established in
tests/test_domain_1_ensemble_methods_subsection.py.

Run with:
    python3 -m unittest tests/test_domain_1_sagemaker_ground_truth_subsection.py -v
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
TOC_LINK = (
    "[Amazon SageMaker Ground Truth: data labeling and when NOT to use it]"
    "(#amazon-sagemaker-ground-truth-data-labeling-and-when-not-to-use-it)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain1SageMakerGroundTruthSubsection(unittest.TestCase):
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

    def test_sits_inside_section_5_after_the_mini_quiz(self):
        # The subsection was added after Section 5's existing mini-quiz
        # (which must stay the section's only mini-quiz), but must still
        # land inside Section 5, before Section 6 begins.
        section_5 = _section(
            self.text,
            r"\n## 5\. AWS managed AI/ML services \(conceptual overview\)",
            r"\n## 6\. Model evaluation basics",
        )
        heading_pos = section_5.index(HEADING)
        quiz_pos = section_5.index(
            "#### Mini-quiz: Test your understanding of AWS managed AI/ML "
            "services"
        )
        self.assertGreater(
            heading_pos,
            quiz_pos,
            "Ground Truth subsection should follow Section 5's existing "
            "mini-quiz",
        )

    def test_describes_ground_truth_as_human_in_the_loop_labeling_service(self):
        self.assertRegex(
            self.subsection,
            r"(?i)human-in-the-loop",
            "subsection should describe Ground Truth as human-in-the-loop",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)active learning",
            "subsection should mention active learning as part of how "
            "Ground Truth reduces human labeling effort",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)labe?ling",
            "subsection should frame Ground Truth around data labeling",
        )

    def test_comparison_table_covers_all_four_approaches(self):
        for term in [
            "SageMaker Ground Truth",
            "Manual labeling",
            "SageMaker Data Wrangler",
            "Synthetic data generation",
        ]:
            with self.subTest(term=term):
                self.assertIn(
                    term,
                    self.subsection,
                    f"comparison table should include a row for {term!r}",
                )
        # Confirm it's an actual markdown table (header separator row).
        self.assertRegex(self.subsection, r"\|---\|---\|---\|---\|")

    def test_use_case_scenarios_illustrate_scale_thresholds(self):
        self.assertRegex(
            self.subsection,
            r"100,000|100K",
            "subsection should give a large-scale (100K-image) Ground "
            "Truth use case",
        )
        self.assertRegex(
            self.subsection,
            r"50-image",
            "subsection should give a small-scale (50-image) manual-"
            "labeling counter-example",
        )

    def test_has_an_exam_tip_distinguishing_correct_answer_from_distractor(self):
        self.assertIn("Exam tip:", self.subsection)
        self.assertRegex(
            self.subsection,
            r"(?i)correct.{0,80}answer",
            "exam tip should describe when Ground Truth is the correct "
            "answer",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)distractor",
            "exam tip should describe when Ground Truth is a distractor",
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
        # The repo's DOCUMENTATION_STRUCTURE.md sync tests pin an exact
        # per-domain count of "##"/"###"/"####"-level "Worked example:"
        # headings. This subsection's scenarios are deliberately inline
        # bold bullets, not headings, so they must not add to that count.
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
        # Regression guard: the Ground Truth subsection sits between
        # Section 5's mini-quiz and the closing "---" divider, in the same
        # span the subsection-mini-quiz structural tests scan for numbered
        # quiz questions. Any numbered (markdown ordered) list re-introduced
        # into this subsection would corrupt that scan.
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
            "sequential and uncorrupted by later subsection content",
        )


if __name__ == "__main__":
    unittest.main()
