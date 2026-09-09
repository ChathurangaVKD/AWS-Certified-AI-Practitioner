"""Structural validation for the Domain 5 Fast Track (Part 2) condensed guide.

The gap this covers: Domain 5 (Security, Compliance, and Governance for AI
Solutions) is 2,853 lines -- too long for a last-minute, day-before-the-exam
re-read -- so its fast track is split along its own topic boundary into two
parts (see tests/test_domain_5_fast_track_part_1.py for Part 1's rationale).
Part 2 -- `docs/domain-5-fast-track/part-2-governance-and-monitoring.md` --
covers Section 3 (AWS Config, AWS Audit Manager, and AWS CloudTrail for AI
governance), Section 4 (data governance strategies: data lifecycle, data
residency, data monitoring), Section 5 (the AWS shared responsibility model
applied to AI/ML services), and condensed pointers into the domain's two
cross-cutting worked examples (the HIPAA-regulated Bedrock lifecycle, and the
multi-region GDPR/HIPAA/NIST AI RMF deployment) plus its shared
quick-reference cheat sheet, glossary, and practice question set -- roughly
the last 1,200 of the full guide's 2,853 lines.

These tests assert that Part 2 exists, sits in a sane length band relative
to both the full source guide and the ~1,200-line span it condenses, links
back to the full guide (and to Part 1) with resolving anchors, and actually
preserves the covered material's testable concepts (the CloudTrail/Config/
Audit Manager distinction, data lifecycle/residency/monitoring concepts and
their services, and the shared responsibility model's Bedrock-vs-SageMaker
split) as tables and diagrams rather than just asserting they exist in
prose.

Run with:
    python3 -m unittest tests/test_domain_5_fast_track_part_2.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_PATH = DOCS_DIR / "domain-5-fast-track" / "part-2-governance-and-monitoring.md"
SOURCE_PATH = DOCS_DIR / "domain-5-security-compliance-governance.md"

# Approximate full-guide line span this part condenses (Section 3 through
# the end of the two cross-cutting worked examples, i.e. "3. AWS Config,
# AWS Audit Manager, and AWS CloudTrail ..." through the end of the
# multi-region GDPR/HIPAA/NIST AI RMF worked example, before the shared
# comparison tables / cheat sheet / glossary / practice questions).
COVERED_SOURCE_LINE_ESTIMATE = 1200

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")


def _read(path):
    return path.read_text(encoding="utf-8")


def _line_count(path):
    return _read(path).count("\n")


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


class TestFastTrackPart2Exists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            FAST_TRACK_PATH.is_file(),
            "expected docs/domain-5-fast-track/part-2-governance-and-monitoring.md to exist",
        )

    def test_source_guide_exists(self):
        self.assertTrue(SOURCE_PATH.is_file())


class TestFastTrackPart2Length(unittest.TestCase):
    """Part 2 condenses roughly the last 1,200 lines of the 2,853-line
    source guide down to a fast-track summary. Assert it's a real, sizeable
    condensation of its covered scope -- not a stub, and not a near-copy of
    the whole domain guide (which would defeat the point of splitting it
    into two parts to stay under the repo's diff-size cap)."""

    @classmethod
    def setUpClass(cls):
        cls.fast_track_lines = _line_count(FAST_TRACK_PATH)
        cls.source_lines = _line_count(SOURCE_PATH)

    def test_fast_track_is_substantially_shorter_than_full_source(self):
        self.assertLess(self.fast_track_lines, self.source_lines * 0.6)

    def test_fast_track_is_not_a_trivial_stub(self):
        self.assertGreater(self.fast_track_lines, self.source_lines * 0.15)

    def test_fast_track_is_a_reasonable_condensation_of_its_covered_span(self):
        # Relative to the ~1,200 lines of source material Part 2 actually
        # condenses (Sections 3-5 plus the two cross-cutting worked
        # examples), it should land well under 100% (a real condensation)
        # but comfortably above a token stub.
        ratio = self.fast_track_lines / COVERED_SOURCE_LINE_ESTIMATE
        self.assertGreater(ratio, 0.25)
        self.assertLess(ratio, 0.9)


class TestFastTrackPart2Structure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(self.text.startswith("# Domain 5 Fast Track"))

    def test_heading_identifies_this_as_part_2(self):
        self.assertIn("Part 2", self.text.splitlines()[0])

    def test_links_back_to_full_guide(self):
        self.assertIn(
            "(../domain-5-security-compliance-governance.md)",
            self.text,
        )

    def test_links_back_to_part_1(self):
        self.assertIn(
            "(../domain-5-fast-track/part-1-security-and-compliance.md)",
            self.text,
        )

    def test_has_table_of_contents(self):
        self.assertIn("\n## Table of contents\n", self.text)

    def test_toc_entries_resolve_to_real_headings_in_this_file(self):
        toc_match = re.search(
            r"\n## Table of contents\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(toc_match)
        toc = toc_match.group(1)
        anchors_in_toc = re.findall(r"\]\(#([^)]+)\)", toc)
        self.assertGreaterEqual(len(anchors_in_toc), 8)
        real_anchors = _heading_anchors(self.text)
        for anchor in anchors_in_toc:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, real_anchors)

    def test_contains_at_least_two_mermaid_diagrams(self):
        self.assertGreaterEqual(
            self.text.count("```mermaid"),
            2,
            "expected the fast track guide to carry Mermaid diagrams for "
            "the Config/Audit Manager/Artifact evidence chain and the "
            "data-governance pipeline",
        )

    def test_contains_at_least_seven_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            7,
            "expected multiple comparison/decision tables (governance "
            "services, data monitoring, shared responsibility, etc.)",
        )


class TestFastTrackPart2CrossReferencesResolve(unittest.TestCase):
    """Every internal link out of the fast track guide must resolve to a
    real file and, if anchored, a real heading in that file -- mirroring
    tests/test_domain_5_fast_track_part_1.py's conventions."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)
        all_links = MD_LINK_RE.findall(cls.text)
        cls.links = [
            link
            for link in all_links
            if not link.startswith(("http://", "https://"))
        ]
        cls.anchor_cache = {}

    def _resolve_target_path(self, file_part):
        if file_part == "":
            return FAST_TRACK_PATH
        return (FAST_TRACK_PATH.parent / file_part).resolve()

    def test_has_several_internal_links(self):
        self.assertGreaterEqual(len(self.links), 10)

    def test_every_internal_link_target_file_exists(self):
        for link in self.links:
            file_part = link.split("#", 1)[0]
            with self.subTest(link=link):
                target_path = self._resolve_target_path(file_part)
                self.assertTrue(
                    target_path.is_file(),
                    f"linked file does not exist: {file_part!r} (resolved "
                    f"to {target_path}) in the fast track guide",
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
                    f"{target_path} -- the link {link!r} in the fast track "
                    "guide is stale",
                )


class TestFastTrackPart2Content(unittest.TestCase):
    """Part 2 must keep every testable concept named in its scope: the
    CloudTrail/Config/Audit Manager distinction, data governance strategies
    and their services, and the shared responsibility model."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_covers_governance_and_audit_services(self):
        for term in [
            "AWS CloudTrail",
            "AWS Config",
            "AWS Audit Manager",
            "Config rules",
            "AWS Artifact",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_data_monitoring_services(self):
        for term in ["Amazon Macie", "Amazon CloudWatch", "Amazon GuardDuty"]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_data_governance_concepts(self):
        for term in [
            "Data lifecycle",
            "Data residency",
            "Data sovereignty",
            "Data monitoring",
            "S3 Lifecycle",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_knowledge_base_drift_distinction(self):
        self.assertIn("hallucination", self.text.lower())
        self.assertIn("re-embed", self.text.lower())

    def test_covers_shared_responsibility_model(self):
        for term in [
            "Shared Responsibility Model",
            'security "of" the cloud',
            'security "in" the cloud',
            "Amazon Bedrock",
            "Amazon SageMaker",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_worked_example_topics(self):
        self.assertIn("MedNote", self.text)
        self.assertIn("Northfield Genomics", self.text)

    def test_covers_soc2_type_ii_and_aurora_named_metrics(self):
        # Coverage-verification-report hop-1 gaps: the SOC 2 Type II audit
        # type (Meridian Lending worked example, full guide lines
        # ~1804/1845/1856) and Aurora Benefits' named CloudWatch metrics,
        # namespace, and thresholds (full guide line ~2018) were
        # previously dropped from the Fast Track entirely.
        for term in [
            "SOC 2 Type II",
            "HallucinationRate",
            "FactualConsistencyScore",
            "RAGAssistant/Quality",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_has_comparison_tables_from_full_guide(self):
        self.assertIn(
            "\n## Comparison table: governance and monitoring services\n",
            self.text,
        )
        self.assertIn(
            "\n## Comparison table: governance and compliance regulations at a glance\n",
            self.text,
        )

    def test_has_key_terms_section_with_bolded_terms(self):
        key_terms_match = re.search(
            r"\n## Rapid-fire key terms\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(key_terms_match)
        section = key_terms_match.group(1)
        bolded_bullets = re.findall(r"\n- \*\*[^*]+\*\*", section)
        self.assertGreaterEqual(
            len(bolded_bullets),
            15,
            "expected at least 15 bolded key-term bullets in the rapid-fire "
            "key terms section",
        )

    def test_has_common_exam_traps_checklist(self):
        self.assertIn("\n## Common exam traps checklist\n", self.text)
        traps_match = re.search(
            r"\n## Common exam traps checklist\n(.*?)\n## ", self.text, re.S
        )
        self.assertIsNotNone(traps_match)
        bullet_count = traps_match.group(1).count("\n- [ ]")
        self.assertGreaterEqual(bullet_count, 8)

    def test_links_forward_from_part_1(self):
        # Part 1 must link forward to this file now that it exists.
        part_1_path = (
            FAST_TRACK_PATH.parent / "part-1-security-and-compliance.md"
        )
        part_1_text = _read(part_1_path)
        self.assertIn(
            "(../domain-5-fast-track/part-2-governance-and-monitoring.md)",
            part_1_text,
        )


if __name__ == "__main__":
    unittest.main()
