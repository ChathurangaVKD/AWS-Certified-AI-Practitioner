"""Structural validation for the "Debugging method: isolating the broken
pipeline stage" section added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: the existing "Decision tree: diagnosing RAG retrieval
failures" maps a *symptom* straight to a root cause, but never gives a
learner a systematic *procedure* for narrowing down which of the four RAG
pipeline stages -- embedding, retrieval, ranking, or generation -- is
actually at fault when a query fails, the way a real on-call debugging
session (or an exam scenario) requires. These tests guard the dedicated
stage-isolation flowchart added right after the existing decision tree: it
must exist, sit inside the RAG troubleshooting worked example, name all
four pipeline stages with an ordered checklist, provide a Mermaid
flowchart that isolates each stage in turn, and carry an exam tip.

Mirrors the conventions established in
tests/test_domain_3_rag_failure_decision_tree.py.

Run with:
    python3 -m unittest tests/test_domain_3_rag_pipeline_stage_isolation_flowchart.py -v
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
DECISION_TREE_HEADING = "### Decision tree: diagnosing RAG retrieval failures"
STAGE_HEADING = "### Debugging method: isolating the broken pipeline stage"


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


class TestDomain3RagPipelineStageIsolationFlowchart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.worked_example_section = _section(
            cls.text, r"\n" + re.escape(WORKED_EXAMPLE_HEADING)
        )
        stage_start = cls.worked_example_section.index(STAGE_HEADING)
        cls.stage_section = cls.worked_example_section[stage_start:]

    def test_heading_exists(self):
        self.assertIn(STAGE_HEADING, self.text)

    def test_heading_is_inside_the_rag_troubleshooting_worked_example(self):
        self.assertIn(STAGE_HEADING, self.worked_example_section)

    def test_appears_after_the_existing_decision_tree(self):
        decision_tree_pos = self.worked_example_section.index(DECISION_TREE_HEADING)
        stage_pos = self.worked_example_section.index(STAGE_HEADING)
        self.assertLess(decision_tree_pos, stage_pos)

    def test_names_all_four_pipeline_stages(self):
        for stage in ["embedding", "retrieval", "ranking", "generation"]:
            with self.subTest(stage=stage):
                self.assertRegex(
                    self.stage_section,
                    rf"(?i)\*\*{stage}\b",
                    f"expected the ordered checklist to bold-name the "
                    f"{stage!r} stage",
                )

    def test_has_an_ordered_checklist_of_four_steps(self):
        steps = re.findall(r"^\d+\. \*\*Check the", self.stage_section, re.M)
        self.assertEqual(
            len(steps),
            4,
            f"expected 4 numbered 'Check the ... stage' steps, found {len(steps)}",
        )

    def test_is_a_mermaid_flowchart_with_branching_questions(self):
        fences = re.findall(r"```mermaid(.*?)```", self.stage_section, re.S)
        self.assertTrue(
            fences,
            "expected a ```mermaid fenced code block under the "
            "stage-isolation heading",
        )
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "stage-isolation diagram should use Mermaid flowchart/graph "
            "syntax",
        )
        self.assertIn("?", diagram, "diagram should pose branching decision questions")
        self.diagram = diagram

    def test_flowchart_labels_each_of_the_four_stages(self):
        fences = re.findall(r"```mermaid(.*?)```", self.stage_section, re.S)
        diagram = "\n".join(fences)
        for stage_label in [
            "STAGE: embedding",
            "STAGE: embedding / retrieval",
            "STAGE: ranking",
            "STAGE: generation",
        ]:
            with self.subTest(stage_label=stage_label):
                self.assertIn(
                    stage_label,
                    diagram,
                    f"expected the flowchart to label a node {stage_label!r}",
                )

    def test_flowchart_pairs_stages_with_root_cause_and_fix(self):
        fences = re.findall(r"```mermaid(.*?)```", self.stage_section, re.S)
        diagram = "\n".join(fences)
        root_cause_count = len(re.findall(r"ROOT CAUSE", diagram))
        fix_count = len(re.findall(r"FIX:", diagram))
        self.assertGreaterEqual(
            root_cause_count, 4, "expected at least 4 root-cause callouts"
        )
        self.assertGreaterEqual(fix_count, 4, "expected at least 4 fix callouts")

    def test_flowchart_names_reranking_as_the_ranking_stage_fix(self):
        self.assertRegex(
            self.stage_section,
            r"(?i)rerank",
            "expected reranking to be named as the standard fix for a "
            "ranking-stage failure",
        )

    def test_section_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.stage_section)

    def test_worked_example_still_has_four_failure_mode_subsections(self):
        # The new stage-isolation flowchart must not have disturbed the
        # four failure-mode subsections it sits alongside.
        headings = re.findall(r"^### (.+)$", self.worked_example_section, re.M)
        failure_headings = [h for h in headings if "failure mode" in h.lower()]
        self.assertEqual(len(failure_headings), 4, f"found headings: {headings!r}")


if __name__ == "__main__":
    unittest.main()
