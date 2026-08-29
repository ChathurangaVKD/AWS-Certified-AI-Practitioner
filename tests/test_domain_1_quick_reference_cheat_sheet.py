"""Structural validation for the Domain 1 quick-reference cheat sheet.

The gap this covers: Domain 3 (Applications of Foundation Models) has a
condensed "## Quick-reference cheat sheet" section for last-minute exam
review, but Domain 1 (Fundamentals of AI and ML) had no equivalent, even
though its own material -- the 8-stage ML development lifecycle, the three
learning types, and the AWS managed AI/ML service decision table -- is
exactly the kind of high-yield, easily-condensed content that benefits from
a one-page recap. These tests assert that section exists, is linked from
the table of contents, sits in the same place in the document as Domain
3's (between the comparison table and the glossary), and actually covers
each of the required topics -- so a future edit can't silently drop the
section or let it drift out of sync with the material it condenses.

Mirrors the conventions established in
tests/test_domain_3_quick_reference_cheat_sheet.py.

Run with:
    python3 -m unittest tests/test_domain_1_quick_reference_cheat_sheet.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-1-fundamentals-of-ai-and-ml.md"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _cheat_sheet_section(text):
    match = re.search(r"\n## Quick-reference cheat sheet\n(.*?)(?=\n## )", text, re.S)
    assert match, "expected a '## Quick-reference cheat sheet' section"
    return match.group(1)


class TestQuickReferenceCheatSheetExistsAndIsLinked(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_cheat_sheet_heading_present(self):
        self.assertIn("\n## Quick-reference cheat sheet\n", self.text)

    def test_cheat_sheet_linked_from_table_of_contents(self):
        toc_match = re.search(r"\n## Table of contents\n(.*?)\n## ", self.text, re.S)
        self.assertIsNotNone(toc_match)
        toc = toc_match.group(1)
        self.assertIn(
            "[Quick-reference cheat sheet](#quick-reference-cheat-sheet)",
            toc,
            "table of contents should link to the quick-reference cheat "
            "sheet section",
        )

    def test_cheat_sheet_sits_between_comparison_table_and_glossary(self):
        # Regression guard for placement: the cheat sheet should recap
        # material the reader has just finished (the numbered sections and
        # the comparison table) right before the glossary/practice
        # questions, not be buried mid-document.
        comparison_idx = self.text.index("\n## Comparison table")
        cheat_sheet_idx = self.text.index("\n## Quick-reference cheat sheet")
        glossary_idx = self.text.index("\n## Key terms glossary")
        self.assertLess(comparison_idx, cheat_sheet_idx)
        self.assertLess(cheat_sheet_idx, glossary_idx)


class TestQuickReferenceCheatSheetContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _cheat_sheet_section(cls.text)

    def test_covers_all_eight_lifecycle_stages_in_order(self):
        stages = [
            "Business goal identification",
            "Data collection",
            "Exploratory data analysis (EDA)",
            "Data preparation / feature engineering",
            "Model training",
            "Hyperparameter tuning / evaluation",
            "Deployment",
            "Monitoring",
        ]
        positions = [self.section.index(stage) for stage in stages]
        self.assertEqual(
            positions,
            sorted(positions),
            "ML lifecycle stages should appear in lifecycle order in the "
            "cheat sheet",
        )

    def test_lifecycle_loop_back_behavior_covered(self):
        self.assertIn("loops back to feature engineering", self.section)
        self.assertIn("Feature Store", self.section)

    def test_covers_three_learning_types_with_distinguishers(self):
        for learning_type in ["Supervised", "Unsupervised", "Reinforcement"]:
            with self.subTest(learning_type=learning_type):
                self.assertIn(learning_type, self.section)
        # One-line distinguishers: labeled vs. unlabeled vs. agent/reward.
        self.assertIn("Labeled", self.section)
        self.assertIn("Unlabeled", self.section)
        self.assertIn("agent", self.section.lower())
        self.assertIn("reward", self.section.lower())

    def test_covers_aws_service_decision_table(self):
        required_services = [
            "Amazon SageMaker",
            "Amazon Rekognition",
            "Amazon Transcribe",
            "Amazon Comprehend",
            "Amazon Polly",
            "Amazon Translate",
            "Amazon Lex",
            "Amazon Personalize",
            "Amazon Forecast",
            "Amazon Textract",
            "Amazon Fraud Detector",
        ]
        for service in required_services:
            with self.subTest(service=service):
                self.assertIn(service, self.section)

    def test_has_decision_tree_for_service_selection(self):
        self.assertIn("Decision tree", self.section)
        self.assertIn("purpose-built", self.section.lower())

    def test_has_common_exam_traps_callout(self):
        self.assertIn("Common exam traps", self.section)
        traps_idx = self.section.index("Common exam traps")
        traps = self.section[traps_idx:]
        # At least three distinct trap bullets should follow the heading.
        bullet_count = traps.count("\n- ")
        self.assertGreaterEqual(
            bullet_count,
            3,
            "expected at least 3 common-exam-trap bullets",
        )

    def test_cross_links_to_source_sections(self):
        for anchor in [
            "#2-the-ml-development-lifecycle",
            "#3-types-of-learning",
            "#5-aws-managed-aiml-services-conceptual-overview",
        ]:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.section)


if __name__ == "__main__":
    unittest.main()
