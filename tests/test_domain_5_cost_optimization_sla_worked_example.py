"""Structural validation for the "Worked example: cost optimization
tradeoffs for a latency-critical chat workload vs. a batch analytics
pipeline" subsection added to
docs/domain-5-security-compliance-governance.md.

The gap this covers: Domain 5 Section 1's cost-governance material has
worked examples for capping cost under three threat models and for
sizing Service Quotas for a multi-team Bedrock workload, but neither one
shows how the *SLA target* a workload is held to (a hard per-request
latency SLA vs. a completion-window/throughput target) changes which
cost lever -- on-demand pricing, Provisioned Throughput, batching, or
caching -- actually lowers spend. These tests guard the new worked
example added to close that gap: it must exist as a "####"-level
subsection nested inside the cost-governance subsection, immediately
after the multi-team quota-sizing worked example and before "Security
frameworks...", must not perturb the standalone/nested-"###" worked-
example counts asserted elsewhere, must cover both a latency-critical
real-time workload and a batch-processing workload with the
requirements/configuration/rationale format, must name all four cost
levers (on-demand, Provisioned Throughput, batching, caching) and show
batching being explicitly ruled out for the latency-critical workload,
must include a comparison table contrasting the two workloads, and must
close with an exam tip. It also guards that the existing multi-team
quota-sizing worked example now links forward to this new subsection.

Mirrors the conventions established in
tests/test_domain_5_cost_capping_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_cost_optimization_sla_worked_example.py -v
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
    "#### Worked example: cost optimization tradeoffs for a "
    "latency-critical chat workload vs. a batch analytics pipeline"
)
HEADING_REGEX = (
    r"\n#### Worked example: cost optimization tradeoffs for a "
    r"latency-critical chat workload vs\. a batch analytics pipeline"
)
QUOTA_SIZING_HEADING = (
    "#### Worked example: sizing service quotas for a multi-team "
    "Bedrock workload"
)
SECURITY_FRAMEWORKS_HEADING = (
    "### Security frameworks for AI systems: MITRE ATLAS and OWASP Top "
    "10 for LLM Applications"
)
FORWARD_LINK = (
    "[worked example below]"
    "(#worked-example-cost-optimization-tradeoffs-for-a-latency-critical"
    "-chat-workload-vs-a-batch-analytics-pipeline)"
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


class TestDomain5CostOptimizationSlaWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_after_quota_sizing_and_before_frameworks(
        self,
    ):
        quota_sizing_pos = self.text.index(QUOTA_SIZING_HEADING)
        heading_pos = self.text.index(HEADING)
        frameworks_pos = self.text.index(SECURITY_FRAMEWORKS_HEADING)
        self.assertLess(quota_sizing_pos, heading_pos)
        self.assertLess(heading_pos, frameworks_pos)

    def test_does_not_change_standalone_or_nested_3_worked_example_counts(
        self,
    ):
        # The new subsection is a level-4 heading nested inside the
        # existing cost-governance subsection, not a new standalone
        # "## Worked example" section and not a new "### Worked example"
        # subsection, so it must not perturb the counts asserted in
        # tests/test_domain_5_study_guide.py or
        # tests/test_documentation_structure.py.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 2)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 0)

    def test_covers_both_workloads(self):
        for expected in [
            "Workload 1: a latency-critical real-time chat assistant.",
            "Workload 2: a batch-processing analytics pipeline.",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_each_workload_has_requirements_configuration_and_rationale_labels(
        self,
    ):
        for expected in ["*Requirements:*", "*Configuration:*", "*Why this combination:*"]:
            with self.subTest(expected=expected):
                self.assertEqual(self.section.count(expected), 2)

    def test_covers_all_four_cost_levers(self):
        for expected in [
            "Provisioned Throughput",
            "on-demand",
            "batch",
            "cache",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_batching_is_explicitly_ruled_out_for_the_latency_critical_workload(
        self,
    ):
        self.assertIn("**Batching explicitly ruled out.**", self.section)

    def test_batch_inference_is_the_lever_for_the_batch_workload(self):
        self.assertIn("Bedrock batch inference", self.section)

    def test_has_a_comparison_table_contrasting_both_workloads(self):
        self.assertIn("**Comparison table:**", self.section)
        table_section = self.section[self.section.index("**Comparison table:**"):]
        self.assertRegex(table_section, r"\|\s*-{2,}\s*\|")
        self.assertIn("Real-time chat (hard SLA)", table_section)
        self.assertIn("Batch analytics (completion window)", table_section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_quota_sizing_example_links_forward_to_the_new_worked_example(
        self,
    ):
        quota_sizing_section = _section(
            self.text,
            re.escape(QUOTA_SIZING_HEADING),
            r"\n#{1,4} ",
        )
        self.assertIn(FORWARD_LINK, quota_sizing_section)


if __name__ == "__main__":
    unittest.main()
