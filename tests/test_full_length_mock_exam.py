"""Structural validation for docs/full-length-mock-exam.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. The gap this document fills: the series
had ~85 domain-siloed practice questions but nothing simulating the real
exam's length (65 questions), domain-weight distribution
(~20%/24%/28%/14%/14%), or time constraint (90 minutes). These tests assert
that the mock exam actually has 65 sequentially numbered questions, that
those questions are drawn from all five domains in proportions matching the
real exam's weights, that every question has a full answer key entry with a
substantive explanation, and that the document is reachable from README.md
and cross-linked with the exam preparation guide.

Mirrors the conventions established in tests/test_domain_1_study_guide.py
(question/answer structural checks) and
tests/test_exam_preparation_strategy.py (existence/discoverability/link
resolution checks).

Run with:
    python3 -m unittest tests/test_full_length_mock_exam.py -v
"""

import re
import unittest
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "full-length-mock-exam.md"
README_PATH = REPO_ROOT / "README.md"
EXAM_PREP_PATH = DOCS_DIR / "exam-preparation-strategy.md"

TOTAL_QUESTIONS = 65

# Expected question count per domain, derived from the real exam's domain
# weights (~20%/24%/28%/14%/14%) applied to 65 total questions.
EXPECTED_DOMAIN_COUNTS = {
    1: 13,
    2: 16,
    3: 18,
    4: 9,
    5: 9,
}

REQUIRED_LINKED_DOMAINS = [
    "domain-1-fundamentals-of-ai-and-ml.md",
    "domain-2-fundamentals-of-generative-ai.md",
    "domain-3-applications-of-foundation-models.md",
    "domain-4-guidelines-for-responsible-ai.md",
    "domain-5-security-compliance-governance.md",
]

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")


def _read(path):
    return path.read_text(encoding="utf-8")


def _slugify(heading_text):
    """Approximate the GitHub markdown heading-anchor algorithm: lowercase,
    strip characters that aren't word characters/spaces/hyphens, then turn
    runs of whitespace into single hyphens."""
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


def _numbered_items(section_text):
    return re.findall(r"^(\d+)\.\s", section_text, re.M)


class TestMockExamExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(), f"expected full-length mock exam at {DOC_PATH}"
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/full-length-mock-exam.md",
            readme_text,
            "README.md must link to the full-length mock exam so learners "
            "can discover it",
        )

    def test_linked_from_exam_preparation_strategy(self):
        exam_prep_text = _read(EXAM_PREP_PATH)
        self.assertIn(
            "full-length-mock-exam.md",
            exam_prep_text,
            "exam-preparation-strategy.md's study plans reference a mock "
            "exam but did not link to the actual mock exam document",
        )


class TestMockExamOverview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def test_has_title(self):
        self.assertRegex(self.text, r"^# Full-Length Mock Exam \(AIF-C01\)")

    def test_mentions_exam_format(self):
        for fact in ["65 questions", "90 minutes", "65", "90-minute"]:
            with self.subTest(fact=fact):
                self.assertIn(fact, self.text)

    def test_no_penalty_for_guessing_guidance_present(self):
        self.assertRegex(
            self.text,
            re.compile(r"no penalty for guessing|answer every question", re.IGNORECASE),
            "expected timing/strategy guidance telling learners to answer "
            "every question since there's no penalty for guessing",
        )

    def test_domain_distribution_table_matches_expected_counts(self):
        table_section = _section(
            self.text,
            r"\n## 2\. Domain-weighted question distribution",
            r"\n---",
        )
        # Every domain's weight and its question count in this mock exam
        # must both appear in the distribution table.
        weights = {1: "20%", 2: "24%", 3: "28%", 4: "14%", 5: "14%"}
        for domain, weight in weights.items():
            with self.subTest(domain=domain):
                self.assertIn(weight, table_section)
        for domain, count in EXPECTED_DOMAIN_COUNTS.items():
            with self.subTest(domain=domain, count=count):
                self.assertIn(
                    f"| {count} |",
                    table_section,
                    f"distribution table missing a row with {count} "
                    f"questions for Domain {domain}",
                )
        self.assertIn(
            str(TOTAL_QUESTIONS),
            table_section,
            "distribution table should state the total of 65 questions",
        )
        self.assertEqual(sum(EXPECTED_DOMAIN_COUNTS.values()), TOTAL_QUESTIONS)


class TestMockExamQuestions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.questions_section = _section(
            cls.text,
            r"\n## Mock exam questions",
            r"\n## 3\. Scoring your mock exam",
        )
        cls.answers_section = _section(
            cls.text, r"\n## 4\. Answer key and explanations"
        )

    def test_exactly_65_sequentially_numbered_questions(self):
        numbers = _numbered_items(self.questions_section)
        self.assertEqual(
            [int(n) for n in numbers],
            list(range(1, TOTAL_QUESTIONS + 1)),
            "mock exam must have exactly 65 sequentially numbered questions "
            "starting at 1",
        )

    def test_questions_are_not_grouped_by_domain(self):
        # The whole point of a mock exam (vs. the domain guides' siloed
        # question sets) is that questions are mixed, not grouped in five
        # contiguous domain blocks. Detect accidental domain-siloing by
        # checking the answer key's domain tags aren't just five long runs.
        tags = re.findall(r"\*\(Domain (\d)\)\*", self.answers_section)
        self.assertEqual(len(tags), TOTAL_QUESTIONS)
        # Count the number of "runs" of consecutive identical domain tags.
        runs = 1
        for prev, cur in zip(tags, tags[1:]):
            if cur != prev:
                runs += 1
        # If every question were grouped by domain, there would be exactly
        # 5 runs (one per domain). A well-mixed exam should have far more
        # run transitions than that.
        self.assertGreater(
            runs,
            10,
            "questions appear to be grouped by domain rather than mixed "
            "in exam-like order",
        )

    def test_every_question_has_at_least_four_options(self):
        blocks = re.split(r"\n(?=\d+\.\s)", self.questions_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
        self.assertEqual(len(blocks), TOTAL_QUESTIONS)
        for block in blocks:
            qnum = block.split(".", 1)[0]
            with self.subTest(question=qnum):
                options = re.findall(r"^\s*[A-E]\.\s", block, re.M)
                self.assertGreaterEqual(
                    len(options),
                    4,
                    f"question {qnum} should have at least 4 answer options",
                )

    def test_select_two_questions_offer_five_options(self):
        blocks = re.split(r"\n(?=\d+\.\s)", self.questions_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
        select_two_blocks = [b for b in blocks if "Select TWO" in b]
        self.assertGreaterEqual(
            len(select_two_blocks),
            1,
            "expected at least one multiple-response (Select TWO) question, "
            "matching the real exam's mix of question formats",
        )
        for block in select_two_blocks:
            qnum = block.split(".", 1)[0]
            with self.subTest(question=qnum):
                options = re.findall(r"^\s*[A-E]\.\s", block, re.M)
                self.assertGreaterEqual(len(options), 5)


class TestMockExamAnswerKey(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.questions_section = _section(
            cls.text,
            r"\n## Mock exam questions",
            r"\n## 3\. Scoring your mock exam",
        )
        cls.answers_section = _section(
            cls.text, r"\n## 4\. Answer key and explanations"
        )

    def test_answer_key_covers_every_question(self):
        q_numbers = [int(n) for n in _numbered_items(self.questions_section)]
        a_numbers = [int(n) for n in _numbered_items(self.answers_section)]
        self.assertEqual(
            q_numbers,
            a_numbers,
            "answer key must have exactly one entry per mock exam question, "
            "in order",
        )

    def test_every_answer_has_substantive_explanation_and_bolded_choice(self):
        blocks = re.split(r"\n(?=\d+\.\s)", self.answers_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
        self.assertEqual(len(blocks), TOTAL_QUESTIONS)
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
                    r"\*\*[A-E](?:\s*(?:,|and)\s*[A-E])*\s*[—-]",
                    f"answer {anum} should clearly state the correct "
                    f"option letter(s)",
                )
                self.assertRegex(
                    block,
                    r"\*\(Domain [1-5]\)\*",
                    f"answer {anum} should be tagged with its source "
                    f"domain so learners can self-score by domain",
                )

    def test_domain_tag_counts_match_expected_weighted_distribution(self):
        tags = re.findall(r"\*\(Domain (\d)\)\*", self.answers_section)
        counts = Counter(int(t) for t in tags)
        self.assertEqual(
            dict(counts),
            EXPECTED_DOMAIN_COUNTS,
            "the number of questions tagged per domain in the answer key "
            "should match the real exam's domain-weight distribution",
        )


class TestMockExamLinksResolve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.links = MD_LINK_RE.findall(cls.text)
        cls.internal_links = [
            link
            for link in cls.links
            if not link.startswith(("http://", "https://", "#"))
        ]

    def test_links_into_every_domain_guide(self):
        for domain_file in REQUIRED_LINKED_DOMAINS:
            with self.subTest(domain=domain_file):
                self.assertIn(domain_file, self.text)

    def test_links_into_exam_preparation_strategy(self):
        self.assertIn("exam-preparation-strategy.md", self.text)

    def test_every_internal_link_target_file_exists(self):
        for link in self.internal_links:
            file_part = link.split("#", 1)[0]
            if not file_part:
                # Pure same-document anchor link (e.g. "#section").
                continue
            with self.subTest(link=link):
                target_path = (DOCS_DIR / file_part).resolve()
                self.assertTrue(
                    target_path.is_file(),
                    f"linked file does not exist: {file_part!r} "
                    f"(resolved to {target_path})",
                )

    def test_every_cross_document_anchor_matches_a_real_heading(self):
        anchor_cache = {}
        for link in self.internal_links:
            if "#" not in link:
                continue
            file_part, anchor = link.split("#", 1)
            if not file_part:
                # Same-document anchor, checked separately below.
                continue
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

    def test_every_same_document_anchor_matches_a_real_heading(self):
        own_anchors = _heading_anchors(self.text)
        same_doc_anchors = [
            link.split("#", 1)[1] for link in self.links if link.startswith("#")
        ]
        self.assertGreater(
            len(same_doc_anchors), 0, "expected at least one same-document anchor link"
        )
        for anchor in same_doc_anchors:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, own_anchors)


if __name__ == "__main__":
    unittest.main()
