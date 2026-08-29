"""Regression tests for docs/DOCUMENTATION_STRUCTURE.md staying in sync with
the files it describes.

The gap this covers: DOCUMENTATION_STRUCTURE.md records prose metadata
about the repo's own content -- per-domain line counts and a list of the
cross-domain support files -- that nothing enforced, so it silently drifted
out of date as the domain guides grew and new supporting files (like
cross-domain-scenario-questions.md) were added. This test asserts:

  * every line count for a domain guide stated in DOCUMENTATION_STRUCTURE.md
    matches that file's actual current line count, and
  * cross-domain-scenario-questions.md is documented alongside the repo's
    other cross-domain support materials.

Run with:
    python3 -m unittest tests/test_documentation_structure.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
STRUCTURE_DOC = DOCS_DIR / "DOCUMENTATION_STRUCTURE.md"

DOMAIN_FILES = {
    1: DOCS_DIR / "domain-1-fundamentals-of-ai-and-ml.md",
    2: DOCS_DIR / "domain-2-fundamentals-of-generative-ai.md",
    3: DOCS_DIR / "domain-3-applications-of-foundation-models.md",
    4: DOCS_DIR / "domain-4-guidelines-for-responsible-ai.md",
    5: DOCS_DIR / "domain-5-security-compliance-governance.md",
}

CROSS_DOMAIN_SUPPORT_FILES = [
    "cross-domain-scenario-questions.md",
    "cross-domain-concept-map.md",
    "case-study-ai-system-lifecycle.md",
    "exam-preparation-strategy.md",
    "full-length-mock-exam.md",
    "aws-service-decision-guide.md",
    "master-glossary.md",
]


def _line_count(path):
    text = path.read_text(encoding="utf-8")
    # Match `wc -l`: count newline characters.
    return text.count("\n")


class TestDocumentationStructureLineCounts(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md states an exact line count per domain
    guide (e.g. "Domain 1: 1,118 lines"); each must match reality so the
    doc doesn't silently go stale as guides grow."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def test_stated_domain_line_counts_match_actual_files(self):
        for domain_number, path in DOMAIN_FILES.items():
            actual = _line_count(path)
            formatted = f"{actual:,}"
            with self.subTest(domain=domain_number):
                self.assertIn(
                    f"Domain {domain_number}: {formatted} lines",
                    self.structure_text,
                    f"DOCUMENTATION_STRUCTURE.md does not state the "
                    f"current line count ({formatted}) for domain "
                    f"{domain_number}'s guide ({path.name}) -- it has "
                    "gone stale or the file was edited without updating "
                    "the recorded count",
                )

    def test_no_stale_domain_line_count_figures(self):
        """Guard against an old, now-wrong count lingering alongside (or
        instead of) the correct one."""
        stated_counts = {
            int(n): int(c.replace(",", ""))
            for n, c in re.findall(
                r"Domain (\d): ([\d,]+) lines", self.structure_text
            )
        }
        self.assertEqual(set(stated_counts), set(DOMAIN_FILES))
        for domain_number, stated in stated_counts.items():
            actual = _line_count(DOMAIN_FILES[domain_number])
            with self.subTest(domain=domain_number):
                self.assertEqual(
                    stated,
                    actual,
                    f"DOCUMENTATION_STRUCTURE.md states {stated} lines for "
                    f"domain {domain_number}, but the file actually has "
                    f"{actual} lines",
                )


class TestDocumentationStructureCrossDomainMaterials(unittest.TestCase):
    """cross-domain-scenario-questions.md must be documented alongside the
    repo's other cross-domain support materials."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def test_cross_domain_scenario_questions_mentioned(self):
        self.assertIn(
            "cross-domain-scenario-questions.md",
            self.structure_text,
            "DOCUMENTATION_STRUCTURE.md does not mention "
            "cross-domain-scenario-questions.md",
        )

    def test_cross_domain_support_files_all_exist(self):
        # Sanity check the fixture list itself stays valid.
        for filename in CROSS_DOMAIN_SUPPORT_FILES:
            with self.subTest(filename=filename):
                self.assertTrue((DOCS_DIR / filename).is_file())

    def test_cross_domain_scenario_questions_listed_with_siblings(self):
        """The entry describing cross-domain-scenario-questions.md should
        sit alongside mentions of the repo's other cross-domain support
        files, not stand alone."""
        idx = self.structure_text.find("cross-domain-scenario-questions.md")
        self.assertNotEqual(idx, -1)
        # Look at the surrounding paragraph (a generous window) for the
        # other known cross-domain support filenames.
        window = self.structure_text[max(0, idx - 500) : idx + 1000]
        siblings = [
            f
            for f in CROSS_DOMAIN_SUPPORT_FILES
            if f != "cross-domain-scenario-questions.md"
        ]
        mentioned = [f for f in siblings if f in window]
        self.assertGreaterEqual(
            len(mentioned),
            3,
            "expected cross-domain-scenario-questions.md's entry in "
            "DOCUMENTATION_STRUCTURE.md to be near mentions of the other "
            f"cross-domain support materials, found only {mentioned}",
        )


class TestDocumentationStructureDomain5Accuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously described Domain 5 as lacking
    a test file, multiple-response questions, and a worked example section,
    and described every domain's diagrams as ASCII art. All four claims are
    now false -- these tests guard against the doc drifting back to them."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.domain_5_text = DOMAIN_FILES[5].read_text(encoding="utf-8")

    def test_domain_5_test_file_exists(self):
        test_file = REPO_ROOT / "tests" / "test_domain_5_study_guide.py"
        self.assertTrue(
            test_file.is_file(),
            "tests/test_domain_5_study_guide.py should exist",
        )

    def test_structure_doc_does_not_claim_domain_5_lacks_a_test_file(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("domain 5 has no", lowered)
        self.assertNotIn("d5 lacks test file", lowered)
        self.assertNotIn("test_domain_5_study_guide.py` is missing", lowered)
        self.assertNotIn("test_domain_5_study_guide.py` file; domains 1", lowered)

    def test_structure_doc_documents_validation_tests_for_all_five_domains(self):
        self.assertIn(
            "`tests/test_domain_N_study_guide.py` for all five domains",
            self.structure_text,
        )

    def test_domain_5_has_multiple_response_questions(self):
        self.assertEqual(
            self.domain_5_text.count("(Multiple response — select TWO)"),
            2,
            "expected exactly 2 multiple-response questions (Q3 and Q14) "
            "in the Domain 5 guide",
        )

    def test_structure_doc_documents_domain_5_multiple_response_questions(self):
        self.assertIn("multiple-response", self.structure_text.lower())
        self.assertIn("Domain 5", self.structure_text)
        # The sentence documenting this fact should reference Domain 5.
        idx = self.structure_text.lower().find("multiple-response")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[max(0, idx - 200) : idx + 200]
        self.assertIn("Domain 5", window)

    def test_domain_5_has_worked_example_section(self):
        self.assertIn(
            "## Worked example: securing and governing a HIPAA-regulated "
            "Bedrock application",
            self.domain_5_text,
        )

    def test_structure_doc_documents_domain_5_worked_example(self):
        self.assertIn("Worked example", self.structure_text)
        idx = self.structure_text.find("Worked examples")
        self.assertNotEqual(
            idx, -1, "expected a 'Worked examples' entry in DOCUMENTATION_STRUCTURE.md"
        )
        window = self.structure_text[idx : idx + 500]
        self.assertIn("D5", window)

    def test_structure_doc_describes_flowcharts_as_mermaid_not_ascii(self):
        diagrams_idx = self.structure_text.find("**Diagrams:**")
        self.assertNotEqual(diagrams_idx, -1)
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 800]
        self.assertIn("Mermaid flowchart", diagrams_section)
        self.assertIn("13", diagrams_section)


class TestDocumentationStructureDomain4Accuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously claimed Domain 4 has no
    worked-example section and that only Domains 1-3 and 5 have one, and
    that all five domains use a uniform 15-20 practice question count.
    Domain 4 actually has a worked example ("## Worked example: auditing
    and documenting a responsible e-commerce recommendation engine") and
    Domain 5 actually has 26 practice questions, not 15-20. These tests
    guard against the doc drifting back to those stale claims."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.domain_4_text = DOMAIN_FILES[4].read_text(encoding="utf-8")
        cls.domain_5_text = DOMAIN_FILES[5].read_text(encoding="utf-8")

    def test_domain_4_has_worked_example_section(self):
        self.assertIn(
            "## Worked example: auditing and documenting a responsible "
            "e-commerce recommendation engine",
            self.domain_4_text,
        )

    def test_structure_doc_does_not_claim_domain_4_lacks_a_worked_example(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("domain 4 has no worked-example section", lowered)

    def test_structure_doc_documents_domain_4_worked_example(self):
        idx = self.structure_text.find("Worked examples")
        self.assertNotEqual(
            idx, -1, "expected a 'Worked examples' entry in DOCUMENTATION_STRUCTURE.md"
        )
        window = self.structure_text[idx : idx + 500]
        self.assertIn("Domains 1, 2, 3, 4, and 5", window)
        self.assertIn("D4", window)

    def test_domain_5_actual_practice_question_count(self):
        questions_section_match = re.search(
            r"\n## Practice questions(.*?)\n## Answer key",
            self.domain_5_text,
            re.DOTALL,
        )
        self.assertIsNotNone(questions_section_match)
        numbers = re.findall(
            r"(?m)^(\d+)\.\s", questions_section_match.group(1)
        )
        self.assertEqual(
            len(numbers),
            26,
            "expected Domain 5 to currently have 26 practice questions",
        )

    def test_structure_doc_documents_domain_5s_26_practice_questions(self):
        self.assertIn("26", self.structure_text)
        idx = self.structure_text.find("15–20 per domain")
        self.assertNotEqual(
            idx,
            -1,
            "expected DOCUMENTATION_STRUCTURE.md to describe the 15-20 "
            "per-domain practice question norm",
        )
        window = self.structure_text[idx : idx + 200]
        self.assertIn("26", window)
        self.assertIn("Domain 5", window)


if __name__ == "__main__":
    unittest.main()
