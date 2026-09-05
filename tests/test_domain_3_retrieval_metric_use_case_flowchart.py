"""Structural validation for the use-case-first retrieval metric decision
flowchart added to the "Retrieval quality metrics: NDCG, MAP, Recall@k,
and MRR" subsection of docs/domain-3-applications-of-foundation-models.md.

The gap this covers: the subsection's existing decision flowchart routes
from the *phrasing* of a requirement (binary vs. graded relevance, one
correct answer vs. many) to a metric, but Domain 3 had no diagram that
starts from a named RAG *use case* (legal e-discovery, search ranking,
open-domain QA, support-ticket lookup) -- the way exam scenarios and real
system descriptions are just as often framed -- and routes that straight
to a recommended metric. This new flowchart is a second, complementary
lookup that also cross-references the domain's existing RAG
troubleshooting decision tree.

Mirrors the conventions established in
tests/test_domain_3_retrieval_quality_metrics_decision_guide.py.

Run with:
    python3 -m unittest tests/test_domain_3_retrieval_metric_use_case_flowchart.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

SECTION_HEADING = (
    "### Retrieval quality metrics: NDCG, MAP, Recall@k, and MRR "
    "(a selection decision guide)"
)

LEAD_IN = "**Decision flowchart: which metric fits this RAG use case?**"

WORKED_EXAMPLE_HEADING = (
    "#### Worked example: computing Recall@k, MRR, MAP, and NDCG on a "
    "sample retrieval result set"
)

RAG_TROUBLESHOOTING_HEADING = "### Decision tree: diagnosing RAG retrieval failures"


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


class TestDomain3RetrievalMetricUseCaseFlowchart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        # Isolate the new use-case flowchart: it sits between the lead-in
        # sentence and the worked-example heading that follows it.
        start = cls.text.index(LEAD_IN)
        end = cls.text.index(WORKED_EXAMPLE_HEADING)
        assert start < end, "lead-in must appear before the worked example"
        cls.block = cls.text[start:end]

    # -- Placement ---------------------------------------------------

    def test_lead_in_exists(self):
        self.assertIn(LEAD_IN, self.text)

    def test_appears_inside_the_retrieval_quality_metrics_subsection(self):
        section_pos = self.text.index(SECTION_HEADING)
        lead_in_pos = self.text.index(LEAD_IN)
        worked_example_pos = self.text.index(WORKED_EXAMPLE_HEADING)
        self.assertLess(section_pos, lead_in_pos)
        self.assertLess(lead_in_pos, worked_example_pos)

    def test_appears_after_the_existing_requirement_phrasing_flowchart(self):
        existing_flowchart_heading = (
            "**Decision flowchart: which retrieval metric fits this "
            "requirement?**"
        )
        existing_pos = self.text.index(existing_flowchart_heading)
        lead_in_pos = self.text.index(LEAD_IN)
        self.assertLess(existing_pos, lead_in_pos)

    def test_cross_references_the_rag_troubleshooting_decision_tree(self):
        self.assertIn(RAG_TROUBLESHOOTING_HEADING, self.text)
        self.assertIn(
            "#decision-tree-diagnosing-rag-retrieval-failures", self.block
        )

    # -- Flowchart content ---------------------------------------------

    def test_flowchart_present_and_is_a_mermaid_flowchart(self):
        self.assertIn("```mermaid", self.block)
        self.assertIn("flowchart TD", self.block)

    def test_flowchart_routes_to_all_four_metrics(self):
        for node in ["MAP", "NDCG", "MRR", "RECALL"]:
            with self.subTest(node=node):
                self.assertIn(node, self.block)

    def test_flowchart_names_the_expected_use_case_archetypes(self):
        for phrase in [
            "e-discovery",
            "search ranking",
            "Open-domain QA",
            "Support-ticket",
        ]:
            with self.subTest(phrase=phrase):
                self.assertRegex(
                    self.block, re.escape(phrase).replace(r"\-", "[- ]")
                )

    def test_flowchart_gives_a_numeric_threshold_per_metric(self):
        for threshold in [
            "MAP >= 0.75",
            "NDCG@10 >= 0.85",
            "MRR >= 0.80",
            "Recall@5 >= 0.90",
        ]:
            with self.subTest(threshold=threshold):
                self.assertIn(threshold, self.block)

    def test_flowchart_has_a_fallback_branch_to_the_requirement_flowchart(self):
        self.assertRegex(self.block, r"(?i)fall back")

    def test_flowchart_is_well_formed_mermaid(self):
        fence_start = self.block.index("```mermaid")
        fence_end = self.block.index("```", fence_start + len("```mermaid"))
        body = self.block[fence_start:fence_end]
        self.assertEqual(body.count("["), body.count("]"))
        self.assertEqual(body.count("{"), body.count("}"))
        self.assertEqual(body.count("("), body.count(")"))

    # -- Exam tip ---------------------------------------------------

    def test_has_an_exam_tip_mapping_use_case_to_metric(self):
        exam_tip_pos = self.block.index("Exam tip:")
        self.assertGreater(exam_tip_pos, 0)
        exam_tip_text = self.block[exam_tip_pos:]
        for metric in ["MAP", "NDCG", "MRR", "Recall@k"]:
            with self.subTest(metric=metric):
                self.assertIn(metric, exam_tip_text)


if __name__ == "__main__":
    unittest.main()
