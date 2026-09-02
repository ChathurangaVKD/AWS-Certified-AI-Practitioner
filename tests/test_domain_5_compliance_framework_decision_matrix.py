"""Structural validation for the "Compliance framework decision matrix"
subsection added to docs/domain-5-security-compliance-governance.md's
Section 2 ("AWS compliance standards relevant to AI workloads").

The gap this covers: Section 2 explained GDPR, HIPAA, the NIST AI RMF, the
EU AI Act, ISO/IEC 42001, and the Algorithmic Accountability Act entirely
in prose, with no visual aid to help a learner quickly map a scenario
(region, data type, use case) to the correct framework and the AWS
services that support it -- a heavily exam-tested pattern. Domain 5 also
had zero Mermaid diagrams in Section 2 (all three of its diagrams lived in
Section 1). These tests guard the new subsection: it must sit inside
Section 2 (between the "ISO/IEC 42001 and the Algorithmic Accountability
Act" subsection and the Section 2 mini-quiz), contain a comparison table
with the requested columns covering all six frameworks, and a Mermaid
decision-tree diagram that resolves a scenario down to one of those six
frameworks.

Mirrors the conventions established in
tests/test_domain_3_rag_failure_decision_tree.py and
tests/test_domain_5_study_guide.py.

Run with:
    python3 -m unittest tests/test_domain_5_compliance_framework_decision_matrix.py -v
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
ISO_HEADING = "### ISO/IEC 42001 and the Algorithmic Accountability Act"
TABLE_HEADING = "### Compliance framework decision matrix"
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of AWS compliance standards "
    "for AI workloads"
)

# Keep in sync with REQUIRED_REGULATIONS in tests/test_domain_5_study_guide.py.
# Duplicated locally (rather than imported) so this file has no cross-file
# dependency.
REQUIRED_FRAMEWORKS = [
    "GDPR",
    "HIPAA",
    "NIST AI Risk Management Framework",
    "EU AI Act",
    "ISO/IEC 42001",
    "Algorithmic Accountability Act",
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


class TestDomain5ComplianceFrameworkDecisionMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section_2 = _section(cls.text, SECTION_2_HEADING)

    def test_heading_exists(self):
        self.assertIn(TABLE_HEADING, self.text)

    def test_heading_is_inside_section_2(self):
        self.assertIn(TABLE_HEADING, self.section_2)

    def test_heading_appears_after_algorithmic_accountability_subsection_and_before_mini_quiz(self):
        iso_pos = self.section_2.index(ISO_HEADING)
        table_pos = self.section_2.index(TABLE_HEADING)
        mini_quiz_pos = self.section_2.index(MINI_QUIZ_HEADING)
        self.assertLess(iso_pos, table_pos)
        self.assertLess(table_pos, mini_quiz_pos)

    def _matrix_subsection(self):
        start = self.section_2.index(TABLE_HEADING)
        end = self.section_2.index(MINI_QUIZ_HEADING)
        return self.section_2[start:end]

    def test_table_has_required_columns(self):
        subsection = self._matrix_subsection()
        fence_start = subsection.index("```mermaid")
        table_text = subsection[:fence_start]
        self.assertRegex(table_text, r"\|\s*-{2,}\s*\|")
        self.assertIn("Geographic scope", table_text)
        self.assertIn("Covered data", table_text)
        self.assertIn("Applicable AWS services", table_text)

    def test_table_covers_all_six_frameworks(self):
        subsection = self._matrix_subsection()
        fence_start = subsection.index("```mermaid")
        table_text = subsection[:fence_start]
        for framework in REQUIRED_FRAMEWORKS:
            with self.subTest(framework=framework):
                self.assertIn(framework, table_text)

    def test_diagram_is_a_mermaid_flowchart_with_branching_questions(self):
        subsection = self._matrix_subsection()
        fences = re.findall(r"```mermaid(.*?)```", subsection, re.S)
        self.assertTrue(
            fences,
            "expected a ```mermaid fenced code block under the compliance "
            "framework decision matrix heading",
        )
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "decision matrix diagram should use Mermaid flowchart/graph syntax",
        )
        self.assertIn(
            "?", diagram, "diagram should pose branching decision questions"
        )
        self.diagram = diagram

    def test_diagram_resolves_to_all_six_frameworks(self):
        subsection = self._matrix_subsection()
        fences = re.findall(r"```mermaid(.*?)```", subsection, re.S)
        diagram = "\n".join(fences)
        for pattern, label in [
            (r"GDPR", "GDPR"),
            (r"HIPAA", "HIPAA"),
            (r"EU AI Act", "EU AI Act"),
            (r"NIST", "NIST AI RMF"),
            (r"ISO", "ISO/IEC 42001"),
            (r"Algorithmic Accountability Act", "Algorithmic Accountability Act"),
        ]:
            with self.subTest(framework=label):
                self.assertRegex(diagram, pattern, f"diagram missing framework: {label!r}")

    def test_section_still_has_an_exam_tip(self):
        subsection = self._matrix_subsection()
        self.assertIn("Exam tip:", subsection)

    def test_toc_links_to_the_new_subsection(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(
            "[Compliance framework decision matrix](#compliance-framework-decision-matrix)",
            toc,
        )


if __name__ == "__main__":
    unittest.main()
