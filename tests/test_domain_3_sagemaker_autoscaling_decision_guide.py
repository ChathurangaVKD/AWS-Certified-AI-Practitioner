"""Structural validation for the "SageMaker endpoint auto-scaling: a
parameter-tuning decision guide" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Section 8 ("AWS infrastructure for generative AI
workloads") mentions SageMaker, and the "Inference failures and recovery
strategies" Scenario 1 diagnoses a SageMaker real-time endpoint that
scales too slowly for a traffic spike -- but neither ever gave guidance
on how to *choose* target-tracking thresholds, scale-up/scale-down
cooldown periods, or min/max instance counts up front, for different
workload shapes. These tests guard the new subsection's decision tree
for parameter selection by workload type, its worked example configuring
auto-scaling for a real-time inference endpoint with concrete CPU/
invocation targets and cooldown values, and its troubleshooting table for
common scaling problems.

Mirrors the conventions established in
tests/test_domain_3_retrieval_quality_metrics_decision_guide.py.

Run with:
    python3 -m unittest tests/test_domain_3_sagemaker_autoscaling_decision_guide.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

HEADING = "### SageMaker endpoint auto-scaling: a parameter-tuning decision guide"
HEADING_REGEX = re.escape(HEADING)

WORKED_EXAMPLE_HEADING = (
    "#### Worked example: configuring auto-scaling for a real-time "
    "customer-support chatbot endpoint"
)
WORKED_EXAMPLE_HEADING_REGEX = re.escape(WORKED_EXAMPLE_HEADING)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,4} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading (level 1-4), or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3SageMakerAutoscalingDecisionGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)
        cls.worked_example = _section(cls.text, WORKED_EXAMPLE_HEADING_REGEX)

    # -- Placement ---------------------------------------------------

    def test_subsection_exists(self):
        self.assertIn(HEADING, self.text)

    def test_listed_in_table_of_contents(self):
        toc = _section(
            self.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        self.assertIn(
            "[SageMaker endpoint auto-scaling: a parameter-tuning "
            "decision guide]"
            "(#sagemaker-endpoint-auto-scaling-a-parameter-tuning-"
            "decision-guide)",
            toc,
        )
        self.assertIn(
            "[Worked example: configuring auto-scaling for a real-time "
            "customer-support chatbot endpoint]"
            "(#worked-example-configuring-auto-scaling-for-a-real-time-"
            "customer-support-chatbot-endpoint)",
            toc,
        )

    def test_appears_within_section_8_before_its_mini_quiz(self):
        section_8_pos = self.text.index(
            "## 8. AWS infrastructure for generative AI workloads"
        )
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(
            "#### Mini-quiz: Test your understanding of AWS "
            "infrastructure for generative AI workloads"
        )
        inference_failures_pos = self.text.index(
            "## Inference failures and recovery strategies"
        )
        self.assertLess(section_8_pos, heading_pos)
        self.assertLess(heading_pos, mini_quiz_pos)
        self.assertLess(mini_quiz_pos, inference_failures_pos)

    def test_worked_example_appears_inside_the_new_subsection(self):
        heading_pos = self.text.index(HEADING)
        worked_example_pos = self.text.index(WORKED_EXAMPLE_HEADING)
        mini_quiz_pos = self.text.index(
            "#### Mini-quiz: Test your understanding of AWS "
            "infrastructure for generative AI workloads"
        )
        self.assertLess(heading_pos, worked_example_pos)
        self.assertLess(worked_example_pos, mini_quiz_pos)

    def test_scenario_1_cross_references_the_new_decision_guide(self):
        scenario_1 = _section(
            self.text,
            r"### Scenario 1: a SageMaker real-time endpoint that can't "
            r"scale fast enough for a traffic spike",
            r"\n### Scenario 2",
        )
        self.assertIn(
            "#sagemaker-endpoint-auto-scaling-a-parameter-tuning-"
            "decision-guide",
            scenario_1,
        )

    # -- Key parameters ------------------------------------------------

    def test_names_the_five_core_autoscaling_parameters(self):
        for term in [
            "Target metric",
            "Target value",
            "Scale-out (scale-up) cooldown",
            "Scale-in (scale-down) cooldown",
            "MinCapacity",
            "MaxCapacity",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.section)

    def test_mentions_the_predefined_invocations_metric_and_cpu_alternative(self):
        self.assertIn("SageMakerVariantInvocationsPerInstance", self.section)
        self.assertRegex(self.section, r"(?i)CPUUtilization")

    def test_states_the_flapping_vs_slow_reaction_tradeoff(self):
        self.assertRegex(self.section, r"(?i)flap")

    # -- Decision tree ---------------------------------------------------

    def test_decision_tree_present_and_covers_workload_shapes(self):
        self.assertIn("```mermaid", self.section)
        self.assertIn("flowchart TD", self.section)
        for node in ["STEADY", "BURSTY", "SCHEDULED"]:
            with self.subTest(node=node):
                self.assertIn(node, self.section)

    def test_decision_tree_gives_bursty_traffic_a_longer_scale_in_cooldown(self):
        self.assertRegex(
            self.section,
            r"(?i)BURSTY.{0,400}scale-in cooldown \(~600-900s\)",
        )

    def test_has_an_exam_tip_on_the_asymmetric_cooldown_pattern(self):
        self.assertIn("Exam tip:", self.section)
        self.assertRegex(self.section, r"(?i)asymmetry")

    # -- Worked example --------------------------------------------------

    def test_worked_example_section_exists(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.text)

    def test_worked_example_has_a_concrete_configuration_table(self):
        tables = re.findall(
            r"^\|.+\|$\n(?:^\|.+\|$\n?)+", self.worked_example, re.M
        )
        config_tables = [
            t
            for t in tables
            if "Target metric" in t and "Scale-out cooldown" in t
            and "Scale-in cooldown" in t
        ]
        self.assertTrue(
            config_tables,
            "expected a configuration table with target metric and "
            "cooldown rows",
        )
        table = config_tables[0]
        for value in [
            "450 invocations/instance/minute",
            "60 seconds",
            "900 seconds",
        ]:
            with self.subTest(value=value):
                self.assertIn(value, table)

    def test_worked_example_computes_required_instance_count_for_the_spike(self):
        self.assertIn("ceil(4000 / 450) = 9", self.worked_example)

    def test_worked_example_contrasts_with_a_steady_traffic_workload(self):
        self.assertRegex(self.worked_example, r"(?i)steady-traffic workload")

    def test_worked_example_has_a_troubleshooting_table(self):
        self.assertIn("Troubleshooting common SageMaker", self.worked_example)
        tables = re.findall(
            r"^\|.+\|$\n(?:^\|.+\|$\n?)+", self.worked_example, re.M
        )
        troubleshooting_tables = [
            t for t in tables if "Symptom" in t and "Likely cause" in t and "Fix" in t
        ]
        self.assertTrue(
            troubleshooting_tables,
            "expected a troubleshooting table with Symptom/Likely "
            "cause/Fix columns",
        )
        table = troubleshooting_tables[0]
        self.assertGreaterEqual(
            table.count("\n"),
            6,
            "expected the troubleshooting table to list several rows",
        )

    def test_troubleshooting_table_addresses_flapping_with_longer_scale_in_cooldown(self):
        self.assertRegex(
            self.worked_example,
            r"(?i)flapping.{0,400}Lengthen the scale-in \(scale-down\) "
            r"cooldown",
        )

    def test_troubleshooting_table_links_back_to_scenario_1(self):
        self.assertIn(
            "#scenario-1-a-sagemaker-real-time-endpoint-that-cant-scale-"
            "fast-enough-for-a-traffic-spike",
            self.worked_example,
        )


if __name__ == "__main__":
    unittest.main()
