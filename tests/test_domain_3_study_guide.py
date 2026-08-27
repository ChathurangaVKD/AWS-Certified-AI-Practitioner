"""Structural validation for docs/domain-3-applications-of-foundation-models.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. What *can* regress silently is the
required structure of each domain study guide (README.md promises every
domain doc covers its task statements, includes worked AWS examples, and
ends with a practice-question set + answer key). These tests assert that
structure directly against the rendered Markdown so a future edit that
drops a required section, mismatches the question/answer count, or forgets
an AWS service is caught automatically instead of only in manual review.

Mirrors the conventions established in tests/test_domain_2_study_guide.py
and tests/test_domain_4_study_guide.py.

Run with:
    python3 -m unittest tests/test_domain_3_study_guide.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-3-applications-of-foundation-models.md"
)

# Topic areas the task description requires as their own section.
REQUIRED_TOPIC_HEADINGS = [
    "Design considerations for foundation model applications",
    "Prompt engineering techniques",
    "Retrieval Augmented Generation (RAG) and Amazon Bedrock Knowledge Bases",
    "Fine-tuning vs. continued pre-training vs. RAG vs. prompt engineering",
    "Amazon Bedrock features",
    "Vector databases and embeddings for search and retrieval",
    "Evaluating foundation model performance",
    "AWS infrastructure for generative AI workloads",
]

# Design-consideration factors the task explicitly requires.
REQUIRED_DESIGN_CONSIDERATIONS = [
    "Model selection",
    "Cost",
    "Latency",
    "Modality",
    "Customization options",
]

# Prompt engineering techniques the task explicitly requires be covered
# "in depth".
REQUIRED_PROMPTING_TECHNIQUES = [
    "Zero-shot",
    "Few-shot",
    "Chain-of-thought",
    "Negative prompting",
    "Prompt template",
    "Prompt chaining",
    "Prompt injection",
]

# Amazon Bedrock features the task explicitly requires.
REQUIRED_BEDROCK_FEATURES = [
    "model access",
    "Agents",
    "Guardrails",
    "Knowledge Bases",
    "model evaluation",
    "provisioned throughput",
]

# Vector database / embeddings services the task explicitly requires.
REQUIRED_VECTOR_SERVICES = [
    "Amazon OpenSearch Service",
    "Amazon Aurora",
    "pgvector",
    "Amazon Kendra",
]

# Evaluation approaches the task explicitly requires.
REQUIRED_EVALUATION_APPROACHES = [
    "human evaluation",
    "benchmark dataset",
    "business metric",
]

# Infrastructure the task explicitly requires.
REQUIRED_INFRASTRUCTURE = [
    "Amazon SageMaker",
    "AWS Trainium",
    "AWS Inferentia",
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


class TestDomain3StudyGuideExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected study guide at {DOC_PATH}",
        )


class TestDomain3StudyGuideStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_has_domain_overview(self):
        self.assertRegex(
            self.text, r"^# Domain 3: Applications of Foundation Models"
        )
        self.assertIn("## Domain overview", self.text)

    def test_no_stray_html_tags(self):
        # Regression guard: a previous draft left a stray unopened
        # </section> tag inside the prompt engineering section.
        self.assertNotIn("</section>", self.text)
        self.assertNotIn("<section>", self.text)

    def test_customization_section_has_a_decision_tree_diagram(self):
        section = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG vs\. prompt engineering",
        )
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences, "customization section should include a decision-tree diagram"
        )
        diagram = "\n".join(fences)
        for approach in [
            "PROMPT ENGINEERING",
            "RAG",
            "FINE-TUNING",
            "CONTINUED PRE-TRAINING",
        ]:
            with self.subTest(approach=approach):
                self.assertIn(approach, diagram)
        self.assertIn(
            "?", diagram, "diagram should pose branching decision questions"
        )

    def test_has_every_required_topic_section(self):
        for heading in REQUIRED_TOPIC_HEADINGS:
            with self.subTest(heading=heading):
                self.assertIn(
                    heading,
                    self.text,
                    f"missing required topic section: {heading!r}",
                )

    def test_every_topic_section_has_an_exam_tip(self):
        # Each major numbered section ("## 1. ..." through "## 8. ...")
        # must contain an "Exam tip" callout per the required structure.
        sections = re.findall(r"\n## [1-8]\. .*?(?=\n## |\Z)", self.text, re.S)
        self.assertEqual(
            len(sections), 8, "expected exactly 8 numbered topic sections"
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
        sections = re.findall(r"\n## [1-8]\. .*?(?=\n## |\Z)", self.text, re.S)
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
        for approach in [
            "Prompt engineering",
            "RAG",
            "Fine-tuning",
            "Continued pre-training",
        ]:
            with self.subTest(approach=approach):
                self.assertIn(approach, table_section)

    def test_design_considerations_section_covers_required_factors(self):
        section = _section(
            self.text,
            r"\n## 1\. Design considerations for foundation model applications",
        )
        for factor in REQUIRED_DESIGN_CONSIDERATIONS:
            with self.subTest(factor=factor):
                self.assertRegex(
                    section,
                    re.compile(re.escape(factor), re.IGNORECASE),
                    f"design considerations section missing factor: {factor!r}",
                )

    def test_prompt_engineering_section_covers_required_techniques(self):
        section = _section(
            self.text, r"\n## 2\. Prompt engineering techniques"
        )
        for technique in REQUIRED_PROMPTING_TECHNIQUES:
            with self.subTest(technique=technique):
                self.assertRegex(
                    section,
                    re.compile(re.escape(technique), re.IGNORECASE),
                    f"prompt engineering section missing technique: {technique!r}",
                )

    def test_rag_section_covers_knowledge_bases_and_pipeline(self):
        section = _section(
            self.text,
            r"\n## 3\. Retrieval Augmented Generation \(RAG\) and Amazon "
            r"Bedrock Knowledge Bases",
        )
        for term in [
            "Amazon Bedrock Knowledge Bases",
            "chunk",
            "embedding",
            "hallucination",
        ]:
            with self.subTest(term=term):
                self.assertRegex(
                    section,
                    re.compile(re.escape(term), re.IGNORECASE),
                    f"RAG section missing term: {term!r}",
                )

    def test_rag_section_has_a_system_architecture_diagram(self):
        section = _section(
            self.text,
            r"\n## 3\. Retrieval Augmented Generation \(RAG\) and Amazon "
            r"Bedrock Knowledge Bases",
        )
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences, "RAG section should include a system architecture diagram"
        )
        diagram = "\n".join(fences)
        # Pipeline stages the diagram must depict, per the RAG pipeline
        # described in prose immediately above it.
        for stage in [
            "document",
            "chunk",
            "embed",
            "vector store",
            "retriev",
            "LLM",
            "citation",
        ]:
            with self.subTest(stage=stage):
                self.assertRegex(
                    diagram,
                    re.compile(re.escape(stage), re.IGNORECASE),
                    f"RAG diagram missing pipeline stage: {stage!r}",
                )
        # AWS integration points the diagram must call out.
        for service in ["OpenSearch", "Aurora", "Kendra", "Bedrock"]:
            with self.subTest(service=service):
                self.assertIn(
                    service,
                    diagram,
                    f"RAG diagram missing AWS integration point: {service!r}",
                )

    def test_tradeoff_section_covers_labeled_vs_unlabeled_distinction(self):
        section = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG "
            r"vs\. prompt engineering",
        )
        for term in ["labeled", "unlabeled", "fine-tuning", "continued pre-training"]:
            with self.subTest(term=term):
                self.assertRegex(
                    section,
                    re.compile(re.escape(term), re.IGNORECASE),
                    f"trade-off section missing term: {term!r}",
                )

    def test_bedrock_features_section_covers_required_features(self):
        section = _section(self.text, r"\n## 5\. Amazon Bedrock features")
        for feature in REQUIRED_BEDROCK_FEATURES:
            with self.subTest(feature=feature):
                self.assertRegex(
                    section,
                    re.compile(re.escape(feature), re.IGNORECASE),
                    f"Bedrock features section missing feature: {feature!r}",
                )

    def test_vector_database_section_covers_required_services(self):
        section = _section(
            self.text,
            r"\n## 6\. Vector databases and embeddings for search and "
            r"retrieval",
        )
        for service in REQUIRED_VECTOR_SERVICES:
            with self.subTest(service=service):
                self.assertIn(service, section)

    def test_evaluation_section_covers_required_approaches(self):
        section = _section(
            self.text, r"\n## 7\. Evaluating foundation model performance"
        )
        for approach in REQUIRED_EVALUATION_APPROACHES:
            with self.subTest(approach=approach):
                self.assertRegex(
                    section,
                    re.compile(re.escape(approach), re.IGNORECASE),
                    f"evaluation section missing approach: {approach!r}",
                )

    def test_infrastructure_section_covers_required_services(self):
        section = _section(
            self.text,
            r"\n## 8\. AWS infrastructure for generative AI workloads",
        )
        for service in REQUIRED_INFRASTRUCTURE:
            with self.subTest(service=service):
                self.assertIn(service, section)

    def test_has_key_terms_glossary_with_substantial_coverage(self):
        glossary = _section(self.text, r"\n## Key terms glossary")
        entries = re.findall(r"^- \*\*.+?\*\*", glossary, re.M)
        self.assertGreaterEqual(
            len(entries),
            15,
            "key terms glossary should cover at least 15 terms",
        )


class TestDomain3PracticeQuestions(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
