"""Structural validation for the "Choosing among on-demand, provisioned
throughput, and batch inference: a decision guide" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3's cost-governance material already builds
up two deep, numbers-heavy worked examples -- on-demand vs. provisioned
throughput, and batch vs. real-time vs. provisioned throughput -- but has
no scenario-first entry point that lets a reader map a scenario's SLA,
request volume, and latency tolerance straight to the cost-optimal
capacity choice without running the arithmetic first. These tests guard
the new decision guide added to close that gap: it must exist inside
"## 5. Amazon Bedrock features", sit right after the cost-governance
introduction's exam tip and before the "On-demand vs. provisioned
throughput" worked example (i.e. as the scenario-driven entry point the
two worked examples elaborate on), be linked from the table of contents,
and cover all three capacity options keyed on SLA, volume, and latency
tolerance.

Mirrors the conventions established in
tests/test_domain_3_batch_inference_worked_example.py and
tests/test_domain_3_cost_governance_subsection.py (including
deliberately avoiding the "#### Worked example: ..." heading prefix so
as not to perturb the pinned worked-example heading counts asserted in
tests/test_documentation_structure.py).

Run with:
    python3 -m unittest tests/test_domain_3_inference_cost_decision_guide.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

COST_GOVERNANCE_HEADING = (
    "### Cost governance: bounding per-request cost with max tokens and "
    "provisioned throughput"
)
HEADING = (
    "#### Choosing among on-demand, provisioned throughput, and batch "
    "inference: a decision guide"
)
PROVISIONED_THROUGHPUT_HEADING = (
    "#### On-demand vs. provisioned throughput: a worked cost-comparison "
    "example"
)
BATCH_HEADING = (
    "#### Batch inference vs. real-time vs. provisioned throughput: a "
    "worked cost-and-latency example"
)
TOC_LINK = (
    "[Choosing among on-demand, provisioned throughput, and batch "
    "inference: a decision guide]"
    "(#choosing-among-on-demand-provisioned-throughput-and-batch-"
    "inference-a-decision-guide)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3InferenceCostDecisionGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.subsection = _section(
            cls.text,
            re.escape(HEADING),
            r"\n#{1,4} ",
        )

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(
            self.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        self.assertIn(TOC_LINK, toc)

    def test_sits_inside_cost_governance_before_the_worked_examples(self):
        section_5 = _section(
            self.text,
            r"\n## 5\. Amazon Bedrock features",
            r"\n## 6\. ",
        )
        cost_gov_pos = section_5.index(COST_GOVERNANCE_HEADING)
        heading_pos = section_5.index(HEADING)
        provisioned_pos = section_5.index(PROVISIONED_THROUGHPUT_HEADING)
        batch_pos = section_5.index(BATCH_HEADING)
        quiz_pos = section_5.index(
            "#### Mini-quiz: Test your understanding of Amazon Bedrock features"
        )
        self.assertLess(cost_gov_pos, heading_pos)
        self.assertLess(heading_pos, provisioned_pos)
        self.assertLess(provisioned_pos, batch_pos)
        self.assertLess(batch_pos, quiz_pos)

    def test_covers_all_three_capacity_options(self):
        for expected in [
            "on-demand real-time",
            "provisioned throughput",
            "Bedrock batch inference",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_keys_the_decision_on_sla_volume_and_latency_tolerance(self):
        for expected in [
            "SLA",
            "request volume",
            "latency tolerance",
            "completion-window deadline",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_has_a_decision_table_mapping_constraints_to_a_choice(self):
        self.assertIn(
            "| Per-request SLA (latency tolerance) | Request volume | "
            "Cost-optimal choice | Why |",
            self.subsection,
        )
        self.assertIn("**On-demand real-time**", self.subsection)
        self.assertIn("**Provisioned throughput**", self.subsection)
        self.assertIn("**Bedrock batch inference**", self.subsection)

    def test_has_scenario_walkthrough_examples(self):
        self.assertIn("live chat widget", self.subsection)
        self.assertIn("search-ranking API", self.subsection)
        self.assertIn("stand-up", self.subsection)
        self.assertIn("legacy support tickets", self.subsection)

    def test_cross_links_to_both_worked_examples(self):
        self.assertIn(
            "#on-demand-vs-provisioned-throughput-a-worked-cost-comparison-example",
            self.subsection,
        )
        self.assertIn(
            "#batch-inference-vs-real-time-vs-provisioned-throughput-a-"
            "worked-cost-and-latency-example",
            self.subsection,
        )

    def test_has_an_aws_example_and_exam_tip(self):
        self.assertIn("**AWS example:**", self.subsection)
        self.assertIn("Exam tip:", self.subsection)

    def test_does_not_use_the_worked_example_heading_prefix(self):
        # Deliberately avoids "#### Worked example: ..." so it does not
        # perturb the pinned worked-example heading counts asserted in
        # tests/test_documentation_structure.py.
        self.assertNotRegex(HEADING, r"^#{2,4} Worked examples?:")

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-8]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            8,
            "Domain 3 must still have exactly 8 numbered sections",
        )
        section_5 = _section(
            self.text,
            r"\n## 5\. Amazon Bedrock features",
            r"\n## 6\. ",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_5)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 5 must still contain exactly one mini-quiz heading",
        )


if __name__ == "__main__":
    unittest.main()
