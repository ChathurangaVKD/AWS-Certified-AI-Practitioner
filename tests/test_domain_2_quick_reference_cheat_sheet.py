"""Structural validation for the Domain 2 quick-reference cheat sheet.

The gap this covers: Domain 3 (Applications of Foundation Models) already
has a condensed "## Quick-reference cheat sheet" section for last-minute
exam review, but Domain 2 (Fundamentals of Generative AI) -- the largest
single knowledge domain on the exam at ~24% of scored questions -- had no
equivalent. This adds a matching cheat sheet distilling transformer
architecture/self-attention, inference parameters, and foundation model
selection criteria into key facts and decision tables. These tests assert
the section exists, is linked from the table of contents, sits in the same
place relative to the comparison table and glossary as Domain 3's does, and
actually covers each required topic -- so a future edit can't silently drop
the section or let it drift out of sync with the material it condenses.

Mirrors the conventions established in
tests/test_domain_3_quick_reference_cheat_sheet.py.

Run with:
    python3 -m unittest tests/test_domain_2_quick_reference_cheat_sheet.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-2-fundamentals-of-generative-ai.md"
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

    def test_mentions_domain_weight(self):
        self.assertIn("24%", self.section)

    def test_covers_transformer_pipeline_stages_in_order(self):
        stages = [
            "Input text",
            "Tokenization",
            "Embeddings",
            "Positional encoding",
            "Self-attention",
            "Feed-forward network",
            "Output",
        ]
        positions = [self.section.index(stage) for stage in stages]
        self.assertEqual(
            positions,
            sorted(positions),
            "transformer pipeline stages should appear in pipeline order "
            "in the cheat sheet",
        )

    def test_notes_self_attention_is_defining_innovation(self):
        self.assertIn("Self-attention is the defining innovation", self.section)

    def test_covers_inference_parameters(self):
        for parameter in [
            "Temperature",
            "Top-p (nucleus sampling)",
            "Top-k",
            "Max tokens (maximum length)",
            "Stop sequences",
        ]:
            with self.subTest(parameter=parameter):
                self.assertIn(parameter, self.section)

    def test_inference_parameter_table_has_low_and_high_columns(self):
        self.assertIn("Low / small value", self.section)
        self.assertIn("High / large value", self.section)

    def test_notes_inference_parameters_do_not_reduce_hallucination(self):
        self.assertIn("hallucination", self.section)
        self.assertIn(
            "none of them retrain or change model weights", self.section
        )

    def test_covers_fm_selection_criteria_checklist(self):
        for criterion in [
            "Cost",
            "Modality",
            "Latency",
            "Context window",
            "Fine-tuning / customization support",
            "Model size, accuracy, licensing",
        ]:
            with self.subTest(criterion=criterion):
                self.assertIn(criterion, self.section)

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
            "#1-generative-ai-core-concepts",
            "#6-prompt-engineering-fundamentals",
            "#7-foundation-model-selection-criteria",
        ]:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.section)


if __name__ == "__main__":
    unittest.main()
