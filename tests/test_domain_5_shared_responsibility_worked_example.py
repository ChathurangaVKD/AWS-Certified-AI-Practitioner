"""Structural validation for the "Worked example: shared responsibility
for a SageMaker-to-Bedrock fine-tuning pipeline" subsection added to
docs/domain-5-security-compliance-governance.md.

The gap this covers: Domain 5 Section 5 ("AWS shared responsibility model
applied to AI/ML services") explains the Bedrock-vs-SageMaker
customer/AWS split only at a high level -- a diagram, a one-paragraph
example, and an exam tip -- without ever walking through a concrete,
multi-stage architecture that chains the two services together and
assigns responsibility stage by stage. That is exactly the pattern the
exam tests: a scenario question plants one misconfigured control
somewhere in a pipeline and asks whose responsibility it was. These
tests guard the new worked example added to close that gap: it must
exist as a "####"-level subsection nested inside Section 5 (after the
Section 5 exam tip, before the Section 5 mini-quiz), must not perturb
the standalone worked-example counts asserted elsewhere, must cover all
three pipeline stages with named AWS controls, must show a customer/AWS
contrast via a concrete incident, must include a summary table, and must
close with an exam tip. It also guards that the existing Section 5 exam
tip now links forward to this new subsection.

Mirrors the conventions established in
tests/test_domain_5_cost_capping_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_shared_responsibility_worked_example.py -v
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
    "#### Worked example: shared responsibility for a SageMaker-to-"
    "Bedrock fine-tuning pipeline"
)
HEADING_REGEX = (
    r"\n#### Worked example: shared responsibility for a SageMaker-to-"
    r"Bedrock fine-tuning pipeline"
)
SECTION_5_HEADING = (
    "## 5. AWS shared responsibility model applied to AI/ML services"
)
SECTION_5_MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of the AWS shared "
    "responsibility model"
)
FORWARD_LINK = (
    "[worked example below]"
    "(#worked-example-shared-responsibility-for-a-sagemaker-to-bedrock-fine-tuning-pipeline)"
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


class TestDomain5SharedResponsibilityWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_inside_section_5_after_exam_tip_and_before_mini_quiz(
        self,
    ):
        section_5_pos = self.text.index(SECTION_5_HEADING)
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(SECTION_5_MINI_QUIZ_HEADING)
        self.assertLess(section_5_pos, heading_pos)
        self.assertLess(heading_pos, mini_quiz_pos)

    def test_does_not_change_standalone_worked_example_count(self):
        # The new subsection is a level-4 heading nested inside Section 5,
        # not a new standalone "## Worked example" section, so it must not
        # perturb the counts asserted in tests/test_domain_5_study_guide.py
        # or tests/test_documentation_structure.py. There remain two
        # standalone "## Worked example" sections in Domain 5 (the closing
        # HIPAA walkthrough and the multi-region/multi-compliance
        # example).
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 2)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 0)

    def test_covers_all_three_pipeline_stages(self):
        for expected in [
            "SageMaker Processing",
            "Bedrock model-customization job",
            "Bedrock Provisioned Throughput",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_named_controls_per_stage(self):
        for expected in [
            "bedrock:CreateModelCustomizationJob",
            "AWS KMS",
            "AWS PrivateLink",
            "Guardrails for Amazon Bedrock",
            "bedrock:InvokeModel",
            "AWS CloudTrail",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_each_stage_has_customer_and_aws_responsibility_callouts(self):
        self.assertEqual(
            self.section.count("*Customer responsibility:*"), 3
        )
        self.assertEqual(self.section.count("*AWS responsibility:*"), 3)
        self.assertEqual(
            self.section.count("*Why the split lands here:*"), 3
        )

    def test_has_a_contrasting_incident_traced_to_the_customer_side(self):
        self.assertIn("**Contrasting incident:**", self.section)
        self.assertIn("anonymization", self.section.lower())

    def test_has_a_summary_table_covering_all_three_stages(self):
        self.assertIn("| Stage | Customer responsibility | AWS responsibility |", self.section)
        self.assertIn("SageMaker Processing (data prep)", self.section)
        self.assertIn("Bedrock fine-tuning", self.section)
        self.assertIn("Bedrock Provisioned Throughput (serving)", self.section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_section_5_exam_tip_links_forward_to_the_worked_example(self):
        section_5_text = _section(
            self.text,
            re.escape(SECTION_5_HEADING),
            r"\n## ",
        )
        self.assertIn(FORWARD_LINK, section_5_text)


if __name__ == "__main__":
    unittest.main()
