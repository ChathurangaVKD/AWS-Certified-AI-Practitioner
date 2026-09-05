"""Structural validation for the "On-demand vs. provisioned throughput: a
worked cost-comparison example" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 5's "Cost governance" subsection
explains *qualitatively* that Bedrock Provisioned Throughput trades a
flat committed rate for guaranteed capacity, and that it only pays off
for high/steady/predictable volume -- but never shows the arithmetic that
turns that rule into an actual purchase decision (a request volume, a
token estimate, an on-demand vs. provisioned cost comparison, and a
break-even point). These tests guard the new worked example added to
close that gap: it must exist inside the "Cost governance" subsection,
sit before Section 5's mini-quiz, and cover a realistic monthly request
volume, a per-request token estimate, a side-by-side on-demand vs.
provisioned cost calculation, an explicit break-even calculation, and
decision guidance for when the commitment is worth it.

Mirrors the conventions established in
tests/test_domain_3_cost_governance_subsection.py and
tests/test_domain_3_inference_failures_worked_example.py (the latter
deliberately avoids the "Worked example:" heading prefix so as not to
perturb the pinned worked-example heading counts asserted in
tests/test_documentation_structure.py -- this subsection follows the
same convention).

Run with:
    python3 -m unittest tests/test_domain_3_provisioned_throughput_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

COST_GOVERNANCE_HEADING = (
    "### Cost governance: bounding per-request cost with max tokens and "
    "provisioned throughput"
)
HEADING = (
    "#### On-demand vs. provisioned throughput: a worked cost-comparison "
    "example"
)
TOC_LINK = (
    "[On-demand vs. provisioned throughput: a worked cost-comparison "
    "example]"
    "(#on-demand-vs-provisioned-throughput-a-worked-cost-comparison-example)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3ProvisionedThroughputWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.subsection = _section(
            cls.text,
            re.escape(HEADING),
            r"\n#{1,4} ",
        )

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(
            self.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        self.assertIn(TOC_LINK, toc)

    def test_sits_inside_cost_governance_and_before_the_mini_quiz(self):
        section_5 = _section(
            self.text,
            r"\n## 5\. Amazon Bedrock features",
            r"\n## 6\. ",
        )
        cost_gov_pos = section_5.index(COST_GOVERNANCE_HEADING)
        heading_pos = section_5.index(HEADING)
        quiz_pos = section_5.index(
            "#### Mini-quiz: Test your understanding of Amazon Bedrock features"
        )
        self.assertLess(cost_gov_pos, heading_pos)
        self.assertLess(heading_pos, quiz_pos)

    def test_has_a_realistic_request_volume(self):
        for expected in ["200,000 requests/day", "6,000,000 requests/month"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_has_a_per_request_token_estimate(self):
        for expected in ["1,000 input tokens", "250 output tokens"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_has_side_by_side_on_demand_and_provisioned_cost_calculations(self):
        self.assertIn("$3,375/month", self.subsection)
        self.assertIn("$2,190/month", self.subsection)

    def test_has_an_explicit_break_even_calculation(self):
        self.assertRegex(self.subsection, r"(?i)break-even")
        self.assertIn("3,893,333 requests/month", self.subsection)

    def test_has_decision_guidance_on_when_reservation_is_worth_it(self):
        self.assertRegex(self.subsection, r"(?i)steady, not just high")
        self.assertRegex(self.subsection, r"(?i)commitment term")

    def test_has_an_aws_example_and_exam_tip(self):
        self.assertIn("**AWS example:**", self.subsection)
        self.assertIn("Exam tip:", self.subsection)

    def test_does_not_use_the_worked_example_heading_prefix(self):
        # Deliberately avoids "#### Worked example: ..." so it does not
        # perturb the pinned worked-example heading counts asserted in
        # tests/test_documentation_structure.py.
        self.assertNotRegex(HEADING, r"^#{2,4} Worked examples?:")

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
