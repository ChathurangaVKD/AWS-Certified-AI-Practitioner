"""Structural validation for the Domain 2 Ultra Fast Track cram sheet.

The gap this covers: learners doing last-minute review before the exam
need an even denser, single/two-page recall aid than a full domain
guide's own "## Quick-reference cheat sheet" -- something that is bullets
and tables only, with no prose, worked examples, or mini-quizzes to read
through. `docs/domain-2-fast-track/ULTRA-FAST-LEARN.md` fills that gap
for Domain 2 (the largest single knowledge domain on the exam, ~24% of
scored questions). These tests assert that the file exists, is a real
1-2 page condensation (not a stub or a near-duplicate of the full guide),
sticks to the bullets-and-tables-only format the task calls for, links
back to the full guide with resolving anchors, and actually preserves
every testable Domain 2 concept named in the task: transformer
mechanics, foundation-model selection criteria, prompt-engineering
techniques, RAG architecture, common GenAI risks, and an AWS
service-to-use-case table.

Run with:
    python3 -m unittest tests/test_domain_2_ultra_fast_learn.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
ULTRA_FAST_LEARN_PATH = DOCS_DIR / "domain-2-fast-track" / "ULTRA-FAST-LEARN.md"
SOURCE_PATH = DOCS_DIR / "domain-2-fundamentals-of-generative-ai.md"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")


def _read(path):
    return path.read_text(encoding="utf-8")


def _line_count(path):
    return _read(path).count("\n")


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


class TestUltraFastLearnExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            ULTRA_FAST_LEARN_PATH.is_file(),
            "expected docs/domain-2-fast-track/ULTRA-FAST-LEARN.md to exist",
        )

    def test_source_guide_exists(self):
        self.assertTrue(SOURCE_PATH.is_file())


class TestUltraFastLearnLength(unittest.TestCase):
    """The task calls for a 1-2 page cram sheet -- assert it is a real,
    heavily condensed recall aid, not a stub or a near-duplicate copy of
    the 2,000+ line full Domain 2 guide."""

    @classmethod
    def setUpClass(cls):
        cls.ultra_lines = _line_count(ULTRA_FAST_LEARN_PATH)
        cls.source_lines = _line_count(SOURCE_PATH)

    def test_is_substantially_shorter_than_full_source_guide(self):
        # 1-2 pages against a 2,000+ line source is nowhere near even the
        # ~30-45% "Fast Track" condensation band -- keep it well under 25%.
        self.assertLess(self.ultra_lines, self.source_lines * 0.25)

    def test_is_not_a_trivial_stub(self):
        self.assertGreater(self.ultra_lines, 80)


class TestUltraFastLearnStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(ULTRA_FAST_LEARN_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(self.text.startswith("# Domain 2 Ultra Fast Track"))

    def test_links_back_to_full_guide(self):
        self.assertIn(
            "(../domain-2-fundamentals-of-generative-ai.md)",
            self.text,
        )

    def test_has_table_of_contents(self):
        self.assertIn("\n## Table of contents\n", self.text)

    def test_toc_entries_resolve_to_real_headings_in_this_file(self):
        toc_match = re.search(
            r"\n## Table of contents\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(toc_match)
        toc = toc_match.group(1)
        anchors_in_toc = re.findall(r"\]\(#([^)]+)\)", toc)
        self.assertGreaterEqual(len(anchors_in_toc), 6)
        real_anchors = _heading_anchors(self.text)
        for anchor in anchors_in_toc:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, real_anchors)

    def test_contains_at_least_seven_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            7,
            "expected multiple decision/comparison tables (transformer "
            "mechanics, foundation model selection, Nova variants, "
            "prompt-engineering techniques, inference parameters, RAG "
            "architecture, GenAI risks, AWS service/use-case table)",
        )


class TestUltraFastLearnIsBulletsAndTablesOnly(unittest.TestCase):
    """The task explicitly calls for "bullets and tables only (no
    prose)". Flag any non-heading, non-table, non-bullet, non-blockquote
    line that looks like a prose paragraph (long free text not structured
    as a bullet or table row)."""

    @classmethod
    def setUpClass(cls):
        cls.lines = _read(ULTRA_FAST_LEARN_PATH).splitlines()

    def test_no_long_freeform_prose_lines(self):
        allowed_prefixes = ("#", "-", "|", ">", "[", "**Ultra-condensed")
        offending = []
        for line in self.lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("---"):
                continue
            if stripped.startswith(allowed_prefixes):
                continue
            # A short continuation line (e.g. wrapped bullet text) is fine;
            # only flag lines long enough to be a real prose paragraph.
            if len(stripped) > 220:
                offending.append(stripped)
        self.assertEqual(
            offending,
            [],
            "found long freeform prose line(s) in a doc that should be "
            "bullets and tables only: " + repr(offending),
        )


class TestUltraFastLearnCrossReferencesResolve(unittest.TestCase):
    """Every internal link out of the cram sheet must resolve to a real
    file and, if anchored, a real heading in that file."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(ULTRA_FAST_LEARN_PATH)
        all_links = MD_LINK_RE.findall(cls.text)
        cls.links = [
            link
            for link in all_links
            if not link.startswith(("http://", "https://"))
        ]
        cls.anchor_cache = {}

    def _resolve_target_path(self, file_part):
        if file_part == "":
            return ULTRA_FAST_LEARN_PATH
        return (ULTRA_FAST_LEARN_PATH.parent / file_part).resolve()

    def test_has_several_internal_links(self):
        self.assertGreaterEqual(len(self.links), 5)

    def test_every_internal_link_target_file_exists(self):
        for link in self.links:
            file_part = link.split("#", 1)[0]
            with self.subTest(link=link):
                target_path = self._resolve_target_path(file_part)
                self.assertTrue(
                    target_path.is_file(),
                    f"linked file does not exist: {file_part!r} (resolved "
                    f"to {target_path}) in the ultra fast track cram sheet",
                )

    def test_every_internal_anchor_matches_a_real_heading(self):
        for link in self.links:
            if "#" not in link:
                continue
            file_part, anchor = link.split("#", 1)
            if not anchor:
                continue
            with self.subTest(link=link):
                target_path = self._resolve_target_path(file_part)
                cache_key = str(target_path)
                if cache_key not in self.anchor_cache:
                    self.anchor_cache[cache_key] = _heading_anchors(
                        _read(target_path)
                    )
                self.assertIn(
                    anchor,
                    self.anchor_cache[cache_key],
                    f"anchor #{anchor} does not match any heading slug in "
                    f"{target_path} -- the link {link!r} in the cram sheet "
                    "is stale",
                )


class TestUltraFastLearnContent(unittest.TestCase):
    """Every testable Domain 2 concept named in the task must map to at
    least one bullet or table cell."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(ULTRA_FAST_LEARN_PATH)

    def test_covers_transformer_mechanics(self):
        for term in [
            "Tokenization",
            "Embeddings",
            "Positional encoding",
            "Self-attention",
            "Feed-forward network",
            "vector",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_foundation_model_selection_criteria(self):
        for factor in [
            "Cost",
            "Modality",
            "Latency",
            "Context window",
            "Fine-tuning",
        ]:
            with self.subTest(factor=factor):
                self.assertIn(factor, self.text)

    def test_covers_nova_model_variants(self):
        for variant in [
            "Nova Micro",
            "Nova Lite",
            "Nova Pro",
            "Nova Premier",
            "Nova Canvas",
            "Nova Reel",
            "Nova Sonic",
        ]:
            with self.subTest(variant=variant):
                self.assertIn(variant, self.text)

    def test_covers_prompt_engineering_techniques(self):
        for technique in [
            "Zero-shot",
            "Few-shot",
            "Chain-of-thought",
            "Negative prompting",
            "Fine-tuning",
            "Prompt injection",
        ]:
            with self.subTest(technique=technique):
                self.assertIn(technique, self.text)

    def test_covers_inference_parameters(self):
        for param in [
            "Temperature",
            "Top-p",
            "Top-k",
            "Max tokens",
            "Stop sequences",
        ]:
            with self.subTest(param=param):
                self.assertIn(param, self.text)

    def test_covers_rag_architecture(self):
        for term in [
            "Ingest",
            "Chunk + embed",
            "Index",
            "Retrieve",
            "Augment + generate",
            "Knowledge Bases for Amazon Bedrock",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_common_genai_risks(self):
        for risk in [
            "Hallucination",
            "Interpretability",
            "Inaccuracy",
            "Nondeterminism",
            "Cost / compute intensity",
            "Prompt injection",
        ]:
            with self.subTest(risk=risk):
                self.assertIn(risk, self.text)

    def test_covers_aws_service_use_case_table_entries(self):
        for service in [
            "Amazon Bedrock",
            "Knowledge Bases for Amazon Bedrock",
            "Agents for Amazon Bedrock",
            "Guardrails for Amazon Bedrock",
            "Amazon Bedrock Model Evaluation",
            "Provisioned Throughput",
            "Amazon Q Business",
            "Amazon Q Developer",
            "Amazon SageMaker JumpStart",
            "PartyRock",
        ]:
            with self.subTest(service=service):
                self.assertIn(service, self.text)

    def test_has_common_exam_traps_checklist(self):
        self.assertIn("\n## Common exam traps checklist\n", self.text)
        traps_match = re.search(
            r"\n## Common exam traps checklist\n(.*?)(\n## |\Z)",
            self.text,
            re.S,
        )
        self.assertIsNotNone(traps_match)
        bullet_count = traps_match.group(1).count("\n- [ ]")
        self.assertGreaterEqual(bullet_count, 8)

    def test_has_key_terms_section_with_bolded_terms(self):
        key_terms_match = re.search(
            r"\n## Rapid-fire key terms\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(key_terms_match)
        section = key_terms_match.group(1)
        bolded_bullets = re.findall(r"\n- \*\*[^*]+\*\*", section)
        self.assertGreaterEqual(
            len(bolded_bullets),
            15,
            "expected at least 15 bolded key-term bullets in the "
            "rapid-fire key terms section",
        )


if __name__ == "__main__":
    unittest.main()
