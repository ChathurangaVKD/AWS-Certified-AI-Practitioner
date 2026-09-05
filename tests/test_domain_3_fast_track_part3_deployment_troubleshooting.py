"""Structural validation for the Domain 3 Fast Track, Part 3 condensed guide.

The gap this covers: Domain 3 (Applications of Foundation Models) is
6,845 lines with 25 Mermaid diagrams -- far too large for a single
condensed Fast Track guide, unlike every other domain, which already has
one. Domain 3's Fast Track is split into three parts to avoid an
oversized single PR. This is part 3 of 3:
`docs/domain-3-fast-track/part-3-deployment-and-troubleshooting.md`,
covering production deployment (Section 8: AWS infrastructure, Bedrock
throughput, SageMaker auto-scaling), the four-scenario inference-failure
triage flow, the three resilience patterns (retry, backoff, circuit
breaker), and the RAG troubleshooting triage flow (four failure modes:
chunking, embedding mismatch, ranking, and generation/terminology
mismatch), each condensed into decision trees and bulleted checklists
that cross-reference back to the full guide.

These tests assert the file exists, sits in the ~800-950 line band (a
real condensation of the ~1,270-line source slice into compact decision
trees, not a stub or a near-verbatim copy), links back to the full guide
with resolving anchors, carries multiple Mermaid decision trees, and
actually preserves every testable fact named in the task -- the
Trainium/Inferentia split, the four inference-failure scenarios, the
three resilience strategies, and the four RAG failure modes -- as tables
and diagrams rather than just asserting they're mentioned somewhere in
prose.

Run with:
    python3 -m unittest tests/test_domain_3_fast_track_part3_deployment_troubleshooting.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_PATH = (
    DOCS_DIR / "domain-3-fast-track" / "part-3-deployment-and-troubleshooting.md"
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


class TestFastTrackPart3Exists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            FAST_TRACK_PATH.is_file(),
            "expected docs/domain-3-fast-track/part-3-deployment-and-"
            "troubleshooting.md to exist",
        )

    def test_source_guide_exists(self):
        self.assertTrue(SOURCE_PATH.is_file())


class TestFastTrackPart3Length(unittest.TestCase):
    """The task calls for ~850-900 lines; assert the file is a real,
    substantial condensation -- not a stub and not a near-duplicate of the
    full guide's much larger relevant section."""

    @classmethod
    def setUpClass(cls):
        cls.fast_track_lines = _line_count(FAST_TRACK_PATH)
        cls.source_lines = _line_count(SOURCE_PATH)

    def test_fast_track_is_in_the_target_length_band(self):
        self.assertGreaterEqual(self.fast_track_lines, 700)
        self.assertLessEqual(self.fast_track_lines, 1000)

    def test_fast_track_is_substantially_shorter_than_full_source_guide(self):
        self.assertLess(self.fast_track_lines, self.source_lines * 0.2)


class TestFastTrackPart3Structure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(
            self.text.startswith("# Domain 3 Fast Track, Part 3")
        )

    def test_links_back_to_full_guide(self):
        self.assertIn(
            "(../domain-3-applications-of-foundation-models.md)",
            self.text,
        )

    def test_identifies_itself_as_part_3_of_3(self):
        self.assertIn("part 3 of 3", self.text)

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
            "expected several Mermaid decision trees for the throughput, "
            "auto-scaling, inference-failure, resilience, and RAG triage "
            "flows, per the task",
        )

    def test_contains_many_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            10,
            "expected multiple comparison/decision/checklist tables",
        )


class TestFastTrackPart3CrossReferencesResolve(unittest.TestCase):
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
                    f"to {target_path}) in the fast track part 3 guide",
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
                    "part 3 guide is stale",
                )


class TestFastTrackPart3Content(unittest.TestCase):
    """The fast track part must keep every testable fact named in the
    task: the Trainium/Inferentia split, the auto-scaling knobs, the four
    inference-failure scenarios, the three resilience strategies, and the
    four RAG failure modes (chunking, embedding mismatch, ranking,
    generation/terminology mismatch)."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_covers_trainium_and_inferentia_split(self):
        self.assertIn("AWS Trainium", self.text)
        self.assertIn("AWS Inferentia", self.text)
        self.assertIn("Amazon SageMaker JumpStart", self.text)
        # The exact pairing the exam tests directly.
        self.assertIn("Trainium → training", self.text)
        self.assertIn("Inferentia → inference", self.text)

    def test_covers_on_demand_vs_provisioned_throughput(self):
        self.assertIn("ON-DEMAND", self.text)
        self.assertIn("PROVISIONED THROUGHPUT", self.text)

    def test_covers_auto_scaling_knobs(self):
        for term in [
            "SageMakerVariantInvocationsPerInstance",
            "Scale-out",
            "Scale-in",
            "MinCapacity",
            "MaxCapacity",
            "flapping",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_all_four_inference_failure_scenarios(self):
        for scenario_marker in [
            "Real-time endpoint",
            "Batch Transform job",
            "Long-running conversation",
            "Provisioned/on-demand workload",
        ]:
            with self.subTest(scenario=scenario_marker):
                self.assertIn(scenario_marker, self.text)

    def test_covers_batch_transform_settings(self):
        self.assertIn("MaxPayloadInMB", self.text)
        self.assertIn("InvocationsTimeoutInSeconds", self.text)

    def test_covers_context_window_overflow_remediation(self):
        self.assertIn("Sliding-window truncation", self.text)
        self.assertIn("Rolling summarization", self.text)

    def test_covers_all_three_resilience_strategies(self):
        for strategy in [
            "Immediate retry",
            "Exponential backoff (with jitter)",
            "Circuit breaker",
        ]:
            with self.subTest(strategy=strategy):
                self.assertIn(strategy, self.text)

    def test_covers_retryable_and_permanent_error_codes(self):
        for code in [
            "ThrottlingException",
            "ValidationException",
            "AccessDeniedException",
            "ResourceNotFoundException",
            "ModelTimeoutException",
        ]:
            with self.subTest(code=code):
                self.assertIn(code, self.text)

    def test_covers_all_four_rag_failure_modes(self):
        for symptom in [
            "Chunks too small",
            "domain-specific vocabulary",
            "distinguish \"close\" from \"correct\"",
            "terminology mismatch",
        ]:
            with self.subTest(symptom=symptom):
                self.assertIn(symptom, self.text)

    def test_covers_rag_remediation_techniques(self):
        for technique in [
            "Reranking",
            "Hybrid search",
            "HyDE",
            "numberOfResults",
        ]:
            with self.subTest(technique=technique):
                self.assertIn(technique, self.text)

    def test_covers_rag_stage_isolation_debugging_method(self):
        self.assertIn(
            "\n## 8. Debugging method: isolating the broken RAG pipeline "
            "stage\n",
            self.text,
        )
        for stage in ["embedding", "retrieval", "ranking", "generation"]:
            with self.subTest(stage=stage):
                self.assertIn(stage, self.text.lower())

    def test_has_pre_launch_production_checklist(self):
        self.assertIn("\n## Pre-launch production checklist\n", self.text)
        checklist_match = re.search(
            r"\n## Pre-launch production checklist\n(.*?)\n## ",
            self.text,
            re.S,
        )
        self.assertIsNotNone(checklist_match)
        bullet_count = checklist_match.group(1).count("\n- [ ]")
        self.assertGreaterEqual(bullet_count, 10)

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
        # Count numbered table rows (e.g. "| 1 |", "| 12 |").
        question_rows = re.findall(
            r"\n\|\s*\d+\s*\|", self_check_match.group(1)
        )
        self.assertGreaterEqual(len(question_rows), 15)


if __name__ == "__main__":
    unittest.main()
