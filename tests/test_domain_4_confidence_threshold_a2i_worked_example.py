"""Structural validation for the confidence-threshold / Amazon A2I worked
example nested inside Section 3 of
docs/domain-4-guidelines-for-responsible-ai.md.

The gap this covers: cross-domain scenario question 22
(docs/cross-domain-scenario-questions.md) tests routing a classical
model's low-confidence predictions to a human reviewer -- combining
Domain 1, Section 6 (classification thresholds and AUC-ROC) with Domain
4, Section 3's one-sentence mention of Amazon A2I -- but no worked
example previously connected the two end to end. This test file guards
the new "### Worked example: routing low-confidence predictions to human
review with Amazon A2I" subsection, nested inside Section 3 right after
its exam tip and before that section's mini-quiz, mirroring the nested
"###"/"####" worked-example convention used elsewhere (e.g.
tests/test_domain_5_cost_capping_worked_example.py).

Run with:
    python3 -m unittest tests/test_domain_4_confidence_threshold_a2i_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-4-guidelines-for-responsible-ai.md"
)

WORKED_EXAMPLE_HEADING = (
    "### Worked example: routing low-confidence predictions to human "
    "review with Amazon A2I"
)
SECTION_3_HEADING = "## 3. AWS tools for responsible AI"
SECTION_4_HEADING = "## 4. Legal and ethical considerations"
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of AWS tools for "
    "responsible AI"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading, end_heading_regex=r"\n## "):
    """Return the text between an exact start_heading string and the next
    matching heading, or end of file."""
    start = text.index(start_heading)
    rest = text[start + len(start_heading):]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain4ConfidenceThresholdA2IWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        # Bounded by the mini-quiz heading that follows it, not just the
        # next "## " top-level heading -- the worked example sits *before*
        # Section 3's mini-quiz, so without this explicit bound the
        # section would swallow the mini-quiz too (a "#### " heading isn't
        # matched by the default "\n## " boundary).
        cls.section = _section(
            cls.text, WORKED_EXAMPLE_HEADING, re.escape("\n" + MINI_QUIZ_HEADING)
        )
        # Markdown line-wraps mid-phrase (e.g. "worker task\ntemplate"), so
        # phrase-level assertions match against whitespace-normalized text
        # rather than the raw, line-wrapped section.
        cls.normalized = re.sub(r"\s+", " ", cls.section)

    def test_heading_exists(self):
        self.assertIn(WORKED_EXAMPLE_HEADING, self.text)

    def test_nested_as_h3_not_a_standalone_h2(self):
        self.assertTrue(WORKED_EXAMPLE_HEADING.startswith("### "))
        self.assertNotIn("#" + WORKED_EXAMPLE_HEADING, self.text)

    def test_appears_inside_section_3_before_the_mini_quiz(self):
        section3_idx = self.text.index(SECTION_3_HEADING)
        worked_idx = self.text.index(WORKED_EXAMPLE_HEADING)
        mini_quiz_idx = self.text.index(MINI_QUIZ_HEADING)
        section4_idx = self.text.index(SECTION_4_HEADING)
        self.assertLess(section3_idx, worked_idx)
        self.assertLess(worked_idx, mini_quiz_idx)
        self.assertLess(mini_quiz_idx, section4_idx)

    def test_not_listed_as_a_standalone_toc_entry(self):
        # Nested "###" worked examples aren't given their own top-level
        # table-of-contents bullet elsewhere in this doc series (mirrors
        # the Domain 5 cost-capping and shared-responsibility
        # subsections), so this one shouldn't be either.
        toc = _section(self.text, "## Table of contents", r"\n## Domain overview")
        self.assertNotIn("Worked example: routing low-confidence", toc)

    def test_has_scenario_and_exam_tip(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_cross_references_domain_1_model_evaluation_section(self):
        self.assertIn(
            "domain-1-fundamentals-of-ai-and-ml.md#6-model-evaluation-basics",
            self.normalized,
        )

    def test_names_a_healthcare_scenario(self):
        self.assertRegex(
            self.normalized,
            r"(?i)hospital|clinician|patient|clinical",
            "expected a healthcare human-in-the-loop scenario",
        )

    def test_includes_concrete_threshold_and_metric_values(self):
        for term in ["AUC-ROC", "0.91", "0.35", "recall", "precision"]:
            with self.subTest(term=term):
                self.assertIn(term, self.normalized)

    def test_explains_threshold_selection_reasoning(self):
        # More than one candidate threshold should be discussed, not just
        # the one that was ultimately chosen.
        thresholds = re.findall(r"0\.\d\d", self.normalized)
        self.assertGreaterEqual(
            len(set(thresholds)),
            3,
            "expected multiple candidate thresholds to be compared before "
            "settling on one",
        )

    def test_describes_a2i_integration_steps(self):
        for term in [
            "Amazon A2I",
            "StartHumanLoop",
            "worker task template",
            "flow definition",
            "private workforce",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.normalized)

    def test_explains_why_a_private_workforce_is_required(self):
        self.assertRegex(
            self.normalized,
            r"(?i)PHI|protected health information",
            "expected the example to explain the private-workforce "
            "requirement in terms of PHI exposure",
        )

    def test_no_autonomous_clinical_action_before_human_review(self):
        self.assertRegex(
            self.normalized,
            r"(?i)never.{0,40}(autonomous|autonomously)|autonomous.{0,40}action",
            "expected the example to state the model must never take a "
            "clinical action autonomously",
        )

    def test_documents_the_decision_in_a_model_card(self):
        self.assertIn("Model Card", self.normalized)

    def test_mentions_ongoing_monitoring(self):
        self.assertIn("SageMaker Model Monitor", self.normalized)

    def test_has_at_least_five_numbered_steps(self):
        steps = re.findall(r"^\d+\.\s", self.section, re.M)
        self.assertGreaterEqual(
            len(steps),
            5,
            "worked example should walk through at least five numbered steps",
        )

    def test_word_count_within_expected_range(self):
        words = re.findall(r"\w+", self.section)
        self.assertGreaterEqual(len(words), 400)
        self.assertLessEqual(len(words), 900)


if __name__ == "__main__":
    unittest.main()
