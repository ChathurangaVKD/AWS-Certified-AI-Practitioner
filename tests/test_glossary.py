"""Structural validation for docs/GLOSSARY.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. Each domain guide has its own "Key
terms"/"Key terms glossary" section, but there was previously no
integrated, series-wide index -- learners had to know (or guess) which
domain defined a term before they could look it up. docs/GLOSSARY.md fixes
that by merging every domain's key terms into one alphabetical glossary
with backlinks into the domain section that explains each term in detail.

These tests assert that the glossary actually achieves that: it is
reachable from README.md, it is sorted alphabetically, it contains (at
minimum) the key terms pulled directly out of each domain guide's own
glossary section, and every backlink it makes into a domain guide resolves
to a real file and a real heading anchor in that file (mirrors the
conventions established in tests/test_cross_domain_concept_map.py).

Run with:
    python3 -m unittest tests/test_glossary.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
GLOSSARY_PATH = DOCS_DIR / "GLOSSARY.md"
README_PATH = REPO_ROOT / "README.md"

# Every domain guide, its own "Key terms" heading text, and the anchor that
# heading slugifies to.
DOMAIN_KEY_TERMS_SECTIONS = [
    ("domain-1-fundamentals-of-ai-and-ml.md", "Key terms glossary"),
    ("domain-2-fundamentals-of-generative-ai.md", "Key terms glossary"),
    ("domain-3-applications-of-foundation-models.md", "Key terms glossary"),
    ("domain-4-guidelines-for-responsible-ai.md", "Key terms glossary"),
    ("domain-5-security-compliance-governance.md", "Key terms glossary"),
]

# A representative sample of terms that must appear in the merged glossary,
# spanning all five domains (not every single term -- just enough that a
# regression dropping a whole domain's contribution would be caught).
REQUIRED_SAMPLE_TERMS = [
    "AI (Artificial Intelligence)",  # Domain 1
    "Overfitting",  # Domain 1
    "Foundation model (FM)",  # Domain 2
    "Retrieval Augmented Generation (RAG)",  # Domain 2 & 3
    "Amazon Bedrock Knowledge Bases",  # Domain 2 & 3 (aliased names merged)
    "Vector database",  # Domain 2 & 3
    "Fairness",  # Domain 4
    "Amazon SageMaker Clarify",  # Domain 4
    "AWS PrivateLink",  # Domain 5
    "Shared responsibility model",  # Domain 5
]

TERM_ENTRY_RE = re.compile(r"^- \*\*(?P<term>.+?)\*\*\s*[—-]\s*.+$", re.M)
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


def _extract_domain_terms(filename, heading):
    text = _read(DOCS_DIR / filename)
    pattern = re.compile(
        r"^## " + re.escape(heading) + r"\s*$(.*?)(?:^## |\Z)", re.M | re.S
    )
    match = pattern.search(text)
    assert match, f"could not find {heading!r} section in {filename}"
    return TERM_ENTRY_RE.findall(match.group(1))


class TestGlossaryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            GLOSSARY_PATH.is_file(), f"expected glossary at {GLOSSARY_PATH}"
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/GLOSSARY.md",
            readme_text,
            "README.md must link to the glossary so learners can discover it",
        )


class TestGlossaryCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(GLOSSARY_PATH)
        cls.entries = TERM_ENTRY_RE.findall(cls.text)

    def test_has_title(self):
        self.assertRegex(self.text, r"^# .*Glossary")

    def test_covers_required_sample_terms(self):
        for term in REQUIRED_SAMPLE_TERMS:
            with self.subTest(term=term):
                self.assertIn(
                    term,
                    self.entries,
                    f"glossary missing expected term entry: {term!r}",
                )

    def test_found_a_substantial_number_of_terms(self):
        # Sanity check that the entry regex is matching the document's
        # bullet syntax, and that the merge actually pulled in terms from
        # all five (~150-term) domain glossaries rather than just one.
        self.assertGreaterEqual(
            len(self.entries),
            100,
            "expected the merged glossary to contain at least 100 terms "
            "across the five domain guides",
        )

    def test_entries_are_sorted_alphabetically(self):
        sort_keys = [term.lower() for term in self.entries]
        self.assertEqual(
            sort_keys,
            sorted(sort_keys),
            "glossary entries must be in alphabetical order so it can be "
            "used as a lookup index",
        )

    def test_no_duplicate_terms(self):
        seen = set()
        duplicates = set()
        for term in self.entries:
            key = term.lower()
            if key in seen:
                duplicates.add(term)
            seen.add(key)
        self.assertFalse(
            duplicates,
            f"glossary has duplicate term entries: {sorted(duplicates)}",
        )

    def test_every_domain_key_term_is_represented(self):
        # Every term listed in each domain's own "Key terms" section must
        # show up (verbatim, or as a normalized/aliased form) somewhere in
        # the merged glossary -- otherwise the merge silently dropped terms.
        def normalize(term):
            t = term.lower()
            t = re.sub(r"\([^)]*\)", "", t)
            t = re.sub(r"[^a-z0-9 ]", "", t)
            return re.sub(r"\s+", " ", t).strip()

        glossary_normalized = {normalize(t) for t in self.entries}
        # A handful of terms are deliberately merged under a different
        # canonical name/ordering than their per-domain source (e.g.
        # "Agents for Amazon Bedrock" (D2) and "Amazon Bedrock Agents" (D3)
        # both describe the same feature) -- allow those known aliases.
        alias_overrides = {
            "knowledge bases for amazon bedrock": "amazon bedrock knowledge bases",
            "agents for amazon bedrock": "amazon bedrock agents",
            "personally identifiable information": "pii",
        }

        missing = []
        for filename, heading in DOMAIN_KEY_TERMS_SECTIONS:
            for term in _extract_domain_terms(filename, heading):
                key = normalize(term)
                key = alias_overrides.get(key, key)
                if key not in glossary_normalized:
                    missing.append((filename, term))
        self.assertFalse(
            missing,
            f"glossary is missing terms from domain guides: {missing}",
        )


class TestGlossaryLinksResolve(unittest.TestCase):
    """The whole point of this doc is its backlinks. Verify every relative
    markdown link (optionally with a #anchor) points at a real file, and
    that the anchor -- if present -- matches a real heading in that file."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(GLOSSARY_PATH)
        cls.links = MD_LINK_RE.findall(cls.text)
        cls.internal_links = [
            link
            for link in cls.links
            if not link.startswith(("http://", "https://", "#"))
        ]

    def test_found_a_substantial_number_of_internal_links(self):
        self.assertGreaterEqual(
            len(self.internal_links),
            100,
            "expected many backlinks from the glossary into the domain "
            "guides' key-terms sections",
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
                    f"{file_part} -- the glossary link is stale",
                )

    def test_links_reach_every_domain_guide(self):
        for filename, _heading in DOMAIN_KEY_TERMS_SECTIONS:
            with self.subTest(domain=filename):
                self.assertTrue(
                    any(link.split("#", 1)[0] == filename for link in self.internal_links),
                    f"glossary has no backlink into {filename}",
                )


if __name__ == "__main__":
    unittest.main()
