"""Structural validation for the "Worked example: troubleshooting a
failing RAG system" section added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3, Section 3 (and the existing "implementing
RAG" worked example) only ever describe RAG on the happy path -- a
well-formed system that quietly returns the right chunks. Neither shows a
learner what a *failing* RAG system looks like or how to diagnose which
pipeline stage broke it, even though AIF-C01 scenario questions frequently
describe an already-deployed RAG system that answers badly and ask which
fix applies. These tests guard the dedicated worked example added to close
that gap: it must exist, be linked from the table of contents, cover the
four named failure modes (chunking, embedding mismatch, retrieval
quality, query/document terminology mismatch) each with a diagnosis and a
remediation, name the specific fixes the task calls for (reranking,
hybrid search, embedding-model swap, query rewriting), and carry an exam
tip like every other worked example in this domain guide.

Mirrors the conventions established in
tests/test_domain_3_study_guide.py::TestDomain3MultiConstraintWorkedExample.

Run with:
    python3 -m unittest tests/test_domain_3_rag_troubleshooting_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

HEADING = "## Worked example: troubleshooting a failing RAG system"
HEADING_REGEX = r"\n## Worked example: troubleshooting a failing RAG system"


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


class TestDomain3RagTroubleshootingWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents")
        self.assertIn(
            "[Worked example: troubleshooting a failing RAG system]"
            "(#worked-example-troubleshooting-a-failing-rag-system)",
            toc,
        )

    def test_worked_example_appears_after_the_rag_pipeline_section(self):
        # The troubleshooting example builds on the pipeline concepts from
        # Section 3, so it should be positioned after that section (and
        # after the happy-path RAG worked example) in reading order.
        rag_section_pos = self.text.index(
            "## 3. Retrieval Augmented Generation (RAG) and Amazon Bedrock "
            "Knowledge Bases"
        )
        happy_path_pos = self.text.index(
            "## Worked example: implementing RAG for an internal "
            "policy-lookup assistant"
        )
        troubleshooting_pos = self.text.index(HEADING)
        self.assertLess(rag_section_pos, happy_path_pos)
        self.assertLess(happy_path_pos, troubleshooting_pos)

    def test_covers_chunking_failure_mode_with_diagnosis_and_remediation(self):
        self.assertRegex(
            self.section,
            r"(?i)chunk(?:s|ing)? too small",
            "expected a failure mode about chunks too small to answer a query",
        )
        self.assertIn("**Diagnosis.**", self.section)
        self.assertIn("**Remediation.**", self.section)
        self.assertRegex(
            self.section,
            r"(?i)chunk (?:size|overlap)",
            "chunking remediation should mention adjusting chunk size/overlap",
        )

    def test_covers_embedding_mismatch_failure_mode_with_remediation(self):
        self.assertRegex(
            self.section,
            r"(?i)embedding model.{0,40}mismatch|mismatch.{0,40}embedding "
            r"model|embeddings model.{0,60}domain",
            "expected a failure mode about an embedding model mismatched "
            "to the domain",
        )
        self.assertRegex(
            self.section,
            r"(?i)swap.{0,60}embeddings? model|re-embed",
            "expected remediation to mention swapping the embeddings "
            "model and re-embedding the corpus",
        )

    def test_covers_irrelevant_retrieval_failure_mode(self):
        self.assertRegex(
            self.section,
            r"(?i)irrelevant|not necessarily the.{0,10}correct",
            "expected a failure mode about retrieval returning irrelevant "
            "or merely-similar results",
        )

    def test_names_reranking_and_hybrid_search_as_remediations(self):
        for term in ["Reranking", "Hybrid search"]:
            with self.subTest(term=term):
                self.assertIn(
                    term,
                    self.section,
                    f"worked example should name {term!r} as a remediation",
                )

    def test_covers_query_document_terminology_mismatch_failure_mode(self):
        self.assertRegex(
            self.section,
            r"(?i)terminology mismatch",
            "expected a fourth failure mode about query/document "
            "terminology mismatch",
        )
        self.assertRegex(
            self.section,
            r"(?i)bi-encoder|question-vs-statement|question.{0,15}statement",
            "expected the diagnosis to explain the query-vs-document "
            "phrasing asymmetry",
        )

    def test_names_reranking_query_rewriting_and_hyde_for_terminology_mismatch(self):
        for term in ["HyDE", "Query rewriting", "cross-encoder"]:
            with self.subTest(term=term):
                self.assertIn(
                    term,
                    self.section,
                    f"worked example should name {term!r} as a remediation "
                    "for the terminology-mismatch failure mode",
                )

    def test_has_four_distinct_failure_mode_subsections(self):
        headings = re.findall(r"^### (.+)$", self.section, re.M)
        failure_headings = [h for h in headings if "failure mode" in h.lower()]
        self.assertEqual(
            len(failure_headings),
            4,
            f"expected exactly 4 failure-mode subsections, found {headings!r}",
        )

    def test_every_failure_mode_has_symptom_diagnosis_and_remediation(self):
        failure_blocks = re.split(r"\n(?=### )", self.section.strip())
        failure_blocks = [
            b
            for b in failure_blocks
            if b.startswith("### ") and "failure mode" in b.splitlines()[0].lower()
        ]
        self.assertEqual(len(failure_blocks), 4)
        for block in failure_blocks:
            heading = block.splitlines()[0]
            with self.subTest(section=heading):
                self.assertIn("**Symptom:**", block)
                self.assertIn("**Diagnosis.**", block)
                self.assertIn("**Remediation.**", block)

    def test_has_a_symptom_to_fix_summary_table(self):
        self.assertIn("### Summary: matching the symptom to the fix", self.section)
        table = self.section[
            self.section.index("### Summary: matching the symptom to the fix"):
        ]
        self.assertRegex(table, r"\|\s*-{2,}\s*\|")
        for column in ["Symptom", "Root cause", "Fix"]:
            with self.subTest(column=column):
                self.assertIn(column, table)

    def test_worked_example_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.section)

    def test_worked_example_cross_references_the_rag_section(self):
        self.assertIn(
            "#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases",
            self.section,
        )


if __name__ == "__main__":
    unittest.main()
