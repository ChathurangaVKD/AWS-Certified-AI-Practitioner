"""Structural validation for the two additional worked-example sections
added to docs/domain-4-guidelines-for-responsible-ai.md.

The gap this covers: Domain 4 previously had exactly one worked example
("## Worked example: auditing and documenting a responsible e-commerce
recommendation engine") showing bias-detection patterns for a single
context (a deep-learning recommendation ranking model). AIF-C01 scenario
questions test bias detection across multiple model types and use
cases, so this only demonstrated one corner of the pattern. These tests
guard the two additional worked examples added to broaden that coverage:
a classical ML (gradient-boosted tree) loan-approval classifier bias
audit, and a foundation-model/RAG HR assistant example showing
retrieval-corpus bias and hallucination-driven fairness issues.

Mirrors the conventions established in
tests/test_domain_3_rag_troubleshooting_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_4_cross_context_bias_worked_examples.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-4-guidelines-for-responsible-ai.md"
)

CLASSICAL_ML_HEADING = (
    "## Worked example: auditing a classical ML small-business "
    "loan-approval classifier for bias"
)
RAG_HEADING = (
    "## Worked example: diagnosing retrieval-induced bias and "
    "hallucination in a RAG-based HR assistant"
)
ECOMMERCE_HEADING = (
    "## Worked example: auditing and documenting a responsible "
    "e-commerce recommendation engine"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading, end_heading_regex=r"\n## "):
    """Return the text between an exact start_heading string and the next
    top-level (##) heading, or end of file."""
    start = text.index(start_heading)
    rest = text[start + len(start_heading):]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain4ClassicalMLBiasWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, CLASSICAL_ML_HEADING)

    def test_heading_exists(self):
        self.assertIn(CLASSICAL_ML_HEADING, self.text)

    def test_linked_from_table_of_contents(self):
        toc = _section(self.text, "## Table of contents", r"\n## Domain overview")
        self.assertIn(
            "[Worked example: auditing a classical ML small-business "
            "loan-approval classifier for bias]"
            "(#worked-example-auditing-a-classical-ml-small-business-"
            "loan-approval-classifier-for-bias)",
            toc,
        )

    def test_appears_after_the_ecommerce_worked_example(self):
        ecommerce_idx = self.text.index(ECOMMERCE_HEADING)
        classical_idx = self.text.index(CLASSICAL_ML_HEADING)
        self.assertLess(ecommerce_idx, classical_idx)

    def test_appears_before_the_rag_worked_example(self):
        classical_idx = self.text.index(CLASSICAL_ML_HEADING)
        rag_idx = self.text.index(RAG_HEADING)
        self.assertLess(classical_idx, rag_idx)

    def test_has_scenario_and_exam_tip(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_describes_a_classical_ml_model_not_deep_learning(self):
        self.assertRegex(
            self.section,
            r"(?i)gradient-boosted tree",
            "expected the scenario to name a classical ML model type",
        )

    def test_covers_measurement_bias_via_a_proxy_variable(self):
        self.assertIn("measurement bias", self.section)
        self.assertRegex(
            self.section,
            r"(?i)proxy variable",
            "expected the audit to identify ZIP code as a proxy variable",
        )

    def test_uses_sagemaker_clarify_pre_and_post_training_metrics(self):
        for term in [
            "Amazon SageMaker Clarify",
            "difference in proportions of labels",
            "disparate impact",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.section)

    def test_reverses_the_performance_interpretability_tradeoff(self):
        # The first (e-commerce) worked example favors a complex model with
        # post-hoc explanations because the stakes are low; this one is
        # high-stakes/regulated, so it should favor the natively
        # interpretable model instead -- the tests lock in that contrast.
        self.assertRegex(
            self.section,
            r"(?i)natively interpretable",
            "expected the high-stakes scenario to favor a natively "
            "interpretable model",
        )
        self.assertIn(
            "#5-balancing-model-performance-and-interpretability",
            self.section,
        )

    def test_has_at_least_six_numbered_steps(self):
        steps = re.findall(r"^\d+\.\s", self.section, re.M)
        self.assertGreaterEqual(
            len(steps),
            6,
            "worked example should walk through at least six numbered steps",
        )

    def test_closes_the_legal_gap_with_a2i_human_review(self):
        self.assertIn("Amazon A2I", self.section)
        self.assertIn("#4-legal-and-ethical-considerations", self.section)

    def test_word_count_within_expected_range(self):
        words = re.findall(r"\w+", self.section)
        self.assertGreaterEqual(len(words), 400)
        self.assertLessEqual(len(words), 900)


class TestDomain4RagBiasWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, RAG_HEADING)

    def test_heading_exists(self):
        self.assertIn(RAG_HEADING, self.text)

    def test_linked_from_table_of_contents(self):
        toc = _section(self.text, "## Table of contents", r"\n## Domain overview")
        self.assertIn(
            "[Worked example: diagnosing retrieval-induced bias and "
            "hallucination in a RAG-based HR assistant]"
            "(#worked-example-diagnosing-retrieval-induced-bias-and-"
            "hallucination-in-a-rag-based-hr-assistant)",
            toc,
        )

    def test_appears_after_the_classical_ml_worked_example(self):
        classical_idx = self.text.index(CLASSICAL_ML_HEADING)
        rag_idx = self.text.index(RAG_HEADING)
        self.assertLess(classical_idx, rag_idx)

    def test_appears_before_the_comparison_table(self):
        rag_idx = self.text.index(RAG_HEADING)
        comparison_idx = self.text.index(
            "## Comparison table: AWS responsible AI tools at a glance"
        )
        self.assertLess(rag_idx, comparison_idx)

    def test_has_scenario_and_exam_tip(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_cross_references_the_domain_3_rag_section(self):
        self.assertIn(
            "domain-3-applications-of-foundation-models.md"
            "#3-retrieval-augmented-generation-rag-and-amazon-bedrock-"
            "knowledge-bases",
            self.section,
        )

    def test_covers_retrieval_corpus_imbalance(self):
        self.assertRegex(
            self.section,
            r"(?i)knowledge base|retrieval corpus",
            "expected the scenario to describe an unrepresentative "
            "retrieval corpus",
        )

    def test_covers_hallucination_as_a_fairness_issue(self):
        self.assertRegex(
            self.section,
            r"(?i)hallucinat",
            "expected the example to name hallucination explicitly",
        )
        self.assertRegex(
            self.section,
            r"(?i)hallucination.{0,40}fairness|fairness.{0,40}hallucination",
            "expected the example to explicitly connect hallucination to "
            "a fairness outcome",
        )

    def test_names_guardrails_contextual_grounding_as_the_remediation(self):
        self.assertRegex(
            self.section,
            r"(?i)guardrails for amazon bedrock.{0,40}contextual grounding|"
            r"contextual grounding checks",
            "expected Guardrails' contextual grounding checks to be named "
            "as the runtime mitigation",
        )

    def test_explains_why_clarify_does_not_apply_here(self):
        self.assertRegex(
            self.section,
            r"(?i)can'?t run clarify|no labeled training set|no trained\s*\n?\s*model for.{0,20}clarify",
            "expected the example to explain why SageMaker Clarify's "
            "dataset/model metrics don't apply to a RAG/FM application",
        )

    def test_has_at_least_six_numbered_steps(self):
        steps = re.findall(r"^\d+\.\s", self.section, re.M)
        self.assertGreaterEqual(
            len(steps),
            6,
            "worked example should walk through at least six numbered steps",
        )

    def test_routes_low_confidence_answers_through_a2i(self):
        self.assertIn("Amazon A2I", self.section)

    def test_word_count_within_expected_range(self):
        words = re.findall(r"\w+", self.section)
        self.assertGreaterEqual(len(words), 400)
        self.assertLessEqual(len(words), 900)


if __name__ == "__main__":
    unittest.main()
