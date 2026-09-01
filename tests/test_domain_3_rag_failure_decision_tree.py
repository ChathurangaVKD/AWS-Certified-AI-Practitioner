"""Structural validation for the "Decision tree: diagnosing RAG retrieval
failures" Mermaid diagram added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: the "Worked example: troubleshooting a failing RAG
system" section walks through three specific failure modes (chunking,
embedding mismatch, irrelevant retrieval) for one running scenario, but has
no single visual reference mapping the broader set of RAG retrieval-quality
symptoms -- including hallucination and token-limit overflow, which the
worked example never names -- to their root cause and mitigation. These
tests guard the decision-tree diagram added immediately after that worked
example: it must exist as a Mermaid flowchart, sit adjacent to (inside) the
RAG troubleshooting worked example section, and cover all four named
failure symptoms (hallucination, relevance drift, token-limit overflow,
embedding model mismatch) each paired with a root cause and a fix.

Mirrors the conventions established in
tests/test_domain_3_rag_troubleshooting_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_rag_failure_decision_tree.py -v
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
DIAGRAM_HEADING = "### Decision tree: diagnosing RAG retrieval failures"


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


class TestDomain3RagFailureDecisionTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.worked_example_section = _section(
            cls.text, r"\n" + re.escape(WORKED_EXAMPLE_HEADING)
        )

    def test_diagram_heading_exists(self):
        self.assertIn(DIAGRAM_HEADING, self.text)

    def test_diagram_heading_is_inside_the_rag_troubleshooting_worked_example(self):
        # The diagram is meant to sit adjacent to the existing RAG
        # troubleshooting worked example, so it must live inside that
        # section (before the next top-level "## " heading), not off in
        # some unrelated part of the document.
        self.assertIn(DIAGRAM_HEADING, self.worked_example_section)

    def test_diagram_appears_after_the_symptom_to_fix_summary_table(self):
        summary_pos = self.worked_example_section.index(
            "### Summary: matching the symptom to the fix"
        )
        diagram_pos = self.worked_example_section.index(DIAGRAM_HEADING)
        self.assertLess(summary_pos, diagram_pos)

    def test_diagram_is_a_mermaid_flowchart_with_branching_questions(self):
        section = self.worked_example_section[
            self.worked_example_section.index(DIAGRAM_HEADING):
        ]
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertTrue(
            fences, "expected a ```mermaid fenced code block under the decision-tree heading"
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

    def test_diagram_covers_all_four_named_failure_symptoms(self):
        section = self.worked_example_section[
            self.worked_example_section.index(DIAGRAM_HEADING):
        ]
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        diagram = "\n".join(fences)
        for symptom_regex, label in [
            (r"(?i)hallucinat", "hallucination"),
            (r"(?i)relevance drift|off-topic retrieval", "relevance drift"),
            (r"(?i)token-limit overflow|context-length", "token-limit overflow"),
            (
                r"(?i)embedding model.{0,40}mismatch(?:ed)?|mismatch(?:ed)?"
                r".{0,40}embedding model",
                "embedding model mismatch",
            ),
        ]:
            with self.subTest(symptom=label):
                self.assertRegex(
                    diagram, symptom_regex, f"diagram missing symptom: {label!r}"
                )

    def test_diagram_pairs_each_symptom_with_a_root_cause_and_a_fix(self):
        section = self.worked_example_section[
            self.worked_example_section.index(DIAGRAM_HEADING):
        ]
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        diagram = "\n".join(fences)
        root_cause_count = len(re.findall(r"ROOT CAUSE", diagram))
        fix_count = len(re.findall(r"FIX:", diagram))
        self.assertGreaterEqual(
            root_cause_count, 4, "expected at least 4 root-cause callouts"
        )
        self.assertGreaterEqual(fix_count, 4, "expected at least 4 fix callouts")

    def test_diagram_section_has_an_exam_tip(self):
        section = self.worked_example_section[
            self.worked_example_section.index(DIAGRAM_HEADING):
        ]
        self.assertIn("Exam tip:", section)

    def test_worked_example_still_has_three_failure_mode_subsections(self):
        # The new diagram must not have disturbed the existing three
        # failure-mode subsections it sits alongside.
        headings = re.findall(r"^### (.+)$", self.worked_example_section, re.M)
        failure_headings = [h for h in headings if "failure mode" in h.lower()]
        self.assertEqual(len(failure_headings), 3, f"found headings: {headings!r}")


if __name__ == "__main__":
    unittest.main()
