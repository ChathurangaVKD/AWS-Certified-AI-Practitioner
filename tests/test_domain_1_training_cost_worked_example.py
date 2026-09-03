"""Structural validation for the "Worked example: estimating training cost
for the loan-default predictor: SageMaker managed spot training vs.
on-demand" subsection added to docs/domain-1-fundamentals-of-ai-and-ml.md.

The gap this covers: Domain 1's "The ML development lifecycle" section
names Managed Spot Training as the tool for cutting model-training compute
cost (Section 2, step 5) but never shows the arithmetic behind that claim,
unlike Domain 3's several inference-cost worked examples (e.g.
docs/domain-3-applications-of-foundation-models.md's "estimating and
comparing monthly inference costs across three model tiers" walkthrough).
These tests guard the new worked-example subsection added to close that
gap: it must exist as a "###"-level subsection nested inside Section 2
(after its exam tip, before the "Production deployment strategies and
model versioning" subsection), be linked from the table of contents, cover
instance-type selection, Managed Spot Training's checkpoint/interruption
mechanics, a per-run and monthly cost comparison against On-Demand, when
Spot is *not* appropriate, and close with an exam tip -- and must not
perturb the standalone/nested "## Worked example" and mini-quiz counts
asserted elsewhere in this repo's test suite.

Mirrors the conventions established in
tests/test_domain_1_canary_blue_green_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_1_training_cost_worked_example.py -v
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
    "### Worked example: estimating training cost for the loan-default "
    "predictor: SageMaker managed spot training vs. on-demand"
)
HEADING_REGEX = (
    r"\n### Worked example: estimating training cost for the loan-default "
    r"predictor: SageMaker managed spot training vs\. on-demand"
)
TOC_LINK = (
    "[Worked example: estimating training cost for the loan-default "
    "predictor: SageMaker managed spot training vs. on-demand]"
    "(#worked-example-estimating-training-cost-for-the-loan-default-"
    "predictor-sagemaker-managed-spot-training-vs-on-demand)"
)
SECTION_2_HEADING = "## 2. The ML development lifecycle"
DEPLOYMENT_STRATEGIES_HEADING = (
    "### Production deployment strategies and model versioning"
)
MINI_QUIZ_HEADING = "#### Mini-quiz: Test your understanding of the ML lifecycle"


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


class TestDomain1TrainingCostWorkedExample(unittest.TestCase):
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

    def test_worked_example_is_nested_after_the_section_2_exam_tip_and_before_deployment_strategies(
        self,
    ):
        section_2_pos = self.text.index(SECTION_2_HEADING)
        heading_pos = self.text.index(HEADING)
        deployment_pos = self.text.index(DEPLOYMENT_STRATEGIES_HEADING)
        quiz_pos = self.text.index(MINI_QUIZ_HEADING)
        self.assertLess(section_2_pos, heading_pos)
        self.assertLess(heading_pos, deployment_pos)
        self.assertLess(deployment_pos, quiz_pos)

    def test_does_not_change_standalone_worked_example_or_mini_quiz_counts(
        self,
    ):
        # The new subsection is a level-3 heading nested inside Section 2,
        # not a new standalone "## Worked example" section and not a new
        # mini-quiz, so it must not perturb the counts asserted in
        # tests/test_domain_1_canary_blue_green_worked_example.py or
        # tests/test_documentation_structure.py's per-domain accounting
        # (beyond the deliberate +1 nested "###"/"####" worked-example
        # subsection count already reflected there).
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
        self.assertIn("loan-default", self.section)

    def test_covers_instance_type_selection_with_a_comparison_table(self):
        self.assertIn("ml.m5.2xlarge", self.section)
        self.assertIn("ml.m5.xlarge", self.section)
        self.assertIn("ml.p3.2xlarge", self.section)
        self.assertIn("vCPU", self.section)
        self.assertIn("Memory", self.section)

    def test_covers_managed_spot_training_interruption_mechanics(self):
        for expected in [
            "MaxRuntimeInSeconds",
            "MaxWaitTimeInSeconds",
            "checkpoint",
            "2-minute interruption notice",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_a_per_run_and_monthly_cost_comparison(self):
        self.assertIn("Cost per run", self.section)
        self.assertIn("Monthly workload", self.section)
        self.assertIn("On-Demand", self.section)
        self.assertIn("Managed Spot", self.section)
        # The dollar arithmetic itself, not just the labels.
        self.assertIn("$0.69", self.section)
        self.assertIn("$0.21", self.section)
        self.assertIn("$20.75", self.section)
        self.assertIn("$6.21", self.section)

    def test_covers_when_spot_is_not_appropriate(self):
        self.assertIn("24-hour compliance SLA", self.section)
        self.assertIn("emergency retrain", self.section)

    def test_cross_links_to_the_end_to_end_lifecycle_worked_example(self):
        self.assertIn(
            "#worked-example-end-to-end-ml-lifecycle-for-a-loan-default-predictor",
            self.section,
        )

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)


if __name__ == "__main__":
    unittest.main()
