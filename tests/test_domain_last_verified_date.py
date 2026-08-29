"""Regression test: each domain guide must record a 'Last verified' date.

The gap this covers: aws-service-decision-guide.md carries a
'Last verified: YYYY-MM-DD' checkpoint, but none of the five domain guides
did, even though DOCUMENTATION_STRUCTURE.md claims the series is "kept
current." This test encodes the invariant so a future edit that adds the
line to only some domain guides fails fast, locally.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

DOMAIN_FILENAMES = {
    1: "domain-1-fundamentals-of-ai-and-ml.md",
    2: "domain-2-fundamentals-of-generative-ai.md",
    3: "domain-3-applications-of-foundation-models.md",
    4: "domain-4-guidelines-for-responsible-ai.md",
    5: "domain-5-security-compliance-governance.md",
}
DOMAIN_FILES = {n: DOCS_DIR / fname for n, fname in DOMAIN_FILENAMES.items()}

LAST_VERIFIED_RE = re.compile(r"\*\*Last verified:\*\*\s*\d{4}-\d{2}-\d{2}")


class TestDomainLastVerifiedDate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {n: p.read_text(encoding="utf-8") for n, p in DOMAIN_FILES.items()}

    def test_every_domain_guide_has_a_last_verified_date(self):
        for domain_number, text in self.texts.items():
            with self.subTest(domain=domain_number):
                self.assertRegex(
                    text,
                    LAST_VERIFIED_RE,
                    f"domain {domain_number} guide is missing a "
                    "'**Last verified:** YYYY-MM-DD' line",
                )

    def test_last_verified_date_appears_near_the_top(self):
        # Freshness info is only useful if a reader sees it before the
        # table of contents / body, not buried deep in the document.
        for domain_number, text in self.texts.items():
            with self.subTest(domain=domain_number):
                match = LAST_VERIFIED_RE.search(text)
                self.assertIsNotNone(match)
                toc_match = re.search(r"^## Table of contents", text, re.M)
                self.assertIsNotNone(toc_match)
                self.assertLess(
                    match.start(),
                    toc_match.start(),
                    f"domain {domain_number} guide's 'Last verified' line "
                    "should appear before the Table of contents",
                )


if __name__ == "__main__":
    unittest.main()
