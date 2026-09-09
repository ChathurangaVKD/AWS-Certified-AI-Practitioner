"""Validation for the Domain 3 Fast Track / Ultra Fast Learn coverage
verification report.

The gap this covers: Domain 3's Fast Track and Ultra Fast Learn materials
carry an explicit coverage guarantee (docs/DOCUMENTATION_STRUCTURE.md:
"every testable concept the full domain guide covers is retained somewhere
in the condensed layer") that had never been technically verified against
the source guide -- flagged in the Content Health assessment as "requires
technical verification." Domain 3 is the highest-weight domain (~28%) and
the longest guide (6,957 lines), split into a three-part Fast Track
(part-1/2/3) plus ULTRA-FAST-LEARN.md, so it warrants extra scrutiny.

`docs/domain-3-fast-track/COVERAGE-VERIFICATION-REPORT.md` is that
verification. It originally found two classes of gap:

- A hop-1 gap (full guide -> Fast Track): the "Kendra GenAI Index as a
  Bedrock Knowledge Base data source" worked example is present in the
  full guide AND in Ultra Fast Learn, but absent from both Fast Track
  Part 1 and Part 2 -- an inversion of the normal layering, where the
  further-condensed cram sheet has a concept the intermediate condensed
  guide dropped. This gap is still open.
- Four hop-2 gaps (Fast Track -> Ultra Fast Learn): fine-tuning
  efficiency techniques (LoRA/QLoRA/instruction tuning), RLHF, fine-tuning
  dataset curation, and retrieval quality metrics (NDCG/MAP/Recall@k/MRR)
  were all fully covered in Part 1 or Part 2 but entirely absent from
  Ultra Fast Learn. These four have since been backfilled into
  ULTRA-FAST-LEARN.md (2026-09-09), sourced verbatim from the same Fast
  Track subsections, closing the gap.

These tests assert the report exists, links back to the files it audits
with resolving anchors, and that its central claims still hold against the
live files -- so this test would start failing, as a useful signal, the
day someone backfills the remaining hop-1 gap and the report's "still
open" claim about it goes stale.

Run with:
    python3 -m unittest tests/test_domain_3_coverage_verification_report.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_DIR = DOCS_DIR / "domain-3-fast-track"
REPORT_PATH = FAST_TRACK_DIR / "COVERAGE-VERIFICATION-REPORT.md"
PART1_PATH = FAST_TRACK_DIR / "part-1-application-design-and-customization.md"
PART2_PATH = FAST_TRACK_DIR / "part-2-inference-and-multimodal.md"
PART3_PATH = FAST_TRACK_DIR / "part-3-deployment-and-troubleshooting.md"
ULTRA_FAST_LEARN_PATH = FAST_TRACK_DIR / "ULTRA-FAST-LEARN.md"
SOURCE_PATH = DOCS_DIR / "domain-3-applications-of-foundation-models.md"

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")

# The four concept groups the report identifies as fully covered in the
# Fast Track (hop 1 is clean) but missing entirely from Ultra Fast Learn
# (hop 2 has the gap). Each is a list of keywords that must ALL appear
# together for that concept to count as "covered."
HOP2_GAP_TOPICS = {
    "fine-tuning efficiency techniques (LoRA/QLoRA/instruction tuning)": [
        "LoRA",
        "QLoRA",
        "instruction tuning",
    ],
    "RLHF": [
        "RLHF",
        "reward model",
    ],
    "fine-tuning dataset curation": [
        "catastrophic forgetting",
        "early stopping",
        "inter-annotator",
    ],
    "retrieval quality metrics": [
        "NDCG",
        "MRR",
        "Recall@k",
    ],
}

# The one hop-1 finding: "Kendra GenAI Index" is present in the full guide
# and in Ultra Fast Learn, but absent from both Fast Track Part 1 and
# Part 2.
HOP1_GAP_KEYWORD = "Kendra GenAI Index"


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
            "expected docs/domain-3-fast-track/COVERAGE-VERIFICATION-REPORT.md "
            "to exist",
        )

    def test_audited_files_exist(self):
        for path in (
            PART1_PATH,
            PART2_PATH,
            PART3_PATH,
            ULTRA_FAST_LEARN_PATH,
            SOURCE_PATH,
        ):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())


class TestReportStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(REPORT_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(
            self.text.startswith(
                "# Domain 3 Fast Track / Ultra Fast Learn: coverage "
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
        # major sections" ask -- this report checked more, given Domain 3's
        # explicit "extra scrutiny" instruction.
        for fragment in (
            "Retrieval Augmented Generation (RAG) and Amazon Bedrock",
            "Fine-tuning vs. continued pre-training vs. RAG vs. prompt",
            "Amazon Bedrock features",
            "Vector databases and embeddings for search",
        ):
            with self.subTest(section=fragment):
                self.assertIn(fragment, self.text)

    def test_names_the_hop1_gap(self):
        self.assertIn(HOP1_GAP_KEYWORD, self.text)


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
    full guide and at least one Fast Track part, or the report's
    "verified clean" claim for that hop is wrong."""

    @classmethod
    def setUpClass(cls):
        cls.source_text = _read(SOURCE_PATH)
        cls.fast_track_text = (
            _read(PART1_PATH) + "\n" + _read(PART2_PATH) + "\n" + _read(PART3_PATH)
        )

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


class TestHop2GapTopicsNowPresentInUltraFastLearn(unittest.TestCase):
    """Hop 2 (Fast Track -> Ultra Fast Learn) gap for these four topics has
    been backfilled (2026-09-09): every keyword must now appear in Ultra
    Fast Learn. If this test starts failing, the backfill has regressed
    (a keyword was removed) and COVERAGE-VERIFICATION-REPORT.md's
    "Findings 2-5" update should be re-checked against the live file."""

    @classmethod
    def setUpClass(cls):
        cls.ultra_text = _read(ULTRA_FAST_LEARN_PATH)

    def test_ultra_fast_learn_contains_every_gap_topic_keyword(self):
        for topic, keywords in HOP2_GAP_TOPICS.items():
            for keyword in keywords:
                with self.subTest(topic=topic, keyword=keyword):
                    self.assertIn(
                        keyword,
                        self.ultra_text,
                        f"expected {keyword!r} (part of the {topic} gap) to "
                        "be present in ULTRA-FAST-LEARN.md now that this "
                        "hop-2 gap has been backfilled -- if it's missing, "
                        "the backfill has regressed",
                    )


class TestHop1GapTopicPresentInSourceAndUltraFastLearnOnly(unittest.TestCase):
    """The hop-1 finding: "Kendra GenAI Index" is present in the full guide
    and (independently) in Ultra Fast Learn, but absent from both Fast
    Track Part 1 and Part 2 -- the inverse of the usual layering. If either
    Fast Track part starts containing it, the report's "falls through the
    gap between Part 1 and Part 2" claim has been resolved and should be
    updated to match, rather than silently left describing a stale
    problem."""

    @classmethod
    def setUpClass(cls):
        cls.source_text = _read(SOURCE_PATH)
        cls.part1_text = _read(PART1_PATH)
        cls.part2_text = _read(PART2_PATH)
        cls.ultra_text = _read(ULTRA_FAST_LEARN_PATH)

    def test_source_guide_contains_the_hop1_gap_keyword(self):
        self.assertIn(HOP1_GAP_KEYWORD, self.source_text)

    def test_part1_is_missing_the_hop1_gap_keyword(self):
        self.assertNotIn(HOP1_GAP_KEYWORD, self.part1_text)

    def test_part2_is_missing_the_hop1_gap_keyword(self):
        self.assertNotIn(HOP1_GAP_KEYWORD, self.part2_text)

    def test_ultra_fast_learn_contains_the_hop1_gap_keyword(self):
        # Ultra Fast Learn captured this concept independently, which is
        # exactly what makes it identifiable as exam-relevant rather than
        # full-guide-only narrative.
        self.assertIn(HOP1_GAP_KEYWORD, self.ultra_text)


if __name__ == "__main__":
    unittest.main()
