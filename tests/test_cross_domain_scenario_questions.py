"""Structural validation for docs/cross-domain-scenario-questions.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. The gap this document fills: every
practice question in the five domain guides (and the full-length mock
exam) is scoped to a single domain, but the real AIF-C01 exam frequently
tests two or more domains in the same scenario question (e.g., "choose a
Domain 3 customization method that satisfies a Domain 5 security
requirement"). These tests assert that the new cross-domain question set
actually has that property: every question is tagged with a difficulty
level, has a well-formed answer key entry, and -- critically -- every
answer is tagged with two or more distinct domain numbers rather than
being secretly single-domain.

Mirrors the conventions established in tests/test_domain_1_study_guide.py
(question/answer structural checks) and tests/test_full_length_mock_exam.py
(domain-tag and discoverability checks).

Run with:
    python3 -m unittest tests/test_cross_domain_scenario_questions.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "cross-domain-scenario-questions.md"
README_PATH = REPO_ROOT / "README.md"

MIN_QUESTIONS = 10
MAX_QUESTIONS = 30
MIN_THREE_PLUS_DOMAIN_QUESTIONS = 4

DIFFICULTY_RE = re.compile(r"\*\*\[(Beginner|Intermediate|Advanced)\]\*\*")
DOMAIN_TAG_RE = re.compile(r"\*\(Domains?\s+([0-9,\s]+)\)\*")
CORRECT_LETTER_RE = re.compile(r"\*\*[A-E](?:\s*(?:,|and)\s*[A-E])*\s*[—-]")


def _read(path):
    return path.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


def _numbered_items(section_text):
    return re.findall(r"^(\d+)\.\s", section_text, re.M)


def _blocks(section_text):
    parts = re.split(r"\n(?=\d+\.\s)", section_text.strip())
    return [b for b in parts if re.match(r"^\d+\.\s", b)]


class TestCrossDomainScenarioQuestionsExist(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected cross-domain scenario questions at {DOC_PATH}",
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/cross-domain-scenario-questions.md",
            readme_text,
            "README.md must link to the cross-domain scenario questions "
            "so learners can discover them",
        )

    def test_readme_question_count_matches_actual_count(self):
        readme_text = _read(README_PATH)
        count_match = re.search(r"for (\d+) scenario questions", readme_text)
        self.assertIsNotNone(
            count_match,
            "README.md should state how many scenario questions the doc "
            "has, e.g. 'for 22 scenario questions'",
        )

        doc_text = _read(DOC_PATH)
        questions_section = _section(
            doc_text, r"\n## Practice questions", r"\n## Answer key"
        )
        actual_count = len(_numbered_items(questions_section))

        self.assertEqual(
            int(count_match.group(1)),
            actual_count,
            "README.md's claimed scenario question count must match the "
            "actual number of questions in "
            "docs/cross-domain-scenario-questions.md",
        )


class TestCrossDomainScenarioQuestionsOverview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def test_has_title(self):
        self.assertRegex(self.text, r"^# Cross-Domain Scenario Questions")

    def test_links_back_to_domain_guides_and_concept_map(self):
        for target in [
            "domain-1-fundamentals-of-ai-and-ml.md",
            "domain-2-fundamentals-of-generative-ai.md",
            "domain-3-applications-of-foundation-models.md",
            "domain-4-guidelines-for-responsible-ai.md",
            "domain-5-security-compliance-governance.md",
            "cross-domain-concept-map.md",
        ]:
            with self.subTest(target=target):
                self.assertIn(target, self.text)

    def test_difficulty_tags_are_paired_with_pacing_guidance(self):
        # Each question's difficulty tag sits at the very start of the
        # question (before its scenario text -- see
        # test_every_question_has_options_and_a_difficulty_tag), so a
        # learner already sees pacing-relevant info before reading. This
        # asserts the doc also spells out *what* pacing each tag implies,
        # tied to the shared pacing model in exam-preparation-strategy.md,
        # rather than leaving the tag as a topic label with no time budget
        # attached.
        overview_section = self.text[: self.text.index("## Practice questions")]

        self.assertIn(
            "exam-preparation-strategy.md#pacing-model-by-question-type",
            overview_section,
            "the difficulty-tag explanation should link to the shared "
            "pacing model so tags double as timing guidance",
        )
        for tier in ("Beginner", "Intermediate", "Advanced"):
            with self.subTest(tier=tier):
                self.assertIn(f"[{tier}]", overview_section)
        self.assertRegex(
            overview_section,
            r"~1–2 minute",
            "should state a concrete pacing target for Beginner/"
            "Intermediate questions",
        )
        self.assertRegex(
            overview_section,
            r"~2–3 minute",
            "should state a concrete pacing target for Advanced questions",
        )


class TestCrossDomainScenarioQuestions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.questions_section = _section(
            cls.text, r"\n## Practice questions", r"\n## Answer key"
        )
        cls.answers_section = _section(
            cls.text, r"\n## Answer key and explanations"
        )

    def test_question_count_within_range_and_sequential(self):
        numbers = _numbered_items(self.questions_section)
        self.assertEqual(
            [int(n) for n in numbers],
            list(range(1, len(numbers) + 1)),
            "cross-domain questions must be sequentially numbered starting at 1",
        )
        self.assertGreaterEqual(len(numbers), MIN_QUESTIONS)
        self.assertLessEqual(len(numbers), MAX_QUESTIONS)

    def test_every_question_has_options_and_a_difficulty_tag(self):
        blocks = _blocks(self.questions_section)
        for block in blocks:
            qnum = block.split(".", 1)[0]
            with self.subTest(question=qnum):
                self.assertRegex(
                    block,
                    r"^\d+\.\s\*\*\[(Beginner|Intermediate|Advanced)\]\*\*\s",
                    f"question {qnum} should start with a difficulty tag",
                )
                options = re.findall(r"^\s*[A-E]\.\s", block, re.M)
                min_options = 5 if "Select TWO" in block else 4
                self.assertGreaterEqual(
                    len(options),
                    min_options,
                    f"question {qnum} should have at least {min_options} options",
                )

    def test_answer_key_covers_every_question_with_explanation_and_domain_tags(self):
        q_numbers = [int(n) for n in _numbered_items(self.questions_section)]
        a_numbers = [int(n) for n in _numbered_items(self.answers_section)]
        self.assertEqual(
            q_numbers,
            a_numbers,
            "answer key must have exactly one entry per question, in order",
        )

        blocks = _blocks(self.answers_section)
        all_domains_seen = set()
        for block in blocks:
            anum = block.split(".", 1)[0]
            with self.subTest(answer=anum):
                self.assertGreater(
                    len(block.strip()),
                    120,
                    f"answer {anum} explanation looks too short to justify "
                    f"the correct choice and rule out the distractors",
                )
                self.assertRegex(
                    block,
                    CORRECT_LETTER_RE,
                    f"answer {anum} should clearly state the correct option letter(s)",
                )
                tag_match = DOMAIN_TAG_RE.search(block)
                self.assertTrue(
                    tag_match,
                    f"answer {anum} should be tagged with the domains it draws "
                    f"on, e.g. '*(Domains 3, 5)*'",
                )
                domains = {
                    int(d) for d in re.findall(r"[0-9]+", tag_match.group(1))
                }
                self.assertTrue(
                    domains.issubset({1, 2, 3, 4, 5}),
                    f"answer {anum} domain tag references an invalid domain "
                    f"number: {domains}",
                )
                self.assertGreaterEqual(
                    len(domains),
                    2,
                    f"answer {anum} must name at least two distinct domains "
                    f"to be a genuine cross-domain question, got {domains}",
                )
                all_domains_seen |= domains

        # Sanity check against a degenerate set that always pairs the same
        # two domains -- a real cross-domain set should span most/all of
        # the five domains across its full question list.
        self.assertGreaterEqual(
            len(all_domains_seen),
            4,
            "cross-domain questions collectively should span at least 4 "
            "distinct domains, not repeatedly pair the same two",
        )

    def test_includes_multiple_three_or_more_domain_questions(self):
        # The original 22-question set was entirely pairwise (exactly two
        # domains per answer), which left no practice for the real exam's
        # (and this repo's own case-study-ai-system-lifecycle.md's) habit
        # of layering three or more domains into a single scenario. This
        # asserts that gap is actually closed, not just documented.
        blocks = _blocks(self.answers_section)
        three_plus_count = 0
        for block in blocks:
            tag_match = DOMAIN_TAG_RE.search(block)
            if not tag_match:
                continue
            domains = {int(d) for d in re.findall(r"[0-9]+", tag_match.group(1))}
            if len(domains) >= 3:
                three_plus_count += 1

        self.assertGreaterEqual(
            three_plus_count,
            MIN_THREE_PLUS_DOMAIN_QUESTIONS,
            "expected at least "
            f"{MIN_THREE_PLUS_DOMAIN_QUESTIONS} scenario questions whose "
            "answer is tagged with three or more distinct domains -- "
            "genuine 3+ domain reasoning, not just pairwise combinations",
        )

    def test_three_or_more_domain_questions_are_advanced(self):
        # Every current 3+ domain question is tagged Advanced; verify any
        # question whose answer spans 3+ domains carries that difficulty
        # tag, since layering that many concepts together is inherently
        # harder than a pairwise question.
        q_blocks = {
            int(b.split(".", 1)[0]): b for b in _blocks(self.questions_section)
        }
        a_blocks = _blocks(self.answers_section)
        for block in a_blocks:
            anum = int(block.split(".", 1)[0])
            tag_match = DOMAIN_TAG_RE.search(block)
            if not tag_match:
                continue
            domains = {int(d) for d in re.findall(r"[0-9]+", tag_match.group(1))}
            if len(domains) >= 3:
                with self.subTest(question=anum):
                    self.assertIn(
                        "[Advanced]",
                        q_blocks[anum],
                        f"question {anum} draws on 3+ domains "
                        f"({sorted(domains)}) and should be tagged "
                        "[Advanced]",
                    )


if __name__ == "__main__":
    unittest.main()
