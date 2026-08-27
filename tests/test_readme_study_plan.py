"""Structural validation for the "Study plan" section of README.md.

The gap this covers: README.md lists the five exam domains in a table but
previously gave no recommended reading order or prerequisite guidance, so a
reader landing on Domain 5 first had no signal to read Domains 1-4 first.
This test asserts README.md has a "Study plan" section that:

  * recommends the 1 -> 2 -> 3 -> 4 -> 5 reading order,
  * calls out Domain 1 as foundational,
  * notes that Domains 2-3 assume Domain 1 knowledge, and
  * links to the deeper reading-order discussion in
    docs/exam-preparation-strategy.md with an anchor that actually
    resolves to a real heading, so the pointer doesn't go stale.

Mirrors the conventions established in tests/test_cross_domain_concept_map.py.

Run with:
    python3 -m unittest tests/test_readme_study_plan.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
README_PATH = REPO_ROOT / "README.md"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")


def _read(path):
    return path.read_text(encoding="utf-8")


def _slugify(heading_text):
    """Approximate the GitHub markdown heading-anchor algorithm: lowercase,
    strip characters that aren't word characters/spaces/hyphens, then turn
    runs of whitespace into single hyphens."""
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def _heading_anchors(doc_text):
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


def _section_text(readme_text, heading):
    """Return the body of a '## <heading>' section, up to the next '## '."""
    pattern = re.compile(
        r"^## " + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)",
        re.M | re.S,
    )
    match = pattern.search(readme_text)
    return match.group(1) if match else None


class TestReadmeHasStudyPlanSection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme_text = _read(README_PATH)
        cls.section = _section_text(cls.readme_text, "Study plan")

    def test_study_plan_section_exists(self):
        self.assertIsNotNone(
            self.section,
            "README.md must have a '## Study plan' section",
        )

    def test_recommends_domains_in_numeric_order(self):
        # Look for the domains appearing in strict 1 -> 2 -> 3 -> 4 -> 5
        # order somewhere in the section (allowing arrows or other
        # connective text between the numbers).
        positions = [
            self.section.find(f"Domain {n}") for n in range(1, 6)
        ]
        self.assertTrue(
            all(p != -1 for p in positions),
            f"expected all five domains to be mentioned by name, got "
            f"positions {positions}",
        )
        self.assertEqual(
            positions,
            sorted(positions),
            "domains must be recommended in numeric reading order "
            "(1 -> 2 -> 3 -> 4 -> 5)",
        )

    def test_domain_1_called_out_as_foundational(self):
        self.assertRegex(
            self.section,
            re.compile(r"Domain 1[^.\n]*foundational", re.IGNORECASE),
            "Study plan section must call out Domain 1 as foundational",
        )

    def test_domains_2_and_3_note_domain_1_prerequisite(self):
        self.assertRegex(
            self.section,
            re.compile(
                r"Domains 2 and 3[^.\n]*(assume|require|build on)"
                r"[^.\n]*Domain 1",
                re.IGNORECASE,
            ),
            "Study plan section must note that Domains 2-3 assume "
            "Domain 1 knowledge",
        )

    def test_links_to_exam_preparation_strategy(self):
        self.assertIn(
            "docs/exam-preparation-strategy.md",
            self.section,
            "Study plan section should point to the deeper "
            "exam-preparation-strategy.md guide",
        )


class TestReadmeStudyPlanLinksResolve(unittest.TestCase):
    """The study plan section links into docs/exam-preparation-strategy.md
    with an anchor; verify that link actually resolves so the pointer
    can't silently go stale if the target doc's headings change."""

    @classmethod
    def setUpClass(cls):
        cls.readme_text = _read(README_PATH)
        cls.section = _section_text(cls.readme_text, "Study plan") or ""
        cls.links = MD_LINK_RE.findall(cls.section)
        cls.internal_links = [
            link
            for link in cls.links
            if not link.startswith(("http://", "https://", "#"))
        ]

    def test_found_at_least_one_internal_link(self):
        self.assertGreaterEqual(
            len(self.internal_links),
            1,
            "expected the Study plan section to link into docs/",
        )

    def test_every_internal_link_target_file_exists(self):
        for link in self.internal_links:
            file_part = link.split("#", 1)[0]
            with self.subTest(link=link):
                target_path = (REPO_ROOT / file_part).resolve()
                self.assertTrue(
                    target_path.is_file(),
                    f"linked file does not exist: {file_part!r} "
                    f"(resolved to {target_path})",
                )

    def test_every_internal_anchor_matches_a_real_heading(self):
        anchor_cache = {}
        for link in self.internal_links:
            if "#" not in link:
                continue
            file_part, anchor = link.split("#", 1)
            with self.subTest(link=link):
                if file_part not in anchor_cache:
                    target_path = (REPO_ROOT / file_part).resolve()
                    anchor_cache[file_part] = _heading_anchors(
                        _read(target_path)
                    )
                self.assertIn(
                    anchor,
                    anchor_cache[file_part],
                    f"anchor #{anchor} does not match any heading slug in "
                    f"{file_part} -- the README study plan link is stale",
                )


if __name__ == "__main__":
    unittest.main()
