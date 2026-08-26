"""Structural validation for docs/master-glossary.md.

docs/GLOSSARY.md already merges every domain's "Key terms" section into one
alphabetical, backlinked glossary (see tests/test_glossary.py). It answers
"what does term X mean, and where is it explained?" but reading it to
answer "which domain(s) touch term X?" means reading the whole prose entry.

docs/master-glossary.md is the companion cross-domain *index*: the same
merged, alphabetical term set, but each entry carries an explicit domain
tag (e.g. "[D1, D3]") up front plus a link per tagged domain, so a learner
can scan the tag alone to see which domain guide(s) cover a term before
following a link.

These tests mirror tests/test_glossary.py's structural checks (existence,
README discoverability, alphabetical order, no duplicates, domain
coverage, link resolution) and additionally verify the domain-tag format
itself: every entry has a `[D#, ...]` tag, and every tagged domain has a
corresponding resolvable link in that same entry.

Run with:
    python3 -m unittest tests/test_master_glossary.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
MASTER_GLOSSARY_PATH = DOCS_DIR / "master-glossary.md"
README_PATH = REPO_ROOT / "README.md"

DOMAIN_KEY_TERMS_SECTIONS = [
    ("domain-1-fundamentals-of-ai-and-ml.md", "Key terms glossary"),
    ("domain-2-fundamentals-of-generative-ai.md", "Key terms glossary"),
    ("domain-3-applications-of-foundation-models.md", "Key terms glossary"),
    ("domain-4-guidelines-for-responsible-ai.md", "Key terms glossary"),
    ("domain-5-security-compliance-governance.md", "Key terms glossary"),
]

# A representative sample spanning all five domains -- enough to catch a
# regression that drops a whole domain's contribution.
REQUIRED_SAMPLE_TERMS = [
    "AI (Artificial Intelligence)",  # Domain 1
    "Overfitting",  # Domain 1
    "Foundation model (FM)",  # Domain 2
    "Retrieval Augmented Generation (RAG)",  # Domain 2 & 3
    "Amazon Bedrock Knowledge Bases",  # Domain 2 & 3
    "Vector database",  # Domain 2 & 3
    "Fairness",  # Domain 4
    "Amazon SageMaker Clarify",  # Domain 4
    "AWS PrivateLink",  # Domain 5
    "Shared responsibility model",  # Domain 5
]

# - **Term** `[D1, D3]` — definition. [D1](link) · [D3](link)
ENTRY_RE = re.compile(
    r"^- \*\*(?P<term>.+?)\*\* `\[(?P<tags>D\d(?:, D\d)*)\]` — (?P<rest>.+)$",
    re.M,
)
DOMAIN_TAG_LINK_RE = re.compile(r"\[D(?P<num>\d)\]\((?P<target>[^)\s]+)\)")


def _read(path):
    return path.read_text(encoding="utf-8")


def _slugify(heading_text):
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def _heading_anchors(doc_text):
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


def _extract_domain_terms(filename, heading):
    text = _read(DOCS_DIR / filename)
    pattern = re.compile(
        r"^## " + re.escape(heading) + r"\s*$(.*?)(?:^## |\Z)", re.M | re.S
    )
    match = pattern.search(text)
    assert match, f"could not find {heading!r} section in {filename}"
    term_re = re.compile(r"^- \*\*(?P<term>.+?)\*\*\s*[—-]\s*.+$", re.M)
    return term_re.findall(match.group(1))


class TestMasterGlossaryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            MASTER_GLOSSARY_PATH.is_file(),
            f"expected master glossary at {MASTER_GLOSSARY_PATH}",
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/master-glossary.md",
            readme_text,
            "README.md must link to the master glossary so learners can "
            "discover it",
        )

    def test_linked_from_glossary(self):
        glossary_text = _read(DOCS_DIR / "GLOSSARY.md")
        self.assertIn(
            "master-glossary.md",
            glossary_text,
            "GLOSSARY.md should cross-reference the master index",
        )


class TestMasterGlossaryCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(MASTER_GLOSSARY_PATH)
        cls.entries = ENTRY_RE.findall(cls.text)

    def test_has_title(self):
        self.assertRegex(self.text, r"^# .*Master Glossary")

    def test_found_entries(self):
        # Sanity check the entry regex actually matches the document's
        # bullet syntax before relying on it in the rest of this class.
        self.assertGreaterEqual(
            len(self.entries),
            100,
            "expected the master glossary to contain at least 100 terms "
            "across the five domain guides",
        )

    def test_covers_required_sample_terms(self):
        terms = [term for term, _tags, _rest in self.entries]
        for term in REQUIRED_SAMPLE_TERMS:
            with self.subTest(term=term):
                self.assertIn(
                    term, terms, f"master glossary missing term entry: {term!r}"
                )

    def test_entries_are_sorted_alphabetically(self):
        sort_keys = [term.lower() for term, _tags, _rest in self.entries]
        self.assertEqual(
            sort_keys,
            sorted(sort_keys),
            "master glossary entries must be in alphabetical order so it "
            "can be used as an index",
        )

    def test_no_duplicate_terms(self):
        seen = set()
        duplicates = set()
        for term, _tags, _rest in self.entries:
            key = term.lower()
            if key in seen:
                duplicates.add(term)
            seen.add(key)
        self.assertFalse(
            duplicates,
            f"master glossary has duplicate term entries: {sorted(duplicates)}",
        )

    def test_every_domain_key_term_is_represented(self):
        def normalize(term):
            t = term.lower()
            t = re.sub(r"\([^)]*\)", "", t)
            t = re.sub(r"[^a-z0-9 ]", "", t)
            return re.sub(r"\s+", " ", t).strip()

        glossary_normalized = {normalize(term) for term, _tags, _rest in self.entries}
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
            f"master glossary is missing terms from domain guides: {missing}",
        )


class TestMasterGlossaryDomainTags(unittest.TestCase):
    """The whole point of this doc is the domain tag + matching link per
    entry. Verify every entry's tag set is non-empty, matches the domains
    it links to, and every link resolves to a real file and heading."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(MASTER_GLOSSARY_PATH)
        cls.entries = ENTRY_RE.findall(cls.text)
        cls.anchor_cache = {}

    def _anchors_for(self, filename):
        if filename not in self.anchor_cache:
            target_path = (DOCS_DIR / filename).resolve()
            self.anchor_cache[filename] = _heading_anchors(_read(target_path))
        return self.anchor_cache[filename]

    def test_every_entry_tag_matches_its_links(self):
        for term, tags, rest in self.entries:
            with self.subTest(term=term):
                tag_nums = {t.strip()[1:] for t in tags.split(",")}
                link_matches = DOMAIN_TAG_LINK_RE.findall(rest)
                link_nums = {num for num, _target in link_matches}
                self.assertTrue(tag_nums, f"entry {term!r} has an empty domain tag")
                self.assertEqual(
                    tag_nums,
                    link_nums,
                    f"entry {term!r} has domain tag [{tags}] that does not "
                    f"match its D#(...) links {link_matches!r}",
                )

    def test_every_tag_link_target_file_exists_with_anchor(self):
        for term, _tags, rest in self.entries:
            for num, target in DOMAIN_TAG_LINK_RE.findall(rest):
                with self.subTest(term=term, target=target):
                    file_part, _, anchor = target.partition("#")
                    target_path = (DOCS_DIR / file_part).resolve()
                    self.assertTrue(
                        target_path.is_file(),
                        f"linked file does not exist: {file_part!r} "
                        f"(resolved to {target_path})",
                    )
                    if anchor:
                        self.assertIn(
                            anchor,
                            self._anchors_for(file_part),
                            f"anchor #{anchor} does not match any heading "
                            f"slug in {file_part} for term {term!r}",
                        )

    def test_links_reach_every_domain_guide(self):
        all_targets = []
        for _term, _tags, rest in self.entries:
            all_targets.extend(t for _num, t in DOMAIN_TAG_LINK_RE.findall(rest))
        for filename, _heading in DOMAIN_KEY_TERMS_SECTIONS:
            with self.subTest(domain=filename):
                self.assertTrue(
                    any(t.split("#", 1)[0] == filename for t in all_targets),
                    f"master glossary has no tagged link into {filename}",
                )

    def test_multi_domain_terms_have_multiple_tags(self):
        # Spot-check known cross-domain terms actually carry >1 tag, since
        # that's the entire value proposition of this index over a plain
        # per-domain glossary.
        multi_domain_terms = {
            "Retrieval Augmented Generation (RAG)",
            "Amazon Bedrock Knowledge Bases",
            "Vector database",
        }
        by_term = {term: tags for term, tags, _rest in self.entries}
        for term in multi_domain_terms:
            with self.subTest(term=term):
                self.assertIn(term, by_term)
                self.assertGreaterEqual(
                    len(by_term[term].split(",")),
                    2,
                    f"expected {term!r} to be tagged with 2+ domains",
                )


if __name__ == "__main__":
    unittest.main()
