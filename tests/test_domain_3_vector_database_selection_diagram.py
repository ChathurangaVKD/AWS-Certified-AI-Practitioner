"""Structural validation for the vector database / search backend
decision-tree diagram in "## 6. Vector databases and embeddings for search
and retrieval" of docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Section 6 explains the tradeoffs between Amazon
Aurora/RDS PostgreSQL + pgvector, Amazon OpenSearch Service/Serverless, and
Amazon Kendra entirely in prose -- unlike the adjacent "Choosing an
embedding model" subsection, which pairs its comparison guidance with a
Mermaid decision tree. Two practice questions (Q14, Q15) directly test
vector database selection, so the section needs the same kind of visual
decision aid the rest of the domain guide uses. These tests guard the
Mermaid flowchart living directly under "## 6." (before the "Choosing an
embedding model" subsection): it must pose branching yes/no questions,
cover all four backend options (Aurora + pgvector, RDS + pgvector,
OpenSearch, Kendra), sit before both the embedding-model subsection and the
section's mini-quiz, and be followed by an exam tip -- without adding any
new numbered section or mini-quiz block (this repo's structural tests
assert exact counts for both).

Mirrors the conventions established in
tests/test_domain_3_embedding_model_selection_diagram.py and
tests/test_domain_3_reranking_hybrid_search_diagram.py.

Run with:
    python3 -m unittest tests/test_domain_3_vector_database_selection_diagram.py -v
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
    "## 6. Vector databases and embeddings for search and retrieval"
)
DECISION_TREE_LEAD_IN = (
    "**Decision tree: choosing a vector database or search backend.**"
)
EMBEDDING_MODEL_HEADING = (
    "### Choosing an embedding model: domain-specific vs. general vs. "
    "fine-tuned"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3VectorDatabaseSelectionDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section_6 = _section(
            cls.text,
            r"\n" + re.escape(SECTION_HEADING),
            r"\n## 7\. ",
        )
        cls.subsection = _section(
            cls.section_6,
            re.escape(DECISION_TREE_LEAD_IN),
            re.escape(EMBEDDING_MODEL_HEADING),
        )
        fences = re.findall(r"```mermaid(.*?)```", cls.subsection, re.S)
        cls.diagram = "\n".join(fences)

    def test_decision_tree_lead_in_exists(self):
        self.assertIn(DECISION_TREE_LEAD_IN, self.text)

    def test_sits_inside_section_6_before_embedding_model_subsection_and_quiz(self):
        section_6_pos = self.text.index(SECTION_HEADING)
        lead_in_pos = self.text.index(DECISION_TREE_LEAD_IN)
        embedding_heading_pos = self.text.index(EMBEDDING_MODEL_HEADING)
        quiz_pos = self.text.index(
            "#### Mini-quiz: Test your understanding of vector databases "
            "and embeddings"
        )
        self.assertLess(section_6_pos, lead_in_pos)
        self.assertLess(lead_in_pos, embedding_heading_pos)
        self.assertLess(embedding_heading_pos, quiz_pos)

    def test_diagram_is_a_mermaid_flowchart_with_branching_questions(self):
        self.assertTrue(
            self.diagram,
            "expected a ```mermaid fenced code block after the decision "
            "tree lead-in",
        )
        self.assertRegex(
            self.diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "decision diagram should use Mermaid flowchart/graph syntax",
        )
        self.assertIn(
            "?", self.diagram, "diagram should pose branching decision questions"
        )

    def test_diagram_covers_aurora_rds_opensearch_and_kendra_branches(self):
        for name_regex, label in [
            (r"(?i)aurora.{0,30}pgvector", "Aurora + pgvector branch"),
            (r"(?i)rds for postgresql.{0,30}pgvector", "RDS + pgvector branch"),
            (r"(?i)opensearch", "OpenSearch branch"),
            (r"(?i)kendra", "Kendra branch"),
        ]:
            with self.subTest(branch=label):
                self.assertRegex(
                    self.diagram, name_regex, f"diagram missing branch: {label!r}"
                )

    def test_diagram_branches_on_existing_rds_usage_and_hybrid_search_need(self):
        self.assertRegex(
            self.diagram,
            r"(?is)RDS or Aurora.{0,60}ALREADY exist",
            "diagram should branch on whether RDS/Aurora infrastructure "
            "already exists",
        )
        self.assertRegex(
            self.diagram,
            r"(?i)hybrid",
            "diagram should branch on the need for hybrid "
            "(vector + keyword) search",
        )
        self.assertRegex(
            self.diagram,
            r"(?is)no embeddings.{0,20}pipeline to build",
            "diagram should branch on wanting a fully-managed option with "
            "no embeddings pipeline to build (the Kendra path)",
        )

    def test_has_an_exam_tip_after_the_diagram(self):
        diagram_end = self.subsection.index("```mermaid")
        after_diagram = self.subsection[diagram_end:]
        self.assertIn("Exam tip:", after_diagram)

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-8]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            8,
            "Domain 3 must still have exactly 8 numbered sections",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", self.section_6)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 6 must still contain exactly one mini-quiz heading",
        )


if __name__ == "__main__":
    unittest.main()
