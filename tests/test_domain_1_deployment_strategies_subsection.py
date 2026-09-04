"""Structural validation for the "Production deployment strategies and
model versioning" subsection added to
docs/domain-1-fundamentals-of-ai-and-ml.md.

The gap this covers: cross-domain scenario questions in
docs/cross-domain-scenario-questions.md test production rollout and model
governance decisions (staged rollout patterns, and SageMaker Model
Registry usage for version management), but Domain 1 previously only
covered a classical-ML-lifecycle worked example that stopped at
"Deployment: expose the trained model for inference" -- with no
systematic coverage of canary/blue-green/A-B-testing/shadow rollout
patterns or how SageMaker Model Registry tracks and promotes model
versions. These tests guard the new subsection added to close that gap:
it must exist inside "## 2. The ML development lifecycle", sit before
that section's mini-quiz, be linked from the table of contents, cover all
four staged-rollout patterns plus SageMaker Model Registry, and cross-link
to Domain 5 -- without adding any new numbered section or mini-quiz block
(this repo's structural tests assert exact counts for both).

Mirrors the conventions established in
tests/test_domain_3_cost_governance_subsection.py.

Run with:
    python3 -m unittest tests/test_domain_1_deployment_strategies_subsection.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-1-fundamentals-of-ai-and-ml.md"
)

HEADING = "### Production deployment strategies and model versioning"
TOC_LINK = (
    "[Production deployment strategies and model versioning]"
    "(#production-deployment-strategies-and-model-versioning)"
)
CROSS_LINK = (
    "domain-5-security-compliance-governance.md#1-securing-ai-systems"
)

REQUIRED_ROLLOUT_PATTERNS = [
    "Canary deployment",
    "Blue/green deployment",
    "A/B testing",
    "Shadow deployment",
]


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain1DeploymentStrategiesSubsection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.subsection = _section(
            cls.text,
            re.escape(HEADING),
            r"\n#{1,3} ",
        )

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_sits_inside_section_2_before_its_mini_quiz(self):
        section_2 = _section(
            self.text,
            r"\n## 2\. The ML development lifecycle",
            r"\n## 3\. ",
        )
        heading_pos = section_2.index(HEADING)
        quiz_pos = section_2.index(
            "#### Mini-quiz: Test your understanding of the ML lifecycle"
        )
        self.assertLess(heading_pos, quiz_pos)

    def test_covers_all_four_staged_rollout_patterns(self):
        for expected in REQUIRED_ROLLOUT_PATTERNS:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_covers_sagemaker_model_registry(self):
        self.assertIn("SageMaker Model Registry", self.subsection)
        self.assertIn("model package groups", self.subsection)
        self.assertRegex(self.subsection, r"(?i)approve or reject")

    def test_cross_links_to_domain_5(self):
        self.assertIn(CROSS_LINK, self.subsection)

    def test_has_an_aws_example_and_exam_tip(self):
        self.assertIn("**AWS example:**", self.subsection)
        self.assertIn("Exam tip:", self.subsection)

    def test_distinguishes_patterns_from_model_monitor_and_model_cards(self):
        # The exam tip should explicitly disambiguate Model Registry from
        # two commonly-confused services, since that's the crux of the
        # governance scenario questions this subsection targets.
        self.assertIn("Model Monitor", self.subsection)
        self.assertIn("Model Cards", self.subsection)

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-7]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            7,
            "Domain 1 must still have exactly 7 numbered sections",
        )
        section_2 = _section(
            self.text,
            r"\n## 2\. The ML development lifecycle",
            r"\n## 3\. ",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_2)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 2 must still contain exactly one mini-quiz heading",
        )


if __name__ == "__main__":
    unittest.main()
