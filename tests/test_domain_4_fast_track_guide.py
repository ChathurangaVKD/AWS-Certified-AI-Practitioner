"""Structural validation for the Domain 4 Fast Track condensed guide.

The gap this covers: Domain 4 (Guidelines for Responsible AI) is 2,250
lines -- too long for a last-minute, day-before-the-exam re-read -- and,
unlike the full guide's own "## Quick-reference cheat sheet", there was no
standalone, ~40%-length condensed guide a reader could work through start
to finish with its own table of contents, comparison tables, and Mermaid
diagrams. `docs/domain-4-fast-track/README.md` fills that gap. These tests
assert that the fast track file exists, sits in the ~30-45% length band
relative to the source guide, links back to the full guide with resolving
anchors, and actually preserves the source's testable concepts (the 8
responsible AI dimensions, the 6 bias categories, the bias-detection
metrics, the AWS responsible-AI tools, interpretability methods, and
monitoring approaches) as tables and diagrams rather than just asserting
they exist in prose.

Run with:
    python3 -m unittest tests/test_domain_4_fast_track_guide.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_PATH = DOCS_DIR / "domain-4-fast-track" / "README.md"
SOURCE_PATH = DOCS_DIR / "domain-4-guidelines-for-responsible-ai.md"

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
            "expected docs/domain-4-fast-track/README.md to exist",
        )

    def test_source_guide_exists(self):
        self.assertTrue(SOURCE_PATH.is_file())


class TestFastTrackGuideLength(unittest.TestCase):
    """The task calls for a ~30-40% condensation (~850-900 lines against a
    2,250-line source); assert the file is a real condensation, not a
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
        self.assertTrue(self.text.startswith("# Domain 4 Fast Track"))

    def test_links_back_to_full_guide(self):
        self.assertIn(
            "(../domain-4-guidelines-for-responsible-ai.md)",
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
        self.assertGreaterEqual(len(anchors_in_toc), 8)
        real_anchors = _heading_anchors(self.text)
        for anchor in anchors_in_toc:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, real_anchors)

    def test_contains_at_least_two_mermaid_diagrams(self):
        self.assertGreaterEqual(
            self.text.count("```mermaid"),
            2,
            "expected the fast track guide to carry Mermaid diagrams for "
            "the fairness/transparency relationships, per the task",
        )

    def test_contains_at_least_seven_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            7,
            "expected multiple comparison/decision tables (bias-mitigation "
            "techniques, interpretability methods, AWS tools, etc.)",
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
    task: disparate impact, fairness metrics, SageMaker Clarify, and
    monitoring approaches."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_covers_all_eight_responsible_ai_dimensions(self):
        for dimension in [
            "Fairness",
            "Explainability",
            "Privacy and security",
            "Transparency",
            "Veracity and robustness",
            "Governance",
            "Safety",
            "Controllability",
        ]:
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, self.text)

    def test_covers_all_six_bias_categories(self):
        for bias_type in [
            "Sampling bias",
            "Measurement bias",
            "Label bias / human bias",
            "Historical bias",
            "Exclusion bias",
            "Aggregation bias",
        ]:
            with self.subTest(bias_type=bias_type):
                self.assertIn(bias_type, self.text)

    def test_covers_bias_mitigation_stages(self):
        for stage in ["Pre-processing", "In-processing", "Post-processing"]:
            with self.subTest(stage=stage):
                self.assertIn(stage, self.text)

    def test_covers_bias_detection_metrics(self):
        for metric in [
            "Difference in proportions of labels (DPL)",
            "Class imbalance",
            "Disparate impact",
            "Accuracy/recall difference",
        ]:
            with self.subTest(metric=metric):
                self.assertIn(metric, self.text)

    def test_covers_representativeness_bias(self):
        self.assertIn("Representativeness bias", self.text)

    def test_covers_sagemaker_clarify_and_shap(self):
        self.assertIn("Amazon SageMaker Clarify", self.text)
        self.assertIn("SHAP", self.text)

    def test_covers_aws_responsible_ai_tools(self):
        for tool in [
            "Amazon SageMaker Clarify",
            "Amazon SageMaker Model Cards",
            "Guardrails for Amazon Bedrock",
            "AI Service Cards",
            "Amazon A2I",
        ]:
            with self.subTest(tool=tool):
                self.assertIn(tool, self.text)

    def test_covers_monitoring_approaches(self):
        self.assertIn(
            "\n## Monitoring responsible AI in production\n", self.text
        )
        self.assertIn("SageMaker Model Monitor", self.text)

    def test_covers_interpretability_methods(self):
        self.assertIn("Natively interpretable model", self.text)
        self.assertIn("Post-hoc SHAP", self.text)

    def test_covers_legal_and_ethical_considerations(self):
        for category in [
            "Intellectual property",
            "Data privacy",
            "Toxicity",
            "Environmental impact",
        ]:
            with self.subTest(category=category):
                self.assertIn(category, self.text)

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


if __name__ == "__main__":
    unittest.main()
