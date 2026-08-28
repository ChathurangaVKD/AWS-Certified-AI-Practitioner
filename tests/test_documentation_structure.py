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


if __name__ == "__main__":
    unittest.main()
