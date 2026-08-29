"""Structural validation for docs/aws-service-index.md.

docs/master-glossary.md and docs/GLOSSARY.md already index every domain
guide's *terms* (concepts like "overfitting" or "prompt injection")
alphabetically. They don't make it easy to answer a different, common
question: "where does this series discuss AWS service X?" -- e.g. "every
mention of Amazon SageMaker" or "all Amazon Bedrock capabilities" in one
place, without scanning past unrelated concept terms or re-reading whole
domain guides.

docs/aws-service-index.md closes that gap: a service-centric index, one
alphabetical entry per AWS service referenced anywhere across the five
domain guides, each tagged with the domain(s) `[D#, ...]` that discuss it
and linked directly to the relevant section in each tagged domain.

These tests mirror tests/test_master_glossary.py's structural checks
(existence, discoverability from README/glossary/decision-guide,
alphabetical order, no duplicates, domain-tag format, and link
resolution).

Run with:
    python3 -m unittest tests/test_aws_service_index.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
SERVICE_INDEX_PATH = DOCS_DIR / "aws-service-index.md"
README_PATH = REPO_ROOT / "README.md"

DOMAIN_FILES = {
    "1": "domain-1-fundamentals-of-ai-and-ml.md",
    "2": "domain-2-fundamentals-of-generative-ai.md",
    "3": "domain-3-applications-of-foundation-models.md",
    "4": "domain-4-guidelines-for-responsible-ai.md",
    "5": "domain-5-security-compliance-governance.md",
}

# A representative sample spanning all five domains -- enough to catch a
# regression that drops a whole domain's contribution or a specific
# heavily-referenced service.
REQUIRED_SAMPLE_SERVICES = [
    "Amazon SageMaker",  # D1, D2, D3, D4, D5
    "Amazon Bedrock",  # D2, D3, D4, D5
    "Amazon Rekognition",  # D1
    "Guardrails for Amazon Bedrock",  # D2, D3, D4, D5
    "Amazon SageMaker Clarify",  # D4
    "AWS CloudTrail",  # D5
    "AWS PrivateLink",  # D5
    "Amazon Kendra",  # D3
]

# AWS services that are referenced by name in the domain guides but were
# historically missing their own service-index entry -- regression guard
# for that specific documentation gap.
REQUIRED_FORMERLY_MISSING_AWS_SERVICES = [
    "Amazon S3",  # D1, D3, D5
    "AWS Lambda",  # D2, D3
    "Amazon EC2",  # D3
    "Amazon RDS",  # D3
    "Amazon Athena",  # D1
    "Amazon Kinesis",  # D1
    "AWS Glue",  # D1
    "Amazon Inspector",  # D5
    "AWS Shield",  # D5
    "AWS Trusted Advisor",  # D5
    "AWS Organizations",  # D5
    "Amazon VPC",  # D5
    "Amazon DynamoDB",  # D5
    "Amazon SageMaker Data Wrangler",  # D1
    "Amazon SageMaker Feature Store",  # D1
]

# The five third-party foundation model providers referenced in Bedrock
# coverage (D2, D3) that were previously missing their own entries.
REQUIRED_THIRD_PARTY_FM_PROVIDERS = [
    "Anthropic Claude",
    "Meta Llama",
    "Cohere",
    "Mistral AI",
    "Stability AI",
]

# The Amazon Nova model family variants mentioned in the AWS service
# decision guide that were previously missing their own index entries.
REQUIRED_NOVA_VARIANTS = [
    "Amazon Nova Canvas",
    "Amazon Nova Reel",
    "Amazon Nova Micro",
    "Amazon Nova Lite",
    "Amazon Nova Pro",
    "Amazon Nova Premier",
]

# - **Service** `[D1, D3]` — definition. [D1](link) · [D3](link)
ENTRY_RE = re.compile(
    r"^- \*\*(?P<service>.+?)\*\* `\[(?P<tags>D\d(?:, D\d)*)\]` — (?P<rest>.+)$",
    re.M,
)
DOMAIN_TAG_LINK_RE = re.compile(r"\[D(?P<num>\d)\]\((?P<target>[^)\s]+)\)")


def _read(path):
    return path.read_text(encoding="utf-8")


def _slugify(heading_text):
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def _heading_anchors(doc_text):
    headings = re.findall(r"^#{1,6}\s+(.*)$", doc_text, re.M)
    return {_slugify(h) for h in headings}


class TestAwsServiceIndexExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            SERVICE_INDEX_PATH.is_file(),
            f"expected AWS service index at {SERVICE_INDEX_PATH}",
        )

    def test_linked_from_readme(self):
        readme_text = _read(README_PATH)
        self.assertIn(
            "docs/aws-service-index.md",
            readme_text,
            "README.md must link to the AWS service index so learners can "
            "discover it",
        )

    def test_linked_from_master_glossary(self):
        text = _read(DOCS_DIR / "master-glossary.md")
        self.assertIn(
            "aws-service-index.md",
            text,
            "master-glossary.md should cross-reference the service index",
        )

    def test_linked_from_glossary(self):
        text = _read(DOCS_DIR / "GLOSSARY.md")
        self.assertIn(
            "aws-service-index.md",
            text,
            "GLOSSARY.md should cross-reference the service index",
        )

    def test_linked_from_decision_guide(self):
        text = _read(DOCS_DIR / "aws-service-decision-guide.md")
        self.assertIn(
            "aws-service-index.md",
            text,
            "aws-service-decision-guide.md should cross-reference the "
            "service index",
        )


class TestAwsServiceIndexCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(SERVICE_INDEX_PATH)
        cls.entries = ENTRY_RE.findall(cls.text)

    def test_has_title(self):
        self.assertRegex(self.text, r"^# .*AWS Service Index")

    def test_found_entries(self):
        self.assertGreaterEqual(
            len(self.entries),
            30,
            "expected the AWS service index to contain at least 30 "
            "service entries across the five domain guides",
        )

    def test_covers_required_sample_services(self):
        services = [service for service, _tags, _rest in self.entries]
        for service in REQUIRED_SAMPLE_SERVICES:
            with self.subTest(service=service):
                self.assertIn(
                    service,
                    services,
                    f"AWS service index missing service entry: {service!r}",
                )

    def test_covers_formerly_missing_aws_services(self):
        services = [service for service, _tags, _rest in self.entries]
        for service in REQUIRED_FORMERLY_MISSING_AWS_SERVICES:
            with self.subTest(service=service):
                self.assertIn(
                    service,
                    services,
                    f"AWS service index missing service entry: {service!r}",
                )

    def test_covers_third_party_foundation_model_providers(self):
        services = [service for service, _tags, _rest in self.entries]
        for provider in REQUIRED_THIRD_PARTY_FM_PROVIDERS:
            with self.subTest(provider=provider):
                self.assertIn(
                    provider,
                    services,
                    "AWS service index missing third-party foundation "
                    f"model provider entry: {provider!r}",
                )

    def test_covers_nova_model_family_variants(self):
        services = [service for service, _tags, _rest in self.entries]
        for variant in REQUIRED_NOVA_VARIANTS:
            with self.subTest(variant=variant):
                self.assertIn(
                    variant,
                    services,
                    f"AWS service index missing Amazon Nova variant entry: {variant!r}",
                )

    def test_entries_are_sorted_alphabetically(self):
        sort_keys = [service.lower() for service, _tags, _rest in self.entries]
        self.assertEqual(
            sort_keys,
            sorted(sort_keys),
            "AWS service index entries must be in alphabetical order so it "
            "can be used as an index",
        )

    def test_no_duplicate_services(self):
        seen = set()
        duplicates = set()
        for service, _tags, _rest in self.entries:
            key = service.lower()
            if key in seen:
                duplicates.add(service)
            seen.add(key)
        self.assertFalse(
            duplicates,
            f"AWS service index has duplicate service entries: {sorted(duplicates)}",
        )

    def test_titan_entry_does_not_claim_image_generation(self):
        self.assertNotIn(
            "text, embeddings, image generation",
            self.text,
            "Amazon Titan entry should not claim image-generation "
            "capability; that moved to Amazon Nova Canvas",
        )
        titan_line = next(
            line
            for line in self.text.splitlines()
            if line.startswith("- **Amazon Titan**")
        )
        self.assertIn("Amazon Nova Canvas", titan_line)

    def test_links_reach_every_domain_guide(self):
        all_targets = []
        for _service, _tags, rest in self.entries:
            all_targets.extend(t for _num, t in DOMAIN_TAG_LINK_RE.findall(rest))
        for filename in DOMAIN_FILES.values():
            with self.subTest(domain=filename):
                self.assertTrue(
                    any(t.split("#", 1)[0] == filename for t in all_targets),
                    f"AWS service index has no tagged link into {filename}",
                )

    def test_multi_domain_services_have_multiple_tags(self):
        # Spot-check known cross-domain services actually carry >1 tag,
        # since that's the entire value proposition of this index over
        # reading a single domain's own comparison table.
        multi_domain_services = {
            "Amazon SageMaker",
            "Amazon Bedrock",
            "Guardrails for Amazon Bedrock",
        }
        by_service = {service: tags for service, tags, _rest in self.entries}
        for service in multi_domain_services:
            with self.subTest(service=service):
                self.assertIn(service, by_service)
                self.assertGreaterEqual(
                    len(by_service[service].split(",")),
                    2,
                    f"expected {service!r} to be tagged with 2+ domains",
                )


class TestAwsServiceIndexDomainTags(unittest.TestCase):
    """Verify every entry's tag set is non-empty, matches the domains it
    links to, and every link resolves to a real file and heading."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read(SERVICE_INDEX_PATH)
        cls.entries = ENTRY_RE.findall(cls.text)
        cls.anchor_cache = {}

    def _anchors_for(self, filename):
        if filename not in self.anchor_cache:
            target_path = (DOCS_DIR / filename).resolve()
            self.anchor_cache[filename] = _heading_anchors(_read(target_path))
        return self.anchor_cache[filename]

    def test_every_entry_tag_matches_its_links(self):
        for service, tags, rest in self.entries:
            with self.subTest(service=service):
                tag_nums = {t.strip()[1:] for t in tags.split(",")}
                link_matches = DOMAIN_TAG_LINK_RE.findall(rest)
                link_nums = {num for num, _target in link_matches}
                self.assertTrue(
                    tag_nums, f"entry {service!r} has an empty domain tag"
                )
                self.assertEqual(
                    tag_nums,
                    link_nums,
                    f"entry {service!r} has domain tag [{tags}] that does "
                    f"not match its D#(...) links {link_matches!r}",
                )

    def test_every_tag_link_target_file_exists_with_anchor(self):
        for service, _tags, rest in self.entries:
            for num, target in DOMAIN_TAG_LINK_RE.findall(rest):
                with self.subTest(service=service, target=target):
                    file_part, _, anchor = target.partition("#")
                    target_path = (DOCS_DIR / file_part).resolve()
                    self.assertTrue(
                        target_path.is_file(),
                        f"linked file does not exist: {file_part!r} "
                        f"(resolved to {target_path})",
                    )
                    self.assertEqual(
                        file_part,
                        DOMAIN_FILES[num],
                        f"entry {service!r} tags D{num} but links to "
                        f"{file_part!r}, not {DOMAIN_FILES[num]!r}",
                    )
                    if anchor:
                        self.assertIn(
                            anchor,
                            self._anchors_for(file_part),
                            f"anchor #{anchor} does not match any heading "
                            f"slug in {file_part} for service {service!r}",
                        )


if __name__ == "__main__":
    unittest.main()
