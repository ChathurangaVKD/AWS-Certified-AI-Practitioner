"""Structural validation for the "Inference error handling and resilience
patterns" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: the "Inference failures and recovery strategies"
subsection (see tests/test_domain_3_inference_failures_worked_example.py)
teaches how to *diagnose* a failing real-time endpoint, batch job, or
Bedrock call, but stops short of showing what the calling application
should actually do about a failure once it's happened -- retry loops,
exponential backoff, circuit breakers, or handling cascading failures in a
production inference path. These tests guard the dedicated subsection
added to close that gap: it must exist, be linked from the table of
contents, sit immediately after "Inference failures and recovery
strategies", and cover (1) a comparison of retry strategies (immediate
retry vs. exponential backoff vs. circuit breaker), (2) a decision
flowchart choosing a strategy by error type, (3) a worked example
implementing retries with backoff for a Bedrock API call, and (4)
pseudocode for each of the three patterns.

Mirrors the conventions established in
tests/test_domain_3_inference_failures_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_inference_resilience_patterns.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

HEADING = "## Inference error handling and resilience patterns"
HEADING_REGEX = r"\n## Inference error handling and resilience patterns"


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


class TestDomain3InferenceResiliencePatterns(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_section_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents")
        self.assertIn(
            "[Inference error handling and resilience patterns]"
            "(#inference-error-handling-and-resilience-patterns)",
            toc,
        )

    def test_toc_links_all_four_subsections(self):
        toc = _section(self.text, r"\n## Table of contents")
        for link in [
            "[Retry strategies compared: immediate retry vs. exponential "
            "backoff vs. circuit breaker]"
            "(#retry-strategies-compared-immediate-retry-vs-exponential-backoff-vs-circuit-breaker)",
            "[Decision flowchart: choosing a resilience strategy by error type]"
            "(#decision-flowchart-choosing-a-resilience-strategy-by-error-type)",
            "[Pseudocode reference: immediate retry, exponential backoff, "
            "and circuit breaker]"
            "(#pseudocode-reference-immediate-retry-exponential-backoff-and-circuit-breaker)",
        ]:
            with self.subTest(link=link):
                self.assertIn(link, toc)

    def test_section_appears_immediately_after_inference_failures_section(self):
        # This subsection builds directly on the failure-diagnosis
        # subsection immediately above it, so it should sit right after it
        # (before the next unrelated worked example) rather than somewhere
        # else in the domain guide.
        failures_pos = self.text.index(
            "## Inference failures and recovery strategies"
        )
        resilience_pos = self.text.index(HEADING)
        next_worked_example_pos = self.text.index(
            "## Worked example: implementing RAG for an internal "
            "policy-lookup assistant"
        )
        self.assertLess(failures_pos, resilience_pos)
        self.assertLess(resilience_pos, next_worked_example_pos)

    def test_section_cross_references_the_inference_failures_section(self):
        self.assertIn(
            "#inference-failures-and-recovery-strategies",
            self.section,
        )

    def test_has_retry_strategy_comparison_table(self):
        self.assertIn(
            "### Retry strategies compared: immediate retry vs. "
            "exponential backoff vs. circuit breaker",
            self.section,
        )
        table_section = _section(
            self.section,
            r"### Retry strategies compared",
            end_heading_regex=r"\n### ",
        )
        self.assertRegex(table_section, r"\|\s*-{2,}\s*\|")
        for strategy in [
            "Immediate retry",
            "Exponential backoff (with jitter)",
            "Circuit breaker",
        ]:
            with self.subTest(strategy=strategy):
                self.assertIn(strategy, table_section)
        for column in ["Strategy", "How it behaves", "Best fit", "Risk if misapplied"]:
            with self.subTest(column=column):
                self.assertIn(column, table_section)

    def test_has_decision_flowchart_by_error_type(self):
        self.assertIn(
            "### Decision flowchart: choosing a resilience strategy by "
            "error type",
            self.section,
        )
        flowchart_section = _section(
            self.section,
            r"### Decision flowchart",
            end_heading_regex=r"\n### ",
        )
        self.assertIn("```mermaid", flowchart_section)
        self.assertIn("flowchart TD", flowchart_section)
        # Must distinguish transient (retry) from permanent (fail-fast)
        # errors, and route repeated failures to a circuit breaker.
        for term in [
            "ValidationException",
            "AccessDeniedException",
            "Fail fast",
            "Retry with exponential backoff",
            "circuit breaker",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, flowchart_section)

    def test_has_bedrock_worked_example_with_backoff_code(self):
        heading = (
            "### Worked example: retrying a throttled Bedrock "
            "`InvokeModel` call with exponential backoff and jitter"
        )
        self.assertIn(heading, self.section)
        worked_example_section = _section(
            self.section,
            r"### Worked example: retrying a throttled Bedrock",
            end_heading_regex=r"\n### ",
        )
        self.assertIn("**Scenario:**", worked_example_section)
        self.assertIn("```python", worked_example_section)
        for term in [
            "invoke_model",
            "ThrottlingException",
            "RETRYABLE_ERROR_CODES",
            "MAX_ATTEMPTS",
            "random.uniform",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, worked_example_section)
        # A worked example should include concrete worked numbers, not just
        # prose -- guard the backoff-delay table.
        self.assertRegex(worked_example_section, r"\|\s*-{2,}\s*\|")

    def test_worked_example_heading_uses_worked_example_convention(self):
        # Unlike "Inference failures and recovery strategies" (which
        # deliberately avoided the "Worked example:" heading convention to
        # not perturb the pinned counts in test_documentation_structure.py),
        # this subsection's worked example is a genuine, freestanding
        # numbered worked example and should use the standard heading
        # phrasing so it reads consistently with the rest of the domain
        # guide.
        self.assertRegex(
            self.section, re.compile(r"^#{2,4} Worked examples?:", re.M)
        )

    def test_has_pseudocode_for_all_three_patterns(self):
        heading = (
            "### Pseudocode reference: immediate retry, exponential "
            "backoff, and circuit breaker"
        )
        self.assertIn(heading, self.section)
        pseudocode_section = self.section[self.section.index(heading):]
        code_blocks = re.findall(r"```\n(.*?)```", pseudocode_section, re.S)
        self.assertGreaterEqual(
            len(code_blocks),
            3,
            "expected at least 3 fenced pseudocode blocks (one per "
            "pattern)",
        )
        self.assertIn("call_with_immediate_retry", pseudocode_section)
        self.assertIn("call_with_backoff", pseudocode_section)
        self.assertIn("call_through_breaker", pseudocode_section)
        # The circuit breaker pseudocode must model the closed/open/
        # half-open state machine, not just a bare retry loop.
        for state in ["OPEN", "HALF_OPEN", "CLOSED"]:
            with self.subTest(state=state):
                self.assertIn(state, pseudocode_section)

    def test_subsections_appear_in_order(self):
        order = [
            "### Retry strategies compared",
            "### Decision flowchart: choosing a resilience strategy",
            "### Worked example: retrying a throttled Bedrock",
            "### Pseudocode reference: immediate retry",
        ]
        positions = [self.section.index(marker) for marker in order]
        self.assertEqual(positions, sorted(positions))

    def test_has_exam_tips(self):
        exam_tip_count = len(re.findall(r"Exam tip:", self.section))
        self.assertGreaterEqual(
            exam_tip_count,
            2,
            "expected at least 2 'Exam tip' callouts in the resilience "
            "patterns subsection",
        )

    def test_section_has_no_stray_prevention_or_remediation_labels(self):
        # Sanity check this subsection wasn't accidentally merged with (or
        # copy-pasted from) the "Inference failures and recovery
        # strategies" scenario structure, which uses a different label
        # convention (Symptom/Diagnosis/Remediation/Prevention).
        for label in ["**Symptom:**", "**Diagnosis.**", "**Remediation.**", "**Prevention.**"]:
            with self.subTest(label=label):
                self.assertNotIn(label, self.section)


if __name__ == "__main__":
    unittest.main()
