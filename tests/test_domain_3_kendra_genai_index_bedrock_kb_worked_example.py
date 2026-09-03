"""Structural validation for the "Worked example: building a
product-knowledge assistant using Kendra's GenAI Index as a Bedrock
Knowledge Base data source" subsection added to
docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 3's RAG section (Section 3) and
docs/aws-service-decision-guide.md's "Branch expansion: Amazon Kendra +
Bedrock vs. Bedrock Knowledge Bases alone" both describe, at the decision-
tree/exam-tip level, that an existing Amazon Kendra GenAI Index can be
reused as a Bedrock Knowledge Base's retriever instead of standing up a
second vector store -- but neither showed a concrete worked example of the
integration (setup steps, cost trade-offs, latency trade-offs) the way
Section 3's earlier "Worked example: Selecting a vector store for a
compliance-document Q&A assistant" does for the greenfield OpenSearch/
Aurora/Kendra choice. These tests guard the new subsection: it must exist
immediately after that earlier worked example (still inside Section 3, the
RAG section, before Section 4), walk through a concrete setup, compare cost
and latency against Aurora + pgvector and OpenSearch Serverless, land on an
explicit choice, and cross-link to aws-service-decision-guide.md's branch
expansion (in both directions).

Run with:
    python3 -m unittest tests/test_domain_3_kendra_genai_index_bedrock_kb_worked_example.py -v
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOMAIN_3_PATH = (
    REPO_ROOT / "docs" / "domain-3-applications-of-foundation-models.md"
)
DECISION_GUIDE_PATH = REPO_ROOT / "docs" / "aws-service-decision-guide.md"

HEADING = (
    "#### Worked example: building a product-knowledge assistant using "
    "Kendra's GenAI Index as a Bedrock Knowledge Base data source"
)
PRIOR_HEADING = (
    "#### Worked Example: Selecting a vector store for a "
    "compliance-document Q&A assistant"
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _section(text, start_heading, end_heading_regex=r"\n#{1,4} "):
    """Return the text between a literal start_heading and the next
    heading (level 1-4), or end of file."""
    start = text.index(start_heading)
    rest = text[start + len(start_heading):]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain3KendraGenAIIndexBedrockKBWorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOMAIN_3_PATH)
        cls.section = _section(cls.text, HEADING)

    def test_worked_example_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_appears_immediately_after_the_vector_store_worked_example(self):
        prior_pos = self.text.index(PRIOR_HEADING)
        heading_pos = self.text.index(HEADING)
        self.assertLess(
            prior_pos,
            heading_pos,
            "expected the new worked example to come after the existing "
            "vector store worked example",
        )
        between = self.text[prior_pos + len(PRIOR_HEADING) : heading_pos]
        # Nothing at heading level 1-4 should appear between the two --
        # this must be the very next subsection, still inside Section 3.
        self.assertNotRegex(
            between,
            r"^#{1,4} ",
            "expected no other heading between the two worked examples",
        )

    def test_appears_inside_section_3_before_section_4(self):
        section_3_pos = self.text.index(
            "## 3. Retrieval Augmented Generation (RAG) and Amazon "
            "Bedrock Knowledge Bases"
        )
        section_4_pos = self.text.index(
            "## 4. Fine-tuning vs. continued pre-training vs. RAG vs. "
            "prompt engineering"
        )
        heading_pos = self.text.index(HEADING)
        self.assertLess(section_3_pos, heading_pos)
        self.assertLess(heading_pos, section_4_pos)

    def test_explains_what_a_genai_index_is(self):
        self.assertRegex(self.section, r"(?i)genai index")
        self.assertRegex(self.section, r"(?i)index type")
        self.assertRegex(self.section, r"(?i)retriever")

    def test_scenario_reuses_an_existing_kendra_deployment(self):
        self.assertRegex(self.section, r"(?i)already (runs|exists|operates)")
        self.assertRegex(self.section, r"(?i)product-knowledge assistant")

    def test_covers_setup_steps(self):
        # Expect a numbered walkthrough of concrete setup steps.
        self.assertRegex(self.section, r"(?i)setup walkthrough")
        self.assertRegex(self.section, r"(?m)^1\. \*\*")
        self.assertRegex(self.section, r"(?i)kendra:retrieve")

    def test_compares_cost_against_aurora_and_opensearch(self):
        self.assertRegex(self.section, r"(?i)cost trade-offs")
        self.assertRegex(self.section, r"(?i)opensearch serverless")
        self.assertRegex(self.section, r"(?i)aurora \+ pgvector|aurora.{0,20}pgvector")
        self.assertRegex(self.section, r"(?i)embedding cost")

    def test_covers_latency_trade_offs(self):
        self.assertRegex(self.section, r"(?i)latency trade-offs")
        self.assertRegex(self.section, r"(?i)retrieval hop")

    def test_makes_an_explicit_choice(self):
        self.assertRegex(
            self.section,
            r"(?i)\*\*choice:\*\*\s*reuse the existing kendra genai index",
            "expected an explicit, unambiguous choice statement",
        )

    def test_explains_when_alternatives_would_win_instead(self):
        self.assertRegex(self.section, r"(?i)when the alternatives would win instead")
        self.assertRegex(self.section, r"(?i)no kendra deployment exists yet")

    def test_has_an_exam_tip(self):
        self.assertRegex(self.section, r"> \*\*Exam tip:\*\*")

    def test_cross_links_to_aws_service_decision_guide_branch_expansion(self):
        self.assertIn(
            "aws-service-decision-guide.md#branch-expansion-amazon-kendra-"
            "bedrock-vs-bedrock-knowledge-bases-alone",
            self.section,
        )

    def test_is_a_single_self_contained_subsection_with_no_new_headings(self):
        nested_headings = re.findall(r"^#{1,6} .+$", self.section, re.M)
        self.assertEqual(
            nested_headings,
            [],
            f"worked example should not contain nested headings: {nested_headings!r}",
        )


class TestAwsServiceDecisionGuideCrossLinksToKendraGenAIWorkedExample(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DECISION_GUIDE_PATH)

    def test_branch_expansion_links_to_the_domain_3_worked_example(self):
        self.assertIn(
            "domain-3-applications-of-foundation-models.md#worked-example-"
            "building-a-product-knowledge-assistant-using-kendras-genai-"
            "index-as-a-bedrock-knowledge-base-data-source",
            self.text,
        )

    def test_link_sits_within_the_kendra_bedrock_branch_expansion_section(self):
        branch_pos = self.text.index(
            "### Branch expansion: Amazon Kendra + Bedrock vs. Bedrock "
            "Knowledge Bases alone"
        )
        next_heading = re.search(r"\n### ", self.text[branch_pos + 10 :])
        end = (
            branch_pos + 10 + next_heading.start()
            if next_heading
            else len(self.text)
        )
        section = self.text[branch_pos:end]
        self.assertIn("domain-3-applications-of-foundation-models.md#worked-example-", section)


if __name__ == "__main__":
    unittest.main()
