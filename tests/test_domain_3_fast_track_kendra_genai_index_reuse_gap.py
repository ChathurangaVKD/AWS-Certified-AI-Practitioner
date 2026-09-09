"""Structural validation for the Domain 3 Fast Track's Kendra GenAI Index
reuse-over-duplicate fix.

The gap this covers: docs/domain-3-fast-track/COVERAGE-VERIFICATION-REPORT.md
(Finding 1) identified a hop-1 gap -- the full guide's worked example
(lines 1208-1405 of docs/domain-3-applications-of-foundation-models.md)
showing that a Bedrock Knowledge Base can reuse an existing **Kendra
GenAI Index** as its retriever, instead of provisioning a separate
OpenSearch/Aurora vector store, fell through the gap between Part 1,
Section 4 (which defers vector-store depth to Part 2) and Part 2,
Section 4 (which linked only to the full guide's general-purpose
Section 6, never to Section 3's worked example where the fact actually
lives). The concept survived independently into ULTRA-FAST-LEARN.md
(lines 117 and 332), so a reader who only read Part 1 + Part 2, as the
Fast Track's own reading order instructs, would never encounter it,
while a reader who skipped straight to the cram sheet would.

These tests assert that docs/domain-3-fast-track/part-2-inference-and-
multimodal.md, Section 4 now states the reuse-over-duplicate decision
rule (sourced from ULTRA-FAST-LEARN.md lines 117 and 332) with a
concrete compliance-document Q&A example, links to the full guide's
Kendra GenAI Index worked example with a resolving anchor, and that the
Fast Track README's "Where each section comes from" table reflects the
same full-guide line range (1208-1405).

Run with:
    python3 -m unittest tests/test_domain_3_fast_track_kendra_genai_index_reuse_gap.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_DIR = DOCS_DIR / "domain-3-fast-track"
PART2_PATH = FAST_TRACK_DIR / "part-2-inference-and-multimodal.md"
README_PATH = FAST_TRACK_DIR / "README.md"
ULTRA_FAST_LEARN_PATH = FAST_TRACK_DIR / "ULTRA-FAST-LEARN.md"
SOURCE_PATH = DOCS_DIR / "domain-3-applications-of-foundation-models.md"

WORKED_EXAMPLE_ANCHOR = (
    "worked-example-building-a-product-knowledge-assistant-using-"
    "kendras-genai-index-as-a-bedrock-knowledge-base-data-source"
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _slugify(heading_text):
    """Approximate the GitHub markdown heading-anchor algorithm (same
    convention used across the fast-track test suite)."""
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = s.replace(" ", "-")
    return s


def _heading_anchors(doc_text):
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


def _section(text, start_heading, end_heading_regex=r"\n## "):
    start = text.index(start_heading)
    rest = text[start + len(start_heading):]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestKendraReuseFactSourcedFromUltraFastLearn(unittest.TestCase):
    """Confirm the two source facts actually exist in ULTRA-FAST-LEARN.md
    (lines 117 and 332 per the coverage report) so the new subsection can
    be checked against them verbatim."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(ULTRA_FAST_LEARN_PATH)

    def test_line_117_area_states_reuse_fact(self):
        self.assertIn(
            "A Knowledge Base\n  can also reuse an existing "
            "**Kendra GenAI Index** as its retriever",
            self.text,
        )

    def test_line_332_area_states_reuse_fact(self):
        self.assertIn(
            "Reuse an existing **Kendra GenAI Index** as a Knowledge Base's\n"
            "      retriever when one already exists",
            self.text,
        )


class TestPart2VectorStoreSectionCoversKendraReuse(unittest.TestCase):
    """Part 2, Section 4 (vector databases and embeddings) must now state
    the reuse-over-duplicate rule with a concrete example, matching the
    facts already independently present in ULTRA-FAST-LEARN.md."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(PART2_PATH)
        cls.section = _section(
            cls.text,
            "## 4. Vector databases and embeddings: choosing a backend",
        )

    def test_file_exists(self):
        self.assertTrue(PART2_PATH.is_file())

    def test_section_mentions_kendra_genai_index_reuse(self):
        self.assertIn("Kendra GenAI Index", self.section)
        self.assertIn("reuse", self.section.lower())

    def test_section_states_the_decision_rule_over_provisioning_second_store(
        self,
    ):
        # The exam-tested rule: reuse an existing index rather than
        # standing up a second OpenSearch/Aurora vector store.
        self.assertRegex(
            self.section,
            re.compile(
                r"reuse.{0,80}Kendra GenAI Index", re.I | re.S
            ),
        )
        self.assertIn("OpenSearch", self.section)
        self.assertIn("Aurora", self.section)

    def test_section_has_concrete_compliance_document_qa_example(self):
        self.assertIn("compliance", self.section.lower())
        self.assertIn("pgvector", self.section)

    def test_section_links_to_full_guide_kendra_worked_example(self):
        self.assertIn(f"#{WORKED_EXAMPLE_ANCHOR}", self.section)

    def test_worked_example_link_anchor_resolves_in_source_guide(self):
        source_text = _read(SOURCE_PATH)
        self.assertIn(
            WORKED_EXAMPLE_ANCHOR,
            _heading_anchors(source_text),
            "the Kendra GenAI Index worked-example anchor linked from "
            "Part 2 must resolve to a real heading in the full guide",
        )


class TestReadmeSectionMappingTableReflectsWorkedExample(unittest.TestCase):
    """The Fast Track README's 'Where each section comes from' table row
    for Part 2, Section 4 must now cite the Kendra GenAI Index worked
    example and its full-guide line range (1208-1405)."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(README_PATH)

    def test_readme_exists(self):
        self.assertTrue(README_PATH.is_file())

    def test_row_for_part2_section4_cites_worked_example_and_line_range(self):
        row_match = re.search(
            r"\|\s*2\s*\|\s*4\.\s*Vector databases and embeddings[^\n]*\n",
            self.text,
        )
        self.assertIsNotNone(
            row_match,
            "expected a 'Where each section comes from' row for Part 2, "
            "Section 4 (Vector databases and embeddings)",
        )
        row = row_match.group(0)
        self.assertIn(f"#{WORKED_EXAMPLE_ANCHOR}", row)
        self.assertIn("1208-1405", row)

    def test_row_anchor_resolves_in_source_guide(self):
        source_text = _read(SOURCE_PATH)
        self.assertIn(WORKED_EXAMPLE_ANCHOR, _heading_anchors(source_text))


if __name__ == "__main__":
    unittest.main()
