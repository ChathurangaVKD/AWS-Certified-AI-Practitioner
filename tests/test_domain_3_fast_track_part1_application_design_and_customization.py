"""Structural validation for the Domain 3 Fast Track, Part 1 condensed guide.

The gap this covers: Domain 3 (Applications of Foundation Models) is the
exam's heaviest-weighted domain (~28%) at 6,845 lines -- far too large for
a single condensed Fast Track guide. Its Fast Track is split into three
parts along the source's own section boundaries, the same way Part 3
(production deployment/troubleshooting) already is, to avoid the
oversized-single-PR pattern seen with prior condensed-guide opportunities
(1,100-1,450 changed lines).

This is part 1 of 3:
`docs/domain-3-fast-track/part-1-application-design-and-customization.md`,
covering FM application design considerations (Section 1: model
selection, cost/latency/modality trade-offs, multi-model routing and
fallback strategies) and all six customization methods a scenario can ask
a candidate to choose between: prompt engineering, RAG, fine-tuning,
LoRA/QLoRA, RLHF, and continued pre-training (Sections 2-4), each
condensed into comparison tables, decision trees/flowcharts, and bolded
key terms that link back to the corresponding section of the full guide.

These tests assert the file exists, sits in a real-condensation length
band (not a stub, not a near-verbatim copy of the much larger ~2,187-line
source slice), links back to the full guide with resolving anchors,
carries multiple Mermaid decision trees, and actually preserves every
testable decision point named in the task -- not just mentions each
technique's name somewhere in prose.

Run with:
    python3 -m unittest tests/test_domain_3_fast_track_part1_application_design_and_customization.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_PATH = (
    DOCS_DIR
    / "domain-3-fast-track"
    / "part-1-application-design-and-customization.md"
)
SOURCE_PATH = DOCS_DIR / "domain-3-applications-of-foundation-models.md"

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


class TestFastTrackPart1Exists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            FAST_TRACK_PATH.is_file(),
            "expected docs/domain-3-fast-track/part-1-application-design-"
            "and-customization.md to exist",
        )

    def test_source_guide_exists(self):
        self.assertTrue(SOURCE_PATH.is_file())


class TestFastTrackPart1Length(unittest.TestCase):
    """The task calls for ~850-900 lines; assert the file is a real,
    substantial condensation -- not a stub and not a near-duplicate of the
    full guide's much larger relevant section (Sections 1-4, ~2,187
    lines)."""

    @classmethod
    def setUpClass(cls):
        cls.fast_track_lines = _line_count(FAST_TRACK_PATH)
        cls.source_lines = _line_count(SOURCE_PATH)

    def test_fast_track_is_in_the_target_length_band(self):
        self.assertGreaterEqual(self.fast_track_lines, 700)
        self.assertLessEqual(self.fast_track_lines, 1000)

    def test_fast_track_is_substantially_shorter_than_full_source_guide(self):
        self.assertLess(self.fast_track_lines, self.source_lines * 0.2)


class TestFastTrackPart1Structure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(
            self.text.startswith("# Domain 3 Fast Track, Part 1")
        )

    def test_links_back_to_full_guide(self):
        self.assertIn(
            "(../domain-3-applications-of-foundation-models.md)",
            self.text,
        )

    def test_identifies_itself_as_part_1_of_3(self):
        self.assertIn("part 1 of 3", self.text)

    def test_has_table_of_contents(self):
        self.assertIn("\n## Table of contents\n", self.text)

    def test_toc_entries_resolve_to_real_headings_in_this_file(self):
        toc_match = re.search(
            r"\n## Table of contents\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(toc_match)
        toc = toc_match.group(1)
        anchors_in_toc = re.findall(r"\]\(#([^)]+)\)", toc)
        self.assertGreaterEqual(len(anchors_in_toc), 8)
        real_anchors = _heading_anchors(self.text)
        for anchor in anchors_in_toc:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, real_anchors)

    def test_contains_several_mermaid_diagrams(self):
        self.assertGreaterEqual(
            self.text.count("```mermaid"),
            4,
            "expected several Mermaid decision trees/flowcharts for "
            "routing, the customization decision framework, and the "
            "fine-tuning efficiency technique choice, per the task",
        )

    def test_contains_many_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            15,
            "expected multiple comparison/decision/checklist tables",
        )


class TestFastTrackPart1CrossReferencesResolve(unittest.TestCase):
    """Every internal link out of this fast track part must resolve to a
    real file and, if anchored, a real heading in that file."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)
        all_links = MD_LINK_RE.findall(cls.text)
        cls.links = [
            link
            for link in all_links
            if not link.startswith(("http://", "https://"))
        ]
        cls.anchor_cache = {}

    def _resolve_target_path(self, file_part):
        if file_part == "":
            return FAST_TRACK_PATH
        return (FAST_TRACK_PATH.parent / file_part).resolve()

    def test_has_several_internal_links(self):
        self.assertGreaterEqual(len(self.links), 15)

    def test_every_internal_link_target_file_exists(self):
        for link in self.links:
            file_part = link.split("#", 1)[0]
            with self.subTest(link=link):
                target_path = self._resolve_target_path(file_part)
                self.assertTrue(
                    target_path.is_file(),
                    f"linked file does not exist: {file_part!r} (resolved "
                    f"to {target_path}) in the fast track part 1 guide",
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
                    f"{target_path} -- the link {link!r} in the fast track "
                    "part 1 guide is stale",
                )


class TestFastTrackPart1Content(unittest.TestCase):
    """The fast track part must keep every testable decision point named
    in the task: FM application design considerations, multi-model
    routing/fallback, prompt engineering techniques, RAG fundamentals, and
    all six customization methods (prompt engineering, RAG, fine-tuning,
    LoRA/QLoRA, RLHF, continued pre-training)."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_covers_design_consideration_factors(self):
        for term in ["Model selection", "Cost", "Latency", "Modality"]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_context_window_model_tier_table(self):
        for model in [
            "Claude Haiku",
            "Claude Sonnet",
            "Claude Opus",
            "Llama 8B",
            "Llama 70B",
        ]:
            with self.subTest(model=model):
                self.assertIn(model, self.text)

    def test_covers_routing_strategies(self):
        for strategy in [
            "STRICT ROUTING",
            "BEST-EFFORT ROUTING",
            "FALLBACK CHAIN",
        ]:
            with self.subTest(strategy=strategy):
                self.assertIn(strategy, self.text)

    def test_covers_fallback_check_order(self):
        # The exact ordering phrase the exam tests: availability is
        # checked first, then rate limits, then cost as a tie-breaker.
        self.assertIn("availability → rate limits → cost", self.text)

    def test_covers_all_eight_prompt_engineering_techniques(self):
        for technique in [
            "Zero-shot prompting",
            "Few-shot prompting",
            "Chain-of-thought (CoT) prompting",
            "Prompt templates",
            "Negative prompting",
            "Prompt chaining",
            "System prompts",
            "Prompt injection",
        ]:
            with self.subTest(technique=technique):
                self.assertIn(technique, self.text)

    def test_covers_rag_pipeline_stages(self):
        for stage in [
            "Ingestion",
            "Chunking",
            "Embedding",
            "Indexing/storage",
            "Retrieval",
            "Augmentation and generation",
        ]:
            with self.subTest(stage=stage):
                self.assertIn(stage, self.text)

    def test_covers_knowledge_bases_apis(self):
        self.assertIn("`Retrieve`", self.text)
        self.assertIn("`RetrieveAndGenerate`", self.text)

    def test_covers_all_six_customization_methods(self):
        for method in [
            "Prompt engineering",
            "RAG",
            "Fine-tuning",
            "LoRA",
            "QLoRA",
            "RLHF",
            "Continued pre-training",
        ]:
            with self.subTest(method=method):
                self.assertIn(method, self.text)

    def test_covers_fine_tuning_efficiency_techniques(self):
        for term in [
            "Full fine-tuning",
            "Low-Rank Adaptation",
            "Quantized LoRA",
            "Instruction tuning",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_qlora_serving_tradeoff(self):
        self.assertIn("merged", self.text)
        self.assertIn("unmerged", self.text)
        self.assertIn(
            "can't be both low-memory and low-latency at serving time",
            self.text,
        )

    def test_covers_rlhf_three_stages(self):
        self.assertIn("reward model", self.text.lower())
        self.assertIn("Proximal Policy Optimization", self.text)
        self.assertIn("Supervised fine-tuning (SFT)", self.text)

    def test_covers_dataset_size_thresholds(self):
        self.assertIn("~100-500", self.text)
        self.assertIn("catastrophic forgetting", self.text.lower())

    def test_covers_data_quality_checklist(self):
        for item in [
            "Diversity",
            "Edge-case coverage",
            "Label correctness",
            "Class/category balance",
        ]:
            with self.subTest(item=item):
                self.assertIn(item, self.text)

    def test_covers_synthetic_vs_real_data(self):
        self.assertIn("Synthetic data", self.text)
        self.assertIn("Real (human-produced) data", self.text)

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

    def test_has_common_exam_traps_checklist(self):
        self.assertIn("\n## Common exam traps checklist\n", self.text)
        traps_match = re.search(
            r"\n## Common exam traps checklist\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(traps_match)
        bullet_count = traps_match.group(1).count("\n- [ ]")
        self.assertGreaterEqual(bullet_count, 8)

    def test_has_rapid_self_check_with_many_questions(self):
        self.assertIn("\n## Rapid self-check\n", self.text)
        self_check_match = re.search(
            r"\n## Rapid self-check\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(self_check_match)
        question_rows = re.findall(
            r"\n\|\s*\d+\s*\|", self_check_match.group(1)
        )
        self.assertGreaterEqual(len(question_rows), 10)

    def test_has_where_each_section_comes_from_mapping_table(self):
        self.assertIn("Where each section comes from", self.text)

    def test_references_part_3_and_reserves_part_2(self):
        self.assertIn("part-3-deployment-and-troubleshooting.md", self.text)
        self.assertIn("Part 2", self.text)


if __name__ == "__main__":
    unittest.main()
