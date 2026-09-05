"""Structural validation for the "Multi-model routing and fallback
strategies" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3's Section 1 ("Design considerations for
foundation model applications") teaches how to select a *single* foundation
model for an application, but had no content on routing different requests
within the same application to different models based on cost/accuracy/
latency trade-offs, or on building a fallback chain for when a preferred
model times out or fails. This test guards the new subsection added to
close that gap: it must exist nested inside Section 1 (before the
section's mini-quiz), contain a Mermaid decision flowchart for when
multi-model routing is worth the complexity, a comparison table of routing
strategies (strict routing / best-effort routing / fallback chains), a
worked example routing requests by latency sensitivity, and an
implementation-patterns subsection covering Bedrock Agents and SageMaker
multi-model endpoints.

Mirrors the conventions established in
tests/test_domain_3_model_pair_comparison_worked_example.py and
tests/test_domain_3_guardrails_rule_type_decision_tree.py.

Run with:
    python3 -m unittest tests/test_domain_3_multi_model_routing_worked_example.py -v
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
    "### Multi-model routing and fallback strategies: routing requests to "
    "the right model at request time"
)
FLOWCHART_HEADING = (
    "#### Decision flowchart: is multi-model routing worth the added "
    "complexity?"
)
WORKED_EXAMPLE_HEADING = (
    "#### Worked example: routing a dashboard-and-batch analytics feature "
    "by latency sensitivity"
)
IMPLEMENTATION_HEADING = (
    "#### Implementation patterns: Bedrock Agents and SageMaker "
    "multi-model endpoints"
)
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of FM application design "
    "considerations"
)
TOC_LINK = (
    "[Multi-model routing and fallback strategies: routing requests to "
    "the right model at request time]"
    "(#multi-model-routing-and-fallback-strategies-routing-requests-to-the-"
    "right-model-at-request-time)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,4} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading of the same or higher level, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3MultiModelRoutingWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(
            cls.text,
            r"\n### Multi-model routing and fallback strategies: routing "
            r"requests to the right model at request time",
            r"\n#### Mini-quiz: Test your understanding of FM application "
            r"design considerations",
        )

    def test_section_heading_exists(self):
        self.assertIn(SECTION_HEADING, self.text)

    def test_section_is_nested_inside_section_1_before_its_mini_quiz(self):
        section_1_pos = self.text.index(
            "## 1. Design considerations for foundation model applications"
        )
        heading_pos = self.text.index(SECTION_HEADING)
        mini_quiz_pos = self.text.index(MINI_QUIZ_HEADING)
        section_2_pos = self.text.index("## 2. Prompt engineering techniques")
        self.assertLess(section_1_pos, heading_pos)
        self.assertLess(heading_pos, mini_quiz_pos)
        self.assertLess(mini_quiz_pos, section_2_pos)

    def test_toc_links_to_the_new_subsection(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_does_not_change_the_standalone_worked_example_count(self):
        # This subsection's worked example is a level-4 "####" heading
        # nested inside Section 1, not a new standalone "## Worked example"
        # section or a new "### Worked example" subsection, so it must
        # leave the pre-existing counts of those exactly as they were
        # before this subsection was added (8 standalone "##" worked
        # examples, 3 "###"-level ones in Section 7, unaffected by this
        # change).
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 8)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 3)

    def test_has_a_mermaid_decision_flowchart(self):
        self.assertIn(FLOWCHART_HEADING, self.section)
        fences = re.findall(r"```mermaid(.*?)```", self.section, re.S)
        self.assertTrue(fences, "expected a Mermaid flowchart in the section")
        flowchart = "\n".join(fences)
        self.assertRegex(flowchart, r"flowchart\s+\w+|graph\s+\w+")
        for outcome in ["SINGLE MODEL", "STRICT ROUTING", "FALLBACK CHAIN", "BEST-EFFORT ROUTING"]:
            with self.subTest(outcome=outcome):
                self.assertIn(outcome, flowchart)
        self.assertIn("?", flowchart, "flowchart should pose branching decision questions")

    def test_flowchart_is_followed_by_a_routing_strategy_comparison_table(self):
        table_text = self.section[self.section.index(FLOWCHART_HEADING):]
        self.assertRegex(table_text, r"\|\s*-{2,}\s*\|")
        for strategy in ["Strict routing", "Best-effort routing", "Fallback chain"]:
            with self.subTest(strategy=strategy):
                self.assertIn(strategy, table_text)
        for column in [
            "Behavior when the preferred model is unavailable",
            "Latency impact",
            "Cost impact",
            "Best-fit use case",
        ]:
            with self.subTest(column=column):
                self.assertIn(column, table_text)

    def test_worked_example_covers_latency_based_routing(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.section)
        for expected in [
            "*Scenario:*",
            "*Decision factors:*",
            "*Resolution:*",
            "*AWS example:*",
            "dashboard",
            "batch",
            "Claude Haiku",
            "Claude Opus",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_worked_example_includes_a_fallback_chain_on_the_latency_sensitive_path(self):
        example_text = self.section[self.section.index(WORKED_EXAMPLE_HEADING):]
        self.assertRegex(
            example_text,
            r"(?i)fallback chain.*dashboard|dashboard.*fallback chain",
        )
        self.assertIn("Amazon Nova Micro", example_text)

    def test_has_implementation_patterns_for_bedrock_agents_and_sagemaker_mme(self):
        self.assertIn(IMPLEMENTATION_HEADING, self.section)
        impl_text = self.section[self.section.index(IMPLEMENTATION_HEADING):]
        for expected in [
            "Amazon Bedrock Agents",
            "multi-agent collaboration",
            "Amazon SageMaker multi-model endpoints",
            "TargetModel",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, impl_text)

    def test_section_has_exam_tips(self):
        self.assertGreaterEqual(self.section.count("Exam tip:"), 2)


if __name__ == "__main__":
    unittest.main()
