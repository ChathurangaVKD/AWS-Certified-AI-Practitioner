"""Structural validation for docs/case-study-ai-system-lifecycle.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. The case study exists to walk one
fictional company's AI system through all five exam domains, so what
matters most here is that it is actually reachable from README.md, that it
covers every domain, and that every markdown link it makes into a domain
guide resolves to a real file and a real heading in that file. A future
edit that renames a heading in a domain doc (breaking an anchor link) or
removes the README pointer would otherwise go unnoticed since nothing
renders these docs in CI.

Mirrors the conventions established in
tests/test_cross_domain_concept_map.py.

Run with:
    python3 -m unittest tests/test_case_study_ai_system_lifecycle.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "case-study-ai-system-lifecycle.md"
README_PATH = REPO_ROOT / "README.md"

# Every domain guide the task requires this case study to walk through, in
# order, since it must span all five exam domains for a single company.
REQUIRED_DOMAIN_FILES = [
    "domain-1-fundamentals-of-ai-and-ml.md",
    "domain-2-fundamentals-of-generative-ai.md",
    "domain-3-applications-of-foundation-models.md",
    "domain-4-guidelines-for-responsible-ai.md",
    "domain-5-security-compliance-governance.md",
]

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
    """Return the set of anchor slugs for every heading in a markdown doc."""
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


class TestCaseStudyExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected end-to-end case study at {DOC_PATH}",
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/case-study-ai-system-lifecycle.md",
            readme_text,
            "README.md must link to the end-to-end case study so learners "
            "can discover it",
        )


class TestCaseStudyCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def test_has_title(self):
        self.assertRegex(self.text, r"^# Case Study")

    def test_follows_a_single_company_throughout(self):
        # The whole point of a case study (vs. the one-off "AWS example"
        # scenarios already in each domain doc) is a single, named company
        # threaded through every phase -- assert its name recurs
        # substantially rather than appearing once in an intro paragraph.
        company_mentions = len(re.findall(r"Solstice", self.text))
        self.assertGreaterEqual(
            company_mentions,
            5,
            "expected the same company to recur across the case study, "
            "not just be introduced once",
        )

    def test_links_into_every_domain_in_order(self):
        positions = []
        for domain_file in REQUIRED_DOMAIN_FILES:
            with self.subTest(domain=domain_file):
                self.assertIn(
                    domain_file,
                    self.text,
                    f"case study does not link into {domain_file}",
                )
                positions.append(self.text.index(domain_file))
        self.assertEqual(
            positions,
            sorted(positions),
            "case study should walk the five domains in order (D1 -> D5)",
        )

    def test_has_a_phase_section_per_domain(self):
        # Each domain gets its own "## Phase N (Domain N): ..." section.
        phase_headings = re.findall(r"^## Phase \d+ \(Domain \d+\)", self.text, re.M)
        self.assertEqual(
            len(phase_headings),
            len(REQUIRED_DOMAIN_FILES),
            "expected exactly one top-level phase section per exam domain",
        )

    def test_has_a_summary_table_covering_all_five_phases(self):
        # A markdown table needs a header separator row like |---|---|---|
        table_rows = re.findall(r"\|\s*-{2,}\s*\|", self.text)
        self.assertGreaterEqual(
            len(table_rows),
            1,
            "expected a summary table mapping phases to domains",
        )
        for domain_file in REQUIRED_DOMAIN_FILES:
            with self.subTest(domain=domain_file):
                self.assertIn(domain_file, self.text)


class TestCaseStudyLinksResolve(unittest.TestCase):
    """The case study's value depends on its links back into the domain
    guides being correct. Verify every relative markdown link (optionally
    with a #anchor) points at a real file, and that the anchor -- if
    present -- matches a real heading in that file."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.links = MD_LINK_RE.findall(cls.text)
        cls.internal_links = [
            link
            for link in cls.links
            if not link.startswith(("http://", "https://", "#"))
        ]

    def test_found_a_substantial_number_of_internal_links(self):
        # Sanity check that the regex above is actually matching the
        # document's link syntax, so the resolution tests below aren't
        # silently vacuous.
        self.assertGreaterEqual(
            len(self.internal_links),
            15,
            "expected many internal links from the case study into the "
            "domain guides",
        )

    def test_every_internal_link_target_file_exists(self):
        for link in self.internal_links:
            file_part = link.split("#", 1)[0]
            with self.subTest(link=link):
                target_path = (DOCS_DIR / file_part).resolve()
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
                    target_path = (DOCS_DIR / file_part).resolve()
                    anchor_cache[file_part] = _heading_anchors(_read(target_path))
                self.assertIn(
                    anchor,
                    anchor_cache[file_part],
                    f"anchor #{anchor} does not match any heading slug in "
                    f"{file_part} -- the case study link is stale",
                )

    def test_every_required_domain_gets_at_least_one_anchored_link(self):
        # Beyond just naming the file, each domain must be linked into at
        # a specific section -- otherwise "covers all five domains" would
        # be satisfied by five bare file mentions with no real content tie.
        for domain_file in REQUIRED_DOMAIN_FILES:
            with self.subTest(domain=domain_file):
                anchored = [
                    link
                    for link in self.internal_links
                    if link.startswith(domain_file + "#")
                ]
                self.assertGreaterEqual(
                    len(anchored),
                    2,
                    f"expected at least two anchored links into {domain_file}",
                )


if __name__ == "__main__":
    unittest.main()
