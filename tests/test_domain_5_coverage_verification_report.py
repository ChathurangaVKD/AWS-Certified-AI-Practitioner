"""Validation for the Domain 5 Fast Track / Ultra Fast Learn coverage
verification report.

The gap this covers: Domain 5's Fast Track (README.md + part-1 +
part-2) and Ultra Fast Learn materials carry an explicit coverage
guarantee (docs/DOCUMENTATION_STRUCTURE.md: "every testable concept the
full domain guide covers is retained somewhere in the condensed layer")
that had never been technically verified against the source guide.
`docs/domain-5-fast-track/COVERAGE-VERIFICATION-REPORT.md` is that
verification: a section-by-section spot-check confirming the Fast Track
retains almost everything from the full guide (four narrow exceptions:
GDPR's "right to erasure"/"data minimization", GDPR's "special category"
data classification, "SOC 2 Type II" as the specific audit type, and the
Aurora Benefits worked example's named CloudWatch metrics), and
identifying that the further-condensed Ultra Fast Learn cram sheet drops
five additional concept groups the Fast Track retains -- the "insecure
output handling" threat name, MITRE ATLAS / OWASP Top 10, Amazon Macie,
Titan Image Generator watermarking, and the Algorithmic Accountability
Act.

These tests assert the report exists, links back to the files it audits
with resolving anchors, and that its central claims still hold against
the live files: the hop-1 gap topics are present in the full guide but
absent from the entire Fast Track directory (README + part-1 + part-2)
and from Ultra Fast Learn, and the hop-2 gap topics are present in the
Fast Track (hop 1 is otherwise clean for these) but absent from Ultra
Fast Learn (hop 2 has the gap) -- so this test would start failing, as a
useful signal, the day someone backfills either file and the report's
"still open" claims go stale.

Run with:
    python3 -m unittest tests/test_domain_5_coverage_verification_report.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
REPORT_PATH = DOCS_DIR / "domain-5-fast-track" / "COVERAGE-VERIFICATION-REPORT.md"
README_PATH = DOCS_DIR / "domain-5-fast-track" / "README.md"
PART1_PATH = DOCS_DIR / "domain-5-fast-track" / "part-1-security-and-compliance.md"
PART2_PATH = DOCS_DIR / "domain-5-fast-track" / "part-2-governance-and-monitoring.md"
ULTRA_FAST_LEARN_PATH = DOCS_DIR / "domain-5-fast-track" / "ULTRA-FAST-LEARN.md"
SOURCE_PATH = DOCS_DIR / "domain-5-security-compliance-governance.md"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")

# The four concept groups the report identifies as dropped even at hop 1
# (full guide -> Fast Track): absent from the *entire* Fast Track
# directory (README + part-1 + part-2), and therefore also absent from
# Ultra Fast Learn.
HOP1_GAP_TOPICS = {
    "gdpr right to erasure / data minimization": [
        "right to erasure",
        "data minimization",
    ],
    "gdpr special category data classification": [
        "special category",
    ],
    "soc 2 type ii audit type": [
        "SOC 2 Type II",
    ],
    "aurora benefits hallucination-drift named metrics": [
        "HallucinationRate",
        "FactualConsistencyScore",
    ],
}

# The five concept groups the report identifies as retained in the Fast
# Track but missing from Ultra Fast Learn (hop 2: Fast Track -> Ultra
# Fast Learn).
HOP2_GAP_TOPICS = {
    "insecure output handling threat name": ["Insecure output handling"],
    "mitre atlas / owasp top 10 security frameworks": [
        "MITRE ATLAS",
        "OWASP Top 10",
    ],
    "amazon macie": ["Amazon Macie"],
    "titan image generator watermarking / provenance": [
        "Titan Image Generator",
        "watermark",
    ],
    "algorithmic accountability act": ["Algorithmic Accountability Act"],
}


def _read(path):
    return path.read_text(encoding="utf-8")


def _slugify(heading_text):
    """Approximate GitHub's markdown heading-anchor algorithm: lowercase,
    strip characters that aren't word characters/spaces/hyphens, then turn
    each remaining space into a hyphen (consecutive spaces -- e.g. from a
    removed em-dash or parenthesis -- become consecutive hyphens, not a
    single collapsed one, matching GitHub's actual behavior)."""
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = s.replace(" ", "-")
    return s


def _heading_anchors(doc_text):
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


def _combined_fast_track_text():
    return _read(README_PATH) + "\n" + _read(PART1_PATH) + "\n" + _read(PART2_PATH)


class TestReportExists(unittest.TestCase):
    def test_report_file_exists(self):
        self.assertTrue(
            REPORT_PATH.is_file(),
            "expected docs/domain-5-fast-track/COVERAGE-VERIFICATION-REPORT.md "
            "to exist",
        )

    def test_audited_files_exist(self):
        for path in (README_PATH, PART1_PATH, PART2_PATH, ULTRA_FAST_LEARN_PATH, SOURCE_PATH):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())


class TestReportStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(REPORT_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(
            self.text.startswith(
                "# Domain 5 Fast Track / Ultra Fast Learn: coverage "
                "verification report"
            )
        )

    def test_states_it_is_an_audit_not_new_content(self):
        self.assertIn("not new content authoring", self.text)

    def test_quotes_the_coverage_guarantee_under_test(self):
        self.assertIn("every testable concept", self.text)

    def test_lists_sections_spot_checked(self):
        self.assertIn("## Sections spot-checked", self.text)
        for fragment in (
            "Securing AI systems",
            "AWS compliance standards",
            "AWS Config",
        ):
            with self.subTest(section=fragment):
                self.assertIn(fragment, self.text)


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


class TestReportedHop1TopicsAreDocumented(unittest.TestCase):
    """The report's hop-1 finding must name each gap topic with enough
    specificity to identify it."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(REPORT_PATH)

    def test_report_names_each_gap_topic_and_its_keywords(self):
        for topic, keywords in HOP1_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertIn(
                        keyword,
                        self.text,
                        f"report does not mention {keyword!r} while "
                        f"discussing the {topic} gap",
                    )


class TestHop1GapTopicsPresentInSourceOnly(unittest.TestCase):
    """Hop 1 (full guide -> Fast Track) has four confirmed gaps: each
    keyword must appear in the full guide, but be absent from the entire
    Fast Track directory (README + part-1 + part-2) and from Ultra Fast
    Learn. If either downstream file starts containing a keyword, the
    report's "dropped even at this hop" claim has been resolved and
    should be updated to match, rather than silently left describing a
    stale problem."""

    @classmethod
    def setUpClass(cls):
        cls.source_text = _read(SOURCE_PATH)
        cls.fast_track_text = _combined_fast_track_text()
        cls.ultra_text = _read(ULTRA_FAST_LEARN_PATH)

    def test_source_guide_contains_every_gap_topic_keyword(self):
        for topic, keywords in HOP1_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertIn(keyword, self.source_text)

    def test_fast_track_is_missing_every_gap_topic_keyword(self):
        for topic, keywords in HOP1_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertNotIn(
                        keyword,
                        self.fast_track_text,
                        f"expected {keyword!r} (part of the {topic} gap) to "
                        "still be absent from the Fast Track (README + "
                        "part-1 + part-2) -- if it has been added, the "
                        "coverage gap this report documents has been "
                        "closed and the report/tests should be updated to "
                        "match",
                    )

    def test_ultra_fast_learn_is_missing_every_gap_topic_keyword(self):
        for topic, keywords in HOP1_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertNotIn(keyword, self.ultra_text)


class TestReportedHop2TopicsAreDocumented(unittest.TestCase):
    """The report's hop-2 finding must name each gap topic with enough
    specificity to identify it."""

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


class TestHop2GapTopicsPresentInFastTrack(unittest.TestCase):
    """Hop 1 (full guide -> Fast Track) is reported clean for these five
    topics: every hop-2 gap-topic keyword must actually appear in the
    combined Fast Track text (part-1 + part-2), or the report's "verified
    clean" claim for that hop is wrong."""

    @classmethod
    def setUpClass(cls):
        cls.fast_track_text = _read(PART1_PATH) + "\n" + _read(PART2_PATH)

    def test_fast_track_contains_every_gap_topic_keyword(self):
        for topic, keywords in HOP2_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertIn(keyword, self.fast_track_text)


class TestHop2GapTopicsAbsentFromUltraFastLearn(unittest.TestCase):
    """Hop 2 (Fast Track -> Ultra Fast Learn) is reported to have a real
    gap: none of the five topics' keywords should appear in Ultra Fast
    Learn today. If this test starts failing, the gap has been
    backfilled and COVERAGE-VERIFICATION-REPORT.md's "Recommendation"
    section (and this test) should be updated to reflect that, rather
    than silently left describing a stale problem."""

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


if __name__ == "__main__":
    unittest.main()
