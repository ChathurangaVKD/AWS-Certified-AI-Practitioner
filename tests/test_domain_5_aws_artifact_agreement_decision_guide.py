"""Structural validation for the "Decision guide: choosing the right AWS
Artifact agreement (BAA vs. DPA)" subsection added to
docs/domain-5-security-compliance-governance.md's Section 2 ("AWS
compliance standards relevant to AI workloads").

The gap this covers: the existing `### AWS Artifact` subsection explained
that Artifact is where you download compliance reports and agreements
(mentioning the HIPAA BAA), but gave no guidance on *when* to use a BAA
vs. a GDPR Data Processing Addendum (DPA), how to request and verify an
agreement, or where that step belongs in a pre-deployment compliance
checklist. These tests guard the new subsection: it must sit immediately
inside Section 2's AWS Artifact material (after the existing AWS Artifact
prose, before the GDPR subsection), contain a scenario-to-agreement table
covering BAA/DPA/both/neither cases, requesting-and-verifying guidance, a
pre-deployment checklist with at least four steps, an exam tip, a link
back to the existing compliance framework decision matrix, and a new
glossary entry for DPA -- without disturbing the original AWS Artifact
text.

Mirrors the conventions established in
tests/test_domain_5_compliance_framework_decision_matrix.py and
tests/test_domain_5_multi_region_compliance_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_aws_artifact_agreement_decision_guide.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)

AWS_ARTIFACT_HEADING = "### AWS Artifact"
ORIGINAL_EXAMPLE_SENTENCE = "download the relevant report from AWS Artifact Reports."
HEADING = (
    "#### Decision guide: choosing the right AWS Artifact agreement "
    "(BAA vs. DPA)"
)
GDPR_HEADING = "### GDPR (General Data Protection Regulation) — conceptual level"
GLOSSARY_HEADING = "## Key terms glossary"


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    """Return the text between a heading matching start_heading_regex and
    the next top-level (##) heading, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain5AwsArtifactAgreementDecisionGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_heading_is_inside_aws_artifact_subsection_before_gdpr(self):
        artifact_pos = self.text.index(AWS_ARTIFACT_HEADING)
        heading_pos = self.text.index(HEADING)
        gdpr_pos = self.text.index(GDPR_HEADING)
        self.assertLess(artifact_pos, heading_pos)
        self.assertLess(heading_pos, gdpr_pos)

    def _subsection(self):
        start = self.text.index(HEADING)
        end = self.text.index(GDPR_HEADING)
        return self.text[start:end]

    def test_table_has_required_columns(self):
        subsection = self._subsection()
        self.assertRegex(subsection, r"\|\s*-{2,}\s*\|")
        self.assertIn("Compliance scenario", subsection)
        self.assertIn("AWS Artifact agreement", subsection)

    def test_table_covers_baa_dpa_both_and_neither_scenarios(self):
        subsection = self._subsection()
        for expected in [
            "Business Associate Addendum (BAA)",
            "AWS GDPR Data Processing Addendum (DPA)",
            "Both the BAA and the DPA",
            "Artifact **Reports**, not Agreements",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, subsection)

    def test_subsection_explains_requesting_and_verifying(self):
        subsection = self._subsection()
        self.assertIn("**Requesting and verifying an agreement:**", subsection)
        self.assertIn("HIPAA-eligible services", subsection)
        self.assertIn("Active", subsection)

    def test_subsection_has_pre_deployment_checklist_with_at_least_four_steps(self):
        subsection = self._subsection()
        self.assertIn(
            "**Where this fits in the pre-deployment checklist:**", subsection
        )
        steps = re.findall(r"^\d+\.\s", subsection, re.M)
        self.assertGreaterEqual(len(steps), 4)

    def test_subsection_has_exam_tip(self):
        subsection = self._subsection()
        self.assertIn("**Exam tip:**", subsection)

    def test_subsection_links_to_compliance_framework_decision_matrix(self):
        subsection = self._subsection()
        self.assertRegex(
            subsection,
            r"\[Compliance framework decision\s+matrix\]"
            r"\(#compliance-framework-decision-matrix\)",
        )

    def test_glossary_has_dpa_entry(self):
        glossary = _section(self.text, r"\n" + re.escape(GLOSSARY_HEADING))
        self.assertRegex(glossary, r"\*\*DPA \(Data Processing Addendum\)\*\*")

    def test_does_not_disturb_existing_aws_artifact_example(self):
        self.assertIn(ORIGINAL_EXAMPLE_SENTENCE, self.text)
        example_pos = self.text.index(ORIGINAL_EXAMPLE_SENTENCE)
        heading_pos = self.text.index(HEADING)
        self.assertLess(example_pos, heading_pos)


if __name__ == "__main__":
    unittest.main()
