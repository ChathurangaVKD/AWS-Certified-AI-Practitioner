"""Structural validation for the "Worked example: capping cost under
three different threat models" subsection added to
docs/domain-5-security-compliance-governance.md.

The gap this covers: Domain 5's "Cost governance: bounding total spend
with Service Quotas and API Gateway usage plans" subsection explains
*that* Service Quotas and API Gateway usage plans bound aggregate spend,
with one short generic example, but never shows how the configuration of
those two controls actually differs depending on *why* the bill is at
risk -- which is exactly what docs/cross-domain-scenario-questions.md
Q16-Q18 test: malicious abuse, an accidental spike, and a fixed monthly
budget ceiling. These tests guard the new worked example added to close
that gap: it must exist as a "####"-level subsection nested inside the
cost-governance subsection (after it, before "Security frameworks..."),
must not perturb the standalone/nested worked-example counts asserted
elsewhere, must cover all three threat models with the same
Service-Quotas/usage-plan vocabulary and the scenario/configuration/
rationale format, must show the budget-ceiling arithmetic concretely, and
must close with an exam tip. It also guards that the existing
cost-governance exam tip now links forward to this new subsection.

Mirrors the conventions established in
tests/test_domain_3_model_pair_comparison_worked_example.py and
tests/test_domain_5_cost_governance_subsection.py.

Run with:
    python3 -m unittest tests/test_domain_5_cost_capping_worked_example.py -v
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
    "#### Worked example: capping cost under three different threat models"
)
HEADING_REGEX = (
    r"\n#### Worked example: capping cost under three different threat "
    r"models"
)
COST_GOVERNANCE_HEADING = (
    "### Cost governance: bounding total spend with Service Quotas and "
    "API Gateway usage plans"
)
SECURITY_FRAMEWORKS_HEADING = (
    "### Security frameworks for AI systems: MITRE ATLAS and OWASP Top "
    "10 for LLM Applications"
)
FORWARD_LINK = (
    "[worked example below]"
    "(#worked-example-capping-cost-under-three-different-threat-models)"
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


class TestDomain5CostCappingWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_inside_section_1_after_cost_governance_and_before_frameworks(
        self,
    ):
        cost_governance_pos = self.text.index(COST_GOVERNANCE_HEADING)
        heading_pos = self.text.index(HEADING)
        frameworks_pos = self.text.index(SECURITY_FRAMEWORKS_HEADING)
        self.assertLess(cost_governance_pos, heading_pos)
        self.assertLess(heading_pos, frameworks_pos)

    def test_does_not_change_standalone_or_nested_3_worked_example_counts(
        self,
    ):
        # The new subsection is a level-4 heading nested inside the
        # existing cost-governance subsection, not a new standalone
        # "## Worked example" section and not a new "### Worked example"
        # subsection, so it must not perturb the counts asserted in
        # tests/test_domain_5_study_guide.py or
        # tests/test_documentation_structure.py.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 1)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 0)

    def test_covers_all_three_threat_models(self):
        for expected in [
            "credential-stuffing",
            "runaway retry loop",
            "budget ceiling",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_service_quotas_and_usage_plan_controls(self):
        for expected in [
            "Service Quota",
            "usage plan",
            "burst limit",
            "quota",
            "throttle",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_each_scenario_has_scenario_configuration_and_rationale_labels(
        self,
    ):
        for expected in ["*Scenario:*", "*Configuration:*", "*Why this control:*"]:
            with self.subTest(expected=expected):
                self.assertEqual(self.section.count(expected), 3)

    def test_budget_ceiling_scenario_shows_the_arithmetic(self):
        for expected in ["$500", "$0.01", "50,000 requests"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_cost_governance_exam_tip_links_forward_to_the_worked_example(
        self,
    ):
        cost_governance_section = _section(
            self.text,
            re.escape(COST_GOVERNANCE_HEADING),
            r"\n#{1,3} ",
        )
        self.assertIn(FORWARD_LINK, cost_governance_section)


if __name__ == "__main__":
    unittest.main()
