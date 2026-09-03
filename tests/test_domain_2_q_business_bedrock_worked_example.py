"""Structural validation for the "Worked example: Amazon Q Business vs. a
custom Bedrock assistant for enterprise customer support" section added to
docs/domain-2-fundamentals-of-generative-ai.md.

The gap this covers: Amazon Q Business is referenced throughout Domain 2,
Section 5 and in aws-service-decision-guide.md's "layering Amazon Q
Business on an existing Bedrock deployment" branch expansion, but neither
place worked a full decision with numbers for a team choosing between
Amazon Q Business and a custom Bedrock build *from scratch* (as opposed to
layering Q Business onto a deployment that already exists). These tests
guard the new worked example added to close that gap: it must exist as a
standalone "## Worked example" section, be linked from the table of
contents, sit after the LLM-lifecycle worked example and before the
comparison table, cover per-user Amazon Q Business pricing vs. on-demand
Bedrock token cost with worked arithmetic, data-connector breadth, and
customization trade-offs, close with a recommendation, rationale, AWS
example, and exam tip, and must be cross-linked from
aws-service-decision-guide.md.

Mirrors the conventions established in
tests/test_domain_2_llm_lifecycle_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_2_q_business_bedrock_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = (
    REPO_ROOT / "docs" / "domain-2-fundamentals-of-generative-ai.md"
)
DECISION_GUIDE_PATH = REPO_ROOT / "docs" / "aws-service-decision-guide.md"

HEADING = (
    "## Worked example: Amazon Q Business vs. a custom Bedrock assistant "
    "for enterprise customer support"
)
HEADING_REGEX = (
    r"\n## Worked example: Amazon Q Business vs\. a custom Bedrock "
    r"assistant for enterprise customer support"
)
TOC_LINK = (
    "[Worked example: Amazon Q Business vs. a custom Bedrock assistant "
    "for enterprise customer support]"
    "(#worked-example-amazon-q-business-vs-a-custom-bedrock-assistant-"
    "for-enterprise-customer-support)"
)
LIFECYCLE_HEADING = (
    "## Worked example: end-to-end LLM lifecycle for an insurance "
    "claims-triage assistant"
)
COMPARISON_TABLE_HEADING = (
    "## Comparison table: AWS generative AI services at a glance"
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    """Return the text between a heading matching start_heading_regex and
    the next top-level (##) heading, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain2QBusinessBedrockWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(
            self.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        self.assertIn(TOC_LINK, toc)

    def test_sits_after_lifecycle_example_and_before_comparison_table(self):
        lifecycle_pos = self.text.index(LIFECYCLE_HEADING)
        heading_pos = self.text.index(HEADING)
        table_pos = self.text.index(COMPARISON_TABLE_HEADING)
        self.assertLess(lifecycle_pos, heading_pos)
        self.assertLess(heading_pos, table_pos)

    def test_is_a_fifth_standalone_worked_example_and_does_not_change_numbered_sections(
        self,
    ):
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 5)
        numbered_sections = re.findall(r"\n## [1-7]\. ", self.text)
        self.assertEqual(len(numbered_sections), 7)

    def test_has_a_scenario(self):
        self.assertIn("**Scenario:**", self.section)

    def test_has_two_options_considered(self):
        self.assertIn("**Options considered:**", self.section)
        self.assertIn("Amazon Q Business", self.section)
        self.assertIn("Agents for Amazon Bedrock", self.section)

    def test_covers_data_connector_breadth(self):
        self.assertIn("**Dimension 1: data-connector breadth.**", self.section)
        normalized = re.sub(r"\s+", " ", self.section)
        for connector in ["Zendesk", "Salesforce", "Confluence", "SharePoint"]:
            with self.subTest(connector=connector):
                self.assertIn(connector, normalized)

    def test_covers_per_user_vs_on_demand_cost_with_worked_arithmetic(self):
        self.assertIn(
            "**Dimension 2: cost model", self.section
        )
        normalized = re.sub(r"\s+", " ", self.section)
        self.assertIn("per named user per month", normalized)
        self.assertIn("per token actually generated", normalized)
        # A concrete monthly dollar total must appear for each option so
        # this is a worked calculation, not just a qualitative claim.
        self.assertIn("$4,000", self.section)
        self.assertIn("772", self.section)

    def test_covers_customization_tradeoffs(self):
        self.assertIn("**Dimension 3: customization trade-offs.**", self.section)
        normalized = re.sub(r"\s+", " ", self.section)
        self.assertIn("permissions-filtering layer", normalized)

    def test_has_a_recommendation_and_rationale(self):
        self.assertIn("**Recommendation:**", self.section)
        self.assertIn("**Rationale:**", self.section)

    def test_shows_the_recommendation_can_flip(self):
        # Mirrors the voice-assistant worked example's "this doesn't
        # always win" reversal pattern -- the recommendation must be shown
        # as scenario-dependent, not an absolute rule.
        self.assertIn("doesn't mean Amazon Q Business always wins", self.section)

    def test_has_aws_example_and_exam_tip(self):
        self.assertIn("**AWS example:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_cross_links_to_decision_guide_layering_branch(self):
        self.assertIn(
            "aws-service-decision-guide.md#branch-expansion-layering-"
            "amazon-q-business-on-an-existing-bedrock-deployment",
            self.section,
        )

    def test_cross_links_to_section_5(self):
        self.assertIn("#5-aws-generative-ai-services-and-capabilities", self.section)


class TestAwsServiceDecisionGuideLinksToNewWorkedExample(unittest.TestCase):
    """aws-service-decision-guide.md's Q Business layering branch
    expansion should point readers at the new Domain 2 worked example that
    applies it with real numbers, per the task's requested
    cross-reference."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DECISION_GUIDE_PATH)

    def test_links_to_the_domain_2_worked_example(self):
        self.assertIn(
            "domain-2-fundamentals-of-generative-ai.md#worked-example-"
            "amazon-q-business-vs-a-custom-bedrock-assistant-for-"
            "enterprise-customer-support",
            self.text,
        )

    def test_link_sits_near_the_q_business_layering_branch(self):
        idx = self.text.find(
            "### Branch expansion: layering Amazon Q Business on an "
            "existing Bedrock deployment"
        )
        self.assertNotEqual(idx, -1)
        next_section = self.text.find("\n## ", idx)
        window = self.text[idx: next_section if next_section != -1 else len(self.text)]
        self.assertIn("worked-example-amazon-q-business-vs-a-custom-bedrock", window)


if __name__ == "__main__":
    unittest.main()
