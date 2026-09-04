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

# The eight prompt engineering techniques the comparison matrix must
# cover, one row each.
REQUIRED_PROMPT_MATRIX_TECHNIQUES = [
    "Zero-shot prompting",
    "Few-shot prompting",
    "Chain-of-thought (CoT) prompting",
    "Prompt templates",
    "Negative prompting",
    "Prompt chaining / Prompt Flows",
    "System prompts / role prompting",
    "Prompt injection",
]

# The comparison dimensions the matrix must score every technique on.
REQUIRED_PROMPT_MATRIX_DIMENSIONS = [
    "Cost",
    "Complexity",
    "Control over output",
    "Best use-case fit",
    "Exam keywords",
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
MAX_QUESTIONS = 29


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

    def test_customization_decision_tree_is_a_mermaid_flowchart(self):
        # Regression guard: the decision tree used to be an ASCII-art code
        # block. It should now render as an actual Mermaid flowchart, and
        # its branches should map the specific symptoms the exam tests to
        # the right customization approach.
        section = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG vs\. prompt engineering",
        )
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertTrue(
            fences, "customization section should include Mermaid diagrams"
        )
        tree_fences = [f for f in fences if "PROMPT ENGINEERING" in f]
        self.assertTrue(
            tree_fences,
            "expected a Mermaid flowchart (not ASCII art) for the "
            "decision tree, distinct from the comparison matrix",
        )
        tree = "\n".join(tree_fences)
        self.assertRegex(
            tree,
            r"flowchart\s+\w+|graph\s+\w+",
            "decision tree should use Mermaid flowchart/graph syntax",
        )
        decision_points = {
            "factuality/context problem maps to RAG": (
                r"factuality/context",
                "RAG",
            ),
            "style/format problem maps to prompt engineering": (
                r"style/format",
                "PROMPT ENGINEERING",
            ),
            "narrow-task labeled behavior maps to fine-tuning": (
                r"LABELED",
                "FINE-TUNING",
            ),
            "new domain vocabulary maps to continued pre-training": (
                r"UNLABELED",
                "CONTINUED PRE-TRAINING",
            ),
        }
        for description, (cue, outcome) in decision_points.items():
            with self.subTest(decision_point=description):
                self.assertRegex(tree, cue)
                self.assertIn(outcome, tree)

    def test_customization_decision_tree_has_a_quick_reference_cheat_sheet(self):
        # The Mermaid flowchart requires rendering support to read at a
        # glance; a plain-text if-then cheat sheet right below it gives
        # readers (and non-rendering viewers) an equally fast lookup for
        # this domain's most-tested decision.
        section = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG vs\. prompt engineering",
        )
        self.assertIn(
            "Quick reference (if",
            section,
            "decision tree should be followed by an if-then quick "
            "reference list",
        )
        quick_ref = section[section.index("Quick reference (if"):]
        expectations = {
            "frequently changing/proprietary data maps to RAG": (
                r"frequently.*?weights shouldn't\s*\n?\s*change",
                "RAG",
            ),
            "formatting/style need maps to prompt engineering": (
                r"formatting, tone, or\s*\n?\s*output style",
                "prompt engineering",
            ),
            "new proprietary-task skill with labeled data maps to fine-tuning": (
                r"narrow, proprietary task",
                "fine-tuning",
            ),
            "broad domain fluency from unlabeled text maps to continued pre-training": (
                r"unlabeled text",
                "continued pre-training",
            ),
        }
        for description, (cue, outcome) in expectations.items():
            with self.subTest(mapping=description):
                self.assertRegex(quick_ref, cue)
                self.assertIn(outcome, quick_ref)
        self.assertIn(
            "→",
            quick_ref,
            "quick reference entries should use an if-then arrow ("
            "→) to state the conclusion",
        )

    def test_customization_section_has_a_visual_comparison_matrix(self):
        # Regression guard: Section 4 originally compared the four
        # customization approaches in narrative form only. A Mermaid
        # visual matrix should let all four approaches be scanned at a
        # glance across cost, complexity, accuracy, speed, and data
        # requirements.
        section = _section(
            self.text,
            r"\n## 4\. Fine-tuning vs\. continued pre-training vs\. RAG vs\. prompt engineering",
        )
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "customization section should include a Mermaid visual "
            "comparison matrix in addition to the decision-tree diagram",
        )
        matrix_fences = [f for f in fences if "PROMPT ENGINEERING" not in f]
        self.assertTrue(
            matrix_fences,
            "expected a Mermaid diagram distinct from the decision tree "
            "to serve as the comparison matrix",
        )
        matrix = "\n".join(matrix_fences)
        for approach in [
            "Prompt engineering",
            "RAG",
            "Fine-tuning",
            "Continued pre-training",
        ]:
            with self.subTest(approach=approach):
                self.assertIn(approach, matrix)
        for dimension in [
            "Cost",
            "Complexity",
            "Accuracy",
            "Speed",
            "Data",
        ]:
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, matrix)

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

    def test_modality_consideration_uses_current_image_model_name(self):
        self.assertNotIn(
            "Titan Image Generator",
            self.text,
            "doc should not reference the superseded Titan Image "
            "Generator; use Amazon Nova Canvas instead",
        )
        section = _section(
            self.text,
            r"\n## 1\. Design considerations for foundation model applications",
        )
        self.assertIn(
            "Amazon Nova Canvas",
            section,
            "modality design-consideration bullet should cite Amazon "
            "Nova Canvas as a current image-generation model example",
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

    def test_prompt_engineering_section_has_side_by_side_worked_examples(self):
        # The prompt engineering section previously only described
        # techniques conceptually. It should also walk through the same
        # concrete task (classifying a customer review) with several
        # techniques side by side, each showing actual prompt text and
        # the resulting model output.
        section = _section(
            self.text, r"\n## 2\. Prompt engineering techniques"
        )
        self.assertIn(
            "Worked examples: the same task, four techniques",
            section,
            "prompt engineering section should include a worked-examples "
            "subsection comparing techniques on one task",
        )
        examples = section[
            section.index("Worked examples: the same task, four techniques"):
        ]

        # The same input task/review must be reused across every example
        # so the techniques are genuinely comparable.
        self.assertGreaterEqual(
            examples.count("customer support was quick to"),
            4,
            "worked examples should reuse the same input review across "
            "every technique for a fair side-by-side comparison",
        )

        # Each of at least four techniques must show both a labeled
        # prompt and a labeled model output.
        for technique in [
            "Zero-shot prompting",
            "Few-shot prompting",
            "Chain-of-thought prompting",
            "Negative prompting",
        ]:
            with self.subTest(technique=technique):
                self.assertIn(technique, examples)

        self.assertGreaterEqual(
            examples.count("Prompt:"),
            4,
            "expected at least 4 labeled prompts in the worked examples",
        )
        self.assertGreaterEqual(
            examples.count("Model output:"),
            4,
            "expected at least 4 labeled model outputs in the worked examples",
        )

        # Prompts and outputs should be shown as actual text in fenced
        # code blocks, not just described in prose.
        fences = re.findall(r"```(.*?)```", examples, re.S)
        self.assertGreaterEqual(
            len(fences),
            8,
            "expected at least 8 fenced code blocks (prompt + output per "
            "technique) in the worked examples",
        )

    def test_prompt_engineering_section_has_a_technique_comparison_matrix(self):
        # Regression guard: Section 2 covers eight prompt engineering
        # techniques across four worked examples but previously had no
        # single table comparing all eight at a glance. A markdown
        # comparison matrix should map every technique against cost,
        # complexity, control over output, use-case fit, and exam
        # keywords, following the same pattern as the customization
        # trade-offs table under "## Comparison table: customization
        # approaches for foundation model applications".
        section = _section(
            self.text, r"\n## 2\. Prompt engineering techniques"
        )
        self.assertIn(
            "Comparison table: prompt engineering techniques at a glance",
            section,
            "prompt engineering section should include a dedicated "
            "comparison-matrix subsection",
        )
        matrix = section[
            section.index(
                "Comparison table: prompt engineering techniques at a glance"
            ):
        ]
        # A markdown table needs a header separator row like |---|---|.
        self.assertRegex(matrix, r"\|\s*-{2,}\s*\|")
        for technique in REQUIRED_PROMPT_MATRIX_TECHNIQUES:
            with self.subTest(technique=technique):
                self.assertIn(
                    technique,
                    matrix,
                    f"comparison matrix missing technique row: {technique!r}",
                )
        for dimension in REQUIRED_PROMPT_MATRIX_DIMENSIONS:
            with self.subTest(dimension=dimension):
                self.assertIn(
                    dimension,
                    matrix,
                    f"comparison matrix missing dimension column: {dimension!r}",
                )

    def test_prompt_engineering_matrix_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents")
        self.assertIn(
            "[Comparison table: prompt engineering techniques at a glance]"
            "(#comparison-table-prompt-engineering-techniques-at-a-glance)",
            toc,
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

    def test_vector_store_decision_guide_has_a_decision_tree_diagram(self):
        # Regression guard: the vector store decision guide (OpenSearch vs.
        # Aurora + pgvector vs. Amazon Kendra) previously only had a
        # comparison table plus three worked scenarios, with no
        # decision-flow visualization tying the choice to a sequence of
        # yes/no questions, unlike the Section 4 FM-customization decision
        # tree.
        section = _section(
            self.text,
            r"\n### Vector store decision guide: OpenSearch vs\. Aurora \+ "
            r"pgvector vs\. Amazon Kendra",
            end_heading_regex=r"\n(?:## |### )",
        )
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "vector store decision guide should include a Mermaid "
            "decision-tree flowchart",
        )
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "decision tree should use Mermaid flowchart/graph syntax",
        )
        self.assertIn(
            "?", diagram, "diagram should pose branching decision questions"
        )
        decision_points = {
            "hybrid search maps to OpenSearch": (
                r"[Hh]ybrid search",
                "OPENSEARCH",
            ),
            "already running PostgreSQL maps to Aurora + pgvector": (
                r"Aurora/PostgreSQL",
                "PGVECTOR",
            ),
            "fully managed with connectors maps to Kendra": (
                r"connectors",
                "KENDRA",
            ),
        }
        for description, (cue, outcome) in decision_points.items():
            with self.subTest(decision_point=description):
                self.assertRegex(diagram, cue)
                self.assertIn(outcome, diagram)

    def test_infrastructure_section_has_inference_type_decision_tree_diagram(self):
        # Regression guard: cross-domain-concept-map.md previously only
        # described, in prose, how the Domain 1 inference-type decision
        # (real-time vs. batch vs. serverless) flows into the Domain 3
        # Bedrock on-demand vs. provisioned-throughput decision, with no
        # diagram anywhere in the series visualizing that decision path.
        section = _section(
            self.text,
            r"\n## 8\. AWS infrastructure for generative AI workloads",
        )
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "AWS infrastructure section should include a Mermaid "
            "inference-type decision-tree flowchart",
        )
        # The vector store decision tree (Section 6) also renders as a
        # Mermaid flowchart; make sure we're looking at *this* section's
        # own diagram, not accidentally matching another section's.
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "decision tree should use Mermaid flowchart/graph syntax",
        )
        self.assertIn(
            "?", diagram, "diagram should pose branching decision questions"
        )
        for cue in [
            "real-time",
            "batch",
            "ON-DEMAND",
            "PROVISIONED",
        ]:
            with self.subTest(cue=cue):
                self.assertRegex(diagram, re.compile(re.escape(cue), re.IGNORECASE))
        # The three deciding factors the task requires must be named in the
        # surrounding prose, not just implied by the diagram shape.
        for factor in ["traffic predictability", "latency", "cost model"]:
            with self.subTest(factor=factor):
                self.assertRegex(
                    section,
                    re.compile(re.escape(factor), re.IGNORECASE),
                    f"inference-type decision tree section missing deciding "
                    f"factor: {factor!r}",
                )

    def test_concept_map_links_to_inference_type_decision_tree(self):
        # The cross-domain concept map's D1-inference-type-to-D3-Bedrock-
        # throughput row should point readers at the new diagram, not just
        # the section that contains it.
        concept_map_path = DOC_PATH.parent / "cross-domain-concept-map.md"
        concept_map_text = concept_map_path.read_text(encoding="utf-8")
        self.assertIn(
            "inference-type decision tree",
            concept_map_text,
            "cross-domain-concept-map.md should cross-link the new "
            "inference-type decision tree diagram",
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

    def test_bedrock_features_section_cross_links_domain_4_guardrails(self):
        # Guardrails for Amazon Bedrock is covered here (runtime safety) and
        # again in Domain 4 §3 (responsible-AI tooling). Readers studying one
        # should be pointed at the other.
        section = _section(self.text, r"\n## 5\. Amazon Bedrock features")
        self.assertIn(
            "domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai",
            section,
            "Bedrock features section should cross-link Domain 4 §3's "
            "responsible-AI coverage of Guardrails",
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

    def test_vector_database_section_has_a_selection_decision_tree_diagram(self):
        # Regression guard: Section 6 previously explained the vector
        # database options (OpenSearch Serverless, Aurora/RDS + pgvector,
        # Kendra) with prose and bullets only, unlike other decision points
        # in this domain (e.g. the Section 4 customization decision tree),
        # which pair the narrative with a Mermaid flowchart.
        section = _section(
            self.text,
            r"\n## 6\. Vector databases and embeddings for search and "
            r"retrieval",
        )
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "vector database section should include a Mermaid "
            "selection decision-tree flowchart",
        )
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "decision tree should use Mermaid flowchart/graph syntax",
        )
        self.assertIn(
            "?", diagram, "diagram should pose branching decision questions"
        )
        # The three deciding factors the task requires must drive the
        # diagram's branches.
        for cue in [
            r"RDS.*Aurora",
            r"VECTOR-ONLY",
            r"[Hh]ybrid",
            r"throughput",
        ]:
            with self.subTest(cue=cue):
                self.assertRegex(diagram, cue)
        # It must terminate in a recommended service for each branch.
        for outcome in ["KENDRA", "PGVECTOR", "OPENSEARCH"]:
            with self.subTest(outcome=outcome):
                self.assertIn(outcome, diagram)

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

    def test_evaluation_section_names_common_benchmark_datasets(self):
        # Regression guard: Section 7 previously described "benchmark
        # datasets" only generically (standardized, publicly available
        # datasets paired with automatic metrics) without naming any real
        # benchmark or which task type each one is used for, leaving
        # learners unable to recognize a named benchmark in an exam
        # scenario.
        section = _section(
            self.text, r"\n## 7\. Evaluating foundation model performance"
        )
        tables = re.findall(r"^\|.+\|$\n(?:^\|.+\|$\n?)+", section, re.M)
        benchmark_tables = [t for t in tables if "MMLU" in t]
        self.assertTrue(
            benchmark_tables,
            "evaluation section should include a reference table of named "
            "benchmark datasets",
        )
        table = benchmark_tables[0]
        # Named benchmarks the task explicitly requires, each mapped to the
        # task type it evaluates.
        for benchmark, task_type in [
            ("MMLU", "reasoning"),
            ("ARC", "[Ss]cience"),
            ("HumanEval", "[Cc]ode"),
            ("GSM8K", "[Mm]ath"),
        ]:
            with self.subTest(benchmark=benchmark):
                self.assertIn(benchmark, table)
                row = next(
                    line for line in table.splitlines() if benchmark in line
                )
                self.assertRegex(
                    row,
                    task_type,
                    f"{benchmark} row should describe its task type",
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


class TestDomain3MultiConstraintWorkedExample(unittest.TestCase):
    """Domain 2 Section 7 and Domain 3 Section 1 each introduce foundation
    model selection criteria one at a time, but neither showed a worked
    example reasoning through several competing constraints (modality,
    cost, latency, fine-tuning support, context window) simultaneously --
    the pattern real scenario questions test. These tests guard the
    dedicated worked example added to close that gap."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.heading = (
            "## Worked example: selecting a foundation model under "
            "multiple competing constraints"
        )

    def test_worked_example_section_exists(self):
        self.assertIn(self.heading, self.text)

    def test_worked_example_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents")
        self.assertIn(
            "[Worked example: selecting a foundation model under multiple "
            "competing constraints]"
            "(#worked-example-selecting-a-foundation-model-under-multiple-"
            "competing-constraints)",
            toc,
        )

    def test_worked_example_covers_at_least_four_competing_constraints(self):
        section = _section(
            self.text,
            r"\n## Worked example: selecting a foundation model under "
            r"multiple competing constraints",
        )
        for constraint in [
            "Modality",
            "Latency",
            "Cost",
            "Fine-tuning support",
            "Context window",
        ]:
            with self.subTest(constraint=constraint):
                self.assertIn(constraint, section)

    def test_worked_example_has_a_candidate_model_comparison_table(self):
        section = _section(
            self.text,
            r"\n## Worked example: selecting a foundation model under "
            r"multiple competing constraints",
        )
        # A markdown table needs a header separator row like |---|---|.
        self.assertRegex(section, r"\|\s*-{2,}\s*\|")
        for model in ["Model A", "Model B", "Model C", "Model D", "Model E"]:
            with self.subTest(model=model):
                self.assertIn(model, section)

    def test_worked_example_eliminates_candidates_down_to_one_survivor(self):
        # The walkthrough should narrow the five candidates step by step
        # until exactly one remains, not just describe the criteria in the
        # abstract.
        section = _section(
            self.text,
            r"\n## Worked example: selecting a foundation model under "
            r"multiple competing constraints",
        )
        self.assertRegex(
            section,
            r"eliminat\w*",
            "worked example should describe eliminating candidate models",
        )
        for remaining in [
            "**A, C, D, E**",
            "**C, D, E**",
            "**D, E**",
            "**E**",
        ]:
            with self.subTest(remaining=remaining):
                self.assertIn(
                    remaining,
                    section,
                    "expected the elimination steps to narrow the "
                    f"surviving candidates down to {remaining!r}",
                )

    def test_worked_example_has_a_mermaid_elimination_decision_tree(self):
        # The worked example narrates a five-constraint elimination process
        # in prose; it should also depict the same elimination sequence as
        # a Mermaid flowchart so learners can trace it visually.
        section = _section(
            self.text,
            r"\n## Worked example: selecting a foundation model under "
            r"multiple competing constraints",
        )
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "worked example should include a Mermaid decision-tree diagram",
        )
        diagram = "\n".join(fences)
        self.assertRegex(
            diagram,
            r"flowchart|graph",
            "expected a Mermaid flowchart/graph, not another diagram type",
        )
        for constraint in [
            "MODALITY",
            "COST",
            "LATENCY",
            "FINE-TUNING SUPPORT",
            "CONTEXT WINDOW",
        ]:
            with self.subTest(constraint=constraint):
                self.assertIn(constraint, diagram)
        for model in ["Model A", "Model B", "Model C", "Model D", "Model E"]:
            with self.subTest(model=model):
                self.assertIn(model, diagram)
        self.assertIn(
            "MODEL E",
            diagram,
            "diagram should land on Model E as the sole survivor",
        )

    def test_worked_example_has_an_exam_tip(self):
        section = _section(
            self.text,
            r"\n## Worked example: selecting a foundation model under "
            r"multiple competing constraints",
        )
        self.assertIn("Exam tip:", section)

    def test_worked_example_cross_references_related_sections(self):
        section = _section(
            self.text,
            r"\n## Worked example: selecting a foundation model under "
            r"multiple competing constraints",
        )
        self.assertIn(
            "#1-design-considerations-for-foundation-model-applications",
            section,
        )
        self.assertIn(
            "domain-2-fundamentals-of-generative-ai.md#7-foundation-model-"
            "selection-criteria",
            section,
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


if __name__ == "__main__":
    unittest.main()
