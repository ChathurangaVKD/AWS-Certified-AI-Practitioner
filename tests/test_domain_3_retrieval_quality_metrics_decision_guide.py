"""Structural validation for the "Retrieval quality metrics: NDCG, MAP,
Recall@k, and MRR" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Section 6 ("Vector databases and embeddings for
search and retrieval") already used Precision@k and Recall@k throughout
its Cohere Rerank worked example, but never explained NDCG, MAP, or MRR --
so a learner could see those metric names elsewhere (e.g., in a retrieval
benchmark writeup) without knowing what each measures, how it's computed,
or which one a given exam scenario is pointing at. These tests guard the
new subsection's comparison table, its metric-selection decision
flowchart, and its worked example computing all four metrics on a small
sample retrieval result set.

Mirrors the conventions established in
tests/test_domain_3_cohere_rerank_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_retrieval_quality_metrics_decision_guide.py -v
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
    "### Retrieval quality metrics: NDCG, MAP, Recall@k, and MRR "
    "(a selection decision guide)"
)
HEADING_REGEX = re.escape(HEADING)

WORKED_EXAMPLE_HEADING = (
    "#### Worked example: computing Recall@k, MRR, MAP, and NDCG on a "
    "sample retrieval result set"
)
WORKED_EXAMPLE_HEADING_REGEX = re.escape(WORKED_EXAMPLE_HEADING)


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


class TestDomain3RetrievalQualityMetricsDecisionGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)
        cls.worked_example = _section(cls.text, WORKED_EXAMPLE_HEADING_REGEX)

    # -- Placement ---------------------------------------------------

    def test_subsection_exists(self):
        self.assertIn(HEADING, self.text)

    def test_listed_in_table_of_contents(self):
        toc = _section(
            self.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        self.assertIn(
            "[Retrieval quality metrics: NDCG, MAP, Recall@k, and MRR "
            "(a selection decision guide)]"
            "(#retrieval-quality-metrics-ndcg-map-recallk-and-mrr-a-"
            "selection-decision-guide)",
            toc,
        )
        self.assertIn(
            "[Worked example: computing Recall@k, MRR, MAP, and NDCG on "
            "a sample retrieval result set]"
            "(#worked-example-computing-recallk-mrr-map-and-ndcg-on-a-"
            "sample-retrieval-result-set)",
            toc,
        )

    def test_appears_after_the_multimodal_token_budget_worked_example(self):
        multimodal_heading_pos = self.text.index(
            "#### Worked example: budgeting tokens for a multimodal "
            "financial-report RAG pipeline"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(multimodal_heading_pos, heading_pos)

    def test_appears_before_the_section_6_mini_quiz_and_section_7(self):
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(
            "#### Mini-quiz: Test your understanding of vector databases "
            "and embeddings"
        )
        section_7_pos = self.text.index(
            "## 7. Evaluating foundation model performance"
        )
        self.assertLess(heading_pos, mini_quiz_pos)
        self.assertLess(mini_quiz_pos, section_7_pos)

    def test_worked_example_appears_inside_the_new_subsection(self):
        heading_pos = self.text.index(HEADING)
        worked_example_pos = self.text.index(WORKED_EXAMPLE_HEADING)
        mini_quiz_pos = self.text.index(
            "#### Mini-quiz: Test your understanding of vector databases "
            "and embeddings"
        )
        self.assertLess(heading_pos, worked_example_pos)
        self.assertLess(worked_example_pos, mini_quiz_pos)

    # -- Comparison table ----------------------------------------------

    def test_comparison_table_covers_all_four_metrics(self):
        tables = re.findall(r"^\|.+\|$\n(?:^\|.+\|$\n?)+", self.section, re.M)
        metric_tables = [
            t
            for t in tables
            if "Recall@k" in t and "MRR" in t and "MAP" in t and "NDCG" in t
        ]
        self.assertTrue(
            metric_tables,
            "expected a single comparison table listing Recall@k, MRR, "
            "MAP, and NDCG together",
        )
        table = metric_tables[0]
        for header in [
            "What it measures",
            "How it's computed",
            "When to use it",
            "Example threshold",
        ]:
            with self.subTest(header=header):
                self.assertIn(header, table)

    def test_comparison_table_gives_a_numeric_example_threshold_per_metric(self):
        for threshold in [
            "Recall@5 ≥ 0.90",
            "MRR ≥ 0.80",
            "MAP ≥ 0.75",
            "NDCG@10 ≥ 0.85",
        ]:
            with self.subTest(threshold=threshold):
                self.assertIn(threshold, self.section)

    def test_ndcg_formula_mentions_dcg_and_log_discount(self):
        self.assertRegex(
            self.section,
            r"(?i)DCG.{0,120}log2",
            "expected the NDCG row to spell out the log-based rank "
            "discount",
        )

    def test_map_formula_references_average_precision(self):
        self.assertRegex(self.section, r"(?i)Average Precision")

    # -- Decision flowchart ----------------------------------------------

    def test_decision_flowchart_present_and_routes_to_all_four_metrics(self):
        self.assertIn("```mermaid", self.section)
        self.assertIn("flowchart TD", self.section)
        for node in ["RECALL", "MRR", "NDCG", "MAP"]:
            with self.subTest(node=node):
                self.assertIn(node, self.section)

    def test_flowchart_distinguishes_top_k_hit_from_ranking_order(self):
        self.assertRegex(self.section, r"(?i)top k")
        self.assertRegex(self.section, r"(?i)graded")

    def test_has_an_exam_tip_mapping_phrasing_to_metric(self):
        self.assertIn("Exam tip:", self.section)

    # -- Worked example --------------------------------------------------

    def test_worked_example_section_exists(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.text)

    def test_worked_example_has_a_ranked_result_table_with_graded_relevance(self):
        self.assertIn("Graded relevance", self.worked_example)
        self.assertIn("Relevant?", self.worked_example)

    def test_worked_example_computes_all_four_metrics_with_correct_values(self):
        # Recall@5 = 3/4 = 0.75
        self.assertRegex(self.worked_example, r"Recall@5 = 3 . 4 = \*\*0\.75\*\*")
        # MRR (this query) = 1/1 = 1.0
        self.assertIn("1.0", self.worked_example)
        # MAP (Average Precision) = 2.267 / 4 = 0.567
        self.assertIn("0.567", self.worked_example)
        # NDCG@5 = 4.387 / 4.762 = 0.92
        self.assertIn("0.92", self.worked_example)

    def test_worked_example_shows_dcg_and_idcg_intermediate_values(self):
        self.assertIn("DCG@5", self.worked_example)
        self.assertIn("IDCG@5", self.worked_example)

    def test_worked_example_synthesizes_a_takeaway_across_metrics(self):
        self.assertRegex(
            self.worked_example,
            r"(?i)no single metric\s+tells the whole story",
            "expected the worked example to tie its numbers back to the "
            "principle that no single retrieval metric is sufficient "
            "alone",
        )

    def test_is_a_single_self_contained_worked_example_with_no_nested_headings(self):
        nested_headings = re.findall(r"^#{1,6} .+$", self.worked_example, re.M)
        self.assertEqual(
            nested_headings,
            [],
            f"worked example should not contain nested headings: {nested_headings!r}",
        )


if __name__ == "__main__":
    unittest.main()
