"""Structural validation for the "Worked example: comparing fine-tuning and
prompt engineering on the same task" section added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3, Section 4 lays out fine-tuning vs. prompt
engineering (along with RAG and continued pre-training) as a qualitative
decision guide -- cost/complexity/accuracy/speed described as "Lowest",
"Highest", etc. -- and the domain already has worked examples for cost
estimation, RAG implementation/troubleshooting, and model selection under
constraints, but nothing walks through fine-tuning vs. prompt engineering
on one concrete task with actual token math, latency numbers, and accuracy
figures. These tests guard the worked example added to close that gap: it
must exist, be linked from the table of contents and cross-linked from
Section 4, sit between the monthly cost worked example and the
"Comparison table: customization approaches" section, size input tokens
per request for both approaches, convert to a monthly token/cost
comparison, account for fine-tuning's fixed provisioned-throughput cost,
compare latency, compare accuracy, and carry an AWS example and an exam
tip like every other worked example in this domain guide.

Mirrors the conventions established in
tests/test_domain_3_monthly_cost_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_fine_tuning_vs_prompt_engineering_worked_example.py -v
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
    "## Worked example: comparing fine-tuning and prompt engineering on "
    "the same task"
)
HEADING_REGEX = (
    r"\n## Worked example: comparing fine-tuning and prompt engineering "
    r"on the same task"
)
TOC_LINK = (
    "[Worked example: comparing fine-tuning and prompt engineering on the "
    "same task]"
    "(#worked-example-comparing-fine-tuning-and-prompt-engineering-on-the-same-task)"
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


class TestDomain3FineTuningVsPromptEngineeringWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_worked_example_sits_between_the_monthly_cost_example_and_the_comparison_table(self):
        monthly_cost_pos = self.text.index(
            "## Worked example: estimating and comparing monthly inference "
            "costs across three model tiers"
        )
        comparison_table_pos = self.text.index(
            "## Comparison table: customization approaches for foundation "
            "model applications"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(monthly_cost_pos, heading_pos)
        self.assertLess(heading_pos, comparison_table_pos)

    def test_scenario_describes_both_approaches_on_the_same_task(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertRegex(self.section, r"(?i)1,000,000 tickets/month")
        self.assertRegex(self.section, r"(?i)4,000.*labeled example tickets")
        self.assertIn("**Prompt engineering:**", self.section)
        self.assertIn("**Fine-tuning:**", self.section)

    def test_sizes_input_tokens_per_request_for_both_approaches(self):
        for expected in [
            "~2,000 tokens",
            "~300 tokens",
            "Few-shot examples",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_computes_monthly_token_totals_and_costs_for_both_approaches(self):
        for expected in [
            "2,000,000,000",
            "300,000,000",
            "**$625**",
            "**$200**",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_accounts_for_fine_tunings_fixed_provisioned_throughput_cost(self):
        self.assertRegex(self.section, r"(?i)provisioned throughput")
        self.assertRegex(self.section, r"(?i)\$4,000/month")
        self.assertRegex(self.section, r"(?i)\$4,200")

    def test_compares_latency_with_concrete_numbers(self):
        self.assertRegex(self.section, r"(?i)~450ms")
        self.assertRegex(self.section, r"(?i)~90ms")

    def test_compares_accuracy_with_concrete_numbers(self):
        self.assertRegex(self.section, r"(?i)82% exact-format compliance")
        self.assertRegex(self.section, r"(?i)97%")

    def test_has_an_aws_example_referencing_bedrock(self):
        self.assertIn("**AWS example:**", self.section)
        self.assertRegex(self.section, r"(?i)bedrock")

    def test_worked_example_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.section)

    def test_section_4_cross_links_to_the_new_worked_example(self):
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG vs\. prompt engineering",
            r"\n## 5\. ",
        )
        self.assertRegex(
            section_4,
            r"\[fine-tuning vs\. prompt engineering worked\s+"
            r"example\]\(#worked-example-comparing-fine-tuning-and-prompt-engineering-on-the-same-task\)",
        )


if __name__ == "__main__":
    unittest.main()
