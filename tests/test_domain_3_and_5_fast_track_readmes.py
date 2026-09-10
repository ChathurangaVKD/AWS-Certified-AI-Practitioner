"""Structural validation for the Domain 3 and Domain 5 Fast Track landing
pages (docs/domain-3-fast-track/README.md and
docs/domain-5-fast-track/README.md).

The gap this covers: Domains 1, 2, and 4 each pair a single
domain-N-fast-track/README.md with an ULTRA-FAST-LEARN.md cram sheet, and
that README.md serves as the entry point/navigation hub for the domain's
condensed material. Domains 3 and 5 are the only Fast Track guides split
into multiple numbered parts (Domain 3: 3 parts; Domain 5: 2 parts) because
their source domains are longer, and until now their directories had no
equivalent landing page -- a reader arriving at either directory had to
infer from the part-1 file alone which part to start with, how many parts
exist, and where the cram sheet lives.

These tests assert that both landing pages exist and:

  * explain why the guide is split into multiple parts,
  * provide a table of contents linking to every part file and to
    ULTRA-FAST-LEARN.md,
  * carry the same "how to use this fast track" usage guidance already
    present in the part-1 files, and
  * carry a front-matter table mapping each section back to the
    corresponding full-guide line ranges,

and that every internal link out of each landing page resolves to a real
file and, if anchored, a real heading -- mirroring the conventions in
tests/test_domain_1_fast_track_guide.py and
tests/test_cross_reference_links.py.

Run with:
    python3 -m unittest tests/test_domain_3_and_5_fast_track_readmes.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")


def _read(path):
    return path.read_text(encoding="utf-8")


def _slugify(heading_text):
    """Approximate the GitHub markdown heading-anchor algorithm: lowercase,
    strip characters that aren't word characters/spaces/hyphens, then turn
    runs of whitespace into single hyphens. Matches the convention used by
    tests/test_cross_reference_links.py and the rest of this repo's link
    tests, which is also what every hand-authored link in this doc set was
    written against."""
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def _heading_anchors(doc_text):
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


# Per-domain fixture: the README landing page, its directory, the expected
# part files (in order), and the ULTRA-FAST-LEARN.md cram sheet.
FAST_TRACKS = {
    3: {
        "dir": DOCS_DIR / "domain-3-fast-track",
        "readme": DOCS_DIR / "domain-3-fast-track" / "README.md",
        "parts": [
            "part-1-application-design-and-customization.md",
            "part-2-inference-and-multimodal.md",
            "part-3-deployment-and-troubleshooting.md",
        ],
        "ultra": DOCS_DIR / "domain-3-fast-track" / "ULTRA-FAST-LEARN.md",
        "source": DOCS_DIR / "domain-3-applications-of-foundation-models.md",
        "heading_prefix": "# Domain 3 Fast Track",
    },
    5: {
        "dir": DOCS_DIR / "domain-5-fast-track",
        "readme": DOCS_DIR / "domain-5-fast-track" / "README.md",
        "parts": [
            "part-1-security-and-compliance.md",
            "part-2-governance-and-monitoring.md",
        ],
        "ultra": DOCS_DIR / "domain-5-fast-track" / "ULTRA-FAST-LEARN.md",
        "source": DOCS_DIR / "domain-5-security-compliance-governance.md",
        "heading_prefix": "# Domain 5 Fast Track",
    },
}


class TestFastTrackReadmesExist(unittest.TestCase):
    def test_readme_files_exist(self):
        for domain_number, fixture in FAST_TRACKS.items():
            with self.subTest(domain=domain_number):
                self.assertTrue(
                    fixture["readme"].is_file(),
                    f"expected {fixture['readme']} to exist as the "
                    f"Domain {domain_number} Fast Track landing page",
                )

    def test_part_files_and_ultra_fast_learn_still_exist(self):
        # Sanity check the fixture itself -- adding the README should not
        # remove or rename any pre-existing part file or cram sheet.
        for domain_number, fixture in FAST_TRACKS.items():
            for part_name in fixture["parts"]:
                with self.subTest(domain=domain_number, part=part_name):
                    self.assertTrue((fixture["dir"] / part_name).is_file())
            with self.subTest(domain=domain_number, part="ULTRA-FAST-LEARN.md"):
                self.assertTrue(fixture["ultra"].is_file())


class TestFastTrackReadmesStructure(unittest.TestCase):
    """Each landing page must have the right heading, explain the split,
    link to every part and the cram sheet from its table of contents, and
    carry the shared usage guidance."""

    @classmethod
    def setUpClass(cls):
        cls.texts = {n: _read(f["readme"]) for n, f in FAST_TRACKS.items()}

    def test_has_top_level_heading(self):
        for domain_number, fixture in FAST_TRACKS.items():
            with self.subTest(domain=domain_number):
                self.assertTrue(
                    self.texts[domain_number].startswith(fixture["heading_prefix"])
                )

    def test_links_back_to_full_guide(self):
        for domain_number, fixture in FAST_TRACKS.items():
            source_link = f"({'../' + fixture['source'].name})"
            with self.subTest(domain=domain_number):
                self.assertIn(source_link, self.texts[domain_number])

    def test_explains_why_split_into_multiple_parts(self):
        for domain_number in FAST_TRACKS:
            text = self.texts[domain_number]
            with self.subTest(domain=domain_number):
                self.assertRegex(
                    text,
                    re.compile(r"split into (two|three) parts", re.I),
                    "expected the landing page to explain why the fast "
                    "track is split into multiple parts",
                )

    def test_has_how_to_use_this_fast_track_section(self):
        for domain_number in FAST_TRACKS:
            with self.subTest(domain=domain_number):
                self.assertIn(
                    "\n## How to use this fast track\n", self.texts[domain_number]
                )

    def test_usage_section_mentions_reading_day_before_exam(self):
        # The same usage guidance already present in the part-1 files.
        for domain_number in FAST_TRACKS:
            text = self.texts[domain_number]
            with self.subTest(domain=domain_number):
                self.assertIn("day before the exam", text)
                self.assertIn("already know", text)

    def test_usage_section_tells_reader_to_read_full_guide_first_if_new(self):
        for domain_number in FAST_TRACKS:
            with self.subTest(domain=domain_number):
                self.assertRegex(
                    self.texts[domain_number],
                    re.compile(r"read the \[full\s+guide\]"),
                )

    def test_has_table_of_contents(self):
        for domain_number in FAST_TRACKS:
            with self.subTest(domain=domain_number):
                self.assertIn(
                    "\n## Table of contents\n", self.texts[domain_number]
                )

    def test_table_of_contents_links_every_part_and_ultra_fast_learn(self):
        for domain_number, fixture in FAST_TRACKS.items():
            text = self.texts[domain_number]
            toc_match = re.search(
                r"\n## Table of contents\n(.*?)\n## ", text, re.S
            )
            with self.subTest(domain=domain_number):
                self.assertIsNotNone(toc_match)
                toc = toc_match.group(1)
                for part_name in fixture["parts"]:
                    with self.subTest(part=part_name):
                        self.assertIn(f"]({part_name})", toc)
                self.assertIn("](ULTRA-FAST-LEARN.md)", toc)

    def test_has_front_matter_table_mapping_sections_to_full_guide_lines(self):
        for domain_number, fixture in FAST_TRACKS.items():
            text = self.texts[domain_number]
            with self.subTest(domain=domain_number):
                self.assertIn("Approx. full-guide lines", text)
                # At least one data row citing the full guide file with a
                # numeric line-range value (e.g. "98-353" or "58–92").
                self.assertRegex(
                    text,
                    re.compile(
                        re.escape(fixture["source"].name) + r"[^\n|]*\)\s*\|\s*[\d,]+"
                    ),
                )

    def test_front_matter_table_covers_every_part(self):
        # The combined table should cite every part number (1, 2, [3]).
        for domain_number, fixture in FAST_TRACKS.items():
            text = self.texts[domain_number]
            num_parts = len(fixture["parts"])
            for part_number in range(1, num_parts + 1):
                with self.subTest(domain=domain_number, part=part_number):
                    self.assertRegex(
                        text,
                        re.compile(rf"\|\s*{part_number}\s*\|"),
                        f"expected the front-matter table to have at least "
                        f"one row citing part {part_number}",
                    )


class TestFastTrackReadmesCrossReferencesResolve(unittest.TestCase):
    """Every internal link out of each landing page must resolve to a real
    file and, if anchored, a real heading in that file."""

    @classmethod
    def setUpClass(cls):
        cls.anchor_cache = {}

    def _links_for(self, readme_path):
        text = _read(readme_path)
        links = MD_LINK_RE.findall(text)
        return [
            link for link in links if not link.startswith(("http://", "https://"))
        ]

    def _resolve_target_path(self, readme_path, file_part):
        if file_part == "":
            return readme_path
        return (readme_path.parent / file_part).resolve()

    def test_has_several_internal_links(self):
        for domain_number, fixture in FAST_TRACKS.items():
            with self.subTest(domain=domain_number):
                links = self._links_for(fixture["readme"])
                self.assertGreaterEqual(len(links), 10)

    def test_every_internal_link_target_file_exists(self):
        for domain_number, fixture in FAST_TRACKS.items():
            readme_path = fixture["readme"]
            for link in self._links_for(readme_path):
                file_part = link.split("#", 1)[0]
                with self.subTest(domain=domain_number, link=link):
                    target_path = self._resolve_target_path(readme_path, file_part)
                    self.assertTrue(
                        target_path.is_file(),
                        f"linked file does not exist: {file_part!r} "
                        f"(resolved to {target_path}) in the Domain "
                        f"{domain_number} Fast Track README",
                    )

    def test_every_internal_anchor_matches_a_real_heading(self):
        for domain_number, fixture in FAST_TRACKS.items():
            readme_path = fixture["readme"]
            for link in self._links_for(readme_path):
                if "#" not in link:
                    continue
                file_part, anchor = link.split("#", 1)
                if not anchor:
                    continue
                with self.subTest(domain=domain_number, link=link):
                    target_path = self._resolve_target_path(readme_path, file_part)
                    cache_key = str(target_path)
                    if cache_key not in self.anchor_cache:
                        self.anchor_cache[cache_key] = _heading_anchors(
                            _read(target_path)
                        )
                    self.assertIn(
                        anchor,
                        self.anchor_cache[cache_key],
                        f"anchor #{anchor} does not match any heading slug "
                        f"in {target_path} -- the link {link!r} in the "
                        f"Domain {domain_number} Fast Track README is stale",
                    )


if __name__ == "__main__":
    unittest.main()
