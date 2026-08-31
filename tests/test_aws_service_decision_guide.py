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

# Model families the Bedrock model reference section must cover -- these
# are the families the five domain guides mention by name without ever
# consolidating them into one comparison (the gap this section closes).
REQUIRED_BEDROCK_MODEL_FAMILIES = [
    "Titan",
    "Nova",
    "Claude",
    "Llama",
    "Cohere",
    "Mistral",
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

    def test_has_bedrock_model_reference_section(self):
        self.assertRegex(
            self.text,
            re.compile(r"^##\s+4\.\s+Bedrock model reference", re.M),
            "expected a numbered 'Bedrock model reference' section "
            "closing the model-capability content gap",
        )

    def test_bedrock_model_reference_covers_required_families(self):
        section_match = re.search(
            r"^##\s+4\.\s+Bedrock model reference.*?(?=^## |\Z)",
            self.text,
            re.M | re.S,
        )
        self.assertIsNotNone(
            section_match, "could not locate the Bedrock model reference section"
        )
        section_text = section_match.group(0)
        for family in REQUIRED_BEDROCK_MODEL_FAMILIES:
            with self.subTest(family=family):
                self.assertIn(
                    family,
                    section_text,
                    f"Bedrock model reference section missing model "
                    f"family: {family!r}",
                )

    def test_bedrock_model_reference_has_a_comparison_table(self):
        section_match = re.search(
            r"^##\s+4\.\s+Bedrock model reference.*?(?=^## |\Z)",
            self.text,
            re.M | re.S,
        )
        self.assertIsNotNone(section_match)
        section_text = section_match.group(0)
        table_rows = re.findall(r"\|\s*-{2,}\s*\|", section_text)
        self.assertGreaterEqual(
            len(table_rows),
            1,
            "expected the Bedrock model reference section to include a "
            "markdown comparison table",
        )

    def test_bedrock_model_reference_flags_staleness(self):
        section_match = re.search(
            r"^##\s+4\.\s+Bedrock model reference.*?(?=^## |\Z)",
            self.text,
            re.M | re.S,
        )
        self.assertIsNotNone(section_match)
        section_text = section_match.group(0)
        self.assertRegex(
            section_text,
            re.compile(r"staleness|changes frequently|snapshot", re.IGNORECASE),
            "expected the Bedrock model reference to warn readers that "
            "Bedrock's model catalog changes frequently",
        )

    def test_bedrock_model_reference_records_last_verification_date(self):
        # The staleness warning alone doesn't tell a future reviewer
        # whether the table has ever actually been checked against AWS's
        # docs, or when. This asserts the section records a concrete
        # "last verified" checkpoint with a real ISO date, not just the
        # general warning that the catalog changes often.
        section_match = re.search(
            r"^##\s+4\.\s+Bedrock model reference.*?(?=^## |\Z)",
            self.text,
            re.M | re.S,
        )
        self.assertIsNotNone(section_match)
        section_text = section_match.group(0)
        self.assertRegex(
            section_text,
            re.compile(r"last verified\W{0,6}\d{4}-\d{2}-\d{2}", re.IGNORECASE),
            "expected the Bedrock model reference section to record a "
            "'Last verified: YYYY-MM-DD' checkpoint against the official "
            "Bedrock model catalog",
        )

    def test_bedrock_model_reference_retires_titan_text_generation_row(self):
        # As of the most recent verification pass, Titan Text
        # (Lite/Express/Premier) has been retired from the Bedrock catalog
        # in favor of Nova. The row should stay (for exam-history context)
        # but must be clearly marked retired rather than presented as a
        # currently available choice.
        section_match = re.search(
            r"^##\s+4\.\s+Bedrock model reference.*?(?=^## |\Z)",
            self.text,
            re.M | re.S,
        )
        self.assertIsNotNone(section_match)
        section_text = section_match.group(0)
        titan_text_row = next(
            (
                line
                for line in section_text.splitlines()
                if line.strip().startswith("| **Amazon Titan Text**")
            ),
            None,
        )
        self.assertIsNotNone(
            titan_text_row,
            "expected an Amazon Titan Text row in the Bedrock model table",
        )
        self.assertRegex(
            titan_text_row,
            re.compile(r"retired", re.IGNORECASE),
            "Titan Text (Lite/Express/Premier) is retired in the current "
            "Bedrock catalog and should be labeled as such rather than "
            "listed as a currently available family",
        )

    def test_bedrock_model_reference_jurassic_family_removed(self):
        # AI21's Jurassic line is no longer offered in Bedrock -- Jamba is
        # AI21's only current family there. Verify it isn't still listed
        # as an available option in the table.
        section_match = re.search(
            r"^##\s+4\.\s+Bedrock model reference.*?(?=^## |\Z)",
            self.text,
            re.M | re.S,
        )
        self.assertIsNotNone(section_match)
        section_text = section_match.group(0)
        table_match = re.search(
            r"^\| Model family \|.*?\n\|---.*?\n(?P<rows>(?:\|.*\n)+)",
            section_text,
            re.M,
        )
        self.assertIsNotNone(table_match, "could not locate the model table rows")
        family_column_text = table_match.group("rows")
        self.assertNotIn(
            "Jamba/Jurassic",
            family_column_text,
            "Jurassic should no longer be listed alongside Jamba as a "
            "currently available AI21 family name",
        )


API_GATEWAY_SECTION_RE = re.compile(
    r"^##\s+6\.\s+Decision guide: Amazon API Gateway.*?(?=^## |\Z)", re.M | re.S
)

PROMPT_MANAGEMENT_SECTION_RE = re.compile(
    r"^##\s+7\.\s+Decision guide: Bedrock Prompt Management.*?(?=^## |\Z)",
    re.M | re.S,
)


class TestAwsServiceDecisionGuideApiGatewaySection(unittest.TestCase):
    """Section 6 -- API Gateway request throttling/Service Quotas in front
    of Bedrock/SageMaker endpoints, referenced but previously unguided
    (see Domain 5's 'model denial of service' mitigation content)."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        section_match = API_GATEWAY_SECTION_RE.search(cls.text)
        assert section_match is not None, "could not locate section 6"
        cls.section_text = section_match.group(0)

    def test_has_api_gateway_section(self):
        self.assertRegex(
            self.text,
            re.compile(
                r"^##\s+6\.\s+Decision guide: Amazon API Gateway", re.M
            ),
            "expected a numbered decision-guide section for Amazon API "
            "Gateway in front of Bedrock/SageMaker endpoints",
        )

    def test_covers_related_controls(self):
        for term in [
            "Amazon API Gateway",
            "Service Quotas",
            "Provisioned Throughput",
            "Guardrails",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.section_text)

    def test_has_a_comparison_table(self):
        table_rows = re.findall(r"\|\s*-{2,}\s*\|", self.section_text)
        self.assertGreaterEqual(
            len(table_rows),
            1,
            "expected the API Gateway section to include a markdown "
            "comparison table of decision criteria",
        )

    def test_has_exam_style_scenario_with_answer(self):
        self.assertRegex(
            self.section_text,
            re.compile(r"exam-style scenario", re.IGNORECASE),
            "expected an explicit exam-style scenario",
        )
        self.assertRegex(
            self.section_text,
            re.compile(r"\*\*Answer:\s*[A-D]\*\*"),
            "expected the scenario to state its answer letter",
        )

    def test_links_back_to_domain_5_threat_section(self):
        self.assertIn("domain-5-security-compliance-governance.md", self.section_text)


class TestAwsServiceDecisionGuidePromptManagementSection(unittest.TestCase):
    """Section 7 -- Bedrock Prompt Management vs. Prompt Flows vs. direct
    prompting, referenced but previously unguided (see Domain 3's prompt
    engineering content)."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        section_match = PROMPT_MANAGEMENT_SECTION_RE.search(cls.text)
        assert section_match is not None, "could not locate section 7"
        cls.section_text = section_match.group(0)

    def test_has_prompt_management_section(self):
        self.assertRegex(
            self.text,
            re.compile(
                r"^##\s+7\.\s+Decision guide: Bedrock Prompt Management",
                re.M,
            ),
            "expected a numbered decision-guide section for Bedrock "
            "Prompt Management vs. Prompt Flows vs. direct prompting",
        )

    def test_covers_all_three_approaches(self):
        for term in [
            "Direct prompting",
            "Amazon Bedrock Prompt Management",
            "Amazon Bedrock Prompt Flows",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.section_text)

    def test_has_a_comparison_table(self):
        table_rows = re.findall(r"\|\s*-{2,}\s*\|", self.section_text)
        self.assertGreaterEqual(
            len(table_rows),
            1,
            "expected the Prompt Management section to include a "
            "markdown comparison table of decision criteria",
        )

    def test_has_exam_style_scenario_with_answer(self):
        self.assertRegex(
            self.section_text,
            re.compile(r"exam-style scenario", re.IGNORECASE),
            "expected an explicit exam-style scenario",
        )
        self.assertRegex(
            self.section_text,
            re.compile(r"\*\*Answer:\s*[A-D]\*\*"),
            "expected the scenario to state its answer letter",
        )

    def test_links_back_to_domain_3_prompt_engineering_section(self):
        self.assertIn(
            "domain-3-applications-of-foundation-models.md",
            self.section_text,
        )


CONSOLIDATED_MATRIX_HEADING_RE = re.compile(
    r"^##\s+5\.\s+Consolidated service matrix.*?(?=^## |\Z)", re.M | re.S
)

# A markdown table row belonging to the consolidated matrix, e.g.:
# | **Amazon Bedrock** | D2, D3, D4, D5 | ~24% + ~28% | ... | ... |
MATRIX_ROW_RE = re.compile(r"^\|\s*\*\*(?P<service>[^*]+)\*\*\s*\|", re.M)

# A representative sample spanning multiple domains -- enough to catch a
# regression that drops a whole domain's services from the matrix, without
# requiring the test to enumerate all 45+ rows verbatim.
REQUIRED_MATRIX_SAMPLE_SERVICES = [
    "Amazon SageMaker",
    "Amazon Bedrock",
    "Amazon Rekognition",
    "Guardrails for Amazon Bedrock",
    "AWS CloudTrail",
    "AWS PrivateLink",
    "Amazon Kendra",
    "AWS Trainium",
    "AWS Inferentia",
]


class TestAwsServiceDecisionGuideConsolidatedMatrix(unittest.TestCase):
    """Section 5 -- the consolidated matrix spanning all 45+ services
    referenced across the domain guides, with domain, exam-weight,
    when-to-use, and common-confusion columns."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOC_PATH)
        section_match = CONSOLIDATED_MATRIX_HEADING_RE.search(cls.text)
        assert section_match is not None, "could not locate section 5"
        cls.section_text = section_match.group(0)

    def test_has_consolidated_matrix_section(self):
        self.assertRegex(
            self.text,
            re.compile(r"^##\s+5\.\s+Consolidated service matrix", re.M),
            "expected a numbered 'Consolidated service matrix' section "
            "spanning all domains",
        )

    def test_matrix_has_required_columns(self):
        header_line = next(
            line
            for line in self.section_text.splitlines()
            if line.strip().startswith("| Service")
        )
        for column in [
            "Domain",
            "Exam weight relevance",
            "When to use it",
            "Common point of confusion",
        ]:
            with self.subTest(column=column):
                self.assertIn(column, header_line)

    def test_matrix_has_at_least_45_service_rows(self):
        rows = MATRIX_ROW_RE.findall(self.section_text)
        self.assertGreaterEqual(
            len(rows),
            45,
            "expected the consolidated matrix to cover at least 45 "
            f"services (found {len(rows)})",
        )

    def test_matrix_covers_required_sample_services(self):
        rows = MATRIX_ROW_RE.findall(self.section_text)
        for service in REQUIRED_MATRIX_SAMPLE_SERVICES:
            with self.subTest(service=service):
                self.assertIn(
                    service,
                    rows,
                    f"consolidated matrix missing service row: {service!r}",
                )

    def test_matrix_row_count_matches_service_index_entry_count(self):
        # The whole point of this matrix is to cover the exact same
        # population of services as aws-service-index.md -- just reshaped
        # into a multi-dimensional table instead of an alphabetical list.
        index_text = _read(DOCS_DIR / "aws-service-index.md")
        index_entries = re.findall(r"^- \*\*(?P<service>.+?)\*\* `\[", index_text, re.M)
        matrix_rows = MATRIX_ROW_RE.findall(self.section_text)
        self.assertEqual(
            sorted(s.lower() for s in index_entries),
            sorted(s.lower() for s in matrix_rows),
            "consolidated matrix service set does not match "
            "aws-service-index.md's service set",
        )

    def test_matrix_links_back_to_service_index(self):
        self.assertIn("aws-service-index.md", self.section_text)


DOMAIN_LAST_VERIFIED_RE = re.compile(r"\*\*Last verified:\*\*\s*(?P<date>\d{4}-\d{2}-\d{2})")
BEDROCK_LAST_VERIFIED_RE = re.compile(
    r"last verified\W{0,6}(?P<date>\d{4}-\d{2}-\d{2})", re.IGNORECASE
)

DOMAIN_GUIDE_FILENAMES = [
    "domain-1-fundamentals-of-ai-and-ml.md",
    "domain-2-fundamentals-of-generative-ai.md",
    "domain-3-applications-of-foundation-models.md",
    "domain-4-guidelines-for-responsible-ai.md",
    "domain-5-security-compliance-governance.md",
]


class TestAwsServiceDecisionGuideLastVerifiedDateAgreesWithDomains(unittest.TestCase):
    """The decision guide's Bedrock model reference carries its own
    'Last verified' checkpoint (section 4), separate from the five domain
    guides' shared checkpoint. A prior review synced all five domain guides
    to the same date but left this doc a day behind, which made the
    series' freshness metadata look inconsistent even though nothing was
    actually stale. Guard against that drifting again."""

    def test_decision_guide_date_matches_domain_guides(self):
        domain_dates = set()
        for filename in DOMAIN_GUIDE_FILENAMES:
            text = _read(DOCS_DIR / filename)
            match = DOMAIN_LAST_VERIFIED_RE.search(text)
            self.assertIsNotNone(
                match, f"{filename} is missing a 'Last verified' date"
            )
            domain_dates.add(match.group("date"))

        self.assertEqual(
            len(domain_dates),
            1,
            f"domain guides disagree on their 'Last verified' date: {domain_dates}",
        )
        domain_date = next(iter(domain_dates))

        decision_guide_text = _read(DOC_PATH)
        section_match = re.search(
            r"^##\s+4\.\s+Bedrock model reference.*?(?=^## |\Z)",
            decision_guide_text,
            re.M | re.S,
        )
        self.assertIsNotNone(
            section_match, "could not locate the Bedrock model reference section"
        )
        bedrock_match = BEDROCK_LAST_VERIFIED_RE.search(section_match.group(0))
        self.assertIsNotNone(
            bedrock_match,
            "Bedrock model reference section is missing a 'Last verified' date",
        )

        self.assertEqual(
            bedrock_match.group("date"),
            domain_date,
            "aws-service-decision-guide.md's 'Last verified' date "
            f"({bedrock_match.group('date')}) has drifted from the domain "
            f"guides' shared date ({domain_date}); the whole series should "
            "stay in sync",
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
