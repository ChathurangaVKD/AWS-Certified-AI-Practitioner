"""Regression tests for the second-query extension to the "Worked example:
computing Recall@k, MRR, MAP, and NDCG on a sample retrieval result set"
subsection in docs/domain-3-applications-of-foundation-models.md.

The gap this covers: the pre-existing worked example computed Recall@k,
MRR, MAP, and NDCG for a *single* query, explicitly noting that "MRR is
the mean of this value over every query" and "a full MAP score averages
this Average-Precision value across every query" -- but never actually
computed that mean, since only one query's numbers existed. A reader could
walk away thinking a single query's reciprocal rank or Average Precision
*is* MRR/MAP, rather than an input to a mean. This adds a second query
against the same corpus and averages both queries' scores together, so the
worked example demonstrates the real definition of MRR and MAP (a mean
over a query set) rather than only gesturing at it.

Mirrors the conventions established in
tests/test_domain_3_retrieval_quality_metrics_decision_guide.py.

Run with:
    python3 -m unittest tests/test_domain_3_retrieval_metrics_two_query_mean_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

WORKED_EXAMPLE_HEADING = (
    "#### Worked example: computing Recall@k, MRR, MAP, and NDCG on a "
    "sample retrieval result set"
)
WORKED_EXAMPLE_HEADING_REGEX = re.escape(WORKED_EXAMPLE_HEADING)

STEP5_HEADING_REGEX = re.escape(
    "**Step 5 — a second query, to turn MRR and MAP into real means:**"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,4} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading (level 1-4), or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end() :]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3RetrievalMetricsTwoQueryMeanWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.worked_example = _section(cls.text, WORKED_EXAMPLE_HEADING_REGEX)

    # -- Placement -----------------------------------------------------

    def test_step_5_appears_inside_the_worked_example(self):
        self.assertRegex(self.worked_example, STEP5_HEADING_REGEX)

    def test_step_5_appears_after_the_first_four_steps(self):
        step4_pos = self.worked_example.index("**Step 4")
        step5_pos = self.worked_example.index("**Step 5")
        self.assertLess(step4_pos, step5_pos)

    def test_worked_example_still_has_no_nested_headings(self):
        # The second-query extension must stay inside the existing
        # worked example as prose/tables, not introduce new markdown
        # headings (which would break the "single self-contained worked
        # example" invariant asserted elsewhere).
        nested_headings = re.findall(r"^#{1,6} .+$", self.worked_example, re.M)
        self.assertEqual(nested_headings, [])

    # -- Second query's per-metric numbers -----------------------------

    def test_second_query_ranked_result_table_present(self):
        self.assertRegex(
            self.worked_example,
            r"What is the process for returning a damaged\s+item\?",
        )
        self.assertIn(
            "Damaged items may be returned within 14 days for a full "
            "refund.",
            self.worked_example,
        )

    def test_second_query_recall_and_reciprocal_rank_are_perfect(self):
        self.assertRegex(
            self.worked_example,
            r"Recall@5\*\* = 3 relevant found . 3 relevant total = \*\*1\.00\*\*",
        )
        self.assertRegex(
            self.worked_example,
            r"Reciprocal rank\*\* = 1 . 1 = \*\*1\.00\*\*",
        )

    def test_second_query_average_precision_is_perfect(self):
        self.assertRegex(
            self.worked_example,
            r"AP = \(1\.000 \+ 1\.000 \+ 1\.000\) . 3 =\s*\n?\s*\*\*1\.00\*\*",
        )
        self.assertRegex(self.worked_example, r"precision@3 = 3/3 = 1\.000")

    def test_second_query_ndcg_is_perfect_because_ranking_is_already_ideal(self):
        self.assertRegex(
            self.worked_example, r"(?i)already in\s*\n?\s*descending order"
        )
        self.assertRegex(
            self.worked_example, r"NDCG@5 = 4\.762 . 4\.762 = \*\*1\.00\*\*"
        )

    # -- The actual mean across the two-query set -----------------------

    def test_two_query_mean_table_present_with_correct_arithmetic(self):
        table_match = re.search(
            r"\| Metric \| Query 1 \| Query 2 \| Mean across the 2-query "
            r"set \|\n(?:\|.+\|\n?)+",
            self.worked_example,
        )
        self.assertIsNotNone(
            table_match, "expected a Query 1 / Query 2 / mean summary table"
        )
        table = table_match.group(0)

        # MRR = mean(1.00, 1.00) = 1.00
        self.assertIn("(1.00 + 1.00) ÷ 2 = **1.00**", table)
        # MAP = mean(0.567, 1.00) = 0.783
        self.assertIn("(0.567 + 1.00) ÷ 2 = **0.783**", table)
        # Recall@5 mean = mean(0.75, 1.00) = 0.875
        self.assertIn("(0.75 + 1.00) ÷ 2 = **0.875**", table)
        # NDCG@5 mean = mean(0.92, 1.00) = 0.96
        self.assertIn("(0.92 + 1.00) ÷ 2 = **0.96**", table)

    def test_takeaway_explains_why_map_stays_below_one(self):
        self.assertIn("0.783", self.worked_example)
        self.assertRegex(
            self.worked_example,
            r"(?i)one\s+weak query with a missed document drags the mean "
            r"down",
        )

    def test_worked_example_still_synthesizes_the_no_single_metric_takeaway(self):
        self.assertRegex(
            self.worked_example,
            r"(?i)no single metric\s+tells the whole story",
        )


if __name__ == "__main__":
    unittest.main()
