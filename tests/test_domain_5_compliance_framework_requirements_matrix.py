"""Structural validation for the "Compliance framework requirements
comparison matrix" subsection added to
docs/domain-5-security-compliance-governance.md's Section 2 ("AWS
compliance standards relevant to AI workloads").

The gap this covers: Section 2 already had a "Compliance framework
decision matrix" that maps a scenario's region/data-type/use-case clues
to the right framework and its supporting AWS services, but nothing that
cross-cuts the five frameworks (GDPR, HIPAA, the NIST AI RMF, the EU AI
Act, and ISO/IEC 42001) by the specific compliance *requirements*
(encryption, audit logging, data residency, human oversight) that
scenario questions repeatedly test -- forcing a learner to re-read five
separate subsections to compare them. These tests guard the new
subsection: it must sit inside Section 2, immediately after the existing
decision matrix's exam tip and before the SageMaker Model Card worked
example, contain a table with the four requirement columns covering all
five frameworks (one row each), and close with an exam tip. It also
guards that the Table of Contents links to it.

Mirrors the conventions established in
tests/test_domain_5_compliance_framework_decision_matrix.py.

Run with:
    python3 -m unittest tests/test_domain_5_compliance_framework_requirements_matrix.py -v
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
DECISION_MATRIX_HEADING = "### Compliance framework decision matrix"
TABLE_HEADING = "### Compliance framework requirements comparison matrix"
MODEL_CARD_HEADING = (
    "#### Worked example: filling out a SageMaker Model Card for "
    "governance sign-off"
)

REQUIRED_FRAMEWORKS = [
    "GDPR",
    "HIPAA",
    "NIST AI RMF",
    "EU AI Act",
    "ISO/IEC 42001",
]

REQUIRED_COLUMNS = [
    "Encryption mandate",
    "Audit logging requirement",
    "Data residency requirement",
    "Human oversight requirement",
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


class TestDomain5ComplianceFrameworkRequirementsMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section_2 = _section(cls.text, SECTION_2_HEADING)

    def test_heading_exists(self):
        self.assertIn(TABLE_HEADING, self.text)

    def test_heading_is_inside_section_2(self):
        self.assertIn(TABLE_HEADING, self.section_2)

    def test_heading_appears_after_decision_matrix_and_before_model_card_worked_example(self):
        decision_matrix_pos = self.section_2.index(DECISION_MATRIX_HEADING)
        table_pos = self.section_2.index(TABLE_HEADING)
        model_card_pos = self.section_2.index(MODEL_CARD_HEADING)
        self.assertLess(decision_matrix_pos, table_pos)
        self.assertLess(table_pos, model_card_pos)

    def _matrix_subsection(self):
        start = self.section_2.index(TABLE_HEADING)
        end = self.section_2.index(MODEL_CARD_HEADING)
        return self.section_2[start:end]

    def test_table_has_required_columns(self):
        subsection = self._matrix_subsection()
        self.assertRegex(subsection, r"\|\s*-{2,}\s*\|")
        for column in REQUIRED_COLUMNS:
            with self.subTest(column=column):
                self.assertIn(column, subsection)

    def test_table_covers_all_five_frameworks(self):
        subsection = self._matrix_subsection()
        table_lines = [
            line for line in subsection.splitlines() if line.strip().startswith("|")
        ]
        table_text = "\n".join(table_lines)
        for framework in REQUIRED_FRAMEWORKS:
            with self.subTest(framework=framework):
                self.assertIn(framework, table_text)

    def test_table_has_one_row_per_framework(self):
        subsection = self._matrix_subsection()
        table_lines = [
            line
            for line in subsection.splitlines()
            if line.strip().startswith("|") and "---" not in line
        ]
        # header row + 5 framework rows
        self.assertEqual(len(table_lines), 1 + len(REQUIRED_FRAMEWORKS))

    def test_section_has_an_exam_tip(self):
        subsection = self._matrix_subsection()
        self.assertIn("Exam tip:", subsection)

    def test_toc_links_to_the_new_subsection(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(
            "[Compliance framework requirements comparison matrix]"
            "(#compliance-framework-requirements-comparison-matrix)",
            toc,
        )


if __name__ == "__main__":
    unittest.main()
