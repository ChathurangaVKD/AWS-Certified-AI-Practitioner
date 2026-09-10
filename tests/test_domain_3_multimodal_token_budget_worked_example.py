"""Structural validation for the "Worked example: budgeting tokens for a
multimodal financial-report RAG pipeline (text + tables + images)"
subsection added to docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 covers multimodal applications as a design
consideration (Section 1) and embeddings for search (Section 6), and it
already has a worked example contrasting *retrieval patterns* for a
multimodal product-catalog RAG system (dual embedding indexes vs. a single
combined index) -- but nothing shows how to *budget tokens* when a single
source document mixes text and images, e.g. a financial report with dense
tables plus prose, where the design choice is between embedding a text
summary only, OCR'ing tables to text, or embedding images directly. These
tests guard the new subsection added immediately after the "Worked
example: when to use Cohere Rerank in a RAG pipeline" subsection (and
before the vector-databases-and-embeddings mini-quiz): it must exist, be
linked from the table of contents, sit in the right place in reading
order, name the three representation options with a concrete per-table
token cost for each, roll those costs into a full request's token budget,
and land on an explicit, content-type-specific verdict justified by the
quantified figures.

Mirrors the conventions established in
tests/test_domain_3_context_window_budget_worked_example.py and
tests/test_domain_3_multimodal_retrieval_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_multimodal_token_budget_worked_example.py -v
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
    "#### Worked example: budgeting tokens for a multimodal "
    "financial-report RAG pipeline (text + tables + images)"
)
HEADING_REGEX = re.escape(HEADING)
TOC_LINK = (
    "[Worked example: budgeting tokens for a multimodal financial-report "
    "RAG pipeline (text + tables + images)]"
    "(#worked-example-budgeting-tokens-for-a-multimodal-financial-report-rag-pipeline-text--tables--images)"
)


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


class TestDomain3MultimodalTokenBudgetWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_appears_after_the_cohere_rerank_worked_example(self):
        rerank_pos = self.text.index(
            "#### Worked example: when to use Cohere Rerank in a RAG pipeline"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(
            rerank_pos,
            heading_pos,
            "new worked example should come after the Cohere Rerank "
            "worked example",
        )

    def test_appears_before_the_embeddings_mini_quiz(self):
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(
            "#### Mini-quiz: Test your understanding of vector databases "
            "and embeddings"
        )
        self.assertLess(heading_pos, mini_quiz_pos)

    def test_is_distinct_from_the_multimodal_retrieval_worked_example(self):
        # This is a token-budgeting example, not the earlier retrieval-
        # pattern example -- confirm both exist independently.
        self.assertIn(
            "#### Worked example: retrieval patterns for a multimodal "
            "product-catalog RAG system (text + images)",
            self.text,
        )
        self.assertNotEqual(
            self.text.index(HEADING),
            self.text.index(
                "#### Worked example: retrieval patterns for a multimodal "
                "product-catalog RAG system (text + images)"
            ),
        )

    def test_scenario_is_a_financial_report_with_tables_and_charts(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertRegex(self.section, r"(?i)50-page")
        self.assertRegex(self.section, r"(?i)financial reports?")
        self.assertRegex(self.section, r"(?i)tables")
        self.assertRegex(self.section, r"(?i)charts?")

    def test_names_the_three_representation_options(self):
        self.assertIn("Option A", self.section)
        self.assertIn("Option B", self.section)
        self.assertIn("Option C", self.section)
        self.assertRegex(self.section, r"(?i)text summary only")
        self.assertRegex(self.section, r"(?i)OCR")
        self.assertRegex(self.section, r"(?i)embed the image directly|raw image")

    def test_names_a_concrete_multimodal_embedding_model(self):
        self.assertIn("Amazon Titan Multimodal Embeddings", self.section)

    def test_quantifies_a_per_table_token_cost_for_each_option(self):
        for marker in ["~80 tokens", "~330 tokens", "~1,600 tokens"]:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.section)

    def test_rolls_per_table_costs_into_a_full_request_budget(self):
        for marker in [
            "5 × 80 = 400",
            "5 × 330 = 1,650",
            "5 × 1,600 = 8,000",
            "**2,340**",
            "**3,590**",
            "**9,940**",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.section)

    def test_flags_the_8k_context_window_overflow(self):
        self.assertRegex(
            self.section,
            r"(?i)8K-context model|8K context",
        )
        self.assertRegex(self.section, r"(?i)overflows the window")

    def test_lands_on_a_content_type_specific_verdict(self):
        self.assertRegex(
            self.section,
            r"(?is)\*\*choice:\s*option b.{0,120}option c",
            "expected an explicit choice statement splitting tables "
            "(Option B) from charts (Option C)",
        )
        self.assertRegex(
            self.section,
            r"(?is)option a is rejected",
            "expected the text-summary-only option to be explicitly "
            "rejected for this scenario",
        )

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.section)

    def test_is_a_single_self_contained_subsection_with_no_new_headings(self):
        nested_headings = re.findall(r"^#{1,6} .+$", self.section, re.M)
        self.assertEqual(
            nested_headings,
            [],
            f"worked example should not contain nested headings: {nested_headings!r}",
        )


if __name__ == "__main__":
    unittest.main()
