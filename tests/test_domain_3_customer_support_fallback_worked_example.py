"""Structural validation for the "Worked example: fallback routing for a
customer support assistant across three candidate models" subsection
added to docs/domain-3-applications-of-foundation-models.md.

The gap this covers: the "Multi-model routing and fallback strategies"
subsection already had a design-time flowchart, a runtime decision tree
for choosing among fallback candidates, a latency-based routing worked
example (dashboard vs. batch), and implementation patterns -- but no
worked example that walks through a full customer-support-assistant
scenario routing between multiple (2-3) candidate models based on
availability, cost, and performance trade-offs, with an explicit outcome
for each decision branch. This test guards the new subsection that closes
that gap: it must exist nested inside the "Multi-model routing and
fallback strategies" subsection, after the implementation-patterns
subsection and before Section 1's mini-quiz, describe three named
candidate models, and spell out the outcome for each of the runtime
decision tree's branches (primary succeeds, first fallback, second
fallback, chain exhausted).

Mirrors the conventions established in
tests/test_domain_3_multi_model_routing_worked_example.py and
tests/test_domain_3_fallback_routing_decision_tree.py.

Run with:
    python3 -m unittest tests/test_domain_3_customer_support_fallback_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

PARENT_SECTION_HEADING = (
    "### Multi-model routing and fallback strategies: routing requests to "
    "the right model at request time"
)
IMPLEMENTATION_HEADING = (
    "#### Implementation patterns: Bedrock Agents and SageMaker "
    "multi-model endpoints"
)
WORKED_EXAMPLE_HEADING = (
    "#### Worked example: fallback routing for a customer support "
    "assistant across three candidate models"
)
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of FM application design "
    "considerations"
)
TOC_LINK = (
    "[Worked example: fallback routing for a customer support assistant "
    "across three candidate models]"
    "(#worked-example-fallback-routing-for-a-customer-support-assistant-"
    "across-three-candidate-models)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


class TestDomain3CustomerSupportFallbackWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        start = cls.text.index(WORKED_EXAMPLE_HEADING)
        end = cls.text.index(MINI_QUIZ_HEADING)
        cls.section = cls.text[start:end]

    def test_heading_exists(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.text)

    def test_toc_links_to_the_new_subsection(self):
        toc_start = self.text.index("## Table of contents")
        toc_end = self.text.index("## Domain overview")
        toc = self.text[toc_start:toc_end]
        self.assertIn(TOC_LINK, toc)

    def test_is_positioned_after_implementation_patterns_and_before_mini_quiz(self):
        parent_pos = self.text.index(PARENT_SECTION_HEADING)
        implementation_pos = self.text.index(IMPLEMENTATION_HEADING)
        worked_example_pos = self.text.index(WORKED_EXAMPLE_HEADING)
        mini_quiz_pos = self.text.index(MINI_QUIZ_HEADING)
        self.assertLess(parent_pos, implementation_pos)
        self.assertLess(implementation_pos, worked_example_pos)
        self.assertLess(worked_example_pos, mini_quiz_pos)

    def test_does_not_change_the_standalone_or_nested_level_3_worked_example_counts(self):
        # This subsection's heading is a level-4 "####" heading nested
        # inside Section 1, not a new standalone "## Worked example:"
        # section or a new "### Worked example:" subsection, so it must
        # not change either of those pre-existing counts.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 8)

    def test_describes_a_customer_support_assistant_scenario(self):
        for expected in [
            "*Scenario:*",
            "customer support",
            "*Decision factors:*",
            "Availability",
            "Rate limits",
            "Cost",
            "*Resolution:*",
            "*AWS example:*",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_names_three_distinct_candidate_models(self):
        for model in ["Claude Sonnet", "Nova Lite", "Claude Haiku"]:
            with self.subTest(model=model):
                self.assertIn(model, self.section)

    def test_has_a_branch_outcome_table_covering_all_four_runtime_outcomes(self):
        self.assertRegex(self.section, r"\|\s*-{2,}\s*\|")
        for column in ["Branch", "Condition", "Model called", "Outcome"]:
            with self.subTest(column=column):
                self.assertIn(column, self.section)
        # Every branch of the runtime decision tree gets an explicit,
        # distinct outcome: primary succeeds, first fallback, second
        # fallback, and chain exhausted.
        self.assertIn("primary", self.section.lower())
        self.assertIn("FM-2", self.section)
        self.assertIn("FM-3", self.section)
        self.assertRegex(self.section, r"(?i)exhausted")
        self.assertRegex(self.section, r"(?i)human agent")

    def test_references_the_runtime_decision_tree_check_order(self):
        self.assertRegex(
            self.section,
            r"(?i)availability, then rate limits, then cost",
        )
        self.assertIn(
            "#runtime-decision-tree-selecting-a-fallback-model-when-the-"
            "primary-is-unavailable-rate-limited-or-too-costly",
            self.section,
        )

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.section)


if __name__ == "__main__":
    unittest.main()
