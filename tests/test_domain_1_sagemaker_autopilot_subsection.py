"""Structural validation for the "SageMaker Autopilot vs. manual model
training" subsection added to docs/domain-1-fundamentals-of-ai-and-ml.md.

The gap this covers: Domain 1 Section 2 (the ML development lifecycle)
mentioned SageMaker Autopilot exactly once, in passing, inside the
end-to-end loan-default worked example ("...additionally launches a
SageMaker Autopilot run as a fast baseline to sanity-check that a
hand-built model is worth the extra effort") -- with no explanation
anywhere in the domain of what Autopilot actually does, when to reach for
it instead of manual SageMaker training, or what it can't do. These tests
guard the new subsection added to close that gap: it must exist inside
"## 2. The ML development lifecycle", be linked from the table of
contents, explain that Autopilot automates model selection/tuning,
contrast when to use Autopilot (rapid prototyping, baseline
establishment) against when to train manually (custom algorithms,
domain-specific feature engineering), call out Autopilot's fixed
feature-engineering and lack of custom-loss-function support as
limitations, and include an exam tip -- without adding a new numbered
section.

Mirrors the conventions established in
tests/test_domain_1_ensemble_methods_subsection.py.

Run with:
    python3 -m unittest tests/test_domain_1_sagemaker_autopilot_subsection.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-1-fundamentals-of-ai-and-ml.md"
)

HEADING = "### SageMaker Autopilot vs. manual model training"
TOC_LINK = (
    "[SageMaker Autopilot vs. manual model training]"
    "(#sagemaker-autopilot-vs-manual-model-training)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain1SageMakerAutopilotSubsection(unittest.TestCase):
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

    def test_sits_inside_section_2_before_the_training_cost_worked_example(self):
        section_2 = _section(
            self.text,
            r"\n## 2\. The ML development lifecycle",
            r"\n## 3\. Types of learning",
        )
        heading_pos = section_2.index(HEADING)
        worked_example_pos = section_2.index(
            "### Worked example: estimating training cost for the "
            "loan-default predictor"
        )
        self.assertLess(
            heading_pos,
            worked_example_pos,
            "Autopilot subsection should come before the training-cost "
            "worked example, right after the core lifecycle explanation",
        )

    def test_explains_what_autopilot_does(self):
        self.assertRegex(
            self.subsection,
            r"(?i)automat",
            "subsection should explain that Autopilot automates the "
            "modeling process",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)feature engineering",
            "subsection should mention Autopilot's automatic feature "
            "engineering",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)hyperparameter",
            "subsection should mention Autopilot tunes hyperparameters "
            "as part of model selection",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)leaderboard",
            "subsection should mention the candidate-model leaderboard "
            "Autopilot produces",
        )

    def test_contrasts_when_to_use_autopilot_vs_manual_training(self):
        self.assertRegex(
            self.subsection,
            r"(?i)baseline",
            "subsection should mention establishing a baseline as an "
            "Autopilot use case",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)prototyp",
            "subsection should mention rapid prototyping as an Autopilot "
            "use case",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)custom\s+algorithm",
            "subsection should call out custom algorithms as a reason "
            "to train manually instead of using Autopilot",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)domain-specific feature engineering",
            "subsection should call out domain-specific feature "
            "engineering as a reason to train manually instead of using "
            "Autopilot",
        )

    def test_states_autopilots_limitations(self):
        self.assertRegex(
            self.subsection,
            r"(?i)fixed",
            "subsection should describe Autopilot's feature-engineering "
            "steps as fixed/automatic, not customizable",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)custom loss function",
            "subsection should state that Autopilot does not support "
            "custom loss functions",
        )

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_no_new_numbered_section_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-7]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            7,
            "Domain 1 must still have exactly 7 numbered sections",
        )

    def test_does_not_introduce_a_new_worked_example_heading(self):
        # DOCUMENTATION_STRUCTURE.md's sync tests pin an exact per-domain
        # count of "##"/"###"/"####"-level "Worked example:" headings.
        # This subsection deliberately has no worked-example heading of
        # its own, so it must not add to that count.
        heading_worked_examples = re.findall(
            r"(?m)^#{2,4} Worked examples?:", self.text
        )
        self.assertEqual(
            len(heading_worked_examples),
            3,
            "Domain 1 must still have exactly 3 heading-level 'Worked "
            "example' sections",
        )


if __name__ == "__main__":
    unittest.main()
