"""Structural validation for the Domain 5 quick-reference cheat sheet.

The gap this covers: Domain 3 (Applications of Foundation Models) already
has an effective "## Quick-reference cheat sheet" section for last-minute
exam review, but Domain 5 (Security, Compliance, and Governance) had no
equivalent, even though it carries ~14% of scored questions and hinges on
several easily-confused service pairs (CloudTrail vs. Config vs. Audit
Manager; KMS vs. CloudTrail; interface vs. gateway VPC endpoints). This adds
a condensed, decision-table-driven cheat sheet near the end of the domain
guide, mirroring Domain 3's cheat-sheet style and placement. These tests
assert that section exists, is linked from the table of contents, sits in
the right place in the document, and actually covers the required topics --
so a future edit can't silently drop the section or let it drift out of
sync with the material it condenses.

Mirrors the conventions established in
tests/test_domain_3_quick_reference_cheat_sheet.py.

Run with:
    python3 -m unittest tests/test_domain_5_quick_reference_cheat_sheet.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _cheat_sheet_section(text):
    match = re.search(r"\n## Quick-reference cheat sheet\n(.*?)(?=\n## )", text, re.S)
    assert match, "expected a '## Quick-reference cheat sheet' section"
    return match.group(1)


class TestQuickReferenceCheatSheetExistsAndIsLinked(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_cheat_sheet_heading_present(self):
        self.assertIn("\n## Quick-reference cheat sheet\n", self.text)

    def test_cheat_sheet_linked_from_table_of_contents(self):
        toc_match = re.search(r"\n## Table of contents\n(.*?)\n## ", self.text, re.S)
        self.assertIsNotNone(toc_match)
        toc = toc_match.group(1)
        self.assertIn(
            "[Quick-reference cheat sheet](#quick-reference-cheat-sheet)",
            toc,
            "table of contents should link to the quick-reference cheat "
            "sheet section",
        )

    def test_cheat_sheet_sits_between_comparison_tables_and_glossary(self):
        # Regression guard for placement: the cheat sheet should recap
        # material the reader has just finished (the numbered sections and
        # the comparison tables) right before the glossary/practice
        # questions, not be buried mid-document.
        comparison_idx = self.text.index("\n## Comparison table")
        second_comparison_idx = self.text.index(
            "\n## Comparison table: governance and compliance regulations"
        )
        cheat_sheet_idx = self.text.index("\n## Quick-reference cheat sheet")
        glossary_idx = self.text.index("\n## Key terms glossary")
        self.assertLess(comparison_idx, second_comparison_idx)
        self.assertLess(second_comparison_idx, cheat_sheet_idx)
        self.assertLess(cheat_sheet_idx, glossary_idx)


class TestQuickReferenceCheatSheetContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _cheat_sheet_section(cls.text)

    def test_mentions_domain_weight(self):
        self.assertIn("14%", self.section)

    def test_covers_governance_service_comparison_table(self):
        for service in ["AWS CloudTrail", "AWS Config", "AWS Audit Manager"]:
            with self.subTest(service=service):
                self.assertIn(service, self.section)

    def test_governance_service_table_is_a_markdown_table(self):
        self.assertIn("| Service | Answers the question... | Example |", self.section)

    def test_covers_iam_least_privilege(self):
        for fact in [
            "least privilege",
            "execution role",
            "Resource-based policies",
            "IAM Access Analyzer",
        ]:
            with self.subTest(fact=fact):
                self.assertIn(fact, self.section)

    def test_covers_kms_cmk_encryption_at_rest_and_in_transit(self):
        for fact in [
            "customer managed keys (CMKs)",
            "At rest",
            "In transit",
            "TLS/HTTPS",
        ]:
            with self.subTest(fact=fact):
                self.assertIn(fact, self.section)

    def test_covers_privatelink_and_vpc_endpoints(self):
        for fact in [
            "interface VPC endpoint",
            "AWS PrivateLink",
            "gateway VPC",
        ]:
            with self.subTest(fact=fact):
                self.assertIn(fact, self.section)

    def test_has_common_exam_traps_callout(self):
        self.assertIn("Common exam traps", self.section)
        traps_idx = self.section.index("Common exam traps")
        traps = self.section[traps_idx:]
        # At least three distinct trap bullets should follow the heading.
        bullet_count = traps.count("\n- ")
        self.assertGreaterEqual(
            bullet_count,
            3,
            "expected at least 3 common-exam-trap bullets",
        )

    def test_cross_links_to_source_sections(self):
        for anchor in [
            "#1-securing-ai-systems",
            "#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance",
            "#comparison-table-governance-and-monitoring-services",
        ]:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.section)

    def test_is_decision_tables_not_prose(self):
        # The section should contain at least two markdown tables (pipe
        # rows), matching the "decision table" format requested, rather
        # than being written as long-form prose paragraphs.
        pipe_table_rows = len(re.findall(r"^\|.*\|$", self.section, re.M))
        self.assertGreaterEqual(
            pipe_table_rows,
            6,
            "expected multiple markdown table rows across the governance "
            "service and KMS/CMK decision tables",
        )


if __name__ == "__main__":
    unittest.main()
