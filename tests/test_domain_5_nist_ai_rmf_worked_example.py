"""Structural validation for the "Worked example: applying NIST AI RMF to
a multi-region Bedrock deployment" subsection added to
docs/domain-5-security-compliance-governance.md.

The gap this covers: Domain 5's "NIST AI Risk Management Framework (AI
RMF) — conceptual level" subsection explains the framework's four core
functions (Govern, Map, Measure, Manage) in prose, plus a diagram mapping
each function to supporting AWS services — but, unlike nearly every
sibling subsection in this domain doc, never traces all four functions
through one concrete, end-to-end scenario. That is exactly the kind of
gap the exam probes: a scenario describing a specific activity (e.g.
"comparing candidate models before launch") and asking which NIST
function it maps to. These tests guard the new worked example added to
close that gap: it must exist as a "####"-level subsection nested between
the existing NIST exam tip and the mini-quiz heading, must not perturb
the standalone worked-example counts asserted elsewhere, must cover all
four NIST functions with concrete AWS-service detail, must cover the
multi-region aspect, and must close with an exam tip. It also guards that
the existing NIST exam tip now links forward to this new subsection.

Mirrors the conventions established in
tests/test_domain_5_data_vs_model_encryption_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_nist_ai_rmf_worked_example.py -v
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
    "#### Worked example: applying NIST AI RMF to a multi-region "
    "Bedrock deployment"
)
HEADING_REGEX = (
    r"\n#### Worked example: applying NIST AI RMF to a multi-region "
    r"Bedrock deployment"
)
NIST_EXAM_TIP_START = (
    "**Exam tip:** Govern is the cross-cutting foundation"
)
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of GDPR, HIPAA, and the "
    "NIST AI RMF"
)
FORWARD_LINK = (
    "[worked example\n"
    "below](#worked-example-applying-nist-ai-rmf-to-a-multi-region-"
    "bedrock-deployment)"
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


class TestDomain5NistAiRmfWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_between_exam_tip_and_mini_quiz(self):
        exam_tip_pos = self.text.index(NIST_EXAM_TIP_START)
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(MINI_QUIZ_HEADING)
        self.assertLess(exam_tip_pos, heading_pos)
        self.assertLess(heading_pos, mini_quiz_pos)

    def test_does_not_change_standalone_worked_example_count(self):
        # The new subsection is a level-4 heading, not a new standalone
        # "## Worked example" section, so it must not perturb the counts
        # asserted in tests/test_domain_5_study_guide.py or
        # tests/test_documentation_structure.py.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 2)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 0)

    def test_covers_all_four_nist_functions(self):
        for expected in [
            "**Map —",
            "**Measure —",
            "**Manage —",
            "**Govern —",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_map_model_inventory_content(self):
        for expected in ["Model\n   Card", "Clarify", "bias"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_measure_evaluation_and_monitoring_content(self):
        for expected in ["model evaluation", "Model\n   Monitor", "drift"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_manage_guardrails_and_fine_tuning_content(self):
        for expected in [
            "Guardrails for Amazon Bedrock",
            "fine-tun",
            "Model Registry",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_govern_audit_logging_and_compliance_tracking_content(
        self,
    ):
        for expected in ["CloudTrail", "AWS Config", "Audit Manager"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_multi_region_aspect(self):
        for expected in ["`us-east-1`", "`eu-west-1`"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_nist_exam_tip_links_forward_to_the_worked_example(self):
        self.assertIn(FORWARD_LINK, self.text)
        exam_tip_pos = self.text.index(NIST_EXAM_TIP_START)
        forward_link_pos = self.text.index(FORWARD_LINK)
        heading_pos = self.text.index(HEADING)
        self.assertLess(exam_tip_pos, forward_link_pos)
        self.assertLess(forward_link_pos, heading_pos)


if __name__ == "__main__":
    unittest.main()
