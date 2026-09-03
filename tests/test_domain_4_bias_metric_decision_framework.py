"""Structural validation for the bias-metric decision-framework subsection
added to docs/domain-4-guidelines-for-responsible-ai.md.

The gap this covers: Domain 4's "Comparison table: AWS responsible AI
tools at a glance" lists SageMaker Clarify, Model Cards, Guardrails, and
A2I side by side, but gave no guidance on *which bias metric to check in
which scenario*, and didn't clearly distinguish Difference in Positive
Proportions in Labels (DPL) from Disparate Impact -- two exam-tested
SageMaker Clarify metrics with different use cases (pre-training data
audit vs. post-training prediction audit). This test guards the new
prose decision-framework subsection added immediately after that
comparison table, which (1) explains when to use DPL vs. Disparate
Impact, (2) gives guidance on layering SHAP, Model Cards, and A2I
together for high-stakes scenarios, and (3) includes a worked example
applying the framework to a HIPAA-regulated hiring/lending scenario.

Mirrors the conventions established in
tests/test_domain_4_performance_interpretability_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_4_bias_metric_decision_framework.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-4-guidelines-for-responsible-ai.md"
)

FRAMEWORK_HEADING = (
    "## Decision framework: choosing a bias metric and layering tools "
    "for high-stakes AI"
)
COMPARISON_HEADING = "## Comparison table: AWS responsible AI tools at a glance"
CHEAT_SHEET_HEADING = "## Quick-reference cheat sheet"


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading, end_heading_regex=r"\n## "):
    """Return the text between an exact start_heading string and the next
    top-level (##) heading, or end of file."""
    start = text.index(start_heading)
    rest = text[start + len(start_heading):]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain4BiasMetricDecisionFramework(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, FRAMEWORK_HEADING)

    def test_heading_exists(self):
        self.assertIn(FRAMEWORK_HEADING, self.text)

    def test_linked_from_table_of_contents(self):
        toc = _section(self.text, "## Table of contents", r"\n## Domain overview")
        self.assertIn(
            "[Decision framework: choosing a bias metric and layering "
            "tools for high-stakes AI]"
            "(#decision-framework-choosing-a-bias-metric-and-layering-"
            "tools-for-high-stakes-ai)",
            toc,
        )

    def test_appears_immediately_after_comparison_table(self):
        comparison_idx = self.text.index(COMPARISON_HEADING)
        framework_idx = self.text.index(FRAMEWORK_HEADING)
        cheat_sheet_idx = self.text.index(CHEAT_SHEET_HEADING)
        self.assertLess(comparison_idx, framework_idx)
        self.assertLess(framework_idx, cheat_sheet_idx)

    def test_distinguishes_dpl_as_pre_training(self):
        self.assertRegex(
            self.section,
            r"(?i)Difference in Positive Proportions in Labels.{0,40}"
            r"pre-training|pre-training.{0,80}DPL",
        )
        self.assertIn("DPL", self.section)

    def test_distinguishes_disparate_impact_as_post_training(self):
        self.assertRegex(self.section, r"(?i)disparate impact")
        self.assertRegex(self.section, r"(?i)post-training")

    def test_gives_a_shortcut_for_telling_the_two_metrics_apart(self):
        self.assertRegex(
            self.section,
            r"(?i)dataset.{0,60}(no trained model|before)|"
            r"predictions.{0,60}(endpoint|deployed)",
        )

    def test_covers_layering_shap_model_cards_and_a2i(self):
        for term in ["SHAP", "Model Card", "Amazon A2I"]:
            with self.subTest(term=term):
                self.assertIn(term, self.section)

    def test_has_worked_example(self):
        self.assertIn("**Worked example.**", self.section)

    def test_worked_example_mentions_hipaa_and_hiring_or_lending(self):
        self.assertIn("HIPAA", self.section)
        self.assertRegex(self.section, r"(?i)hiring|hir(ed|ing)|lending|loan")

    def test_worked_example_applies_both_metrics(self):
        worked_example_start = self.section.index("**Worked example.**")
        worked_example = self.section[worked_example_start:]
        self.assertIn("DPL", worked_example)
        self.assertRegex(worked_example, r"(?i)disparate impact")

    def test_word_count_within_expected_range(self):
        words = re.findall(r"\w+", self.section)
        self.assertGreaterEqual(
            len(words),
            300,
            "expected the decision-framework subsection to be a "
            "substantial (~350-450 word) prose section",
        )
        self.assertLessEqual(len(words), 600)


if __name__ == "__main__":
    unittest.main()
