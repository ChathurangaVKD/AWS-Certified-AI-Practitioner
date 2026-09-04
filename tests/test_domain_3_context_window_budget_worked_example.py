"""Structural validation for the "Worked example: estimating a
context-window token budget" section added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3, Section 1 lists context window as a
model-selection criterion (and the "Context window vs. cost and latency"
subsection compares it against cost/latency across model tiers), and
Section 5 discusses context window again for Bedrock features -- but
neither ever walks through *estimating* the token budget a real scenario
needs before checking whether a candidate model's window is big enough.
These tests guard the worked example added to close that gap: it must
exist, be linked from the table of contents, sit between the
"selecting a foundation model under multiple competing constraints" worked
example and the "Comparison table: customization approaches" section, cover
a customer-service-chatbot-plus-100-page-policy-document scenario, show a
token-budget breakdown (system prompt, retrieved RAG context, conversation
history, reserved output) that sums to concrete worked totals, compare an
8K-context model against Claude's 200K context window (including the 8K
model failing to fit the escalated-turn total), discuss the resulting
cost/capability trade-off, and carry an AWS example and an exam tip like
every other worked example in this domain guide.

Mirrors the conventions established in
tests/test_domain_3_statistical_significance_worked_example.py and
tests/test_domain_3_rag_troubleshooting_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_context_window_budget_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

HEADING = "## Worked example: estimating a context-window token budget"
HEADING_REGEX = r"\n## Worked example: estimating a context-window token budget"
TOC_LINK = (
    "[Worked example: estimating a context-window token budget]"
    "(#worked-example-estimating-a-context-window-token-budget)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,2} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading of the same or higher level, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3ContextWindowBudgetWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_worked_example_sits_between_the_multi_constraint_example_and_the_comparison_table(self):
        multi_constraint_pos = self.text.index(
            "## Worked example: selecting a foundation model under multiple "
            "competing constraints"
        )
        comparison_table_pos = self.text.index(
            "## Comparison table: customization approaches for foundation "
            "model applications"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(multi_constraint_pos, heading_pos)
        self.assertLess(heading_pos, comparison_table_pos)

    def test_scenario_covers_multi_turn_chatbot_and_100_page_policy_document(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertRegex(self.section, r"(?i)multi-turn")
        self.assertRegex(self.section, r"(?i)100-page")
        self.assertRegex(self.section, r"(?i)policy document")

    def test_estimates_tokens_per_page_of_source_document(self):
        for expected in ["~650 tokens per page", "~65,000-token"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_token_budget_breakdown_table_has_worked_totals(self):
        # Component figures for the "typical turn" and "escalated turn"
        # columns of the token-budget breakdown table.
        for expected in [
            "System / instruction prompt",
            "Retrieved RAG context",
            "Conversation history so far",
            "4 × 650 = 2,600",
            "8 × 650 = 5,200",
            "8 × 160 = 1,280",
            "20 × 160 = 3,200",
            "**4,520**",
            "**9,040**",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_compares_8k_model_against_claude_200k_context_window(self):
        self.assertRegex(self.section, r"(?i)8K-context model")
        self.assertRegex(self.section, r"(?i)claude")
        self.assertIn("200,000 tokens", self.section)
        self.assertIn("8,000 tokens", self.section)

    def test_8k_model_fails_to_fit_the_escalated_turn(self):
        self.assertRegex(
            self.section,
            r"(?i)doesn't fit|does not fit",
            "expected the worked example to show the 8K-context model "
            "failing to fit the escalated-turn token total",
        )
        self.assertIn("1,040 tokens over budget", self.section)

    def test_discusses_cost_capability_trade_off(self):
        self.assertRegex(self.section, r"(?i)cost/capability trade-off")
        self.assertRegex(self.section, r"(?i)truncation")

    def test_has_an_aws_example_referencing_bedrock(self):
        self.assertIn("**AWS example:**", self.section)
        self.assertRegex(self.section, r"(?i)bedrock")

    def test_worked_example_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.section)

    def test_section_1_exam_tip_cross_links_to_the_new_worked_example(self):
        section_1 = _section(
            self.text,
            r"\n## 1\. Design considerations for foundation model applications",
            r"\n## 2\. ",
        )
        self.assertIn(
            "[token-budget worked example]"
            "(#worked-example-estimating-a-context-window-token-budget)",
            section_1,
        )


if __name__ == "__main__":
    unittest.main()
