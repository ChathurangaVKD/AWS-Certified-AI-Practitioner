"""Structural validation for in-text cross-reference hyperlinks in the
domain guides.

The gap this covers: the domain guides frequently mention "Section N" or
"Domain N" in prose when referring to another part of the same file or to
another domain guide, but those mentions used to be bare text rather than
real markdown links -- so a reader had no way to jump straight to the
referenced material. This test asserts:

  * a curated set of those prose mentions were converted into real
    markdown links (regression guard against the fix being reverted or an
    anchor typo creeping back in), and
  * every internal link across all five domain guides (the new
    cross-reference links plus the pre-existing TOC/breadcrumb/glossary
    links) actually resolves: the target file exists, and if the link has
    an anchor, that anchor matches a real heading slug in the target file.

It also independently spot-checks link/anchor integrity in a second,
broader tier of documents that are individually covered by their own
dedicated test files (test_case_study_ai_system_lifecycle.py,
test_master_glossary.py, test_glossary.py, test_aws_service_index.py, and
the per-domain fast-track guide tests) but whose combined "does every
cross-reference still resolve" claim -- as stated in
DOCUMENTATION_STRUCTURE.md -- was previously only true by inference across
those separate files rather than checked in one place. Headers reworded or
sections reorganized during a content backfill can silently break a
heading-derived anchor without changing the link text itself, so this
re-derives every anchor from the *current* heading text on every run
rather than trusting that a prior audit still holds.

The second tier also covers README.md, DOCUMENTATION_STRUCTURE.md, and the
remaining cross-domain support documents that reference the five domain
guides and each other -- aws-service-decision-guide.md,
cross-domain-concept-map.md, cross-domain-scenario-questions.md,
exam-preparation-strategy.md, study-progress-tracker.md, mock-exam.md, and
full-length-mock-exam.md -- closing the previously-unverified
"comprehensive cross-linking" claim called out for README.md,
DOCUMENTATION_STRUCTURE.md, and the cross-domain materials as a whole.

Mirrors the conventions established in tests/test_readme_study_plan.py.

Run with:
    python3 -m unittest tests/test_cross_reference_links.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")

DOMAIN_FILES = {
    1: DOCS_DIR / "domain-1-fundamentals-of-ai-and-ml.md",
    2: DOCS_DIR / "domain-2-fundamentals-of-generative-ai.md",
    3: DOCS_DIR / "domain-3-applications-of-foundation-models.md",
    4: DOCS_DIR / "domain-4-guidelines-for-responsible-ai.md",
    5: DOCS_DIR / "domain-5-security-compliance-governance.md",
}

# Second tier of documents spot-checked for cross-reference link integrity:
# the AI system lifecycle case study's back-references into domain
# sections, each domain's Fast Track front-matter mapping table, the two
# glossaries' term backlinks into domain guides, and the AWS service
# index's section links. Each already has its own dedicated content test,
# but none of those individually re-derive *every* file's worth of anchors
# in one consolidated pass the way DOCUMENTATION_STRUCTURE.md's "every
# internal link and anchor across every file resolves" claim implies.
#
# DOCUMENTATION_STRUCTURE.md itself is included here too, closing the one
# named source that a 2026-09-10 audit found was never actually a checked
# *source* of links (only a checked *target*): it is a narrative/structural
# map rather than a lookup table, so it carries no real markdown links today
# other than one prose example (`[← Domain N-1 of 5](...)`) that
# illustrates the breadcrumb link *format* with a literal "..." placeholder
# rather than linking anywhere -- that placeholder is filtered out below so
# it isn't mistaken for a broken link.
SPOT_CHECK_FILES = {
    "README.md": REPO_ROOT / "README.md",
    "DOCUMENTATION_STRUCTURE.md": DOCS_DIR / "DOCUMENTATION_STRUCTURE.md",
    "case-study-ai-system-lifecycle.md": DOCS_DIR
    / "case-study-ai-system-lifecycle.md",
    "master-glossary.md": DOCS_DIR / "master-glossary.md",
    "GLOSSARY.md": DOCS_DIR / "GLOSSARY.md",
    "aws-service-index.md": DOCS_DIR / "aws-service-index.md",
    "aws-service-decision-guide.md": DOCS_DIR / "aws-service-decision-guide.md",
    "cross-domain-concept-map.md": DOCS_DIR / "cross-domain-concept-map.md",
    "cross-domain-scenario-questions.md": DOCS_DIR
    / "cross-domain-scenario-questions.md",
    "exam-preparation-strategy.md": DOCS_DIR / "exam-preparation-strategy.md",
    "study-progress-tracker.md": DOCS_DIR / "study-progress-tracker.md",
    "mock-exam.md": DOCS_DIR / "mock-exam.md",
    "full-length-mock-exam.md": DOCS_DIR / "full-length-mock-exam.md",
    "domain-1-fast-track/README.md": DOCS_DIR / "domain-1-fast-track" / "README.md",
    "domain-2-fast-track/README.md": DOCS_DIR / "domain-2-fast-track" / "README.md",
    "domain-3-fast-track/README.md": DOCS_DIR / "domain-3-fast-track" / "README.md",
    "domain-4-fast-track/README.md": DOCS_DIR / "domain-4-fast-track" / "README.md",
    "domain-5-fast-track/README.md": DOCS_DIR / "domain-5-fast-track" / "README.md",
}

# One expected linked substring per prose mention that was converted to a
# link, keyed by the domain file it lives in.
EXPECTED_LINKS = {
    1: [
        "[generative AI](domain-2-fundamentals-of-generative-ai.md#1-generative-ai-core-concepts)",
        "[foundation model applications](domain-3-applications-of-foundation-models.md#1-design-considerations-for-foundation-model-applications)",
        "[responsible AI](domain-4-guidelines-for-responsible-ai.md#1-core-dimensions-of-responsible-ai)",
        "[security/governance](domain-5-security-compliance-governance.md#1-securing-ai-systems)",
        "[Domain 2](domain-2-fundamentals-of-generative-ai.md#1-generative-ai-core-concepts), but you should know",
    ],
    2: [
        "[Domain 1](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle)",
        "(see [Section 7](#7-foundation-model-selection-criteria))",
        "([Section 6](#6-prompt-engineering-fundamentals))",
        "[Domain 1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview)",
        "[Domain 4](domain-4-guidelines-for-responsible-ai.md)/[Domain 5](domain-5-security-compliance-governance.md)",
        "[Domain 3](domain-3-applications-of-foundation-models.md)",
        "[Domain 3, Section\n  6](domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval)",
        "[Domain 3, Section\n6](domain-3-applications-of-foundation-models.md#choosing-an-embedding-model-domain-specific-vs-general-vs-fine-tuned)",
        "[Domain 3, Section\n     4](domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering)",
    ],
    3: [
        "[Domain 2](domain-2-fundamentals-of-generative-ai.md) tests whether",
        "[Section 5](#5-amazon-bedrock-features)). Larger",
        "in [Section 4](#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering) that requires no",
        "([Section 5](#5-amazon-bedrock-features)).",
        "([Section 6](#6-vector-databases-and-embeddings-for-search-and-retrieval))",
        "Covered in [Section 2](#2-prompt-engineering-techniques).",
        "Covered in [Section 3](#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases).",
        "[Domain 4 study guide](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai)",
        "in [Section 3](#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases): automatic ingestion",
    ],
    4: [
        "[Domain 5](domain-5-security-compliance-governance.md) (security, compliance",
        "([Section 2](#2-identifying-bias-and-fairness-issues-in-training-data-and-model-outputs)).",
        "([Section 3](#3-aws-tools-for-responsible-ai)).",
        "[Domain 5](domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance).",
        "[Domain 1](domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off): high bias",
        "[Domain 1](domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off)); the exam",
        "(see [Section 5](#5-balancing-model-performance-and-interpretability)),",
        "[Domain 2](domain-2-fundamentals-of-generative-ai.md#3-advantages-and-disadvantages-of-generative-ai) — because their reasoning",
        "[Domain 1](domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off)).",
        "[Domain 2](domain-2-fundamentals-of-generative-ai.md#1-generative-ai-core-concepts);",
        "[Domain 1](domain-1-fundamentals-of-ai-and-ml.md)–[Domain 3](domain-3-applications-of-foundation-models.md)",
    ],
}


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


class TestCrossReferenceLinksPresent(unittest.TestCase):
    """Each prose "Section N" / "Domain N" mention identified as a
    navigation gap must now be a real markdown link."""

    @classmethod
    def setUpClass(cls):
        cls.texts = {n: _read(p) for n, p in DOMAIN_FILES.items()}

    def test_expected_links_present(self):
        for domain_number, expected_substrings in EXPECTED_LINKS.items():
            text = self.texts[domain_number]
            for substring in expected_substrings:
                with self.subTest(domain=domain_number, substring=substring):
                    self.assertIn(
                        substring,
                        text,
                        f"expected domain {domain_number} guide to contain "
                        f"the cross-reference link {substring!r}",
                    )


class TestCrossReferenceLinksResolve(unittest.TestCase):
    """Every internal markdown link in the domain guides -- newly added
    cross-reference links plus the pre-existing TOC/breadcrumb/glossary
    links -- must resolve to a real file and, if anchored, a real
    heading."""

    @classmethod
    def setUpClass(cls):
        cls.anchor_cache = {}
        cls.links_by_domain = {}
        for domain_number, path in DOMAIN_FILES.items():
            text = _read(path)
            links = MD_LINK_RE.findall(text)
            cls.links_by_domain[domain_number] = [
                link
                for link in links
                if not link.startswith(("http://", "https://"))
            ]

    def _resolve_target_path(self, source_domain, file_part):
        if file_part == "":
            # Same-file anchor-only link, e.g. "(#5-...)".
            return DOMAIN_FILES[source_domain]
        return (DOCS_DIR / file_part).resolve()

    def test_found_internal_links_in_every_domain(self):
        for domain_number in DOMAIN_FILES:
            with self.subTest(domain=domain_number):
                self.assertGreaterEqual(
                    len(self.links_by_domain[domain_number]),
                    1,
                    f"expected domain {domain_number} guide to contain at "
                    "least one internal link (TOC/breadcrumb at minimum)",
                )

    def test_every_internal_link_target_file_exists(self):
        for domain_number, links in self.links_by_domain.items():
            for link in links:
                file_part = link.split("#", 1)[0]
                with self.subTest(domain=domain_number, link=link):
                    target_path = self._resolve_target_path(
                        domain_number, file_part
                    )
                    self.assertTrue(
                        target_path.is_file(),
                        f"linked file does not exist: {file_part!r} "
                        f"(resolved to {target_path}) in domain "
                        f"{domain_number} guide",
                    )

    def test_every_internal_anchor_matches_a_real_heading(self):
        for domain_number, links in self.links_by_domain.items():
            for link in links:
                if "#" not in link:
                    continue
                file_part, anchor = link.split("#", 1)
                if not anchor:
                    continue
                with self.subTest(domain=domain_number, link=link):
                    target_path = self._resolve_target_path(
                        domain_number, file_part
                    )
                    cache_key = str(target_path)
                    if cache_key not in self.anchor_cache:
                        self.anchor_cache[cache_key] = _heading_anchors(
                            _read(target_path)
                        )
                    self.assertIn(
                        anchor,
                        self.anchor_cache[cache_key],
                        f"anchor #{anchor} does not match any heading slug "
                        f"in {target_path} -- the link {link!r} in domain "
                        f"{domain_number} guide is stale",
                    )


class TestSpotCheckedFilesExist(unittest.TestCase):
    """Sanity check that the spot-check target set itself hasn't drifted
    (e.g. a fast-track README got renamed or moved)."""

    def test_all_spot_check_files_exist(self):
        for label, path in SPOT_CHECK_FILES.items():
            with self.subTest(file=label):
                self.assertTrue(path.is_file(), f"expected {label} to exist at {path}")


class TestSpotCheckedCrossReferenceLinksResolve(unittest.TestCase):
    """Independent spot-check of cross-reference link integrity in the
    case study, both glossaries, the AWS service index, and every domain's
    Fast Track front-matter mapping table: every internal link must
    resolve to a real file, and every anchored link must match a heading
    slug that actually exists in the *current* target file. This re-runs
    the same resolution algorithm the per-file tests use, but in one place
    across the whole second tier of documents, so a heading reworded
    during a content backfill in one file can't silently break a link
    living in a different file's dedicated test that nobody re-ran."""

    # Files that are known, checked sources of zero *real* internal links --
    # e.g. a narrative/structural document that only mentions the link
    # *format* in prose via a literal "..." placeholder rather than linking
    # anywhere. Kept explicit (rather than silently allowed) so a future
    # file added to SPOT_CHECK_FILES with genuinely zero links doesn't slip
    # through test_found_internal_links_in_every_spot_checked_file unnoticed.
    NO_REAL_LINKS_EXPECTED = {"DOCUMENTATION_STRUCTURE.md"}

    @classmethod
    def setUpClass(cls):
        cls.anchor_cache = {}
        cls.links_by_file = {}
        for label, path in SPOT_CHECK_FILES.items():
            text = _read(path)
            links = MD_LINK_RE.findall(text)
            cls.links_by_file[label] = [
                link
                for link in links
                if not link.startswith(("http://", "https://", "mailto:"))
                # Prose placeholder used to illustrate the breadcrumb link
                # *format* (e.g. "[← Domain N-1 of 5](...)"), not a real link.
                and link != "..."
            ]

    def _resolve_target_path(self, source_label, file_part):
        source_path = SPOT_CHECK_FILES[source_label]
        if file_part == "":
            # Same-file anchor-only link, e.g. "(#5-...)".
            return source_path
        # Resolve relative to the source file's own directory so that
        # fast-track READMEs' "../domain-N-....md#anchor" links resolve
        # the same way a browser or GitHub would render them.
        return (source_path.parent / file_part).resolve()

    def test_found_internal_links_in_every_spot_checked_file(self):
        for label in SPOT_CHECK_FILES:
            if label in self.NO_REAL_LINKS_EXPECTED:
                continue
            with self.subTest(file=label):
                self.assertGreaterEqual(
                    len(self.links_by_file[label]),
                    1,
                    f"expected {label} to contain at least one internal link",
                )

    def test_every_internal_link_target_file_exists(self):
        for label, links in self.links_by_file.items():
            for link in links:
                file_part = link.split("#", 1)[0]
                with self.subTest(file=label, link=link):
                    target_path = self._resolve_target_path(label, file_part)
                    self.assertTrue(
                        target_path.is_file(),
                        f"linked file does not exist: {file_part!r} "
                        f"(resolved to {target_path}) in {label}",
                    )

    def test_every_internal_anchor_matches_a_real_heading(self):
        for label, links in self.links_by_file.items():
            for link in links:
                if "#" not in link:
                    continue
                file_part, anchor = link.split("#", 1)
                if not anchor:
                    continue
                with self.subTest(file=label, link=link):
                    target_path = self._resolve_target_path(label, file_part)
                    cache_key = str(target_path)
                    if cache_key not in self.anchor_cache:
                        self.anchor_cache[cache_key] = _heading_anchors(
                            _read(target_path)
                        )
                    self.assertIn(
                        anchor,
                        self.anchor_cache[cache_key],
                        f"anchor #{anchor} does not match any heading slug "
                        f"in {target_path} -- the link {link!r} in {label} "
                        "is stale",
                    )


if __name__ == "__main__":
    unittest.main()
