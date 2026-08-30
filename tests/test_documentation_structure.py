"""Regression tests for docs/DOCUMENTATION_STRUCTURE.md staying in sync with
the files it describes.

The gap this covers: DOCUMENTATION_STRUCTURE.md records prose metadata
about the repo's own content -- per-domain line counts and a list of the
cross-domain support files -- that nothing enforced, so it silently drifted
out of date as the domain guides grew and new supporting files (like
cross-domain-scenario-questions.md) were added. This test asserts:

  * every line count for a domain guide stated in DOCUMENTATION_STRUCTURE.md
    matches that file's actual current line count, and
  * cross-domain-scenario-questions.md is documented alongside the repo's
    other cross-domain support materials.

Run with:
    python3 -m unittest tests/test_documentation_structure.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
STRUCTURE_DOC = DOCS_DIR / "DOCUMENTATION_STRUCTURE.md"
README_PATH = REPO_ROOT / "README.md"
SCENARIO_QUESTIONS_DOC = DOCS_DIR / "cross-domain-scenario-questions.md"

DOMAIN_FILES = {
    1: DOCS_DIR / "domain-1-fundamentals-of-ai-and-ml.md",
    2: DOCS_DIR / "domain-2-fundamentals-of-generative-ai.md",
    3: DOCS_DIR / "domain-3-applications-of-foundation-models.md",
    4: DOCS_DIR / "domain-4-guidelines-for-responsible-ai.md",
    5: DOCS_DIR / "domain-5-security-compliance-governance.md",
}

CROSS_DOMAIN_SUPPORT_FILES = [
    "cross-domain-scenario-questions.md",
    "cross-domain-concept-map.md",
    "case-study-ai-system-lifecycle.md",
    "exam-preparation-strategy.md",
    "full-length-mock-exam.md",
    "aws-service-decision-guide.md",
    "master-glossary.md",
]


def _line_count(path):
    text = path.read_text(encoding="utf-8")
    # Match `wc -l`: count newline characters.
    return text.count("\n")


class TestDocumentationStructureLineCounts(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md states an exact line count per domain
    guide (e.g. "Domain 1: 1,118 lines"); each must match reality so the
    doc doesn't silently go stale as guides grow."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def test_stated_domain_line_counts_match_actual_files(self):
        for domain_number, path in DOMAIN_FILES.items():
            actual = _line_count(path)
            formatted = f"{actual:,}"
            with self.subTest(domain=domain_number):
                self.assertIn(
                    f"Domain {domain_number}: {formatted} lines",
                    self.structure_text,
                    f"DOCUMENTATION_STRUCTURE.md does not state the "
                    f"current line count ({formatted}) for domain "
                    f"{domain_number}'s guide ({path.name}) -- it has "
                    "gone stale or the file was edited without updating "
                    "the recorded count",
                )

    def test_no_stale_domain_line_count_figures(self):
        """Guard against an old, now-wrong count lingering alongside (or
        instead of) the correct one."""
        stated_counts = {
            int(n): int(c.replace(",", ""))
            for n, c in re.findall(
                r"Domain (\d): ([\d,]+) lines", self.structure_text
            )
        }
        self.assertEqual(set(stated_counts), set(DOMAIN_FILES))
        for domain_number, stated in stated_counts.items():
            actual = _line_count(DOMAIN_FILES[domain_number])
            with self.subTest(domain=domain_number):
                self.assertEqual(
                    stated,
                    actual,
                    f"DOCUMENTATION_STRUCTURE.md states {stated} lines for "
                    f"domain {domain_number}, but the file actually has "
                    f"{actual} lines",
                )


class TestDocumentationStructureCrossDomainMaterials(unittest.TestCase):
    """cross-domain-scenario-questions.md must be documented alongside the
    repo's other cross-domain support materials."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def test_cross_domain_scenario_questions_mentioned(self):
        self.assertIn(
            "cross-domain-scenario-questions.md",
            self.structure_text,
            "DOCUMENTATION_STRUCTURE.md does not mention "
            "cross-domain-scenario-questions.md",
        )

    def test_cross_domain_support_files_all_exist(self):
        # Sanity check the fixture list itself stays valid.
        for filename in CROSS_DOMAIN_SUPPORT_FILES:
            with self.subTest(filename=filename):
                self.assertTrue((DOCS_DIR / filename).is_file())

    def test_cross_domain_scenario_questions_listed_with_siblings(self):
        """The entry describing cross-domain-scenario-questions.md should
        sit alongside mentions of the repo's other cross-domain support
        files, not stand alone."""
        idx = self.structure_text.find("cross-domain-scenario-questions.md")
        self.assertNotEqual(idx, -1)
        # Look at the surrounding paragraph (a generous window) for the
        # other known cross-domain support filenames.
        window = self.structure_text[max(0, idx - 500) : idx + 1000]
        siblings = [
            f
            for f in CROSS_DOMAIN_SUPPORT_FILES
            if f != "cross-domain-scenario-questions.md"
        ]
        mentioned = [f for f in siblings if f in window]
        self.assertGreaterEqual(
            len(mentioned),
            3,
            "expected cross-domain-scenario-questions.md's entry in "
            "DOCUMENTATION_STRUCTURE.md to be near mentions of the other "
            f"cross-domain support materials, found only {mentioned}",
        )


class TestDocumentationStructureDomain5Accuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously described Domain 5 as lacking
    a test file, multiple-response questions, and a worked example section,
    and described every domain's diagrams as ASCII art. All four claims are
    now false -- these tests guard against the doc drifting back to them."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.domain_5_text = DOMAIN_FILES[5].read_text(encoding="utf-8")

    def test_domain_5_test_file_exists(self):
        test_file = REPO_ROOT / "tests" / "test_domain_5_study_guide.py"
        self.assertTrue(
            test_file.is_file(),
            "tests/test_domain_5_study_guide.py should exist",
        )

    def test_structure_doc_does_not_claim_domain_5_lacks_a_test_file(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("domain 5 has no", lowered)
        self.assertNotIn("d5 lacks test file", lowered)
        self.assertNotIn("test_domain_5_study_guide.py` is missing", lowered)
        self.assertNotIn("test_domain_5_study_guide.py` file; domains 1", lowered)

    def test_structure_doc_documents_validation_tests_for_all_five_domains(self):
        self.assertIn(
            "`tests/test_domain_N_study_guide.py` for all five domains",
            self.structure_text,
        )

    def test_domain_5_has_multiple_response_questions(self):
        self.assertEqual(
            self.domain_5_text.count("(Multiple response — select TWO)"),
            2,
            "expected exactly 2 multiple-response questions (Q3 and Q14) "
            "in the Domain 5 guide",
        )

    def test_structure_doc_documents_domain_5_multiple_response_questions(self):
        self.assertIn("multiple-response", self.structure_text.lower())
        self.assertIn("Domain 5", self.structure_text)
        # The sentence documenting this fact should reference Domain 5.
        idx = self.structure_text.lower().find("multiple-response")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[max(0, idx - 200) : idx + 200]
        self.assertIn("Domain 5", window)

    def test_domain_5_has_worked_example_section(self):
        self.assertIn(
            "## Worked example: securing and governing a HIPAA-regulated "
            "Bedrock application",
            self.domain_5_text,
        )

    def test_structure_doc_documents_domain_5_worked_example(self):
        self.assertIn("Worked example", self.structure_text)
        idx = self.structure_text.find("Worked examples")
        self.assertNotEqual(
            idx, -1, "expected a 'Worked examples' entry in DOCUMENTATION_STRUCTURE.md"
        )
        window = self.structure_text[idx : idx + 500]
        self.assertIn("D5", window)

    def test_structure_doc_describes_flowcharts_as_mermaid_not_ascii(self):
        diagrams_idx = self.structure_text.find("**Diagrams:**")
        self.assertNotEqual(diagrams_idx, -1)
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 800]
        self.assertIn("Mermaid flowchart", diagrams_section)
        self.assertIn("19", diagrams_section)


class TestDocumentationStructureDomain4Accuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously claimed Domain 4 has no
    worked-example section and that only Domains 1-3 and 5 have one, and
    that all five domains use a uniform 15-20 practice question count.
    Domain 4 actually has a worked example ("## Worked example: auditing
    and documenting a responsible e-commerce recommendation engine") and
    Domain 5 actually has 26 practice questions, not 15-20. These tests
    guard against the doc drifting back to those stale claims."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.domain_4_text = DOMAIN_FILES[4].read_text(encoding="utf-8")
        cls.domain_5_text = DOMAIN_FILES[5].read_text(encoding="utf-8")

    def test_domain_4_has_worked_example_section(self):
        self.assertIn(
            "## Worked example: auditing and documenting a responsible "
            "e-commerce recommendation engine",
            self.domain_4_text,
        )

    def test_structure_doc_does_not_claim_domain_4_lacks_a_worked_example(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("domain 4 has no worked-example section", lowered)

    def test_structure_doc_documents_domain_4_worked_example(self):
        idx = self.structure_text.find("Worked examples")
        self.assertNotEqual(
            idx, -1, "expected a 'Worked examples' entry in DOCUMENTATION_STRUCTURE.md"
        )
        window = self.structure_text[idx : idx + 500]
        self.assertIn("Domains 1, 2, 3, 4, and 5", window)
        self.assertIn("D4", window)

    def test_domain_5_actual_practice_question_count(self):
        questions_section_match = re.search(
            r"\n## Practice questions(.*?)\n## Answer key",
            self.domain_5_text,
            re.DOTALL,
        )
        self.assertIsNotNone(questions_section_match)
        numbers = re.findall(
            r"(?m)^(\d+)\.\s", questions_section_match.group(1)
        )
        self.assertEqual(
            len(numbers),
            26,
            "expected Domain 5 to currently have 26 practice questions",
        )

    def test_structure_doc_documents_domain_5s_26_practice_questions(self):
        self.assertIn("26", self.structure_text)
        idx = self.structure_text.find("15–20 per domain")
        self.assertNotEqual(
            idx,
            -1,
            "expected DOCUMENTATION_STRUCTURE.md to describe the 15-20 "
            "per-domain practice question norm",
        )
        window = self.structure_text[idx : idx + 200]
        self.assertIn("26", window)
        self.assertIn("Domain 5", window)


class TestDocumentationStructureCrossDomainMaterialsAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously claimed cross-domain materials
    (concept map, mock exam, case study, master glossary/AWS service index,
    breadcrumb navigation) were missing or gapped. All of these now exist
    and are well-integrated; these tests guard against the doc drifting
    back to describing that stale, earlier snapshot."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def test_all_cross_domain_support_files_exist_on_disk(self):
        # cross-domain-scenario-questions.md, cross-domain-concept-map.md,
        # case-study-ai-system-lifecycle.md, full-length-mock-exam.md,
        # master-glossary.md, and aws-service-index.md all ship today.
        for filename in (
            "cross-domain-concept-map.md",
            "full-length-mock-exam.md",
            "case-study-ai-system-lifecycle.md",
            "cross-domain-scenario-questions.md",
            "master-glossary.md",
            "GLOSSARY.md",
            "aws-service-index.md",
        ):
            with self.subTest(filename=filename):
                self.assertTrue(
                    (DOCS_DIR / filename).is_file(),
                    f"expected {filename} to exist in docs/",
                )

    def test_does_not_claim_no_integrated_concept_map(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("no integrated concept map", lowered)

    def test_does_not_claim_no_mock_exam(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("no mock exam", lowered)
        self.assertNotIn("no exam preparation guide", lowered)

    def test_does_not_claim_no_case_study(self):
        lowered = self.structure_text.lower()
        self.assertNotIn(
            "no deep end-to-end case study showing a single company",
            lowered,
        )

    def test_does_not_claim_no_breadcrumb_navigation(self):
        lowered = self.structure_text.lower()
        self.assertNotIn('no breadcrumb or "previous/next" navigation', lowered)
        self.assertNotIn("no breadcrumb or", lowered)

    def test_does_not_claim_no_master_glossary_or_service_index(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("no master glossary index", lowered)
        self.assertNotIn("no aws service index", lowered)

    def test_does_not_claim_no_table_of_contents_in_domain_files(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("no table of contents within each", lowered)

    def test_does_not_claim_no_exam_strategy_guidance(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("no exam strategy or time-management guidance", lowered)

    def test_mentions_mock_exam_with_question_count(self):
        self.assertIn("full-length-mock-exam.md", self.structure_text)
        idx = self.structure_text.find("full-length-mock-exam.md")
        window = self.structure_text[idx : idx + 300]
        self.assertIn("65", window)

    def test_mentions_case_study_file(self):
        self.assertIn("case-study-ai-system-lifecycle.md", self.structure_text)

    def test_mentions_master_glossary_and_service_index(self):
        self.assertIn("master-glossary.md", self.structure_text)
        self.assertIn("aws-service-index.md", self.structure_text)

    def test_navigation_section_documents_breadcrumbs(self):
        nav_idx = self.structure_text.find("## Navigation")
        self.assertNotEqual(nav_idx, -1)
        nav_section = self.structure_text[nav_idx : nav_idx + 1500]
        self.assertIn("breadcrumb", nav_section.lower())

    def test_all_five_domain_guides_actually_have_breadcrumb_navigation(self):
        # Guards the underlying fact the doc now asserts: every domain
        # guide opens with a prev/next breadcrumb line.
        for domain_number, path in DOMAIN_FILES.items():
            text = path.read_text(encoding="utf-8")
            with self.subTest(domain=domain_number):
                self.assertRegex(
                    text,
                    re.compile(r"^\[← .*Domain \d of 5", re.MULTILINE),
                    f"domain {domain_number} guide ({path.name}) is missing "
                    "its breadcrumb navigation line",
                )


class TestDocumentationStructureDiagramMiniQuizServiceIndexAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously stated 13 total Mermaid
    diagrams (actually 16, with Domain 2 having four and Domain 3 having
    five rather than three), didn't state the actual subsection mini-quiz
    total (31),
    and didn't describe aws-service-index.md's actual letter-section
    coverage (A, C, G, I, M, P, S). These tests derive the true figures
    directly from the domain guides / index file and assert
    DOCUMENTATION_STRUCTURE.md matches them, guarding against the doc
    drifting stale again."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def test_stated_total_diagram_count_matches_actual_mermaid_diagrams(self):
        actual_total = 0
        for path in DOMAIN_FILES.values():
            text = path.read_text(encoding="utf-8")
            actual_total += len(re.findall(r"```mermaid", text))
        self.assertEqual(
            actual_total,
            23,
            "sanity check: expected 23 total Mermaid diagrams across the "
            "five domain guides",
        )
        diagrams_idx = self.structure_text.find("**Diagrams:**")
        self.assertNotEqual(diagrams_idx, -1)
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 800]
        self.assertIn(
            f"All {actual_total} flowchart-style diagrams",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md's stated total diagram count does "
            "not match the actual number of ```mermaid blocks across the "
            "domain guides",
        )
        self.assertNotIn(
            "not among the 13 flowcharts",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md still references the stale "
            "13-diagram count",
        )

    def test_stated_per_domain_diagram_counts_match_actual(self):
        expected_words = {1: "six", 2: "four", 3: "seven", 4: "three", 5: "three"}
        diagrams_idx = self.structure_text.find("**Diagrams:**")
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 800]
        for domain_number, path in DOMAIN_FILES.items():
            text = path.read_text(encoding="utf-8")
            actual_count = len(re.findall(r"```mermaid", text))
            expected_word = expected_words[domain_number]
            word_to_count = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7}
            with self.subTest(domain=domain_number):
                self.assertEqual(
                    actual_count,
                    word_to_count[expected_word],
                    f"sanity check failed for domain {domain_number}'s "
                    "actual Mermaid diagram count",
                )
                self.assertIn(f"Domain {domain_number} has {expected_word}", diagrams_section)

    def test_stated_mini_quiz_total_matches_actual(self):
        # Counts every "Mini-quiz" heading regardless of level: Domain 3's
        # Section 1 checkpoint predates the "#### Mini-quiz: Test your
        # understanding of ..." convention adopted for the other seven and
        # is still a level-3 "### Mini-quiz: check your understanding
        # (Section 1)" heading, so a count restricted to "####" headings
        # undercounts Domain 3 by one.
        actual_total = 0
        for path in DOMAIN_FILES.values():
            text = path.read_text(encoding="utf-8")
            actual_total += len(re.findall(r"^#{3,4} Mini-quiz:", text, re.M))
        self.assertEqual(
            actual_total,
            32,
            "sanity check: expected 32 total subsection mini-quizzes "
            "across the five domain guides",
        )
        self.assertIn(
            f"mini quizzes ({actual_total} in total",
            self.structure_text,
            "DOCUMENTATION_STRUCTURE.md does not state the actual total "
            "subsection mini-quiz count",
        )
        self.assertNotIn("31 in total", self.structure_text)

    def test_stated_service_index_letter_sections_match_actual(self):
        service_index_path = DOCS_DIR / "aws-service-index.md"
        text = service_index_path.read_text(encoding="utf-8")
        actual_letters = re.findall(r"(?m)^## ([A-Z])$", text)
        self.assertEqual(
            actual_letters,
            ["A", "C", "G", "I", "M", "P", "S"],
            "sanity check: expected aws-service-index.md's actual letter "
            "sections to be A, C, G, I, M, P, S",
        )
        idx = self.structure_text.find("**`aws-service-index.md`**")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[idx : idx + 400]
        letters_match = re.search(r"letter sections ([A-Z](?:, [A-Z])*, and [A-Z])", window)
        self.assertIsNotNone(
            letters_match,
            "expected DOCUMENTATION_STRUCTURE.md's aws-service-index.md "
            "entry to spell out its actual letter sections",
        )
        stated_letters = re.findall(r"[A-Z]", letters_match.group(1))
        self.assertEqual(stated_letters, actual_letters)
        self.assertNotIn("only sections A, G, I, P", window)

    def test_does_not_falsely_claim_services_are_missing_from_service_index(self):
        """DOCUMENTATION_STRUCTURE.md must never claim that Amazon API
        Gateway, Amazon Bedrock Prompt Management/Flows, Amazon MSK, or
        Amazon SageMaker Autopilot/Model Monitor/RL lack standalone
        aws-service-index.md entries -- they are all indexed (also guarded
        by tests/test_aws_service_index.py's
        REQUIRED_SEVEN_MISSING_SERVICES). This locks in that the doc
        doesn't regress back to that false claim."""
        seven_services = [
            "Amazon API Gateway",
            "Amazon Bedrock Prompt Management",
            "Amazon Bedrock Prompt Flows",
            "Amazon MSK",
            "Amazon SageMaker Autopilot",
            "Amazon SageMaker Model Monitor",
            "Amazon SageMaker RL",
        ]
        service_index_path = DOCS_DIR / "aws-service-index.md"
        service_index_text = service_index_path.read_text(encoding="utf-8")
        for service in seven_services:
            with self.subTest(service=service):
                self.assertIn(
                    service,
                    service_index_text,
                    f"{service!r} must have a standalone entry in "
                    "aws-service-index.md",
                )
        self.assertNotIn("CRITICAL COMPLETENESS ISSUE", self.structure_text)
        lowered = self.structure_text.lower()
        self.assertNotIn("lack standalone entries", lowered)
        self.assertNotIn("actively-referenced services", lowered)


class TestDocumentationStructureLastVerifiedAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md's 'Content health' section must not claim
    domain guides are missing a freshness/version-date stamp now that all
    five carry a '**Last verified:**' line (see
    tests/test_domain_last_verified_date.py, which locks that invariant at
    the domain-guide level)."""

    LAST_VERIFIED_RE = re.compile(r"\*\*Last verified:\*\*\s*\d{4}-\d{2}-\d{2}")

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def test_all_domain_guides_actually_have_a_last_verified_stamp(self):
        # Sanity check the underlying fact before asserting the doc
        # reflects it.
        for domain_number, path in DOMAIN_FILES.items():
            with self.subTest(domain=domain_number):
                text = path.read_text(encoding="utf-8")
                self.assertRegex(
                    text,
                    self.LAST_VERIFIED_RE,
                    f"domain {domain_number} guide is missing a "
                    "'**Last verified:** YYYY-MM-DD' line",
                )

    def test_structure_doc_notes_domain_guides_carry_last_verified_stamps(self):
        health_idx = self.structure_text.find("## Content health")
        self.assertNotEqual(health_idx, -1)
        health_section = self.structure_text[health_idx : health_idx + 1200]
        self.assertIn(
            "Last verified",
            health_section,
            "DOCUMENTATION_STRUCTURE.md's Content health section does not "
            "mention that domain guides carry a 'Last verified' stamp",
        )

    def test_structure_doc_does_not_claim_guides_lack_a_date_stamp(self):
        lowered = self.structure_text.lower()
        for phrase in (
            "missing a version-date",
            "lack a version-date",
            "lack version-date",
            "missing a last verified",
            "lacks a last verified",
            "no version-date stamp",
            "don't carry a version-date",
            "do not carry a version-date",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, lowered)


class TestDocumentationStructureScenarioQuestionCountAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md states the cross-domain scenario question
    count twice (once in the repo-layout tree, once in the cross-domain
    support document list) and README.md states it a third time. A past
    incident let README.md's count (12) drift out of sync with the actual,
    larger question count (22) that DOCUMENTATION_STRUCTURE.md already
    correctly reflected -- which could mislead a future contributor into
    "fixing" DOCUMENTATION_STRUCTURE.md (or cross-domain-scenario-
    questions.md) to match README.md's stale figure instead of the other
    way around. These tests pin all three stated counts to the actual
    number of practice questions in cross-domain-scenario-questions.md so
    they can't silently drift apart again."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.readme_text = README_PATH.read_text(encoding="utf-8")
        cls.scenario_questions_text = SCENARIO_QUESTIONS_DOC.read_text(
            encoding="utf-8"
        )

    def _actual_question_count(self):
        match = re.search(
            r"\n## Practice questions(.*?)\n## Answer key",
            self.scenario_questions_text,
            re.DOTALL,
        )
        self.assertIsNotNone(
            match,
            "expected a '## Practice questions' ... '## Answer key' "
            "section in cross-domain-scenario-questions.md",
        )
        return len(re.findall(r"(?m)^(\d+)\.\s", match.group(1)))

    def test_stated_tree_count_matches_actual(self):
        actual = self._actual_question_count()
        self.assertIn(
            f"cross-domain-scenario-questions.md      {actual} questions "
            "spanning 2+ domains",
            self.structure_text,
            "DOCUMENTATION_STRUCTURE.md's repo-layout tree states a "
            "cross-domain-scenario-questions.md question count that does "
            f"not match the actual count ({actual})",
        )

    def test_stated_prose_count_matches_actual(self):
        actual = self._actual_question_count()
        idx = self.structure_text.find("`cross-domain-scenario-questions.md`")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[idx : idx + 200]
        self.assertIn(
            f"{actual} scenario questions",
            window,
            "DOCUMENTATION_STRUCTURE.md's cross-domain support document "
            "entry states a scenario question count that does not match "
            f"the actual count ({actual})",
        )

    def test_readme_stated_count_matches_actual(self):
        actual = self._actual_question_count()
        count_match = re.search(
            r"for (\d+) scenario questions", self.readme_text
        )
        self.assertIsNotNone(
            count_match,
            "README.md should state how many scenario questions "
            "cross-domain-scenario-questions.md has",
        )
        self.assertEqual(
            int(count_match.group(1)),
            actual,
            "README.md's stated scenario question count does not match "
            f"the actual count ({actual}) in "
            "cross-domain-scenario-questions.md",
        )


if __name__ == "__main__":
    unittest.main()
