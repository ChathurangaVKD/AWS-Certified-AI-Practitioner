"""Structural validation for the "Topic-based review quick reference"
section added to docs/exam-preparation-strategy.md.

The gap this covers: docs/full-length-mock-exam.md already has
score-band remediation tables that point a weak *domain* score to specific
sections in that one domain's guide (a domain-based view), but nothing in
the series helps a learner who has identified one specific weak *topic*
that spans multiple domains (e.g. cost governance, bias and fairness, RAG
concepts, model evaluation) jump directly to all the related material
across the series. This section closes that gap: a new "## 6. Topic-based
review quick reference" section, placed after "## 5. Study plans", listing
high-leverage cross-domain topics with links into each of the five domain
guides (where that domain covers the topic) plus the matching
cross-domain-concept-map.md entry.

These tests guard that the new section exists, is linked from the page's
own intro table of contents, sits after Section 5, covers each of the four
topics with a link into every domain guide that addresses it plus a
cross-domain-concept-map.md link, and that no existing section/heading was
disturbed by the insertion.

Mirrors the conventions established in
tests/test_domain_1_deployment_strategies_subsection.py and
tests/test_domain_3_cost_governance_subsection.py. Link-resolution
(file exists, anchor matches a real heading) for every link introduced
here -- including the new cross-domain-concept-map.md links -- is already
covered generically by
tests/test_exam_preparation_strategy.py::TestExamPreparationStrategyLinksResolve,
which walks every internal markdown link in this file.

Run with:
    python3 -m unittest tests/test_exam_preparation_strategy_topic_quick_reference.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "exam-preparation-strategy.md"

SECTION_HEADING = "## 6. Topic-based review quick reference"
TOC_LINK = "[Topic-based review quick reference](#6-topic-based-review-quick-reference)"

TOPIC_HEADINGS = [
    "### Cost governance",
    "### Bias and fairness",
    "### RAG (Retrieval-Augmented Generation) concepts",
    "### Model evaluation and performance measurement",
]

DOMAIN_FILES = [
    "domain-1-fundamentals-of-ai-and-ml.md",
    "domain-2-fundamentals-of-generative-ai.md",
    "domain-3-applications-of-foundation-models.md",
    "domain-4-guidelines-for-responsible-ai.md",
    "domain-5-security-compliance-governance.md",
]


def _read():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=None):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    if end_heading_regex is None:
        return rest
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestTopicQuickReferenceSectionExists(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read()

    def test_heading_exists(self):
        self.assertIn(SECTION_HEADING, self.text)

    def test_is_linked_from_the_intro_table_of_contents(self):
        intro = _section(self.text, r"^# Exam Preparation and Study Strategy Guide", r"\n---")
        self.assertIn(TOC_LINK, intro)

    def test_sits_after_section_5_study_plans(self):
        section_5_pos = self.text.index("## 5. Study plans")
        section_6_pos = self.text.index(SECTION_HEADING)
        self.assertLess(
            section_5_pos,
            section_6_pos,
            "Topic-based review quick reference must be placed after "
            "Section 5: Study plans",
        )

    def test_is_the_last_section_in_the_document(self):
        # No section heading should follow it -- it's appended at the end.
        section_6_start = self.text.index(SECTION_HEADING)
        rest = self.text[section_6_start + len(SECTION_HEADING):]
        self.assertNotRegex(
            rest,
            r"\n## \d",
            "no other numbered '## N.' section should follow Section 6",
        )

    def test_explains_relationship_to_mock_exam_remediation_tables(self):
        section = _section(self.text, re.escape(SECTION_HEADING))
        self.assertIn("full-length-mock-exam.md", section)
        self.assertIn(
            "full-length-mock-exam.md#score-band-remediation-by-domain",
            section,
        )


class TestTopicQuickReferenceCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read()
        cls.section = _section(cls.text, re.escape(SECTION_HEADING))

    def test_all_four_topics_present(self):
        for heading in TOPIC_HEADINGS:
            with self.subTest(heading=heading):
                self.assertIn(heading, self.section)

    def test_each_topic_links_into_every_domain_guide(self):
        # Slice the section into one chunk per topic heading so a missing
        # domain link in one topic can't be masked by another topic's link
        # to the same file elsewhere in the section.
        boundaries = [self.section.index(h) for h in TOPIC_HEADINGS] + [len(self.section)]
        for i, heading in enumerate(TOPIC_HEADINGS):
            chunk = self.section[boundaries[i]:boundaries[i + 1]]
            for domain_file in DOMAIN_FILES:
                with self.subTest(topic=heading, domain=domain_file):
                    self.assertIn(
                        domain_file,
                        chunk,
                        f"topic {heading!r} does not link into {domain_file}",
                    )

    def test_each_topic_links_to_the_cross_domain_concept_map(self):
        boundaries = [self.section.index(h) for h in TOPIC_HEADINGS] + [len(self.section)]
        for i, heading in enumerate(TOPIC_HEADINGS):
            chunk = self.section[boundaries[i]:boundaries[i + 1]]
            with self.subTest(topic=heading):
                self.assertIn(
                    "cross-domain-concept-map.md",
                    chunk,
                    f"topic {heading!r} does not link to "
                    "cross-domain-concept-map.md",
                )

    def test_found_a_substantial_number_of_internal_links(self):
        md_link_re = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")
        links = [
            link
            for link in md_link_re.findall(self.section)
            if not link.startswith(("http://", "https://", "#"))
        ]
        # 4 topics x (5 domain links + 1 concept-map link) = 24 minimum.
        self.assertGreaterEqual(
            len(links),
            24,
            "expected at least 24 internal links across the four topic "
            "tables (5 domains + concept map per topic)",
        )


class TestTopicQuickReferenceDoesNotDisturbExistingStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read()

    def test_still_exactly_five_numbered_sections_before_section_6(self):
        before_section_6 = self.text[: self.text.index(SECTION_HEADING)]
        numbered_sections = re.findall(r"\n## [1-5]\. ", before_section_6)
        self.assertEqual(
            len(numbered_sections),
            5,
            "Sections 1-5 must be unchanged and precede the new Section 6",
        )

    def test_all_three_study_plans_still_present(self):
        for heading in ["4-week plan", "2-week plan", "1-week plan"]:
            with self.subTest(heading=heading):
                self.assertIn(heading, self.text)


if __name__ == "__main__":
    unittest.main()
