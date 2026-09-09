"""Validation for the Domain 4 Fast Track / Ultra Fast Learn coverage
verification report.

The gap this covers: Domain 4's Fast Track and Ultra Fast Learn materials
carry an explicit coverage guarantee (docs/DOCUMENTATION_STRUCTURE.md:
"every testable concept the full domain guide covers is retained somewhere
in the condensed layer") that had never been technically verified against
the source guide. `docs/domain-4-fast-track/COVERAGE-VERIFICATION-REPORT.md`
is that verification: a section-by-section spot-check confirming the Fast
Track retains almost everything from the full guide (one narrow exception,
since backfilled: the Amazon A2I "worker task template" term), and
identifying that the further-condensed Ultra Fast Learn cram sheet drops
four concept groups the Fast Track retains -- Guardrails'
word/sensitive-information filters, Amazon A2I's routing mechanics, the
Model Card vs. AI Service Card distinction, and the entire "Legal and
ethical considerations" category.

These tests assert the report exists, links back to the files it audits
with resolving anchors, and that its central claims still hold against the
live files: the hop-1 gap topic is present in the full guide and has now
been backfilled into the Fast Track (but is still absent from Ultra Fast
Learn), and the hop-2 gap topics are present in the full guide and the
Fast Track (hop 1 is otherwise clean) but absent from Ultra Fast Learn
(hop 2 has the gap) -- so these tests would start failing, as a useful
signal, the day someone backfills Ultra Fast Learn too and the report's
"still open" claims go stale.

Run with:
    python3 -m unittest tests/test_domain_4_coverage_verification_report.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
REPORT_PATH = DOCS_DIR / "domain-4-fast-track" / "COVERAGE-VERIFICATION-REPORT.md"
FAST_TRACK_PATH = DOCS_DIR / "domain-4-fast-track" / "README.md"
ULTRA_FAST_LEARN_PATH = DOCS_DIR / "domain-4-fast-track" / "ULTRA-FAST-LEARN.md"
SOURCE_PATH = DOCS_DIR / "domain-4-guidelines-for-responsible-ai.md"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")

# The four concept groups the report identifies as retained in the Fast
# Track but missing from Ultra Fast Learn (hop 2: Fast Track -> Ultra Fast
# Learn). Each is a list of keywords that must ALL appear together for
# that concept to count as "covered".
HOP2_GAP_TOPICS = {
    "guardrails word / sensitive-information filters": [
        "word filters",
        "sensitive information filters",
    ],
    "amazon a2i routing mechanics": [
        "StartHumanLoop",
        "private workforce",
    ],
    "model card vs ai service card distinction": [
        "you fill it in",
        "self-authored",
    ],
    "legal and ethical considerations": [
        "indemnification",
        "Carbon Footprint",
    ],
}

# The one item the report identifies as dropped even at hop 1 (full guide
# -> Fast Track): the Amazon A2I "worker task template" building block.
# The full guide wraps this phrase across a line break, so it is matched
# with a whitespace-tolerant regex rather than a plain substring.
HOP1_GAP_PATTERN = re.compile(r"worker task\s+template")


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


class TestReportExists(unittest.TestCase):
    def test_report_file_exists(self):
        self.assertTrue(
            REPORT_PATH.is_file(),
            "expected docs/domain-4-fast-track/COVERAGE-VERIFICATION-REPORT.md "
            "to exist",
        )

    def test_audited_files_exist(self):
        for path in (FAST_TRACK_PATH, ULTRA_FAST_LEARN_PATH, SOURCE_PATH):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())


class TestReportStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(REPORT_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(
            self.text.startswith(
                "# Domain 4 Fast Track / Ultra Fast Learn: coverage "
                "verification report"
            )
        )

    def test_states_it_is_an_audit_not_new_content(self):
        self.assertIn("not new content authoring", self.text)

    def test_quotes_the_coverage_guarantee_under_test(self):
        self.assertIn("every testable concept", self.text)

    def test_lists_sections_spot_checked(self):
        self.assertIn("## Sections spot-checked", self.text)
        # At least four full-guide sections named, per the task's "2-3
        # major sections" ask -- this report checked four.
        for fragment in (
            "Core dimensions of responsible AI",
            "Identifying bias and fairness issues",
            "AWS tools for responsible AI",
            "Legal and ethical considerations",
        ):
            with self.subTest(section=fragment):
                self.assertIn(fragment, self.text)

    def test_names_the_hop1_gap(self):
        self.assertIn("worker task template", self.text)


class TestReportLinksResolve(unittest.TestCase):
    """Every internal link out of the report must resolve to a real file
    and, if anchored, a real heading in that file."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(REPORT_PATH)
        all_links = MD_LINK_RE.findall(cls.text)
        cls.links = [
            link
            for link in all_links
            if not link.startswith(("http://", "https://"))
        ]
        cls.anchor_cache = {}

    def _resolve_target_path(self, file_part):
        if file_part == "":
            return REPORT_PATH
        return (REPORT_PATH.parent / file_part).resolve()

    def test_has_several_internal_links(self):
        self.assertGreaterEqual(len(self.links), 5)

    def test_every_internal_link_target_file_exists(self):
        for link in self.links:
            file_part = link.split("#", 1)[0]
            with self.subTest(link=link):
                target_path = self._resolve_target_path(file_part)
                self.assertTrue(
                    target_path.is_file(),
                    f"linked file does not exist: {file_part!r} (resolved "
                    f"to {target_path}) in the coverage verification report",
                )

    def test_every_internal_anchor_matches_a_real_heading(self):
        for link in self.links:
            if "#" not in link:
                continue
            file_part, anchor = link.split("#", 1)
            if not anchor:
                continue
            with self.subTest(link=link):
                target_path = self._resolve_target_path(file_part)
                cache_key = str(target_path)
                if cache_key not in self.anchor_cache:
                    self.anchor_cache[cache_key] = _heading_anchors(
                        _read(target_path)
                    )
                self.assertIn(
                    anchor,
                    self.anchor_cache[cache_key],
                    f"anchor #{anchor} does not match any heading slug in "
                    f"{target_path} -- the link {link!r} in the coverage "
                    "verification report is stale",
                )


class TestReportedHop2GapTopicsAreDocumented(unittest.TestCase):
    """The report's central hop-2 finding is that four concept groups are
    named in the report itself with enough specificity to identify them."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(REPORT_PATH)

    def test_report_names_each_gap_topic_and_its_keywords(self):
        for topic, keywords in HOP2_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertIn(
                        keyword,
                        self.text,
                        f"report does not mention {keyword!r} while "
                        f"discussing the {topic} gap",
                    )


class TestHop2GapTopicsPresentInSourceAndFastTrack(unittest.TestCase):
    """Hop 1 (full guide -> Fast Track) is reported clean for these four
    topics: every hop-2 gap-topic keyword must actually appear in both the
    full guide and the Fast Track, or the report's "verified clean" claim
    for that hop is wrong."""

    @classmethod
    def setUpClass(cls):
        cls.source_text = _read(SOURCE_PATH)
        cls.fast_track_text = _read(FAST_TRACK_PATH)

    def test_source_guide_contains_every_gap_topic_keyword(self):
        for topic, keywords in HOP2_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertIn(keyword, self.source_text)

    def test_fast_track_contains_every_gap_topic_keyword(self):
        for topic, keywords in HOP2_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertIn(keyword, self.fast_track_text)


class TestHop2GapTopicsAbsentFromUltraFastLearn(unittest.TestCase):
    """Hop 2 (Fast Track -> Ultra Fast Learn) is reported to have a real
    gap: none of the four topics' keywords should appear in Ultra Fast
    Learn today. If this test starts failing, the gap has been backfilled
    and COVERAGE-VERIFICATION-REPORT.md's "Recommendation" section (and
    this test) should be updated to reflect that, rather than silently
    left describing a stale problem."""

    @classmethod
    def setUpClass(cls):
        cls.ultra_text = _read(ULTRA_FAST_LEARN_PATH)

    def test_ultra_fast_learn_is_missing_every_gap_topic_keyword(self):
        for topic, keywords in HOP2_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertNotIn(
                        keyword,
                        self.ultra_text,
                        f"expected {keyword!r} (part of the {topic} gap) to "
                        "still be absent from ULTRA-FAST-LEARN.md -- if it "
                        "has been added, the coverage gap this report "
                        "documents has been closed and the report/tests "
                        "should be updated to match",
                    )


class TestHop1GapTopicNowFixedInFastTrack(unittest.TestCase):
    """The one hop-1 finding: the Amazon A2I "worker task template" term
    was present in the full guide but absent from both the Fast Track and
    Ultra Fast Learn. That gap has since been backfilled into the Fast
    Track (README.md Section 3's condensed A2I worked-example pattern), so
    the term must now appear in the full guide and the Fast Track alike.
    Ultra Fast Learn is a separate, still-open hop-2 gap and should
    continue to omit it until that follow-up work happens."""

    @classmethod
    def setUpClass(cls):
        cls.source_text = _read(SOURCE_PATH)
        cls.fast_track_text = _read(FAST_TRACK_PATH)
        cls.ultra_text = _read(ULTRA_FAST_LEARN_PATH)

    def test_source_guide_contains_worker_task_template(self):
        self.assertRegex(self.source_text, HOP1_GAP_PATTERN)

    def test_fast_track_now_contains_worker_task_template(self):
        self.assertRegex(self.fast_track_text, HOP1_GAP_PATTERN)

    def test_ultra_fast_learn_is_missing_worker_task_template(self):
        self.assertNotRegex(self.ultra_text, HOP1_GAP_PATTERN)


if __name__ == "__main__":
    unittest.main()
