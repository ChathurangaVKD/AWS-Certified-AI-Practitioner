"""Structural validation for the "Runtime decision tree: selecting a
fallback model when the primary is unavailable, rate-limited, or too
costly" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3's "Multi-model routing and fallback
strategies" subsection already had a decision flowchart for whether
routing/fallback belongs in the design at all (design-time), plus a
worked example and implementation patterns, but had no diagram for the
runtime decision every request actually makes once a fallback chain
exists: is the primary model healthy/available, is it rate-limited, does
its cost fit the budget, and if not, which of the 2-3 configured
fallback candidates should handle the request instead. This test guards
the new subsection that closes that gap: it must exist nested inside the
"Multi-model routing and fallback strategies" subsection, immediately
after the design-time flowchart's comparison table and exam tip and
before the latency-sensitivity worked example, contain a Mermaid
flowchart with an availability check, a rate-limit check, a cost check,
and a choice among more than one fallback candidate, and be linked from
the table of contents.

Mirrors the conventions established in
tests/test_domain_3_multi_model_routing_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_fallback_routing_decision_tree.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

PARENT_SECTION_HEADING = (
    "### Multi-model routing and fallback strategies: routing requests to "
    "the right model at request time"
)
DESIGN_TIME_FLOWCHART_HEADING = (
    "#### Decision flowchart: is multi-model routing worth the added "
    "complexity?"
)
RUNTIME_TREE_HEADING = (
    "#### Runtime decision tree: selecting a fallback model when the "
    "primary is unavailable, rate-limited, or too costly"
)
WORKED_EXAMPLE_HEADING = (
    "#### Worked example: routing a dashboard-and-batch analytics feature "
    "by latency sensitivity"
)
TOC_LINK = (
    "[Runtime decision tree: selecting a fallback model when the primary "
    "is unavailable, rate-limited, or too costly]"
    "(#runtime-decision-tree-selecting-a-fallback-model-when-the-primary-"
    "is-unavailable-rate-limited-or-too-costly)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


class TestDomain3FallbackRoutingDecisionTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_heading_exists(self):
        self.assertIn(RUNTIME_TREE_HEADING, self.text)

    def test_toc_links_to_the_new_subsection(self):
        toc_start = self.text.index("## Table of contents")
        toc_end = self.text.index("## Domain overview")
        toc = self.text[toc_start:toc_end]
        self.assertIn(TOC_LINK, toc)

    def test_is_positioned_between_the_design_time_flowchart_and_the_worked_example(
        self,
    ):
        parent_pos = self.text.index(PARENT_SECTION_HEADING)
        design_flowchart_pos = self.text.index(DESIGN_TIME_FLOWCHART_HEADING)
        runtime_tree_pos = self.text.index(RUNTIME_TREE_HEADING)
        worked_example_pos = self.text.index(WORKED_EXAMPLE_HEADING)
        self.assertLess(parent_pos, design_flowchart_pos)
        self.assertLess(design_flowchart_pos, runtime_tree_pos)
        self.assertLess(runtime_tree_pos, worked_example_pos)

    def test_has_a_mermaid_flowchart_with_availability_rate_limit_and_cost_checks(
        self,
    ):
        section = self.text[
            self.text.index(RUNTIME_TREE_HEADING) : self.text.index(
                WORKED_EXAMPLE_HEADING
            )
        ]
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertEqual(
            len(fences),
            1,
            "expected exactly one Mermaid flowchart in the runtime "
            "decision tree subsection",
        )
        flowchart = fences[0]
        self.assertRegex(flowchart, r"flowchart\s+\w+|graph\s+\w+")

        # Availability/health check.
        self.assertRegex(
            flowchart,
            r"(?i)healthy and\\nreachable",
            "flowchart should check whether the primary model is healthy "
            "and reachable",
        )
        # Rate-limit check, distinct from the availability check.
        self.assertRegex(
            flowchart,
            r"(?i)rate-limited",
            "flowchart should check whether the primary model is "
            "rate-limited",
        )
        # Cost comparison check.
        self.assertRegex(
            flowchart,
            r"(?i)cost ceiling",
            "flowchart should compare the model's cost against a budget "
            "ceiling",
        )
        self.assertIn("?", flowchart, "flowchart should pose branching decision questions")

    def test_flowchart_selects_among_at_least_two_fallback_candidates(self):
        section = self.text[
            self.text.index(RUNTIME_TREE_HEADING) : self.text.index(
                WORKED_EXAMPLE_HEADING
            )
        ]
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        flowchart = fences[0]
        # At least two distinct fallback candidates must be represented as
        # decision outcomes (2-3 candidates per the task's evidence).
        self.assertIn("FM-2", flowchart)
        self.assertIn("FM-3", flowchart)
        self.assertIn("PRIMARY", section)
        self.assertIn("EXHAUSTED", flowchart)

    def test_explains_the_availability_then_cost_check_ordering(self):
        section = self.text[
            self.text.index(RUNTIME_TREE_HEADING) : self.text.index(
                WORKED_EXAMPLE_HEADING
            )
        ]
        self.assertRegex(
            section,
            r"(?i)availability, then rate limits, then cost",
        )

    def test_has_an_exam_tip(self):
        section = self.text[
            self.text.index(RUNTIME_TREE_HEADING) : self.text.index(
                WORKED_EXAMPLE_HEADING
            )
        ]
        self.assertIn("Exam tip:", section)

    def test_does_not_duplicate_the_design_time_flowchart_outcomes(self):
        # The new runtime tree must be a genuinely different diagram from
        # the pre-existing design-time flowchart, not a near-duplicate --
        # it should not reuse that flowchart's SINGLE MODEL / STRICT
        # ROUTING / BEST-EFFORT ROUTING outcome labels.
        section = self.text[
            self.text.index(RUNTIME_TREE_HEADING) : self.text.index(
                WORKED_EXAMPLE_HEADING
            )
        ]
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        flowchart = fences[0]
        for outcome in ["SINGLE MODEL", "STRICT ROUTING", "BEST-EFFORT ROUTING"]:
            with self.subTest(outcome=outcome):
                self.assertNotIn(outcome, flowchart)


if __name__ == "__main__":
    unittest.main()
