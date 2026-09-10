"""Structural validation for the Domain 3 Fast Track, Part 2 condensed guide.

The gap this covers: Domain 3 (Applications of Foundation Models) is the
exam's heaviest-weighted domain (~28%) at 6,845 lines -- far too large for
a single condensed Fast Track guide. Its Fast Track is split into three
parts along the source's own section boundaries: Part 1 (published)
covers Sections 1-4, and Part 3 (published) covers Section 8 onward. This
is Part 2 -- the previously missing middle third --
`docs/domain-3-fast-track/part-2-inference-and-multimodal.md`, covering
Sections 5-7: Amazon Bedrock's inference architecture (model access,
Agents vs. Prompt Flows vs. prompt chaining, Guardrails and
prompt-injection prevention, cost governance, and the
on-demand/provisioned-throughput/batch capacity decision), vector
databases and embeddings (including multi-modal embeddings and
multi-modal RAG retrieval/token-budgeting patterns), and evaluating
foundation model performance -- each condensed into comparison tables,
decision trees, and bolded key terms that link back to the corresponding
section of the full guide.

These tests assert the file exists, sits in a real-condensation length
band (not a stub, not a near-verbatim copy of the much larger source
slice), links back to the full guide with resolving anchors, carries
multiple Mermaid decision trees, and actually preserves every testable
decision point named in the task -- not just mentions each concept's name
somewhere in prose. They also assert Part 1 and Part 3 were updated to
stop calling Part 2 "not yet published" now that it exists.

Run with:
    python3 -m unittest tests/test_domain_3_fast_track_part2_inference_and_multimodal.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_PATH = (
    DOCS_DIR / "domain-3-fast-track" / "part-2-inference-and-multimodal.md"
)
SOURCE_PATH = DOCS_DIR / "domain-3-applications-of-foundation-models.md"
PART1_PATH = (
    DOCS_DIR
    / "domain-3-fast-track"
    / "part-1-application-design-and-customization.md"
)
PART3_PATH = (
    DOCS_DIR
    / "domain-3-fast-track"
    / "part-3-deployment-and-troubleshooting.md"
)

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")


def _read(path):
    return path.read_text(encoding="utf-8")


def _line_count(path):
    return _read(path).count("\n")


def _slugify(heading_text):
    """Approximate the GitHub markdown heading-anchor algorithm: lowercase,
    strip characters that aren't word characters/spaces/hyphens, then turn
    runs of whitespace into single hyphens. Matches the convention used by
    tests/test_cross_reference_links.py and the rest of this repo's link
    tests, which is also what every hand-authored link in this doc set was
    written against."""
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def _heading_anchors(doc_text):
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


class TestFastTrackPart2Exists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            FAST_TRACK_PATH.is_file(),
            "expected docs/domain-3-fast-track/"
            "part-2-inference-and-multimodal.md to exist",
        )

    def test_source_guide_exists(self):
        self.assertTrue(SOURCE_PATH.is_file())


class TestFastTrackPart2Length(unittest.TestCase):
    """The task calls for ~850-900 lines; assert the file is a real,
    substantial condensation -- not a stub and not a near-duplicate of the
    full guide's much larger relevant section (Sections 5-7 plus the
    multi-modal worked examples, ~2,200 lines)."""

    @classmethod
    def setUpClass(cls):
        cls.fast_track_lines = _line_count(FAST_TRACK_PATH)
        cls.source_lines = _line_count(SOURCE_PATH)

    def test_fast_track_is_in_the_target_length_band(self):
        self.assertGreaterEqual(self.fast_track_lines, 650)
        self.assertLessEqual(self.fast_track_lines, 1000)

    def test_fast_track_is_substantially_shorter_than_full_source_guide(self):
        self.assertLess(self.fast_track_lines, self.source_lines * 0.2)


class TestFastTrackPart2Structure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(
            self.text.startswith("# Domain 3 Fast Track, Part 2")
        )

    def test_links_back_to_full_guide(self):
        self.assertIn(
            "(../domain-3-applications-of-foundation-models.md)",
            self.text,
        )

    def test_identifies_itself_as_part_2_of_3(self):
        self.assertIn("part 2 of 3", self.text)

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
            5,
            "expected several Mermaid decision trees for Guardrails rule "
            "selection, orchestration choice, capacity planning, vector "
            "database selection, embedding model selection, reranking/"
            "hybrid search, retrieval metric choice, and evaluation "
            "approach, per the task",
        )

    def test_contains_many_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            15,
            "expected multiple comparison/decision/checklist tables",
        )


class TestFastTrackPart2CrossReferencesResolve(unittest.TestCase):
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
                    f"to {target_path}) in the fast track part 2 guide",
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
                    "part 2 guide is stale",
                )


class TestFastTrackPart2Content(unittest.TestCase):
    """The fast track part must keep every testable decision point named
    in the task: Bedrock inference architecture, multi-modal application
    patterns, and prompt-injection prevention guidance."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_covers_bedrock_orchestration_options(self):
        for term in [
            "Amazon Bedrock Agents",
            "Amazon Bedrock Prompt Flows",
            "prompt chaining",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_all_five_guardrails_rule_types(self):
        for rule_type in [
            "Sensitive information filters",
            "Word filters",
            "Denied topics",
            "Content filters",
            "Contextual grounding checks",
        ]:
            with self.subTest(rule_type=rule_type):
                self.assertIn(rule_type, self.text)

    def test_has_dedicated_prompt_injection_prevention_section(self):
        self.assertIn("\n### Preventing prompt injection\n", self.text)

    def test_covers_direct_and_indirect_prompt_injection(self):
        self.assertIn("directly", self.text)
        self.assertIn("indirectly", self.text)
        self.assertIn("indirect prompt injection", self.text.lower())

    def test_covers_prompt_injection_prevention_checklist_items(self):
        section_match = re.search(
            r"\n### Preventing prompt injection\n(.*?)\n> \*\*Exam tip",
            self.text,
            re.S,
        )
        self.assertIsNotNone(section_match)
        section = section_match.group(1)
        for item in [
            "Content filters",
            "untrusted",
            "Least-privilege",
            "Contextual grounding checks",
            "Output validation",
        ]:
            with self.subTest(item=item):
                self.assertIn(item, section)

    def test_covers_capacity_decision_options(self):
        for option in [
            "On-demand real-time",
            "Provisioned throughput",
            "Bedrock batch inference",
        ]:
            with self.subTest(option=option):
                self.assertIn(option, self.text)

    def test_covers_max_tokens_cost_control(self):
        self.assertIn("Max tokens", self.text)

    def test_covers_vector_database_options(self):
        for option in [
            "Amazon OpenSearch",
            "pgvector",
            "Amazon Kendra",
        ]:
            with self.subTest(option=option):
                self.assertIn(option, self.text)

    def test_covers_embedding_model_tiers(self):
        for tier in [
            "General-purpose",
            "Domain-specific pretrained",
            "Fine-tuned on your own data",
        ]:
            with self.subTest(tier=tier):
                self.assertIn(tier, self.text)

    def test_covers_reranking_and_hybrid_search(self):
        self.assertIn("Reranking", self.text)
        self.assertIn("Hybrid (vector + keyword) search", self.text)
        self.assertIn("Cohere Rerank", self.text)

    def test_covers_multimodal_embedding_model(self):
        self.assertIn("Amazon Titan Multimodal Embeddings", self.text)

    def test_covers_dual_index_vs_single_index_multimodal_patterns(self):
        self.assertIn(
            "dual embedding indexes", self.text.lower().replace("-", " ")
        )
        self.assertIn("single combined multimodal index", self.text)
        self.assertIn("Reciprocal Rank Fusion", self.text)

    def test_covers_multimodal_token_budgeting_options(self):
        for option in [
            "Text summary only",
            "OCR/extract to structured text",
            "Raw image embed",
        ]:
            with self.subTest(option=option):
                self.assertIn(option, self.text)

    def test_covers_retrieval_quality_metrics(self):
        for metric in ["Recall@k", "MRR", "MAP", "NDCG@k"]:
            with self.subTest(metric=metric):
                self.assertIn(metric, self.text)

    def test_covers_three_evaluation_approaches(self):
        for approach in [
            "Human evaluation",
            "Benchmark datasets",
            "Business metrics",
        ]:
            with self.subTest(approach=approach):
                self.assertIn(approach, self.text)

    def test_covers_named_benchmarks(self):
        for benchmark in ["MMLU", "ARC", "HumanEval", "GSM8K"]:
            with self.subTest(benchmark=benchmark):
                self.assertIn(benchmark, self.text)

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

    def test_references_part_1_and_part_3(self):
        self.assertIn(
            "part-1-application-design-and-customization.md", self.text
        )
        self.assertIn("part-3-deployment-and-troubleshooting.md", self.text)


class TestFastTrackTrilogyCrossLinks(unittest.TestCase):
    """Part 1 and Part 3 both promised a future Part 2; now that it
    exists, they should point to it instead of calling it unpublished."""

    def test_part1_links_to_part2_and_no_longer_calls_it_unpublished(self):
        text = _read(PART1_PATH)
        self.assertIn("part-2-inference-and-multimodal.md", text)
        self.assertNotIn("not yet published", text)

    def test_part3_links_to_part1_and_part2(self):
        text = _read(PART3_PATH)
        self.assertIn(
            "part-1-application-design-and-customization.md", text
        )
        self.assertIn("part-2-inference-and-multimodal.md", text)


if __name__ == "__main__":
    unittest.main()
