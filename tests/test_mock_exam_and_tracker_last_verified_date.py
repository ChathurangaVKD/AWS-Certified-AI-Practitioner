"""Regression test: the mock-exam and study-progress-tracker docs must
record a 'Last verified' date.

The gap this covers: every other cross-domain support file
(master-glossary.md, GLOSSARY.md, cross-domain-concept-map.md,
cross-domain-scenario-questions.md, case-study-ai-system-lifecycle.md,
exam-preparation-strategy.md -- see
tests/test_cross_domain_docs_last_verified_date.py) carries a header-level
'**Last verified:** YYYY-MM-DD' line, but these three files did not, even
though they reference the same fast-changing AWS services and exam
content:

- docs/mock-exam.md
- docs/full-length-mock-exam.md
- docs/study-progress-tracker.md

This test encodes the invariant so a future edit that drops the date from
one of these files fails fast, locally.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

FILENAMES = [
    "mock-exam.md",
    "full-length-mock-exam.md",
    "study-progress-tracker.md",
]

LAST_VERIFIED_RE = re.compile(r"\*\*Last verified:\*\*\s*\d{4}-\d{2}-\d{2}")


def _read(path):
    return path.read_text(encoding="utf-8")


class TestMockExamAndTrackerLastVerifiedDate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {fname: _read(DOCS_DIR / fname) for fname in FILENAMES}

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
                self.assertTrue(
                    lines[0].startswith("# "), f"{fname} should start with a title heading"
                )
                idx = 1
                while idx < len(lines) and lines[idx].strip() == "":
                    idx += 1
                self.assertRegex(
                    lines[idx],
                    LAST_VERIFIED_RE,
                    f"{fname}'s 'Last verified' line should be the first "
                    "content directly under the title heading",
                )

    def test_last_verified_line_is_a_standalone_header_not_embedded_in_prose(self):
        # Unlike master-glossary.md's multi-line cadence paragraph, these
        # files should carry a single, standalone header line.
        for fname, text in self.texts.items():
            with self.subTest(file=fname):
                lines = text.splitlines()
                idx = 1
                while idx < len(lines) and lines[idx].strip() == "":
                    idx += 1
                line = lines[idx].strip()
                self.assertRegex(
                    line,
                    re.compile(r"^\*\*Last verified:\*\*\s*\d{4}-\d{2}-\d{2}$"),
                    f"{fname}'s 'Last verified' line should be a standalone "
                    f"header (got: {line!r})",
                )


if __name__ == "__main__":
    unittest.main()
