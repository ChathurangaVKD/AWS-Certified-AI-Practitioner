"""Structural validation for the "Cost and latency implications of
temperature, top-p, and top-k" subsection added to
docs/domain-2-fundamentals-of-generative-ai.md, plus its cross-reference
from docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 2's Section 6 ("Prompt engineering
fundamentals") explained temperature, top-p, and top-k as output-shaping
levers and how they interact with each other
(tests/test_domain_2_inference_parameter_interactions.py), but never
connected any of that to **cost or latency** -- e.g., a lower temperature
reducing retries (and therefore effective token consumption), or how
autoregressive decoding means response length, not the sampling strategy
itself, drives per-request latency. Domain 3's "Design considerations"
section separately covered cost and latency as FM-selection factors but
never mentioned inference parameters as a lever on either. These tests
guard the new Domain 2 subsection (heading, retry/token-consumption
explanation, a worked budget example with the specific dollar and
time-savings figures) and the new Domain 3 cross-reference paragraph
pointing back to it, so a future edit can't silently drop either piece.

Run with:
    python3 -m unittest tests/test_domain_2_inference_parameter_cost_latency.py -v
"""

import re
import unittest
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
DOMAIN_2_PATH = DOCS_DIR / "domain-2-fundamentals-of-generative-ai.md"
DOMAIN_3_PATH = DOCS_DIR / "domain-3-applications-of-foundation-models.md"

HEADING = "### Cost and latency implications of temperature, top-p, and top-k"
TOC_LINK = (
    "[Cost and latency implications of temperature, top-p, and top-k]"
    "(#cost-and-latency-implications-of-temperature-top-p-and-top-k)"
)
CROSS_LINK = (
    "domain-2-fundamentals-of-generative-ai.md"
    "#cost-and-latency-implications-of-temperature-top-p-and-top-k"
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain2InferenceParameterCostLatencySubsection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOMAIN_2_PATH)
        cls.subsection = _section(cls.text, re.escape(HEADING), r"\n#{1,3} ")

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(self.text, r"\n## Table of contents", r"\n## Domain overview")
        self.assertIn(TOC_LINK, toc)

    def test_sits_inside_section_6_before_its_mini_quiz(self):
        section_6 = _section(
            self.text,
            r"\n## 6\. Prompt engineering fundamentals",
            r"\n## 7\. ",
        )
        heading_pos = section_6.index(HEADING)
        quiz_pos = section_6.index(
            "#### Mini-quiz: Test your understanding of prompt engineering "
            "fundamentals"
        )
        self.assertLess(heading_pos, quiz_pos)

    def test_explains_retries_drive_effective_token_consumption(self):
        lowered = self.subsection.lower()
        self.assertIn("retry", lowered)
        self.assertIn("retries", lowered)
        self.assertRegex(
            self.subsection,
            r"(?i)(don't|do not) change the per-token price",
            "should explicitly say sampling settings don't change the "
            "per-token price, only the effective token/retry count",
        )

    def test_explains_autoregressive_decoding_and_stop_conditions(self):
        self.assertIn("autoregressive", self.subsection.lower())
        self.assertIn("stop sequence", self.subsection.lower())
        self.assertIn("maximum length", self.subsection.lower())

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_has_a_worked_budget_example_with_correct_figures(self):
        self.assertIn("Worked example", self.subsection)
        for expected in [
            "50,000",
            "12%",
            "1.5%",
            "$100.80",
            "$91.35",
            "$9.45",
            "$283.50",
            "10,500",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.subsection)

    def test_worked_example_cross_links_to_provisioned_throughput(self):
        self.assertIn(
            "domain-3-applications-of-foundation-models.md"
            "#5-amazon-bedrock-features",
            self.subsection,
        )
        self.assertIn("provisioned throughput", self.subsection.lower())


class TestDomain3CrossReferencesInferenceParameterCostLatency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOMAIN_3_PATH)
        cls.section_1 = _section(
            cls.text,
            r"\n## 1\. Design considerations for foundation model applications",
            r"\n## 2\. ",
        )

    def test_section_1_cross_links_to_domain_2_subsection(self):
        self.assertIn(CROSS_LINK, self.section_1)

    def test_section_1_mentions_retries_as_the_cost_mechanism(self):
        self.assertIn("retries", self.section_1.lower())
        self.assertIn("temperature", self.section_1.lower())

    def test_cross_link_sits_before_the_context_window_subsection(self):
        link_pos = self.section_1.index(CROSS_LINK)
        context_window_pos = self.section_1.index(
            "### Context window vs. cost and latency: comparing model tiers"
        )
        self.assertLess(link_pos, context_window_pos)


if __name__ == "__main__":
    unittest.main()
