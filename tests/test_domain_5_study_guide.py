"""Structural validation for the shared-responsibility diagram added to
docs/domain-5-security-compliance-governance.md.

Domain 5 has no broader structural test suite yet (unlike Domains 1-4);
this file only covers the new diagram added for the Section 5 shared
responsibility model, mirroring the `_section` helper convention used in
tests/test_domain_1_study_guide.py.

Run with:
    python3 -m unittest tests/test_domain_5_study_guide.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain5StudyGuideExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(DOC_PATH.is_file(), f"expected study guide at {DOC_PATH}")


class TestDomain5SharedResponsibilityDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_shared_responsibility_section_has_a_boundary_diagram(self):
        section = _section(
            self.text,
            r"\n## 5\. AWS shared responsibility model applied to AI/ML services",
        )
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "shared responsibility section should include a boundary diagram",
        )
        diagram = "\n".join(fences)
        for term in [
            "Bedrock",
            "SageMaker",
            "CUSTOMER",
            "in the cloud",
            "of the cloud",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)


class TestDomain5GovernanceDecisionTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_governance_section_has_a_decision_tree(self):
        section = _section(
            self.text,
            r"\n## 3\. AWS Config, AWS Audit Manager, and AWS CloudTrail for AI governance",
        )
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "governance services section should include a decision-tree diagram",
        )
        diagram = "\n".join(fences)
        for term in [
            "AWS CloudTrail",
            "AWS Config",
            "AWS Audit Manager",
            "API activity",
            "configuration compliance",
            "audit-ready evidence report",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)


if __name__ == "__main__":
    unittest.main()
