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
MOCK_EXAM_DOC = DOCS_DIR / "full-length-mock-exam.md"
SECOND_MOCK_EXAM_DOC = DOCS_DIR / "mock-exam.md"

DOMAIN_FILES = {
    1: DOCS_DIR / "domain-1-fundamentals-of-ai-and-ml.md",
    2: DOCS_DIR / "domain-2-fundamentals-of-generative-ai.md",
    3: DOCS_DIR / "domain-3-applications-of-foundation-models.md",
    4: DOCS_DIR / "domain-4-guidelines-for-responsible-ai.md",
    5: DOCS_DIR / "domain-5-security-compliance-governance.md",
}

MASTER_GLOSSARY_DOC = DOCS_DIR / "master-glossary.md"
GLOSSARY_DOC = DOCS_DIR / "GLOSSARY.md"
SERVICE_INDEX_DOC = DOCS_DIR / "aws-service-index.md"
STUDY_PROGRESS_TRACKER_DOC = DOCS_DIR / "study-progress-tracker.md"

# The Fast Track condensed-guide layer: 15 files across five
# domain-N-fast-track/ directories. Domains 1, 2, and 4 each pair a single
# README.md with an ULTRA-FAST-LEARN.md cram sheet; Domains 3 and 5 split
# their condensed guide content into multiple numbered parts (plus their
# own ULTRA-FAST-LEARN.md), but each still has its own README.md acting as
# a landing page for that split rather than holding the guide itself.
FAST_TRACK_FILES_BY_DOMAIN = {
    1: [
        DOCS_DIR / "domain-1-fast-track" / "README.md",
        DOCS_DIR / "domain-1-fast-track" / "ULTRA-FAST-LEARN.md",
    ],
    2: [
        DOCS_DIR / "domain-2-fast-track" / "README.md",
        DOCS_DIR / "domain-2-fast-track" / "ULTRA-FAST-LEARN.md",
    ],
    3: [
        DOCS_DIR / "domain-3-fast-track" / "README.md",
        DOCS_DIR
        / "domain-3-fast-track"
        / "part-1-application-design-and-customization.md",
        DOCS_DIR / "domain-3-fast-track" / "part-2-inference-and-multimodal.md",
        DOCS_DIR
        / "domain-3-fast-track"
        / "part-3-deployment-and-troubleshooting.md",
        DOCS_DIR / "domain-3-fast-track" / "ULTRA-FAST-LEARN.md",
    ],
    4: [
        DOCS_DIR / "domain-4-fast-track" / "README.md",
        DOCS_DIR / "domain-4-fast-track" / "ULTRA-FAST-LEARN.md",
    ],
    5: [
        DOCS_DIR / "domain-5-fast-track" / "README.md",
        DOCS_DIR / "domain-5-fast-track" / "part-1-security-and-compliance.md",
        DOCS_DIR / "domain-5-fast-track" / "part-2-governance-and-monitoring.md",
        DOCS_DIR / "domain-5-fast-track" / "ULTRA-FAST-LEARN.md",
    ],
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


class TestDocumentationStructureCrossDomainLineCounts(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md's "Complete file inventory" section states
    a combined line count for the ten cross-domain support documents and a
    grand total across all seventeen tracked Markdown files. Both figures
    must match the files' actual current line counts so they don't silently
    drift stale as the cross-domain documents grow (as previously happened:
    the section once stated 5,931 lines for the ten cross-domain documents
    when they actually totaled 5,413)."""

    CROSS_DOMAIN_LINE_COUNT_FILES = [
        "aws-service-index.md",
        "aws-service-decision-guide.md",
        "cross-domain-concept-map.md",
        "cross-domain-scenario-questions.md",
        "case-study-ai-system-lifecycle.md",
        "exam-preparation-strategy.md",
        "full-length-mock-exam.md",
        "mock-exam.md",
        "master-glossary.md",
        "GLOSSARY.md",
    ]

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.normalized_text = re.sub(r"\s+", " ", cls.structure_text)

    def test_stated_per_file_cross_domain_line_counts_match_actual(self):
        for filename in self.CROSS_DOMAIN_LINE_COUNT_FILES:
            actual = _line_count(DOCS_DIR / filename)
            formatted = f"{actual:,}"
            match = re.search(
                r"`" + re.escape(filename) + r"`:\s*([\d,]+)",
                self.normalized_text,
            )
            with self.subTest(filename=filename):
                self.assertIsNotNone(
                    match,
                    "DOCUMENTATION_STRUCTURE.md does not state a per-file "
                    f"line count for {filename} in the cross-domain support "
                    "documents breakdown",
                )
                stated = int(match.group(1).replace(",", ""))
                self.assertEqual(
                    stated,
                    actual,
                    f"DOCUMENTATION_STRUCTURE.md states {stated} lines for "
                    f"{filename}, but it actually has {actual} ({formatted}) "
                    "lines",
                )

    def test_stated_cross_domain_support_total_matches_actual(self):
        match = re.search(
            r"ten cross-domain support documents listed above total "
            r"\*\*([\d,]+) lines\*\*",
            self.normalized_text,
        )
        self.assertIsNotNone(
            match,
            "expected DOCUMENTATION_STRUCTURE.md to state a combined line "
            "count for the ten cross-domain support documents",
        )
        stated = int(match.group(1).replace(",", ""))
        actual = sum(
            _line_count(DOCS_DIR / name)
            for name in self.CROSS_DOMAIN_LINE_COUNT_FILES
        )
        self.assertEqual(
            stated,
            actual,
            f"DOCUMENTATION_STRUCTURE.md states the ten cross-domain "
            f"support documents total {stated} lines, but they actually "
            f"total {actual} lines",
        )

    def test_stated_grand_total_matches_actual_files(self):
        totals_stated = re.findall(
            r"total \*\*([\d,]+) lines\*\*", self.normalized_text
        )
        self.assertEqual(
            len(totals_stated),
            2,
            "expected exactly two stated line-count totals in the "
            "'Complete file inventory' section (the ten cross-domain "
            f"documents, then the thirty-file grand total), found "
            f"{len(totals_stated)}",
        )
        grand_stated = int(totals_stated[-1].replace(",", ""))
        fast_track_files = [
            path
            for paths in FAST_TRACK_FILES_BY_DOMAIN.values()
            for path in paths
        ]
        all_files = (
            [README_PATH]
            + list(DOMAIN_FILES.values())
            + fast_track_files
            + [DOCS_DIR / name for name in self.CROSS_DOMAIN_LINE_COUNT_FILES]
            + [STUDY_PROGRESS_TRACKER_DOC]
            + [STRUCTURE_DOC]
        )
        self.assertEqual(len(all_files), 33, "expected exactly 33 tracked files")
        grand_actual = sum(_line_count(path) for path in all_files)
        self.assertEqual(
            grand_stated,
            grand_actual,
            "DOCUMENTATION_STRUCTURE.md states the thirty-three tracked "
            f"files total {grand_stated} lines, but they actually total "
            f"{grand_actual} lines",
        )


class TestDocumentationStructureFastTrackSection(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md must document the Fast Track /
    Ultra Fast Learn condensed-guide layer: 15 files across five
    domain-N-fast-track/ directories (including the Domain 3 and Domain 5
    README.md landing pages), previously omitted entirely even though the
    files exist in the repo (a content-completeness gap in the structure
    doc itself)."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.normalized_text = re.sub(r"\s+", " ", cls.structure_text)

    def test_fast_track_files_all_exist(self):
        # Sanity check the fixture list itself stays valid.
        for domain_number, paths in FAST_TRACK_FILES_BY_DOMAIN.items():
            for path in paths:
                with self.subTest(domain=domain_number, path=path.name):
                    self.assertTrue(path.is_file(), f"{path} does not exist")

    def test_fast_track_section_heading_present(self):
        self.assertIn(
            "## Fast Track condensed guides (15 files, 7,464 lines total)",
            self.structure_text,
            "DOCUMENTATION_STRUCTURE.md is missing the 'Fast Track "
            "condensed guides' section documenting the 15-file, "
            "domain-N-fast-track/ condensed-guide layer",
        )

    def test_three_tier_structure_documented(self):
        for term in ("Full guide", "Fast Track", "Ultra Fast Learn"):
            with self.subTest(term=term):
                self.assertIn(term, self.structure_text)

    def test_domain_3_and_5_part_split_documented(self):
        for fragment in (
            "part-1-application-design-and-customization.md",
            "part-2-inference-and-multimodal.md",
            "part-3-deployment-and-troubleshooting.md",
            "part-1-security-and-compliance.md",
            "part-2-governance-and-monitoring.md",
            "Both domains still have a `README.md` in their",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.structure_text)

    def test_domain_3_and_5_readme_landing_pages_documented(self):
        # Domain 3 and Domain 5 each have their own README.md landing page
        # (88 and 81 lines respectively) explaining the split-part
        # structure -- this must not be described as absent.
        self.assertNotIn(
            "Neither Domain 3 nor Domain 5 has a single",
            self.structure_text,
            "DOCUMENTATION_STRUCTURE.md still claims Domain 3/5 lack a "
            "README.md Fast Track file, but both have one "
            "(domain-3-fast-track/README.md, domain-5-fast-track/README.md)",
        )
        domain_3_readme = DOCS_DIR / "domain-3-fast-track" / "README.md"
        domain_5_readme = DOCS_DIR / "domain-5-fast-track" / "README.md"
        self.assertTrue(domain_3_readme.is_file())
        self.assertTrue(domain_5_readme.is_file())
        domain_3_lines = _line_count(domain_3_readme)
        domain_5_lines = _line_count(domain_5_readme)
        self.assertIn(
            f"{domain_3_lines} lines for Domain 3, {domain_5_lines} for",
            self.normalized_text,
            "DOCUMENTATION_STRUCTURE.md does not state the actual line "
            f"counts of the Domain 3 ({domain_3_lines}) and Domain 5 "
            f"({domain_5_lines}) Fast Track README.md landing pages",
        )

    def test_coverage_guarantee_documented(self):
        self.assertIn("coverage guarantee", self.structure_text)
        self.assertIn("every testable concept", self.structure_text)

    def test_stated_fast_track_per_domain_line_counts_match_actual(self):
        expected = {1: 975, 2: 1135, 3: 2909, 4: 954, 5: 1491}
        for domain_number, paths in FAST_TRACK_FILES_BY_DOMAIN.items():
            actual = sum(_line_count(path) for path in paths)
            with self.subTest(domain=domain_number):
                self.assertEqual(
                    actual,
                    expected[domain_number],
                    f"Domain {domain_number}'s Fast Track files actually "
                    f"total {actual} lines, not the {expected[domain_number]} "
                    "this test (and the structure doc) expect",
                )
                formatted = f"{actual:,}"
                self.assertIn(
                    f"Domain {domain_number} Fast Track: {formatted} lines",
                    self.structure_text,
                    "DOCUMENTATION_STRUCTURE.md does not state the "
                    f"current Fast Track line count ({formatted}) for "
                    f"domain {domain_number}",
                )

    def test_stated_fast_track_total_matches_actual(self):
        fast_track_files = [
            path
            for paths in FAST_TRACK_FILES_BY_DOMAIN.values()
            for path in paths
        ]
        actual_total = sum(_line_count(path) for path in fast_track_files)
        formatted = f"{actual_total:,}"
        self.assertEqual(len(fast_track_files), 15)
        self.assertIn(
            f"Fast Track condensed guides (15 files, {formatted} lines total)",
            self.structure_text,
        )
        self.assertIn(f"**{formatted} lines**", self.structure_text)


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
        self.assertIn("35", diagrams_section)


class TestDocumentationStructureDomain4Accuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously claimed Domain 4 has no
    worked-example section and that only Domains 1-3 and 5 have one, and
    that all five domains use a uniform 15-20 practice question count.
    Domain 4 actually has a worked example ("## Worked example: auditing
    and documenting a responsible e-commerce recommendation engine") and
    Domain 5 actually has 29 practice questions, not 15-20. These tests
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
            29,
            "expected Domain 5 to currently have 29 practice questions",
        )

    def test_structure_doc_documents_domain_5s_29_practice_questions(self):
        self.assertIn("29", self.structure_text)
        idx = self.structure_text.find("15–20 per domain")
        self.assertNotEqual(
            idx,
            -1,
            "expected DOCUMENTATION_STRUCTURE.md to describe the 15-20 "
            "per-domain practice question norm",
        )
        window = self.structure_text[idx : idx + 200]
        self.assertIn("29", window)
        self.assertIn("Domain 5", window)


class TestDocumentationStructureWorkedExampleGrandTotalAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously described the five domain
    guides as marking "20+ worked-example sections in total", with no
    per-domain breakdown. That vague figure undercounted reality (31
    worked-example headings total: 2+4+10+6+9 across Domains 1-5) and gave
    no way to check it against the domain guides directly. These tests
    derive the true per-domain and grand-total counts from every "##"/
    "###"/"####" level "Worked example[s]" heading in each domain guide and
    assert DOCUMENTATION_STRUCTURE.md's "Worked examples" paragraph states
    them exactly, guarding against the doc drifting back to vague or
    stale language."""

    EXPECTED_PER_DOMAIN = {1: 3, 2: 5, 3: 18, 4: 8, 5: 13}

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    @staticmethod
    def _worked_example_heading_count(text):
        return len(re.findall(r"(?m)^#{2,4} Worked examples?:", text))

    def test_per_domain_worked_example_heading_counts_match_expected(self):
        for domain_number, path in DOMAIN_FILES.items():
            text = path.read_text(encoding="utf-8")
            actual = self._worked_example_heading_count(text)
            with self.subTest(domain=domain_number):
                self.assertEqual(
                    actual,
                    self.EXPECTED_PER_DOMAIN[domain_number],
                    f"sanity check: expected domain {domain_number}'s guide "
                    f"({path.name}) to have "
                    f"{self.EXPECTED_PER_DOMAIN[domain_number]} "
                    "'Worked example' headings (any of '##', '###', or "
                    f"'####' level), found {actual}",
                )

    def test_grand_total_worked_example_count_is_46(self):
        actual_total = sum(
            self._worked_example_heading_count(path.read_text(encoding="utf-8"))
            for path in DOMAIN_FILES.values()
        )
        self.assertEqual(
            actual_total,
            47,
            "sanity check: expected 47 total 'Worked example' headings "
            "across the five domain guides",
        )

    def test_structure_doc_states_45_worked_examples_with_per_domain_breakdown(self):
        anchor = "worked-example sections in total"
        idx = self.structure_text.find(anchor)
        self.assertNotEqual(
            idx,
            -1,
            "expected a 'worked-example sections in total' summary in "
            "DOCUMENTATION_STRUCTURE.md",
        )
        window = self.structure_text[max(0, idx - 50) : idx + 300]
        self.assertIn(
            "47",
            window,
            "DOCUMENTATION_STRUCTURE.md does not state the 47-worked-example "
            "grand total",
        )
        for domain_number, count in self.EXPECTED_PER_DOMAIN.items():
            with self.subTest(domain=domain_number):
                self.assertRegex(
                    window,
                    re.compile(rf"{count} in\s+Domain {domain_number}"),
                    "DOCUMENTATION_STRUCTURE.md does not state the "
                    f"per-domain worked-example breakdown for Domain "
                    f"{domain_number} ({count})",
                )

    def test_structure_doc_no_longer_uses_vague_worked_example_count(self):
        self.assertNotIn(
            "20+",
            self.structure_text,
            "DOCUMENTATION_STRUCTURE.md still uses vague '20+' "
            "worked-example language instead of the exact 30-count "
            "breakdown",
        )


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


class TestDocumentationStructureGlossaryEntryCountAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md's cross-domain support document entry for
    master-glossary.md and GLOSSARY.md states an exact entry count for the
    shared, merged term set. Both files must actually carry that many
    top-level `- **Term**` entries, so the stated figure can't silently
    drift stale as terms are added or removed."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.master_glossary_text = MASTER_GLOSSARY_DOC.read_text(encoding="utf-8")
        cls.glossary_text = GLOSSARY_DOC.read_text(encoding="utf-8")

    @staticmethod
    def _entry_count(text):
        return len(re.findall(r"(?m)^- \*\*", text))

    def test_master_glossary_and_glossary_have_the_same_entry_count(self):
        # Sanity check: both files are meant to be two views of the same
        # merged term set, so they should carry the same number of entries.
        self.assertEqual(
            self._entry_count(self.master_glossary_text),
            self._entry_count(self.glossary_text),
            "master-glossary.md and GLOSSARY.md are expected to carry the "
            "same number of entries (two views of the same merged term set)",
        )

    def test_stated_glossary_entry_count_matches_actual(self):
        actual = self._entry_count(self.master_glossary_text)
        idx = self.structure_text.find("**`master-glossary.md`**")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[idx : idx + 400]
        self.assertIn(
            f"**{actual} entries**",
            window,
            "DOCUMENTATION_STRUCTURE.md's master-glossary.md/GLOSSARY.md "
            f"entry does not state the actual glossary entry count ({actual})",
        )

    def test_no_stale_glossary_entry_count(self):
        idx = self.structure_text.find("**`master-glossary.md`**")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[idx : idx + 400]
        stale_counts = re.findall(r"\*\*(\d+) entries\*\*", window)
        actual = self._entry_count(self.master_glossary_text)
        for stale_count in stale_counts:
            with self.subTest(stated=stale_count):
                self.assertEqual(int(stale_count), actual)


class TestDocumentationStructureServiceIndexCountAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md's cross-domain support document entry for
    aws-service-index.md states an exact count of indexed AWS services.
    docs/aws-service-index.md must actually carry that many top-level
    `- **Service**` entries, so the stated figure can't silently drift
    stale as services are added or removed."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.service_index_text = SERVICE_INDEX_DOC.read_text(encoding="utf-8")

    @staticmethod
    def _entry_count(text):
        return len(re.findall(r"(?m)^- \*\*", text))

    def test_stated_service_count_matches_actual(self):
        actual = self._entry_count(self.service_index_text)
        idx = self.structure_text.find("**`aws-service-index.md`**")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[idx : idx + 400]
        self.assertIn(
            f"**{actual} services**",
            window,
            "DOCUMENTATION_STRUCTURE.md's aws-service-index.md entry does "
            f"not state the actual service count ({actual})",
        )

    def test_no_stale_service_count(self):
        idx = self.structure_text.find("**`aws-service-index.md`**")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[idx : idx + 400]
        stale_counts = re.findall(r"\*\*(\d+) services\*\*", window)
        actual = self._entry_count(self.service_index_text)
        for stale_count in stale_counts:
            with self.subTest(stated=stale_count):
                self.assertEqual(int(stale_count), actual)


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
            35,
            "sanity check: expected 35 total Mermaid diagrams across the "
            "five domain guides",
        )
        diagrams_idx = self.structure_text.find("**Diagrams:**")
        self.assertNotEqual(diagrams_idx, -1)
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 800]
        self.assertIn(
            f"{actual_total} Mermaid flowchart diagrams",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md's stated domain-guide diagram "
            "count does not match the actual number of ```mermaid blocks "
            "across the domain guides",
        )
        self.assertNotIn(
            "not among the 13 flowcharts",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md still references the stale "
            "13-diagram count",
        )
        self.assertNotIn(
            "All 24 flowchart-style diagrams",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md still references the stale "
            "24-diagram count",
        )

    def test_stated_grand_total_diagram_count_includes_cross_domain_and_ascii(self):
        # The domain guides' 35 Mermaid diagrams are not the whole picture:
        # cross-domain-concept-map.md's "Visual overview" section has one
        # more Mermaid diagram, and aws-service-decision-guide.md's Section
        # 4.1 Bedrock model family selection flow and Section 6 cost-control
        # decision flow add two more still (38 Mermaid diagrams
        # total), and three of the domain guides also carry a plain-text
        # ASCII rendering of a diagram that already exists as Mermaid
        # (Domain 1's ML lifecycle, Domain 5's data-governance lifecycle
        # diagram, and Domain 5's shared-responsibility model), for 41
        # diagrams overall. DOCUMENTATION_STRUCTURE.md previously undercounted
        # this (stating "All 24 flowchart-style diagrams") and omitted the
        # cross-domain diagrams and the ASCII diagrams entirely.
        domain_mermaid_total = sum(
            len(re.findall(r"```mermaid", path.read_text(encoding="utf-8")))
            for path in DOMAIN_FILES.values()
        )
        concept_map_path = DOCS_DIR / "cross-domain-concept-map.md"
        concept_map_mermaid_total = len(
            re.findall(r"```mermaid", concept_map_path.read_text(encoding="utf-8"))
        )
        self.assertEqual(
            concept_map_mermaid_total,
            1,
            "sanity check: expected exactly one Mermaid diagram in "
            "cross-domain-concept-map.md's Visual overview section",
        )
        decision_guide_path = DOCS_DIR / "aws-service-decision-guide.md"
        decision_guide_mermaid_total = len(
            re.findall(r"```mermaid", decision_guide_path.read_text(encoding="utf-8"))
        )
        self.assertEqual(
            decision_guide_mermaid_total,
            2,
            "sanity check: expected exactly two Mermaid diagrams in "
            "aws-service-decision-guide.md (Section 4.1's Bedrock model "
            "family selection flow and Section 6's cost-control flow)",
        )
        grand_mermaid_total = (
            domain_mermaid_total
            + concept_map_mermaid_total
            + decision_guide_mermaid_total
        )
        self.assertEqual(grand_mermaid_total, 38)
        ascii_diagram_count = 3
        grand_total = grand_mermaid_total + ascii_diagram_count
        self.assertEqual(grand_total, 41)

        diagrams_idx = self.structure_text.find("**Diagrams:**")
        self.assertNotEqual(diagrams_idx, -1)
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 2000]
        self.assertIn(
            "cross-domain-concept-map.md",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md's diagram count does not mention "
            "cross-domain-concept-map.md's additional Mermaid diagram",
        )
        self.assertIn(
            "aws-service-decision-guide.md",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md's diagram count does not mention "
            "aws-service-decision-guide.md's additional Mermaid diagram",
        )
        self.assertIn(
            f"{grand_mermaid_total} Mermaid diagrams",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md does not state the 38-diagram "
            "Mermaid total once cross-domain-concept-map.md and "
            "aws-service-decision-guide.md are included",
        )
        self.assertIn(
            "3 ASCII diagrams",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md does not call out the 3 ASCII "
            "diagrams (Domain 1's ML lifecycle, Domain 5's data-governance "
            "lifecycle diagram, Domain 5's shared responsibility model)",
        )
        self.assertIn(
            f"{grand_total} total diagrams",
            diagrams_section,
            "DOCUMENTATION_STRUCTURE.md does not state the 41-diagram "
            "grand total (38 Mermaid + 3 ASCII)",
        )

    def test_stated_per_domain_diagram_counts_match_actual(self):
        expected_words = {1: "seven", 2: "five", 3: "fourteen", 4: "four", 5: "five"}
        diagrams_idx = self.structure_text.find("**Diagrams:**")
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 800]
        for domain_number, path in DOMAIN_FILES.items():
            text = path.read_text(encoding="utf-8")
            actual_count = len(re.findall(r"```mermaid", text))
            expected_word = expected_words[domain_number]
            word_to_count = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14}
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
            35,
            "sanity check: expected 35 total subsection mini-quizzes "
            "across the five domain guides",
        )
        self.assertIn(
            f"mini quizzes ({actual_total} in total",
            self.structure_text,
            "DOCUMENTATION_STRUCTURE.md does not state the actual total "
            "subsection mini-quiz count",
        )
        self.assertNotIn("31 in total", self.structure_text)
        self.assertNotIn("32 in total", self.structure_text)

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


class TestDocumentationStructureQuestionTotalsAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously stated 101 total domain
    practice questions and 188 total questions overall (101 domain + 65
    mock + 22 scenario). The five domain guides actually carry 117 practice
    questions in total (24 for Domain 1, 24 for Domain 2, 20 each for
    Domains 3-4, 29 for Domain 5), which combined with the 65-question mock
    exam and the 22 cross-domain scenario questions comes to 204 total
    questions. These tests derive the true figures directly from the
    source files and assert DOCUMENTATION_STRUCTURE.md matches them,
    guarding against the doc drifting stale again."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    @staticmethod
    def _count_numbered_questions(text, start_heading, end_heading):
        match = re.search(
            rf"\n{re.escape(start_heading)}(.*?)\n{re.escape(end_heading)}",
            text,
            re.DOTALL,
        )
        assert match is not None, (
            f"expected a {start_heading!r} ... {end_heading!r} section"
        )
        return len(re.findall(r"(?m)^(\d+)\.\s", match.group(1)))

    def _actual_domain_question_total(self):
        total = 0
        for path in DOMAIN_FILES.values():
            text = path.read_text(encoding="utf-8")
            total += self._count_numbered_questions(
                text, "## Practice questions", "## Answer key"
            )
        return total

    def _actual_mock_exam_question_total(self):
        full_length_text = MOCK_EXAM_DOC.read_text(encoding="utf-8")
        full_length_count = self._count_numbered_questions(
            full_length_text,
            "## Mock exam questions (1–65)",
            "## 3. Scoring your mock exam",
        )
        second_text = SECOND_MOCK_EXAM_DOC.read_text(encoding="utf-8")
        second_count = self._count_numbered_questions(
            second_text,
            "## Mock exam questions",
            "## Answer key and explanations",
        )
        # full-length-mock-exam.md and mock-exam.md are two separate,
        # independent 65-question mock exams (130 combined); both count
        # toward the repository's total self-assessment items.
        return full_length_count + second_count

    def _actual_scenario_question_total(self):
        text = SCENARIO_QUESTIONS_DOC.read_text(encoding="utf-8")
        return self._count_numbered_questions(
            text, "## Practice questions", "## Answer key"
        )

    @staticmethod
    def _actual_mini_quiz_total():
        total = 0
        for path in DOMAIN_FILES.values():
            text = path.read_text(encoding="utf-8")
            total += len(re.findall(r"^#{3,4} Mini-quiz:", text, re.M))
        return total

    def test_actual_domain_question_total_is_117(self):
        self.assertEqual(
            self._actual_domain_question_total(),
            117,
            "sanity check: expected 117 practice questions across the "
            "five domain guides (24 for Domain 1, 24 for Domain 2, 20 "
            "each for Domains 3-4, 29 for Domain 5)",
        )

    def test_actual_grand_total_is_204(self):
        grand_total = (
            self._actual_domain_question_total()
            + self._actual_mock_exam_question_total()
            + self._actual_scenario_question_total()
        )
        self.assertEqual(
            grand_total,
            204,
            "sanity check: expected 117 domain + 65 mock-exam + 22 "
            "scenario questions to sum to 204",
        )

    def test_structure_doc_states_106_domain_practice_questions(self):
        actual = self._actual_domain_question_total()
        idx = self.structure_text.find("15–20 per domain")
        self.assertNotEqual(
            idx,
            -1,
            "expected DOCUMENTATION_STRUCTURE.md to describe the "
            "per-domain practice question norm",
        )
        window = self.structure_text[idx : idx + 300]
        self.assertIn(
            f"{actual} domain practice questions in total",
            window,
            "DOCUMENTATION_STRUCTURE.md's domain-guide description does "
            f"not state the actual domain practice question total ({actual})",
        )

    def test_structure_doc_test_coverage_paragraph_states_106_total(self):
        actual = self._actual_domain_question_total()
        idx = self.structure_text.find("**Test coverage:**")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[idx : idx + 400]
        self.assertIn(
            f"**{actual} total**",
            window,
            "DOCUMENTATION_STRUCTURE.md's 'Test coverage' paragraph does "
            f"not state the actual domain practice question total ({actual})",
        )

    def test_structure_doc_states_total_assessment_line(self):
        domain_total = self._actual_domain_question_total()
        mock_total = self._actual_mock_exam_question_total()
        scenario_total = self._actual_scenario_question_total()
        mini_quiz_total = self._actual_mini_quiz_total()
        grand_total = domain_total + mock_total + scenario_total + mini_quiz_total
        idx = self.structure_text.find("**Total assessment:**")
        self.assertNotEqual(
            idx,
            -1,
            "expected a '**Total assessment:**' line in "
            "DOCUMENTATION_STRUCTURE.md",
        )
        window = self.structure_text[idx : idx + 300]
        self.assertIn(f"{domain_total} domain practice questions", window)
        self.assertIn(f"{mock_total} mock-exam questions", window)
        self.assertIn(f"{scenario_total} scenario questions", window)
        self.assertIn(f"{mini_quiz_total} embedded mini-quiz questions", window)
        self.assertIn(f"{grand_total}", window)
        self.assertIn("total self-assessment items", window)

    def test_structure_doc_does_not_state_stale_101_or_188_counts(self):
        self.assertNotIn("101 domain practice questions", self.structure_text)
        self.assertNotIn("188 questions", self.structure_text)
        self.assertNotIn("188 total questions", self.structure_text)


class TestDocumentationStructureDomain2Domain4Domain5LineCounts(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md previously stated stale per-domain line
    counts for Domain 2 (1,986), Domain 4 (1,879), and Domain 5 (2,162)
    that no longer matched the actual, larger current line counts of those
    guides (1,993 / 1,905 / 2,305 respectively) after later commits added
    content to them. These tests pin the stated Domain 2/4/5 line counts to
    the files' actual current line counts so the two can't silently drift
    apart again."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def test_domain_2_domain_4_domain_5_line_counts_are_current(self):
        for domain_number in (2, 4, 5):
            actual = _line_count(DOMAIN_FILES[domain_number])
            formatted = f"{actual:,}"
            with self.subTest(domain=domain_number):
                self.assertIn(
                    f"Domain {domain_number}: {formatted} lines",
                    self.structure_text,
                    f"DOCUMENTATION_STRUCTURE.md does not state the "
                    f"current line count ({formatted}) for domain "
                    f"{domain_number}'s guide",
                )

    def test_no_stale_domain_2_domain_4_domain_5_line_counts_linger(self):
        stale_counts = {2: "1,986 lines", 4: "1,879 lines", 5: "2,162 lines"}
        for domain_number, stale in stale_counts.items():
            with self.subTest(domain=domain_number):
                self.assertNotIn(
                    f"Domain {domain_number}: {stale}",
                    self.structure_text,
                    f"DOCUMENTATION_STRUCTURE.md still states the stale "
                    f"Domain {domain_number} line count ({stale})",
                )


class TestDocumentationStructureDiagramCountRestored(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md's "**Diagrams:**" paragraph, which states
    the total number of Mermaid flowchart diagrams across the domain guides
    and the two cross-domain documents that also carry one (
    cross-domain-concept-map.md's "Visual overview" section and
    aws-service-decision-guide.md's Section 4.1 and Section 6 decision
    flows), had gone missing from the file entirely and, before that, had
    stated a stale total (37) that undercounted the actual, larger current
    total (39) once Domain 2 gained an additional diagram. These tests
    derive the true per-file and grand-total Mermaid diagram counts
    directly from the source files and assert DOCUMENTATION_STRUCTURE.md's
    "**Diagrams:**" paragraph states them, guarding against the paragraph
    drifting stale -- or disappearing -- again."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    @staticmethod
    def _mermaid_count(path):
        return len(re.findall(r"```mermaid", path.read_text(encoding="utf-8")))

    def test_domain_guide_mermaid_total_is_36(self):
        actual_total = sum(
            self._mermaid_count(path) for path in DOMAIN_FILES.values()
        )
        self.assertEqual(
            actual_total,
            36,
            "sanity check: expected 36 total Mermaid diagrams across the "
            "five domain guides",
        )

    def test_concept_map_and_decision_guide_mermaid_counts(self):
        concept_map_path = DOCS_DIR / "cross-domain-concept-map.md"
        decision_guide_path = DOCS_DIR / "aws-service-decision-guide.md"
        self.assertEqual(self._mermaid_count(concept_map_path), 2)
        self.assertEqual(self._mermaid_count(decision_guide_path), 3)

    def test_structure_doc_has_diagrams_paragraph_stating_grand_total_of_40(self):
        domain_total = sum(
            self._mermaid_count(path) for path in DOMAIN_FILES.values()
        )
        concept_map_total = self._mermaid_count(
            DOCS_DIR / "cross-domain-concept-map.md"
        )
        decision_guide_total = self._mermaid_count(
            DOCS_DIR / "aws-service-decision-guide.md"
        )
        grand_total = domain_total + concept_map_total + decision_guide_total
        self.assertEqual(grand_total, 40)

        diagrams_idx = self.structure_text.find("**Diagrams:**")
        self.assertNotEqual(
            diagrams_idx,
            -1,
            "expected a '**Diagrams:**' paragraph in "
            "DOCUMENTATION_STRUCTURE.md",
        )
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 800]
        self.assertIn(f"{domain_total} Mermaid flowchart diagrams", diagrams_section)
        self.assertIn("cross-domain-concept-map.md", diagrams_section)
        self.assertIn("aws-service-decision-guide.md", diagrams_section)
        self.assertIn(f"{grand_total} Mermaid", diagrams_section)

    def test_structure_doc_does_not_state_stale_37_or_39_diagram_total(self):
        # Note: this guards the *grand* total specifically (the bolded
        # "**N Mermaid diagrams**" figure combining the domain guides with
        # cross-domain-concept-map.md and aws-service-decision-guide.md),
        # not the unbolded per-domain-guide subtotal earlier in the same
        # paragraph -- that subtotal legitimately reads 39 once Domain 3
        # gains two more diagrams and Domain 4 gains one, coinciding with
        # (but distinct from) the old stale grand-total figure this test
        # was written to catch.
        diagrams_idx = self.structure_text.find("**Diagrams:**")
        self.assertNotEqual(diagrams_idx, -1)
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 800]
        self.assertNotIn("37 Mermaid diagrams**", diagrams_section)
        self.assertNotIn("39 Mermaid diagrams**", diagrams_section)


class TestDocumentationStructure2026ContentMetricsRefresh(unittest.TestCase):
    """A 2026-09-03 documentation scan found several of
    DOCUMENTATION_STRUCTURE.md's content metrics had drifted stale as the
    domain guides (especially Domain 3) kept growing: the domain-guide
    line-count total/breakdown (12,417 stated vs. 13,169 actual, with
    Domain 1, 3, and 4 each individually wrong), the worked-example total
    (34 stated vs. 39 actual -- Domain 3 alone has 15, not 10, once all
    seven of its "###"/"####"-level nested subsections are counted rather
    than just the BLEU/ROUGE one), the Mermaid diagram total (40 stated
    vs. 43 actual -- Domain 3 has sixteen, not fourteen, and Domain 4 has
    six, not five), and the domain practice-question total (126 stated vs.
    129 actual -- Domain 3 has 29, not 26). These tests derive the true
    figures directly from the source files and assert
    DOCUMENTATION_STRUCTURE.md states them, guarding against this refresh
    drifting stale again."""

    EXPECTED_LINE_COUNTS = {1: 2030, 2: 2213, 3: 5482, 4: 2247, 5: 2535}
    EXPECTED_WORKED_EXAMPLES = {1: 3, 2: 5, 3: 18, 4: 8, 5: 11}
    EXPECTED_MERMAID_DIAGRAMS = {1: 7, 2: 5, 3: 16, 4: 6, 5: 6}
    EXPECTED_PRACTICE_QUESTIONS = {1: 24, 2: 24, 3: 29, 4: 20, 5: 32}

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    @staticmethod
    def _mermaid_count(path):
        return len(re.findall(r"```mermaid", path.read_text(encoding="utf-8")))

    @staticmethod
    def _worked_example_heading_count(text):
        return len(re.findall(r"(?m)^#{2,4} Worked examples?:", text))

    @staticmethod
    def _practice_question_count(text):
        match = re.search(
            r"\n## Practice questions(.*?)\n## Answer key", text, re.DOTALL
        )
        assert match is not None, "expected a Practice questions section"
        return len(re.findall(r"(?m)^(\d+)\.\s", match.group(1)))

    def test_actual_domain_line_counts_match_expected(self):
        for domain_number, path in DOMAIN_FILES.items():
            with self.subTest(domain=domain_number):
                self.assertEqual(
                    _line_count(path),
                    self.EXPECTED_LINE_COUNTS[domain_number],
                    f"sanity check: domain {domain_number}'s guide "
                    f"({path.name}) line count no longer matches the "
                    "figure this refresh was based on -- re-verify and "
                    "update both the guide and this test",
                )

    def test_structure_doc_states_13298_line_total(self):
        total = sum(self.EXPECTED_LINE_COUNTS.values())
        self.assertEqual(total, 14507)
        self.assertIn(f"**{total:,} lines total**", self.structure_text)

    def test_actual_worked_example_counts_match_expected(self):
        for domain_number, path in DOMAIN_FILES.items():
            with self.subTest(domain=domain_number):
                actual = self._worked_example_heading_count(
                    path.read_text(encoding="utf-8")
                )
                self.assertEqual(
                    actual,
                    self.EXPECTED_WORKED_EXAMPLES[domain_number],
                    f"sanity check: domain {domain_number}'s guide "
                    f"({path.name}) has {actual} 'Worked example' "
                    "headings, not the figure this refresh was based on",
                )

    def test_structure_doc_states_45_worked_examples_with_domain_3_breakdown(self):
        total = sum(self.EXPECTED_WORKED_EXAMPLES.values())
        self.assertEqual(total, 46)
        anchor = "worked-example sections in total"
        idx = self.structure_text.find(anchor)
        self.assertNotEqual(idx, -1)
        window = self.structure_text[max(0, idx - 50) : idx + 300]
        self.assertIn("46", window)
        for domain_number, count in self.EXPECTED_WORKED_EXAMPLES.items():
            with self.subTest(domain=domain_number):
                self.assertRegex(
                    window,
                    re.compile(rf"{count} in\s+Domain {domain_number}"),
                    "DOCUMENTATION_STRUCTURE.md does not state the "
                    f"per-domain worked-example count for Domain "
                    f"{domain_number} ({count}) in its grand-total tally",
                )

    def test_structure_doc_domain_3_worked_example_methodology_is_8_plus_9(self):
        idx = self.structure_text.find("Worked examples")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[idx : idx + 2100]
        self.assertIn("eight standalone", window)
        self.assertIn("ten", window)
        self.assertIn("eighteen", window)
        self.assertIn("BLEU/ROUGE", window)
        self.assertIn("Cohere Rerank", window)
        self.assertIn("multimodal\nproduct-catalog RAG system", window)
        self.assertIn("multimodal financial-report RAG\npipeline", window)

    def test_structure_doc_notes_depth_gaps_now_filled(self):
        anchor = "depth gap previously flagged"
        idx = self.structure_text.find(anchor)
        self.assertNotEqual(
            idx,
            -1,
            "expected DOCUMENTATION_STRUCTURE.md to note that previously "
            "flagged depth gaps are now filled with worked examples",
        )
        window = self.structure_text[idx : idx + 700]
        for phrase in (
            "Amazon Q Business",
            "LoRA/QLoRA",
            "Kendra",
            "troubleshooting a failing RAG system",
            "Clarify",
            "Guardrails",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, window)

    def test_actual_mermaid_diagram_counts_match_expected(self):
        for domain_number, path in DOMAIN_FILES.items():
            with self.subTest(domain=domain_number):
                actual = self._mermaid_count(path)
                self.assertEqual(
                    actual,
                    self.EXPECTED_MERMAID_DIAGRAMS[domain_number],
                    f"sanity check: domain {domain_number}'s guide "
                    f"({path.name}) has {actual} Mermaid diagrams, not "
                    "the figure this refresh was based on",
                )

    def test_structure_doc_states_45_mermaid_diagram_grand_total(self):
        domain_total = sum(self.EXPECTED_MERMAID_DIAGRAMS.values())
        self.assertEqual(domain_total, 40)
        concept_map_total = self._mermaid_count(
            DOCS_DIR / "cross-domain-concept-map.md"
        )
        decision_guide_total = self._mermaid_count(
            DOCS_DIR / "aws-service-decision-guide.md"
        )
        self.assertEqual(concept_map_total, 2)
        self.assertEqual(decision_guide_total, 3)
        grand_total = domain_total + concept_map_total + decision_guide_total
        self.assertEqual(grand_total, 45)

        diagrams_idx = self.structure_text.find("**Diagrams:**")
        self.assertNotEqual(diagrams_idx, -1)
        diagrams_section = self.structure_text[diagrams_idx : diagrams_idx + 800]
        self.assertIn(f"{domain_total} Mermaid flowchart diagrams", diagrams_section)
        self.assertIn("sixteen", diagrams_section)
        self.assertIn("Domain 4 has six", diagrams_section)
        self.assertIn(f"**{grand_total} Mermaid\ndiagrams**", diagrams_section)

    def test_actual_practice_question_counts_match_expected(self):
        for domain_number, path in DOMAIN_FILES.items():
            with self.subTest(domain=domain_number):
                actual = self._practice_question_count(
                    path.read_text(encoding="utf-8")
                )
                self.assertEqual(
                    actual,
                    self.EXPECTED_PRACTICE_QUESTIONS[domain_number],
                    f"sanity check: domain {domain_number}'s guide "
                    f"({path.name}) has {actual} practice questions, not "
                    "the figure this refresh was based on",
                )

    def test_structure_doc_states_129_domain_practice_questions(self):
        total = sum(self.EXPECTED_PRACTICE_QUESTIONS.values())
        self.assertEqual(total, 129)
        self.assertIn("**29 for Domain 3**", self.structure_text)
        self.assertIn(
            f"**{total} domain practice questions in total**", self.structure_text
        )


class TestDocumentationStructureMockExamDistinctionAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md's 'Total assessment' paragraph previously
    described the second 65-question mock-exam.md as "a deliberate
    duplicate-format check rather than a distinct practice pool" -- which
    is factually wrong. full-length-mock-exam.md (question set A) and
    mock-exam.md (question set B) contain two completely different
    65-question sets, not a format-only duplicate (see
    tests/test_mock_exam.py and tests/test_full_length_mock_exam.py, which
    verify each file's own question content independently). These tests
    guard against the doc drifting back to that misleading description.

    The paragraph also previously excluded mock-exam.md's 65 questions from
    the stated grand total (259 instead of the correct 324), on the theory
    that a second, independent practice pool shouldn't count toward the
    total -- contradicting README.md and docs/study-progress-tracker.md,
    which both correctly count all 130 combined mock-exam questions toward
    324 total self-assessment items. These tests also guard against that
    exclusion note reappearing."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def test_does_not_describe_mock_exam_as_a_duplicate_format_check(self):
        lowered = self.structure_text.lower()
        self.assertNotIn("duplicate-format check", lowered)
        self.assertNotIn(
            "deliberate duplicate-format check rather than a distinct "
            "practice pool",
            lowered,
        )

    def test_describes_mock_exam_as_independent_practice_pool(self):
        idx = self.structure_text.find("independent 65-question practice pools")
        self.assertNotEqual(
            idx,
            -1,
            "expected the 'Total assessment' paragraph to describe "
            "full-length-mock-exam.md and mock-exam.md as independent "
            "65-question practice pools",
        )
        window = self.structure_text[idx : idx + 100]
        self.assertIn("completely different set of questions", window)

    def test_does_not_exclude_second_mock_exam_from_total(self):
        idx = self.structure_text.find("**Total assessment:**")
        self.assertNotEqual(idx, -1)
        window = self.structure_text[idx : idx + 400]
        self.assertNotIn("this excludes", window)
        self.assertIn("130 mock-exam questions", window)
        self.assertIn("324 total self-assessment items", window)

    def test_full_length_and_second_mock_exam_have_different_questions(self):
        # Sanity check the underlying fact the doc now asserts: the two
        # mock exams are not a format duplicate of each other.
        full_length_text = MOCK_EXAM_DOC.read_text(encoding="utf-8")
        second_mock_exam_text = (DOCS_DIR / "mock-exam.md").read_text(
            encoding="utf-8"
        )
        self.assertNotEqual(full_length_text, second_mock_exam_text)


class TestDocumentationStructureQuickReferenceCheatSheetAccuracy(
    unittest.TestCase
):
    """DOCUMENTATION_STRUCTURE.md's 'Repository layout' section previously
    never mentioned that each of the five domain guides has its own
    '## Quick-reference cheat sheet' section (a condensed, print-friendly
    recap distinct from that domain's closing worked example / practice
    questions), even though every domain guide has one and each is
    independently tested by its own
    tests/test_domain_N_quick_reference_cheat_sheet.py file. These tests
    guard the bullet documenting that gap, and pin its stated per-domain
    line numbers to each domain guide's actual current
    '## Quick-reference cheat sheet' heading line so the numbers can't
    silently drift stale as the guides grow (mirroring the pattern used
    elsewhere in this file for line counts and other figures)."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")

    def _cheat_sheet_heading_line(self, path):
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.strip() == "## Quick-reference cheat sheet":
                return line_number
        self.fail(f"{path.name} has no '## Quick-reference cheat sheet' heading")

    def test_mentions_quick_reference_cheat_sheets_bullet(self):
        self.assertIn(
            "**Quick-reference cheat sheets:**",
            self.structure_text,
            "expected DOCUMENTATION_STRUCTURE.md to document the five "
            "in-domain quick-reference cheat sheets",
        )

    def test_stated_cheat_sheet_line_numbers_match_actual_headings(self):
        for domain_number, path in DOMAIN_FILES.items():
            actual_line = self._cheat_sheet_heading_line(path)
            with self.subTest(domain=domain_number):
                self.assertIn(
                    f"Domain {domain_number}: line {actual_line}",
                    self.structure_text,
                    "DOCUMENTATION_STRUCTURE.md does not state the "
                    f"current '## Quick-reference cheat sheet' heading "
                    f"line ({actual_line}) for domain {domain_number}'s "
                    f"guide ({path.name}) -- it has gone stale or the "
                    "guide was edited without updating the recorded line",
                )

    def test_mentions_cheat_sheet_test_file_pattern(self):
        self.assertIn(
            "tests/test_domain_N_quick_reference_cheat_sheet.py",
            self.structure_text,
        )

    def test_mentions_relationship_to_ultra_fast_track_cram_sheets(self):
        self.assertIn("Ultra Fast Track", self.structure_text)
        self.assertIn(
            "docs/domain-N-fast-track/ULTRA-FAST-LEARN.md", self.structure_text
        )


class TestDocumentationStructureFastTrackDiagramTotalAccuracy(unittest.TestCase):
    """DOCUMENTATION_STRUCTURE.md's 'Diagrams' subsection previously stated
    only the 55 Mermaid diagrams in the full domain guides and cross-domain
    materials, and mentioned the 39 additional diagrams in the Fast Track
    condensed guides only as a parenthetical caveat excluded from the
    total -- leaving readers unsure whether 55 or 94 was the repo's actual
    diagram count. The 39 figure itself was also wrong: it omitted Domain
    5 part 1 (`part-1-security-and-compliance.md`), which carries 4 more
    Mermaid diagrams, so the true Fast Track subtotal is 43 and the true
    grand total is 98. These tests derive the true full-guide, cross-domain,
    and Fast Track diagram counts directly from the source files and
    assert DOCUMENTATION_STRUCTURE.md states the correct, internally
    consistent 98-diagram grand total with an itemized breakdown, so the
    count can't silently drift stale or under-report again."""

    FAST_TRACK_DIAGRAM_FILES = {
        "Domain 1": DOCS_DIR / "domain-1-fast-track" / "README.md",
        "Domain 2": DOCS_DIR / "domain-2-fast-track" / "README.md",
        "Domain 3 part 1": DOCS_DIR
        / "domain-3-fast-track"
        / "part-1-application-design-and-customization.md",
        "Domain 3 part 2": DOCS_DIR
        / "domain-3-fast-track"
        / "part-2-inference-and-multimodal.md",
        "Domain 3 part 3": DOCS_DIR
        / "domain-3-fast-track"
        / "part-3-deployment-and-troubleshooting.md",
        "Domain 4": DOCS_DIR / "domain-4-fast-track" / "README.md",
        "Domain 5 part 1": DOCS_DIR
        / "domain-5-fast-track"
        / "part-1-security-and-compliance.md",
        "Domain 5 part 2": DOCS_DIR
        / "domain-5-fast-track"
        / "part-2-governance-and-monitoring.md",
    }

    CONCEPT_MAP_DOC = DOCS_DIR / "cross-domain-concept-map.md"
    DECISION_GUIDE_DOC = DOCS_DIR / "aws-service-decision-guide.md"

    @staticmethod
    def _mermaid_count(path):
        return len(re.findall(r"```mermaid", path.read_text(encoding="utf-8")))

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        diagrams_idx = cls.structure_text.find("**Diagrams:**")
        assert diagrams_idx != -1
        cls.diagrams_section = cls.structure_text[diagrams_idx : diagrams_idx + 2000]

    def test_actual_per_domain_diagram_counts_are_7_5_25_6_7(self):
        expected = {1: 7, 2: 5, 3: 25, 4: 6, 5: 7}
        for domain_number, path in DOMAIN_FILES.items():
            with self.subTest(domain=domain_number):
                self.assertEqual(self._mermaid_count(path), expected[domain_number])

    def test_actual_cross_domain_diagram_counts_are_2_and_3(self):
        self.assertEqual(self._mermaid_count(self.CONCEPT_MAP_DOC), 2)
        self.assertEqual(self._mermaid_count(self.DECISION_GUIDE_DOC), 3)

    def test_actual_fast_track_diagram_counts_are_6_8_4_8_7_4_4_2(self):
        expected = {
            "Domain 1": 6,
            "Domain 2": 8,
            "Domain 3 part 1": 4,
            "Domain 3 part 2": 8,
            "Domain 3 part 3": 7,
            "Domain 4": 4,
            "Domain 5 part 1": 4,
            "Domain 5 part 2": 2,
        }
        for label, path in self.FAST_TRACK_DIAGRAM_FILES.items():
            with self.subTest(label=label):
                self.assertEqual(self._mermaid_count(path), expected[label])

    def test_full_guide_and_cross_domain_total_is_55(self):
        domain_total = sum(
            self._mermaid_count(path) for path in DOMAIN_FILES.values()
        )
        grand = (
            domain_total
            + self._mermaid_count(self.CONCEPT_MAP_DOC)
            + self._mermaid_count(self.DECISION_GUIDE_DOC)
        )
        self.assertEqual(grand, 55)

    def test_fast_track_total_is_43(self):
        fast_track_total = sum(
            self._mermaid_count(path)
            for path in self.FAST_TRACK_DIAGRAM_FILES.values()
        )
        self.assertEqual(fast_track_total, 43)

    def test_structure_doc_states_98_total_mermaid_diagrams(self):
        self.assertIn(
            "**98 total Mermaid diagrams**",
            self.diagrams_section,
            "DOCUMENTATION_STRUCTURE.md's Diagrams subsection does not "
            "state the full 98-diagram grand total (55 full-guide/"
            "cross-domain + 43 Fast Track)",
        )

    def test_structure_doc_states_55_and_43_component_totals(self):
        self.assertIn("**55 Mermaid diagrams**", self.diagrams_section)
        self.assertIn("**43 Fast Track diagrams**", self.diagrams_section)

    def test_structure_doc_no_longer_excludes_fast_track_from_total(self):
        lowered = self.diagrams_section.lower()
        self.assertNotIn("not counted in the 55 figure", lowered)
        self.assertNotIn(
            "additional diagrams adapted for condensed-format presentation, "
            "not counted",
            lowered,
        )

    def test_structure_doc_itemizes_fast_track_breakdown(self):
        for fragment in (
            "6 in\nDomain 1",
            "8 in\nDomain 2",
            "4 in\nDomain 3's part 1",
            "8 in\nDomain 3's part 2",
            "7 in\nDomain 3's part 3",
            "4 in\nDomain 4",
            "4 in\nDomain 5\npart 1",
            "2 in\nDomain\n5's part 2",
        ):
            normalized_section = re.sub(r"\s+", " ", self.diagrams_section)
            normalized_fragment = re.sub(r"\s+", " ", fragment)
            with self.subTest(fragment=fragment):
                self.assertIn(normalized_fragment, normalized_section)


class TestDocumentationStructureNavigationGapAccuracy(unittest.TestCase):
    """A prior scan's suggested Navigation-section gap claimed README.md
    'does NOT mention Fast Track condensed guides or Ultra Fast Learn cram
    sheets.' That claim is false -- README.md's own "Three-tier learning
    structure" section (currently around lines 21-57) already explains all
    three study tiers and links into every domain's condensed material. This
    class guards against that false claim being (re-)stated in
    DOCUMENTATION_STRUCTURE.md's Navigation section, while making sure the
    two genuinely still-open navigation gaps (domain guide introductions,
    and exam-preparation-strategy.md's study plans) stay documented."""

    @classmethod
    def setUpClass(cls):
        cls.structure_text = STRUCTURE_DOC.read_text(encoding="utf-8")
        cls.readme_text = README_PATH.read_text(encoding="utf-8")
        nav_idx = cls.structure_text.find("## Navigation")
        content_health_idx = cls.structure_text.find("## Content health")
        assert nav_idx != -1 and content_health_idx != -1 and content_health_idx > nav_idx
        cls.nav_section = cls.structure_text[nav_idx:content_health_idx]

    def test_readme_actually_has_a_three_tier_learning_structure_section(self):
        # Guards the underlying fact: README.md must actually carry the
        # section that makes the old "README doesn't mention Fast Track /
        # Ultra Fast Learn" claim false.
        self.assertIn("## Three-tier learning structure", self.readme_text)
        idx = self.readme_text.find("## Three-tier learning structure")
        window = self.readme_text[idx : idx + 2000]
        self.assertIn("Fast Track", window)
        self.assertIn("Ultra Fast Learn", window)

    def test_navigation_section_does_not_repeat_false_readme_gap_claim(self):
        lowered = self.nav_section.lower()
        self.assertNotIn(
            "does not mention fast track",
            lowered,
            "Navigation section should not claim README.md lacks Fast "
            "Track / Ultra Fast Learn coverage -- it already has a "
            "'Three-tier learning structure' section that covers this.",
        )
        self.assertNotIn("does not mention ultra fast learn", lowered)

    def test_navigation_section_credits_readme_three_tier_structure(self):
        self.assertIn("Three-tier learning structure", self.nav_section)
        self.assertIn("README.md", self.nav_section)

    def test_navigation_section_still_documents_domain_intro_gap(self):
        lowered = self.nav_section.lower()
        self.assertIn("domain guide introductions", lowered)
        self.assertIn("fast-track", lowered)

    def test_navigation_section_still_documents_exam_prep_gap(self):
        self.assertIn("exam-preparation-strategy.md", self.nav_section)
        idx = self.nav_section.find("exam-preparation-strategy.md")
        window = self.nav_section[idx : idx + 400]
        self.assertIn("study plan", window.lower())


class TestDocumentationStructureAnswerKeyHeadingConsistency(unittest.TestCase):
    """All five domain guides must use identical answer-key heading wording.

    Domain 5 previously used the bare "## Answer key" heading while
    Domains 1-4 all used "## Answer key and explanations" -- a
    naming-convention inconsistency with no content impact (Domain 5's 32
    questions already all had full explanations). This guards against that
    drift recurring for any domain guide.
    """

    EXPECTED_HEADING = "## Answer key and explanations"

    def test_every_domain_guide_uses_the_same_answer_key_heading(self):
        for domain_number, path in DOMAIN_FILES.items():
            text = path.read_text(encoding="utf-8")
            with self.subTest(domain=domain_number):
                self.assertIn(
                    self.EXPECTED_HEADING,
                    text,
                    f"domain {domain_number}'s guide ({path.name}) should "
                    f"use the heading {self.EXPECTED_HEADING!r} for its "
                    "answer key section, matching the other domain guides.",
                )
                self.assertNotIn(
                    "\n## Answer key\n",
                    text,
                    f"domain {domain_number}'s guide ({path.name}) still "
                    "has a bare '## Answer key' heading; it should be "
                    f"{self.EXPECTED_HEADING!r} for consistency with the "
                    "other domain guides.",
                )

    def test_domain_5_table_of_contents_links_to_the_renamed_heading(self):
        text = DOMAIN_FILES[5].read_text(encoding="utf-8")
        self.assertIn("[Answer key and explanations](#answer-key-and-explanations)", text)
        self.assertNotIn("[Answer key](#answer-key)", text)


if __name__ == "__main__":
    unittest.main()
