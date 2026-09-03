"""Structural validation for the fifth standalone worked-example section
added to docs/domain-4-guidelines-for-responsible-ai.md.

The gap this covers: Domain 4 already had a nested "### Worked example:
layering SageMaker Clarify and Guardrails for Amazon Bedrock to audit a
generative recommendation engine" subsection (Section 3), but that example
layers both tools on *one* fine-tuned foundation model across two points
in its lifecycle -- Clarify audits the FM itself pre-launch, and
Guardrails filters the same FM at runtime. Nothing in the domain showed
the more common production pattern of a **classical ML model** and a
**foundation model** as two distinct components in one system, each
needing its own tool and neither substituting for the other. This test
file guards the new closing worked example, which walks a two-component
recommendation system (a classical ML ranker scored with SageMaker
Clarify, feeding a Bedrock foundation model that writes personalized copy
protected by Guardrails) through exactly that architecture.

Mirrors the conventions established in
tests/test_domain_4_performance_interpretability_worked_example.py and
tests/test_domain_4_clarify_guardrails_layering_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_4_classical_ml_ranker_bedrock_fm_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-4-guidelines-for-responsible-ai.md"
)

WORKED_EXAMPLE_HEADING = (
    "## Worked example: pairing a classical ML ranker scored by "
    "SageMaker Clarify with a Bedrock FM protected by Guardrails"
)
TRADEOFF_HEADING = (
    "## Worked example: deciding whether to trade accuracy for "
    "interpretability to meet a regulatory explainability requirement"
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


class TestDomain4ClassicalMlRankerBedrockFmWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, WORKED_EXAMPLE_HEADING)
        cls.normalized = re.sub(r"\s+", " ", cls.section)

    def test_heading_exists(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.text)

    def test_linked_from_table_of_contents(self):
        toc = _section(self.text, "## Table of contents", r"\n## Domain overview")
        self.assertIn(
            "[Worked example: pairing a classical ML ranker scored by "
            "SageMaker Clarify with a Bedrock FM protected by Guardrails]"
            "(#worked-example-pairing-a-classical-ml-ranker-scored-by-"
            "sagemaker-clarify-with-a-bedrock-fm-protected-by-guardrails)",
            toc,
        )

    def test_appears_after_the_tradeoff_worked_example(self):
        tradeoff_idx = self.text.index(TRADEOFF_HEADING)
        worked_idx = self.text.index(WORKED_EXAMPLE_HEADING)
        self.assertLess(tradeoff_idx, worked_idx)

    def test_appears_before_the_comparison_table(self):
        worked_idx = self.text.index(WORKED_EXAMPLE_HEADING)
        comparison_idx = self.text.index(COMPARISON_HEADING)
        self.assertLess(worked_idx, comparison_idx)

    def test_has_scenario_and_exam_tip(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_names_both_tools(self):
        for term in ["SageMaker Clarify", "Guardrails for Amazon Bedrock"]:
            with self.subTest(term=term):
                self.assertIn(term, self.normalized)

    def test_describes_two_distinct_components(self):
        self.assertIn("Component 1", self.section)
        self.assertIn("Component 2", self.section)
        self.assertRegex(self.normalized, r"(?i)classical ML")
        self.assertRegex(self.normalized, r"(?i)foundation model")

    def test_covers_clarify_bias_metrics(self):
        for term in [
            "pre-training",
            "post-training",
            "class imbalance",
            "DPL",
            "disparate impact",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.normalized)

    def test_covers_guardrails_capabilities(self):
        for term in [
            "denied topics",
            "content filters",
            "word filters",
            "sensitive information filters",
            "contextual grounding checks",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.normalized)

    def test_explains_clarify_cannot_substitute_for_guardrails_and_vice_versa(self):
        self.assertRegex(
            self.normalized,
            r"(?i)Guardrails cannot do",
            "expected the example to explain what Guardrails cannot "
            "do on the classical ranker",
        )
        self.assertRegex(
            self.normalized,
            r"(?i)Clarify cannot do",
            "expected the example to explain what Clarify cannot do "
            "on the live FM generations",
        )

    def test_rejects_collapsing_both_audits_into_one_metric(self):
        self.assertRegex(
            self.normalized,
            r"(?i)reject",
            "expected the example to explicitly reject running a single "
            "combined bias metric across both components",
        )

    def test_cross_references_and_contrasts_the_nested_layering_example(self):
        self.assertIn(
            "#worked-example-layering-sagemaker-clarify-and-guardrails-for-"
            "amazon-bedrock-to-audit-a-generative-recommendation-engine",
            self.section,
        )
        self.assertRegex(
            self.normalized,
            r"(?i)differs from the Section 3 worked example",
            "expected an explicit contrast against the earlier "
            "single-model, two-stage Clarify/Guardrails layering example",
        )

    def test_documents_in_a_model_card_and_monitors_with_model_monitor(self):
        self.assertIn("Model Card", self.normalized)
        self.assertIn("SageMaker Model Monitor", self.normalized)

    def test_has_at_least_six_numbered_steps(self):
        steps = re.findall(r"^\d+\.\s", self.section, re.M)
        self.assertGreaterEqual(
            len(steps),
            6,
            "worked example should walk through at least six numbered steps",
        )

    def test_word_count_within_expected_range(self):
        words = re.findall(r"\w+", self.section)
        self.assertGreaterEqual(len(words), 800)
        self.assertLessEqual(len(words), 1800)


if __name__ == "__main__":
    unittest.main()
