"""Structural validation for the "Worked example: a Bedrock Agent executing
a multi-step task with tool calling" section added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3, Section 5 introduces Amazon Bedrock Agents
conceptually (plan -> invoke a tool -> observe the result -> continue) and
the Agents vs. Prompt Flows vs. prompt chaining comparison drills the
"who decides the next step" distinction, but nothing in the domain's
worked-example set actually traces an Agent through a concrete multi-step
request invoking more than one action group/tool. These tests guard the
worked example added to close that gap: it must exist, be linked from the
table of contents, sit between the fine-tuning-vs-prompt-engineering
worked example and the "Comparison table: customization approaches"
section, describe an Agent invoking multiple tools/action groups across a
plan -> invoke -> observe loop where a later tool call depends on an
earlier tool's result, and carry an AWS example and an exam tip like every
other worked example in this domain guide.

Mirrors the conventions established in
tests/test_domain_3_fine_tuning_vs_prompt_engineering_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_bedrock_agents_multi_step_worked_example.py -v
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
    "## Worked example: a Bedrock Agent executing a multi-step task with "
    "tool calling"
)
HEADING_REGEX = (
    r"\n## Worked example: a Bedrock Agent executing a multi-step task "
    r"with tool calling"
)
TOC_LINK = (
    "[Worked example: a Bedrock Agent executing a multi-step task with "
    "tool calling]"
    "(#worked-example-a-bedrock-agent-executing-a-multi-step-task-with-tool-calling)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,2} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading of the same or higher level, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3BedrockAgentsMultiStepWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_linked_from_the_table_of_contents(self):
        toc = _section(
            self.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        self.assertIn(TOC_LINK, toc)

    def test_worked_example_sits_between_fine_tuning_example_and_comparison_table(self):
        fine_tuning_pos = self.text.index(
            "## Worked example: comparing fine-tuning and prompt "
            "engineering on the same task"
        )
        comparison_table_pos = self.text.index(
            "## Comparison table: customization approaches for foundation "
            "model applications"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(fine_tuning_pos, heading_pos)
        self.assertLess(heading_pos, comparison_table_pos)

    def test_scenario_describes_a_multi_step_customer_request(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertRegex(self.section, r"(?i)order #48213")
        self.assertRegex(self.section, r"(?i)\$15 credit")

    def test_defines_two_action_groups_backed_by_lambda(self):
        self.assertIn("`CheckOrderStatus`", self.section)
        self.assertIn("`IssueCredit`", self.section)
        self.assertRegex(self.section, r"(?i)action groups?")
        self.assertRegex(self.section, r"(?i)lambda")
        self.assertRegex(self.section, r"(?i)openapi schema")

    def test_traces_the_plan_invoke_observe_loop_across_multiple_tool_calls(self):
        for expected in [
            "**Plan.**",
            "**Invoke (step 1).**",
            "**Observe (step 1).**",
            "**Re-plan.**",
            "**Invoke (step 2).**",
            "**Observe (step 2).**",
            "**Invoke (step 3).**",
            "**Observe (step 3).**",
            "**Final response.**",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_second_tool_call_is_conditioned_on_the_first_tools_result(self):
        self.assertRegex(self.section, r"(?i)delay_flag")
        self.assertRegex(
            self.section,
            r"(?i)knowledge base",
        )
        self.assertRegex(
            self.section,
            r"(?i)set of steps taken depends on an intermediate result",
        )

    def test_contrasts_with_prompt_flows_orchestration(self):
        self.assertRegex(
            self.section,
            r"\[Agents vs\. Prompt Flows vs\. prompt chaining\s+"
            r"comparison\]\(#bedrock-agents-vs-prompt-flows-vs-prompt-chaining-choosing-an-orchestration-approach\)",
        )

    def test_has_an_aws_example_referencing_bedrock_agents(self):
        self.assertIn("**AWS example:**", self.section)
        self.assertRegex(self.section, r"(?i)action group")

    def test_worked_example_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.section)
        self.assertRegex(self.section, r"(?i)re-planning based on what a prior tool call")


if __name__ == "__main__":
    unittest.main()
