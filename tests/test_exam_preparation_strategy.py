"""Structural validation for docs/exam-preparation-strategy.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. The exam preparation and study strategy
guide exists to consolidate exam format/time-management guidance, domain
weight prioritization, the recommended reading order, every domain's "Exam
tip" callouts, and multi-length study plans into one page, so what matters
most here is that it is actually reachable from README.md, that it covers
the specific content the gap report calls for (domain weights with Domain 3
and Domain 2 called out first, a reading order from Domain 1 to Domain 5,
consolidated exam traps, and 1-week/2-week/4-week study plans), and that
every markdown link it makes into a domain guide resolves to a real file
and a real heading in that file. A future edit that renames a heading in a
domain doc (breaking an anchor link) or removes the README pointer would
otherwise go unnoticed since nothing renders these docs in CI.

Mirrors the conventions established in tests/test_aws_service_decision_guide.py
and tests/test_cross_domain_concept_map.py.

Run with:
    python3 -m unittest tests/test_exam_preparation_strategy.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "exam-preparation-strategy.md"
README_PATH = REPO_ROOT / "README.md"

# Every domain guide the task requires this page to link into (reading
# order + consolidated exam traps must touch all five).
REQUIRED_LINKED_DOMAINS = [
    "domain-1-fundamentals-of-ai-and-ml.md",
    "domain-2-fundamentals-of-generative-ai.md",
    "domain-3-applications-of-foundation-models.md",
    "domain-4-guidelines-for-responsible-ai.md",
    "domain-5-security-compliance-governance.md",
]

# The task explicitly calls out Domain 3 (28%) and Domain 2 (24%) as the
# first two high-yield focus areas by weight.
REQUIRED_WEIGHTS = ["28%", "24%", "20%", "14%"]

REQUIRED_STUDY_PLAN_HEADINGS = [
    "1-week plan",
    "2-week plan",
    "4-week plan",
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
    """Return the set of anchor slugs for every heading in a markdown doc."""
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


class TestExamPreparationStrategyExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected exam preparation strategy guide at {DOC_PATH}",
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/exam-preparation-strategy.md",
            readme_text,
            "README.md must link to the exam preparation strategy guide so "
            "learners can discover it",
        )


class TestExamPreparationStrategyCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def test_has_title(self):
        self.assertRegex(
            self.text, r"^# Exam Preparation and Study Strategy Guide"
        )

    def test_covers_exam_format_and_time_management(self):
        self.assertRegex(self.text, re.compile(r"time management", re.IGNORECASE))
        # Concrete exam-format facts the section should ground its advice in.
        for fact in ["65 questions", "90 minutes"]:
            with self.subTest(fact=fact):
                self.assertIn(fact, self.text)

    def test_covers_domain_weights_with_highest_first(self):
        for weight in REQUIRED_WEIGHTS:
            with self.subTest(weight=weight):
                self.assertIn(weight, self.text)
        # Domain 3 (28%) and Domain 2 (24%) must be called out as the top
        # two high-yield priorities, per the gap report.
        domain_3_pos = self.text.find("28%")
        domain_2_pos = self.text.find("24%")
        domain_1_pos = self.text.find("20%")
        self.assertNotEqual(domain_3_pos, -1)
        self.assertNotEqual(domain_2_pos, -1)
        self.assertNotEqual(domain_1_pos, -1)
        self.assertLess(
            domain_3_pos,
            domain_1_pos,
            "Domain 3 (28%) should be introduced before Domain 1 (20%) in "
            "the weight-prioritized focus-area guidance",
        )
        self.assertLess(
            domain_2_pos,
            domain_1_pos,
            "Domain 2 (24%) should be introduced before Domain 1 (20%) in "
            "the weight-prioritized focus-area guidance",
        )

    def test_has_reading_order_section(self):
        self.assertRegex(
            self.text,
            re.compile(r"reading order", re.IGNORECASE),
            "expected an explicit recommended reading order section",
        )
        # Reading order must be presented Domain 1 first through Domain 5,
        # not weight order, per the gap report.
        self.assertRegex(self.text, re.compile(r"Domain 1.*Domain 2.*Domain 3.*Domain 4.*Domain 5", re.DOTALL))

    def test_has_consolidated_exam_traps_section(self):
        self.assertRegex(
            self.text,
            re.compile(r"exam traps", re.IGNORECASE),
            "expected a section consolidating per-section 'Exam tip' "
            "callouts into common exam traps",
        )
        # Spot-check a handful of distinctive traps drawn from each domain's
        # "Exam tip" callouts to make sure this is a real consolidation, not
        # just a section header.
        for trap_fragment in [
            "overfitting",
            "hallucination",
            "Trainium",
            "Model Card",
            "PrivateLink",
        ]:
            with self.subTest(trap_fragment=trap_fragment):
                self.assertIn(trap_fragment, self.text)

    def test_has_all_three_study_plans(self):
        for heading in REQUIRED_STUDY_PLAN_HEADINGS:
            with self.subTest(heading=heading):
                self.assertRegex(
                    self.text,
                    re.compile(re.escape(heading), re.IGNORECASE),
                    f"expected a {heading!r} study plan section",
                )

    def test_links_into_every_domain(self):
        for domain_file in REQUIRED_LINKED_DOMAINS:
            with self.subTest(domain=domain_file):
                self.assertIn(
                    domain_file,
                    self.text,
                    f"exam prep guide does not link into {domain_file}",
                )

    def test_has_pacing_model_by_question_type_section(self):
        self.assertRegex(
            self.text,
            re.compile(r"^### Pacing model by question type", re.M),
            "expected a 'Pacing model by question type' subsection under "
            "Section 1 (exam format and time management)",
        )

    def test_pacing_section_is_nested_under_time_management(self):
        # The pacing subsection must live inside Section 1, not as a
        # standalone top-level section, since it elaborates on that
        # section's time-management guidance.
        section_1_start = self.text.index("## 1. Exam format and time management")
        section_2_start = self.text.index(
            "## 2. Domain weights and high-yield focus areas"
        )
        pacing_start = self.text.index("### Pacing model by question type")
        self.assertTrue(
            section_1_start < pacing_start < section_2_start,
            "the pacing subsection should appear between Section 1's start "
            "and Section 2's start",
        )

    def test_pacing_section_covers_all_three_question_types_with_times(self):
        pacing_start = self.text.index("### Pacing model by question type")
        section_2_start = self.text.index(
            "## 2. Domain weights and high-yield focus areas"
        )
        pacing_text = self.text[pacing_start:section_2_start]

        for fragment in [
            "Definitional",
            "30–45 seconds",
            "Single-scenario",
            "1–2 minutes",
            "multi-domain scenario",
            "2–3 minutes",
        ]:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, pacing_text)

    def test_pacing_section_covers_flag_and_move_on_guidance(self):
        pacing_start = self.text.index("### Pacing model by question type")
        section_2_start = self.text.index(
            "## 2. Domain weights and high-yield focus areas"
        )
        pacing_text = self.text[pacing_start:section_2_start]

        self.assertRegex(
            pacing_text,
            re.compile(r"flag.{0,20}move on", re.IGNORECASE | re.DOTALL),
            "expected explicit flag-and-move-on guidance in the pacing "
            "subsection",
        )
        self.assertIn(
            "work through",
            pacing_text.lower(),
            "expected explicit 'work through it now' guidance contrasting "
            "with flag-and-move-on",
        )
        self.assertIn(
            "no penalty",
            pacing_text.lower(),
            "expected the pacing guidance to reiterate the no-penalty-for-"
            "guessing rule from Section 1 when advising against leaving "
            "flagged questions unanswered",
        )


class TestExamPreparationStrategyMiniQuizGuidance(unittest.TestCase):
    """The exam prep guide discusses domain practice questions, cross-domain
    scenario questions, and the two mock exams, but historically omitted the
    35 mini-quizzes embedded within each domain guide's own sections. Verify
    the guide now explains what they are, where they live, and how they
    differ from the other, summative practice material."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def test_has_mini_quiz_subsection(self):
        self.assertRegex(
            self.text,
            re.compile(r"^### Mini-quizzes", re.M),
            "expected a 'Mini-quizzes' subsection explaining the embedded "
            "in-domain self-checks",
        )

    def test_mini_quiz_subsection_is_nested_under_time_management(self):
        # Mirrors test_pacing_section_is_nested_under_time_management above:
        # this subsection should live inside Section 1, not stand alone.
        section_1_start = self.text.index("## 1. Exam format and time management")
        section_2_start = self.text.index(
            "## 2. Domain weights and high-yield focus areas"
        )
        mini_quiz_start = self.text.index("### Mini-quizzes")
        self.assertTrue(
            section_1_start < mini_quiz_start < section_2_start,
            "the mini-quiz subsection should appear between Section 1's "
            "start and Section 2's start",
        )

    def test_mini_quiz_subsection_states_the_count_and_placement_facts(self):
        mini_quiz_start = self.text.index("### Mini-quizzes")
        section_2_start = self.text.index(
            "## 2. Domain weights and high-yield focus areas"
        )
        mini_quiz_text = self.text[mini_quiz_start:section_2_start]

        for fragment in [
            "35",
            "5–8 per domain",
        ]:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, mini_quiz_text)

        # Markdown source-wraps long lines, so allow whitespace (including a
        # literal newline) between the two words instead of requiring an
        # exact substring match.
        self.assertRegex(
            mini_quiz_text,
            re.compile(r"table\s+of\s+contents", re.IGNORECASE),
            "expected the mini-quiz guidance to explain that mini-quizzes "
            "are intentionally left out of the domain guides' tables of "
            "contents",
        )

    def test_mini_quiz_subsection_distinguishes_formative_from_summative(self):
        mini_quiz_start = self.text.index("### Mini-quizzes")
        section_2_start = self.text.index(
            "## 2. Domain weights and high-yield focus areas"
        )
        mini_quiz_text = self.text[mini_quiz_start:section_2_start]

        self.assertIn("formative", mini_quiz_text.lower())
        self.assertIn(
            "summative",
            mini_quiz_text.lower(),
            "expected the mini-quiz guidance to explicitly contrast "
            "formative in-section quizzes with summative practice material",
        )
        # Must reference at least one of the other practice-material layers
        # it's being distinguished from.
        self.assertRegex(
            mini_quiz_text,
            re.compile(r"practice questions|scenario questions|mock exam", re.IGNORECASE),
        )

    def test_intro_links_to_mini_quiz_subsection(self):
        # The top-of-page summary of what this guide covers should point
        # readers at the mini-quiz subsection, same as it does for the
        # numbered sections.
        self.assertIn("#mini-quizzes-formative-checks-while-you-study", self.text)


class TestExamPreparationStrategyLinksResolve(unittest.TestCase):
    """This page's value comes from linking back into the domain guides it
    consolidates. Verify every relative markdown link (optionally with a
    #anchor) points at a real file, and that the anchor -- if present --
    matches a real heading in that file."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.links = MD_LINK_RE.findall(cls.text)
        cls.internal_links = [
            link
            for link in cls.links
            if not link.startswith(("http://", "https://", "#"))
        ]

    def test_found_a_substantial_number_of_internal_links(self):
        # Sanity check that the regex above is actually matching the
        # document's link syntax, so the resolution tests below aren't
        # silently vacuous.
        self.assertGreaterEqual(
            len(self.internal_links),
            20,
            "expected many internal links from the exam prep guide into "
            "the domain guides",
        )

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
                    f"{file_part} -- the exam prep guide link is stale",
                )


if __name__ == "__main__":
    unittest.main()
