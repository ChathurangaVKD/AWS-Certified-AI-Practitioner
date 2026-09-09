"""Structural validation for the Domain 5 Fast Track (Part 1) condensed guide.

The gap this covers: Domain 5 (Security, Compliance, and Governance for AI
Solutions) is 2,853 lines -- too long for a last-minute, day-before-the-exam
re-read, and unlike Domain 4 there was no fast-track condensed guide at all.
A single ~1,100-1,150 line condensation of the whole domain would land in the
size range that has previously caused single-document opportunities to be
rejected as oversized, so Domain 5's fast track is split along its own topic
boundary into two parts. Part 1 --
`docs/domain-5-fast-track/part-1-security-and-compliance.md` -- covers
Section 1 (Securing AI systems: IAM, encryption, PrivateLink/VPC endpoints,
source citation/lineage, security threats, cost governance, MITRE
ATLAS/OWASP) and Section 2 (the five compliance frameworks: GDPR, HIPAA,
NIST AI RMF, EU AI Act, ISO/IEC 42001, plus the two compliance comparison
matrices) -- roughly the first 1,600 of the full guide's 2,853 lines. Part 2
(`docs/domain-5-fast-track/part-2-governance-and-monitoring.md`, covering
Sections 3-5: governance/audit services, data governance, shared
responsibility, plus the domain's two cross-cutting worked examples) is
intentionally out of scope for this file and is validated separately by
tests/test_domain_5_fast_track_part_2.py.

These tests assert that Part 1 exists, sits in a sane length band relative
to both the full source guide and the ~1,600-line span it condenses, links
back to the full guide with resolving anchors, and actually preserves the
covered material's testable concepts (IAM/least privilege, the
encryption-at-rest/in-transit/model-encryption distinction, PrivateLink,
every named security threat and its mitigation, MITRE ATLAS/OWASP, and all
five compliance frameworks with their binding-vs-voluntary status) as tables
and diagrams rather than just asserting they exist in prose.

Run with:
    python3 -m unittest tests/test_domain_5_fast_track_part_1.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
FAST_TRACK_PATH = DOCS_DIR / "domain-5-fast-track" / "part-1-security-and-compliance.md"
SOURCE_PATH = DOCS_DIR / "domain-5-security-compliance-governance.md"

# Approximate full-guide line span this part condenses (Section 1 + Section 2,
# i.e. "1. Securing AI systems" through the end of the requirements
# comparison matrix worked example, before "3. AWS Config, ...").
COVERED_SOURCE_LINE_ESTIMATE = 1600

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


class TestFastTrackPart1Exists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            FAST_TRACK_PATH.is_file(),
            "expected docs/domain-5-fast-track/part-1-security-and-compliance.md to exist",
        )

    def test_source_guide_exists(self):
        self.assertTrue(SOURCE_PATH.is_file())


class TestFastTrackPart1Length(unittest.TestCase):
    """Part 1 condenses roughly the first 1,600 lines of the 2,853-line
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
        # Relative to the ~1,600 lines of source material Part 1 actually
        # condenses (Sections 1-2), it should land well under 100% (a real
        # condensation) but comfortably above a token stub.
        ratio = self.fast_track_lines / COVERED_SOURCE_LINE_ESTIMATE
        self.assertGreater(ratio, 0.25)
        self.assertLess(ratio, 0.9)


class TestFastTrackPart1Structure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_has_top_level_heading(self):
        self.assertTrue(self.text.startswith("# Domain 5 Fast Track"))

    def test_heading_identifies_this_as_part_1(self):
        self.assertIn("Part 1", self.text.splitlines()[0])

    def test_links_back_to_full_guide(self):
        self.assertIn(
            "(../domain-5-security-compliance-governance.md)",
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
            "the KMS key lifecycle / architecture and the compliance "
            "decision tree / NIST AI RMF mapping",
        )

    def test_contains_at_least_seven_markdown_tables(self):
        table_separator_rows = re.findall(r"\n\|[-\s|]+\|\n", self.text)
        self.assertGreaterEqual(
            len(table_separator_rows),
            7,
            "expected multiple comparison/decision tables (security "
            "threats, compliance frameworks, requirements matrix, etc.)",
        )


class TestFastTrackPart1CrossReferencesResolve(unittest.TestCase):
    """Every internal link out of the fast track guide must resolve to a
    real file and, if anchored, a real heading in that file -- mirroring
    tests/test_cross_reference_links.py's conventions for the five domain
    guides and tests/test_domain_4_fast_track_guide.py's conventions for
    the Domain 4 fast track."""

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


class TestFastTrackPart1Content(unittest.TestCase):
    """Part 1 must keep every testable concept named in its scope: IAM and
    least privilege, the data-vs-model encryption distinction, PrivateLink,
    every named security threat and its mitigation, both security
    frameworks, and all five compliance frameworks with their
    binding-vs-voluntary status."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(FAST_TRACK_PATH)

    def test_covers_iam_concepts(self):
        for term in [
            "IAM roles",
            "IAM policies",
            "Least privilege",
            "IAM Access Analyzer",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_encryption_concepts(self):
        for term in [
            "Encryption at rest",
            "customer managed key",
            "Model encryption",
            "AWS KMS",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_privatelink_and_vpc_endpoints(self):
        self.assertIn("AWS PrivateLink", self.text)
        self.assertIn("interface VPC endpoint", self.text)

    def test_covers_source_citation_and_lineage(self):
        self.assertIn("Source citation", self.text)
        self.assertIn("Data lineage", self.text)
        self.assertIn("SageMaker ML Lineage Tracking", self.text)

    def test_covers_all_named_security_threats(self):
        for threat in [
            "Data poisoning",
            "Prompt injection (direct)",
            "Prompt injection (indirect)",
            "Model inversion / extraction",
            "Model drift",
            "Insecure output handling",
            "Model denial of service",
            "Supply chain vulnerabilities",
            "Sensitive information disclosure",
            "Insecure plugin design",
            "Excessive agency",
            "Overreliance",
        ]:
            with self.subTest(threat=threat):
                self.assertIn(threat, self.text)

    def test_covers_differential_privacy(self):
        self.assertIn("Differential privacy", self.text)
        self.assertIn("privacy budget", self.text)

    def test_covers_cost_governance_controls(self):
        for term in ["Service Quotas", "usage plan"]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_security_frameworks(self):
        self.assertIn("MITRE ATLAS", self.text)
        self.assertIn("OWASP Top 10 for LLM Applications", self.text)

    def test_covers_aws_artifact_reports_vs_agreements(self):
        self.assertIn("Artifact Reports", self.text)
        self.assertIn("Artifact Agreements", self.text)
        self.assertIn("Business Associate Addendum", self.text)
        self.assertIn("Data Processing Addendum", self.text)

    def test_covers_all_five_compliance_frameworks(self):
        for framework in [
            "GDPR",
            "HIPAA",
            "NIST AI RMF",
            "EU AI Act",
            "ISO/IEC 42001",
        ]:
            with self.subTest(framework=framework):
                self.assertIn(framework, self.text)

    def test_covers_binding_vs_voluntary_distinction(self):
        self.assertIn("Binding vs. voluntary", self.text)
        self.assertIn("Algorithmic Accountability Act", self.text)

    def test_covers_gdpr_erasure_minimization_and_special_category(self):
        # Coverage-verification-report hop-1 gap: these named GDPR facts
        # (full guide line ~1206 and the Northfield worked example, line
        # ~2371) were previously dropped from the Fast Track entirely.
        for term in [
            "right to erasure",
            "data minimization",
            "special category",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.text)

    def test_covers_nist_ai_rmf_four_functions(self):
        for function in ["GOVERN", "MAP", "MEASURE", "MANAGE"]:
            with self.subTest(function=function):
                self.assertIn(function, self.text)

    def test_covers_eu_ai_act_risk_tiers(self):
        for tier in ["unacceptable", "high", "limited", "minimal"]:
            with self.subTest(tier=tier):
                self.assertIn(tier, self.text)

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

    def test_links_forward_to_part_2(self):
        # Part 2 now exists, so Part 1 should link to it by name rather than
        # just mentioning it in prose.
        self.assertIn("Part 2", self.text)
        self.assertIn(
            "(../domain-5-fast-track/part-2-governance-and-monitoring.md)",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
