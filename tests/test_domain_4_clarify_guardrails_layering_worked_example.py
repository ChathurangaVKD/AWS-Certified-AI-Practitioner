"""Structural validation for the SageMaker Clarify + Guardrails for Amazon
Bedrock layering worked example nested inside Section 3 of
docs/domain-4-guidelines-for-responsible-ai.md.

The gap this covers: Section 3 introduces Amazon SageMaker Clarify
(pre-generation training-data/model bias analysis) and Guardrails for
Amazon Bedrock (runtime content filtering) as separate tools solving
separate problems, but -- before this change -- no worked example showed
them layered together on a single generative AI application. This test
file guards the new "### Worked example: layering SageMaker Clarify and
Guardrails for Amazon Bedrock to audit a generative recommendation
engine" subsection, nested inside Section 3 right after the existing
Amazon A2I worked example and before Section 3's mini-quiz, mirroring the
nested "###"/"####" worked-example convention used elsewhere (e.g.
tests/test_domain_4_confidence_threshold_a2i_worked_example.py).

Run with:
    python3 -m unittest tests/test_domain_4_clarify_guardrails_layering_worked_example.py -v
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
    "### Worked example: layering SageMaker Clarify and Guardrails for "
    "Amazon Bedrock to audit a generative recommendation engine"
)
A2I_WORKED_EXAMPLE_HEADING = (
    "### Worked example: routing low-confidence predictions to human "
    "review with Amazon A2I"
)
SECTION_3_HEADING = "## 3. AWS tools for responsible AI"
SECTION_4_HEADING = "## 4. Legal and ethical considerations"
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of AWS tools for "
    "responsible AI"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading, end_heading_regex=r"\n## "):
    """Return the text between an exact start_heading string and the next
    matching heading, or end of file."""
    start = text.index(start_heading)
    rest = text[start + len(start_heading):]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain4ClarifyGuardrailsLayeringWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        # Bounded by the mini-quiz heading that follows it, not just the
        # next "## " top-level heading -- the worked example sits *before*
        # Section 3's mini-quiz, so without this explicit bound the
        # section would swallow the mini-quiz too (a "#### " heading isn't
        # matched by the default "\n## " boundary).
        cls.section = _section(
            cls.text, WORKED_EXAMPLE_HEADING, re.escape("\n" + MINI_QUIZ_HEADING)
        )
        # Markdown line-wraps mid-phrase, so phrase-level assertions match
        # against whitespace-normalized text rather than the raw,
        # line-wrapped section.
        cls.normalized = re.sub(r"\s+", " ", cls.section)

    def test_heading_exists(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.text)

    def test_nested_as_h3_not_a_standalone_h2(self):
        self.assertTrue(WORKED_EXAMPLE_HEADING.startswith("### "))
        self.assertNotIn("#" + WORKED_EXAMPLE_HEADING, self.text)

    def test_appears_inside_section_3_after_a2i_example_before_mini_quiz(self):
        section3_idx = self.text.index(SECTION_3_HEADING)
        a2i_idx = self.text.index(A2I_WORKED_EXAMPLE_HEADING)
        worked_idx = self.text.index(WORKED_EXAMPLE_HEADING)
        mini_quiz_idx = self.text.index(MINI_QUIZ_HEADING)
        section4_idx = self.text.index(SECTION_4_HEADING)
        self.assertLess(section3_idx, a2i_idx)
        self.assertLess(a2i_idx, worked_idx)
        self.assertLess(worked_idx, mini_quiz_idx)
        self.assertLess(mini_quiz_idx, section4_idx)

    def test_not_listed_as_a_standalone_toc_entry(self):
        # Nested "###" worked examples aren't given their own top-level
        # table-of-contents bullet elsewhere in this doc series (mirrors
        # the Domain 4 A2I and Domain 5 cost-capping subsections), so this
        # one shouldn't be either.
        toc = _section(self.text, "## Table of contents", r"\n## Domain overview")
        self.assertNotIn("Worked example: layering SageMaker Clarify", toc)

    def test_has_scenario_and_exam_tip(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_names_both_tools_being_layered(self):
        for term in ["SageMaker Clarify", "Guardrails for Amazon Bedrock"]:
            with self.subTest(term=term):
                self.assertIn(term, self.normalized)

    def test_describes_two_distinct_stages(self):
        self.assertIn("Stage 1", self.section)
        self.assertIn("Stage 2", self.section)
        self.assertRegex(self.normalized, r"(?i)pre-generation")
        self.assertRegex(self.normalized, r"(?i)runtime")

    def test_covers_pre_training_and_post_training_clarify_metrics(self):
        for term in [
            "pre-training",
            "post-training",
            "class imbalance",
            "difference in proportions of labels",
            "disparate impact",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.normalized)

    def test_covers_guardrails_capabilities(self):
        for term in [
            "content filters",
            "denied topics",
            "word filters",
            "sensitive information filters",
            "contextual grounding checks",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.normalized)

    def test_names_a_generative_ai_recommendation_scenario(self):
        self.assertRegex(
            self.normalized,
            r"(?i)fine-tun|foundation model|generative",
            "expected a generative AI / foundation model recommendation scenario",
        )

    def test_explains_why_neither_stage_alone_is_sufficient(self):
        self.assertRegex(
            self.normalized,
            r"(?i)neither.{0,60}(substitute|enough|sufficient)|one stage alone",
            "expected the example to explicitly justify layering both tools "
            "rather than picking one",
        )

    def test_describes_a_feedback_loop_from_runtime_back_to_training_data(self):
        self.assertRegex(
            self.normalized,
            r"(?i)feed.{0,40}back|feedback loop",
            "expected a blocked runtime interaction to feed back into the "
            "training-data audit stage",
        )

    def test_documents_in_a_model_card_and_monitors_with_model_monitor(self):
        self.assertIn("Model Card", self.normalized)
        self.assertIn("SageMaker Model Monitor", self.normalized)

    def test_includes_a_mermaid_pipeline_diagram(self):
        self.assertIn("```mermaid", self.section)
        self.assertIn("flowchart TD", self.section)

    def test_includes_a_stage_comparison_table(self):
        self.assertIn("| Stage 1: SageMaker Clarify", self.section)
        self.assertIn("Stage 2: Guardrails for Amazon Bedrock", self.section)

    def test_has_at_least_ten_numbered_steps(self):
        steps = re.findall(r"^\d+\.\s", self.section, re.M)
        self.assertGreaterEqual(
            len(steps),
            10,
            "worked example should walk through at least ten numbered steps "
            "across both stages",
        )

    def test_word_count_within_expected_range(self):
        words = re.findall(r"\w+", self.section)
        self.assertGreaterEqual(len(words), 900)
        self.assertLessEqual(len(words), 2200)


if __name__ == "__main__":
    unittest.main()
