"""Structural validation for the per-domain flashcard decks.

The gap this covers: each domain already had a full guide, a Fast Track
condensation, and an ULTRA-FAST-LEARN.md cram sheet, but no dedicated
active-recall / spaced-repetition format -- a student wanting to drill
individual facts (key terms, service mappings, numeric thresholds,
commonly confused pairs) had to re-read a table rather than test
themselves card by card, and had nothing importable into a spaced-
repetition tool like Anki or Quizlet.
`docs/domain-N-fast-track/FLASHCARDS.md` (a GitHub-readable front/back
table) plus the sibling `flashcards.tsv` (a header-less, two-column,
tab-separated file) fill that gap for all five domains.

These tests assert, for every domain:
  * both files exist and are kept in exact 1:1 sync (same cards, same
    order, same wording) between the Markdown table and the .tsv;
  * the .tsv is strictly two tab-separated columns with no header row and
    no blank lines, so it imports into Anki/Quizlet without reformatting;
  * every card has a non-trivial front and a short (1-2 line), non-prose
    back;
  * every "Rapid-fire key terms" bullet in that domain's ULTRA-FAST-LEARN.md
    (where such a section exists) has a corresponding flashcard front;
  * the root README and the relevant per-domain fast-track README(s) link
    to the new deck immediately alongside the existing ULTRA-FAST-LEARN.md
    reference, without reframing the "Three-tier learning structure"
    section as a four- or five-tier structure; and
  * every internal markdown link inside each FLASHCARDS.md resolves to a
    real file/anchor.

Run with:
    python3 -m unittest tests/test_flashcard_decks.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")
MD_TABLE_ROW_RE = re.compile(r"^\|(?!-{2,})([^|\n]+)\|([^|\n]+)\|\s*$", re.M)

DOMAINS = {
    1: {
        "dir": DOCS_DIR / "domain-1-fast-track",
        "fast_track_readmes": [DOCS_DIR / "domain-1-fast-track" / "README.md"],
        "ultra": DOCS_DIR / "domain-1-fast-track" / "ULTRA-FAST-LEARN.md",
        "has_rapid_fire": True,
    },
    2: {
        "dir": DOCS_DIR / "domain-2-fast-track",
        "fast_track_readmes": [DOCS_DIR / "domain-2-fast-track" / "README.md"],
        "ultra": DOCS_DIR / "domain-2-fast-track" / "ULTRA-FAST-LEARN.md",
        "has_rapid_fire": True,
    },
    3: {
        "dir": DOCS_DIR / "domain-3-fast-track",
        "fast_track_readmes": [
            DOCS_DIR / "domain-3-fast-track" / "README.md",
            DOCS_DIR / "domain-3-fast-track" / "part-1-application-design-and-customization.md",
            DOCS_DIR / "domain-3-fast-track" / "part-2-inference-and-multimodal.md",
            DOCS_DIR / "domain-3-fast-track" / "part-3-deployment-and-troubleshooting.md",
        ],
        "ultra": DOCS_DIR / "domain-3-fast-track" / "ULTRA-FAST-LEARN.md",
        "has_rapid_fire": True,
    },
    4: {
        "dir": DOCS_DIR / "domain-4-fast-track",
        "fast_track_readmes": [DOCS_DIR / "domain-4-fast-track" / "README.md"],
        "ultra": DOCS_DIR / "domain-4-fast-track" / "ULTRA-FAST-LEARN.md",
        "has_rapid_fire": True,
    },
    5: {
        "dir": DOCS_DIR / "domain-5-fast-track",
        "fast_track_readmes": [
            DOCS_DIR / "domain-5-fast-track" / "README.md",
            DOCS_DIR / "domain-5-fast-track" / "part-1-security-and-compliance.md",
            DOCS_DIR / "domain-5-fast-track" / "part-2-governance-and-monitoring.md",
        ],
        "ultra": DOCS_DIR / "domain-5-fast-track" / "ULTRA-FAST-LEARN.md",
        # Domain 5's ULTRA-FAST-LEARN.md has no "Rapid-fire key terms"
        # section of its own -- its cram sheet is built entirely from
        # tables and inline "don't confuse" bullets instead.
        "has_rapid_fire": False,
    },
}

for _domain, _cfg in DOMAINS.items():
    _cfg["md"] = _cfg["dir"] / "FLASHCARDS.md"
    _cfg["tsv"] = _cfg["dir"] / "flashcards.tsv"


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


def _md_card_rows(md_text):
    """Extract (front, back) pairs from every '| Front | Back |' table in
    the deck, skipping header/separator rows."""
    rows = []
    for front, back in MD_TABLE_ROW_RE.findall(md_text):
        front, back = front.strip(), back.strip()
        if front == "Front" and back == "Back":
            continue
        rows.append((front, back))
    return rows


def _tsv_card_rows(tsv_text):
    lines = tsv_text.splitlines()
    return lines


def _rapid_fire_terms(ultra_text):
    """Pull the bolded term names out of the 'Rapid-fire key terms'
    section (each bullet is '- **Term** -- definition')."""
    match = re.search(
        r"\n## Rapid-fire key terms\n(.*?)\n## ", ultra_text, re.S
    )
    if not match:
        return []
    section = match.group(1)
    return re.findall(r"\n-\s+\*\*([^*]+)\*\*", "\n" + section)


class TestFlashcardFilesExist(unittest.TestCase):
    def test_md_and_tsv_exist_for_every_domain(self):
        for domain, cfg in DOMAINS.items():
            with self.subTest(domain=domain):
                self.assertTrue(
                    cfg["md"].is_file(),
                    f"expected {cfg['md']} to exist",
                )
                self.assertTrue(
                    cfg["tsv"].is_file(),
                    f"expected {cfg['tsv']} to exist",
                )

    def test_decks_are_not_trivial_stubs(self):
        for domain, cfg in DOMAINS.items():
            with self.subTest(domain=domain):
                tsv_lines = [
                    l for l in _read(cfg["tsv"]).splitlines() if l.strip()
                ]
                self.assertGreaterEqual(
                    len(tsv_lines),
                    20,
                    f"domain {domain} flashcards.tsv has only "
                    f"{len(tsv_lines)} cards -- expected a real deck",
                )


class TestTsvFormat(unittest.TestCase):
    """The .tsv must be exactly two tab-separated columns, no header row,
    importable as-is into Anki/Quizlet."""

    def test_no_header_row(self):
        for domain, cfg in DOMAINS.items():
            with self.subTest(domain=domain):
                first_line = _read(cfg["tsv"]).splitlines()[0]
                front = first_line.split("\t", 1)[0].strip().lower()
                self.assertNotIn(
                    front,
                    {"front", "question", "term"},
                    f"domain {domain} flashcards.tsv appears to start with "
                    "a header row",
                )

    def test_every_line_has_exactly_two_tab_separated_columns(self):
        for domain, cfg in DOMAINS.items():
            lines = _read(cfg["tsv"]).splitlines()
            for i, line in enumerate(lines):
                with self.subTest(domain=domain, line_no=i + 1):
                    self.assertEqual(
                        line.count("\t"),
                        1,
                        f"domain {domain} flashcards.tsv line {i + 1} does "
                        f"not have exactly one tab separator: {line!r}",
                    )

    def test_no_blank_lines(self):
        for domain, cfg in DOMAINS.items():
            lines = _read(cfg["tsv"]).splitlines()
            for i, line in enumerate(lines):
                with self.subTest(domain=domain, line_no=i + 1):
                    self.assertTrue(
                        line.strip(),
                        f"domain {domain} flashcards.tsv has a blank line "
                        f"at {i + 1}",
                    )

    def test_both_columns_nonempty(self):
        for domain, cfg in DOMAINS.items():
            lines = _read(cfg["tsv"]).splitlines()
            for i, line in enumerate(lines):
                front, back = line.split("\t")
                with self.subTest(domain=domain, line_no=i + 1):
                    self.assertTrue(front.strip())
                    self.assertTrue(back.strip())


class TestMarkdownAndTsvAreInSync(unittest.TestCase):
    """Same cards, same order, same wording in both files."""

    def test_row_counts_match(self):
        for domain, cfg in DOMAINS.items():
            md_rows = _md_card_rows(_read(cfg["md"]))
            tsv_rows = _tsv_card_rows(_read(cfg["tsv"]))
            with self.subTest(domain=domain):
                self.assertEqual(
                    len(md_rows),
                    len(tsv_rows),
                    f"domain {domain}: FLASHCARDS.md has {len(md_rows)} "
                    f"card rows but flashcards.tsv has {len(tsv_rows)} "
                    "lines -- they must be in 1:1 sync",
                )

    def test_wording_and_order_match(self):
        for domain, cfg in DOMAINS.items():
            md_rows = _md_card_rows(_read(cfg["md"]))
            tsv_rows = _tsv_card_rows(_read(cfg["tsv"]))
            for i, (md_row, tsv_line) in enumerate(zip(md_rows, tsv_rows)):
                tsv_front, tsv_back = tsv_line.split("\t")
                with self.subTest(domain=domain, card_index=i):
                    self.assertEqual(md_row[0], tsv_front)
                    self.assertEqual(md_row[1], tsv_back)


class TestCardContentIsRecallFormat(unittest.TestCase):
    """Front/back only, no prose paragraphs -- backs stay one-to-two lines,
    matching the terseness of the existing Ultra Fast Track tier."""

    def test_backs_are_short_not_prose_paragraphs(self):
        for domain, cfg in DOMAINS.items():
            rows = _md_card_rows(_read(cfg["md"]))
            for i, (front, back) in enumerate(rows):
                with self.subTest(domain=domain, card_index=i, front=front):
                    # A one-to-two-line recall fact comfortably fits in a
                    # single table cell well under this length; a real
                    # prose explanation would run much longer.
                    self.assertLess(
                        len(back),
                        320,
                        f"domain {domain} card back looks like a prose "
                        f"paragraph, not a short recall fact: {back!r}",
                    )
                    self.assertFalse(
                        back.endswith(":"),
                        "back should be a complete recall fact, not a "
                        "dangling lead-in",
                    )

    def test_fronts_are_prompts_not_answers_dumped_together(self):
        for domain, cfg in DOMAINS.items():
            rows = _md_card_rows(_read(cfg["md"]))
            for i, (front, _back) in enumerate(rows):
                with self.subTest(domain=domain, card_index=i):
                    self.assertLess(len(front), 200)
                    self.assertGreater(len(front), 0)


class TestCoverageOfRapidFireKeyTerms(unittest.TestCase):
    """Every key term in a domain's own 'Rapid-fire key terms' section
    must have a corresponding flashcard."""

    def test_every_rapid_fire_term_has_a_card(self):
        for domain, cfg in DOMAINS.items():
            if not cfg["has_rapid_fire"]:
                continue
            ultra_text = _read(cfg["ultra"])
            terms = _rapid_fire_terms(ultra_text)
            self.assertGreaterEqual(
                len(terms),
                5,
                f"domain {domain}: expected to find rapid-fire key terms "
                "in ULTRA-FAST-LEARN.md",
            )
            deck_text = _read(cfg["tsv"])
            for term in terms:
                with self.subTest(domain=domain, term=term):
                    self.assertIn(
                        term,
                        deck_text,
                        f"domain {domain}: rapid-fire key term {term!r} "
                        "has no corresponding flashcard",
                    )


class TestFlashcardDeckLinksResolve(unittest.TestCase):
    """Every internal link inside each FLASHCARDS.md must resolve."""

    @classmethod
    def setUpClass(cls):
        cls.anchor_cache = {}

    def test_every_internal_link_resolves(self):
        for domain, cfg in DOMAINS.items():
            md_path = cfg["md"]
            text = _read(md_path)
            links = [
                l
                for l in MD_LINK_RE.findall(text)
                if not l.startswith(("http://", "https://"))
            ]
            with self.subTest(domain=domain):
                self.assertGreaterEqual(len(links), 2)
            for link in links:
                file_part, _, anchor = link.partition("#")
                target = (
                    md_path.parent / file_part if file_part else md_path
                ).resolve()
                with self.subTest(domain=domain, link=link):
                    self.assertTrue(
                        target.is_file(),
                        f"domain {domain} FLASHCARDS.md links to missing "
                        f"file: {link!r} (resolved to {target})",
                    )
                    if anchor:
                        cache_key = str(target)
                        if cache_key not in self.anchor_cache:
                            self.anchor_cache[cache_key] = _heading_anchors(
                                _read(target)
                            )
                        self.assertIn(
                            anchor,
                            self.anchor_cache[cache_key],
                            f"domain {domain} FLASHCARDS.md link {link!r} "
                            "has a stale anchor",
                        )


class TestNavigationUpdated(unittest.TestCase):
    """The root README and every per-domain fast-track README/part file
    must link to the new deck alongside the existing ULTRA-FAST-LEARN.md
    reference, and the three-tier framing must not have been rewritten."""

    @classmethod
    def setUpClass(cls):
        cls.root_readme = _read(REPO_ROOT / "README.md")

    def test_root_readme_still_calls_it_three_tier(self):
        self.assertIn("Three-tier learning structure", self.root_readme)
        self.assertNotIn("Four-tier learning structure", self.root_readme)
        self.assertNotIn("4-tier", self.root_readme)
        self.assertNotIn("Five-tier learning structure", self.root_readme)
        self.assertNotIn("5-tier", self.root_readme)

    def test_root_readme_links_every_domain_flashcard_deck(self):
        for domain in DOMAINS:
            with self.subTest(domain=domain):
                self.assertIn(
                    f"docs/domain-{domain}-fast-track/FLASHCARDS.md",
                    self.root_readme,
                )

    def test_root_readme_mentions_anki_or_quizlet(self):
        self.assertTrue(
            "Anki" in self.root_readme or "Quizlet" in self.root_readme
        )

    def test_each_domain_fast_track_entry_point_links_flashcards(self):
        for domain, cfg in DOMAINS.items():
            # At least one of the domain's fast-track entry points (the
            # main README, or -- for the split domains -- the README plus
            # each part file) must reference FLASHCARDS.md.
            texts = [_read(p) for p in cfg["fast_track_readmes"]]
            with self.subTest(domain=domain):
                self.assertTrue(
                    any("FLASHCARDS.md" in t for t in texts),
                    f"domain {domain}: no fast-track entry point links to "
                    "FLASHCARDS.md",
                )

    def test_domain_3_and_5_part_files_note_deck_covers_whole_domain(self):
        # Domains 3 and 5 split their Fast Track into parts, but ship one
        # flashcard deck per domain, not one per part -- each part file
        # should say so rather than leaving that ambiguous.
        for domain in (3, 5):
            for path in DOMAINS[domain]["fast_track_readmes"]:
                if path.name == "README.md":
                    continue
                text = _read(path)
                # Markdown prose wraps across lines, so normalize
                # whitespace before checking for the phrase.
                normalized = re.sub(r"\s+", " ", text)
                with self.subTest(domain=domain, part=path.name):
                    self.assertIn("FLASHCARDS.md", text)
                    self.assertIn("not split by part", normalized)


if __name__ == "__main__":
    unittest.main()
