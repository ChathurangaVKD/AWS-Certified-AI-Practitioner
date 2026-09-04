"""Structural validation for the "Worked example: monitoring hallucination
rate drift in a production RAG assistant" subsection added to
docs/domain-5-security-compliance-governance.md.

The gap this covers: the "Data monitoring" subsection (inside "## 4. Data
governance strategies") documents Amazon Macie, Amazon CloudWatch, and
Amazon GuardDuty for infrastructure- and classical-ML-drift-style
monitoring, but never covered generative-AI-specific production
monitoring metrics -- hallucination rate and factual consistency -- for
a RAG application whose knowledge base drifts out of sync with the
foundation model over time. No file in the repo mentioned "factual
consistency" before this change. This new worked example must exist as a
"####"-level subsection nested inside the "Data monitoring" subsection
(after its exam tip, before that subsection's mini-quiz), must not
perturb the standalone/other-nested worked-example counts asserted
elsewhere, must cover the RAG-drift scenario and its core vocabulary
(hallucination rate, factual consistency, CloudWatch custom metric),
must explicitly distinguish itself from classical SageMaker Model
Monitor drift monitoring covered elsewhere in the file, must close with
an exam tip, and must fall within the requested ~250-350 word range. It
also guards that the existing "Data monitoring" exam tip now links
forward to this new subsection.

Mirrors the conventions established in
tests/test_domain_5_differential_privacy_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_hallucination_monitoring_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)

HEADING = (
    "#### Worked example: monitoring hallucination rate drift in a "
    "production RAG assistant"
)
HEADING_REGEX = (
    r"\n#### Worked example: monitoring hallucination rate drift in a "
    r"production RAG assistant"
)
DATA_MONITORING_HEADING = "### Data monitoring"
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of data governance strategies"
)
FORWARD_LINK = (
    "[worked example "
    "below](#worked-example-monitoring-hallucination-rate-drift-in-a-"
    "production-rag-assistant)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,4} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading of the same or higher level, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain5HallucinationMonitoringWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_between_data_monitoring_and_mini_quiz(
        self,
    ):
        data_monitoring_pos = self.text.index(DATA_MONITORING_HEADING)
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(MINI_QUIZ_HEADING)
        self.assertLess(data_monitoring_pos, heading_pos)
        self.assertLess(heading_pos, mini_quiz_pos)

    def test_does_not_change_standalone_worked_example_count(self):
        # The new subsection is a level-4 heading nested inside the
        # existing "Data monitoring" subsection, not a new standalone
        # "## Worked example" section, so it must not perturb the
        # standalone count asserted in tests/test_documentation_structure.py.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 2)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 0)

    def test_is_the_eighth_level_4_nested_worked_example_in_domain_5(self):
        # Pre-existing level-4 nested worked examples: data-encryption-vs-
        # model-encryption, Titan Image Generator watermarking-provenance,
        # differential privacy, cost-capping, multi-team quota-sizing,
        # cost-optimization-SLA-tradeoffs, and shared-responsibility. This
        # one is the eighth.
        nested_level_4 = re.findall(r"^#### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_4), 8)

    def test_covers_the_rag_drift_scenario_and_vocabulary(self):
        for expected in [
            "Aurora Benefits Co.",
            "Bedrock RAG assistant",
            "hallucination rate",
            "factual consistency",
            "2%",
            "8%",
            "RAGAssistant/Quality",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_labeled_parts(self):
        for expected in [
            "**The scenario.**",
            "**Detecting and quantifying the drift.**",
            "**Thresholds and alarms.**",
            "**Remediation, and how this differs from classical drift monitoring.**",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_distinguishes_from_classical_drift_monitoring(self):
        self.assertIn("SageMaker Model Monitor", self.section)
        self.assertIn("retraining", self.section)
        self.assertIn("knowledge base", self.section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_word_count_is_within_requested_range(self):
        body = self.section
        body = re.sub(r"^#{1,4} .*\n", "", body)
        words = body.split()
        self.assertGreaterEqual(len(words), 250)
        self.assertLessEqual(len(words), 350)

    def test_data_monitoring_exam_tip_links_forward_to_the_worked_example(
        self,
    ):
        data_monitoring_section = _section(
            self.text,
            re.escape(DATA_MONITORING_HEADING),
            r"\n#{1,3} ",
        )
        self.assertIn(FORWARD_LINK, data_monitoring_section)


if __name__ == "__main__":
    unittest.main()
