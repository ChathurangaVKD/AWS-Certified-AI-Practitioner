"""Regression tests for the domain guides' breadcrumb/footer navigation.

The gap this covers: a past autopilot implementation diff added the
"[← ...] · **Domain N of 5** · [... →]" breadcrumb/footer navigation line
to Domain 1 and Domain 2 but left Domains 3-5 without it, which the
code_review pipeline stage caught and rejected -- costing a full failed
pipeline run because nothing in this repo mechanically enforced the
invariant. This test encodes that invariant directly so a future diff
that repeats the same partial edit fails fast, locally, instead of
depending on an LLM reviewer catching it after the fact.

Each domain guide must carry the identical navigation line in two
places: immediately below the H1 title (the breadcrumb) and as the very
last line of the file, right after the closing "---" divider (the
footer). The line must link back to the previous domain guide (or
../README.md for Domain 1) and forward to the next domain guide (or
../README.md for Domain 5), and must state "**Domain N of 5**" for the
correct N.

Run with:
    python3 -m unittest tests/test_domain_footer_navigation.py -v
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

NAV_LINE_RE = re.compile(
    r"\[← [^\]]+\]\((?P<back>[^)]+)\)"
    r"\s*·\s*\*\*Domain (?P<num>\d) of 5\*\*\s*·\s*"
    r"\[[^\]]+ →\]\((?P<forward>[^)]+)\)"
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _expected_back_target(domain_number):
    if domain_number == 1:
        return "../README.md"
    return DOMAIN_FILENAMES[domain_number - 1]


def _expected_forward_target(domain_number):
    if domain_number == 5:
        return "../README.md"
    return DOMAIN_FILENAMES[domain_number + 1]


class TestDomainFooterNavigation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {n: _read(p) for n, p in DOMAIN_FILES.items()}

    def test_every_domain_has_a_breadcrumb_nav_line_matching_its_position(self):
        for domain_number, text in self.texts.items():
            with self.subTest(domain=domain_number):
                match = NAV_LINE_RE.search(text)
                self.assertIsNotNone(
                    match,
                    f"domain {domain_number} guide is missing the "
                    "'[← ...] · **Domain N of 5** · [... →]' navigation line",
                )
                self.assertEqual(int(match.group("num")), domain_number)
                self.assertEqual(
                    match.group("back"), _expected_back_target(domain_number)
                )
                self.assertEqual(
                    match.group("forward"),
                    _expected_forward_target(domain_number),
                )

    def test_every_domain_footer_repeats_the_same_nav_line_at_the_end(self):
        for domain_number, text in self.texts.items():
            with self.subTest(domain=domain_number):
                stripped = text.rstrip("\n")
                lines = stripped.splitlines()
                self.assertGreaterEqual(
                    len(lines), 2,
                    f"domain {domain_number} guide is too short to contain "
                    "a footer divider and navigation line",
                )
                footer_line = lines[-1]
                divider_line = next(
                    (l for l in reversed(lines[:-1]) if l.strip()), ""
                )
                self.assertEqual(
                    divider_line.strip(),
                    "---",
                    f"domain {domain_number} guide's footer navigation "
                    "line should be immediately preceded by a '---' "
                    f"divider (last non-blank line before it was "
                    f"{divider_line!r})",
                )
                footer_match = NAV_LINE_RE.search(footer_line)
                self.assertIsNotNone(
                    footer_match,
                    f"domain {domain_number} guide's last line does not "
                    "contain the footer navigation "
                    "('[← ...] · **Domain N of 5** · [... →]') -- footer "
                    "navigation is missing",
                )
                self.assertEqual(int(footer_match.group("num")), domain_number)
                self.assertEqual(
                    footer_match.group("back"),
                    _expected_back_target(domain_number),
                )
                self.assertEqual(
                    footer_match.group("forward"),
                    _expected_forward_target(domain_number),
                )


if __name__ == "__main__":
    unittest.main()
