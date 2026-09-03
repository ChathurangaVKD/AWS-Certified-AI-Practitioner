"""Structural validation for the "Reranking and hybrid search: sharpening
vector-only results" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 6 explained vector databases and
embeddings, and how to choose a vector store, but never explained
**reranking** (re-scoring retrieved candidates with a separate model) or
**hybrid search** (fusing vector and keyword search) -- both flagged by
the documentation scan as a missing diagram and a structural gap. These
tests guard the new subsection added to close that gap: it must exist
inside "## 6. Vector databases and embeddings for search and retrieval",
sit before that section's mini-quiz, be linked from the table of
contents, contain a Mermaid decision diagram covering reranking, hybrid
search, and the "plain vector search is enough" fallback, a comparison
table covering reranking vs. hybrid search, and mention how Amazon
Bedrock Knowledge Bases relates to both -- without adding any new
numbered section or mini-quiz block (this repo's structural tests assert
exact counts for both).

Mirrors the conventions established in
tests/test_domain_3_bedrock_agents_vs_prompt_flows_diagram.py and
tests/test_domain_3_rag_failure_decision_tree.py.

Run with:
    python3 -m unittest tests/test_domain_3_reranking_hybrid_search_diagram.py -v
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
    "### Reranking and hybrid search: sharpening vector-only results"
)
TOC_LINK = (
    "[Reranking and hybrid search: sharpening vector-only results]"
    "(#reranking-and-hybrid-search-sharpening-vector-only-results)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3RerankingHybridSearchDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.subsection = _section(
            cls.text,
            re.escape(HEADING),
            r"\n#{1,3} ",
        )

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_sits_inside_section_6_before_its_mini_quiz(self):
        section_6 = _section(
            self.text,
            r"\n## 6\. Vector databases and embeddings for search and "
            r"retrieval",
            r"\n## 7\. ",
        )
        heading_pos = section_6.index(HEADING)
        quiz_pos = section_6.index(
            "#### Mini-quiz: Test your understanding of vector databases "
            "and embeddings"
        )
        self.assertLess(heading_pos, quiz_pos)

    def test_diagram_is_a_mermaid_flowchart_with_branching_questions(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        self.assertTrue(
            fences,
            "expected a ```mermaid fenced code block under the new heading",
        )
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "decision diagram should use Mermaid flowchart/graph syntax",
        )
        self.assertIn(
            "?", diagram, "diagram should pose branching decision questions"
        )
        self.diagram = diagram

    def test_diagram_covers_reranking_hybrid_search_and_plain_vector_fallback(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        diagram = "\n".join(fences)
        for name_regex, label in [
            (r"(?i)rerank", "reranking"),
            (r"(?i)hybrid search", "hybrid search"),
            (r"(?i)plain vector search", "plain vector search fallback"),
        ]:
            with self.subTest(branch=label):
                self.assertRegex(
                    diagram, name_regex, f"diagram missing branch: {label!r}"
                )

    def test_comparison_table_covers_reranking_and_hybrid_search(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection
        )
        self.assertTrue(tables, "expected a Markdown comparison table")
        table = "\n".join(tables)
        for expected in [
            "Reranking",
            "Hybrid",
            "When it's essential",
            "Bedrock Knowledge Bases",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, table)

    def test_explains_how_bedrock_knowledge_bases_relates(self):
        self.assertRegex(
            self.subsection,
            r"(?i)Amazon Bedrock Knowledge Bases",
            "subsection should explain how Bedrock Knowledge Bases relates "
            "to reranking and hybrid search",
        )

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-8]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            8,
            "Domain 3 must still have exactly 8 numbered sections",
        )
        section_6 = _section(
            self.text,
            r"\n## 6\. Vector databases and embeddings for search and "
            r"retrieval",
            r"\n## 7\. ",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_6)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 6 must still contain exactly one mini-quiz heading",
        )


if __name__ == "__main__":
    unittest.main()
