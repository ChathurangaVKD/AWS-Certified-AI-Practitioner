"""Structural validation for the "Orientation: a first-pass triage
flowchart" Mermaid diagram added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: the "Worked example: troubleshooting a failing RAG
system" section (four failure-mode subsections, a symptom-to-fix summary
table, and two deeper Mermaid diagrams) walked a learner through five
diagnostic branches -- no relevant passages retrieved, irrelevant passages
retrieved, and poor generation despite good retrieval -- entirely in prose
before the reader ever reaches a visual. There was no standalone diagram at
the *start* of the section giving a quick, high-level map of where to look
first. These tests guard the triage flowchart added immediately after the
scenario intro and before the first failure-mode subsection: it must exist
as a Mermaid flowchart, sit at the very start of the RAG troubleshooting
worked example (before any "### Failure mode" subsection), and cover the
three coarse branches -- no relevant passages (chunking, embedding model,
vector index quality), irrelevant passages (ranking algorithm), and poor
generation despite good retrieval (model capability/temperature/prompt
engineering) -- without disturbing the existing prose sections beneath it.

Mirrors the conventions established in
tests/test_domain_3_rag_failure_decision_tree.py and
tests/test_domain_3_rag_pipeline_stage_isolation_flowchart.py.

Run with:
    python3 -m unittest tests/test_domain_3_rag_troubleshooting_triage_flowchart.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

WORKED_EXAMPLE_HEADING = "## Worked example: troubleshooting a failing RAG system"
TRIAGE_HEADING = "### Orientation: a first-pass triage flowchart"
FAILURE_MODE_1_HEADING = "### Failure mode 1: chunks too small to answer the query"


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


class TestDomain3RagTroubleshootingTriageFlowchart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.worked_example_section = _section(
            cls.text, r"\n" + re.escape(WORKED_EXAMPLE_HEADING)
        )
        triage_start = cls.worked_example_section.index(TRIAGE_HEADING)
        failure_mode_1_start = cls.worked_example_section.index(
            FAILURE_MODE_1_HEADING
        )
        cls.triage_section = cls.worked_example_section[
            triage_start:failure_mode_1_start
        ]

    def test_heading_exists(self):
        self.assertIn(TRIAGE_HEADING, self.text)

    def test_heading_is_inside_the_rag_troubleshooting_worked_example(self):
        self.assertIn(TRIAGE_HEADING, self.worked_example_section)

    def test_appears_before_the_first_failure_mode_subsection(self):
        triage_pos = self.worked_example_section.index(TRIAGE_HEADING)
        failure_mode_1_pos = self.worked_example_section.index(
            FAILURE_MODE_1_HEADING
        )
        self.assertLess(triage_pos, failure_mode_1_pos)

    def test_appears_early_in_the_worked_example_before_any_failure_mode(self):
        # This is meant to be a standalone orientation diagram at the top
        # of the section, not tucked in after the detailed failure modes.
        headings = re.findall(r"^### (.+)$", self.worked_example_section, re.M)
        self.assertTrue(headings, "expected at least one ### heading")
        self.assertEqual(headings[0], TRIAGE_HEADING[4:])

    def test_is_a_mermaid_flowchart_with_branching_questions(self):
        fences = re.findall(r"```mermaid(.*?)```", self.triage_section, re.S)
        self.assertTrue(
            fences,
            "expected a ```mermaid fenced code block under the triage "
            "heading",
        )
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "triage diagram should use Mermaid flowchart/graph syntax",
        )
        self.assertIn(
            "?", diagram, "diagram should pose branching decision questions"
        )
        self.diagram = diagram

    def test_diagram_covers_the_no_relevant_passages_branch(self):
        fences = re.findall(r"```mermaid(.*?)```", self.triage_section, re.S)
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"(?i)returning no.{0,30}relevant passages",
            "expected a branch for retrieval returning no relevant "
            "passages",
        )
        for term in ["chunking", "embedding model", "vector index"]:
            with self.subTest(term=term):
                self.assertRegex(
                    diagram,
                    rf"(?i){re.escape(term)}",
                    f"expected the no-relevant-passages branch to check "
                    f"{term!r}",
                )

    def test_diagram_covers_the_irrelevant_passages_branch(self):
        fences = re.findall(r"```mermaid(.*?)```", self.triage_section, re.S)
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"(?i)irrelevant",
            "expected a branch for retrieval returning irrelevant "
            "passages",
        )
        self.assertRegex(
            diagram,
            r"(?i)ranking algorithm|rerank",
            "expected the irrelevant-passages branch to check the "
            "ranking algorithm",
        )

    def test_diagram_covers_the_poor_generation_branch(self):
        fences = re.findall(r"```mermaid(.*?)```", self.triage_section, re.S)
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"(?i)generation.{0,30}(?:is still poor|poor)",
            "expected a branch for poor generation despite good "
            "retrieval",
        )
        for term in ["model capability", "temperature", "prompt engineering"]:
            with self.subTest(term=term):
                self.assertRegex(
                    diagram,
                    rf"(?i){re.escape(term)}",
                    f"expected the poor-generation branch to check "
                    f"{term!r}",
                )

    def test_existing_prose_failure_modes_are_undisturbed(self):
        # The new diagram is additive: the four detailed failure-mode
        # subsections must still exist, unchanged in count, beneath it.
        headings = re.findall(r"^### (.+)$", self.worked_example_section, re.M)
        failure_headings = [h for h in headings if "failure mode" in h.lower()]
        self.assertEqual(len(failure_headings), 4, f"found headings: {headings!r}")

    def test_worked_example_section_still_has_its_summary_table(self):
        self.assertIn(
            "### Summary: matching the symptom to the fix",
            self.worked_example_section,
        )


if __name__ == "__main__":
    unittest.main()
