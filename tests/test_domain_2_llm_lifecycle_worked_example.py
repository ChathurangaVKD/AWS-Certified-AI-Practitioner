"""Structural validation for the "Worked example: end-to-end LLM lifecycle
for an insurance claims-triage assistant" section added to
docs/domain-2-fundamentals-of-generative-ai.md.

The gap this covers: Domain 1 closes its ML lifecycle section with a full
end-to-end worked example tracing every stage of the classical ML
lifecycle for one continuous scenario (the loan-default predictor), but
Domain 2's three prior worked examples (token estimation, the generative
AI support assistant build, and the voice-assistant modality comparison)
each focus on a single isolated technique rather than lifecycle-stage
reasoning across all six Section 2 stages. These tests guard the new
worked example added to close that gap: it must exist as a standalone
"## Worked example" section, be linked from the table of contents, sit
after the voice-assistant worked example and before the comparison table,
walk through all six Section 2 LLM lifecycle stages (scope, select,
adapt/customize, evaluate, deploy, monitor) for one continuous scenario,
show the adaptation stage escalating from prompt engineering to RAG to
fine-tuning, close with an exam tip, and must not perturb the standalone
worked-example and numbered-section counts asserted elsewhere in this
repo's test suite.

Mirrors the conventions established in
tests/test_domain_1_canary_blue_green_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_2_llm_lifecycle_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-2-fundamentals-of-generative-ai.md"
)

HEADING = (
    "## Worked example: end-to-end LLM lifecycle for an insurance "
    "claims-triage assistant"
)
HEADING_REGEX = (
    r"\n## Worked example: end-to-end LLM lifecycle for an insurance "
    r"claims-triage assistant"
)
TOC_LINK = (
    "[Worked example: end-to-end LLM lifecycle for an insurance "
    "claims-triage assistant]"
    "(#worked-example-end-to-end-llm-lifecycle-for-an-insurance-claims-"
    "triage-assistant)"
)
VOICE_ASSISTANT_HEADING = (
    "## Worked example: selecting and comparing models for a real-time "
    "voice assistant use case"
)
COMPARISON_TABLE_HEADING = "## Comparison table: AWS generative AI services at a glance"


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


class TestDomain2LlmLifecycleWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(
            self.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        self.assertIn(TOC_LINK, toc)

    def test_sits_after_voice_assistant_example_and_before_comparison_table(
        self,
    ):
        voice_pos = self.text.index(VOICE_ASSISTANT_HEADING)
        heading_pos = self.text.index(HEADING)
        table_pos = self.text.index(COMPARISON_TABLE_HEADING)
        self.assertLess(voice_pos, heading_pos)
        self.assertLess(heading_pos, table_pos)

    def test_does_not_change_standalone_worked_example_or_section_counts(
        self,
    ):
        # This is a fourth standalone "## Worked example" section for
        # Domain 2 (per docs/DOCUMENTATION_STRUCTURE.md's "Domain 2 also
        # grew beyond a single worked example..." paragraph), and it must
        # not add or remove any of the seven required numbered topic
        # sections.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 4)
        numbered_sections = re.findall(r"\n## [1-7]\. ", self.text)
        self.assertEqual(len(numbered_sections), 7)

    def test_has_a_scenario(self):
        self.assertIn("**Scenario:**", self.section)

    def test_walks_through_all_six_lifecycle_stages(self):
        for expected in [
            "**Scope the use case.**",
            "**Select a foundation model.**",
            "**Adapt and customize the model**",
            "**Evaluate the model.**",
            "**Deploy and integrate.**",
            "**Monitor.**",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_adaptation_stage_escalates_prompt_engineering_to_rag_to_fine_tuning(
        self,
    ):
        adapt_start = self.section.index("**Adapt and customize the model**")
        evaluate_start = self.section.index("**Evaluate the model.**")
        adapt_text = self.section[adapt_start:evaluate_start]
        prompt_pos = adapt_text.index("prompt engineering")
        rag_pos = adapt_text.index("Retrieval\n   Augmented Generation") if (
            "Retrieval\n   Augmented Generation" in adapt_text
        ) else adapt_text.index("Retrieval")
        finetune_pos = adapt_text.index("fine-tunes")
        pretrain_pos = adapt_text.index("continued\n   pre-training") if (
            "continued\n   pre-training" in adapt_text
        ) else adapt_text.lower().index("pre-training")
        self.assertLess(prompt_pos, rag_pos)
        self.assertLess(rag_pos, finetune_pos)
        self.assertLess(finetune_pos, pretrain_pos)

    def test_mentions_relevant_aws_services(self):
        # Markdown source wraps long lines, so a multi-word service name can
        # legitimately have a line break inside it (e.g. "Amazon Bedrock
        # Model\n   Evaluation"); collapse whitespace before comparing.
        normalized = re.sub(r"\s+", " ", self.section)
        for service in [
            "Amazon Bedrock",
            "Knowledge Bases for Amazon Bedrock",
            "Amazon Bedrock Model Evaluation",
            "Guardrails for Amazon Bedrock",
            "Amazon CloudWatch",
        ]:
            with self.subTest(service=service):
                self.assertIn(service, normalized)

    def test_cross_links_to_domain_1_lifecycle_example(self):
        self.assertIn(
            "domain-1-fundamentals-of-ai-and-ml.md"
            "#worked-example-end-to-end-ml-lifecycle-for-a-loan-default-predictor",
            self.section,
        )

    def test_cross_links_to_section_2_lifecycle_diagram(self):
        self.assertIn("#2-llm-lifecycle-basics", self.section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)


if __name__ == "__main__":
    unittest.main()
