"""Structural validation for docs/domain-4-guidelines-for-responsible-ai.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. What *can* regress silently is the
required structure of each domain study guide (README.md promises every
domain doc covers its task statements, includes worked AWS examples, and
ends with a practice-question set + answer key). These tests assert that
structure directly against the rendered Markdown so a future edit that
drops a required section, mismatches the question/answer count, or forgets
an AWS service is caught automatically instead of only in manual review.

Mirrors the conventions established in tests/test_domain_2_study_guide.py.

Run with:
    python3 -m unittest tests/test_domain_4_study_guide.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-4-guidelines-for-responsible-ai.md"
)

# Topic areas the task description requires as their own section.
REQUIRED_TOPIC_HEADINGS = [
    "Core dimensions of responsible AI",
    "Identifying bias and fairness issues in training data and model outputs",
    "AWS tools for responsible AI",
    "Legal and ethical considerations",
    "Balancing model performance and interpretability",
]

# The 8 responsible AI dimensions the task explicitly requires.
REQUIRED_RESPONSIBLE_AI_DIMENSIONS = [
    "Fairness",
    "Explainability",
    "Privacy and security",
    "Transparency",
    "Veracity and robustness",
    "Governance",
    "Safety",
    "Controllability",
]

# AWS tools for responsible AI the task explicitly calls out.
REQUIRED_AWS_TOOLS = [
    "Amazon SageMaker Clarify",
    "SageMaker Model Cards",
    "Guardrails for Amazon Bedrock",
    "AI Service Cards",
]

# The six bias types the bias-detection-and-mitigation workflow diagram
# must surface as distinct nodes.
REQUIRED_BIAS_TYPES = [
    "Sampling bias",
    "Measurement bias",
    "Label / human bias",
    "Historical bias",
    "Exclusion bias",
    "Aggregation bias",
]

# The mitigation tools the bias-detection-and-mitigation workflow diagram
# must surface as distinct nodes.
REQUIRED_BIAS_MITIGATION_TOOLS = [
    "Guardrails for Amazon Bedrock",
    "SageMaker Model Cards",
    "Amazon A2I",
]

# Legal/ethical considerations the task explicitly requires.
REQUIRED_LEGAL_ETHICAL_TOPICS = [
    "intellectual property",
    "data privacy",
    "toxicity",
    "environmental impact",
]

MIN_QUESTIONS = 15
MAX_QUESTIONS = 20


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex=r"\n## "):
    """Return the text between a heading matching start_heading_regex and
    the next top-level (##) heading, or end of file."""
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain4StudyGuideExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected study guide at {DOC_PATH}",
        )


class TestDomain4StudyGuideStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_has_domain_overview(self):
        self.assertRegex(
            self.text, r"^# Domain 4: Guidelines for Responsible AI"
        )
        self.assertIn("## Domain overview", self.text)

    def test_has_every_required_topic_section(self):
        for heading in REQUIRED_TOPIC_HEADINGS:
            with self.subTest(heading=heading):
                self.assertIn(
                    heading,
                    self.text,
                    f"missing required topic section: {heading!r}",
                )

    def test_every_topic_section_has_an_exam_tip(self):
        # Each major numbered section ("## 1. ..." through "## 5. ...")
        # must contain an "Exam tip" callout per the required structure.
        sections = re.findall(r"\n## [1-5]\. .*?(?=\n## |\Z)", self.text, re.S)
        self.assertEqual(
            len(sections), 5, "expected exactly 5 numbered topic sections"
        )
        for section in sections:
            heading = section.strip().splitlines()[0]
            with self.subTest(section=heading):
                self.assertIn(
                    "Exam tip:",
                    section,
                    f"section {heading!r} is missing an 'Exam tip' callout",
                )

    def test_every_topic_section_has_an_aws_example(self):
        sections = re.findall(r"\n## [1-5]\. .*?(?=\n## |\Z)", self.text, re.S)
        for section in sections:
            heading = section.strip().splitlines()[0]
            with self.subTest(section=heading):
                self.assertIn(
                    "AWS example:",
                    section,
                    f"section {heading!r} is missing an 'AWS example' callout",
                )

    def test_has_comparison_table(self):
        table_section = _section(self.text, r"\n## Comparison table")
        # A markdown table needs a header separator row like |---|---|
        self.assertRegex(table_section, r"\|\s*-{2,}\s*\|")
        for tool in REQUIRED_AWS_TOOLS:
            with self.subTest(tool=tool):
                self.assertIn(tool, table_section)

    def test_all_required_aws_tools_mentioned_in_doc(self):
        for tool in REQUIRED_AWS_TOOLS:
            with self.subTest(tool=tool):
                self.assertIn(tool, self.text)

    def test_all_responsible_ai_dimensions_covered(self):
        dimensions_section = _section(
            self.text, r"\n## 1\. Core dimensions of responsible AI"
        )
        for dimension in REQUIRED_RESPONSIBLE_AI_DIMENSIONS:
            with self.subTest(dimension=dimension):
                self.assertRegex(
                    dimensions_section,
                    re.compile(re.escape(dimension), re.IGNORECASE),
                    f"core dimensions section missing dimension: {dimension!r}",
                )

    def test_core_dimensions_section_has_relationship_diagrams(self):
        # The section must include a visual diagram of how the 8
        # dimensions interconnect, plus a diagram mapping each dimension
        # to the AWS tool(s) that support it (not just prose).
        dimensions_section = _section(
            self.text, r"\n## 1\. Core dimensions of responsible AI"
        )
        mermaid_blocks = re.findall(
            r"```mermaid\n(.*?)```", dimensions_section, re.S
        )
        self.assertGreaterEqual(
            len(mermaid_blocks),
            2,
            "core dimensions section should contain a dimensions-relationship "
            "diagram and a dimension-to-AWS-tool mapping diagram",
        )
        combined_diagrams = "\n".join(mermaid_blocks)
        for dimension in REQUIRED_RESPONSIBLE_AI_DIMENSIONS:
            with self.subTest(dimension=dimension):
                self.assertRegex(
                    combined_diagrams,
                    re.compile(
                        re.escape(dimension.split(" and ")[0]), re.IGNORECASE
                    ),
                    f"relationship diagrams missing dimension node: {dimension!r}",
                )
        for tool in REQUIRED_AWS_TOOLS:
            with self.subTest(tool=tool):
                self.assertIn(
                    tool,
                    combined_diagrams,
                    f"AWS-tool mapping diagram missing tool: {tool!r}",
                )

    def test_bias_section_covers_bias_and_fairness(self):
        bias_section = _section(
            self.text,
            r"\n## 2\. Identifying bias and fairness issues in training "
            r"data and model outputs",
        )
        for term in ["bias", "variance", "fairness", "mitigat"]:
            with self.subTest(term=term):
                self.assertRegex(
                    bias_section,
                    re.compile(re.escape(term), re.IGNORECASE),
                    f"bias/fairness section missing term: {term!r}",
                )

    def test_bias_section_opens_with_bias_vs_variance_clarification(self):
        # Regression test: the bias/fairness section must open with a
        # dedicated subsection distinguishing statistical bias/variance
        # (Domain 1, tied to overfitting/underfitting) from fairness bias
        # (systematic disadvantage against a group), so readers who jump
        # straight into Domain 4 don't conflate the two meanings of "bias".
        bias_section = _section(
            self.text,
            r"\n## 2\. Identifying bias and fairness issues in training "
            r"data and model outputs",
        )
        heading_match = re.search(
            r"### Bias \W+ Variance: Terminology Clarification", bias_section
        )
        self.assertIsNotNone(
            heading_match,
            "bias/fairness section is missing the 'Bias vs. Variance: "
            "Terminology Clarification' subsection",
        )
        clarification_section = _section(
            bias_section,
            r"\n### Bias \W+ Variance: Terminology Clarification",
            end_heading_regex=r"\n\*\*Bias\*\* in ML",
        )
        for term in ["underfitting", "overfitting", "Domain 1"]:
            with self.subTest(term=term):
                self.assertIn(
                    term,
                    clarification_section,
                    f"bias-vs-variance clarification missing term: {term!r}",
                )
        self.assertRegex(
            clarification_section,
            re.compile(r"statistical bias", re.IGNORECASE),
            "bias-vs-variance clarification should explicitly name "
            "'statistical bias'",
        )
        self.assertRegex(
            clarification_section,
            re.compile(r"fairness bias", re.IGNORECASE),
            "bias-vs-variance clarification should explicitly name "
            "'fairness bias'",
        )
        # The clarification must appear before the rest of the section's
        # existing bias-type content (e.g. sampling bias), i.e. it must be
        # the very first thing under the "## 2." heading.
        self.assertLess(
            heading_match.start(),
            bias_section.index("Sampling bias"),
            "the terminology clarification subsection must come before the "
            "rest of Section 2's content",
        )

    def test_bias_vs_variance_clarification_forward_references_clarify(self):
        # Regression test: the terminology clarification must forward-
        # reference Amazon SageMaker Clarify and make explicit that it
        # measures fairness bias specifically, not statistical bias or
        # variance, so readers don't assume Clarify's metrics have
        # anything to do with the Domain 1 bias-variance trade-off.
        bias_section = _section(
            self.text,
            r"\n## 2\. Identifying bias and fairness issues in training "
            r"data and model outputs",
        )
        clarification_section = _section(
            bias_section,
            r"\n### Bias \W+ Variance: Terminology Clarification",
            end_heading_regex=r"\n\*\*Bias\*\* in ML",
        )
        self.assertRegex(
            clarification_section,
            re.compile(r"Amazon\s+SageMaker\s+Clarify"),
            "bias-vs-variance clarification should forward-reference "
            "Amazon SageMaker Clarify",
        )
        self.assertRegex(
            clarification_section,
            re.compile(r"fairness bias", re.IGNORECASE),
            "clarification's Clarify forward-reference should tie Clarify "
            "to fairness bias specifically",
        )
        self.assertRegex(
            clarification_section,
            re.compile(
                r"Clarify[^.]*(?:no role|not[^.]*statistical bias"
                r"|nothing to do with statistical bias)",
                re.IGNORECASE,
            ),
            "clarification should explicitly state Clarify does not "
            "measure statistical bias/variance",
        )

    def test_bias_section_has_detection_and_mitigation_workflow_diagram(self):
        # The bias section must include a visual workflow diagram going
        # from bias type -> detection method -> mitigation tool, not just
        # prose, mirroring the two diagrams already present in Section 1.
        bias_section = _section(
            self.text,
            r"\n## 2\. Identifying bias and fairness issues in training "
            r"data and model outputs",
        )
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", bias_section, re.S)
        self.assertGreaterEqual(
            len(mermaid_blocks),
            1,
            "bias section should contain a bias detection and mitigation "
            "workflow diagram",
        )
        combined_diagrams = "\n".join(mermaid_blocks)
        for bias_type in REQUIRED_BIAS_TYPES:
            with self.subTest(bias_type=bias_type):
                self.assertRegex(
                    combined_diagrams,
                    re.compile(re.escape(bias_type), re.IGNORECASE),
                    f"bias workflow diagram missing bias type node: {bias_type!r}",
                )
        self.assertRegex(
            combined_diagrams,
            re.compile(r"pre-training", re.IGNORECASE),
            "bias workflow diagram missing a pre-training detection path",
        )
        self.assertRegex(
            combined_diagrams,
            re.compile(r"post-training", re.IGNORECASE),
            "bias workflow diagram missing a post-training detection path",
        )
        self.assertIn(
            "DPL",
            combined_diagrams,
            "bias workflow diagram missing the DPL pre-training metric",
        )
        self.assertRegex(
            combined_diagrams,
            re.compile(r"disparate impact", re.IGNORECASE),
            "bias workflow diagram missing the disparate impact post-training metric",
        )
        for tool in REQUIRED_BIAS_MITIGATION_TOOLS:
            with self.subTest(tool=tool):
                self.assertIn(
                    tool,
                    combined_diagrams,
                    f"bias workflow diagram missing mitigation tool: {tool!r}",
                )

    def test_bias_section_has_pre_vs_post_training_decision_tree_diagram(self):
        # Regression test: Section 2 must include a second, standalone
        # Mermaid diagram dedicated to the pre-training vs. post-training
        # bias detection decision ("do you have a trained model yet?"),
        # distinct from the broader six-bias-type detection-and-mitigation
        # workflow diagram tested above. This distinction is exercised by
        # cross-domain scenario questions 2, 13, and 19.
        bias_section = _section(
            self.text,
            r"\n## 2\. Identifying bias and fairness issues in training "
            r"data and model outputs",
        )
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", bias_section, re.S)
        self.assertGreaterEqual(
            len(mermaid_blocks),
            2,
            "bias section should contain both the six-bias-type workflow "
            "diagram and a dedicated pre-training vs. post-training "
            "decision-tree diagram",
        )
        decision_tree_candidates = [
            block
            for block in mermaid_blocks
            if re.search(r"trained model yet", block, re.IGNORECASE)
        ]
        self.assertEqual(
            len(decision_tree_candidates),
            1,
            "expected exactly one Mermaid diagram asking whether a "
            "trained model exists yet",
        )
        decision_tree = decision_tree_candidates[0]
        self.assertRegex(
            decision_tree,
            re.compile(r"pre-training metrics", re.IGNORECASE),
            "decision tree missing the pre-training metrics branch",
        )
        self.assertRegex(
            decision_tree,
            re.compile(r"post-training metrics", re.IGNORECASE),
            "decision tree missing the post-training metrics branch",
        )
        self.assertIn(
            "DPL",
            decision_tree,
            "decision tree missing the DPL pre-training metric",
        )
        self.assertRegex(
            decision_tree,
            re.compile(r"class imbalance", re.IGNORECASE),
            "decision tree missing the class imbalance pre-training metric",
        )
        self.assertRegex(
            decision_tree,
            re.compile(r"disparate impact", re.IGNORECASE),
            "decision tree missing the disparate impact post-training metric",
        )
        self.assertRegex(
            decision_tree,
            re.compile(r"accuracy/recall difference", re.IGNORECASE),
            "decision tree missing the accuracy/recall difference "
            "post-training metric",
        )
        # The prose immediately around the diagram should tie it back to
        # the practice questions that test this exact branch.
        diagram_start = bias_section.index(decision_tree)
        surrounding = bias_section[
            max(0, diagram_start - 800) : diagram_start + len(decision_tree) + 800
        ]
        self.assertRegex(
            surrounding,
            re.compile(r"cross-domain-scenario-questions\.md"),
            "pre- vs. post-training decision tree should cross-reference "
            "cross-domain-scenario-questions.md",
        )

    def test_aws_tools_section_covers_required_tools(self):
        tools_section = _section(
            self.text, r"\n## 3\. AWS tools for responsible AI"
        )
        for tool in REQUIRED_AWS_TOOLS:
            with self.subTest(tool=tool):
                self.assertIn(tool, tools_section)

    def test_aws_tools_section_cross_links_domain_3_bedrock_features(self):
        # Guardrails for Amazon Bedrock is covered here (responsible-AI
        # framing) and again in Domain 3 §5 (runtime implementation detail).
        # Readers studying one should be pointed at the other.
        tools_section = _section(
            self.text, r"\n## 3\. AWS tools for responsible AI"
        )
        self.assertIn(
            "domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features",
            tools_section,
            "AWS tools section should cross-link Domain 3 §5's "
            "implementation detail for Guardrails",
        )

    def test_legal_ethical_section_covers_required_topics(self):
        legal_section = _section(
            self.text, r"\n## 4\. Legal and ethical considerations"
        )
        for topic in REQUIRED_LEGAL_ETHICAL_TOPICS:
            with self.subTest(topic=topic):
                self.assertRegex(
                    legal_section,
                    re.compile(re.escape(topic), re.IGNORECASE),
                    f"legal/ethical section missing topic: {topic!r}",
                )

    def test_performance_interpretability_section_covers_tradeoff(self):
        tradeoff_section = _section(
            self.text,
            r"\n## 5\. Balancing model performance and interpretability",
        )
        for term in ["interpretability", "performance", "accuracy"]:
            with self.subTest(term=term):
                self.assertRegex(
                    tradeoff_section,
                    re.compile(re.escape(term), re.IGNORECASE),
                    f"performance/interpretability section missing term: {term!r}",
                )

    def test_has_key_terms_glossary_with_substantial_coverage(self):
        glossary = _section(self.text, r"\n## Key terms glossary")
        entries = re.findall(r"^- \*\*.+?\*\*", glossary, re.M)
        self.assertGreaterEqual(
            len(entries),
            15,
            "key terms glossary should cover at least 15 terms",
        )


class TestDomain4PracticeQuestions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.questions_section = _section(
            cls.text, r"\n## Practice questions", r"\n## Answer key"
        )
        cls.answers_section = _section(
            cls.text, r"\n## Answer key and explanations"
        )

    def _numbered_items(self, section_text):
        return re.findall(r"^(\d+)\.\s", section_text, re.M)

    def test_question_count_within_required_range(self):
        numbers = self._numbered_items(self.questions_section)
        self.assertEqual(
            [int(n) for n in numbers],
            list(range(1, len(numbers) + 1)),
            "practice questions must be sequentially numbered starting at 1",
        )
        self.assertGreaterEqual(len(numbers), MIN_QUESTIONS)
        self.assertLessEqual(len(numbers), MAX_QUESTIONS)

    def test_every_question_has_at_least_four_options(self):
        blocks = re.split(r"\n(?=\d+\.\s)", self.questions_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
        for block in blocks:
            qnum = block.split(".", 1)[0]
            with self.subTest(question=qnum):
                options = re.findall(r"^\s*[A-E]\.\s", block, re.M)
                self.assertGreaterEqual(
                    len(options),
                    4,
                    f"question {qnum} should have at least 4 answer options",
                )

    def test_answer_key_covers_every_question_with_explanation(self):
        q_numbers = [int(n) for n in self._numbered_items(self.questions_section)]
        a_numbers = [int(n) for n in self._numbered_items(self.answers_section)]
        self.assertEqual(
            q_numbers,
            a_numbers,
            "answer key must have exactly one entry per practice question, in order",
        )

        blocks = re.split(r"\n(?=\d+\.\s)", self.answers_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
        for block in blocks:
            anum = block.split(".", 1)[0]
            with self.subTest(answer=anum):
                # Each explanation should be substantive, not just "A is correct."
                self.assertGreater(
                    len(block.strip()),
                    120,
                    f"answer {anum} explanation looks too short to justify "
                    f"the correct choice and rule out the distractors",
                )
                # Bolded letter(s) mark the stated correct choice, e.g.
                # "**B —" for single-answer or "**A and B —" for
                # multiple-response questions.
                self.assertRegex(
                    block,
                    r"\*\*[A-E](?:\s*(?:,|and)\s*[A-E])*\s*[—-]",
                    f"answer {anum} should clearly state the correct option letter(s)",
                )

    def test_every_question_is_tagged_with_a_difficulty_level(self):
        blocks = re.split(r"\n(?=\d+\.\s)", self.questions_section.strip())
        blocks = [b for b in blocks if re.match(r"^\d+\.\s", b)]
        levels_seen = set()
        for block in blocks:
            qnum = block.split(".", 1)[0]
            with self.subTest(question=qnum):
                match = re.match(
                    r"^\d+\.\s\*\*\[(Beginner|Intermediate|Advanced)\]\*\*\s",
                    block,
                )
                self.assertTrue(
                    match,
                    f"question {qnum} should start with a "
                    f"**[Beginner|Intermediate|Advanced]** difficulty tag",
                )
                if match:
                    levels_seen.add(match.group(1))
        self.assertEqual(
            levels_seen,
            {"Beginner", "Intermediate", "Advanced"},
            "practice questions should include all three difficulty levels",
        )


class TestDomain4WorkedExample(unittest.TestCase):
    """Domains 1, 2, 3, and 5 each end with a dedicated
    '## Worked example: ...' section stitching every concept in the domain
    into one continuous scenario. Domain 4 previously had only inline
    'AWS example:' callouts and no such section; these tests guard the
    worked example added to close that gap."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.toc = _section(
            cls.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        cls.section = _section(cls.text, r"\n## Worked example: .+")

    def test_worked_example_heading_exists(self):
        self.assertRegex(self.text, r"\n## Worked example: .+")

    def test_worked_example_sits_between_section_5_and_comparison_table(self):
        section_5_idx = self.text.index(
            "## 5. Balancing model performance and interpretability"
        )
        # Anchor to "\n## " (not a plain substring search) so this
        # doesn't accidentally match a nested "### Worked example: ..."
        # subsection (e.g. the confidence-threshold/Amazon A2I example
        # nested inside Section 3) instead of the top-level, closing
        # "## Worked example: " section.
        worked_example_match = re.search(r"\n## Worked example: ", self.text)
        assert worked_example_match, "no top-level '## Worked example: ' heading found"
        worked_example_idx = worked_example_match.start()
        comparison_idx = self.text.index(
            "## Comparison table: AWS responsible AI tools at a glance"
        )
        self.assertLess(section_5_idx, worked_example_idx)
        self.assertLess(worked_example_idx, comparison_idx)

    def test_worked_example_has_scenario_and_exam_tip(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_worked_example_covers_fairness_explainability_transparency_and_governance(
        self,
    ):
        for term in [
            "bias",
            "disparate impact",
            "Amazon SageMaker Clarify",
            "SHAP",
            "Model Card",
            "SageMaker Model Monitor",
            "Amazon A2I",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.section)

    def test_worked_example_has_at_least_six_numbered_steps(self):
        steps = re.findall(r"^\d+\.\s", self.section, re.M)
        self.assertGreaterEqual(
            len(steps),
            6,
            "worked example should walk through at least six numbered "
            "steps",
        )

    def test_worked_example_word_count_within_expected_range(self):
        words = re.findall(r"\w+", self.section)
        self.assertGreaterEqual(
            len(words),
            500,
            "worked example should be at least 500 words",
        )
        self.assertLessEqual(
            len(words),
            800,
            "worked example should be at most 800 words",
        )

    def test_table_of_contents_links_to_worked_example(self):
        self.assertIn("Worked example", self.toc)
        self.assertIn(
            "#worked-example-auditing-and-documenting-a-responsible-"
            "e-commerce-recommendation-engine",
            self.toc,
        )


if __name__ == "__main__":
    unittest.main()
