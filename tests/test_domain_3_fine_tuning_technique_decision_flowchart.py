"""Structural validation for the "Choosing a fine-tuning efficiency
technique: GPU memory, training time, and quality benchmarks" subsection
added to docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 4's "Fine-tuning efficiency
techniques" subsection (full fine-tuning vs. LoRA vs. QLoRA vs.
instruction tuning) was purely qualitative -- "low," "modest trade-off,"
"lowest" -- with no quantitative GPU memory, training time, or accuracy
numbers, and no worked example showing when a technique's quality
trade-off actually becomes unacceptable. This test file guards the new
subsection added to close that gap: it must sit inside "## 4. Fine-tuning
vs. continued pre-training vs. RAG vs. prompt engineering", after the
existing "Fine-tuning efficiency techniques" exam tip and before that
section's mini-quiz, contain a Mermaid decision flowchart titled
"Choosing a fine-tuning efficiency technique" that covers full
fine-tuning, LoRA, and QLoRA, a comparison table with approximate GPU
memory, training time, and quality-trade-off columns for all four
techniques, and a worked example contrasting a scenario where QLoRA's
quality loss is unacceptable against one where it's fine -- without
adding any new numbered section or a second mini-quiz (this repo's
structural tests assert exact counts for both).

Mirrors the conventions established in
tests/test_domain_3_fine_tuning_efficiency_techniques_diagram.py.

Run with:
    python3 -m unittest tests/test_domain_3_fine_tuning_technique_decision_flowchart.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

FLOWCHART_HEADING = (
    "#### Choosing a fine-tuning efficiency technique: GPU memory, "
    "training time, and quality benchmarks"
)
WORKED_EXAMPLE_HEADING = (
    "#### Worked example: when does QLoRA's quality loss become "
    "unacceptable?"
)
PRIOR_SUBSECTION_HEADING = (
    "### Fine-tuning efficiency techniques: full fine-tuning vs. LoRA vs. "
    "QLoRA vs. instruction tuning"
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


class TestDomain3FineTuningTechniqueDecisionFlowchart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        # Everything from the new flowchart heading up to (not including)
        # the section's mini-quiz -- covers both new subsections.
        cls.new_content = _section(
            cls.text,
            re.escape(FLOWCHART_HEADING),
            re.escape(MINI_QUIZ_HEADING),
        )
        cls.flowchart_subsection = _section(
            cls.text,
            re.escape(FLOWCHART_HEADING),
            re.escape(WORKED_EXAMPLE_HEADING),
        )
        cls.worked_example_subsection = _section(
            cls.text,
            re.escape(WORKED_EXAMPLE_HEADING),
            re.escape(MINI_QUIZ_HEADING),
        )

    def test_both_headings_exist(self):
        self.assertIn(FLOWCHART_HEADING, self.text)
        self.assertIn(WORKED_EXAMPLE_HEADING, self.text)

    def test_sits_after_prior_subsection_and_before_the_mini_quiz(self):
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        prior_pos = section_4.index(PRIOR_SUBSECTION_HEADING)
        flowchart_pos = section_4.index(FLOWCHART_HEADING)
        worked_example_pos = section_4.index(WORKED_EXAMPLE_HEADING)
        quiz_pos = section_4.index(MINI_QUIZ_HEADING)
        self.assertLess(prior_pos, flowchart_pos)
        self.assertLess(flowchart_pos, worked_example_pos)
        self.assertLess(worked_example_pos, quiz_pos)

    def test_flowchart_is_titled_choosing_a_fine_tuning_efficiency_technique(self):
        self.assertRegex(
            self.flowchart_subsection,
            r"(?i)choosing a fine-tuning efficiency technique",
        )

    def test_diagram_is_a_mermaid_flowchart(self):
        fences = re.findall(
            r"```mermaid(.*?)```", self.flowchart_subsection, re.S
        )
        self.assertTrue(
            fences,
            "expected a ```mermaid fenced code block under the new heading",
        )
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+",
            "diagram should use Mermaid flowchart syntax",
        )
        self.diagram = diagram

    def test_diagram_covers_full_fine_tuning_lora_and_qlora(self):
        fences = re.findall(
            r"```mermaid(.*?)```", self.flowchart_subsection, re.S
        )
        diagram = "\n".join(fences)
        for name_regex, label in [
            (r"FULL FINE-TUNING", "full fine-tuning branch"),
            (r"LoRA", "LoRA branch"),
            (r"QLoRA", "QLoRA branch"),
        ]:
            with self.subTest(branch=label):
                self.assertRegex(
                    diagram, name_regex, f"diagram missing branch: {label!r}"
                )

    def test_diagram_has_decision_nodes(self):
        fences = re.findall(
            r"```mermaid(.*?)```", self.flowchart_subsection, re.S
        )
        diagram = "\n".join(fences)
        decision_nodes = re.findall(r"\{[^{}]+\}", diagram)
        self.assertGreaterEqual(
            len(decision_nodes),
            2,
            "expected multiple decision (diamond) nodes in the flowchart",
        )

    def test_comparison_table_has_gpu_memory_time_and_quality_columns(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.flowchart_subsection
        )
        self.assertTrue(tables, "expected a Markdown comparison table")
        table = "\n".join(tables)
        for expected in [
            "GPU memory",
            "training time",
            "quality",
            "Full fine-tuning",
            "LoRA",
            "QLoRA",
            "Instruction tuning",
        ]:
            with self.subTest(expected=expected):
                self.assertRegex(table, re.escape(expected), re.IGNORECASE)

    def test_comparison_table_has_approximate_numeric_figures(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.flowchart_subsection
        )
        table = "\n".join(tables)
        # GPU memory figures like "~112 GB" or "~16-24 GB" and a relative
        # training-time multiplier like "1.0x" or "~0.3-0.4x".
        self.assertRegex(table, r"~?\d+(?:\.\d+)?\s*(?:GB|x)\b")

    def test_has_a_worked_example_with_a_quantitative_results_table(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)",
            self.worked_example_subsection,
        )
        self.assertTrue(
            tables, "expected a quantitative results table in the worked example"
        )

    def test_worked_example_shows_qlora_unacceptable_scenario(self):
        self.assertRegex(
            self.worked_example_subsection,
            r"(?i)QLoRA.{0,600}(fails|unacceptable|exceed)",
            "worked example should show a scenario where QLoRA's quality "
            "loss is unacceptable",
        )

    def test_worked_example_shows_full_fine_tuning_justified_scenario(self):
        self.assertRegex(
            self.worked_example_subsection,
            r"(?i)full fine-tuning is justified",
            "worked example should explicitly justify full fine-tuning in "
            "the high-stakes scenario",
        )

    def test_worked_example_also_shows_a_scenario_where_qlora_is_fine(self):
        self.assertRegex(
            self.worked_example_subsection,
            r"(?i)QLoRA.{0,400}(acceptable|fine|flips)",
            "worked example should also show a low-stakes scenario where "
            "QLoRA's quality trade-off is acceptable",
        )

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
