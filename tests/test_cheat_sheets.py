"""Structural validation for the interactive quick-scan cheat sheets added
under each docs/domain-N-fast-track/CHEAT-SHEET.md.

The gap this covers: the repo already has a three-tier learning structure
per domain (full guide, Fast Track, Ultra Fast Learn), but nothing offered
a GitHub-flavored-Markdown *interactive* scan format -- collapsible
sections, jump links, and a self-check checklist -- distinct from those
three tiers. This test asserts, for all five domains, that CHEAT-SHEET.md:

  * exists alongside README.md and ULTRA-FAST-LEARN.md in that domain's
    docs/domain-N-fast-track/ directory,
  * has a "## Table of contents" section whose links all resolve to real
    heading anchors in the same file (so a student can actually jump to
    the topic they're weak on),
  * uses collapsible <details><summary> blocks -- one balanced pair per
    major heading -- so the page loads as a compact list of headings,
  * contains GFM tables (comparisons, thresholds, confused pairs) rather
    than prose paragraphs,
  * has a dedicated "Commonly confused pairs" section,
  * ends with a "## Self-check checklist" section made of GFM task-list
    (`- [ ]`) items, one per exam-critical fact, and
  * carries forward a representative sample of the key terms/services/
    numeric thresholds already verified in that domain's Ultra Fast Track
    cram sheet -- a spot-check that this is a reformat of existing
    verified content, not new material.

It also checks that README.md and each domain's own Fast Track README.md
link to the new cheat sheet, per the navigation requirement that it be
discoverable from wherever the existing Fast Track / Ultra Fast Track
links already live.

Run with:
    python3 -m unittest tests/test_cheat_sheets.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
README_PATH = REPO_ROOT / "README.md"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")

CHEAT_SHEETS = {
    n: DOCS_DIR / f"domain-{n}-fast-track" / "CHEAT-SHEET.md" for n in range(1, 6)
}
FAST_TRACK_READMES = {
    n: DOCS_DIR / f"domain-{n}-fast-track" / "README.md" for n in range(1, 6)
}

# A representative sample of facts already verified in each domain's
# ULTRA-FAST-LEARN.md cram sheet that must survive, unchanged, into the
# cheat sheet -- proof this is a reformat, not new research.
EXPECTED_CARRIED_FACTS = {
    1: [
        "SageMaker Feature Store",
        "~90% cheaper",
        "SageMaker Ground Truth",
        "Random Forest",
    ],
    2: [
        "Nova Micro",
        "chain-of-thought",
        "Provisioned Throughput",
        "hallucination",
    ],
    3: [
        "QLoRA",
        "Kendra GenAI Index",
        "Recall@k",
        "AWS Trainium",
    ],
    4: [
        "SHAP",
        "disparate impact",
        "Amazon A2I",
        "IP indemnification",
    ],
    5: [
        "GDPR",
        "HIPAA",
        "PrivateLink",
        "AWS Audit Manager",
    ],
}


def _read(path):
    return path.read_text(encoding="utf-8")


def _slugify(heading_text):
    """Approximate GitHub's markdown heading-anchor algorithm, matching the
    convention already used by tests/test_cross_reference_links.py and
    tests/test_readme_three_tier_learning_structure.py."""
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def _heading_anchors(doc_text):
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


class TestCheatSheetsExist(unittest.TestCase):
    def test_cheat_sheet_files_exist(self):
        for domain_number, path in CHEAT_SHEETS.items():
            with self.subTest(domain=domain_number):
                self.assertTrue(
                    path.is_file(),
                    f"expected {path} to exist as the Domain {domain_number} "
                    "interactive cheat sheet",
                )


class TestCheatSheetsStructure(unittest.TestCase):
    """Every cheat sheet must actually use GFM's interactive/scannable
    features -- a ToC with resolving anchors, collapsible sections, tables,
    a confused-pairs section, and a checkbox self-check list -- not just
    claim to."""

    @classmethod
    def setUpClass(cls):
        cls.texts = {n: _read(p) for n, p in CHEAT_SHEETS.items()}

    def test_has_table_of_contents(self):
        for domain_number in CHEAT_SHEETS:
            with self.subTest(domain=domain_number):
                self.assertIn("\n## Table of contents\n", self.texts[domain_number])

    def test_table_of_contents_anchors_resolve_to_real_headings(self):
        for domain_number, text in self.texts.items():
            toc_match = re.search(
                r"\n## Table of contents\n(.*?)\n---\n", text, re.S
            )
            with self.subTest(domain=domain_number):
                self.assertIsNotNone(toc_match, "expected a ToC block")
                toc_links = MD_LINK_RE.findall(toc_match.group(1))
                self.assertGreaterEqual(
                    len(toc_links), 5, "expected several jump links in the ToC"
                )
                anchors = _heading_anchors(text)
                for link in toc_links:
                    self.assertTrue(link.startswith("#"), f"expected an in-file jump link, got {link!r}")
                    with self.subTest(link=link):
                        self.assertIn(
                            link.lstrip("#"),
                            anchors,
                            f"ToC link {link!r} does not match any heading "
                            f"in domain {domain_number}'s cheat sheet",
                        )

    def test_uses_balanced_collapsible_details_blocks(self):
        for domain_number, text in self.texts.items():
            with self.subTest(domain=domain_number):
                opens = text.count("<details>")
                closes = text.count("</details>")
                summaries = text.count("<summary>")
                self.assertGreaterEqual(
                    opens, 6, "expected at least one <details> block per major section"
                )
                self.assertEqual(opens, closes, "<details> blocks must be balanced")
                self.assertEqual(
                    opens, summaries, "each <details> block must carry its own <summary>"
                )

    def test_has_gfm_tables(self):
        for domain_number, text in self.texts.items():
            with self.subTest(domain=domain_number):
                # A GFM table header-separator row, e.g. "|---|---|".
                separator_rows = re.findall(r"^\|[\s:-]*-[\s:|-]*\|$", text, re.M)
                self.assertGreaterEqual(
                    len(separator_rows),
                    8,
                    "expected many GFM comparison tables, not prose paragraphs",
                )

    def test_has_commonly_confused_pairs_section(self):
        for domain_number, text in self.texts.items():
            with self.subTest(domain=domain_number):
                self.assertIn("### Commonly confused pairs", text)

    def test_has_self_check_checklist_of_task_list_items(self):
        for domain_number, text in self.texts.items():
            checklist_match = re.search(
                r"\n## Self-check checklist\n(.*?)\Z", text, re.S
            )
            with self.subTest(domain=domain_number):
                self.assertIsNotNone(
                    checklist_match, "expected a '## Self-check checklist' section"
                )
                items = re.findall(r"^- \[ \] .+$", checklist_match.group(1), re.M)
                self.assertGreaterEqual(
                    len(items),
                    5,
                    "expected several one-line GFM task-list self-check items",
                )

    def test_bolds_exam_critical_facts(self):
        # Every self-check item and confused-pair table should bold at
        # least the exam-critical term/number, not just prose it.
        for domain_number, text in self.texts.items():
            checklist_match = re.search(
                r"\n## Self-check checklist\n(.*?)\Z", text, re.S
            )
            with self.subTest(domain=domain_number):
                items = re.findall(r"^- \[ \] (.+)$", checklist_match.group(1), re.M)
                bolded = [item for item in items if "**" in item]
                self.assertEqual(
                    len(bolded),
                    len(items),
                    "every self-check item should bold its exam-critical fact",
                )


class TestCheatSheetsCarryForwardVerifiedFacts(unittest.TestCase):
    """The cheat sheet is a reformat of the Fast Track / Ultra Fast Track
    tiers, not new research -- spot-check that key terms/services/numbers
    already present in ULTRA-FAST-LEARN.md survive into CHEAT-SHEET.md."""

    def test_expected_facts_carried_forward(self):
        for domain_number, expected_facts in EXPECTED_CARRIED_FACTS.items():
            cheat_sheet_text = _read(CHEAT_SHEETS[domain_number])
            ultra_path = (
                DOCS_DIR / f"domain-{domain_number}-fast-track" / "ULTRA-FAST-LEARN.md"
            )
            ultra_text = _read(ultra_path)
            for fact in expected_facts:
                with self.subTest(domain=domain_number, fact=fact):
                    self.assertIn(
                        fact,
                        ultra_text,
                        f"test fixture assumption broken: {fact!r} is no "
                        f"longer in domain {domain_number}'s Ultra Fast "
                        "Track cram sheet",
                    )
                    self.assertIn(
                        fact,
                        cheat_sheet_text,
                        f"{fact!r} is verified content in domain "
                        f"{domain_number}'s Ultra Fast Track cram sheet but "
                        "missing from its cheat sheet",
                    )


class TestCheatSheetsAreDiscoverable(unittest.TestCase):
    """The cheat sheet must be linked from wherever the existing Fast Track
    / Ultra Fast Track links already live: the root README and each
    domain's own Fast Track landing page."""

    def test_root_readme_links_to_a_cheat_sheet(self):
        readme_text = _read(README_PATH)
        self.assertIn("CHEAT-SHEET.md", readme_text)

    def test_each_fast_track_readme_links_to_its_cheat_sheet(self):
        for domain_number, readme_path in FAST_TRACK_READMES.items():
            with self.subTest(domain=domain_number):
                text = _read(readme_path)
                self.assertIn(
                    "](CHEAT-SHEET.md)",
                    text,
                    f"expected domain {domain_number}'s Fast Track README "
                    "to link to its CHEAT-SHEET.md companion",
                )

    def test_each_ultra_fast_learn_links_to_its_cheat_sheet(self):
        for domain_number in CHEAT_SHEETS:
            ultra_path = (
                DOCS_DIR / f"domain-{domain_number}-fast-track" / "ULTRA-FAST-LEARN.md"
            )
            with self.subTest(domain=domain_number):
                text = _read(ultra_path)
                self.assertIn("](CHEAT-SHEET.md)", text)


if __name__ == "__main__":
    unittest.main()
