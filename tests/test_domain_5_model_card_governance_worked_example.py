"""Structural validation for the "Worked example: filling out a
SageMaker Model Card for governance sign-off" subsection added to
docs/domain-5-security-compliance-governance.md.

The gap this covers: Domain 4 Section 3 and Domain 5 both name Amazon
SageMaker Model Cards repeatedly as the governance artifact that
satisfies frameworks like the EU AI Act's high-risk documentation
obligations and the NIST AI RMF's Govern/Map functions -- Domain 4's
existing "auditing a classical ML small-business loan-approval
classifier for bias" worked example even has a step where the team
"complete[s] a SageMaker Model Card" -- but neither domain guide ever
shows what a completed Model Card actually contains, which sections
require a governance committee's formal sign-off, how a
performance/fairness trade-off gets documented on it, or how it's used
to defend a deployment decision to a compliance/risk team. These tests
guard the new worked example added to close that gap: it must exist as
a "####"-level subsection nested inside Domain 5 Section 2 (after the
Compliance framework decision matrix's exam tip, before Section 2's
mini-quiz), must not perturb the standalone worked-example counts
asserted elsewhere, must cover all nine standard Model Card sections,
must include a sign-off-requirement table, must document the
performance/fairness trade-off, must show the Model Card being used to
defend the deployment decision to a committee, and must close with an
exam tip. It also guards that the Section 2 exam tip now links forward
to this new subsection, and that Domain 4's existing loan-approval
worked example links forward to it too.

Mirrors the conventions established in
tests/test_domain_5_shared_responsibility_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_model_card_governance_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
DOC_PATH = DOCS_DIR / "domain-5-security-compliance-governance.md"
DOMAIN_4_DOC_PATH = DOCS_DIR / "domain-4-guidelines-for-responsible-ai.md"

HEADING = (
    "#### Worked example: filling out a SageMaker Model Card for "
    "governance sign-off"
)
HEADING_REGEX = (
    r"\n#### Worked example: filling out a SageMaker Model Card for "
    r"governance sign-off"
)
SECTION_2_HEADING = (
    "## 2. AWS compliance standards relevant to AI workloads"
)
SECTION_2_MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of AWS compliance "
    "standards for AI workloads"
)
FORWARD_LINK = (
    "[worked example below]"
    "(#worked-example-filling-out-a-sagemaker-model-card-for-governance-sign-off)"
)
DOMAIN_4_FORWARD_LINK = (
    "[Domain 5's worked example]"
    "(domain-5-security-compliance-governance.md"
    "#worked-example-filling-out-a-sagemaker-model-card-for-governance-sign-off)"
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


class TestDomain5ModelCardGovernanceWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_inside_section_2_after_decision_matrix_and_before_mini_quiz(
        self,
    ):
        section_2_pos = self.text.index(SECTION_2_HEADING)
        heading_pos = self.text.index(HEADING)
        mini_quiz_pos = self.text.index(SECTION_2_MINI_QUIZ_HEADING)
        self.assertLess(section_2_pos, heading_pos)
        self.assertLess(heading_pos, mini_quiz_pos)

    def test_does_not_change_standalone_worked_example_count(self):
        # The new subsection is a level-4 heading nested inside Section 2,
        # not a new standalone "## Worked example" section, so it must not
        # perturb the counts asserted in tests/test_domain_5_study_guide.py
        # or tests/test_documentation_structure.py. There remain two
        # standalone "## Worked example" sections in Domain 5 (the closing
        # HIPAA walkthrough and the multi-region/multi-compliance
        # example).
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 2)

    def test_covers_all_nine_model_card_sections(self):
        for expected in [
            "Model overview.",
            "Intended use.",
            "Training data provenance.",
            "Evaluation metrics.",
            "Bias assessment results.",
            "Explainability.",
            "Known limitations.",
            "Human oversight controls.",
            "Monitoring plan.",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_has_sign_off_requirement_table(self):
        self.assertIn(
            "| Model Card section | Committee sign-off required? | Why |",
            self.section,
        )
        self.assertEqual(self.section.count("**Yes**"), 5)

    def test_documents_the_performance_fairness_tradeoff(self):
        self.assertIn(
            "**Documenting the performance/fairness trade-off.**",
            self.section,
        )
        tradeoff_idx = self.section.index(
            "**Documenting the performance/fairness trade-off.**"
        )
        self.assertIn(
            "AUC-ROC", self.section[tradeoff_idx : tradeoff_idx + 600]
        )

    def test_documents_defending_the_decision_to_the_committee(self):
        self.assertIn(
            "**Defending the deployment decision to the committee.**",
            self.section,
        )
        self.assertGreaterEqual(self.section.count("*Committee:*"), 4)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_section_2_exam_tip_links_forward_to_the_worked_example(self):
        exam_tip_section = _section(
            self.text,
            r"\*\*Exam tip:\*\* Anchor on two clues together",
            HEADING_REGEX,
        )
        self.assertIn(FORWARD_LINK, exam_tip_section)

    def test_domain_4_links_forward_to_this_worked_example(self):
        domain_4_text = DOMAIN_4_DOC_PATH.read_text(encoding="utf-8")
        self.assertIn(DOMAIN_4_FORWARD_LINK, domain_4_text)


if __name__ == "__main__":
    unittest.main()
