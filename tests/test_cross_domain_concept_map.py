"""Structural validation for docs/cross-domain-concept-map.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. The cross-domain concept map exists to
link Domain 1 fundamentals to their downstream applications in Domains
3-5, so what matters most here is that it is actually reachable from
README.md and that every markdown link it makes into a domain guide
resolves to a real file and a real heading in that file. A future edit
that renames a heading in a domain doc (breaking an anchor link) or
removes the README pointer would otherwise go unnoticed since nothing
renders these docs in CI.

Mirrors the conventions established in tests/test_domain_1_study_guide.py.

Run with:
    python3 -m unittest tests/test_cross_domain_concept_map.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "cross-domain-concept-map.md"
README_PATH = REPO_ROOT / "README.md"

# Domain 1 concepts the task description requires this map to cover, since
# they are the concrete examples named in the gap report.
REQUIRED_D1_CONCEPTS = [
    "model evaluation",
    "bias",
    "variance",
    "ML development lifecycle",
]

# Every downstream domain the task requires Domain 1 to be linked to.
REQUIRED_DOWNSTREAM_DOMAINS = [
    "domain-3-applications-of-foundation-models.md",
    "domain-4-guidelines-for-responsible-ai.md",
    "domain-5-security-compliance-governance.md",
]

# The commonly-confused concept pairs the "quick reference" table must cover,
# one substring per pair that is expected to appear verbatim in the table.
REQUIRED_CONFUSED_PAIRS = [
    "Statistical bias (bias–variance trade-off) vs. fairness bias",
    "Precision vs. recall",
    "Fine-tuning vs. continued pre-training",
    "CloudTrail vs. Config vs. Audit Manager",
    "Model Cards vs. AI Service Cards",
    "On-demand vs. provisioned throughput",
    "Real-time vs. batch vs. serverless inference",
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


class TestCrossDomainConceptMapExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected cross-domain concept map at {DOC_PATH}",
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/cross-domain-concept-map.md",
            readme_text,
            "README.md must link to the cross-domain concept map so "
            "learners can discover it",
        )


class TestCrossDomainConceptMapCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def test_has_title(self):
        self.assertRegex(self.text, r"^# Cross-Domain Concept Map")

    def test_covers_required_domain1_concepts(self):
        for concept in REQUIRED_D1_CONCEPTS:
            with self.subTest(concept=concept):
                self.assertRegex(
                    self.text,
                    re.compile(re.escape(concept), re.IGNORECASE),
                    f"concept map missing Domain 1 concept: {concept!r}",
                )

    def test_links_into_every_downstream_domain(self):
        for domain_file in REQUIRED_DOWNSTREAM_DOMAINS:
            with self.subTest(domain=domain_file):
                self.assertIn(
                    domain_file,
                    self.text,
                    f"concept map does not link into {domain_file}",
                )

    def test_links_back_into_domain_1(self):
        self.assertIn("domain-1-fundamentals-of-ai-and-ml.md", self.text)

    def test_has_a_table_per_downstream_domain(self):
        # A markdown table needs a header separator row like |---|---|---|
        table_rows = re.findall(r"\|\s*-{2,}\s*\|", self.text)
        self.assertGreaterEqual(
            len(table_rows),
            len(REQUIRED_DOWNSTREAM_DOMAINS),
            "expected at least one concept-map table per downstream domain",
        )


class TestVisualOverviewDiagram(unittest.TestCase):
    """Regression coverage for the 'Visual overview' Mermaid flowchart: the
    map's whole point is tracing how D1/D2 concepts flow into D3, and how
    both D1/D2 and D3 flow into D4/D5, so this must exist as an actual
    diagram (not just more prose) and must reference all five domains."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        heading_match = re.search(r"^## Visual overview.*?$", cls.text, re.M)
        if heading_match is None:
            raise AssertionError("expected a 'Visual overview' section")
        start = heading_match.end()
        next_heading = re.search(r"^## ", cls.text[start:], re.M)
        end = start + next_heading.start() if next_heading else len(cls.text)
        cls.section_text = cls.text[start:end]
        cls.mermaid_blocks = re.findall(
            r"```mermaid\n(.*?)```", cls.section_text, re.S
        )

    def test_section_exists(self):
        self.assertIn("## Visual overview", self.text)

    def test_section_has_a_mermaid_diagram(self):
        self.assertGreaterEqual(
            len(self.mermaid_blocks),
            1,
            "the visual overview section must contain an actual Mermaid "
            "flowchart, not just prose",
        )

    def test_diagram_is_a_flowchart_or_graph(self):
        combined = "\n".join(self.mermaid_blocks)
        self.assertRegex(
            combined,
            r"^\s*(flowchart|graph)\s+(TD|LR|BT|RL)",
            "expected the diagram to declare a flowchart/graph direction",
        )

    def test_diagram_references_every_domain(self):
        combined = "\n".join(self.mermaid_blocks)
        for domain_label in [
            "Domain 1",
            "Domain 2",
            "Domain 3",
            "Domain 4",
            "Domain 5",
        ]:
            with self.subTest(domain=domain_label):
                self.assertIn(
                    domain_label,
                    combined,
                    f"visual overview diagram missing a node/subgraph for "
                    f"{domain_label!r}",
                )

    def test_diagram_shows_d1_and_d2_flowing_into_d3_d4_d5(self):
        combined = "\n".join(self.mermaid_blocks)
        # Arrows into a D3-, D4-, or D5-prefixed node id demonstrate the
        # flow this diagram exists to visualize.
        for target_prefix in ["D3_", "D4_", "D5_"]:
            with self.subTest(target=target_prefix):
                self.assertRegex(
                    combined,
                    re.compile(r"-->\s*" + re.escape(target_prefix)),
                    f"expected at least one arrow flowing into a "
                    f"{target_prefix}* node",
                )
        # And at least one arrow must originate from a D1_ or D2_ node,
        # confirming the fundamentals are the source of the flow.
        self.assertRegex(
            combined,
            re.compile(r"(D1_|D2_)\w*\s*-->"),
            "expected at least one arrow originating from a D1_ or D2_ node",
        )

    def test_diagram_shows_d3_flowing_into_d4_and_d5(self):
        combined = "\n".join(self.mermaid_blocks)
        self.assertRegex(
            combined,
            re.compile(r"D3_\w*\s*-->\s*D4_"),
            "expected an arrow from a D3_ node into a D4_ node",
        )
        self.assertRegex(
            combined,
            re.compile(r"D3_\w*\s*-->\s*D5_"),
            "expected an arrow from a D3_ node into a D5_ node",
        )


class TestCommonlyConfusedConceptPairsTable(unittest.TestCase):
    """Regression coverage for the 'Commonly confused concept pairs' quick
    reference table: every required pair must be present, in a real
    markdown table, each with at least one source-section link."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        heading_match = re.search(
            r"^## Commonly confused concept pairs.*?$", cls.text, re.M
        )
        if heading_match is None:
            cls.section_text = ""
        else:
            # Slice from the heading to the next top-level (##) heading or
            # end of file, so assertions below only look at this section.
            start = heading_match.end()
            next_heading = re.search(r"^## ", cls.text[start:], re.M)
            end = start + next_heading.start() if next_heading else len(cls.text)
            cls.section_text = cls.text[start:end]

    def test_section_exists(self):
        self.assertIn(
            "## Commonly confused concept pairs",
            self.text,
            "expected a 'Commonly confused concept pairs' quick-reference "
            "section in the cross-domain concept map",
        )

    def test_section_contains_a_markdown_table(self):
        self.assertRegex(
            self.section_text,
            r"\|\s*-{2,}\s*\|",
            "the commonly-confused-pairs section must contain a real "
            "markdown table (header separator row)",
        )

    def test_covers_every_required_pair(self):
        for pair in REQUIRED_CONFUSED_PAIRS:
            with self.subTest(pair=pair):
                self.assertIn(
                    pair,
                    self.section_text,
                    f"commonly-confused-pairs table missing pair: {pair!r}",
                )

    def test_every_row_has_at_least_one_source_link(self):
        # Data rows are lines starting with "|" that aren't the header or
        # separator row.
        rows = [
            line
            for line in self.section_text.splitlines()
            if line.strip().startswith("|")
            and not re.match(r"^\|\s*-{2,}", line.strip())
            and "Term A vs. Term B" not in line
        ]
        self.assertEqual(
            len(rows),
            len(REQUIRED_CONFUSED_PAIRS),
            "expected exactly one table row per required confused pair",
        )
        for row in rows:
            with self.subTest(row=row[:60]):
                self.assertRegex(
                    row,
                    MD_LINK_RE,
                    f"table row has no source-section link: {row!r}",
                )


class TestCrossDomainConceptMapLinksResolve(unittest.TestCase):
    """The whole point of this doc is its links. Verify every relative
    markdown link (optionally with a #anchor) points at a real file, and
    that the anchor -- if present -- matches a real heading in that file."""

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
            10,
            "expected many internal links from the concept map into the "
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
                    f"{file_part} -- the concept map link is stale",
                )


if __name__ == "__main__":
    unittest.main()