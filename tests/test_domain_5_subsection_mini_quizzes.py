"""Structural validation for the Domain 5 subsection mini-quizzes.

Domain 5 (~14% of exam) previously offered only one summative
practice-question set at the very end of the document (26 questions), with
no way for learners to self-check their understanding incrementally while
working through each of its five major numbered sections. This test asserts
that every one of the five major numbered sections ("## 1." through
"## 5.") now contains at least one short formative "Mini-quiz" checkpoint --
2 to 4 multiple-choice questions each, with at least four options and an
inline answer explanation -- placed *within* that section (i.e. before the
section ends), so a future edit that drops a mini-quiz, strips its
explanations, or moves it out of its section is caught automatically.

Sections 1 and 2 carry more than one mini-quiz block (matching Domain 5's
higher conceptual density), so this file bounds each individual quiz block
by the *next* heading of any level (or the section's closing "---"
divider), rather than assuming a single quiz runs to the end of the
section.

Mirrors the conventions established in
tests/test_domain_1_subsection_mini_quizzes.py and
tests/test_domain_3_subsection_mini_quizzes.py.

Run with:
    python3 -m unittest tests/test_domain_5_subsection_mini_quizzes.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)

MIN_QUIZ_QUESTIONS = 2
MAX_QUIZ_QUESTIONS = 4


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _numbered_sections(text):
    """Return (heading, body) pairs for each "## 1." through "## 5."
    top-level section, mirroring tests/test_domain_3_subsection_mini_quizzes.py."""
    sections = re.findall(r"\n## ([1-5]\. .*?)\n(.*?)(?=\n## |\Z)", text, re.S)
    return sections


def _mini_quiz_blocks(body):
    """Return the full text of every '#### Mini-quiz: ...' block in body.

    Each block runs from its own heading up to (but not including) the next
    heading of any level ("#" through "####"), or the section's closing
    "---" divider, whichever comes first. This lets a single "## N. ..."
    section legitimately contain more than one mini-quiz.
    """
    heading_iter = list(re.finditer(r"^#### Mini-quiz: Test your understanding of.*$", body, re.M))
    blocks = []
    for i, match in enumerate(heading_iter):
        start = match.start()
        # End at the next heading of any level, or the next "---" divider,
        # whichever comes first after this quiz's heading.
        search_from = match.end()
        next_heading = re.search(r"^#{1,4}\s", body[search_from:], re.M)
        next_divider = re.search(r"\n---\n", body[search_from:])
        end_candidates = [len(body) - search_from]
        if next_heading:
            end_candidates.append(next_heading.start())
        if next_divider:
            end_candidates.append(next_divider.start())
        end = search_from + min(end_candidates)
        blocks.append(body[start:end])
    return blocks


class TestDomain5SubsectionMiniQuizzes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.sections = _numbered_sections(cls.text)

    def test_found_all_five_numbered_sections(self):
        self.assertEqual(
            len(self.sections),
            5,
            "expected exactly 5 numbered topic sections in Domain 5",
        )

    def test_every_numbered_section_has_a_mini_quiz_heading(self):
        for heading, body in self.sections:
            with self.subTest(section=heading):
                self.assertRegex(
                    body,
                    r"#### Mini-quiz: Test your understanding of",
                    f"section {heading!r} is missing a subsection mini-quiz",
                )

    def test_mini_quiz_sits_before_the_next_top_level_divider(self):
        # Every mini-quiz heading in a section must appear before the "---"
        # divider that closes out the section, i.e. it belongs to *this*
        # section, not dangling after it / before the next "## " heading.
        for heading, body in self.sections:
            with self.subTest(section=heading):
                quiz_matches = list(
                    re.finditer(r"#### Mini-quiz: Test your understanding of", body)
                )
                self.assertTrue(quiz_matches)
                divider_match = re.search(r"\n---\n", body)
                self.assertIsNotNone(
                    divider_match,
                    f"section {heading!r} should end with a '---' divider",
                )
                for quiz_match in quiz_matches:
                    self.assertLess(
                        quiz_match.start(),
                        divider_match.start(),
                        f"mini-quiz in section {heading!r} should appear before "
                        "the section's closing divider",
                    )

    def test_mini_quiz_has_two_to_four_questions_with_four_options_each(self):
        for heading, body in self.sections:
            quiz_blocks = _mini_quiz_blocks(body)
            self.assertTrue(quiz_blocks, f"no mini-quiz found in {heading!r}")
            for quiz_text in quiz_blocks:
                quiz_title_match = re.match(
                    r"#### Mini-quiz: Test your understanding of (.*)", quiz_text
                )
                quiz_label = quiz_title_match.group(1) if quiz_title_match else heading
                question_numbers = re.findall(r"^(\d+)\.\s", quiz_text, re.M)
                with self.subTest(section=heading, quiz=quiz_label):
                    self.assertEqual(
                        [int(n) for n in question_numbers],
                        list(range(1, len(question_numbers) + 1)),
                        f"mini-quiz questions in {quiz_label!r} (section "
                        f"{heading!r}) must be sequentially numbered starting "
                        "at 1",
                    )
                    self.assertGreaterEqual(
                        len(question_numbers),
                        MIN_QUIZ_QUESTIONS,
                        f"mini-quiz {quiz_label!r} in {heading!r} should have "
                        f"at least {MIN_QUIZ_QUESTIONS} questions",
                    )
                    self.assertLessEqual(
                        len(question_numbers),
                        MAX_QUIZ_QUESTIONS,
                        f"mini-quiz {quiz_label!r} in {heading!r} should have "
                        f"at most {MAX_QUIZ_QUESTIONS} questions",
                    )

                blocks = re.split(r"\n(?=\d+\.\s)", quiz_text.strip())
                blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
                for block in blocks:
                    qnum = block.split(".", 1)[0]
                    with self.subTest(section=heading, quiz=quiz_label, question=qnum):
                        options = re.findall(r"^\s*[A-E]\.\s", block, re.M)
                        self.assertGreaterEqual(
                            len(options),
                            4,
                            f"mini-quiz question {qnum} in {quiz_label!r} "
                            f"(section {heading!r}) should have at least 4 "
                            "answer options",
                        )
                        self.assertRegex(
                            block,
                            r"\*\*Answer:\s*[A-E]\*\*\s*[—-]\s*\S",
                            f"mini-quiz question {qnum} in {quiz_label!r} "
                            f"(section {heading!r}) should state the correct "
                            "option with a brief explanation (e.g. "
                            "'**Answer: B** — ...')",
                        )

    def test_mini_quiz_topics_match_their_parent_section(self):
        # Sanity-check the mini-quiz titles line up 1:1 with the sections
        # they follow, e.g. "Test your understanding of data governance
        # strategies" directly after "## 4. Data governance strategies".
        # Sections 1 and 2 carry more than one mini-quiz block, so each
        # section maps to a *list* of acceptable topic fragments, and every
        # quiz heading in that section must match at least one of them.
        expected_topic_fragments = {
            "1": [
                "encryption key management for ai workloads",
                "security and responsible ai intersections",
                "securing ai systems",
            ],
            "2": [
                "gdpr, hipaa, and the nist ai rmf",
                "aws compliance standards for ai workloads",
            ],
            "3": ["aws config, audit manager, and cloudtrail for ai governance"],
            "4": ["data governance strategies"],
            "5": ["aws shared responsibility model"],
        }
        for heading, body in self.sections:
            section_num = heading.split(".", 1)[0]
            with self.subTest(section=heading):
                quiz_heading_matches = re.findall(
                    r"#### Mini-quiz: (Test your understanding of .*)", body
                )
                self.assertTrue(quiz_heading_matches)
                fragments = expected_topic_fragments[section_num]
                for quiz_heading in quiz_heading_matches:
                    self.assertTrue(
                        any(fragment in quiz_heading.lower() for fragment in fragments),
                        f"mini-quiz heading {quiz_heading!r} in section "
                        f"{heading!r} does not match any expected topic "
                        f"fragment {fragments!r}",
                    )
                # And every expected fragment for this section must be used
                # by at least one quiz heading, so a silently dropped quiz
                # is caught too.
                for fragment in fragments:
                    self.assertTrue(
                        any(fragment in qh.lower() for qh in quiz_heading_matches),
                        f"section {heading!r} is missing an expected "
                        f"mini-quiz covering {fragment!r}",
                    )

    def test_expected_number_of_mini_quizzes_per_section(self):
        expected_quiz_counts = {"1": 3, "2": 2, "3": 1, "4": 1, "5": 1}
        for heading, body in self.sections:
            section_num = heading.split(".", 1)[0]
            with self.subTest(section=heading):
                quiz_blocks = _mini_quiz_blocks(body)
                self.assertEqual(
                    len(quiz_blocks),
                    expected_quiz_counts[section_num],
                    f"section {heading!r} should contain "
                    f"{expected_quiz_counts[section_num]} mini-quiz block(s)",
                )


if __name__ == "__main__":
    unittest.main()
