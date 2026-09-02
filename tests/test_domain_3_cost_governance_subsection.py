"""Structural validation for the "Cost governance: bounding per-request
cost with max tokens and provisioned throughput" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: cross-domain scenario questions Q16-Q18 in
docs/cross-domain-scenario-questions.md test *operational* cost-control
techniques (bounding per-request spend via max tokens, and
provisioned-throughput ROI for steady high-volume traffic), but Domain 3
previously only covered cost as an *estimation* concern (the "Worked
example: estimating and comparing monthly inference costs" and the
qualitative model-tier cost/latency table) and mentioned provisioned
throughput only as a Bedrock feature -- with no dedicated section
distinguishing operational cost *governance* from cost *estimation*.
These tests guard the new subsection added to close that gap: it must
exist inside "## 5. Amazon Bedrock features", sit before that section's
mini-quiz, be linked from the table of contents, cover max tokens and
provisioned-throughput ROI, and cross-link to the companion Domain 5
subsection -- without adding any new numbered section or mini-quiz block
(this repo's structural tests assert exact counts for both).

Mirrors the conventions established in
tests/test_domain_3_monthly_cost_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_cost_governance_subsection.py -v
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
    "### Cost governance: bounding per-request cost with max tokens and "
    "provisioned throughput"
)
TOC_LINK = (
    "[Cost governance: bounding per-request cost with max tokens and "
    "provisioned throughput]"
    "(#cost-governance-bounding-per-request-cost-with-max-tokens-and-provisioned-throughput)"
)
CROSS_LINK = (
    "domain-5-security-compliance-governance.md"
    "#cost-governance-bounding-total-spend-with-service-quotas-and-api-gateway-usage-plans"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3CostGovernanceSubsection(unittest.TestCase):
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

    def test_covers_max_tokens_and_provisioned_throughput(self):
        for expected in ["max tokens", "provisioned throughput", "on-demand"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_distinguishes_governance_from_estimation(self):
        self.assertRegex(self.subsection, r"(?i)cost \*estimation\*")
        self.assertRegex(self.subsection, r"(?i)cost\s+\*governance\*")

    def test_cross_links_to_domain_5_subsection(self):
        self.assertIn(CROSS_LINK, self.subsection)

    def test_has_an_aws_example_and_exam_tip(self):
        self.assertIn("**AWS example:**", self.subsection)
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
