"""Structural validation for the "Three-tier learning structure" section of
README.md.

The gap this covers: README.md enumerated the five domains and their full
study guide paths but said nothing about the Fast Track (~40%-length
condensed guides) or Ultra Fast Learn (~15%-length cram sheets) that exist
for all five domains under docs/domain-N-fast-track/, even though
docs/study-progress-tracker.md already treats them as first-class study
materials. This test asserts README.md has a "Three-tier learning
structure" section, placed immediately after "Exam domains", that:

  * explains all three tiers (full guide, Fast Track, Ultra Fast Learn),
  * states the coverage guarantee (every testable concept retained across
    tiers, only narrative/redundant examples trimmed),
  * gives concrete "already know it -> start with Fast Track" guidance,
  * links to a real Fast Track / Ultra Fast Learn entry point, and
  * points to docs/study-progress-tracker.md as already tracking these
    tiers as valid study materials.

Mirrors the conventions established in tests/test_readme_study_plan.py.

Run with:
    python3 -m unittest tests/test_readme_three_tier_learning_structure.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
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


class TestReadmeHasThreeTierSection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme_text = _read(README_PATH)
        cls.section = _section_text(
            cls.readme_text, "Three-tier learning structure"
        )

    def test_section_exists(self):
        self.assertIsNotNone(
            self.section,
            "README.md must have a '## Three-tier learning structure' "
            "section",
        )

    def test_section_is_placed_immediately_after_exam_domains(self):
        # The section should appear right after "## Exam domains" and
        # before "## Study plan", so it's visible before any other
        # narrative section.
        exam_domains_idx = self.readme_text.find("## Exam domains")
        three_tier_idx = self.readme_text.find(
            "## Three-tier learning structure"
        )
        study_plan_idx = self.readme_text.find("## Study plan")

        self.assertNotEqual(exam_domains_idx, -1)
        self.assertNotEqual(three_tier_idx, -1)
        self.assertNotEqual(study_plan_idx, -1)
        self.assertTrue(
            exam_domains_idx < three_tier_idx < study_plan_idx,
            "Three-tier learning structure section must come immediately "
            "after Exam domains and before Study plan",
        )

    def test_explains_full_guide_tier(self):
        self.assertRegex(
            self.section,
            re.compile(r"full[^.\n]*guide", re.IGNORECASE),
            "section must describe the full domain guide tier",
        )

    def test_explains_fast_track_tier(self):
        self.assertRegex(
            self.section,
            re.compile(r"Fast Track(?:(?!\.\s).)*40%", re.IGNORECASE | re.DOTALL),
            "section must describe Fast Track as the ~40%-length tier",
        )

    def test_explains_ultra_fast_learn_tier(self):
        self.assertRegex(
            self.section,
            re.compile(
                r"Ultra Fast Learn(?:(?!\.\s).)*15%", re.IGNORECASE | re.DOTALL
            ),
            "section must describe Ultra Fast Learn as the ~15%-length "
            "tier",
        )

    def test_states_coverage_guarantee(self):
        self.assertRegex(
            self.section,
            re.compile(r"every testable concept", re.IGNORECASE),
            "section must state the coverage guarantee that every "
            "testable concept is retained across tiers",
        )

    def test_gives_concrete_fast_track_guidance(self):
        self.assertRegex(
            self.section,
            re.compile(
                r"already know(?:(?!\.\s).)*Domain 1(?:(?!\.\s).)*Fast Track",
                re.IGNORECASE | re.DOTALL,
            ),
            "section must give concrete guidance like 'if you already "
            "know Domain 1 fundamentals, start with the Fast Track'",
        )

    def test_mentions_study_progress_tracker(self):
        self.assertIn(
            "docs/study-progress-tracker.md",
            self.section,
            "section must point to docs/study-progress-tracker.md as "
            "already tracking Fast Track / Ultra Fast Learn materials",
        )


class TestReadmeThreeTierLinksResolve(unittest.TestCase):
    """The three-tier section links to real Fast Track / Ultra Fast Learn
    entry points; verify those links actually resolve to files on disk."""

    @classmethod
    def setUpClass(cls):
        cls.readme_text = _read(README_PATH)
        cls.section = (
            _section_text(cls.readme_text, "Three-tier learning structure")
            or ""
        )
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
            "expected the section to link into docs/",
        )

    def test_links_to_a_fast_track_entry_point(self):
        self.assertTrue(
            any("fast-track" in link for link in self.internal_links),
            "expected at least one link into a docs/domain-N-fast-track/ "
            "entry point",
        )

    def test_links_to_ultra_fast_learn_entry_point(self):
        self.assertTrue(
            any("ULTRA-FAST-LEARN.md" in link for link in self.internal_links),
            "expected at least one link to an ULTRA-FAST-LEARN.md cram "
            "sheet",
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
                    f"{file_part} -- the README three-tier link is stale",
                )


if __name__ == "__main__":
    unittest.main()
