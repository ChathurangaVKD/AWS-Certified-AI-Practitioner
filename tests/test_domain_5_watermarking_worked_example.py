"""Structural validation for the "Worked example: tracing provenance
through a Titan Image Generator watermarking pipeline" subsection added
to docs/domain-5-security-compliance-governance.md.

The gap this covers: docs/aws-service-decision-guide.md (line 343)
already names Amazon Titan Image Generator G1 v2 and its "built-in
invisible watermarking for provenance," but no domain guide explained
what that watermark is for or traced it end to end. The only other
"watermark" mentions in the repo (Domain 2 and Domain 3) are about the
*opposite* concept -- negative prompting to *exclude* a visible
watermark/logo from generated image content -- which this new worked
example must explicitly distinguish itself from. These tests guard the
new worked example: it must exist as a "####"-level subsection nested
inside the "Source citation and data lineage" subsection (after it,
before "Common security threats..."), must not perturb the
standalone/nested worked-example counts asserted elsewhere, must cover
the generation/embedding/detection/governance pipeline stages using
Titan Image Generator and Bedrock vocabulary, must explicitly
distinguish itself from the negative-prompting watermark-removal
technique, must close with an exam tip, and must fall within the
requested ~250-350 word range. It also guards that the existing source
citation/data lineage exam tip now links forward to this new
subsection.

Mirrors the conventions established in
tests/test_domain_5_cost_capping_worked_example.py.

Run with:
    python3 -m unittest tests/test_domain_5_watermarking_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)

HEADING = (
    "#### Worked example: tracing provenance through a Titan Image "
    "Generator watermarking pipeline"
)
HEADING_REGEX = (
    r"\n#### Worked example: tracing provenance through a Titan Image "
    r"Generator watermarking pipeline"
)
SOURCE_CITATION_HEADING = "### Source citation and data lineage"
SECURITY_THREATS_HEADING = (
    "### Common security threats to AI systems and how to mitigate them"
)
FORWARD_LINK = (
    "[worked example below]"
    "(#worked-example-tracing-provenance-through-a-titan-image-generator-"
    "watermarking-pipeline)"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n#{1,4} "):
    """Return the text between a heading matching start_heading_regex and
    the next heading of the same or higher level, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain5WatermarkingWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(cls.text, HEADING_REGEX)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_worked_example_is_nested_between_source_citation_and_security_threats(
        self,
    ):
        source_citation_pos = self.text.index(SOURCE_CITATION_HEADING)
        heading_pos = self.text.index(HEADING)
        security_threats_pos = self.text.index(SECURITY_THREATS_HEADING)
        self.assertLess(source_citation_pos, heading_pos)
        self.assertLess(heading_pos, security_threats_pos)

    def test_does_not_change_standalone_or_level_3_worked_example_counts(
        self,
    ):
        # The new subsection is a level-4 heading nested inside the
        # existing "Source citation and data lineage" subsection, not a
        # new standalone "## Worked example" section and not a new
        # "### Worked example" subsection, so it must not perturb the
        # counts asserted in tests/test_domain_5_study_guide.py or
        # tests/test_documentation_structure.py.
        standalone = re.findall(r"^## Worked example:", self.text, re.M)
        self.assertEqual(len(standalone), 2)
        nested_level_3 = re.findall(r"^### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_3), 0)

    def test_is_the_fourth_level_4_nested_worked_example_in_domain_5(self):
        # Pre-existing level-4 nested worked examples: "capping cost under
        # three different threat models", "sizing service quotas for a
        # multi-team Bedrock workload", and "shared responsibility for a
        # SageMaker-to-Bedrock fine-tuning pipeline". This one is the
        # fourth.
        nested_level_4 = re.findall(r"^#### Worked example:", self.text, re.M)
        self.assertEqual(len(nested_level_4), 4)

    def test_covers_titan_image_generator_and_bedrock(self):
        for expected in [
            "Titan Image Generator G1 v2",
            "Amazon Bedrock",
            "InvokeModel",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_covers_generation_embedding_detection_pipeline_stages(self):
        for expected in [
            "**Generation.**",
            "**Embedding.**",
            "**Downstream detection and verification.**",
            "**Governance framing.**",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.section)

    def test_distinguishes_from_negative_prompting_watermark_removal(self):
        self.assertIn("negative prompting", self.section)
        self.assertIn("visible", self.section)

    def test_has_a_closing_exam_tip(self):
        self.assertIn("**Exam tip:**", self.section)

    def test_word_count_is_within_requested_range(self):
        body = self.section
        # Strip a leading heading line if present in the extracted
        # section (the section starts right after the heading match, so
        # this is a defensive no-op in practice, kept for robustness).
        body = re.sub(r"^#{1,4} .*\n", "", body)
        words = body.split()
        self.assertGreaterEqual(len(words), 250)
        self.assertLessEqual(len(words), 350)

    def test_source_citation_exam_tip_links_forward_to_the_worked_example(
        self,
    ):
        source_citation_section = _section(
            self.text,
            re.escape(SOURCE_CITATION_HEADING),
            r"\n#{1,4} ",
        )
        self.assertIn(FORWARD_LINK, source_citation_section)


if __name__ == "__main__":
    unittest.main()
