"""Structural validation for the "Curating a fine-tuning dataset: size
thresholds, a quality checklist, and synthetic vs. real data" subsection
added to docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 4 explained fine-tuning techniques
(LoRA, QLoRA, RLHF, continued pre-training) in depth but gave minimal
guidance on preparing the training data itself -- minimum dataset sizes
by model/technique, how to judge data quality, when synthetic data is an
acceptable substitute for real data, and how to avoid overfitting on
small datasets. These tests guard the new subsection added to close that
gap: it must exist inside "## 4. Fine-tuning vs. continued pre-training
vs. RAG vs. prompt engineering", after the section's existing RLHF
subsection, be linked from the table of contents, contain a decision
table mapping model/technique to a recommended dataset size, a
data-quality checklist covering diversity/edge-case coverage/label
correctness/class balance, a synthetic-vs-real data comparison table, and
a worked example curating a dataset for a domain-specific task --
without adding any new numbered section or extra mini-quiz block (this
repo's structural tests assert exact counts for both), and without
introducing a numbered list that would corrupt the section's mini-quiz
question-numbering scan.

Mirrors the conventions established in
tests/test_domain_3_rlhf_subsection.py.

Run with:
    python3 -m unittest tests/test_domain_3_fine_tuning_dataset_curation_subsection.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

HEADING = (
    "### Curating a fine-tuning dataset: size thresholds, a quality "
    "checklist, and synthetic vs. real data"
)
TOC_LINK = (
    "[Curating a fine-tuning dataset: size thresholds, a quality "
    "checklist, and synthetic vs. real data]"
    "(#curating-a-fine-tuning-dataset-size-thresholds-a-quality-checklist-"
    "and-synthetic-vs-real-data)"
)
WORKED_EXAMPLE_HEADING = (
    "#### Worked example: curating a dataset for a domain-specific "
    "fine-tuning task"
)
WORKED_EXAMPLE_TOC_LINK = (
    "[Worked example: curating a dataset for a domain-specific "
    "fine-tuning task]"
    "(#worked-example-curating-a-dataset-for-a-domain-specific-fine-"
    "tuning-task)"
)
RLHF_HEADING = (
    "### Reinforcement Learning from Human Feedback (RLHF): aligning "
    "fine-tuned models to human preferences"
)
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of customization approach "
    "trade-offs"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3FineTuningDatasetCurationSubsection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.subsection = _section(
            cls.text,
            re.escape(HEADING),
            r"\n---\n",
        )

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)
        self.assertIn(WORKED_EXAMPLE_TOC_LINK, toc)

    def test_sits_inside_section_4_after_the_rlhf_subsection(self):
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        heading_pos = section_4.index(HEADING)
        rlhf_pos = section_4.index(RLHF_HEADING)
        quiz_pos = section_4.index(MINI_QUIZ_HEADING)
        self.assertGreater(
            heading_pos,
            rlhf_pos,
            "dataset-curation subsection should follow the RLHF subsection",
        )
        self.assertGreater(
            heading_pos,
            quiz_pos,
            "dataset-curation subsection should follow Section 4's "
            "existing mini-quiz",
        )

    def test_has_a_dataset_size_decision_table(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection
        )
        self.assertTrue(tables, "expected a Markdown decision table")
        size_tables = [t for t in tables if "LoRA" in t and "examples" in t]
        self.assertTrue(
            size_tables,
            "expected a table mapping technique/model scale to a "
            "recommended dataset size",
        )
        table = size_tables[0]
        for expected in [
            "LoRA",
            "Full fine-tuning",
            "Continued pre-training",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, table)

    def test_has_a_data_quality_checklist(self):
        self.assertIn("#### Data-quality checklist", self.subsection)
        checklist_section = _section(
            self.subsection,
            re.escape("#### Data-quality checklist"),
            r"\n#### ",
        )
        for expected in [
            r"(?i)diversity",
            r"(?i)edge-case coverage",
            r"(?i)label correctness",
            r"(?i)class",
        ]:
            with self.subTest(expected=expected):
                self.assertRegex(checklist_section, expected)

    def test_has_a_synthetic_vs_real_data_comparison(self):
        self.assertRegex(self.subsection, r"(?i)synthetic")
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection
        )
        synthetic_tables = [
            t for t in tables if "Synthetic data" in t and "Real" in t
        ]
        self.assertTrue(
            synthetic_tables,
            "expected a table comparing synthetic vs. real training data",
        )

    def test_has_a_worked_example_curating_a_domain_specific_dataset(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.subsection)
        worked_example = _section(
            self.subsection,
            re.escape(WORKED_EXAMPLE_HEADING),
            r"\n---\n",
        )
        self.assertRegex(worked_example, r"(?i)\bScenario\b")
        self.assertRegex(worked_example, r"(?i)class balance|imbalance")

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-8]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            8,
            "Domain 3 must still have exactly 8 numbered sections",
        )
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_4)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 4 must still contain exactly one mini-quiz heading",
        )

    def test_does_not_break_mini_quiz_question_numbering(self):
        # Regression guard, mirroring the RLHF subsection's own test: this
        # subsection sits between Section 4's mini-quiz and its closing
        # "---" divider, in the same span the subsection-mini-quiz
        # structural tests scan for numbered quiz questions. Any
        # top-level numbered (markdown ordered) list re-introduced here
        # would corrupt that scan.
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        quiz_text_match = re.search(
            r"#### Mini-quiz: Test your understanding of.*?(?=\n---\n|\Z)",
            section_4,
            re.S,
        )
        self.assertIsNotNone(quiz_text_match)
        quiz_text = quiz_text_match.group(0)
        question_numbers = re.findall(r"^(\d+)\.\s", quiz_text, re.M)
        self.assertEqual(
            [int(n) for n in question_numbers],
            list(range(1, len(question_numbers) + 1)),
            "mini-quiz question numbering in Section 4 must stay "
            "sequential and uncorrupted by later subsection content",
        )


if __name__ == "__main__":
    unittest.main()
