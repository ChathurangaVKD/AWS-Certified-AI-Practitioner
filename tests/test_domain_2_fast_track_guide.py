"""Structural validation for the Domain 2 Fast Track condensed guide.

The gap this covers: Domain 2 (Fundamentals of Generative AI) is 2,213
lines and is the largest single domain on the exam (~24% of scored
questions), but -- unlike Domain 4, which has both an Ultra Fast Track
cram sheet and an intermediate ~40%-length Fast Track guide -- Domain 2
only had the Ultra Fast Track cram sheet and its own full guide's
in-guide quick-reference cheat sheet. There was no standalone,
~850-900-line condensed guide a reader could work through start to
finish with its own table of contents, comparison tables, and Mermaid
diagrams sitting between the two. `docs/domain-2-fast-track/README.md`
fills that gap. These tests assert that the fast track file exists, sits
in the ~30-45% length band relative to the source guide, links back to
the full guide with resolving anchors, and actually preserves the
source's testable concepts (transformer mechanics, the embedding-model
selection tree, GenAI advantages/disadvantages, business use cases, AWS
generative AI services, prompt-engineering techniques, inference
parameters, foundation-model selection criteria, and RAG architecture) as
tables and diagrams rather than just asserting they exist in prose.

Run with:
    python3 -m unittest tests/test_domain_2_fast_track_guide.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_PATH = DOCS_DIR / "domain-2-fast-track" / "README.md"
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


class TestFastTrackGuideExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            FAST_TRACK_PATH.is_file(),
            "expected docs/domain-2-fast-track/README.md to exist",
        )

    def test_source_guide_exists(self):
        self.assertTrue(SOURCE_PATH.is_file())


class TestFastTrackGuideLength(unittest.TestCase):
    """The task calls for a ~30-40% condensation (~850-900 lines against a
    2,213-line source); assert the file is a real condensation, not a
    stub or a near-duplicate copy."""

    @classmethod
    def setUpClass(cls):
        cls.fast_track_lines = _line_count(FAST_TRACK_PATH)
        cls.source_lines = _line_count(SOURCE_PATH)

    def test_fast_track_is_substantially_shorter_than_source(self):
        self.assertLess(self.fast_track_lines, self.source_lines * 0.6)

    def test_fast_track_is_not_a_trivial_stub(self):
        self.assertGreater(self.fast_track_lines, self.source_lines * 0.2)


class TestFastTrackGuideStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(self.text.startswith("# Domain 2 Fast Track"))

    def test_links_back_to_full_guide(self):
        self.assertIn(
            "(../domain-2-fundamentals-of-generative-ai.md)",
            self.text,
        )

    def test_links_to_ultra_fast_learn(self):
        self.assertIn("(ULTRA-FAST-LEARN.md)", self.text)

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

    def test_contains_at_least_five_mermaid_diagrams(self):
        self.assertGreaterEqual(
            self.text.count("```mermaid"),
            5,
            "expected the fast track guide to carry Mermaid diagrams for "
            "the transformer pipeline, embedding selection, LLM lifecycle, "
            "RAG flow, and model-selection decision trees, per the task",
        )

    def test_contains_at_least_fifteen_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            15,
            "expected multiple comparison/decision tables (prompt "
            "techniques, inference parameters, model selection criteria, "
            "Nova family, AWS services, RAG steps, etc.)",
        )


class TestFastTrackGuideCrossReferencesResolve(unittest.TestCase):
    """Every internal link out of the fast track guide must resolve to a
    real file and, if anchored, a real heading in that file -- mirroring
    tests/test_cross_reference_links.py's conventions for the five domain
    guides."""

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
        self.assertGreaterEqual(len(self.links), 10)

    def test_every_internal_link_target_file_exists(self):
        for link in self.links:
            file_part = link.split("#", 1)[0]
            with self.subTest(link=link):
                target_path = self._resolve_target_path(file_part)
                self.assertTrue(
                    target_path.is_file(),
                    f"linked file does not exist: {file_part!r} (resolved "
                    f"to {target_path}) in the fast track guide",
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
                    "guide is stale",
                )


class TestFastTrackGuideContent(unittest.TestCase):
    """The fast track guide must keep every testable concept named in the
    task: transformer mechanics, model-selection criteria, prompt
    engineering techniques, RAG architecture, GenAI risks, and AWS
    services."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_covers_transformer_mechanics(self):
        for term in [
            "Tokenization",
            "Embeddings",
            "Positional encoding",
            "Self-attention",
            "Feed-forward",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_embedding_model_selection(self):
        self.assertIn("Choosing an embedding model", self.text)
        for option in [
            "General-purpose model",
            "Domain-specific pretrained",
            "Fine-tune an embedding model",
        ]:
            with self.subTest(option=option):
                self.assertIn(option, self.text)

    def test_covers_prompt_engineering_techniques(self):
        for technique in [
            "Zero-shot prompting",
            "Few-shot prompting",
            "Chain-of-thought (CoT) prompting",
            "Negative prompting",
        ]:
            with self.subTest(technique=technique):
                self.assertIn(technique, self.text)

    def test_covers_inference_parameters(self):
        for parameter in [
            "Temperature",
            "Top-p",
            "Top-k",
            "Max tokens",
            "Stop sequences",
        ]:
            with self.subTest(parameter=parameter):
                self.assertIn(parameter, self.text)

    def test_covers_foundation_model_selection_criteria(self):
        for criterion in [
            "Cost",
            "Modality",
            "Latency",
            "Context window",
            "Fine-tuning / customization support",
        ]:
            with self.subTest(criterion=criterion):
                self.assertIn(criterion, self.text)

    def test_covers_amazon_nova_family(self):
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

    def test_covers_genai_advantages_and_disadvantages(self):
        for concept in [
            "Adaptability",
            "Responsiveness",
            "Scalability",
            "Hallucination",
            "Interpretability (lack of)",
            "Nondeterminism",
            "Cost and compute intensity",
        ]:
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)

    def test_covers_business_use_cases(self):
        for use_case in [
            "Content creation",
            "Summarization",
            "Chatbots / conversational assistants",
            "Code generation",
            "Search",
        ]:
            with self.subTest(use_case=use_case):
                self.assertIn(use_case, self.text)

    def test_covers_aws_generative_ai_services(self):
        for service in [
            "Amazon Bedrock",
            "Knowledge Bases for Amazon Bedrock",
            "Agents for Amazon Bedrock",
            "Guardrails for Amazon Bedrock",
            "Amazon Bedrock Model Evaluation",
            "Amazon Q Business",
            "Amazon Q Developer",
            "Amazon SageMaker JumpStart",
            "PartyRock",
            "Provisioned Throughput",
        ]:
            with self.subTest(service=service):
                self.assertIn(service, self.text)

    def test_covers_rag_architecture_steps(self):
        self.assertIn("\n## RAG architecture at a glance\n", self.text)
        for step in ["Ingest", "Chunk + embed", "Index", "Retrieve"]:
            with self.subTest(step=step):
                self.assertIn(step, self.text)

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
            "expected at least 15 bolded key-term bullets in the rapid-fire "
            "key terms section",
        )

    def test_has_common_exam_traps_checklist(self):
        self.assertIn("\n## Common exam traps checklist\n", self.text)
        traps_match = re.search(
            r"\n## Common exam traps checklist\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(traps_match)
        bullet_count = traps_match.group(1).count("\n- [ ]")
        self.assertGreaterEqual(bullet_count, 8)

    def test_has_line_mapping_table_to_full_guide(self):
        mapping_match = re.search(
            r"\n\| This fast track \| Full guide section \|.*?\n\n",
            self.text,
            re.S,
        )
        self.assertIsNotNone(
            mapping_match,
            "expected a table mapping each condensed section to its "
            "full-guide source section, per the Domain 4 template",
        )


if __name__ == "__main__":
    unittest.main()
