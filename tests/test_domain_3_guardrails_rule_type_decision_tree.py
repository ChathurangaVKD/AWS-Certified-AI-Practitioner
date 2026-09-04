"""Structural validation for the "Guardrails rule-type decision tree:
matching the use case to the right filter" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 5 listed Guardrails for Amazon
Bedrock's five rule types (denied topics, content filters, word filters,
sensitive information filters, contextual grounding checks) as a flat
bullet list, but never explained *which* rule type is the efficient
choice for a given use case (PII prevention, brand safety, topic
restriction, factual grounding), nor worked through a concrete example.
These tests guard the new subsection added to close that gap: it must
exist inside "## 5. Amazon Bedrock features", sit before that section's
mini-quiz and before the pre-existing "Bedrock Agents vs. Prompt Flows"
subsection, be linked from the table of contents, contain a Mermaid
decision-tree diagram covering all five rule types, a mapping table
covering the four named use cases, and a worked example for the
brand-safety use case -- without adding any new numbered section or
mini-quiz block (this repo's structural tests assert exact counts for
both).

Mirrors the conventions established in
tests/test_domain_3_bedrock_agents_vs_prompt_flows_diagram.py and
tests/test_domain_3_cost_governance_subsection.py.

Run with:
    python3 -m unittest tests/test_domain_3_guardrails_rule_type_decision_tree.py -v
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
    "### Guardrails rule-type decision tree: matching the use case to the "
    "right filter"
)
TOC_LINK = (
    "[Guardrails rule-type decision tree: matching the use case to the "
    "right filter]"
    "(#guardrails-rule-type-decision-tree-matching-the-use-case-to-the-right-filter)"
)
WORKED_EXAMPLE_HEADING = (
    "#### Worked example: preventing brand-mention violations in product "
    "recommendations"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3GuardrailsRuleTypeDecisionTree(unittest.TestCase):
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

    def test_sits_before_the_agents_vs_prompt_flows_subsection(self):
        section_5 = _section(
            self.text,
            r"\n## 5\. Amazon Bedrock features",
            r"\n## 6\. ",
        )
        heading_pos = section_5.index(HEADING)
        agents_pos = section_5.index(
            "### Bedrock Agents vs. Prompt Flows vs. prompt chaining: "
            "choosing an orchestration approach"
        )
        self.assertLess(heading_pos, agents_pos)

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

    def test_diagram_covers_all_five_guardrails_rule_types(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        diagram = "\n".join(fences)
        for name_regex, label in [
            (r"(?i)sensitive information filters", "sensitive information filters"),
            (r"(?i)word filters", "word filters"),
            (r"(?i)denied topics", "denied topics"),
            (r"(?i)content filters", "content filters"),
            (r"(?i)contextual grounding checks", "contextual grounding checks"),
        ]:
            with self.subTest(rule_type=label):
                self.assertRegex(
                    diagram, name_regex, f"diagram missing rule type: {label!r}"
                )

    def test_mapping_table_covers_the_four_named_use_cases(self):
        tables = re.findall(r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection)
        self.assertTrue(tables, "expected a Markdown mapping table")
        table = "\n".join(tables)
        for expected in [
            "PII prevention",
            "Brand safety",
            "Topic restriction",
            "Factual grounding",
            "Sensitive information filters",
            "Word filters",
            "Denied topics",
            "Contextual grounding checks",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, table)

    def test_has_a_worked_example_for_the_brand_safety_use_case(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.subsection)
        worked_example = _section(
            self.subsection,
            re.escape(WORKED_EXAMPLE_HEADING),
            r"\n#{1,4} ",
        )
        for expected in ["word filter", "competitor", "block"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, worked_example)

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
