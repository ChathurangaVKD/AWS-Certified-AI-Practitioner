"""Structural validation for the "Inference failures and recovery
strategies" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3, Section 8 covers the AWS infrastructure
behind real-time and batch inference (SageMaker, Trainium, Inferentia) and
the decision tree for choosing between real-time and batch deployment, but
never shows either pattern actually *failing* in production -- even though
AIF-C01 scenario questions frequently describe an endpoint or job that
worked fine under normal load and only breaks once traffic or payload size
changes. These tests guard the dedicated subsection added to close that
gap: it must exist, be linked from the table of contents, sit after
Section 8, and cover two worked scenarios -- a SageMaker real-time
endpoint that can't scale fast enough for a traffic spike, and a batch
transform job that times out on oversized payloads -- each with a
symptom, a diagnosis, a remediation, and an exam tip, plus a summary table
tying both scenarios together.

Mirrors the conventions established in
tests/test_domain_3_rag_troubleshooting_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_inference_failures_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

HEADING = "## Inference failures and recovery strategies"
HEADING_REGEX = r"\n## Inference failures and recovery strategies"


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


class TestDomain3InferenceFailuresWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_section_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents")
        self.assertIn(
            "[Inference failures and recovery strategies]"
            "(#inference-failures-and-recovery-strategies)",
            toc,
        )

    def test_section_appears_after_the_infrastructure_section(self):
        # The failure scenarios build on the SageMaker/infrastructure
        # concepts from Section 8, so it should be positioned after that
        # section in reading order.
        infra_section_pos = self.text.index(
            "## 8. AWS infrastructure for generative AI workloads"
        )
        failures_pos = self.text.index(HEADING)
        self.assertLess(infra_section_pos, failures_pos)

    def test_section_cross_references_the_infrastructure_section(self):
        self.assertIn(
            "#8-aws-infrastructure-for-generative-ai-workloads",
            self.section,
        )

    def test_has_two_distinct_scenario_subsections(self):
        headings = re.findall(r"^### (.+)$", self.section, re.M)
        scenario_headings = [h for h in headings if h.lower().startswith("scenario")]
        self.assertEqual(
            len(scenario_headings),
            2,
            f"expected exactly 2 scenario subsections, found {headings!r}",
        )

    def test_every_scenario_has_symptom_diagnosis_remediation_and_exam_tip(self):
        scenario_blocks = re.split(r"\n(?=### )", self.section.strip())
        scenario_blocks = [
            b
            for b in scenario_blocks
            if b.startswith("### ") and b.splitlines()[0].lower().startswith("### scenario")
        ]
        self.assertEqual(len(scenario_blocks), 2)
        for block in scenario_blocks:
            heading = block.splitlines()[0]
            with self.subTest(section=heading):
                self.assertIn("**Scenario:**", block)
                self.assertIn("**Symptom:**", block)
                self.assertIn("**Diagnosis.**", block)
                self.assertIn("**Remediation.**", block)
                self.assertIn("Exam tip:", block)

    def test_covers_realtime_endpoint_autoscaling_lag_failure_mode(self):
        self.assertRegex(
            self.section,
            r"(?i)SageMaker real-time endpoint",
            "expected a scenario about a SageMaker real-time endpoint",
        )
        self.assertRegex(
            self.section,
            r"(?i)traffic spike",
            "expected the scenario to describe a sudden traffic spike",
        )
        self.assertRegex(
            self.section,
            r"(?i)auto.?scaling",
            "expected the diagnosis to discuss auto scaling reacting too "
            "slowly to the spike",
        )

    def test_names_autoscaling_policy_tuning_and_provisioned_concurrency_as_fixes(self):
        for term in [
            "scale-out cooldown",
            "minimum instance count",
            "provisioned concurrency",
        ]:
            with self.subTest(term=term):
                self.assertRegex(
                    self.section,
                    re.compile(re.escape(term), re.I),
                    f"worked example should name {term!r} as a remediation "
                    "for the endpoint-scaling failure mode",
                )

    def test_covers_batch_transform_timeout_failure_mode(self):
        self.assertRegex(
            self.section,
            r"(?i)Batch Transform",
            "expected a scenario about a SageMaker Batch Transform job",
        )
        self.assertRegex(
            self.section,
            r"(?i)large(?:r)? (?:documents|payloads|records)",
            "expected the scenario to describe unusually large payloads",
        )
        self.assertIn("MaxPayloadInMB", self.section)
        self.assertIn("InvocationsTimeoutInSeconds", self.section)

    def test_names_batch_size_and_timeout_config_as_fixes(self):
        for term in ["SingleRecord", "MaxConcurrentTransforms"]:
            with self.subTest(term=term):
                self.assertIn(
                    term,
                    self.section,
                    f"worked example should name {term!r} as part of the "
                    "batch-timeout remediation",
                )

    def test_has_a_symptom_to_fix_summary_table(self):
        self.assertIn(
            "### Summary: matching the inference failure to the fix",
            self.section,
        )
        table = self.section[
            self.section.index(
                "### Summary: matching the inference failure to the fix"
            ):
        ]
        self.assertRegex(table, r"\|\s*-{2,}\s*\|")
        for column in ["Deployment pattern", "Symptom", "Root cause", "Fix"]:
            with self.subTest(column=column):
                self.assertIn(column, table)

    def test_section_has_no_worked_example_heading_drift(self):
        # This subsection is deliberately titled "Inference failures and
        # recovery strategies" rather than "Worked example: ..." so it does
        # not perturb the pinned worked-example heading counts asserted in
        # tests/test_documentation_structure.py. Guard that convention.
        self.assertNotRegex(self.section, r"^#{2,4} Worked examples?:", re.M)
        self.assertNotRegex(HEADING, r"^## Worked example:")


if __name__ == "__main__":
    unittest.main()
