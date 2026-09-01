"""Structural validation for the "Worked example: estimating and comparing
monthly inference costs across three model tiers" section added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3, Section 1 discusses cost as a
foundation-model selection criterion and its "Context window vs. cost and
latency" subsection includes a relative cost comparison table (Lowest /
Moderate / Highest across the Claude and Llama tiers) -- but nothing in the
domain walks through actually estimating or comparing a concrete monthly
inference cost across model tiers given a request volume and average
token counts, the same way the domain's other worked examples turn a
qualitative criterion (context window) into a concrete number before
comparing candidates. These tests guard the worked example added to close
that gap: it must exist, be linked from the table of contents and
cross-linked from Section 1's exam tip, sit between the "estimating tokens
for long-document summarization" worked example and the "Comparison table:
customization approaches" section, cover a request-volume-plus-average-
token scenario, show a monthly token-total calculation, a per-tier rate
table with worked total costs for Claude Haiku/Sonnet/Opus, an explicit
dollar and multiplier comparison across tiers, and carry an AWS example and
an exam tip like every other worked example in this domain guide.

Mirrors the conventions established in
tests/test_domain_3_context_window_budget_worked_example.py and
tests/test_domain_3_rag_troubleshooting_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_monthly_cost_worked_example.py -v
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
    "## Worked example: estimating and comparing monthly inference costs "
    "across three model tiers"
)
HEADING_REGEX = (
    r"\n## Worked example: estimating and comparing monthly inference "
    r"costs across three model tiers"
)
TOC_LINK = (
    "[Worked example: estimating and comparing monthly inference costs "
    "across three model tiers]"
    "(#worked-example-estimating-and-comparing-monthly-inference-costs-across-three-model-tiers)"
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


class TestDomain3MonthlyCostWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_worked_example_sits_between_the_summarization_example_and_the_comparison_table(self):
        summarization_pos = self.text.index(
            "## Worked example: estimating tokens for long-document "
            "summarization"
        )
        comparison_table_pos = self.text.index(
            "## Comparison table: customization approaches for foundation "
            "model applications"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(summarization_pos, heading_pos)
        self.assertLess(heading_pos, comparison_table_pos)

    def test_scenario_gives_request_volume_and_average_token_counts(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("500,000 requests per month", self.section)
        self.assertIn("800 input tokens", self.section)
        self.assertIn("200 output tokens", self.section)

    def test_computes_total_monthly_input_and_output_tokens(self):
        for expected in [
            "400,000,000",
            "input tokens",
            "100,000,000",
            "output tokens",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_per_tier_rate_table_has_worked_totals_for_all_three_tiers(self):
        for expected in [
            "Claude Haiku",
            "Claude Sonnet",
            "Claude Opus",
            "**$225**",
            "**$2,700**",
            "**$13,500**",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_compares_tiers_with_explicit_dollar_deltas_and_multipliers(self):
        self.assertIn("$225", self.section)
        self.assertRegex(self.section, r"(?i)12x")
        self.assertRegex(self.section, r"(?i)60x")
        self.assertIn("$13,275", self.section)

    def test_prices_input_and_output_tokens_separately(self):
        self.assertRegex(self.section, r"(?i)input and output tokens? separately")

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
            "[monthly cost worked example]"
            "(#worked-example-estimating-and-comparing-monthly-inference-costs-across-three-model-tiers)",
            section_1,
        )


if __name__ == "__main__":
    unittest.main()
