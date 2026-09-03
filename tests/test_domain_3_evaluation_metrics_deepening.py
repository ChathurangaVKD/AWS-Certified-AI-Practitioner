"""Structural validation for the deepened evaluation-metrics coverage added
to Section 7 ("Evaluating foundation model performance") of
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Section 7 named only four benchmarks (MMLU, ARC,
HumanEval, GSM8K) and gave no guidance on toxicity scoring, semantic
similarity (BERTScore), perplexity, or how to interpret a benchmark/metric
score once you have one -- so a learner could recognize a named benchmark
but not choose or reason about the broader set of metrics an exam scenario
or a real evaluation pipeline actually needs. These tests guard the new
"Beyond named benchmarks" metrics table, the score-interpretation guidance,
and the "Worked example: picking evaluation metrics for a scenario"
subsection added to close that gap.

Mirrors the conventions established in
tests/test_domain_3_statistical_significance_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_evaluation_metrics_deepening.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

WORKED_EXAMPLE_HEADING = (
    "### Worked example: picking evaluation metrics for a scenario"
)
WORKED_EXAMPLE_HEADING_REGEX = (
    r"\n### Worked example: picking evaluation metrics for a scenario"
)
TOC_LINK = (
    "[Worked example: picking evaluation metrics for a scenario]"
    "(#worked-example-picking-evaluation-metrics-for-a-scenario)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,3} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading of the same or higher level, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3EvaluationMetricsDeepening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section_7 = _section(
            cls.text, r"\n## 7\. Evaluating foundation model performance"
        )
        cls.worked_example = _section(cls.text, WORKED_EXAMPLE_HEADING_REGEX)

    # -- Additional metrics table -------------------------------------

    def test_section_7_names_toxicity_semantic_similarity_and_perplexity(self):
        for term in ["Toxicity scoring", "BERTScore", "Perplexity"]:
            with self.subTest(term=term):
                self.assertIn(term, self.section_7)

    def test_additional_metrics_appear_in_a_table_with_interpretation_guidance(self):
        tables = re.findall(r"^\|.+\|$\n(?:^\|.+\|$\n?)+", self.section_7, re.M)
        metrics_tables = [t for t in tables if "BERTScore" in t and "Perplexity" in t]
        self.assertTrue(
            metrics_tables,
            "expected a table listing toxicity scoring, BERTScore, and "
            "perplexity together",
        )
        table = metrics_tables[0]
        self.assertIn("Toxicity scoring", table)
        # Each row should explain the direction of "better" for that metric.
        for term in ["lower is better", "higher is better"]:
            with self.subTest(term=term):
                self.assertRegex(table, re.escape(term))

    def test_bertscore_explained_relative_to_bleu_rouge(self):
        self.assertRegex(
            self.section_7,
            r"(?i)BERTScore.{0,400}BLEU/ROUGE|BLEU/ROUGE.{0,400}BERTScore",
            "expected BERTScore to be contrasted with BLEU/ROUGE's exact "
            "n-gram/word overlap",
        )

    def test_perplexity_explained_as_fluency_not_correctness(self):
        self.assertRegex(
            self.section_7,
            r"(?i)perplexity",
        )
        self.assertRegex(
            self.section_7,
            r"(?i)fluency|fluent",
            "expected perplexity to be framed as a fluency/confidence "
            "measure",
        )
        self.assertRegex(
            self.section_7,
            r"(?i)not.{0,80}correct|correctness",
            "expected an explicit caveat that perplexity does not measure "
            "factual correctness",
        )

    def test_toxicity_scoring_references_bedrock_automatic_evaluation(self):
        self.assertRegex(
            self.section_7,
            r"(?i)toxicity.{0,300}Bedrock|Bedrock.{0,300}toxicity",
            "expected toxicity scoring to be tied to Bedrock automatic "
            "model evaluation's built-in metric",
        )

    def test_section_7_explains_how_to_interpret_benchmark_scores(self):
        self.assertRegex(
            self.section_7,
            r"(?i)interpreting benchmark",
            "expected explicit guidance on interpreting benchmark/metric "
            "scores",
        )
        self.assertRegex(
            self.section_7,
            r"(?i)compare.{0,40}don.t isolate|baseline",
            "expected guidance that scores should be compared to a "
            "baseline rather than read in isolation",
        )

    # -- Worked example --------------------------------------------------

    def test_worked_example_section_exists(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.text)

    def test_worked_example_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_worked_example_lives_inside_section_7(self):
        section_7_pos = self.text.index(
            "## 7. Evaluating foundation model performance"
        )
        section_8_pos = self.text.index(
            "## 8. AWS infrastructure for generative AI workloads"
        )
        heading_pos = self.text.index(WORKED_EXAMPLE_HEADING)
        self.assertLess(section_7_pos, heading_pos)
        self.assertLess(heading_pos, section_8_pos)

    def test_worked_example_maps_each_requirement_to_a_metric(self):
        for expected in [
            "Accuracy against a held-out labeled QA set",
            "BERTScore",
            "Toxicity scoring",
            "Perplexity",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.worked_example)

    def test_worked_example_has_an_aws_example_referencing_bedrock(self):
        self.assertIn("**AWS example:**", self.worked_example)
        self.assertRegex(self.worked_example, r"(?i)bedrock")

    def test_worked_example_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.worked_example)


if __name__ == "__main__":
    unittest.main()
