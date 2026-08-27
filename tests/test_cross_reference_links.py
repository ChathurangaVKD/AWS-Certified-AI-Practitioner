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


if __name__ == "__main__":
    unittest.main()
