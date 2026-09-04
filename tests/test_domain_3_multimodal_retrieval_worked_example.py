"""Structural validation for the "Worked example: retrieval patterns for
a multimodal product-catalog RAG system (text + images)" subsection added
to docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 3's RAG worked examples ("Selecting
a vector store for a compliance-document Q&A assistant" and "building a
product-knowledge assistant using Kendra's GenAI Index") are both
text-only retrieval scenarios, and the domain's separate token-budgeting
worked example (further down the document) is unrelated to retrieval
design. Neither covers designing a retrieval pattern for a source that
mixes text and images -- e.g. a product catalog RAG system that must
retrieve over both product descriptions and product photos. These tests
guard the new subsection added immediately after the Kendra GenAI Index
worked example (and before Section 4 begins): it must exist, sit in the
right place in reading order, contrast dual embedding indexes against a
single multimodal embedding index, explain how results from each
modality get merged before generation, and land on two explicit,
contrasting verdicts justified by quantified figures.

Run with:
    python3 -m unittest tests/test_domain_3_multimodal_retrieval_worked_example.py -v
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
    "#### Worked example: retrieval patterns for a multimodal "
    "product-catalog RAG system (text + images)"
)
HEADING_REGEX = re.escape(HEADING)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,4} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading (level 1-4), or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3MultimodalRetrievalWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_appears_after_the_kendra_genai_index_worked_example(self):
        kendra_heading_pos = self.text.index(
            "#### Worked example: building a product-knowledge assistant "
            "using Kendra's GenAI Index as a Bedrock Knowledge Base data "
            "source"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(
            kendra_heading_pos,
            heading_pos,
            "new worked example should come after the existing Kendra "
            "GenAI Index worked example",
        )

    def test_appears_before_section_4(self):
        heading_pos = self.text.index(HEADING)
        section_4_pos = self.text.index(
            "## 4. Fine-tuning vs. continued pre-training vs. RAG vs. "
            "prompt engineering"
        )
        self.assertLess(heading_pos, section_4_pos)

    def test_is_distinct_from_the_token_budgeting_worked_example(self):
        # The task calls out that this must be a *separate* worked example
        # from the context-window token-budgeting one -- confirm both
        # headings exist independently and this one isn't a rename/merge.
        self.assertIn(
            "## Worked example: estimating a context-window token budget",
            self.text,
        )
        self.assertNotEqual(
            self.text.index(HEADING),
            self.text.index(
                "## Worked example: estimating a context-window token "
                "budget"
            ),
        )

    def test_scenario_is_a_product_catalog_with_text_and_images(self):
        self.assertRegex(self.section, r"(?i)product-catalog|product catalog")
        self.assertRegex(self.section, r"(?i)SKUs?")
        self.assertRegex(self.section, r"(?i)product photos|images")
        self.assertRegex(self.section, r"(?i)text description")

    def test_contrasts_dual_indexes_with_single_multimodal_index(self):
        self.assertRegex(self.section, r"(?i)dual embedding indexes?")
        self.assertRegex(self.section, r"(?i)single (?:combined |shared )?multimodal (?:embedding )?index")
        self.assertIn("Option A", self.section)
        self.assertIn("Option B", self.section)

    def test_names_a_concrete_multimodal_embedding_model(self):
        self.assertIn("Amazon Titan Multimodal Embeddings", self.section)

    def test_explains_the_merge_step_between_modalities(self):
        self.assertRegex(
            self.section,
            r"(?i)reciprocal rank fusion|RRF",
            "expected an explicit fusion/merge mechanism to be named",
        )
        self.assertRegex(self.section, r"(?i)merge|fusion")

    def test_quantifies_recall_and_precision_for_both_options(self):
        for marker in ["Recall@10", "Precision@5"]:
            with self.subTest(marker=marker):
                self.assertRegex(self.section, re.escape(marker))
        # Spec-only recall figures that motivate the verdict.
        self.assertIn("0.87", self.section)
        self.assertIn("0.61", self.section)

    def test_lands_on_an_explicit_choice_verdict_for_the_dual_index_scenario(self):
        self.assertRegex(
            self.section,
            r"(?i)\*\*choice:\s*option a",
            "expected an explicit choice statement favoring the dual-index "
            "pattern for the furniture-catalog scenario",
        )

    def test_lands_on_a_contrasting_scenario_favoring_the_single_index(self):
        self.assertRegex(
            self.section,
            r"(?i)single combined index.{0,40}wins instead|wins instead",
            "expected an explicit contrasting scenario favoring the "
            "single-index pattern",
        )
        self.assertRegex(
            self.section,
            r"(?i)art-print|boutique",
            "expected a second, contrasting scenario with a visually-"
            "dominant, text-light catalog",
        )

    def test_is_a_single_self_contained_subsection_with_no_new_headings(self):
        nested_headings = re.findall(r"^#{1,6} .+$", self.section, re.M)
        self.assertEqual(
            nested_headings,
            [],
            f"worked example should not contain nested headings: {nested_headings!r}",
        )


if __name__ == "__main__":
    unittest.main()
