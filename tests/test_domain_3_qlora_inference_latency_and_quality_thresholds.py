"""Structural validation for the "QLoRA in production: inference-latency
profile and generalized quality-metric thresholds" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 4's fine-tuning efficiency
subsections quantified *training-time* GPU memory and training time for
full fine-tuning, LoRA, and QLoRA, and worked through one metric pair
(ROUGE-L plus a clinical safety metric) in a single worked example -- but
never quantified *inference-time* latency once a fine-tuned model is
deployed, nor generalized the quality trade-off across the standard
BLEU/ROUGE/F1 metric families, nor offered a standalone decision rule
tying memory, latency, and quality thresholds together (flagged by
identified_content_gaps: "Domain 3: QLoRA quantization trade-offs
(memory/quality thresholds unclear)"). These tests guard the new
subsection added to close that gap: it must sit inside "## 4. Fine-tuning
vs. continued pre-training vs. RAG vs. prompt engineering", after the
existing "when does QLoRA's quality loss become unacceptable?" worked
example and before that section's mini-quiz, contain an inference-latency
comparison table covering merged and unmerged serving for full
fine-tuning, LoRA, and QLoRA, a generalized BLEU/ROUGE/F1 quality
degradation table, and decision guidance for when QLoRA is sufficient
vs. when full fine-tuning is required -- without adding any new numbered
section or a second mini-quiz (this repo's structural tests assert exact
counts for both).

Mirrors the conventions established in
tests/test_domain_3_fine_tuning_technique_decision_flowchart.py.

Run with:
    python3 -m unittest tests/test_domain_3_qlora_inference_latency_and_quality_thresholds.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

NEW_HEADING = (
    "#### QLoRA in production: inference-latency profile and "
    "generalized quality-metric thresholds"
)
PRIOR_WORKED_EXAMPLE_HEADING = (
    "#### Worked example: when does QLoRA's quality loss become "
    "unacceptable?"
)
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of customization approach "
    "trade-offs"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3QloraInferenceLatencyAndQualityThresholds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.subsection = _section(
            cls.text,
            re.escape(NEW_HEADING),
            re.escape(MINI_QUIZ_HEADING),
        )

    def test_heading_exists(self):
        self.assertIn(NEW_HEADING, self.text)

    def test_sits_after_prior_worked_example_and_before_the_mini_quiz(self):
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        prior_pos = section_4.index(PRIOR_WORKED_EXAMPLE_HEADING)
        new_pos = section_4.index(NEW_HEADING)
        quiz_pos = section_4.index(MINI_QUIZ_HEADING)
        self.assertLess(prior_pos, new_pos)
        self.assertLess(new_pos, quiz_pos)

    def test_has_an_inference_latency_comparison_table(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection
        )
        self.assertTrue(tables, "expected Markdown comparison tables")
        table = "\n".join(tables)
        for expected in [
            "inference latency",
            "Full fine-tuning",
            "LoRA, merged",
            "LoRA, unmerged",
            "QLoRA, merged",
            "QLoRA, unmerged",
        ]:
            with self.subTest(expected=expected):
                self.assertRegex(table, re.escape(expected), re.IGNORECASE)

    def test_latency_table_has_relative_numeric_multipliers(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection
        )
        table = "\n".join(tables)
        # Relative latency figures like "1.0x" or "~1.15-1.3x".
        self.assertRegex(table, r"~?\d+(?:\.\d+)?x\b")

    def test_has_a_generalized_bleu_rouge_f1_degradation_table(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection
        )
        table = "\n".join(tables)
        for expected in ["BLEU", "ROUGE-L", "F1"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, table)
        # Each fine-tuning technique row should be present in that table.
        for technique in ["Full fine-tuning", "LoRA", "QLoRA"]:
            with self.subTest(technique=technique):
                self.assertIn(technique, table)

    def test_degradation_table_has_point_estimates(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection
        )
        table = "\n".join(tables)
        self.assertRegex(
            table,
            r"-?\d+(?:\.\d+)?\s*(?:to|-)\s*-?\d+(?:\.\d+)?\s*points?",
            "expected point-based degradation estimates (e.g. '-1 to -2 "
            "points') in the quality table",
        )

    def test_gives_decision_guidance_for_qlora_sufficient_vs_full_fine_tuning(self):
        self.assertRegex(
            self.subsection,
            r"(?i)QLoRA is sufficient",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)Full fine-tuning is required",
        )

    def test_explains_merging_removes_serving_time_overhead(self):
        self.assertRegex(
            self.subsection,
            r"(?i)merged.{0,300}(same latency|baseline latency|same as full fine-tuning)",
            "subsection should explain that a merged adapter serves at "
            "baseline latency",
        )

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_no_new_numbered_section_or_extra_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-8]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            8,
            "Domain 3 must still have exactly 8 numbered sections",
        )
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_4)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 4 must still contain exactly one mini-quiz heading",
        )


if __name__ == "__main__":
    unittest.main()
