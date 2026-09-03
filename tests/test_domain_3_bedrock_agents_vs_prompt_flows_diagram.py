"""Structural validation for the "Bedrock Agents vs. Prompt Flows vs.
prompt chaining: choosing an orchestration approach" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 5 covered Amazon Bedrock Agents in
only a few paragraphs with no visual decision aid, even though Prompt
Flows and manual prompt chaining are both described elsewhere in the same
document (Section 2) as alternative ways to orchestrate multi-step
prompts. There was no single place helping a reader choose between the
three when a scenario doesn't explicitly name the Bedrock feature. These
tests guard the new subsection added to close that gap: it must exist
inside "## 5. Amazon Bedrock features", sit before that section's
mini-quiz, be linked from the table of contents, contain a Mermaid
decision-tree diagram covering all three orchestration approaches, and a
side-by-side comparison table -- without adding any new numbered section
or mini-quiz block (this repo's structural tests assert exact counts for
both).

Mirrors the conventions established in
tests/test_domain_3_cost_governance_subsection.py and
tests/test_domain_3_rag_failure_decision_tree.py.

Run with:
    python3 -m unittest tests/test_domain_3_bedrock_agents_vs_prompt_flows_diagram.py -v
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
    "### Bedrock Agents vs. Prompt Flows vs. prompt chaining: choosing an "
    "orchestration approach"
)
TOC_LINK = (
    "[Bedrock Agents vs. Prompt Flows vs. prompt chaining: choosing an "
    "orchestration approach]"
    "(#bedrock-agents-vs-prompt-flows-vs-prompt-chaining-choosing-an-orchestration-approach)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3BedrockAgentsVsPromptFlowsDiagram(unittest.TestCase):
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

    def test_sits_inside_section_5_before_its_mini_quiz(self):
        section_5 = _section(
            self.text,
            r"\n## 5\. Amazon Bedrock features",
            r"\n## 6\. ",
        )
        heading_pos = section_5.index(HEADING)
        quiz_pos = section_5.index(
            "#### Mini-quiz: Test your understanding of Amazon Bedrock features"
        )
        self.assertLess(heading_pos, quiz_pos)

    def test_sits_before_the_cost_governance_subsection(self):
        section_5 = _section(
            self.text,
            r"\n## 5\. Amazon Bedrock features",
            r"\n## 6\. ",
        )
        heading_pos = section_5.index(HEADING)
        cost_pos = section_5.index(
            "### Cost governance: bounding per-request cost with max tokens "
            "and provisioned throughput"
        )
        self.assertLess(heading_pos, cost_pos)

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

    def test_diagram_covers_all_three_orchestration_approaches(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        diagram = "\n".join(fences)
        for name_regex, label in [
            (r"(?i)bedrock agents", "Amazon Bedrock Agents"),
            (r"(?i)prompt flows", "Amazon Bedrock Prompt Flows"),
            (r"(?i)prompt chaining", "plain prompt chaining"),
        ]:
            with self.subTest(approach=label):
                self.assertRegex(
                    diagram, name_regex, f"diagram missing approach: {label!r}"
                )

    def test_comparison_table_covers_all_three_approaches_and_key_dimensions(self):
        tables = re.findall(r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection)
        self.assertTrue(tables, "expected a Markdown comparison table")
        table = "\n".join(tables)
        for expected in [
            "Amazon Bedrock Agents",
            "Amazon Bedrock Prompt Flows",
            "Plain prompt chaining",
            "Tool / API calling",
            "Exam keywords",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, table)

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-8]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            8,
            "Domain 3 must still have exactly 8 numbered sections",
        )
        section_5 = _section(
            self.text,
            r"\n## 5\. Amazon Bedrock features",
            r"\n## 6\. ",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_5)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 5 must still contain exactly one mini-quiz heading",
        )


if __name__ == "__main__":
    unittest.main()
