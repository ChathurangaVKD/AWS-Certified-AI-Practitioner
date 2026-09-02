"""Structural validation for docs/domain-1-fundamentals-of-ai-and-ml.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. What *can* regress silently is the
required structure of each domain study guide (README.md promises every
domain doc covers its task statements, includes worked AWS examples, and
ends with a practice-question set + answer key). These tests assert that
structure directly against the rendered Markdown so a future edit that
drops a required section, mismatches the question/answer count, or forgets
an AWS service is caught automatically instead of only in manual review.

Run with:
    python3 -m unittest tests/test_domain_1_study_guide.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-1-fundamentals-of-ai-and-ml.md"
)

# Topic areas the task description requires as their own section.
REQUIRED_TOPIC_HEADINGS = [
    "Basic AI/ML/DL terminology and concepts",
    "The ML development lifecycle",
    "Types of learning",
    "Common use cases for AI/ML",
    "AWS managed AI/ML services",
    "Model evaluation basics",
    "Overfitting, underfitting, and the bias",
]

# AWS services the task explicitly calls out for the "managed services" section.
REQUIRED_AWS_SERVICES = [
    "Amazon SageMaker",
    "Amazon Rekognition",
    "Amazon Transcribe",
    "Amazon Comprehend",
    "Amazon Polly",
    "Amazon Translate",
    "Amazon Lex",
    "Amazon Personalize",
    "Amazon Forecast",
    "Amazon Textract",
]

# Model evaluation terms the task explicitly requires.
REQUIRED_EVAL_TERMS = [
    "accuracy",
    "precision",
    "recall",
    "F1",
    "AUC",
    "confusion matrix",
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


class TestDomain1StudyGuideExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            f"expected study guide at {DOC_PATH}",
        )


class TestDomain1StudyGuideStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_has_domain_overview(self):
        self.assertRegex(self.text, r"^# Domain 1: Fundamentals of AI and ML", )
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

    def test_all_required_evaluation_terms_covered(self):
        eval_section = _section(self.text, r"\n## 6\. Model evaluation basics")
        for term in REQUIRED_EVAL_TERMS:
            with self.subTest(term=term):
                self.assertRegex(
                    eval_section,
                    re.compile(re.escape(term), re.IGNORECASE),
                    f"model evaluation section missing term: {term!r}",
                )

    def test_ml_lifecycle_section_has_a_flow_diagram(self):
        section = _section(self.text, r"\n## 2\. The ML development lifecycle")
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences, "ML lifecycle section should include a diagram in a fenced code block"
        )
        diagram = "\n".join(fences)
        for stage in [
            "Business Goal",
            "Data Collection",
            "Exploratory Data Analysis",
            "Feature Engineering",
            "Model Training",
            "Hyperparameter Tuning",
            "Deployment",
            "Monitoring",
        ]:
            with self.subTest(stage=stage):
                self.assertIn(stage, diagram)
        self.assertRegex(
            diagram, r"[↓▶│└]", "diagram should show directional flow between stages"
        )
        self.assertRegex(
            diagram,
            r"(?i)iterat",
            "diagram should depict the loop-back to an earlier stage",
        )

    def test_ml_lifecycle_section_has_a_mermaid_flowchart(self):
        section = _section(self.text, r"\n## 2\. The ML development lifecycle")
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", section, re.S)
        self.assertTrue(
            mermaid_blocks,
            "ML lifecycle section should include a ```mermaid fenced flowchart",
        )
        diagram = "\n".join(mermaid_blocks)

        # Diagram must declare a flowchart and use directional edges.
        self.assertRegex(diagram, r"flowchart\s+(TD|TB|LR|RL|BT)")
        self.assertRegex(diagram, r"-->")

        # All 8 lifecycle stages must be represented as nodes.
        for stage in [
            "Business Goal Identification",
            "Data Collection",
            "Exploratory Data Analysis",
            "Data Preparation / Feature Engineering",
            "Model Training",
            "Hyperparameter Tuning / Evaluation",
            "Deployment",
            "Monitoring",
        ]:
            with self.subTest(stage=stage):
                self.assertIn(stage, diagram)

        # AWS tools called out per stage in the prose must also appear on
        # the diagram so the flowchart maps tools to stages, not just names.
        for tool in [
            "S3",
            "Glue",
            "Kinesis",
            "SageMaker Data Wrangler",
            "Athena",
            "SageMaker Feature Store",
            "JumpStart",
            "SageMaker Automatic Model Tuning",
            "SageMaker Clarify",
            "SageMaker Endpoints",
            "SageMaker Model Monitor",
            "CloudWatch",
        ]:
            with self.subTest(tool=tool):
                self.assertIn(tool, diagram)

        # At least one feedback/loop-back edge must connect a later stage
        # back to an earlier one (dashed edges using "-." syntax), and it
        # must be labeled to explain why the loop happens.
        loopback_edges = re.findall(r'-\.\s*"([^"]+)"\s*\.->', diagram)
        self.assertTrue(
            loopback_edges,
            "diagram should include at least one labeled feedback/loop-back edge",
        )
        self.assertTrue(
            any(
                re.search(r"(?i)evaluat|drift|degrad|retrain", label)
                for label in loopback_edges
            ),
            "feedback edge labels should explain the loop-back reason "
            "(e.g. poor evaluation, drift, degraded accuracy, retraining)",
        )

    def test_ml_lifecycle_mermaid_flowchart_has_evaluation_decision_point(self):
        # The evaluation stage must be an explicit branch point in the
        # diagram, not just another straight-through box: a decision node
        # with distinct "pass" (-> deploy) and "fail" (-> retrain) edges.
        section = _section(self.text, r"\n## 2\. The ML development lifecycle")
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", section, re.S)
        self.assertTrue(mermaid_blocks)
        diagram = "\n".join(mermaid_blocks)

        # A decision node uses Mermaid's diamond syntax: NAME{"..."}
        decision_nodes = re.findall(r'\w+\{"([^"]+)"\}', diagram)
        self.assertTrue(
            decision_nodes,
            "diagram should include a Mermaid decision node (diamond "
            'shape, e.g. NAME{"..."}) for the evaluation gate',
        )

        # Find the decision node's id so we can check its outgoing edges.
        decision_id_match = re.search(r'(\w+)\{"[^"]+"\}', diagram)
        decision_id = decision_id_match.group(1)
        outgoing_edges = re.findall(
            rf'{decision_id}\s*-[-.]+\s*"([^"]+)"\s*[-.]+>', diagram
        )
        self.assertTrue(
            any(re.search(r"(?i)pass", label) for label in outgoing_edges),
            "decision node should have an edge labeled for the passing "
            "case (leading to deployment)",
        )
        self.assertTrue(
            any(re.search(r"(?i)fail", label) for label in outgoing_edges),
            "decision node should have an edge labeled for the failing "
            "case (leading back to retraining)",
        )

    def test_types_of_learning_section_has_a_selection_flowchart(self):
        # The learning-type section defines supervised, unsupervised,
        # semi-supervised, and reinforcement learning in prose but used to
        # provide no visual framework for choosing between them (unlike
        # Domain 3's FM-customization and vector-store decision trees).
        # This asserts a real Mermaid flowchart exists and actually
        # branches on the three questions that distinguish the four types.
        section = _section(self.text, r"\n## 3\. Types of learning")
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", section, re.S)
        self.assertTrue(
            mermaid_blocks,
            "types of learning section should include a ```mermaid "
            "fenced flowchart for choosing between learning types",
        )
        diagram = "\n".join(mermaid_blocks)

        self.assertRegex(diagram, r"flowchart\s+(TD|TB|LR|RL|BT)")
        self.assertRegex(diagram, r"-->")

        # The three questions called out in the task must appear as
        # decision nodes (Mermaid diamond syntax).
        decision_questions = re.findall(r'\w+\{"([^"]+)"\}', diagram)
        self.assertTrue(
            decision_questions,
            "diagram should include Mermaid decision nodes (diamond "
            'shape, e.g. NAME{"..."})',
        )
        combined_questions = "\n".join(decision_questions)
        for cue in [
            r"(?i)labele?d data",
            r"(?i)reward",
            r"(?i)pattern",
        ]:
            with self.subTest(cue=cue):
                self.assertRegex(combined_questions, cue)

        # All four learning types from the prose must be reachable outcomes.
        for outcome in [
            "SUPERVISED LEARNING",
            "UNSUPERVISED LEARNING",
            "REINFORCEMENT LEARNING",
            "SEMI-SUPERVISED LEARNING",
        ]:
            with self.subTest(outcome=outcome):
                self.assertIn(outcome, diagram)

    def test_model_evaluation_section_has_a_metric_selection_flowchart(self):
        # Section 6 listed accuracy/precision/recall/F1/AUC-ROC/MAE in
        # prose but gave no visual guidance on which metric to pick for a
        # given scenario. This asserts a real Mermaid decision tree exists
        # and actually branches on problem type (regression vs.
        # classification) and class imbalance, the two questions called
        # out in the task, and that every metric is a reachable outcome.
        section = _section(self.text, r"\n## 6\. Model evaluation basics")
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", section, re.S)
        self.assertTrue(
            mermaid_blocks,
            "model evaluation section should include a ```mermaid "
            "fenced flowchart for choosing an evaluation metric",
        )
        diagram = "\n".join(mermaid_blocks)

        self.assertRegex(diagram, r"flowchart\s+(TD|TB|LR|RL|BT)")
        self.assertRegex(diagram, r"-->")

        # The two questions called out in the task must appear as decision
        # nodes (Mermaid diamond syntax): imbalance, and regression vs.
        # classification.
        decision_questions = re.findall(r'\w+\{"([^"]+)"\}', diagram)
        self.assertTrue(
            decision_questions,
            "diagram should include Mermaid decision nodes (diamond "
            'shape, e.g. NAME{"..."})',
        )
        combined_questions = "\n".join(decision_questions)
        for cue in [
            r"(?i)regression or classification",
            r"(?i)imbalanced",
        ]:
            with self.subTest(cue=cue):
                self.assertRegex(combined_questions, cue)

        # All the metric outcomes from the prose must be reachable nodes.
        for outcome in [
            "MAE",
            "RMSE",
            "F1 score or AUC-ROC",
            "Precision",
            "Recall",
            "Accuracy",
        ]:
            with self.subTest(outcome=outcome):
                self.assertIn(outcome, diagram)

    def test_bias_variance_section_has_a_trade_off_mermaid_diagram(self):
        # Section 7 explained the bias-variance trade-off in prose only,
        # with no visual anchor for the underfitting/optimal/overfitting
        # spectrum that recurs across later domains. This asserts a real
        # Mermaid flowchart exists and actually depicts the spectrum:
        # complexity increasing left-to-right, with underfitting, an
        # optimal sweet spot, and overfitting as distinct stops, plus a
        # reference to error being minimized at the sweet spot.
        section = _section(
            self.text,
            r"\n## 7\. Overfitting, underfitting, and the bias",
        )
        mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", section, re.S)
        self.assertTrue(
            mermaid_blocks,
            "bias-variance section should include a ```mermaid fenced "
            "flowchart showing the underfitting/optimal/overfitting "
            "spectrum",
        )
        diagram = "\n".join(mermaid_blocks)

        self.assertRegex(diagram, r"flowchart\s+(TD|TB|LR|RL|BT)")
        self.assertRegex(diagram, r"-->")

        # The x-axis (complexity) and y-axis (error) framing from the task
        # must be explicit in the diagram, not just implied.
        self.assertRegex(diagram, r"(?i)model complexity")
        self.assertRegex(diagram, r"(?i)error")

        # The three stops on the spectrum must all be present, in order.
        for stop in ["UNDERFITTING", "OPTIMAL FIT", "OVERFITTING"]:
            with self.subTest(stop=stop):
                self.assertIn(stop, diagram)
        self.assertLess(
            diagram.index("UNDERFITTING"),
            diagram.index("OPTIMAL FIT"),
            "underfitting should appear before the optimal sweet spot",
        )
        self.assertLess(
            diagram.index("OPTIMAL FIT"),
            diagram.index("OVERFITTING"),
            "the optimal sweet spot should appear before overfitting",
        )

        # Bias/variance should be tied to the correct ends of the spectrum.
        self.assertRegex(diagram, r"(?i)high bias")
        self.assertRegex(diagram, r"(?i)high variance")

    def test_has_key_terms_glossary_with_substantial_coverage(self):
        glossary = _section(self.text, r"\n## Key terms glossary")
        entries = re.findall(r"^- \*\*.+?\*\*", glossary, re.M)
        self.assertGreaterEqual(
            len(entries),
            15,
            "key terms glossary should cover at least 15 terms",
        )


class TestDomain1PracticeQuestions(unittest.TestCase):
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
