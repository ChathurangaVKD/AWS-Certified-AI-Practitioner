"""Structural validation for the "Worked example: is a 2-point BLEU/ROUGE
improvement statistically significant?" subsection added to Section 7
("Evaluating foundation model performance") of
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3, Section 7 described "automatic metrics" and
"human evaluation" as evaluation approaches but gave no guidance on
statistical significance, A/B test design, sample size, or confidence
intervals -- so a learner could name the right evaluation approach without
being able to judge whether an observed improvement (e.g., a 2-point
BLEU/ROUGE gain) is actually real or just sampling noise, or how many human
raters are needed for a reliable consensus. These tests guard the worked
example added to close that gap: it must exist, be linked from the table of
contents, live inside Section 7, walk through a paired-difference confidence
interval calculation that flips from significant to not-significant as
sample size shrinks, give a minimum sample-size formula/worked number, cover
human-rater consensus guidance (multiple raters + an inter-rater agreement
measure), and carry an exam tip like every other worked example in this
domain guide.

Mirrors the conventions established in
tests/test_domain_3_rag_troubleshooting_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_3_statistical_significance_worked_example.py -v
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
    "### Worked example: is a 2-point BLEU/ROUGE improvement "
    "statistically significant?"
)
HEADING_REGEX = (
    r"\n### Worked example: is a 2-point BLEU/ROUGE improvement "
    r"statistically significant\?"
)
TOC_LINK = (
    "[Worked example: is a 2-point BLEU/ROUGE improvement statistically "
    "significant?]"
    "(#worked-example-is-a-2-point-bleurouge-improvement-statistically-significant)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,3} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading of the same or higher level, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3StatisticalSignificanceWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_section_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_worked_example_lives_inside_section_7(self):
        section_7_pos = self.text.index(
            "## 7. Evaluating foundation model performance"
        )
        section_8_pos = self.text.index(
            "## 8. AWS infrastructure for generative AI workloads"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(section_7_pos, heading_pos)
        self.assertLess(heading_pos, section_8_pos)

    def test_uses_paired_difference_comparison(self):
        self.assertRegex(
            self.section,
            r"(?i)paired",
            "expected the worked example to compare paired per-prompt "
            "differences rather than two independent averages",
        )

    def test_confidence_interval_worked_calculation(self):
        # The core worked numbers: n=200, mean diff 2.1, std dev 9.4,
        # and the resulting 95% CI that excludes zero.
        for expected in ["200", "2.1", "9.4", "95%", "[0.80, 3.40]"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_explains_ci_crossing_zero_means_not_significant(self):
        self.assertRegex(
            self.section,
            r"(?i)span(?:s)? zero|cross(?:es)? zero",
            "expected an explanation that a CI spanning/crossing zero "
            "means the result is not statistically significant",
        )
        # The small-sample (n=20) example should demonstrate the flip.
        self.assertIn("20", self.section)
        self.assertIn("[−2.02, 6.22]", self.section)

    def test_gives_a_minimum_sample_size_formula_and_worked_number(self):
        self.assertRegex(
            self.section,
            r"(?i)sample size",
            "expected guidance on minimum sample size",
        )
        self.assertIn("174", self.section)

    def test_covers_human_rater_consensus_guidance(self):
        self.assertRegex(
            self.section,
            r"(?i)3–5|3-5|multiple raters",
            "expected guidance on using multiple human raters per output",
        )
        for term in ["Cohen's kappa", "Krippendorff's alpha"]:
            with self.subTest(term=term):
                self.assertIn(
                    term,
                    self.section,
                    f"expected inter-rater agreement measure {term!r}",
                )

    def test_has_an_aws_example_referencing_bedrock_evaluation(self):
        self.assertIn("**AWS example:**", self.section)
        self.assertRegex(self.section, r"(?i)bedrock")

    def test_worked_example_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.section)


if __name__ == "__main__":
    unittest.main()
