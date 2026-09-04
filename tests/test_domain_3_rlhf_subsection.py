"""Structural validation for the "Reinforcement Learning from Human
Feedback (RLHF)" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3 Section 4 compared fine-tuning, LoRA,
QLoRA, continued pre-training, RAG, and prompt engineering -- with a
decision matrix and worked examples for each -- but never covered RLHF,
a distinct customization technique used to align a fine-tuned (SFT)
model to human preference and instruction-following behavior. The exam
may test RLHF vs. SFT vs. RAG/prompt-engineering selection for
preference-optimization and chat/instruction-following scenarios. These
tests guard the new subsection added to close that gap: it must exist
inside "## 4. Fine-tuning vs. continued pre-training vs. RAG vs. prompt
engineering", be linked from the table of contents, explain RLHF's
relationship to supervised fine-tuning (SFT), contain a decision
table/guidance positioning SFT-alone vs. SFT+RLHF vs. RAG/prompt
engineering, and include an exam tip -- without adding any new numbered
section or extra mini-quiz block (this repo's structural tests assert
exact counts for both).

Mirrors the conventions established in
tests/test_domain_3_fine_tuning_efficiency_techniques_diagram.py.

Run with:
    python3 -m unittest tests/test_domain_3_rlhf_subsection.py -v
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
    "### Reinforcement Learning from Human Feedback (RLHF): aligning "
    "fine-tuned models to human preferences"
)
TOC_LINK = (
    "[Reinforcement Learning from Human Feedback (RLHF): aligning "
    "fine-tuned models to human preferences]"
    "(#reinforcement-learning-from-human-feedback-rlhf-aligning-fine-"
    "tuned-models-to-human-preferences)"
)
MINI_QUIZ_HEADING = (
    "#### Mini-quiz: Test your understanding of customization approach "
    "trade-offs"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3RLHFSubsection(unittest.TestCase):
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

    def test_sits_inside_section_4_after_the_mini_quiz(self):
        # The RLHF subsection was added after Section 4's existing
        # mini-quiz (which must stay the section's only mini-quiz), but
        # must still land inside Section 4, before Section 5 begins.
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        heading_pos = section_4.index(HEADING)
        quiz_pos = section_4.index(MINI_QUIZ_HEADING)
        self.assertGreater(
            heading_pos,
            quiz_pos,
            "RLHF subsection should follow Section 4's existing mini-quiz",
        )

    def test_explains_rlhf_relative_to_supervised_fine_tuning(self):
        self.assertRegex(
            self.subsection,
            r"(?i)\bSFT\b.{0,300}\bRLHF\b|\bRLHF\b.{0,300}\bSFT\b",
            "subsection should explain RLHF's relationship to supervised "
            "fine-tuning (SFT)",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)reward model",
            "subsection should describe the reward-model training stage",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)human",
            "subsection should describe human preference/ranking data",
        )

    def test_decision_table_positions_sft_rlhf_and_rag_prompt_engineering(self):
        tables = re.findall(
            r"(\|.+\|\n\|[-\s|:]+\|\n(?:\|.+\|\n?)+)", self.subsection
        )
        self.assertTrue(tables, "expected a Markdown decision table")
        table = "\n".join(tables)
        for expected in ["SFT", "RLHF", "RAG", "Prompt engineering"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, table)

    def test_covers_when_sft_alone_when_to_layer_rlhf_and_when_rag_suffices(self):
        self.assertRegex(
            self.subsection,
            r"(?i)SFT alone",
            "subsection should call out when SFT alone is sufficient",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)layer RLHF",
            "subsection should call out when to layer RLHF on top of SFT",
        )
        self.assertRegex(
            self.subsection,
            r"(?i)RAG",
            "subsection should call out when RAG/prompt engineering is "
            "sufficient instead of RLHF",
        )

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_has_an_aws_example(self):
        self.assertIn("AWS example:", self.subsection)

    def test_no_new_numbered_section_or_mini_quiz_was_introduced(self):
        numbered_sections = re.findall(r"\n## [1-8]\. ", self.text)
        self.assertEqual(
            len(numbered_sections),
            8,
            "Domain 3 must still have exactly 8 numbered sections",
        )
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        quiz_headings = re.findall(r"\n#### Mini-quiz:", section_4)
        self.assertEqual(
            len(quiz_headings),
            1,
            "Section 4 must still contain exactly one mini-quiz heading",
        )

    def test_does_not_break_mini_quiz_question_numbering(self):
        # Regression guard: the RLHF subsection sits between Section 4's
        # mini-quiz and its closing "---" divider, in the same span the
        # subsection-mini-quiz structural tests scan for numbered quiz
        # questions. Any numbered (markdown ordered) list re-introduced
        # into this subsection would corrupt that scan.
        section_4 = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
            r"\n## 5\. ",
        )
        quiz_text_match = re.search(
            r"#### Mini-quiz: Test your understanding of.*?(?=\n---\n|\Z)",
            section_4,
            re.S,
        )
        self.assertIsNotNone(quiz_text_match)
        quiz_text = quiz_text_match.group(0)
        question_numbers = re.findall(r"^(\d+)\.\s", quiz_text, re.M)
        self.assertEqual(
            [int(n) for n in question_numbers],
            list(range(1, len(question_numbers) + 1)),
            "mini-quiz question numbering in Section 4 must stay "
            "sequential and uncorrupted by later subsection content",
        )


if __name__ == "__main__":
    unittest.main()
