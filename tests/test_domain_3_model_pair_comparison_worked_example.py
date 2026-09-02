"""Structural validation for the "Worked example: two concrete model-pair
comparisons" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3, Section 1's "Context window vs. cost and
latency: comparing model tiers" subsection ranks whole model *families*
against each other qualitatively (Lowest/Moderate/Highest cost and
latency), and the domain's other worked examples turn context window and
monthly cost into concrete numbers -- but nothing in the domain walked
through a concrete, *named* model-pair trade-off decision the way a real
exam scenario poses it (e.g., "Claude Sonnet or Amazon Nova Premier for
this task?"). These tests guard the worked example added to close that
gap: it must exist as a subsection nested inside the "Context window vs.
cost and latency" subsection (before the section 1 mini-quiz), and contain
two short worked examples -- a cost-vs-capability comparison (Claude
Sonnet vs. Amazon Nova Premier) and a latency-across-tiers comparison
(Claude Haiku vs. Claude Opus) -- each following the scenario / decision
factors / resolution format used by the domain's other worked examples,
plus a closing exam tip.

Mirrors the conventions established in
tests/test_domain_3_monthly_cost_worked_example.py and
tests/test_domain_3_context_window_budget_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_model_pair_comparison_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

HEADING = "#### Worked example: two concrete model-pair comparisons"
HEADING_REGEX = r"\n#### Worked example: two concrete model-pair comparisons"

CONTEXT_WINDOW_SECTION_HEADING_REGEX = (
    r"\n### Context window vs\. cost and latency: comparing model tiers"
)
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of FM application design "
    "considerations"
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


class TestDomain3ModelPairComparisonWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_inside_the_context_window_subsection(self):
        context_window_pos = self.text.index(
            "### Context window vs. cost and latency: comparing model tiers"
        )
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(MINI_QUIZ_HEADING)
        self.assertLess(context_window_pos, heading_pos)
        self.assertLess(heading_pos, mini_quiz_pos)

    def test_does_not_change_the_standalone_worked_example_count(self):
        # The new subsection is a level-4 heading nested inside Section 1,
        # not a new standalone "## Worked example" section, so it must not
        # perturb the counts asserted in
        # tests/test_documentation_structure.py.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 7)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 1)

    def test_example_one_covers_cost_vs_capability_for_a_named_model_pair(self):
        for expected in [
            "Example 1",
            "Claude Sonnet",
            "Amazon Nova Premier",
            "cost vs. capability",
            "*Scenario:*",
            "*Decision factors:*",
            "*Resolution:*",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_example_two_covers_latency_for_a_named_model_pair(self):
        for expected in [
            "Example 2",
            "Claude Haiku",
            "Claude Opus",
            "latency",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_example_two_gives_a_concrete_resolution_per_feature(self):
        self.assertRegex(
            self.section,
            r"(?i)Haiku for the latency-sensitive chat\s+widget",
        )
        self.assertRegex(
            self.section,
            r"(?i)Opus for the latency-insensitive batch\s+job",
        )

    def test_cross_links_to_the_multi_constraint_worked_example(self):
        self.assertIn(
            "[multi-constraint worked example]"
            "(#worked-example-selecting-a-foundation-model-under-multiple-competing-constraints)",
            self.section,
        )

    def test_worked_example_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.section)


if __name__ == "__main__":
    unittest.main()
