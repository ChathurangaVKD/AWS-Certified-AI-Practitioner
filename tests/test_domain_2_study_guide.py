"""Structural validation for docs/domain-2-fundamentals-of-generative-ai.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. What *can* regress silently is the
required structure of each domain study guide (README.md promises every
domain doc covers its task statements, includes worked AWS examples, and
ends with a practice-question set + answer key). These tests assert that
structure directly against the rendered Markdown so a future edit that
drops a required section, mismatches the question/answer count, or forgets
an AWS service is caught automatically instead of only in manual review.

Mirrors the conventions established in tests/test_domain_1_study_guide.py.

Run with:
    python3 -m unittest tests/test_domain_2_study_guide.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-2-fundamentals-of-generative-ai.md"
)

# Topic areas the task description requires as their own section.
REQUIRED_TOPIC_HEADINGS = [
    "Generative AI core concepts",
    "LLM lifecycle basics",
    "Advantages and disadvantages of generative AI",
    "Business use cases for generative AI",
    "AWS generative AI services and capabilities",
    "Prompt engineering fundamentals",
    "Foundation model selection criteria",
]

# AWS services the task explicitly calls out for the "AWS services" section.
REQUIRED_AWS_SERVICES = [
    "Amazon Bedrock",
    "Amazon Q",
    "Amazon SageMaker JumpStart",
    "PartyRock",
]

# Core generative AI concepts the task explicitly requires.
REQUIRED_CONCEPT_TERMS = [
    "token",
    "embedding",
    "vector",
    "prompt engineering",
    "transformer",
    "foundation model",
    "multimodal",
]

# Prompt engineering techniques the task explicitly requires.
REQUIRED_PROMPTING_TECHNIQUES = [
    "Zero-shot",
    "Few-shot",
    "Chain-of-thought",
    "Negative prompting",
]

# Foundation model selection criteria the task explicitly requires.
REQUIRED_SELECTION_CRITERIA = [
    "Cost",
    "Modality",
    "Latency",
    "Context window",
    "Fine-tuning",
]

MIN_QUESTIONS = 15
MAX_QUESTIONS = 24


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


class TestDomain2StudyGuideExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected study guide at {DOC_PATH}",
        )


class TestDomain2StudyGuideStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_has_domain_overview(self):
        self.assertRegex(
            self.text, r"^# Domain 2: Fundamentals of Generative AI"
        )
        self.assertIn("## Domain overview", self.text)

    def test_generative_ai_section_has_a_transformer_diagram(self):
        section = _section(self.text, r"\n## 1\. Generative AI core concepts")
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences, "core concepts section should include a transformer diagram"
        )
        diagram = "\n".join(fences)
        for term in ["Tokenization", "Embeddings", "Self-Attention", "Feed-Forward"]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)
        self.assertRegex(
            diagram, r"→|↓", "diagram should show the transformer pipeline flow"
        )

    def test_generative_ai_section_has_a_token_flow_mermaid_diagram(self):
        # The core-concepts section must include a Mermaid flowchart (not
        # just the ASCII pipeline summary) that traces a concrete example
        # sentence through tokenization, embeddings, and the transformer's
        # self-attention block to the model's output.
        section = _section(self.text, r"\n## 1\. Generative AI core concepts")
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", section, re.S)
        self.assertTrue(
            mermaid_blocks,
            "core concepts section should include a Mermaid token-flow diagram",
        )
        diagram = "\n".join(mermaid_blocks)

        # Concrete example sentence, tokenized word by word.
        for token in ["The cat sat", "Token: The", "Token: cat", "Token: sat"]:
            with self.subTest(token=token):
                self.assertIn(token, diagram)

        # Stages of the token flow: embeddings -> transformer attention -> output.
        for stage in [
            "Embeddings layer",
            "positional encoding",
            "Transformer block",
            "Self-Attention",
            "Feed-Forward",
            "Output token probabilities",
        ]:
            with self.subTest(stage=stage):
                self.assertIn(stage, diagram)

        # It should be an actual flowchart with connected nodes, not prose.
        self.assertRegex(
            diagram, r"-->", "diagram should connect stages with flowchart edges"
        )

    def test_generative_ai_section_has_an_attention_weight_matrix_diagram(self):
        # Beyond the high-level pipeline diagram, the core-concepts section
        # must include a *detailed* self-attention example: a concrete
        # sentence with numeric attention weights showing how one token
        # ("it") attends to every other token, to make the "long-range
        # dependency" claim concrete rather than just asserted in prose.
        section = _section(self.text, r"\n## 1\. Generative AI core concepts")
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", section, re.S)
        self.assertGreaterEqual(
            len(mermaid_blocks),
            2,
            "core concepts section should include a separate attention-weight "
            "matrix diagram in addition to the token-flow pipeline diagram",
        )
        # The attention diagram is the one keyed on the query token "it".
        attention_diagrams = [b for b in mermaid_blocks if '"it"' in b]
        self.assertTrue(
            attention_diagrams,
            "expected a Mermaid diagram rooted at the query token \"it\"",
        )
        diagram = "\n".join(attention_diagrams)

        # Every token of the example sentence must appear as a key node.
        for token in [
            "cat",
            "sat",
            "on",
            "mat",
            "because",
            "was",
            "tired",
        ]:
            with self.subTest(token=token):
                self.assertIn(f'"{token}"', diagram)

        # Edges must carry actual numeric attention weights, and "it" must
        # attend most strongly back to "cat" (its antecedent).
        weights = re.findall(r'\|"([0-9]*\.[0-9]+)"\|', diagram)
        self.assertTrue(
            weights, "diagram edges should be labeled with numeric attention weights"
        )
        self.assertRegex(
            diagram,
            r'IT -->\|"0\.62"\|\s*CAT',
            "highest attention weight from \"it\" should point to \"cat\"",
        )

        # The full weight distribution should be documented as a matrix
        # table that sums to 1.0, reinforcing that this is a proper
        # attention-weight matrix row and not just an arbitrary graph.
        self.assertIn("Attention weight from \"it\"", section)
        self.assertIn("**1.00**", section)

    def test_lifecycle_section_has_a_mermaid_flowchart(self):
        # The LLM lifecycle section must include a Mermaid diagram (not
        # just prose) showing the six lifecycle stages, the branching
        # customization options for stage 3, and which AWS service
        # supports each option.
        section = _section(self.text, r"\n## 2\. LLM lifecycle basics")
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", section, re.S)
        self.assertTrue(
            mermaid_blocks,
            "LLM lifecycle section should include a Mermaid flowchart",
        )
        diagram = "\n".join(mermaid_blocks)

        # All six lifecycle stages must appear as diagram nodes.
        for stage in [
            "Scope the use case",
            "Select a foundation model",
            "Adapt & customize",
            "Evaluate the model",
            "Deploy & integrate",
            "Monitor",
        ]:
            with self.subTest(stage=stage):
                self.assertIn(stage, diagram)

        # The four customization options branching off stage 3.
        for option in [
            "Prompt engineering",
            "Retrieval Augmented",
            "Fine-tuning",
            "Continued pre-training",
        ]:
            with self.subTest(option=option):
                self.assertIn(option, diagram)

        # The AWS services that support each customization path.
        for service in [
            "Amazon Bedrock",
            "Knowledge Bases for",
            "SageMaker JumpStart",
        ]:
            with self.subTest(service=service):
                self.assertIn(service, diagram)

        # The diagram should show branching out of the adapt/customize
        # decision node and looping back from monitor for iteration.
        self.assertRegex(
            diagram, r"-->\|", "diagram should show labeled branches"
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
        # Each major numbered section ("## 1. ..." through "## 7. ...")
        # must contain an "Exam tip" callout per the required structure.
        sections = re.findall(r"\n## [1-7]\. .*?(?=\n## |\Z)", self.text, re.S)
        self.assertEqual(
            len(sections), 7, "expected exactly 7 numbered topic sections"
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
        sections = re.findall(r"\n## [1-7]\. .*?(?=\n## |\Z)", self.text, re.S)
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
        for service in REQUIRED_AWS_SERVICES:
            with self.subTest(service=service):
                self.assertIn(service, table_section)

    def test_all_required_aws_services_mentioned_in_doc(self):
        for service in REQUIRED_AWS_SERVICES:
            with self.subTest(service=service):
                self.assertIn(service, self.text)

    def test_all_required_concept_terms_covered(self):
        concepts_section = _section(
            self.text, r"\n## 1\. Generative AI core concepts"
        )
        for term in REQUIRED_CONCEPT_TERMS:
            with self.subTest(term=term):
                self.assertRegex(
                    concepts_section,
                    re.compile(re.escape(term), re.IGNORECASE),
                    f"core concepts section missing term: {term!r}",
                )

    def test_all_required_prompting_techniques_covered(self):
        prompting_section = _section(
            self.text, r"\n## 6\. Prompt engineering fundamentals"
        )
        for technique in REQUIRED_PROMPTING_TECHNIQUES:
            with self.subTest(technique=technique):
                self.assertRegex(
                    prompting_section,
                    re.compile(re.escape(technique), re.IGNORECASE),
                    f"prompt engineering section missing technique: {technique!r}",
                )

    def test_all_required_selection_criteria_covered(self):
        selection_section = _section(
            self.text, r"\n## 7\. Foundation model selection criteria"
        )
        for criterion in REQUIRED_SELECTION_CRITERIA:
            with self.subTest(criterion=criterion):
                self.assertRegex(
                    selection_section,
                    re.compile(re.escape(criterion), re.IGNORECASE),
                    f"foundation model selection section missing criterion: {criterion!r}",
                )

    def test_has_key_terms_glossary_with_substantial_coverage(self):
        glossary = _section(self.text, r"\n## Key terms glossary")
        entries = re.findall(r"^- \*\*.+?\*\*", glossary, re.M)
        self.assertGreaterEqual(
            len(entries),
            15,
            "key terms glossary should cover at least 15 terms",
        )

    def test_image_generation_model_reference_is_current(self):
        # Amazon Nova Canvas (not the discontinued-for-this-purpose Titan
        # Image Generator) is Amazon's current first-party Bedrock
        # image-generation model, and the AWS services section should name
        # it explicitly.
        services_section = _section(
            self.text,
            r"\n## 5\. AWS generative AI services and capabilities",
        )
        self.assertIn(
            "Amazon Nova Canvas",
            services_section,
            "AWS services section should name Amazon Nova Canvas as "
            "Amazon's current first-party image-generation model",
        )
        self.assertNotIn(
            "text, embeddings, and image generation models",
            services_section,
            "Amazon Titan bullet should no longer claim image-generation "
            "capability; that moved to Amazon Nova Canvas",
        )

        # Elsewhere in the doc, Titan Image Generator must not be presented
        # as a current, working option (a prior review flagged exactly this
        # in the business-use-cases mini-quiz and the prompt-engineering
        # AWS example).
        use_cases_section = _section(
            self.text, r"\n## 4\. Business use cases for generative AI"
        )
        self.assertNotIn("Titan Image Generator", use_cases_section)
        self.assertIn("Amazon Nova Canvas", use_cases_section)

        prompting_section = _section(
            self.text, r"\n## 6\. Prompt engineering fundamentals"
        )
        self.assertNotIn("Titan Image Generator", prompting_section)
        self.assertIn("Amazon Nova Canvas", prompting_section)


class TestDomain2PracticeQuestions(unittest.TestCase):
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
