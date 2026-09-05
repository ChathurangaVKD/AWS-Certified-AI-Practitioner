"""Structural validation for the Domain 4 Ultra Fast Track cram sheet.

The gap this covers: Domains 1 and 2 both already have a dedicated
`ULTRA-FAST-LEARN.md` -- an even denser, single-page recall aid than a
full domain guide's own "## Quick-reference cheat sheet" -- but Domain 4
only had the ~40%-length `docs/domain-4-fast-track/README.md` condensation,
with no 15-20%-length cram sheet on top of it.
`docs/domain-4-fast-track/ULTRA-FAST-LEARN.md` fills that gap: bullets and
tables only, no prose, no worked examples, no mini-quizzes, condensing the
Fast Track guide itself down to about a page.

These tests assert that the file exists, is a real single-page
condensation of the Fast Track guide (not a stub or a near-duplicate),
sticks to the bullets-and-tables-only format, links back to the Fast
Track guide (and full guide) with resolving anchors, and actually
preserves every testable concept named in the task: the dimensions of
responsible AI, common bias sources, a fairness-metrics table by use
case, the fairness-vs-accuracy and explainability-vs-latency trade-offs,
Amazon SageMaker Clarify capabilities, and a monitoring checklist.

Run with:
    python3 -m unittest tests/test_domain_4_ultra_fast_learn.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
ULTRA_FAST_LEARN_PATH = DOCS_DIR / "domain-4-fast-track" / "ULTRA-FAST-LEARN.md"
FAST_TRACK_PATH = DOCS_DIR / "domain-4-fast-track" / "README.md"
FULL_GUIDE_PATH = DOCS_DIR / "domain-4-guidelines-for-responsible-ai.md"

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
            "expected docs/domain-4-fast-track/ULTRA-FAST-LEARN.md to exist",
        )

    def test_fast_track_guide_exists(self):
        self.assertTrue(FAST_TRACK_PATH.is_file())

    def test_full_guide_exists(self):
        self.assertTrue(FULL_GUIDE_PATH.is_file())


class TestUltraFastLearnLength(unittest.TestCase):
    """The task calls for a single-page cram sheet, 15-20% of the Fast
    Track guide's own length -- assert it is a real, heavily condensed
    recall aid, not a stub or a near-duplicate copy of the ~800-line Fast
    Track guide (let alone the 2,000+ line full guide)."""

    @classmethod
    def setUpClass(cls):
        cls.ultra_lines = _line_count(ULTRA_FAST_LEARN_PATH)
        cls.fast_track_lines = _line_count(FAST_TRACK_PATH)
        cls.full_guide_lines = _line_count(FULL_GUIDE_PATH)

    def test_is_substantially_shorter_than_fast_track_guide(self):
        # Target band is 15-20% of the Fast Track guide; allow generous
        # slack on both sides while still ruling out a near-duplicate.
        self.assertLess(self.ultra_lines, self.fast_track_lines * 0.30)

    def test_is_substantially_shorter_than_full_guide(self):
        self.assertLess(self.ultra_lines, self.full_guide_lines * 0.15)

    def test_is_not_a_trivial_stub(self):
        self.assertGreater(self.ultra_lines, 80)


class TestUltraFastLearnStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(ULTRA_FAST_LEARN_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(self.text.startswith("# Domain 4 Ultra Fast Track"))

    def test_links_back_to_fast_track_guide(self):
        self.assertIn("(README.md)", self.text)

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
        self.assertGreaterEqual(len(anchors_in_toc), 6)
        real_anchors = _heading_anchors(self.text)
        for anchor in anchors_in_toc:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, real_anchors)

    def test_contains_several_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            7,
            "expected multiple tables (dimensions, bias sources, fairness "
            "metrics by stage, fairness metrics by use case, "
            "fairness-vs-accuracy, explainability-vs-latency, "
            "where-each-row-comes-from)",
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
    """Every testable Domain 4 concept named in the task must map to at
    least one bullet or table cell."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(ULTRA_FAST_LEARN_PATH)

    def test_covers_dimensions_of_responsible_ai(self):
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

    def test_covers_common_bias_sources(self):
        for bias in [
            "Sampling bias",
            "Measurement bias",
            "Label / human bias",
            "Historical bias",
            "Exclusion bias",
            "Aggregation bias",
            "Representativeness bias",
        ]:
            with self.subTest(bias=bias):
                self.assertIn(bias, self.text)

    def test_covers_fairness_metrics_by_stage(self):
        for metric in [
            "Difference in proportions of labels (DPL)",
            "Class imbalance",
            "Disparate impact",
            "Accuracy/recall difference",
        ]:
            with self.subTest(metric=metric):
                self.assertIn(metric, self.text)

    def test_covers_fairness_metrics_by_use_case(self):
        for use_case in [
            "Credit/loan approval",
            "Hiring/resume screening",
            "Healthcare triage/diagnosis",
            "Content moderation",
            "RAG/generative assistant",
        ]:
            with self.subTest(use_case=use_case):
                self.assertIn(use_case, self.text)

    def test_covers_fairness_vs_accuracy_trade_off(self):
        self.assertIn("Fairness vs. accuracy", self.text)

    def test_covers_explainability_vs_latency_trade_off(self):
        self.assertIn("Explainability vs. latency", self.text)
        for term in ["Natively interpretable model", "Post-hoc SHAP"]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_sagemaker_clarify_capabilities(self):
        for capability in [
            "Pre-training bias metrics",
            "Post-training bias metrics",
            "SHAP-based explainability",
            "Bias reports",
            "Integration with SageMaker Model Monitor",
        ]:
            with self.subTest(capability=capability):
                self.assertIn(capability, self.text)

    def test_has_monitoring_checklist(self):
        self.assertIn("\n## 6. Monitoring checklist\n", self.text)
        checklist_match = re.search(
            r"\n## 6\. Monitoring checklist\n(.*?)(\n## |\n---\n|\Z)",
            self.text,
            re.S,
        )
        self.assertIsNotNone(checklist_match)
        bullet_count = checklist_match.group(1).count("\n- [ ]")
        self.assertGreaterEqual(bullet_count, 5)


if __name__ == "__main__":
    unittest.main()
