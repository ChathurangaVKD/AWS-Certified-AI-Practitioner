"""Structural validation for docs/domain-5-security-compliance-governance.md.

This repository is a documentation series, not an application, so there is
no application code to unit test. What *can* regress silently is the
required structure of each domain study guide (README.md promises every
domain doc covers its task statements, includes worked examples, and ends
with a practice-question set + answer key). These tests assert that
structure directly against the rendered Markdown so a future edit that
drops a required section, mismatches the question/answer count, or forgets
a required AWS service/regulation is caught automatically instead of only
in manual review.

Mirrors the conventions established in tests/test_domain_4_study_guide.py,
adapted to Domain 5's own conventions: section callouts are
"**Example:**" / "**Exam tip:**" (not "AWS example:"), the answer key
heading is "## Answer key" (not "## Answer key and explanations"), and
answer entries are formatted "N. **Letter.** explanation" (bold letter(s)
immediately followed by a period, not an em-dash).

Also keeps the original diagram/difficulty-tag/existence tests that
predate this expansion.

Run with:
    python3 -m unittest tests.test_domain_5_study_guide -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-5-security-compliance-governance.md"
)

# Topic areas the task description requires as their own section.
REQUIRED_TOPIC_HEADINGS = [
    "Securing AI systems",
    "AWS compliance standards relevant to AI workloads",
    "AWS Config, AWS Audit Manager, and AWS CloudTrail for AI governance",
    "Data governance strategies",
    "AWS shared responsibility model applied to AI/ML services",
]
# 5.1 "Explain methods to secure AI systems" sub-areas the exam guide
# requires: named threats, the AI-vs-traditional distinction, and named
# frameworks, in addition to the IAM/encryption/networking already covered.
REQUIRED_SECURITY_THREATS_AND_FRAMEWORKS = [
    "data poisoning",
    "prompt injection",
    "model inversion",
    "MITRE ATLAS",
    "OWASP",
    "IAM Access Analyzer",
]

# 5.2 "Recognize governance and compliance regulations" sub-areas the exam
# guide requires, beyond GDPR/HIPAA/AWS Artifact.
REQUIRED_REGULATIONS = [
    "GDPR",
    "HIPAA",
    "NIST AI Risk Management Framework",
    "EU AI Act",
    "ISO/IEC 42001",
    "Algorithmic Accountability Act",
]

# Domain 5's 5.1/5.2 sub-topic count, after closing this content gap,
# genuinely exceeds the 15-20 range used by Domains 1-4 (26 base questions
# covering both task statements' full sub-area lists, plus 3 watermarking
# questions covering AI-generated-content detection, plus 3 differential
# privacy / privacy-preserving training questions, for 32 total) --
# MAX_QUESTIONS is widened accordingly rather than left copy-pasted from
# another domain.
MIN_QUESTIONS = 15
MAX_QUESTIONS = 32
    Domains 1-4, so this class covers that one requirement directly."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.questions_section = _section(
            cls.text, r"\n## Practice questions", r"\n## Answer key"
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


class TestDomain5SharedResponsibilityDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_shared_responsibility_section_has_a_boundary_diagram(self):
        section = _section(
            self.text,
            r"\n## 5\. AWS shared responsibility model applied to AI/ML services",
        )
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "shared responsibility section should include a boundary diagram",
        )
        diagram = "\n".join(fences)
        for term in [
            "Bedrock",
            "SageMaker",
            "CUSTOMER",
            "in the cloud",
            "of the cloud",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)


class TestDomain5GovernanceDecisionTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_governance_section_has_a_decision_tree(self):
        section = _section(
            self.text,
            r"\n## 3\. AWS Config, AWS Audit Manager, and AWS CloudTrail for AI governance",
        )
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "governance services section should include a decision-tree diagram",
        )
        diagram = "\n".join(fences)
        for term in [
            "AWS CloudTrail",
            "AWS Config",
            "AWS Audit Manager",
            "API activity",
            "configuration compliance",
            "audit-ready evidence report",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)


class TestDomain5DataGovernanceLifecycleDiagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_data_governance_section_has_a_lifecycle_diagram(self):
        section = _section(
            self.text,
            r"\n## 4\. Data governance strategies",
        )
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "data governance section should include a lifecycle diagram",
        )
        diagram = "\n".join(fences)
        for term in [
            "Amazon Macie",
            "S3 Lifecycle",
            "Fine-tuning data",
            "RAG source documents",
            "SageMaker ML Lineage Tracking",
            "Model Card",
            "Source citation",
            "CloudTrail",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)


class TestDomain5EncryptionArchitectureDiagrams(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_encryption_section_has_kms_key_lifecycle_diagram(self):
        section = _section(
            self.text,
            r"\n### Data encryption at rest and in transit",
            r"\n### ",
        )
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "encryption section should include a KMS key lifecycle diagram",
        )
        diagram = "\n".join(fences)
        for term in ["Key creation", "key rotation", "CloudTrail", "revocation"]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)

    def test_privatelink_section_has_data_flow_diagram(self):
        section = _section(
            self.text,
            r"\n### AWS PrivateLink and VPC endpoints for AI services",
            r"\n### ",
        )
        fences = re.findall(r"```(.*?)```", section, re.S)
        self.assertTrue(
            fences,
            "VPC endpoints section should include a data-flow diagram",
        )
        diagram = "\n".join(fences)
        for term in ["Amazon S3", "AWS KMS", "VPC endpoint", "SageMaker", "Bedrock", "TLS"]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)

    def test_privatelink_section_has_end_to_end_pipeline_decision_diagram(self):
        """A third diagram (beyond the KMS key lifecycle and the request/data
        flow diagrams) should trace the full S3 -> KMS -> SageMaker training
        -> endpoint data journey and show the encryption decision points
        (which key to use, whether to route through PrivateLink)."""
        section = _section(
            self.text,
            r"\n### AWS PrivateLink and VPC endpoints for AI services",
            r"\n### ",
        )
        fences = re.findall(r"```mermaid(.*?)```", section, re.S)
        self.assertGreaterEqual(
            len(fences),
            2,
            "PrivateLink section should include both the request/data flow "
            "diagram and a separate end-to-end encryption pipeline diagram",
        )
        pipeline_diagrams = [f for f in fences if "SENSITIVE" in f]
        self.assertTrue(
            pipeline_diagrams,
            "should include an end-to-end pipeline diagram with a "
            "sensitive-data decision point",
        )
        diagram = pipeline_diagrams[0]
        for term in [
            "Amazon S3",
            "customer managed KMS key",
            "AWS managed key",
            "SENSITIVE",
            "SageMaker training job",
            "AWS PrivateLink",
            "Model artifacts",
            "endpoint deployment",
            "AWS CloudTrail",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, diagram)


class TestDomain5SecurityThreatWorkedExamples(unittest.TestCase):
    """Guards the three concrete attack-scenario 'Example:' callouts added
    to the "Common security threats" subsection (data poisoning, prompt
    injection, model inversion/extraction) so a future edit can't silently
    drop or water down the worked scenarios readers need to recognize
    these threats when described narratively in exam questions."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(
            cls.text,
            r"\n### Common security threats to AI systems and how to mitigate them",
            r"\n### ",
        )

    def test_subsection_has_at_least_three_worked_examples(self):
        examples = re.findall(r"\*\*Example:\*\*", self.section)
        self.assertGreaterEqual(
            len(examples),
            3,
            "Common security threats subsection should have a worked "
            "'Example:' scenario for at least three of the named threats",
        )

    def test_data_poisoning_example_present(self):
        self.assertIn("**data poisoning**", self.section)
        self.assertIn("retrain", self.section.lower())

    def test_prompt_injection_example_includes_a_concrete_payload(self):
        self.assertIn("**indirect prompt injection**", self.section)
        # The scenario should show a concrete attacker payload, not just an
        # abstract description of the attack.
        self.assertRegex(
            self.section,
            r"`[^`]*[Ii]gnore[^`]*instructions[^`]*`",
            "prompt injection example should include a concrete quoted/"
            "code-formatted attacker payload",
        )

    def test_model_inversion_example_describes_systematic_api_querying(self):
        self.assertIn("**model inversion / extraction attack**", self.section)
        self.assertIn("inference endpoint", self.section)

    def test_worked_examples_appear_before_the_section_mini_quiz(self):
        examples_idx = self.text.index(
            "### Common security threats to AI systems and how to mitigate them"
        )
        quiz_idx = self.text.index(
            "#### Mini-quiz: Test your understanding of securing AI systems"
        )
        self.assertLess(examples_idx, quiz_idx)


class TestDomain5ExpandedSecurityThreatWorkedExamples(unittest.TestCase):
    """Guards the seven additional named threats + worked 'Example:'
    scenarios added to the "Common security threats" subsection to close
    the depth gap where only 3 of the ~10 OWASP Top 10 for LLM Applications
    categories (data poisoning, prompt injection, model inversion/
    extraction) had full description + example + mitigation treatment,
    while insecure output handling, model denial of service, supply chain
    vulnerabilities, sensitive information disclosure, insecure plugin
    design, excessive agency, and overreliance only appeared as a
    one-line row in the summary table."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(
            cls.text,
            r"\n### Common security threats to AI systems and how to mitigate them",
            r"\n### ",
        )

    def test_subsection_has_at_least_ten_worked_examples(self):
        examples = re.findall(r"\*\*Example:\*\*", self.section)
        self.assertGreaterEqual(
            len(examples),
            10,
            "Common security threats subsection should have a worked "
            "'Example:' scenario for all ten OWASP LLM Top 10 categories, "
            "not just the original three",
        )

    def test_each_new_threat_is_named_and_mapped_to_an_aws_mitigation(self):
        # Each of the seven previously-undetailed OWASP categories should be
        # named in this subsection with a nearby concrete AWS mitigation,
        # not just left to the summary table in the next subsection.
        expectations = {
            "insecure output handling": "Guardrails for Amazon Bedrock",
            "model denial of service": "API Gateway",
            "supply chain vulnerability": "SageMaker",
            "sensitive information disclosure": "Macie",
            "insecure plugin design": "IAM",
            "excessive agency": "IAM",
            "overreliance": "Guardrails for Amazon Bedrock",
        }
        for threat, aws_service in expectations.items():
            with self.subTest(threat=threat):
                self.assertIn(
                    threat,
                    self.section.lower(),
                    f"expected threat {threat!r} to be named in the "
                    "Common security threats subsection",
                )
                pattern = re.compile(
                    re.escape(threat) + r".{0,600}?" + re.escape(aws_service),
                    re.IGNORECASE | re.DOTALL,
                )
                self.assertRegex(
                    self.section,
                    pattern,
                    f"{threat!r} should be followed nearby by a mention of "
                    f"{aws_service!r}",
                )

    def test_new_threats_appear_before_the_section_mini_quiz(self):
        quiz_idx = self.text.index(
            "#### Mini-quiz: Test your understanding of securing AI systems"
        )
        for threat in [
            "insecure output handling",
            "model denial of service",
            "supply chain vulnerability",
            "sensitive information disclosure",
            "insecure plugin design",
            "excessive agency",
            "overreliance",
        ]:
            with self.subTest(threat=threat):
                idx = self.text.lower().index(threat)
                self.assertLess(idx, quiz_idx)


REQUIRED_OWASP_LLM_CATEGORIES = [
    "Prompt injection",
    "Insecure output handling",
    "Training data poisoning",
    "Model denial of service",
    "Supply chain vulnerabilities",
    "Sensitive information disclosure",
    "Insecure plugin design",
    "Excessive agency",
    "Overreliance",
    "Model theft",
]


class TestDomain5OwaspReferenceTable(unittest.TestCase):
    """Guards the OWASP Top 10 for LLM Applications category-to-AWS-
    mitigation reference table added to the "Security frameworks for AI
    systems" subsection so all ten categories stay mapped to a concrete
    AWS control instead of silently regressing to just the 3 detailed
    earlier in the "Common security threats" subsection."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(
            cls.text,
            r"\n### Security frameworks for AI systems: MITRE ATLAS and OWASP Top 10 for LLM Applications",
            r"\n#### Mini-quiz",
        )

    def test_section_has_a_markdown_table(self):
        self.assertRegex(self.section, r"\|\s*-{2,}\s*\|")

    def test_table_covers_all_ten_owasp_llm_categories(self):
        for category in REQUIRED_OWASP_LLM_CATEGORIES:
            with self.subTest(category=category):
                self.assertRegex(
                    self.section,
                    re.compile(re.escape(category), re.IGNORECASE),
                    f"OWASP reference table missing category: {category!r}",
                )

    def test_previously_unmitigated_categories_map_to_an_aws_service(self):
        # These five were named in the task description as present-but-
        # unmitigated before this change; assert each now sits on a table
        # row naming a concrete AWS service.
        expectations = {
            "Insecure output handling": "Guardrails for Amazon Bedrock",
            "Model denial of service": "API Gateway",
            "Supply chain vulnerabilities": "SageMaker",
            "Excessive agency": "IAM",
            "Model theft": "KMS",
        }
        for category, aws_service in expectations.items():
            with self.subTest(category=category):
                pattern = re.compile(
                    re.escape(category) + r".{0,400}?" + re.escape(aws_service),
                    re.IGNORECASE | re.DOTALL,
                )
                self.assertRegex(
                    self.section,
                    pattern,
                    f"{category!r} row should mention {aws_service!r} nearby",
                )


class TestDomain5GovernanceWorkedScenarios(unittest.TestCase):
    """Guards the CloudTrail vs. Config vs. Audit Manager worked
    scenario-to-answer mini-examples added to Section 3, so a future edit
    can't silently drop the concrete "which service is the right answer"
    drills that back up the section's one-line distinction / exam tip."""

    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.section = _section(
            cls.text,
            r"\n## 3\. AWS Config, AWS Audit Manager, and AWS CloudTrail for AI governance",
            r"\n## ",
        )

    def test_worked_scenarios_lead_in_present(self):
        self.assertIn("**Worked scenarios:**", self.section)

    def test_at_least_three_scenario_answer_pairs(self):
        scenarios = re.findall(r"\*\*Scenario:\*\*", self.section)
        answers = re.findall(r"\*\*Answer:\*\*", self.section)
        self.assertGreaterEqual(
            len(scenarios),
            3,
            "Section 3 should have at least three worked '**Scenario:**' "
            "mini-examples distinguishing CloudTrail, Config, and Audit "
            "Manager",
        )
        self.assertEqual(
            len(scenarios),
            len(answers),
            "every '**Scenario:**' should be paired with an '**Answer:**'",
        )

    def test_each_governance_service_is_a_scenario_answer(self):
        for service in ("AWS Config", "AWS CloudTrail", "AWS Audit Manager"):
            with self.subTest(service=service):
                self.assertRegex(
                    self.section,
                    r"\*\*Answer:\*\*\s*" + re.escape(service),
                    f"expected a worked scenario whose answer is {service}",
                )

    def test_worked_scenarios_appear_before_the_section_mini_quiz(self):
        scenarios_idx = self.text.index("**Worked scenarios:**")
        quiz_idx = self.text.index(
            "#### Mini-quiz: Test your understanding of AWS Config, Audit "
            "Manager, and CloudTrail for AI governance"
        )
        self.assertLess(scenarios_idx, quiz_idx)


class TestDomain5StudyGuideStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_has_domain_overview(self):
        self.assertRegex(
            self.text,
            r"^# Domain 5: Security, Compliance, and Governance for AI Solutions",
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

    def test_every_topic_section_has_an_example_and_exam_tip(self):
        sections = re.findall(r"\n## [1-5]\. .*?(?=\n## |\Z)", self.text, re.S)
        self.assertEqual(
            len(sections), 5, "expected exactly 5 numbered topic sections"
        )
        for section in sections:
            heading = section.strip().splitlines()[0]
            with self.subTest(section=heading):
                self.assertIn(
                    "Example:",
                    section,
                    f"section {heading!r} is missing an 'Example' callout",
                )
                self.assertIn(
                    "Exam tip:",
                    section,
                    f"section {heading!r} is missing an 'Exam tip' callout",
                )

    def test_securing_ai_systems_section_covers_required_threats_and_frameworks(self):
        section = _section(self.text, r"\n## 1\. Securing AI systems")
        for term in REQUIRED_SECURITY_THREATS_AND_FRAMEWORKS:
            with self.subTest(term=term):
                self.assertRegex(
                    section,
                    re.compile(re.escape(term), re.IGNORECASE),
                    f"securing AI systems section missing: {term!r}",
                )
        # Model drift/degradation is described with either wording.
        self.assertRegex(
            section,
            re.compile(r"model (drift|.*degradation)", re.IGNORECASE),
            "securing AI systems section missing model drift/degradation coverage",
        )

    def test_compliance_section_covers_required_regulations(self):
        section = _section(
            self.text, r"\n## 2\. AWS compliance standards relevant to AI workloads"
        )
        for regulation in REQUIRED_REGULATIONS:
            with self.subTest(regulation=regulation):
                self.assertIn(
                    regulation,
                    section,
                    f"compliance section missing regulation/framework: {regulation!r}",
                )

    def test_has_governance_comparison_table(self):
        table_section = _section(
            self.text,
            r"\n## Comparison table: governance and compliance regulations at a glance",
        )
        self.assertRegex(table_section, r"\|\s*-{2,}\s*\|")
        for regulation in REQUIRED_REGULATIONS:
            with self.subTest(regulation=regulation):
                self.assertIn(regulation, table_section)

    def test_has_key_terms_glossary_with_substantial_coverage(self):
        glossary = _section(self.text, r"\n## Key terms glossary")
        entries = re.findall(r"^- \*\*.+?\*\*", glossary, re.M)
        self.assertGreaterEqual(
            len(entries),
            15,
            "key terms glossary should cover at least 15 terms",
        )


class TestDomain5WorkedExample(unittest.TestCase):
    """Domains 1-3 each end with a dedicated '## Worked example: ...'
    section stitching every concept in the domain into one continuous
    scenario. Domain 5 previously had only inline 'Example:' callouts and
    no such section; these tests guard the worked example added to close
    that gap."""

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
            "## 5. AWS shared responsibility model applied to AI/ML services"
        )
        # Anchored on line start (unlike a plain substring search) so this
        # doesn't accidentally match a nested "#### Worked example: ..."
        # subsection elsewhere in the document -- any "#### " heading
        # contains "## " as a literal substring.
        worked_example_match = re.search(r"\n## Worked example: ", self.text)
        assert worked_example_match, "no top-level '## Worked example: ' heading found"
        worked_example_idx = worked_example_match.start()
        comparison_idx = self.text.index(
            "## Comparison table: governance and monitoring services"
        )
        self.assertLess(section_5_idx, worked_example_idx)
        self.assertLess(worked_example_idx, comparison_idx)

    def test_worked_example_has_scenario_and_exam_tip(self):
        self.assertIn("**Scenario:**", self.section)
        self.assertIn("**Exam tip:**", self.section)

    def test_worked_example_covers_topics_across_all_five_sections(self):
        for term in [
            "HIPAA",
            "data residency",
            "AWS Artifact",
            "AWS CloudTrail",
            "AWS Config",
            "Audit Manager",
            "KMS",
            "shared responsibility",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, self.section)

    def test_worked_example_has_at_least_six_numbered_steps(self):
        steps = re.findall(r"^\d+\.\s", self.section, re.M)
        self.assertGreaterEqual(
            len(steps),
            6,
            "worked example should walk through at least six numbered "
            "lifecycle steps",
        )

    def test_table_of_contents_links_to_worked_example(self):
        self.assertIn("Worked example", self.toc)
        self.assertIn(
            "#worked-example-securing-and-governing-a-hipaa-regulated-bedrock-application-across-its-lifecycle",
            self.toc,
        )


class TestDomain5PracticeQuestions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        cls.questions_section = _section(
            cls.text, r"\n## Practice questions", r"\n## Answer key"
        )
        cls.answers_section = _section(cls.text, r"\n## Answer key")

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
                # Each explanation should be substantive, not just "B is correct."
                self.assertGreater(
                    len(block.strip()),
                    120,
                    f"answer {anum} explanation looks too short to justify "
                    f"the correct choice and rule out the distractors",
                )
                # Domain 5's answer key bolds the correct letter(s) followed
                # by a period, e.g. "**B.**" or "**B and D.**" -- distinct
                # from Domain 4's em-dash-based "**B —" style.
                self.assertRegex(
                    block,
                    r"\*\*[A-E](?:\s*(?:,|and)\s*[A-E])*\.\*\*",
                    f"answer {anum} should clearly state the correct option letter(s)",
                )

    def test_covers_differential_privacy_and_privacy_budget(self):
        combined = self.questions_section + self.answers_section
        self.assertIn(
            "differential privacy",
            combined.lower(),
            "practice questions should cover differential privacy",
        )
        self.assertTrue(
            "epsilon" in combined.lower() or "privacy budget" in combined.lower(),
            "practice questions should cover the privacy budget "
            "(epsilon) accuracy/privacy trade-off",
        )


if __name__ == "__main__":
    unittest.main()
