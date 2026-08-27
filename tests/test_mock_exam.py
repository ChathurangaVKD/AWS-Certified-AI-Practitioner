"""Structural validation for docs/mock-exam.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. The gap this document fills is a
full-length, cross-domain mock exam simulating the real AIF-C01 exam's
length (65 questions), timing (90 minutes), and domain-weight distribution
(~20%/24%/28%/14%/14%) -- distinct from the ~85 domain-siloed practice
questions already embedded in the five domain guides. These tests assert
that structure directly against the rendered Markdown so a future edit
can't silently drop the weighted mix, desync the question/answer counts, or
break discoverability from README.md.

Mirrors the conventions established in tests/test_domain_1_study_guide.py
and tests/test_exam_preparation_strategy.py.

Run with:
    python3 -m unittest tests/test_mock_exam.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "mock-exam.md"
README_PATH = REPO_ROOT / "README.md"

TOTAL_QUESTIONS = 65

# Question counts per domain, derived from the real ~20/24/28/14/14 weight
# split applied to a 65-question exam (largest-remainder rounding).
EXPECTED_DOMAIN_COUNTS = {
    1: 13,
    2: 16,
    3: 18,
    4: 9,
    5: 9,
}

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")


def _read(path):
    return path.read_text(encoding="utf-8")


def _slugify(heading_text):
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def _heading_anchors(doc_text):
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestMockExamExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected mock exam document at {DOC_PATH}",
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/mock-exam.md",
            readme_text,
            "README.md must link to the mock exam so learners can "
            "discover it",
        )


class TestMockExamCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def test_has_title(self):
        self.assertRegex(self.text, r"^# Full-Length Mock Exam")

    def test_states_real_exam_length_and_timing(self):
        for fact in ["65", "90 minutes", "90-minute"]:
            with self.subTest(fact=fact):
                self.assertIn(fact, self.text)

    def test_has_domain_weighting_table_with_all_weights_and_counts(self):
        table_section = _section(self.text, r"\n### Domain weighting")
        for weight in ["~20%", "~24%", "~28%", "~14%"]:
            with self.subTest(weight=weight):
                self.assertIn(weight, table_section)
        for count in EXPECTED_DOMAIN_COUNTS.values():
            with self.subTest(count=count):
                self.assertIn(str(count), table_section)
        # A markdown table needs a header separator row.
        self.assertRegex(table_section, r"\|\s*:?-{2,}:?\s*\|")

    def test_question_counts_sum_to_real_exam_length(self):
        self.assertEqual(sum(EXPECTED_DOMAIN_COUNTS.values()), TOTAL_QUESTIONS)

    def test_links_into_every_domain_and_exam_prep_guide(self):
        for domain_file in [
            "domain-1-fundamentals-of-ai-and-ml.md",
            "domain-2-fundamentals-of-generative-ai.md",
            "domain-3-applications-of-foundation-models.md",
            "domain-4-guidelines-for-responsible-ai.md",
            "domain-5-security-compliance-governance.md",
            "exam-preparation-strategy.md",
        ]:
            with self.subTest(domain=domain_file):
                self.assertIn(domain_file, self.text)


class TestMockExamQuestions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.questions_section = _section(
            cls.text, r"\n## Mock exam questions", r"\n## Answer key"
        )
        cls.answers_section = _section(
            cls.text,
            r"\n## Answer key and explanations",
            r"\n## After you finish",
        )

    def _numbered_items(self, section_text):
        return re.findall(r"^(\d+)\.\s", section_text, re.M)

    def test_exactly_65_sequentially_numbered_questions(self):
        numbers = self._numbered_items(self.questions_section)
        self.assertEqual(
            [int(n) for n in numbers],
            list(range(1, TOTAL_QUESTIONS + 1)),
            "mock exam must have exactly 65 sequentially numbered questions",
        )

    def test_every_question_has_at_least_four_options(self):
        blocks = re.split(r"\n(?=\d+\.\s)", self.questions_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
        self.assertEqual(len(blocks), TOTAL_QUESTIONS)
        for block in blocks:
            qnum = block.split(".", 1)[0]
            with self.subTest(question=qnum):
                options = re.findall(r"^\s*[A-F]\.\s", block, re.M)
                self.assertGreaterEqual(
                    len(options),
                    4,
                    f"question {qnum} should have at least 4 answer options",
                )

    def test_at_least_one_multi_response_question(self):
        # The real exam mixes in "Select TWO/THREE" multi-response items;
        # the mock exam should rehearse that format too, not just
        # single-answer multiple choice.
        self.assertRegex(
            self.questions_section,
            re.compile(r"\(Select (TWO|THREE)\.\)"),
            "expected at least one multi-response ('Select TWO/THREE') "
            "question, matching the real exam's question formats",
        )


class TestMockExamAnswerKey(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.questions_section = _section(
            cls.text, r"\n## Mock exam questions", r"\n## Answer key"
        )
        cls.answers_section = _section(
            cls.text,
            r"\n## Answer key and explanations",
            r"\n## After you finish",
        )

    def _numbered_items(self, section_text):
        return re.findall(r"^(\d+)\.\s", section_text, re.M)

    def test_answer_key_covers_every_question_in_order(self):
        q_numbers = [int(n) for n in self._numbered_items(self.questions_section)]
        a_numbers = [int(n) for n in self._numbered_items(self.answers_section)]
        self.assertEqual(
            q_numbers,
            a_numbers,
            "answer key must have exactly one entry per mock exam "
            "question, in order",
        )
        self.assertEqual(len(a_numbers), TOTAL_QUESTIONS)

    def test_every_answer_has_substantive_explanation_and_bolded_letter(self):
        blocks = re.split(r"\n(?=\d+\.\s)", self.answers_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
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
                    r"\*\*[A-F](?:\s*(?:,|and)\s*[A-F])*\s*[—-]",
                    f"answer {anum} should clearly state the correct "
                    f"option letter(s)",
                )

    def test_every_answer_tagged_with_a_domain(self):
        blocks = re.split(r"\n(?=\d+\.\s)", self.answers_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
        for block in blocks:
            anum = block.split(".", 1)[0]
            with self.subTest(answer=anum):
                self.assertRegex(
                    block,
                    r"Domain [1-5]\.",
                    f"answer {anum} should be tagged with the domain it "
                    f"belongs to, so learners can score themselves per "
                    f"domain",
                )

    def test_domain_tag_counts_match_the_weighted_distribution(self):
        tags = re.findall(r"Domain ([1-5])\.", self.answers_section)
        self.assertEqual(len(tags), TOTAL_QUESTIONS)
        counts = {d: 0 for d in EXPECTED_DOMAIN_COUNTS}
        for tag in tags:
            counts[int(tag)] += 1
        self.assertEqual(
            counts,
            EXPECTED_DOMAIN_COUNTS,
            "the mix of domain-tagged answers must match the real exam's "
            "weighted domain distribution",
        )


class TestMockExamLinksResolve(unittest.TestCase):
    """The mock exam's value depends on its links back into the domain
    guides and the exam prep guide actually resolving. Verify every
    relative markdown link (optionally with a #anchor) points at a real
    file, and that the anchor -- if present -- matches a real heading."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.links = MD_LINK_RE.findall(cls.text)
        cls.internal_links = [
            link
            for link in cls.links
            if not link.startswith(("http://", "https://", "#"))
        ]

    def test_found_internal_links(self):
        self.assertGreaterEqual(len(self.internal_links), 5)

    def test_every_internal_link_target_file_exists(self):
        for link in self.internal_links:
            file_part = link.split("#", 1)[0]
            with self.subTest(link=link):
                target_path = (DOCS_DIR / file_part).resolve()
                self.assertTrue(
                    target_path.is_file(),
                    f"linked file does not exist: {file_part!r} "
                    f"(resolved to {target_path})",
                )

    def test_every_internal_anchor_matches_a_real_heading(self):
        anchor_cache = {}
        for link in self.internal_links:
            if "#" not in link:
                continue
            file_part, anchor = link.split("#", 1)
            with self.subTest(link=link):
                if file_part not in anchor_cache:
                    target_path = (DOCS_DIR / file_part).resolve()
                    anchor_cache[file_part] = _heading_anchors(_read(target_path))
                self.assertIn(
                    anchor,
                    anchor_cache[file_part],
                    f"anchor #{anchor} does not match any heading slug in "
                    f"{file_part} -- the mock exam link is stale",
                )


if __name__ == "__main__":
    unittest.main()
