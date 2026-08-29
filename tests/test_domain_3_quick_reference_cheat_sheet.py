"""Structural validation for the Domain 3 quick-reference cheat sheet.

The gap this covers: none of the five domain guides had a condensed,
one-page cheat sheet for last-minute exam review -- each domain guide runs
1,100+ lines of prose, which makes rapid pre-exam review impractical.
Domain 3 (Applications of Foundation Models) carries the highest exam
weight (~28%) of any domain, so it's the first domain guide to get a
"## Quick-reference cheat sheet" section distilling FM selection criteria,
RAG architecture, the customization spectrum, and the Amazon Bedrock
feature set into roughly a page. These tests assert that section exists,
is linked from the table of contents, and actually covers each of those
required topics -- so a future edit can't silently drop the section or
let it drift out of sync with the material it condenses.

Mirrors the conventions established in tests/test_domain_3_study_guide.py.

Run with:
    python3 -m unittest tests/test_domain_3_quick_reference_cheat_sheet.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
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
        self.assertIn("28%", self.section)

    def test_covers_fm_selection_criteria(self):
        for criterion in [
            "Task fit",
            "Context window",
            "Modality",
            "Accuracy",
            "Cost",
            "Latency",
            "Customization",
        ]:
            with self.subTest(criterion=criterion):
                self.assertIn(criterion, self.section)

    def test_covers_rag_architecture_pipeline_steps_in_order(self):
        steps = [
            "Ingestion",
            "Chunking",
            "Embedding",
            "Indexing/storage",
            "Retrieval",
            "Augmentation and generation",
        ]
        positions = [self.section.index(step) for step in steps]
        self.assertEqual(
            positions,
            sorted(positions),
            "RAG pipeline steps should appear in pipeline order in the "
            "cheat sheet",
        )

    def test_rag_notes_weights_are_unchanged(self):
        self.assertIn("RAG never changes model\nweights", self.section)

    def test_covers_customization_spectrum(self):
        for approach in [
            "Prompt engineering",
            "RAG",
            "Fine-tuning",
            "Continued pre-training",
        ]:
            with self.subTest(approach=approach):
                self.assertIn(approach, self.section)

    def test_covers_bedrock_feature_set(self):
        for feature in [
            "Model access",
            "Agents",
            "Guardrails",
            "Knowledge Bases",
            "Automatic model evaluation",
            "Human evaluation",
            "Provisioned throughput",
            "On-demand",
        ]:
            with self.subTest(feature=feature):
                self.assertIn(feature, self.section)

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
            "#1-design-considerations-for-foundation-model-applications",
            "#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases",
            "#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering",
            "#5-amazon-bedrock-features",
        ]:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.section)


if __name__ == "__main__":
    unittest.main()
