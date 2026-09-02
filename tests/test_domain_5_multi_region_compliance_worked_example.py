"""Structural validation for the "Worked example: a multi-region Bedrock
and SageMaker deployment under GDPR, HIPAA, and the NIST AI RMF" section
added to docs/domain-5-security-compliance-governance.md.

The gap this covers: Domain 5 had only two worked examples (the closing
HIPAA-regulated Bedrock walkthrough, and the nested cost-capping
subsection) covering 26 practice questions and 5 sections -- the thinnest
worked-example-to-question ratio of any domain (compare Domain 3's eight
examples for 20 questions). This new standalone section closes that gap
with a scenario that stacks two binding, region-scoped regulations
(GDPR, HIPAA) and one voluntary, global framework (the NIST AI RMF) over
a single company running both Amazon Bedrock and Amazon SageMaker across
both the US and the EU -- a common multi-domain exam scenario type that
none of the existing Domain 5 worked examples cover.

Mirrors the conventions established in
tests/test_domain_5_cost_capping_worked_example.py and
tests/test_domain_5_study_guide.py.

Run with:
    python3 -m unittest tests/test_domain_5_multi_region_compliance_worked_example.py -v
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
    "## Worked example: a multi-region Bedrock and SageMaker deployment "
    "under GDPR, HIPAA, and the NIST AI RMF"
)
HEADING_REGEX = (
    r"\n## Worked example: a multi-region Bedrock and SageMaker "
    r"deployment under GDPR, HIPAA, and the NIST AI RMF"
)
HIPAA_WORKED_EXAMPLE_HEADING = (
    "## Worked example: securing and governing a HIPAA-regulated Bedrock "
    "application across its lifecycle"
)
COMPARISON_TABLE_HEADING = (
    "## Comparison table: governance and monitoring services"
)
TOC_ANCHOR = (
    "#worked-example-a-multi-region-bedrock-and-sagemaker-deployment-"
    "under-gdpr-hipaa-and-the-nist-ai-rmf"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    """Return the text between a heading matching start_heading_regex and
    the next heading of the same or higher level, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain5MultiRegionComplianceWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)
        cls.toc = _section(
            cls.text, r"\n## Table of contents", r"\n## Domain overview"
        )

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_second_standalone_heading_after_hipaa_example(
        self,
    ):
        hipaa_idx = self.text.index(HIPAA_WORKED_EXAMPLE_HEADING)
        new_idx = self.text.index(HEADING)
        comparison_idx = self.text.index(COMPARISON_TABLE_HEADING)
        self.assertLess(hipaa_idx, new_idx)
        self.assertLess(new_idx, comparison_idx)

    def test_worked_example_has_scenario_and_exam_tip(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_worked_example_covers_both_services_both_regions_and_all_three_frameworks(
        self,
    ):
        for term in [
            "Amazon Bedrock",
            "Amazon SageMaker",
            "GDPR",
            "HIPAA",
            "NIST AI RMF",
            "us-east-1",
            "eu-central-1",
            "data residency",
            "AWS Artifact",
            "AWS KMS",
            "AWS CloudTrail",
            "AWS Config",
            "Audit Manager",
            "shared responsibility",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.section)

    def test_worked_example_has_at_least_six_numbered_steps(self):
        steps = re.findall(r"^\d+\.\s", self.section, re.M)
        self.assertGreaterEqual(len(steps), 6)

    def test_table_of_contents_links_to_worked_example(self):
        self.assertIn(TOC_ANCHOR, self.toc)

    def test_does_not_disturb_the_first_worked_example_match(self):
        # tests/test_domain_5_study_guide.py's TestDomain5WorkedExample
        # relies on the FIRST "## Worked example: ..." match in the file
        # being the closing HIPAA walkthrough. Guard that this new
        # section, inserted directly after it, doesn't become the first
        # match instead.
        match = re.search(r"\n## Worked example: .+", self.text)
        assert match, "no top-level '## Worked example: ' heading found"
        self.assertEqual(
            self.text[match.start() : match.end()],
            "\n" + HIPAA_WORKED_EXAMPLE_HEADING,
        )


if __name__ == "__main__":
    unittest.main()
