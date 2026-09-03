"""Structural validation for the "Worked example: data encryption vs.
model encryption in a multi-region HIPAA fine-tuning pipeline" subsection
added to docs/domain-5-security-compliance-governance.md.

The gap this covers: Domain 5 Section 1 ("Encryption of data at rest and
in transit for AI workloads") explains data-at-rest (KMS) and
data-in-transit (TLS) encryption, but never distinguishes that from
*model* encryption -- protecting the trained model artifact/weights as
intellectual property, a distinct asset requiring its own,
separately-configured KMS key. Nor does it show both in context inside
one worked scenario. That is exactly the kind of gap the exam probes: a
scenario that mentions only one of the two controls and asks whether
the other is also required. These tests guard the new worked example
added to close that gap: it must exist as a "####"-level subsection
nested inside Section 1 (after the KMS-key-lifecycle diagram, before the
PrivateLink section), must not perturb the standalone worked-example
counts asserted elsewhere, must cover the data-encryption controls, must
cover model-artifact encryption as a distinct control, must distinguish
PHI confidentiality from IP protection, must cover the multi-region
aspect, must link to the existing model-theft threat row, and must close
with an exam tip. It also guards that the existing Section 1 exam tip
now links forward to this new subsection.

Mirrors the conventions established in
tests/test_domain_5_shared_responsibility_worked_example.py and
tests/test_domain_5_cost_capping_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_data_vs_model_encryption_worked_example.py -v
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
    "#### Worked example: data encryption vs. model encryption in a "
    "multi-region HIPAA fine-tuning pipeline"
)
HEADING_REGEX = (
    r"\n#### Worked example: data encryption vs\. model encryption in a "
    r"multi-region HIPAA fine-tuning pipeline"
)
KMS_DIAGRAM_CLOSING_FENCE = (
    'LOG --> REVOKE["Key revocation\\ndisable the key, or schedule\\n'
    'deletion with a waiting period"]\n```'
)
PRIVATELINK_HEADING = "### AWS PrivateLink and VPC endpoints for AI services"
FORWARD_LINK = (
    "[worked example below]"
    "(#worked-example-data-encryption-vs-model-encryption-in-a-"
    "multi-region-hipaa-fine-tuning-pipeline)"
)
MODEL_THEFT_LINK = "(#common-security-threats-to-ai-systems-and-how-to-mitigate-them)"


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


class TestDomain5DataVsModelEncryptionWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_between_kms_diagram_and_privatelink_section(
        self,
    ):
        diagram_pos = self.text.index(KMS_DIAGRAM_CLOSING_FENCE)
        heading_pos = self.text.index(HEADING)
        privatelink_pos = self.text.index(PRIVATELINK_HEADING)
        self.assertLess(diagram_pos, heading_pos)
        self.assertLess(heading_pos, privatelink_pos)

    def test_does_not_change_standalone_worked_example_count(self):
        # The new subsection is a level-4 heading nested inside Section 1,
        # not a new standalone "## Worked example" section, so it must not
        # perturb the counts asserted in tests/test_domain_5_study_guide.py
        # or tests/test_documentation_structure.py. There remain two
        # standalone "## Worked example" sections in Domain 5 (the closing
        # HIPAA walkthrough and the multi-region/multi-compliance
        # example), and no level-3 "### Worked example:" headings.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 2)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 0)

    def test_covers_data_encryption_controls(self):
        for expected in [
            "customer managed KMS key",
            "TLS/HTTPS",
            "S3 bucket",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_model_encryption_as_a_distinct_control(self):
        for expected in [
            "model-customization job",
            "model artifact",
            "weights",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_distinguishes_phi_confidentiality_from_ip_protection(self):
        self.assertIn("PHI", self.section)
        self.assertTrue(
            "intellectual property" in self.section
            or " IP" in self.section
            or "IP." in self.section,
            "expected the worked example to name intellectual property "
            "as the asset model encryption protects",
        )

    def test_covers_multi_region_aspect(self):
        for expected in ["`us-east-1`", "`us-west-2`", "Region-scoped"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_links_to_the_model_theft_threat(self):
        self.assertIn(MODEL_THEFT_LINK, self.section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_section_1_exam_tip_links_forward_to_the_worked_example(self):
        self.assertIn(FORWARD_LINK, self.text)
        exam_tip_pos = self.text.index(
            '**Exam tip:** "Encryption at rest"'
        )
        forward_link_pos = self.text.index(FORWARD_LINK)
        heading_pos = self.text.index(HEADING)
        self.assertLess(exam_tip_pos, forward_link_pos)
        self.assertLess(forward_link_pos, heading_pos)


if __name__ == "__main__":
    unittest.main()
