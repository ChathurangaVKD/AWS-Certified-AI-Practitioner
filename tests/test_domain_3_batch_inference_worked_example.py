"""Structural validation for the "Batch inference vs. real-time vs.
provisioned throughput: a worked cost-and-latency example" subsection
added to docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 mentions Bedrock batch inference roughly
half a dozen times (the real-time-vs-batch decision tree in Section 8,
the inference-failures scenario about a batch job timing out, the
cost-governance discussion of provisioned throughput vs. on-demand) but
never once attaches a number to it -- a candidate can recite "batch is
cheaper when nothing is waiting on the response" without being able to
size that discount or decide, given a deadline and a volume, whether
batch actually fits. These tests guard the new worked example added to
close that gap: it must exist inside "## 5. Amazon Bedrock features",
sit after the on-demand vs. provisioned throughput worked example and
before that section's mini-quiz, and cover (1) a concrete daily-volume
scenario, (2) side-by-side monthly cost arithmetic for batch,
real-time, and provisioned throughput, (3) a decision flowchart keyed on
deadline and volume, and (4) implementation notes on batching request
payloads and scheduling batch jobs.

Mirrors the conventions established in
tests/test_domain_3_provisioned_throughput_worked_example.py (including
deliberately avoiding the "#### Worked example:" heading prefix so as
not to perturb the pinned worked-example heading counts asserted in
tests/test_documentation_structure.py).

Run with:
    python3 -m unittest tests/test_domain_3_batch_inference_worked_example.py -v
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
PROVISIONED_THROUGHPUT_HEADING = (
    "#### On-demand vs. provisioned throughput: a worked cost-comparison "
    "example"
)
HEADING = (
    "#### Batch inference vs. real-time vs. provisioned throughput: a "
    "worked cost-and-latency example"
)
TOC_LINK = (
    "[Batch inference vs. real-time vs. provisioned throughput: a worked "
    "cost-and-latency example]"
    "(#batch-inference-vs-real-time-vs-provisioned-throughput-a-worked-"
    "cost-and-latency-example)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3BatchInferenceWorkedExample(unittest.TestCase):
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

    def test_sits_after_provisioned_throughput_example_and_before_mini_quiz(self):
        section_5 = _section(
            self.text,
            r"\n## 5\. Amazon Bedrock features",
            r"\n## 6\. ",
        )
        provisioned_pos = section_5.index(PROVISIONED_THROUGHPUT_HEADING)
        heading_pos = section_5.index(HEADING)
        quiz_pos = section_5.index(
            "#### Mini-quiz: Test your understanding of Amazon Bedrock features"
        )
        self.assertLess(provisioned_pos, heading_pos)
        self.assertLess(heading_pos, quiz_pos)

    def test_sits_inside_cost_governance_subsection(self):
        section_5 = _section(
            self.text,
            r"\n## 5\. Amazon Bedrock features",
            r"\n## 6\. ",
        )
        cost_gov_pos = section_5.index(COST_GOVERNANCE_HEADING)
        heading_pos = section_5.index(HEADING)
        self.assertLess(cost_gov_pos, heading_pos)

    def test_has_a_realistic_daily_and_monthly_volume(self):
        for expected in ["20,000 emails/day", "600,000 requests/month"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_has_a_per_request_token_estimate(self):
        for expected in ["600 input tokens", "120 output tokens"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_has_an_explicit_deadline(self):
        self.assertIn("8-hour deadline", self.subsection)

    def test_has_side_by_side_monthly_cost_for_all_three_options(self):
        self.assertIn("**$90/month**", self.subsection)
        self.assertIn("**$180/month**", self.subsection)
        self.assertIn("**$2,190/month**", self.subsection)

    def test_has_a_batch_discount_relative_to_on_demand(self):
        self.assertRegex(self.subsection, r"(?i)50% discount")
        self.assertIn("$0.00015/request", self.subsection)
        self.assertIn("$0.0003/request", self.subsection)

    def test_has_a_side_by_side_comparison_table(self):
        self.assertIn("| Option | Cost/request |", self.subsection)
        self.assertIn("**Bedrock batch inference**", self.subsection)
        self.assertIn("**On-demand real-time**", self.subsection)
        self.assertIn("**Provisioned throughput**", self.subsection)

    def test_has_a_mermaid_decision_flowchart_keyed_on_deadline_and_volume(self):
        fences = re.findall(r"```mermaid(.*?)```", self.subsection, re.S)
        self.assertEqual(
            len(fences), 1, "expected exactly one Mermaid flowchart in this subsection"
        )
        flowchart = fences[0]
        self.assertIn("flowchart TD", flowchart)
        self.assertRegex(flowchart, r"(?i)response within seconds")
        self.assertRegex(flowchart, r"(?i)completion-\\nwindow deadline")
        self.assertIn("BEDROCK BATCH INFERENCE", flowchart)
        self.assertIn("ON-DEMAND REAL-TIME", flowchart)
        self.assertIn("PROVISIONED THROUGHPUT", flowchart)

    def test_has_prose_decision_rule_keyed_on_deadline_and_volume(self):
        self.assertRegex(self.subsection, r"(?i)hard per-request SLA")
        self.assertRegex(self.subsection, r"(?i)completion\s+window of a few\s+hours or more")
        # The flowchart node text embeds a literal "\n" (backslash-n) as
        # Mermaid's line-break escape, not an actual newline.
        self.assertIn("batch's\\nper-job minimum", self.subsection)

    def test_has_implementation_notes_on_batching_payloads_and_scheduling(self):
        for expected in [
            "JSONL",
            "recordId",
            "modelInput",
            "EventBridge Scheduler",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

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
