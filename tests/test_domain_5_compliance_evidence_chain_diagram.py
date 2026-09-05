"""Structural validation for the AWS Config -> Audit Manager -> Artifact
compliance evidence chain diagram added to
docs/domain-5-security-compliance-governance.md's Section 3 ("AWS Config,
AWS Audit Manager, and AWS CloudTrail for AI governance").

The gap this covers: Section 2 discusses AWS Artifact (AWS-provided
compliance reports and agreements) and Section 3 discusses AWS Config and
AWS Audit Manager (customer-resource configuration evidence and
framework-mapped evidence collection), but until now the three services
were only ever discussed separately -- in prose, worked scenarios, and an
ASCII decision tree -- with no diagram showing how they chain together
into a single audit-ready compliance evidence package for an AI system.
The existing NIST AI RMF Mermaid diagram (covered by
tests/test_domain_5_nist_ai_rmf_function_mapping_diagram.py) maps Config
and Audit Manager to RMF functions but never mentions Artifact at all.

These tests guard the new Mermaid diagram: it must sit inside Section 3,
immediately after the third worked scenario ("...package itself.") and
before that section's mini-quiz heading, use Mermaid flowchart/graph
syntax, and show AWS Config's evidence flowing into AWS Audit Manager
alongside AWS Artifact's evidence, joining into one evidence package.

Mirrors the conventions established in
tests/test_domain_5_nist_ai_rmf_function_mapping_diagram.py.

Run with:
    python3 -m unittest tests/test_domain_5_compliance_evidence_chain_diagram.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)

SECTION_3_HEADING = (
    r"\n## 3\. AWS Config, AWS Audit Manager, and AWS CloudTrail for AI "
    r"governance"
)
SECTION_3_MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of AWS Config, Audit "
    "Manager, and CloudTrail for AI governance"
)
ANCHOR_TEXT = "package\nitself."
LEAD_IN_TEXT = "Visual summary — the compliance evidence chain"


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


class TestDomain5ComplianceEvidenceChainDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section_3 = _section(cls.text, SECTION_3_HEADING)

    def test_section_3_heading_still_present(self):
        self.assertIn(
            "AWS Config, AWS Audit Manager, and AWS CloudTrail for AI "
            "governance",
            self.text,
        )

    def _anchor_index(self):
        idx = self.section_3.find(ANCHOR_TEXT)
        self.assertGreaterEqual(
            idx,
            0,
            "expected the third worked scenario's closing text "
            "('...package itself.') to still be present in Section 3",
        )
        return idx

    def test_lead_in_sits_between_anchor_and_mini_quiz(self):
        anchor_pos = self._anchor_index()
        mini_quiz_pos = self.section_3.index(SECTION_3_MINI_QUIZ_HEADING)
        lead_in_pos = self.section_3.index(LEAD_IN_TEXT)
        self.assertLess(anchor_pos, lead_in_pos)
        self.assertLess(lead_in_pos, mini_quiz_pos)

    def _subsection(self):
        anchor_pos = self._anchor_index()
        mini_quiz_pos = self.section_3.index(SECTION_3_MINI_QUIZ_HEADING)
        return self.section_3[anchor_pos:mini_quiz_pos]

    def _diagram(self):
        subsection = self._subsection()
        fences = re.findall(r"```mermaid(.*?)```", subsection, re.S)
        self.assertTrue(
            fences,
            "expected a ```mermaid fenced code block between the third "
            "worked scenario and Section 3's mini-quiz heading",
        )
        return "\n".join(fences)

    def test_subsection_contains_a_mermaid_diagram(self):
        diagram = self._diagram()
        self.assertTrue(diagram.strip())

    def test_diagram_is_a_flowchart(self):
        diagram = self._diagram()
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "compliance evidence chain diagram should use Mermaid "
            "flowchart/graph syntax",
        )

    def test_diagram_references_all_three_services(self):
        diagram = self._diagram()
        for service in ["AWS Config", "AWS Audit Manager", "AWS Artifact"]:
            with self.subTest(service=service):
                self.assertIn(service, diagram)

    def test_config_feeds_audit_manager_and_artifact_is_present(self):
        diagram = self._diagram()
        config_pos = diagram.index("CONFIG")
        auditmgr_pos = diagram.index("AUDITMGR")
        self.assertLess(
            config_pos,
            auditmgr_pos,
            "CONFIG node should be defined/wired before AUDITMGR in the "
            "diagram to reflect Config's evidence feeding Audit Manager",
        )
        self.assertIn("ARTIFACT", diagram)

    def test_diagram_produces_an_evidence_package(self):
        diagram = self._diagram()
        self.assertIn("evidence package", diagram.lower())

    def test_subsection_still_has_an_exam_tip_after_the_diagram(self):
        subsection = self._subsection()
        diagram_end = subsection.index("```mermaid")
        diagram_end = subsection.index("```", diagram_end + len("```mermaid"))
        exam_tip_pos = subsection.index("Exam tip:", diagram_end)
        mini_quiz_marker = len(subsection)
        self.assertLess(exam_tip_pos, mini_quiz_marker)

    def test_existing_worked_scenarios_not_duplicated_or_corrupted(self):
        self.assertEqual(self.section_3.count("**Scenario:**"), 3)


if __name__ == "__main__":
    unittest.main()
