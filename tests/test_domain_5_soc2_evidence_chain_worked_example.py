"""Structural validation for the "Worked example: assembling a SOC 2
audit evidence chain with AWS Config, Audit Manager, and Artifact"
subsection added to docs/domain-5-security-compliance-governance.md.

The gap this covers: Section 3 introduces AWS Config, AWS Audit Manager,
and AWS Artifact, and even adds a "Visual summary" diagram and ASCII
decision tree showing that the three chain together into one audit-ready
evidence package -- but until now nothing walked through a single,
concrete, step-by-step scenario showing *how* that chain actually plays
out for one AI system going through a real audit. The two large
standalone "## Worked example" sections later in the doc (HIPAA across
the lifecycle, and the multi-region GDPR/HIPAA/NIST RMF deployment) only
mention Config/Audit Manager/Artifact working together in passing within
a much broader scenario. This worked example closes that gap directly:
it must exist as a "####"-level subsection nested inside Section 3 after
that section's mini-quiz and before Section 4 begins, must not perturb
the standalone worked-example counts or the existing worked-scenario
count asserted elsewhere, must walk through Config capturing evidence,
Audit Manager assembling it (including a manual-evidence gap), Artifact
supplying AWS's own report, and a final assessment report, and must close
with an exam tip distinguishing the three services' roles.

Mirrors the conventions established in
tests/test_domain_5_nist_ai_rmf_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_soc2_evidence_chain_worked_example.py -v
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
    "#### Worked example: assembling a SOC 2 audit evidence chain with "
    "AWS Config, Audit Manager, and Artifact"
)
HEADING_REGEX = (
    r"\n#### Worked example: assembling a SOC 2 audit evidence chain "
    r"with AWS Config, Audit Manager, and Artifact"
)
SECTION_3_MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of AWS Config, Audit "
    "Manager, and CloudTrail for AI governance"
)
SECTION_3_MINI_QUIZ_LAST_ANSWER = (
    "custom frameworks to streamline audit preparation."
)
SECTION_4_HEADING = "## 4. Data governance strategies"


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


class TestDomain5Soc2EvidenceChainWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX, r"\n---\n")

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_sits_after_section_3_mini_quiz_and_before_section_4(
        self,
    ):
        mini_quiz_pos = self.text.index(SECTION_3_MINI_QUIZ_HEADING)
        last_answer_pos = self.text.index(SECTION_3_MINI_QUIZ_LAST_ANSWER)
        heading_pos = self.text.index(HEADING)
        section_4_pos = self.text.index(SECTION_4_HEADING)
        self.assertLess(mini_quiz_pos, last_answer_pos)
        self.assertLess(last_answer_pos, heading_pos)
        self.assertLess(heading_pos, section_4_pos)

    def test_does_not_change_standalone_worked_example_count(self):
        # The new subsection is a level-4 heading, not a new standalone
        # "## Worked example" section, so it must not perturb the counts
        # asserted in tests/test_domain_5_study_guide.py or
        # tests/test_documentation_structure.py.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 2)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 0)

    def test_does_not_add_a_fourth_scenario_marker_to_section_3(self):
        # tests/test_domain_5_compliance_evidence_chain_diagram.py asserts
        # Section 3 (heading to the next "## ") contains exactly three
        # "**Scenario:**" markers from the pre-existing worked scenarios.
        # This new subsection lives inside that same Section 3 span (it
        # precedes "## 4."), so it must use different wording.
        section_3 = _section(
            self.text,
            r"\n## 3\. AWS Config, AWS Audit Manager, and AWS CloudTrail "
            r"for AI governance",
            r"\n## ",
        )
        self.assertEqual(section_3.count("**Scenario:**"), 3)
        self.assertIn("**Setup:**", section_3)

    def test_covers_config_generating_evidence(self):
        for expected in ["AWS Config\n   rules", "encrypted", "SageMaker endpoint"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_audit_manager_assembling_evidence(self):
        for expected in [
            "AWS Audit Manager",
            "SOC 2",
            "assessment",
            "CloudTrail",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_manual_evidence_gap(self):
        for expected in ["manual evidence", "access-review"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_artifact_supplying_aws_report(self):
        for expected in ["AWS\n   Artifact", "SOC 2 Type II report"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_shared_responsibility_link(self):
        self.assertIn(
            "(#5-aws-shared-responsibility-model-applied-to-aiml-services)",
            self.section,
        )

    def test_covers_final_assessment_report(self):
        self.assertIn("assessment report", self.section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_has_five_numbered_steps(self):
        steps = re.findall(r"^\d+\. \*\*", self.section, re.M)
        self.assertEqual(len(steps), 5)


if __name__ == "__main__":
    unittest.main()
