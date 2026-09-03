"""Structural validation for the "Worked Example: Selecting a vector
store for a compliance-document Q&A assistant" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: the "Vector store decision guide" subsection (inside
"## 3. Retrieval Augmented Generation (RAG) and Amazon Bedrock Knowledge
Bases") has a comparison table and a decision-tree flowchart for choosing
between Amazon OpenSearch, Aurora PostgreSQL + pgvector, and Amazon
Kendra, plus three short per-service "Worked scenario" blurbs -- but no
single worked example that walks a learner through the whole decision
tree, step by step, for one concrete scenario and lands on an explicit,
justified choice. These tests guard the new subsection added immediately
after the existing comparison table/decision tree/exam-tip content: it
must exist, sit in the right place in reading order, walk through the
three decision-tree questions explicitly, land on an explicit choice, and
justify it with concrete cost/latency/scaling tradeoffs -- including when
Kendra's higher per-query cost is worth paying versus self-managing
OpenSearch or Aurora.

Run with:
    python3 -m unittest tests/test_domain_3_vector_store_worked_example.py -v
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
    "#### Worked Example: Selecting a vector store for a "
    "compliance-document Q&A assistant"
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


class TestDomain3VectorStoreWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_appears_after_the_comparison_table_and_decision_tree(self):
        table_header_pos = self.text.index(
            "| Dimension | Amazon OpenSearch (Service / Serverless) "
            "| Amazon Aurora (PostgreSQL) + pgvector | Amazon Kendra |"
        )
        decision_tree_pos = self.text.index(
            'START(["Choosing a vector store /\\nsearch backend for RAG?"])'
        )
        exam_tip_pos = self.text.index(
            "> **Exam tip:** If a scenario says the team **chooses an "
            "embeddings model**"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(table_header_pos, decision_tree_pos)
        self.assertLess(decision_tree_pos, exam_tip_pos)
        self.assertLess(
            exam_tip_pos,
            heading_pos,
            "worked example should come after the existing comparison "
            "table, decision tree, and exam tip",
        )

    def test_appears_before_section_4(self):
        heading_pos = self.text.index(HEADING)
        section_4_pos = self.text.index(
            "## 4. Fine-tuning vs. continued pre-training vs. RAG vs. "
            "prompt engineering"
        )
        self.assertLess(heading_pos, section_4_pos)

    def test_scenario_is_a_financial_services_compliance_scenario(self):
        self.assertRegex(
            self.section,
            r"(?i)bank|financial",
            "expected a financial-services framing for the scenario",
        )
        self.assertRegex(
            self.section,
            r"(?i)complian",
            "expected the scenario to be about compliance documents",
        )

    def test_walks_through_all_three_decision_tree_questions(self):
        for marker in ["Q1", "Q2", "Q3"]:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.section)
        self.assertRegex(self.section, r"(?i)hybrid search")
        self.assertRegex(self.section, r"(?i)aurora.{0,40}postgresql|postgresql.{0,40}sql")
        self.assertRegex(self.section, r"(?i)fully managed")

    def test_makes_an_explicit_choice(self):
        self.assertRegex(
            self.section,
            r"(?i)choice:\s*\*\*amazon kendra\*\*|\*\*choice:\s*amazon kendra\.?\*\*",
            "expected an explicit, unambiguous choice statement naming "
            "Amazon Kendra",
        )

    def test_justifies_the_choice_with_cost_latency_and_scaling_tradeoffs(self):
        for label in ["Cost:", "Latency:", "Scaling:"]:
            with self.subTest(label=label):
                self.assertIn(label, self.section)

    def test_explains_when_kendras_higher_cost_is_justified_vs_self_managed(self):
        self.assertRegex(
            self.section,
            r"(?i)self-manag",
            "expected explicit discussion of the self-managed alternative",
        )
        self.assertRegex(
            self.section,
            r"(?i)higher.{0,40}(?:per-query|cost)|(?:per-query|cost).{0,40}higher",
            "expected the section to name Kendra's higher per-query cost",
        )
        self.assertRegex(
            self.section,
            r"(?i)would justify|justify the added operational burden|"
            r"better fit for this scenario",
            "expected the section to explain when the self-managed option "
            "would instead be worth the operational burden",
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
