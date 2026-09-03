"""Structural validation for the "Worked example: when to use Cohere
Rerank in a RAG pipeline" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: "## 6. Vector databases and embeddings for search
and retrieval" has a "Reranking and hybrid search" subsection with a
comparison table that labels reranking "essential" or "nice-to-have" in
purely qualitative terms, but no worked example quantifying the actual
cost/latency/precision trade-off of adding a reranker to a retrieval
pipeline. These tests guard the new subsection added immediately after
that comparison table's decision tree and exam tip (and before the
section's mini-quiz): it must exist, sit in the right place in reading
order, name Cohere Rerank as the concrete reranking model, measure a
vector-only baseline against a reranked pipeline across precision,
recall, latency, and per-query cost, and land on two explicit,
contrasting verdicts (add it / skip it) justified by the numbers.

Run with:
    python3 -m unittest tests/test_domain_3_cohere_rerank_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

HEADING = "#### Worked example: when to use Cohere Rerank in a RAG pipeline"
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


class TestDomain3CohereRerankWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_listed_in_table_of_contents(self):
        self.assertIn(
            "[Worked example: when to use Cohere Rerank in a RAG "
            "pipeline](#worked-example-when-to-use-cohere-rerank-in-a-"
            "rag-pipeline)",
            self.text,
        )

    def test_appears_after_the_reranking_comparison_table_and_exam_tip(self):
        table_header_pos = self.text.index(
            "| Dimension | Reranking | Hybrid (vector + keyword) search |"
        )
        decision_tree_pos = self.text.index(
            'START(["Retrieval quality problem,\\nor designing retrieval '
            'upfront?"])'
        )
        exam_tip_pos = self.text.index(
            "> **Exam tip:** A scenario describing the FM giving answers "
            "built from"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(table_header_pos, decision_tree_pos)
        self.assertLess(decision_tree_pos, exam_tip_pos)
        self.assertLess(
            exam_tip_pos,
            heading_pos,
            "worked example should come after the existing reranking "
            "comparison table, decision tree, and exam tip",
        )

    def test_appears_before_the_section_6_mini_quiz(self):
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(
            "#### Mini-quiz: Test your understanding of vector databases "
            "and embeddings"
        )
        self.assertLess(heading_pos, mini_quiz_pos)

    def test_appears_before_section_7(self):
        heading_pos = self.text.index(HEADING)
        section_7_pos = self.text.index(
            "## 7. Evaluating foundation model performance"
        )
        self.assertLess(heading_pos, section_7_pos)

    def test_scenario_is_an_ecommerce_product_search_scenario(self):
        self.assertRegex(
            self.section,
            r"(?i)e-commerce|retailer|product-search|shopper",
            "expected an e-commerce product-search framing for the "
            "scenario",
        )
        self.assertIn("Cohere Rerank", self.section)

    def test_names_cohere_rerank_as_a_bedrock_reranking_model(self):
        self.assertRegex(
            self.section,
            r"(?i)cohere rerank.{0,80}bedrock|bedrock.{0,80}cohere rerank",
            "expected Cohere Rerank to be tied to Amazon Bedrock as the "
            "concrete reranking model option",
        )

    def test_measures_precision_recall_latency_and_cost(self):
        for marker in ["Precision@5", "Recall@50", "latency", "cost"]:
            with self.subTest(marker=marker):
                self.assertRegex(self.section, re.escape(marker))

    def test_quantifies_vector_only_vs_reranked_metrics(self):
        # The vector-only baseline and the reranked pipeline should each
        # report explicit precision figures so the comparison is
        # quantitative, not just qualitative.
        self.assertIn("0.62", self.section)
        self.assertIn("0.85", self.section)

    def test_converts_the_per_query_delta_into_a_monthly_cost(self):
        self.assertRegex(
            self.section,
            r"(?i)2,000,000 queries/month|2,000,000\s*×",
            "expected the per-query cost to be multiplied out across "
            "monthly query volume",
        )
        self.assertRegex(self.section, r"(?i)\$4,000/month|~\$4,000")

    def test_lands_on_an_explicit_add_it_verdict_for_the_high_volume_scenario(self):
        self.assertRegex(
            self.section,
            r"(?i)choice:\s*\*\*add cohere rerank\*\*|\*\*choice:\s*add "
            r"cohere rerank\.?\*\*",
            "expected an explicit choice statement to add Cohere Rerank "
            "for the large-retailer scenario",
        )

    def test_lands_on_an_explicit_skip_it_verdict_for_the_low_headroom_scenario(self):
        self.assertRegex(
            self.section,
            r"(?i)skip it",
            "expected an explicit contrasting verdict where reranking is "
            "not worth adding",
        )
        self.assertRegex(
            self.section,
            r"(?i)5,000-sku|boutique",
            "expected a second, contrasting scenario with a small/narrow "
            "catalog",
        )

    def test_is_a_single_self_contained_subsection_with_no_new_headings(self):
        # Should not introduce any nested headings of its own -- it must
        # stay a single subsection, not a rewrite of the surrounding
        # section.
        nested_headings = re.findall(r"^#{1,6} .+$", self.section, re.M)
        self.assertEqual(
            nested_headings,
            [],
            f"worked example should not contain nested headings: {nested_headings!r}",
        )


if __name__ == "__main__":
    unittest.main()
