"""Structural validation for the Domain 4 quick-reference cheat sheet.

The gap this covers: Domain 3 (Applications of Foundation Models) already
has an effective "## Quick-reference cheat sheet" section for last-minute
exam review, but Domain 4 (Guidelines for Responsible AI) had no
equivalent -- readers had to re-skim 1,200+ lines of prose to refresh the
8 responsible AI dimensions and the 6 bias categories in training data
right before the exam. These tests assert that a condensed cheat sheet
section exists, is linked from the table of contents, sits between the
comparison table and the glossary (mirroring Domain 3's placement), and
actually covers each of the 8 dimensions and 6 bias categories as key-fact
tables -- so a future edit can't silently drop the section or let it
drift out of sync with the material it condenses.

Mirrors the conventions established in
tests/test_domain_3_quick_reference_cheat_sheet.py.

Run with:
    python3 -m unittest tests/test_domain_4_quick_reference_cheat_sheet.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-4-guidelines-for-responsible-ai.md"
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

    def test_covers_all_eight_responsible_ai_dimensions(self):
        for dimension in [
            "Fairness",
            "Explainability",
            "Privacy and security",
            "Transparency",
            "Veracity and robustness",
            "Governance",
            "Safety",
            "Controllability",
        ]:
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, self.section)

    def test_dimensions_map_to_aws_tools(self):
        for tool in [
            "Amazon SageMaker Clarify",
            "Guardrails for Amazon Bedrock",
            "SageMaker Model Cards",
            "Amazon A2I",
        ]:
            with self.subTest(tool=tool):
                self.assertIn(tool, self.section)

    def test_covers_all_six_bias_categories(self):
        for bias_type in [
            "Sampling bias",
            "Measurement bias",
            "Label bias / human bias",
            "Historical bias",
            "Exclusion bias",
            "Aggregation bias",
        ]:
            with self.subTest(bias_type=bias_type):
                self.assertIn(bias_type, self.section)

    def test_covers_bias_mitigation_stages(self):
        for stage in ["Pre-processing", "In-processing", "Post-processing"]:
            with self.subTest(stage=stage):
                self.assertIn(stage, self.section)

    def test_covers_bias_detection_metrics(self):
        for metric in [
            "Difference in proportions of labels (DPL)",
            "Class imbalance",
            "Disparate impact",
        ]:
            with self.subTest(metric=metric):
                self.assertIn(metric, self.section)

    def test_content_is_tabular_not_prose(self):
        # The task calls for key-facts/decision tables rather than prose.
        # Expect at least three markdown tables (header + separator rows).
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.section)
        self.assertGreaterEqual(
            len(table_separator_rows),
            3,
            "expected at least 3 markdown tables in the cheat sheet",
        )

    def test_has_key_definitions_callout(self):
        self.assertIn("Key definitions to have cold", self.section)

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
            "#1-core-dimensions-of-responsible-ai",
            "#2-identifying-bias-and-fairness-issues-in-training-data-and-model-outputs",
            "#3-aws-tools-for-responsible-ai",
        ]:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.section)

    def test_distinguishes_bias_from_variance(self):
        self.assertIn("variance", self.section)


if __name__ == "__main__":
    unittest.main()
