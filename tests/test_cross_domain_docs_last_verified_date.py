"""Regression test: cross-domain support docs must record a 'Last verified'
date and a recommended re-verification cadence.

The gap this covers: all five domain guides and aws-service-decision-guide.md
carry a 'Last verified: YYYY-MM-DD' checkpoint (see
tests/test_domain_last_verified_date.py), but several cross-domain support
files did not, even though they reference AWS services, model families, and
compliance details (HIPAA/BAA, Bedrock features, model names) that go stale
just as fast:

- docs/cross-domain-scenario-questions.md
- docs/cross-domain-concept-map.md
- docs/case-study-ai-system-lifecycle.md
- docs/master-glossary.md
- docs/GLOSSARY.md

This test encodes the invariant so a future edit that drops the date (or the
cadence note) from one of these files fails fast, locally.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

# Each file, paired with the minimum re-verification cadence (in days) the
# task requires it to state.
FILES_AND_CADENCE_DAYS = {
    "cross-domain-scenario-questions.md": 60,
    "cross-domain-concept-map.md": 90,
    "case-study-ai-system-lifecycle.md": 90,
    "master-glossary.md": 60,
    "GLOSSARY.md": 60,
}

LAST_VERIFIED_RE = re.compile(r"\*\*Last verified:\*\*\s*\d{4}-\d{2}-\d{2}")


def _read(path):
    return path.read_text(encoding="utf-8")


class TestCrossDomainDocsLastVerifiedDate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {
            fname: _read(DOCS_DIR / fname) for fname in FILES_AND_CADENCE_DAYS
        }

    def test_every_file_has_a_last_verified_date(self):
        for fname, text in self.texts.items():
            with self.subTest(file=fname):
                self.assertRegex(
                    text,
                    LAST_VERIFIED_RE,
                    f"{fname} is missing a '**Last verified:** YYYY-MM-DD' line",
                )

    def test_last_verified_date_appears_directly_under_the_title(self):
        # The line must sit right under the '# Title' heading -- the first
        # non-blank line after the title, before any other prose -- so a
        # reader sees freshness info before anything else.
        for fname, text in self.texts.items():
            with self.subTest(file=fname):
                lines = text.splitlines()
                self.assertTrue(lines[0].startswith("# "), f"{fname} should start with a title heading")
                # Skip the title and any single blank line that follows it.
                idx = 1
                while idx < len(lines) and lines[idx].strip() == "":
                    idx += 1
                self.assertRegex(
                    lines[idx],
                    LAST_VERIFIED_RE,
                    f"{fname}'s 'Last verified' line should be the first "
                    "content directly under the title heading",
                )

    def test_states_the_required_re_verification_cadence(self):
        for fname, cadence_days in FILES_AND_CADENCE_DAYS.items():
            with self.subTest(file=fname):
                text = self.texts[fname]
                self.assertIn(
                    f"every {cadence_days} days",
                    text,
                    f"{fname} should note a recommended re-verification "
                    f"cadence of every {cadence_days} days",
                )


if __name__ == "__main__":
    unittest.main()
