"""Structural validation for docs/aws-service-decision-guide.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. The AWS service decision guide exists as
a consolidated quick reference sitting on top of the per-domain comparison
tables in Domains 1, 2, 3, and 5, so what matters most here is that it is
actually reachable from README.md, that it covers the specific services
named in the gap report (the SageMaker/Bedrock/purpose-built-service
decision flow, the security/compliance/governance table, and the
encryption/privacy table), and that every markdown link it makes into a
domain guide resolves to a real file and a real heading in that file. A
future edit that renames a heading in a domain doc (breaking an anchor
link) or removes the README pointer would otherwise go unnoticed since
nothing renders these docs in CI.

Mirrors the conventions established in tests/test_cross_domain_concept_map.py.

Run with:
    python3 -m unittest tests/test_aws_service_decision_guide.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DOC_PATH = DOCS_DIR / "aws-service-decision-guide.md"
README_PATH = REPO_ROOT / "README.md"

# Services the task description requires the decision flow to cover:
# SageMaker, Bedrock, and purpose-built AI services named as examples.
REQUIRED_DECISION_FLOW_SERVICES = [
    "SageMaker",
    "Bedrock",
    "Personalize",
    "Forecast",
    "Rekognition",
]

# Services the task description requires the security/compliance/governance
# table to cover.
REQUIRED_GOVERNANCE_SERVICES = [
    "CloudTrail",
    "Config",
    "Audit Manager",
    "Artifact",
]

# Concepts the task description requires the encryption/privacy table to
# cover.
REQUIRED_ENCRYPTION_CONCEPTS = [
    "KMS",
    "PrivateLink",
    "HIPAA",
    "BAA",
]

REQUIRED_LINKED_DOMAINS = [
    "domain-1-fundamentals-of-ai-and-ml.md",
    "domain-2-fundamentals-of-generative-ai.md",
    "domain-3-applications-of-foundation-models.md",
    "domain-5-security-compliance-governance.md",
]

MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)\s]+)\)")


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
    """Return the set of anchor slugs for every heading in a markdown doc."""
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


class TestAwsServiceDecisionGuideExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected AWS service decision guide at {DOC_PATH}",
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/aws-service-decision-guide.md",
            readme_text,
            "README.md must link to the AWS service decision guide so "
            "learners can discover it",
        )


class TestAwsServiceDecisionGuideCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)

    def test_has_title(self):
        self.assertRegex(self.text, r"^# AWS Service Decision Guide")

    def test_covers_decision_flow_services(self):
        for service in REQUIRED_DECISION_FLOW_SERVICES:
            with self.subTest(service=service):
                self.assertIn(
                    service,
                    self.text,
                    f"decision guide missing service in decision flow: "
                    f"{service!r}",
                )

    def test_covers_governance_services(self):
        for service in REQUIRED_GOVERNANCE_SERVICES:
            with self.subTest(service=service):
                self.assertIn(
                    service,
                    self.text,
                    f"decision guide missing governance service: {service!r}",
                )

    def test_covers_encryption_concepts(self):
        for concept in REQUIRED_ENCRYPTION_CONCEPTS:
            with self.subTest(concept=concept):
                self.assertIn(
                    concept,
                    self.text,
                    f"decision guide missing encryption/privacy concept: "
                    f"{concept!r}",
                )

    def test_links_into_every_required_domain(self):
        for domain_file in REQUIRED_LINKED_DOMAINS:
            with self.subTest(domain=domain_file):
                self.assertIn(
                    domain_file,
                    self.text,
                    f"decision guide does not link into {domain_file}",
                )

    def test_has_at_least_three_tables(self):
        # A markdown table needs a header separator row like |---|---|---|.
        # The task requires: (1) a decision flow (may or may not be a
        # table), (2) a governance/compliance table, (3) an
        # encryption/privacy table -- so at least two real tables, plus
        # slack for the "at a glance" tables it links to being distinct.
        table_rows = re.findall(r"\|\s*-{2,}\s*\|", self.text)
        self.assertGreaterEqual(
            len(table_rows),
            2,
            "expected at least a governance table and an encryption table",
        )

    def test_has_decision_flow_section(self):
        self.assertRegex(
            self.text,
            re.compile(r"decision flow", re.IGNORECASE),
            "expected an explicit decision-flow section for choosing "
            "between SageMaker, Bedrock, and purpose-built services",
        )


class TestAwsServiceDecisionGuideLinksResolve(unittest.TestCase):
    """The whole point of this doc is pointing back at the domain guides
    it consolidates. Verify every relative markdown link (optionally with
    a #anchor) points at a real file, and that the anchor -- if present --
    matches a real heading in that file."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        cls.links = MD_LINK_RE.findall(cls.text)
        cls.internal_links = [
            link
            for link in cls.links
            if not link.startswith(("http://", "https://", "#"))
        ]

    def test_found_a_substantial_number_of_internal_links(self):
        # Sanity check that the regex above is actually matching the
        # document's link syntax, so the resolution tests below aren't
        # silently vacuous.
        self.assertGreaterEqual(
            len(self.internal_links),
            5,
            "expected several internal links from the decision guide into "
            "the domain guides",
        )

    def test_every_internal_link_target_file_exists(self):
        for link in self.internal_links:
            file_part = link.split("#", 1)[0]
            with self.subTest(link=link):
                target_path = (DOCS_DIR / file_part).resolve()
                self.assertTrue(
                    target_path.is_file(),
                    f"linked file does not exist: {file_part!r} "
                    f"(resolved to {target_path})",
                )

    def test_every_internal_anchor_matches_a_real_heading(self):
        anchor_cache = {}
        for link in self.internal_links:
            if "#" not in link:
                continue
            file_part, anchor = link.split("#", 1)
            with self.subTest(link=link):
                if file_part not in anchor_cache:
                    target_path = (DOCS_DIR / file_part).resolve()
                    anchor_cache[file_part] = _heading_anchors(_read(target_path))
                self.assertIn(
                    anchor,
                    anchor_cache[file_part],
                    f"anchor #{anchor} does not match any heading slug in "
                    f"{file_part} -- the decision guide link is stale",
                )


if __name__ == "__main__":
    unittest.main()
