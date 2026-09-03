"""Structural validation for the "Worked example: applying differential
privacy to a healthcare model-training pipeline" subsection added to
docs/domain-5-security-compliance-governance.md.

The gap this covers: the "Common security threats to AI systems and how
to mitigate them" subsection documents model inversion/extraction
attacks -- an attacker with only ordinary query access against a deployed
model inferring whether a specific individual's record was in its
training data -- but never explained differential privacy (DP), the
training-time technique that directly mitigates that threat. No file in
the repo mentioned "differential privacy" before this change. This new
worked example must exist as a "####"-level subsection nested inside the
"Common security threats..." subsection (after its exam tip, before that
subsection's mini-quiz), must not perturb the standalone/nested
worked-example counts asserted elsewhere, must cover the healthcare
scenario and core DP vocabulary (privacy budget/epsilon, DP-SGD), must
explicitly distinguish itself from the encryption-at-rest control covered
earlier in the file, must close with an exam tip, and must fall within
the requested ~250-350 word range. It also guards that the existing
"Common security threats..." exam tip now links forward to this new
subsection.

Mirrors the conventions established in
tests/test_domain_5_watermarking_worked_example.py and
tests/test_domain_5_cost_capping_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_differential_privacy_worked_example.py -v
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
    "#### Worked example: applying differential privacy to a healthcare "
    "model-training pipeline"
)
HEADING_REGEX = (
    r"\n#### Worked example: applying differential privacy to a "
    r"healthcare model-training pipeline"
)
COMMON_THREATS_HEADING = (
    "### Common security threats to AI systems and how to mitigate them"
)
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of security and responsible "
    "AI intersections"
)
FORWARD_LINK = (
    "[worked example "
    "below](#worked-example-applying-differential-privacy-to-a-healthcare-"
    "model-training-pipeline)"
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


class TestDomain5DifferentialPrivacyWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_between_common_threats_and_mini_quiz(
        self,
    ):
        common_threats_pos = self.text.index(COMMON_THREATS_HEADING)
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(MINI_QUIZ_HEADING)
        self.assertLess(common_threats_pos, heading_pos)
        self.assertLess(heading_pos, mini_quiz_pos)

    def test_does_not_change_standalone_or_level_3_worked_example_counts(
        self,
    ):
        # The new subsection is a level-4 heading nested inside the
        # existing "Common security threats..." subsection, not a new
        # standalone "## Worked example" section and not a new
        # "### Worked example" subsection, so it must not perturb the
        # counts asserted in tests/test_domain_5_study_guide.py or
        # tests/test_documentation_structure.py.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 2)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 0)

    def test_is_the_fifth_level_4_nested_worked_example_in_domain_5(self):
        # Pre-existing level-4 nested worked examples: "capping cost under
        # three different threat models", "sizing service quotas for a
        # multi-team Bedrock workload", "shared responsibility for a
        # SageMaker-to-Bedrock fine-tuning pipeline", and "tracing
        # provenance through a Titan Image Generator watermarking
        # pipeline". This one is the fifth.
        nested_level_4 = re.findall(r"^#### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_4), 5)

    def test_covers_the_healthcare_scenario_and_dp_vocabulary(self):
        for expected in [
            "Meridian Health Alliance",
            "Amazon SageMaker",
            "Differential privacy (DP)",
            "DP-SGD",
            "privacy budget",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_labeled_parts(self):
        for expected in [
            "**The scenario.**",
            "**What it protects against.**",
            "**The accuracy/privacy trade-off.**",
            "**How this differs from encryption at rest.**",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_distinguishes_from_encryption_at_rest(self):
        self.assertIn("KMS", self.section)
        self.assertIn("(#data-encryption-at-rest-and-in-transit)", self.section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_word_count_is_within_requested_range(self):
        body = self.section
        # Strip a leading heading line if present in the extracted
        # section (the section starts right after the heading match, so
        # this is a defensive no-op in practice, kept for robustness).
        body = re.sub(r"^#{1,4} .*\n", "", body)
        words = body.split()
        self.assertGreaterEqual(len(words), 250)
        self.assertLessEqual(len(words), 350)

    def test_common_threats_exam_tip_links_forward_to_the_worked_example(
        self,
    ):
        common_threats_section = _section(
            self.text,
            re.escape(COMMON_THREATS_HEADING),
            r"\n#{1,3} ",
        )
        self.assertIn(FORWARD_LINK, common_threats_section)


if __name__ == "__main__":
    unittest.main()
