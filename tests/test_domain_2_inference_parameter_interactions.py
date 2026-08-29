"""Structural validation for the Domain 2 inference-parameter interaction
guide (temperature / top-p / top-k).

Domain 2 previously covered temperature, top-p, and top-k as three
independent bullet points, with no visual showing how they *interact* --
the exam tests exactly this (e.g., why setting top-k without adjusting
temperature can produce unexpected behavior). This test asserts that the
prompt-engineering section ("## 6. Prompt engineering fundamentals")
contains: a dedicated Mermaid diagram showing the order-of-operations
pipeline (temperature reshapes the distribution, then top-p/top-k prune
the candidate pool, then sampling happens), a comparison table of example
(temperature, top-p, top-k) combinations with their qualitative effect,
and a concrete exam scenario tying a low-moderate temperature + guardrails
combination to a "creative but not harmful" chatbot requirement -- so a
future edit that drops any of these pieces is caught automatically instead
of only in manual review.

Mirrors the conventions established in tests/test_domain_2_study_guide.py.

Run with:
    python3 -m unittest tests/test_domain_2_inference_parameter_interactions.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-2-fundamentals-of-generative-ai.md"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    """Return the text between a heading matching start_heading_regex and
    the next top-level (##) heading, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestInferenceParameterInteractionGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(
            cls.text, r"\n## 6\. Prompt engineering fundamentals"
        )

    def test_section_has_an_interaction_mermaid_diagram(self):
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", self.section, re.S)
        self.assertTrue(
            mermaid_blocks,
            "prompt engineering section should include a Mermaid diagram "
            "of how temperature/top-p/top-k interact",
        )
        # The interaction diagram is the one that walks through the
        # temperature -> top-k/top-p -> sampling pipeline.
        interaction_diagrams = [
            b for b in mermaid_blocks if "Apply temperature" in b
        ]
        self.assertTrue(
            interaction_diagrams,
            "expected a Mermaid diagram showing the temperature -> "
            "top-p/top-k -> sampling order of operations",
        )
        diagram = "\n".join(interaction_diagrams)

        for node in [
            "Raw next-token probability",
            "Apply temperature",
            "Apply top-k / top-p",
            "Sample the next token",
            "Sharper distribution",
            "Flatter distribution",
            "Narrow candidate pool",
            "Wide candidate pool",
        ]:
            with self.subTest(node=node):
                self.assertIn(node, diagram)

        self.assertRegex(
            diagram, r"-->", "diagram should connect stages with flowchart edges"
        )

    def test_section_has_a_parameter_combination_table(self):
        # A markdown table with header separator like |---|---|---|
        self.assertRegex(
            self.section,
            r"\|\s*Temperature\s*\|\s*Top-p\s*\|\s*Top-k\s*\|",
            "expected a table listing example (temperature, top-p, top-k) "
            "combinations",
        )
        self.assertRegex(self.section, r"\|\s*-{2,}\s*\|")

        # Should span the deterministic -> creative spectrum and the
        # narrowed-focus -> broad-sampling spectrum called out in the task.
        for phrase in [
            "Deterministic, repeatable, narrowly focused",
            "Highly creative, varied, less predictable",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.section)

    def test_table_documents_the_top_k_without_temperature_interaction_trap(self):
        # The task explicitly calls out that setting top-k without
        # adjusting temperature can cause unexpected behavior -- assert
        # that exact interaction trap is documented, not just implied.
        self.assertIn(
            "top-k without adjusting temperature",
            self.section,
            "should explicitly explain the top-k-without-temperature "
            "interaction trap called out in the task",
        )

    def test_section_has_a_concrete_exam_scenario_with_guardrails(self):
        self.assertIn("Exam scenario:", self.section)
        scenario_match = re.search(
            r"Exam scenario:.*?(?=\n\n)", self.section, re.S
        )
        self.assertTrue(scenario_match, "expected an 'Exam scenario' callout")
        # Collapse markdown line-wrapping and blockquote markers so phrases
        # that happen to wrap across lines (e.g. "Guardrails for Amazon\n>
        # Bedrock") still match.
        scenario = re.sub(r"\s*\n>\s*", " ", scenario_match.group(0))
        scenario = re.sub(r"\s+", " ", scenario)

        self.assertIn("chatbot", scenario.lower())
        self.assertIn("harmful", scenario.lower())
        self.assertIn("Guardrails for Amazon Bedrock", scenario)
        self.assertRegex(
            scenario,
            r"low-to-moderate temperature|low-moderate temperature",
            "exam scenario should recommend a low-moderate temperature, "
            "not zero temperature or a guardrails-only answer",
        )


if __name__ == "__main__":
    unittest.main()
