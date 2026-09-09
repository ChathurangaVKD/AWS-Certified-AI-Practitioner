"""Verify docs/exam-preparation-strategy.md's three study plans (4-week,
2-week, 1-week) integrate the Fast Track and Ultra Fast Learn condensed
guides, not just the full domain guides.

Before this change, none of the three study plans (lines 457-512)
mentioned "Fast Track" or "Ultra Fast Learn" anywhere, even though the
1-week plan explicitly targets learners with "general AI/ML/cloud
familiarity" -- precisely the audience the ~40%-length Fast Track guides
and ~15%-length Ultra Fast Learn cram sheets are designed for. This test
locks in that:

* the 4-week plan notes Fast Track can substitute for full-guide
  re-reading once a domain feels solid;
* the 2-week plan recommends Fast Track as a time-saving alternative for
  learners with prior exposure;
* the 1-week plan recommends Fast Track guides as the primary material
  for all five domains, with Ultra Fast Learn cram sheets for final
  review;
* every one of those three revisions restates the coverage guarantee
  (every testable concept retained, only narrative explanation and
  redundant examples trimmed) so learners trust the substitution;
* every domain's Fast Track README.md and ULTRA-FAST-LEARN.md is linked
  directly, for all five domains.

Run with:
    python3 -m unittest tests/test_exam_preparation_strategy_fast_track_integration.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "exam-preparation-strategy.md"

COVERAGE_GUARANTEE_RE = re.compile(
    r"every\s+testable\s+concept", re.IGNORECASE
)


def _read(path):
    return path.read_text(encoding="utf-8")


class TestFastTrackIntegrationBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        four_week_start = cls.text.index("### 4-week plan")
        two_week_start = cls.text.index("### 2-week plan")
        one_week_start = cls.text.index("### 1-week plan")
        section_6_start = cls.text.index("## 6. Topic-based review quick reference")
        cls.four_week_text = cls.text[four_week_start:two_week_start]
        cls.two_week_text = cls.text[two_week_start:one_week_start]
        cls.one_week_text = cls.text[one_week_start:section_6_start]


class TestFourWeekPlanFastTrackNote(TestFastTrackIntegrationBase):
    def test_mentions_fast_track(self):
        self.assertIn("Fast Track", self.four_week_text)

    def test_states_coverage_guarantee(self):
        self.assertRegex(self.four_week_text, COVERAGE_GUARANTEE_RE)

    def test_frames_as_substitute_for_later_weeks_once_solid(self):
        # The note should be scoped to "later" study once material already
        # feels solid, not a blanket recommendation to skip full guides
        # entirely.
        self.assertRegex(
            self.four_week_text,
            re.compile(r"solid", re.IGNORECASE),
        )

    def test_links_all_five_domain_fast_track_readmes(self):
        for domain in range(1, 6):
            with self.subTest(domain=domain):
                self.assertIn(
                    f"domain-{domain}-fast-track/README.md",
                    self.four_week_text,
                )


class TestTwoWeekPlanFastTrackNote(TestFastTrackIntegrationBase):
    def test_mentions_fast_track(self):
        self.assertIn("Fast Track", self.two_week_text)

    def test_states_coverage_guarantee(self):
        self.assertRegex(self.two_week_text, COVERAGE_GUARANTEE_RE)

    def test_frames_as_time_saving_alternative_for_prior_exposure(self):
        self.assertRegex(
            self.two_week_text,
            re.compile(r"prior exposure", re.IGNORECASE),
        )

    def test_links_all_five_domain_fast_track_readmes(self):
        for domain in range(1, 6):
            with self.subTest(domain=domain):
                self.assertIn(
                    f"domain-{domain}-fast-track/README.md",
                    self.two_week_text,
                )


class TestOneWeekPlanFastTrackPrimary(TestFastTrackIntegrationBase):
    def test_mentions_fast_track(self):
        self.assertIn("Fast Track", self.one_week_text)

    def test_mentions_ultra_fast_learn(self):
        self.assertIn("Ultra Fast Learn", self.one_week_text)

    def test_states_coverage_guarantee(self):
        self.assertRegex(self.one_week_text, COVERAGE_GUARANTEE_RE)

    def test_links_all_five_domain_fast_track_readmes(self):
        for domain in range(1, 6):
            with self.subTest(domain=domain):
                self.assertIn(
                    f"domain-{domain}-fast-track/README.md",
                    self.one_week_text,
                )

    def test_links_all_five_domain_ultra_fast_learn_cram_sheets(self):
        for domain in range(1, 6):
            with self.subTest(domain=domain):
                self.assertIn(
                    f"domain-{domain}-fast-track/ULTRA-FAST-LEARN.md",
                    self.one_week_text,
                )

    def test_day_table_recommends_fast_track_for_all_five_domains(self):
        # The Day 1-4 table rows are the primary study material for this
        # plan's target audience -- each of the five domains' Fast Track
        # guide should appear inside the markdown table itself, not just
        # in the surrounding prose.
        table_start = self.one_week_text.index("| Day | Focus |")
        table_text = self.one_week_text[table_start:]
        for domain in range(1, 6):
            with self.subTest(domain=domain):
                self.assertIn(
                    f"[Domain {domain} Fast Track](domain-{domain}-fast-track/README.md)",
                    table_text,
                )

    def test_day_table_recommends_ultra_fast_learn_for_final_review(self):
        table_start = self.one_week_text.index("| Day | Focus |")
        table_text = self.one_week_text[table_start:]
        self.assertIn("Ultra Fast Learn", table_text)


class TestFastTrackLinksResolveToRealFiles(unittest.TestCase):
    """Every Fast Track README.md and ULTRA-FAST-LEARN.md linked from the
    three study plans must exist on disk, for all five domains."""

    def test_all_fast_track_readmes_exist(self):
        for domain in range(1, 6):
            with self.subTest(domain=domain):
                path = DOCS_DIR / f"domain-{domain}-fast-track" / "README.md"
                self.assertTrue(path.is_file(), f"missing {path}")

    def test_all_ultra_fast_learn_files_exist(self):
        for domain in range(1, 6):
            with self.subTest(domain=domain):
                path = DOCS_DIR / f"domain-{domain}-fast-track" / "ULTRA-FAST-LEARN.md"
                self.assertTrue(path.is_file(), f"missing {path}")


if __name__ == "__main__":
    unittest.main()
