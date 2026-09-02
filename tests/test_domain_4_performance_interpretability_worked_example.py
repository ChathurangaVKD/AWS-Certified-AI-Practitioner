"""Structural validation for the fourth worked-example section added to
docs/domain-4-guidelines-for-responsible-ai.md.

The gap this covers: Domain 4, Section 5 ("Balancing model performance and
interpretability") explained the accuracy-vs-explainability tension only
in prose and a short "AWS example:" callout, and none of the domain's
three existing worked examples (e-commerce recommendation engine, classical
ML loan-approval classifier, RAG-based HR assistant) isolate that tradeoff
as the central decision -- each folds it into a broader bias-audit
walkthrough. This test file guards the fourth worked example, which walks
through a health-insurance prior-authorization scenario where a regulatory
explainability requirement forces a team to choose a natively interpretable
model over a more accurate black-box model with post-hoc SHAP explanations,
using concrete accuracy/recall metrics and Amazon SageMaker Clarify to make
and document that call.

Mirrors the conventions established in
tests/test_domain_4_cross_context_bias_worked_examples.py.

Run with:
    python3 -m unittest tests/test_domain_4_performance_interpretability_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-4-guidelines-for-responsible-ai.md"
)

TRADEOFF_HEADING = (
    "## Worked example: deciding whether to trade accuracy for "
    "interpretability to meet a regulatory explainability requirement"
)
RAG_HEADING = (
    "## Worked example: diagnosing retrieval-induced bias and "
    "hallucination in a RAG-based HR assistant"
)
COMPARISON_HEADING = "## Comparison table: AWS responsible AI tools at a glance"


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading, end_heading_regex=r"\n## "):
    """Return the text between an exact start_heading string and the next
    top-level (##) heading, or end of file."""
    start = text.index(start_heading)
    rest = text[start + len(start_heading):]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain4PerformanceInterpretabilityWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, TRADEOFF_HEADING)

    def test_heading_exists(self):
        self.assertIn(TRADEOFF_HEADING, self.text)

    def test_linked_from_table_of_contents(self):
        toc = _section(self.text, "## Table of contents", r"\n## Domain overview")
        self.assertIn(
            "[Worked example: deciding whether to trade accuracy for "
            "interpretability to meet a regulatory explainability "
            "requirement]"
            "(#worked-example-deciding-whether-to-trade-accuracy-for-"
            "interpretability-to-meet-a-regulatory-explainability-"
            "requirement)",
            toc,
        )

    def test_appears_after_the_rag_worked_example(self):
        rag_idx = self.text.index(RAG_HEADING)
        tradeoff_idx = self.text.index(TRADEOFF_HEADING)
        self.assertLess(rag_idx, tradeoff_idx)

    def test_appears_before_the_comparison_table(self):
        tradeoff_idx = self.text.index(TRADEOFF_HEADING)
        comparison_idx = self.text.index(COMPARISON_HEADING)
        self.assertLess(tradeoff_idx, comparison_idx)

    def test_has_scenario_and_exam_tip(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_cross_references_section_5(self):
        self.assertIn(
            "#5-balancing-model-performance-and-interpretability",
            self.section,
        )

    def test_names_a_regulatory_explainability_requirement(self):
        self.assertRegex(
            self.section,
            r"(?i)regulation|regulatory",
            "expected the scenario to be driven by a regulatory "
            "explainability requirement",
        )

    def test_includes_concrete_accuracy_and_recall_metrics(self):
        for term in ["AUC-ROC", "recall", "0.93", "0.89", "88%", "82%"]:
            with self.subTest(term=term):
                self.assertIn(term, self.section)

    def test_uses_sagemaker_clarify_and_shap(self):
        self.assertIn("Amazon SageMaker Clarify", self.section)
        self.assertIn("SHAP", self.section)

    def test_favors_natively_interpretable_model_for_the_regulated_decision(self):
        self.assertRegex(
            self.section,
            r"(?i)natively interpretable",
            "expected the regulated scenario to favor a natively "
            "interpretable model over post-hoc explanations",
        )

    def test_explains_why_post_hoc_shap_alone_is_rejected(self):
        self.assertRegex(
            self.section,
            r"(?i)approximation",
            "expected the example to explain that SHAP is an "
            "approximation, not an exact trace of the model's decision "
            "logic",
        )

    def test_documents_the_decision_in_a_model_card(self):
        self.assertIn("Model Card", self.section)

    def test_has_at_least_six_numbered_steps(self):
        steps = re.findall(r"^\d+\.\s", self.section, re.M)
        self.assertGreaterEqual(
            len(steps),
            6,
            "worked example should walk through at least six numbered steps",
        )

    def test_word_count_within_expected_range(self):
        words = re.findall(r"\w+", self.section)
        self.assertGreaterEqual(len(words), 400)
        self.assertLessEqual(len(words), 900)


if __name__ == "__main__":
    unittest.main()
