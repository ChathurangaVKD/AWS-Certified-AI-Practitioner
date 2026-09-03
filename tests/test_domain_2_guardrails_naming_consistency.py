"""Regression test for Guardrails service naming consistency in Domain 2.

Domain 2 previously referred to the same Amazon Bedrock capability by two
different names: the official AWS product name "Guardrails for Amazon
Bedrock" (~3 occurrences) and the informal variant "Amazon Bedrock
Guardrails" (~2 occurrences, including inside a mini-quiz answer option and
the "building an end-to-end generative AI support assistant" worked
example). This inconsistency made the guide read as if two different
services existed. This test locks in the fix by asserting the informal
variant never reappears and that the official name is still used
throughout the document.

Run with:
    python3 -m unittest tests/test_domain_2_guardrails_naming_consistency.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-2-fundamentals-of-generative-ai.md"
)

# The informal variant that should never appear in the guide. Matched with a
# negative lookbehind for "for " so it doesn't also flag "Guardrails for
# Amazon Bedrock".
INFORMAL_VARIANT_RE = re.compile(r"(?<!for )Amazon Bedrock Guardrails")

OFFICIAL_NAME = "Guardrails for Amazon Bedrock"


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


class TestDomain2GuardrailsNamingConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()

    def test_informal_variant_does_not_appear(self):
        matches = INFORMAL_VARIANT_RE.findall(self.text)
        self.assertEqual(
            matches,
            [],
            "Domain 2 guide should not use the informal 'Amazon Bedrock "
            "Guardrails' naming; use the official 'Guardrails for Amazon "
            "Bedrock' name everywhere instead",
        )

    def test_official_name_used_multiple_times(self):
        count = self.text.count(OFFICIAL_NAME)
        self.assertGreaterEqual(
            count,
            5,
            "expected the official 'Guardrails for Amazon Bedrock' name "
            "to be used consistently throughout Domain 2 (found "
            f"{count} occurrences)",
        )

    def test_mini_quiz_agent_question_uses_official_name(self):
        # Section 5's mini-quiz has a question about multi-step task
        # execution whose first (incorrect) answer option previously read
        # "A. Amazon Bedrock Guardrails" instead of the official name.
        idx = self.text.index(
            "Which AWS offering lets a foundation model plan and execute "
            "multi-step"
        )
        question_block = self.text[idx : idx + 400]
        self.assertIn("A. Guardrails for Amazon Bedrock", question_block)

    def test_support_assistant_worked_example_uses_official_name(self):
        # The "building an end-to-end generative AI support assistant"
        # worked example previously used the informal name when describing
        # the guardrails configuration step.
        idx = self.text.index("Add guardrails before exposing it to customers.")
        step_block = self.text[idx : idx + 300]
        self.assertIn("Guardrails for Amazon Bedrock", step_block)
        self.assertNotIn("Amazon Bedrock Guardrails", step_block)


if __name__ == "__main__":
    unittest.main()
