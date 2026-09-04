"""Structural validation for the "Worked example: running a Bedrock Model
Evaluation job to choose between candidate models" subsection added to
Section 7 ("Evaluating foundation model performance") of
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Section 7 named the evaluation *approaches* (human
evaluation, benchmark datasets/automatic model evaluation, business
metrics) and two worked examples deepened statistical rigor and metric
selection, but nothing showed the actual mechanics of using the **Amazon
Bedrock Model Evaluation** service: setting up a job with multiple
candidate models, choosing metrics that fit a specific task type
(summarization vs. Q&A vs. classification), reading conflicting per-model
scores to decide between candidates, and telling automatic metric
comparison apart from a follow-on human evaluation job in practice. These
tests guard the worked example added to close that gap.

Mirrors the conventions established in
tests/test_domain_3_statistical_significance_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_bedrock_model_evaluation_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

HEADING = (
    "### Worked example: running a Bedrock Model Evaluation job to choose "
    "between candidate models"
)
HEADING_REGEX = (
    r"\n### Worked example: running a Bedrock Model Evaluation job to "
    r"choose between candidate models"
)
TOC_LINK = (
    "[Worked example: running a Bedrock Model Evaluation job to choose "
    "between candidate models]"
    "(#worked-example-running-a-bedrock-model-evaluation-job-to-choose-between-candidate-models)"
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


class TestDomain3BedrockModelEvaluationWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

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
        heading_pos = self.text.index(HEADING)
        self.assertLess(section_7_pos, heading_pos)
        self.assertLess(heading_pos, section_8_pos)

    def test_worked_example_appears_after_the_metrics_scenario_example(self):
        prior_heading_pos = self.text.index(
            "### Worked example: picking evaluation metrics for a scenario"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(prior_heading_pos, heading_pos)

    def test_covers_setting_up_an_evaluation_job_with_multiple_models(self):
        for expected in ["Model A", "Model B", "Model C", "S3", "prompt"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)
        self.assertRegex(
            self.section,
            r"(?i)evaluation job",
            "expected the worked example to describe setting up an "
            "evaluation job",
        )

    def test_covers_task_type_metric_mapping_table(self):
        # A table mapping task type -> recommended metrics, covering the
        # three task types called out in the task description.
        for expected in [
            "Summarization",
            "Question and answering",
            "Text classification",
            "ROUGE",
            "BERTScore",
            "Accuracy",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_interprets_conflicting_per_model_results_table(self):
        # The worked results table with conflicting ROUGE-L/BERTScore
        # winners across the three candidate models.
        for expected in ["ROUGE-L", "0.41", "0.36", "0.44", "0.88", "0.91", "0.83"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)
        self.assertRegex(
            self.section,
            r"(?i)shortlist(?:s)?\s+\*\*Model B\*\*",
            "expected the worked example to reason to a concrete decision "
            "(shortlisting Model B) rather than leaving the comparison "
            "unresolved",
        )

    def test_distinguishes_automatic_comparison_from_human_evaluation(self):
        self.assertRegex(
            self.section,
            r"(?i)automatic metric comparison",
        )
        self.assertRegex(
            self.section,
            r"(?i)human evaluation",
        )
        # A comparison table contrasting the two approaches.
        self.assertIn("| **What it measures** |", self.section)

    def test_has_an_aws_example_referencing_bedrock_evaluation(self):
        self.assertIn("**AWS example:**", self.section)
        self.assertRegex(self.section, r"(?i)bedrock")

    def test_worked_example_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.section)


if __name__ == "__main__":
    unittest.main()
