"""Structural validation for the "Fine-tuning efficiency techniques: full
fine-tuning vs. LoRA vs. QLoRA vs. instruction tuning" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 4 compared fine-tuning vs. RAG vs.
prompting overall but never broke down parameter-efficient fine-tuning
methods (LoRA, QLoRA, instruction tuning) -- flagged by the documentation
scan as a missing diagram and a structural gap. These tests guard the new
subsection added to close that gap: it must exist inside "## 4. Fine-tuning
vs. continued pre-training vs. RAG vs. prompt engineering", sit before that
section's mini-quiz, be linked from the table of contents, contain a
Mermaid diagram covering full fine-tuning, LoRA, and QLoRA, a comparison
table contrasting all four techniques (including instruction tuning) on
training speedup, resource cost, and quality trade-offs, and an exam tip --
without adding any new numbered section or mini-quiz block (this repo's
structural tests assert exact counts for both).

Mirrors the conventions established in
tests/test_domain_3_embedding_model_selection_diagram.py.

Run with:
    python3 -m unittest tests/test_domain_3_fine_tuning_efficiency_techniques_diagram.py -v
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
    "### Fine-tuning efficiency techniques: full fine-tuning vs. LoRA vs. "
    "QLoRA vs. instruction tuning"
)
TOC_LINK = (
    "[Fine-tuning efficiency techniques: full fine-tuning vs. LoRA vs. "
    "QLoRA vs. instruction tuning]"
    "(#fine-tuning-efficiency-techniques-full-fine-tuning-vs-lora-vs-qlora-"
    "vs-instruction-tuning)"
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


class TestDomain3FineTuningEfficiencyTechniquesDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.subsection = _section(
            cls.text,
            re.escape(HEADING),
            r"\n#{1,3} ",
        )

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_sits_inside_section_4_before_its_mini_quiz(self):
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        heading_pos = section_4.index(HEADING)
        quiz_pos = section_4.index(MINI_QUIZ_HEADING)
        self.assertLess(
            heading_pos,
            quiz_pos,
            "new subsection must sit before Section 4's mini-quiz",
        )

    def test_diagram_is_a_mermaid_diagram(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        self.assertTrue(
            fences,
            "expected a ```mermaid fenced code block under the new heading",
        )
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"graph\s+\w+|flowchart\s+\w+",
            "diagram should use Mermaid graph/flowchart syntax",
        )
        self.diagram = diagram

    def test_diagram_covers_full_fine_tuning_lora_and_qlora(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        diagram = "\n".join(fences)
        for name_regex, label in [
            (r"Full fine-tuning", "full fine-tuning branch"),
            (r"LoRA", "LoRA branch"),
            (r"QLoRA", "QLoRA branch"),
        ]:
            with self.subTest(branch=label):
                self.assertRegex(
                    diagram, name_regex, f"diagram missing branch: {label!r}"
                )

    def test_diagram_covers_speedup_resource_cost_and_quality(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        diagram = "\n".join(fences)
        self.assertRegex(diagram, r"(?i)training speedup")
        self.assertRegex(diagram, r"(?i)resource cost")
        self.assertRegex(diagram, r"(?i)quality")

    def test_comparison_table_covers_all_four_techniques(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection
        )
        self.assertTrue(tables, "expected a Markdown comparison table")
        table = "\n".join(tables)
        for expected in [
            "Full fine-tuning",
            "LoRA",
            "QLoRA",
            "Instruction tuning",
            "Training speedup",
            "Resource cost",
            "Quality trade-off",
            "Best fit",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, table)

    def test_explains_instruction_tuning_is_an_objective_not_a_parameter_strategy(self):
        self.assertRegex(
            self.subsection,
            r"(?i)instruction tuning.{0,400}(full fine-tuning|LoRA|QLoRA)",
            "subsection should explain instruction tuning can be combined "
            "with full fine-tuning, LoRA, or QLoRA",
        )

    def test_mentions_resource_constrained_scenario_guidance(self):
        self.assertRegex(
            self.subsection,
            r"(?i)single.{0,20}GPU",
            "subsection should call out QLoRA's fit for a single smaller "
            "GPU / resource-constrained scenario",
        )

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
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
