"""Structural validation for the "Cost governance: bounding total spend
with Service Quotas and API Gateway usage plans" subsection added to
docs/domain-5-security-compliance-governance.md.

The gap this covers: cross-domain scenario questions Q16-Q18 in
docs/cross-domain-scenario-questions.md test bounding *aggregate*
inference spend with AWS Service Quotas and Amazon API Gateway usage
plans, but Domain 5 previously only surfaced Service Quotas/API Gateway as
a single bullet inside the "model denial of service" security-threat
catalog, with no dedicated section framing this as a cost-governance
concern distinct from (and complementary to) Domain 3's per-request
token/throughput controls. These tests guard the new subsection added to
close that gap: it must exist inside "## 1. Securing AI systems", sit
after the "Common security threats..." subsection and before "Security
frameworks...", be linked from the table of contents, cover Service
Quotas and API Gateway usage plans, and cross-link to the companion
Domain 3 subsection -- without adding any new numbered section or
mini-quiz block (this repo's structural tests assert exact counts for
both).

Mirrors the conventions established in
tests/test_domain_5_subsection_mini_quizzes.py.

Run with:
    python3 -m unittest tests/test_domain_5_cost_governance_subsection.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)

HEADING = (
    "### Cost governance: bounding total spend with Service Quotas and "
    "API Gateway usage plans"
)
TOC_LINK = (
    "[Cost governance: bounding total spend with Service Quotas and API "
    "Gateway usage plans]"
    "(#cost-governance-bounding-total-spend-with-service-quotas-and-api-gateway-usage-plans)"
)
CROSS_LINK = (
    "domain-3-applications-of-foundation-models.md"
    "#cost-governance-bounding-per-request-cost-with-max-tokens-and-provisioned-throughput"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain5CostGovernanceSubsection(unittest.TestCase):
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
        toc = _section(self.text, r"\n## Table of contents", r"\n## 1\. ")
        self.assertIn(TOC_LINK, toc)

    def test_sits_inside_section_1_after_common_threats_and_before_frameworks(self):
        section_1 = _section(
            self.text,
            r"\n## 1\. Securing AI systems",
            r"\n## 2\. ",
        )
        threats_pos = section_1.index(
            "### Common security threats to AI systems and how to mitigate them"
        )
        heading_pos = section_1.index(HEADING)
        frameworks_pos = section_1.index(
            "### Security frameworks for AI systems: MITRE ATLAS and OWASP "
            "Top 10 for LLM Applications"
        )
        self.assertLess(threats_pos, heading_pos)
        self.assertLess(heading_pos, frameworks_pos)

    def test_covers_service_quotas_and_api_gateway_usage_plans(self):
        for expected in ["Service Quotas", "API Gateway", "usage plan"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_frames_aggregate_spend_as_distinct_from_per_request_cost(self):
        self.assertRegex(self.subsection, r"(?i)\*\*aggregate\*\*")

    def test_cross_links_to_domain_3_subsection(self):
        self.assertIn(CROSS_LINK, self.subsection)

    def test_has_an_example_and_exam_tip(self):
        self.assertIn("**Example:**", self.subsection)
        self.assertIn("**Exam tip:**", self.subsection)

    def test_no_new_numbered_section_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-5]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            5,
            "Domain 5 must still have exactly 5 numbered sections",
        )

    def test_section_1_still_has_exactly_three_mini_quiz_blocks(self):
        section_1 = _section(
            self.text,
            r"\n## 1\. Securing AI systems",
            r"\n## 2\. ",
        )
        quiz_headings = re.findall(
            r"\n#### Mini-quiz: Test your understanding of", section_1
        )
        self.assertEqual(
            len(quiz_headings),
            3,
            "Section 1 must still contain exactly 3 mini-quiz headings "
            "(this change must not add or remove any mini-quiz)",
        )


if __name__ == "__main__":
    unittest.main()
