"""Structural validation for the "Worked example: promoting a new model
version with canary deployment via SageMaker Model Registry" subsection
added to docs/domain-1-fundamentals-of-ai-and-ml.md.

The gap this covers: Domain 1's "Production deployment strategies and
model versioning" subsection explains the four staged-rollout patterns
and SageMaker Model Registry *separately*, with only a two-sentence "AWS
example" callout tying them together, but cross-domain scenario questions
(docs/cross-domain-scenario-questions.md) test the full end-to-end flow --
registering a new model version, staged traffic shifting, and rollback on
regression -- as one continuous decision, not two isolated facts. These
tests guard the new worked-example subsection added to close that gap: it
must exist as a "####"-level subsection nested inside the deployment
strategies subsection (after its exam tip, before the section's
mini-quiz), be linked from the table of contents, walk through registering
a candidate version, approval, staged canary traffic shifting, monitoring,
and automatic rollback, cover the blue/green variant, close with an exam
tip, and must not perturb the standalone/nested "## Worked example" and
mini-quiz counts asserted elsewhere in this repo's test suite.

Mirrors the conventions established in
tests/test_domain_5_cost_capping_worked_example.py and
tests/test_domain_1_deployment_strategies_subsection.py.

Run with:
    python3 -m unittest tests/test_domain_1_canary_blue_green_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-1-fundamentals-of-ai-and-ml.md"
)

HEADING = (
    "#### Worked example: promoting a new model version with canary "
    "deployment via SageMaker Model Registry"
)
HEADING_REGEX = (
    r"\n#### Worked example: promoting a new model version with canary "
    r"deployment via SageMaker Model Registry"
)
TOC_LINK = (
    "[Worked example: promoting a new model version with canary "
    "deployment via SageMaker Model Registry]"
    "(#worked-example-promoting-a-new-model-version-with-canary-"
    "deployment-via-sagemaker-model-registry)"
)
DEPLOYMENT_STRATEGIES_HEADING = (
    "### Production deployment strategies and model versioning"
)
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of the ML lifecycle"
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


class TestDomain1CanaryBlueGreenWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(
            self.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        self.assertIn(TOC_LINK, toc)

    def test_worked_example_is_nested_after_the_deployment_strategies_exam_tip_and_before_the_mini_quiz(
        self,
    ):
        deployment_pos = self.text.index(DEPLOYMENT_STRATEGIES_HEADING)
        heading_pos = self.text.index(HEADING)
        quiz_pos = self.text.index(MINI_QUIZ_HEADING)
        self.assertLess(deployment_pos, heading_pos)
        self.assertLess(heading_pos, quiz_pos)

    def test_does_not_change_standalone_worked_example_or_mini_quiz_counts(
        self,
    ):
        # The new subsection is a level-4 heading nested inside the
        # existing "### Production deployment strategies..." subsection,
        # not a new standalone "## Worked example" section and not a new
        # mini-quiz, so it must not perturb the counts asserted in
        # tests/test_domain_1_deployment_strategies_subsection.py or
        # tests/test_documentation_structure.py.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 1)
        section_2 = _section(
            self.text,
            r"\n## 2\. The ML development lifecycle",
            r"\n## 3\. ",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_2)
        self.assertEqual(len(quiz_headings), 1)
        numbered_sections = re.findall(r"\n## [1-7]\. ", self.text)
        self.assertEqual(len(numbered_sections), 7)

    def test_has_a_scenario(self):
        self.assertIn("**Scenario:**", self.section)

    def test_walks_through_register_approve_stage_monitor_rollback(self):
        for expected in [
            "Register the candidate version",
            "Review and approve",
            "Stage the canary rollout",
            "Monitor at each stage",
            "Roll back automatically on regression",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_model_registry_statuses(self):
        self.assertIn("SageMaker Model Registry", self.section)
        self.assertIn("Pending manual approval", self.section)
        self.assertIn("Approved", self.section)
        self.assertIn("Rejected", self.section)

    def test_covers_staged_canary_traffic_percentages(self):
        for expected in ["10%", "50%", "100%"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_automatic_rollback_trigger(self):
        self.assertIn("CloudWatch alarm", self.section)
        self.assertRegex(self.section, r"(?i)roll(s|ed)? back")

    def test_covers_the_blue_green_variant(self):
        self.assertIn("blue/green", self.section)
        self.assertIn("green", self.section)
        self.assertIn("blue", self.section)

    def test_cross_links_to_domain_5(self):
        self.assertIn(
            "domain-5-security-compliance-governance.md#1-securing-ai-systems",
            self.section,
        )

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)


if __name__ == "__main__":
    unittest.main()
