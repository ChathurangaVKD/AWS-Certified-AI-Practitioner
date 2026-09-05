"""Structural validation for the Domain 1 Fast Track condensed guide.

The gap this covers: Domain 1 (Fundamentals of AI and ML) is 2,030 lines --
the largest single domain guide, at roughly 20% of scored exam questions --
too long for a last-minute, day-before-the-exam re-read. Unlike the full
guide's own "## Quick-reference cheat sheet" (line 1524) or the ultra-dense
bullets-only `ULTRA-FAST-LEARN.md` cram sheet, there was no standalone,
~40%-length condensed guide a reader could work through start to finish
with its own table of contents, comparison tables, and Mermaid diagrams.
`docs/domain-1-fast-track/README.md` fills that gap. These tests assert
that the fast track file exists, sits in the ~20-60% length band relative
to the source guide, links back to the full guide (and to
ULTRA-FAST-LEARN.md) with resolving anchors, and actually preserves the
source's testable concepts (the AI/ML/DL hierarchy, the 8-stage ML
lifecycle, the three learning types, the domain's AWS managed services,
model evaluation metrics, the bias-variance trade-off, and ensemble
methods) as tables and diagrams rather than just asserting they exist in
prose.

Run with:
    python3 -m unittest tests/test_domain_1_fast_track_guide.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_PATH = DOCS_DIR / "domain-1-fast-track" / "README.md"
SOURCE_PATH = DOCS_DIR / "domain-1-fundamentals-of-ai-and-ml.md"
ULTRA_FAST_LEARN_PATH = DOCS_DIR / "domain-1-fast-track" / "ULTRA-FAST-LEARN.md"

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
            "expected docs/domain-1-fast-track/README.md to exist",
        )

    def test_source_guide_exists(self):
        self.assertTrue(SOURCE_PATH.is_file())

    def test_ultra_fast_learn_still_exists(self):
        self.assertTrue(
            ULTRA_FAST_LEARN_PATH.is_file(),
            "adding the fast track README should not remove the existing "
            "ultra-condensed cram sheet -- both should coexist",
        )


class TestFastTrackGuideLength(unittest.TestCase):
    """The task calls for a ~40% condensation (~800-1,000 lines against a
    2,030-line source); assert the file is a real condensation, not a
    stub or a near-duplicate copy."""

    @classmethod
    def setUpClass(cls):
        cls.fast_track_lines = _line_count(FAST_TRACK_PATH)
        cls.source_lines = _line_count(SOURCE_PATH)

    def test_fast_track_is_substantially_shorter_than_source(self):
        self.assertLess(self.fast_track_lines, self.source_lines * 0.6)

    def test_fast_track_is_not_a_trivial_stub(self):
        self.assertGreater(self.fast_track_lines, self.source_lines * 0.2)

    def test_fast_track_is_longer_than_the_ultra_condensed_cram_sheet(self):
        ultra_lines = _line_count(ULTRA_FAST_LEARN_PATH)
        self.assertGreater(
            self.fast_track_lines,
            ultra_lines,
            "the ~40% fast track should be longer than the ~9% ultra-"
            "condensed cram sheet -- they serve different purposes",
        )


class TestFastTrackGuideStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(self.text.startswith("# Domain 1 Fast Track"))

    def test_links_back_to_full_guide(self):
        self.assertIn(
            "(../domain-1-fundamentals-of-ai-and-ml.md)",
            self.text,
        )

    def test_references_ultra_fast_learn(self):
        self.assertIn("ULTRA-FAST-LEARN.md", self.text)

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
            "the AI/ML/DL nesting and the ML lifecycle, per the task",
        )

    def test_contains_at_least_ten_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            10,
            "expected multiple comparison/decision tables (lifecycle, "
            "learning types, AWS services, evaluation metrics, "
            "bias-variance, ensembles, etc.)",
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
    task: the AI/ML/DL hierarchy, the 8-stage ML lifecycle, the three
    learning types, the domain's AWS managed services, model evaluation
    metrics, the bias-variance trade-off, and ensemble methods."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_covers_ai_ml_dl_genai_hierarchy(self):
        for term in [
            "Artificial Intelligence (AI)",
            "Machine Learning (ML)",
            "Deep Learning (DL)",
            "Generative AI",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)
        self.assertIn("AI  ⊃  ML  ⊃  DL  ⊃  Generative AI", self.text)

    def test_covers_all_eight_lifecycle_stages(self):
        for stage in [
            "Business goal identification",
            "Data collection",
            "Exploratory data analysis (EDA)",
            "Data preparation / feature engineering",
            "Model training",
            "Hyperparameter tuning / evaluation",
            "Deployment",
            "Monitoring",
        ]:
            with self.subTest(stage=stage):
                self.assertIn(stage, self.text)

    def test_mentions_sagemaker_autopilot(self):
        self.assertIn("SageMaker Autopilot", self.text)

    def test_covers_all_three_learning_types(self):
        for learning_type in ["Supervised", "Unsupervised", "Reinforcement"]:
            with self.subTest(learning_type=learning_type):
                self.assertIn(learning_type, self.text)

    def test_covers_learning_type_distinguishers(self):
        self.assertIn("agent", self.text.lower())
        self.assertIn("environment", self.text.lower())
        self.assertIn("reward", self.text.lower())

    def test_covers_aws_managed_aiml_services(self):
        for service in [
            "Amazon SageMaker",
            "Amazon Rekognition",
            "Amazon Transcribe",
            "Amazon Comprehend",
            "Amazon Polly",
            "Amazon Translate",
            "Amazon Lex",
            "Amazon Personalize",
            "Amazon Forecast",
            "Amazon Textract",
            "Amazon Fraud Detector",
            "SageMaker Ground Truth",
        ]:
            with self.subTest(service=service):
                self.assertIn(service, self.text)

    def test_covers_model_evaluation_metrics(self):
        for metric in [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 score",
            "AUC-ROC",
            "RMSE",
            "MAE",
        ]:
            with self.subTest(metric=metric):
                self.assertIn(metric, self.text)

    def test_covers_confusion_matrix(self):
        self.assertIn("True Positive", self.text)
        self.assertIn("False Negative", self.text)
        self.assertIn("False Positive", self.text)
        self.assertIn("True Negative", self.text)

    def test_covers_bias_variance_trade_off(self):
        for term in [
            "Underfitting",
            "Overfitting",
            "high bias",
            "high variance",
            "Regularization",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_ensemble_methods(self):
        for term in ["Bagging", "Boosting", "Voting", "Random Forest", "XGBoost"]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_model_registry_and_deployment_strategies(self):
        for term in [
            "SageMaker Model Registry",
            "Canary",
            "Blue/green",
            "A/B testing",
            "Shadow deployment",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

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

    def test_has_rapid_self_check_with_several_questions(self):
        self.assertIn("\n## Rapid self-check\n", self.text)
        section_match = re.search(
            r"\n## Rapid self-check\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(section_match)
        # Rows look like "| 1 | Question | Answer |"
        question_rows = re.findall(
            r"\n\|\s*\d+\s*\|", section_match.group(1)
        )
        self.assertGreaterEqual(len(question_rows), 10)

    def test_has_common_exam_traps_checklist(self):
        self.assertIn("\n## Common exam traps checklist\n", self.text)
        traps_match = re.search(
            r"\n## Common exam traps checklist\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(traps_match)
        bullet_count = traps_match.group(1).count("\n- [ ]")
        self.assertGreaterEqual(bullet_count, 8)

    def test_has_cross_domain_connections_section(self):
        self.assertIn("\n## Cross-domain connections\n", self.text)

    def test_has_where_to_go_deeper_section(self):
        self.assertIn("\n## Where to go deeper\n", self.text)


if __name__ == "__main__":
    unittest.main()
