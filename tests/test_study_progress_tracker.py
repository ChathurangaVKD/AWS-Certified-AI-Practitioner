"""Structural validation for docs/study-progress-tracker.md.

The gap this covers: the series has 324 total self-assessment items (129
domain practice questions + 35 embedded mini-quizzes + 30 cross-domain
scenario questions + 130 mock-exam questions across two 65-question mock
exams) but, before this file
existed, no structured place to log scores across multiple attempts or
notice a recurring weak domain. This test asserts the tracker:

  * exists and is reachable from README.md,
  * ships its attempt-log table with column headers only (no fabricated
    sample scores in the actual template table learners are meant to
    copy),
  * documents all required columns (exam/quiz set, date, correct count,
    percentage score, domain breakdown, weak-area notes, time spent),
  * includes instructions for filling it in,
  * includes a worked example of using recurring weak areas to target
    reinforcement study, anchored on the exam's 700/1000 passing score,
  * includes guidance on interpreting score trends across attempts, and
  * every markdown link it makes into another doc resolves to a real file
    and (if it has an anchor) a real heading in that file, so a future
    heading rename doesn't silently break the pointer.

Mirrors the conventions established in tests/test_exam_preparation_strategy.py.

Run with:
    python3 -m unittest tests/test_study_progress_tracker.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "study-progress-tracker.md"
README_PATH = REPO_ROOT / "README.md"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")

REQUIRED_TEMPLATE_COLUMNS = [
    "Attempt #",
    "Assessment / question set",
    "Date",
    "# Correct",
    "# Total",
    "% Score",
    "Domain breakdown",
    "Time spent",
    "Weak-area notes",
]


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


class TestStudyProgressTrackerExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected a study progress tracker at {DOC_PATH}",
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/study-progress-tracker.md",
            readme_text,
            "README.md must link to the study progress tracker so learners "
            "can discover it",
        )

    def test_linked_from_exam_preparation_strategy(self):
        exam_prep_text = _read(DOCS_DIR / "exam-preparation-strategy.md")
        self.assertIn(
            "study-progress-tracker.md",
            exam_prep_text,
            "exam-preparation-strategy.md should point readers at the "
            "progress tracker once they start taking practice assessments",
        )


class TestAttemptLogTemplate(unittest.TestCase):
    """The template table in Section 1 must ship blank -- headers only,
    no fabricated sample scores -- since it's meant to be copied and
    filled in with the learner's own real attempts."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def _template_section(self):
        start = self.text.find("## 1. Attempt log template")
        self.assertNotEqual(start, -1, "expected a '## 1. Attempt log template' section")
        end = self.text.find("\n## 2.", start)
        self.assertNotEqual(end, -1, "expected a '## 2.' section following the template")
        return self.text[start:end]

    def test_required_columns_present(self):
        section = self._template_section()
        header_line = next(
            line for line in section.splitlines() if line.strip().startswith("|")
        )
        for column in REQUIRED_TEMPLATE_COLUMNS:
            self.assertIn(
                column,
                header_line,
                f"attempt log template header is missing the '{column}' column",
            )

    def test_template_table_has_no_data_rows(self):
        """Only a header row and a markdown separator row (---) should be
        present under the template heading -- any additional row with
        digits in it would be a fabricated sample score."""
        section = self._template_section()
        table_lines = [line for line in section.splitlines() if line.strip().startswith("|")]
        self.assertGreaterEqual(
            len(table_lines), 2, "expected at least a header row and a separator row"
        )
        header, separator, *body_rows = table_lines
        self.assertRegex(
            separator,
            r"^\|[\s:|-]+\|$",
            "second table row must be a markdown header separator, not data",
        )
        for row in body_rows:
            self.assertFalse(
                re.search(r"\d", row),
                f"template table row contains digits, which look like a "
                f"fabricated sample score: {row!r}",
            )


class TestRequiredContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def test_mentions_all_assessment_item_types(self):
        for phrase in [
            "129",
            "35",
            "30",
            "65",
            "324",
        ]:
            self.assertIn(
                phrase,
                self.text,
                f"expected the tracker to reference the '{phrase}' item count "
                "from the assessment inventory",
            )

    def test_has_fill_in_instructions(self):
        self.assertIn("How to fill this in", self.text)

    def test_has_worked_example_of_targeting_recurring_weak_areas(self):
        self.assertIn("## 2. Example", self.text)
        self.assertIn("two consecutive attempts", self.text)
        self.assertIn("700/1000", self.text)

    def test_worked_example_references_real_domain_3_sections(self):
        domain3_text = _read(DOCS_DIR / "domain-3-applications-of-foundation-models.md")
        domain3_anchors = _heading_anchors(domain3_text)
        self.assertIn(
            "4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering",
            domain3_anchors,
        )
        self.assertIn("5-amazon-bedrock-features", domain3_anchors)
        self.assertIn(
            "domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering",
            self.text,
        )
        self.assertIn(
            "domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features",
            self.text,
        )

    def test_has_score_trend_interpretation_guidance(self):
        self.assertIn(
            "## 4. Interpreting score trends across attempts", self.text
        )


class TestInternalLinksResolve(unittest.TestCase):
    """Every markdown link the tracker makes to another file in this repo
    must resolve to a real file, and if it carries an anchor, to a real
    heading in that file."""

    def test_all_links_resolve(self):
        text = _read(DOC_PATH)
        broken = []
        for match in MD_LINK_RE.finditer(text):
            target = match.group("target")
            if target.startswith(("http://", "https://", "#")):
                continue
            file_part, _, anchor = target.partition("#")
            target_path = (DOCS_DIR / file_part).resolve()
            if not target_path.is_file():
                broken.append(f"missing file: {target}")
                continue
            if anchor:
                anchors = _heading_anchors(_read(target_path))
                if anchor not in anchors:
                    broken.append(f"missing anchor '{anchor}' in {file_part}")
        self.assertEqual(broken, [], f"broken internal links: {broken}")


if __name__ == "__main__":
    unittest.main()
