"""Structural validation for the NIST AI RMF -> AWS services mapping
diagram added to docs/domain-5-security-compliance-governance.md's
Section 2 ("AWS compliance standards relevant to AI workloads").

The gap this covers: the "NIST AI Risk Management Framework (AI RMF) --
conceptual level" subsection introduced the framework's four core
functions (Govern, Map, Measure, Manage) entirely in prose, with no visual
mapping of which AWS services support each function. The existing
"Compliance framework decision matrix" diagram (covered by
tests/test_domain_5_compliance_framework_decision_matrix.py) only treats
NIST AI RMF as a single leaf node -- it does not visualize the internal
Govern/Map/Measure/Manage structure or the services that align to each
function. These tests guard the new Mermaid diagram: it must sit inside
the NIST AI RMF subsection (immediately before that subsection's
mini-quiz), use Mermaid flowchart/graph syntax, and reference all four
NIST functions and the AWS services called out for governance (SageMaker,
Bedrock, Clarify, CloudTrail, Config, Audit Manager).

Mirrors the conventions established in
tests/test_domain_5_compliance_framework_decision_matrix.py.

Run with:
    python3 -m unittest tests/test_domain_5_nist_ai_rmf_function_mapping_diagram.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)

SECTION_2_HEADING = r"\n## 2\. AWS compliance standards relevant to AI workloads"
NIST_HEADING = (
    "### NIST AI Risk Management Framework (AI RMF) — conceptual level"
)
NIST_MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of GDPR, HIPAA, and the "
    "NIST AI RMF"
)

REQUIRED_FUNCTIONS = ["GOVERN", "MAP", "MEASURE", "MANAGE"]

REQUIRED_SERVICES = [
    "SageMaker",
    "Bedrock",
    "Clarify",
    "CloudTrail",
    "AWS Config",
    "Audit Manager",
]


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


class TestDomain5NistAiRmfFunctionMappingDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section_2 = _section(cls.text, SECTION_2_HEADING)

    def test_nist_heading_still_present_in_section_2(self):
        self.assertIn(NIST_HEADING, self.section_2)

    def test_nist_subsection_still_immediately_precedes_its_mini_quiz(self):
        nist_pos = self.section_2.index(NIST_HEADING)
        mini_quiz_pos = self.section_2.index(NIST_MINI_QUIZ_HEADING)
        self.assertLess(nist_pos, mini_quiz_pos)

    def _nist_subsection(self):
        start = self.section_2.index(NIST_HEADING)
        end = self.section_2.index(NIST_MINI_QUIZ_HEADING)
        return self.section_2[start:end]

    def _diagram(self):
        subsection = self._nist_subsection()
        fences = re.findall(r"```mermaid(.*?)```", subsection, re.S)
        self.assertTrue(
            fences,
            "expected a ```mermaid fenced code block inside the NIST AI "
            "RMF subsection",
        )
        return "\n".join(fences)

    def test_nist_subsection_contains_a_mermaid_diagram(self):
        diagram = self._diagram()
        self.assertTrue(diagram.strip())

    def test_diagram_is_a_flowchart(self):
        diagram = self._diagram()
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "NIST AI RMF function-mapping diagram should use Mermaid "
            "flowchart/graph syntax",
        )

    def test_diagram_includes_all_four_nist_functions(self):
        diagram = self._diagram()
        for function in REQUIRED_FUNCTIONS:
            with self.subTest(function=function):
                self.assertIn(function, diagram)

    def test_diagram_includes_required_aws_services(self):
        diagram = self._diagram()
        for service in REQUIRED_SERVICES:
            with self.subTest(service=service):
                self.assertIn(service, diagram)

    def test_subsection_still_has_an_exam_tip(self):
        subsection = self._nist_subsection()
        self.assertIn("Exam tip:", subsection)


if __name__ == "__main__":
    unittest.main()
