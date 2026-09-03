"""Structural validation for the "Choosing an embedding model" Mermaid
decision-tree diagram added to
docs/domain-2-fundamentals-of-generative-ai.md.

The gap this covers: Domain 2 Section 1 introduces embeddings and
embedding models (as core vocabulary) but never gives students a visual
aid for choosing between a general-purpose, domain-specific, or
fine-tuned embedding model, or for reasoning about the cost/accuracy
trade-offs between them -- even though that comparison matters for
Domain 3's later vector-store/RAG coverage. These tests guard the new
"### Choosing an embedding model" subsection added inside Section 1,
after the embeddings/vectors vocabulary and its worked AWS example: it
must be linked from the table of contents, sit inside Section 1 before
that section's mini-quiz, contain a Mermaid decision tree that walks
through general-purpose sufficiency, domain specialization, and
fine-tuning justification, and annotate cost/latency trade-offs at each
branch -- without disturbing the existing 7-numbered-section /
one-mini-quiz-per-section structure asserted by other Domain 2 tests.

Mirrors the conventions established in
tests/test_domain_3_rag_failure_decision_tree.py and
tests/test_domain_3_embedding_model_selection_diagram.py.

Run with:
    python3 -m unittest tests/test_domain_2_embedding_model_selection_diagram.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-2-fundamentals-of-generative-ai.md"
)

SECTION_1_HEADING = "## 1. Generative AI core concepts"
DIAGRAM_HEADING = "### Choosing an embedding model"
TOC_LINK = "[Choosing an embedding model](#choosing-an-embedding-model)"
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of generative AI core concepts"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    """Return the text between a heading matching start_heading_regex and
    the next top-level (##) heading, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain2EmbeddingModelSelectionDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section_1 = _section(cls.text, r"\n" + re.escape(SECTION_1_HEADING))
        diagram_start = cls.section_1.index(DIAGRAM_HEADING)
        cls.subsection = cls.section_1[diagram_start:]

    def test_diagram_heading_exists(self):
        self.assertIn(DIAGRAM_HEADING, self.text)

    def test_diagram_heading_is_inside_section_1(self):
        self.assertIn(DIAGRAM_HEADING, self.section_1)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_diagram_appears_after_the_embeddings_vocabulary_and_before_the_mini_quiz(
        self,
    ):
        embedding_vocab_pos = self.section_1.index("**Embedding** — a numeric")
        diagram_pos = self.section_1.index(DIAGRAM_HEADING)
        quiz_pos = self.section_1.index(MINI_QUIZ_HEADING)
        self.assertLess(embedding_vocab_pos, diagram_pos)
        self.assertLess(diagram_pos, quiz_pos)

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
            "decision tree should use Mermaid flowchart/graph syntax",
        )
        self.assertIn(
            "?", diagram, "diagram should pose branching decision questions"
        )
        self.diagram = diagram

    def test_diagram_covers_the_three_required_decision_questions(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        diagram = "\n".join(fences)
        for question_regex, label in [
            (
                r"(?i)general-purpose\\nembedding model\\nsufficient",
                "is a general-purpose embedding sufficient",
            ),
            (
                r"(?i)domain\\nspecialized",
                "is the domain specialized",
            ),
            (
                r"(?i)fine-tuning justified",
                "is fine-tuning justified by data volume/accuracy",
            ),
        ]:
            with self.subTest(question=label):
                self.assertRegex(
                    diagram, question_regex, f"diagram missing question: {label!r}"
                )

    def test_diagram_covers_general_domain_specific_and_fine_tuned_branches(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        diagram = "\n".join(fences)
        for name_regex, label in [
            (r"(?i)general-purpose model", "general-purpose branch"),
            (r"(?i)domain-specific\s*\\npretrained embedding model", "domain-specific branch"),
            (r"(?i)fine-tune an embedding model", "fine-tuned branch"),
            (r"(?i)legal, medical,\\nfinancial", "named specialized domains"),
        ]:
            with self.subTest(branch=label):
                self.assertRegex(
                    diagram, name_regex, f"diagram missing branch: {label!r}"
                )

    def test_diagram_annotates_cost_and_latency_at_each_branch(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        diagram = "\n".join(fences)
        cost_count = len(re.findall(r"Cost: \$", diagram))
        latency_count = len(re.findall(r"Latency:", diagram))
        self.assertGreaterEqual(
            cost_count, 4, "expected cost annotations on at least 4 branches"
        )
        self.assertGreaterEqual(
            latency_count, 4, "expected latency annotations on at least 4 branches"
        )
        # Cost should escalate: at least one $, $$, and $$$ tier represented.
        self.assertIn("$", diagram)
        self.assertIn("$$", diagram)
        self.assertIn("$$$", diagram)

    def test_diagram_section_mentions_domain_3_relevance(self):
        self.assertRegex(
            self.subsection,
            r"(?i)Domain 3",
            "subsection should note relevance to Domain 3's vector-store/RAG "
            "coverage",
        )

    def test_domain_2_still_has_exactly_seven_numbered_sections(self):
        numbered_sections = re.findall(r"\n## [1-7]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            7,
            "Domain 2 must still have exactly 7 numbered sections",
        )

    def test_section_1_still_has_exactly_one_mini_quiz_heading(self):
        quiz_headings = re.findall(r"\n#### Mini-quiz:", self.section_1)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 1 must still contain exactly one mini-quiz heading",
        )


if __name__ == "__main__":
    unittest.main()
