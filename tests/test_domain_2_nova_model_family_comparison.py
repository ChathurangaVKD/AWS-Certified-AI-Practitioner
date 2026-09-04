"""Structural validation for the "Comparing Amazon Nova model variants"
subsection added to docs/domain-2-fundamentals-of-generative-ai.md, plus its
cross-reference from docs/domain-3-applications-of-foundation-models.md.

The gap this covers: Domain 2's worked examples and Section 7 (foundation
model selection criteria) previously only showed **Amazon Nova Canvas** and
**Amazon Nova Premier** in comparisons against other model families (e.g.,
Claude Sonnet vs. Nova Premier in Domain 3's model-tier worked example). The
remaining Nova variants -- Micro, Lite, Pro, Reel, and Sonic -- were listed
individually in docs/aws-service-index.md and
docs/aws-service-decision-guide.md, but nowhere did the domain guides walk
through the *whole* Nova family side by side with cost/latency/use-case
selection criteria the way the Claude and Llama families are compared in
Domain 3's "Context window vs. cost and latency" table. These tests guard
the new Domain 2 subsection (heading, TOC entry, a 7-row table covering every
Nova variant, and an AWS example distinguishing Micro/Lite/Pro) and the new
Domain 3 cross-reference sentence pointing back to it, so a future edit can't
silently drop either piece or regress back to only covering Canvas/Premier.

Run with:
    python3 -m unittest tests/test_domain_2_nova_model_family_comparison.py -v
"""

import re
import unittest
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
DOMAIN_2_PATH = DOCS_DIR / "domain-2-fundamentals-of-generative-ai.md"
DOMAIN_3_PATH = DOCS_DIR / "domain-3-applications-of-foundation-models.md"

HEADING = "### Comparing Amazon Nova model variants"
ANCHOR = "#comparing-amazon-nova-model-variants"
TOC_LINK = f"[Comparing Amazon Nova model variants]({ANCHOR})"
CROSS_LINK = f"domain-2-fundamentals-of-generative-ai.md{ANCHOR}"

# Every Nova variant the task calls out as missing comparison coverage.
NOVA_VARIANTS = [
    "Nova Micro",
    "Nova Lite",
    "Nova Pro",
    "Nova Premier",
    "Nova Canvas",
    "Nova Reel",
    "Nova Sonic",
]


def _read(path):
    return path.read_text(encoding="utf-8")


def _section(text, start_heading_regex, end_heading_regex):
    start = re.search(start_heading_regex, text)
    assert start, f"heading not found: {start_heading_regex}"
    rest = text[start.end():]
    end = re.search(end_heading_regex, rest)
    return rest[: end.start()] if end else rest


class TestDomain2NovaModelFamilyComparisonSubsection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read(DOMAIN_2_PATH)
        cls.subsection = _section(
            cls.text, re.escape(HEADING), r"\n#{1,4} "
        )

    def test_heading_exists(self):
        self.assertIn(HEADING, self.text)

    def test_is_linked_from_the_table_of_contents(self):
        toc = _section(
            self.text, r"\n## Table of contents", r"\n## Domain overview"
        )
        self.assertIn(TOC_LINK, toc)

    def test_sits_inside_section_7_before_its_mini_quiz(self):
        section_7 = _section(
            self.text,
            r"\n## 7\. Foundation model selection criteria",
            r"\n---\n\n## Worked example",
        )
        heading_pos = section_7.index(HEADING)
        quiz_pos = section_7.index(
            "#### Mini-quiz: Test your understanding of foundation model "
            "selection criteria"
        )
        self.assertLess(heading_pos, quiz_pos)

    def test_table_covers_every_nova_variant(self):
        for variant in NOVA_VARIANTS:
            with self.subTest(variant=variant):
                self.assertIn(f"**{variant}**", self.subsection)

    def test_table_has_a_row_per_variant_with_five_columns(self):
        table_lines = [
            line
            for line in self.subsection.splitlines()
            if line.strip().startswith("|") and "**Nova " in line
        ]
        self.assertEqual(
            len(table_lines),
            len(NOVA_VARIANTS),
            "expected exactly one table row per Nova variant",
        )
        for line in table_lines:
            with self.subTest(line=line):
                # 5 data columns => 6 pipe-delimited cells including the
                # leading/trailing empty strings from split("|").
                cells = line.strip().split("|")
                self.assertEqual(len(cells), 7, f"malformed table row: {line!r}")

    def test_distinguishes_text_tiers_from_output_modality_variants(self):
        lowered = self.subsection.lower()
        # Text-oriented tiers should read as an escalating cost/latency
        # ladder, matching the task's "increasing capability/cost" framing.
        self.assertIn("lowest", lowered)
        self.assertIn("moderate", lowered)
        self.assertIn("highest", lowered)
        # Canvas/Reel/Sonic should be called out as separate-by-modality,
        # not a fourth rung on the text-tier cost ladder.
        self.assertIn("image generation", lowered)
        self.assertIn("video generation", lowered)
        self.assertIn("speech-to-speech", lowered)

    def test_has_an_aws_example_distinguishing_micro_lite_pro(self):
        self.assertIn("AWS example:", self.subsection)
        aws_example = self.subsection[self.subsection.index("AWS example:"):]
        # Markdown source-wraps long lines, so "Nova Micro" may have a
        # newline between the two words -- match across that wrap.
        for variant in ("Nova\\s+Micro", "Nova\\s+Lite", "Nova\\s+Pro"):
            with self.subTest(variant=variant):
                self.assertRegex(aws_example, variant)

    def test_has_an_exam_tip(self):
        self.assertIn("Exam tip:", self.subsection)

    def test_cross_links_back_to_section_5_nova_intro(self):
        self.assertIn(
            "(#5-aws-generative-ai-services-and-capabilities)", self.subsection
        )


class TestDomain3CrossReferencesNovaModelFamilyComparison(unittest.TestCase):
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

    def test_section_1_mentions_the_full_nova_family_by_name(self):
        lowered = self.section_1.lower()
        for variant in NOVA_VARIANTS:
            with self.subTest(variant=variant):
                self.assertIn(variant.lower(), lowered)


if __name__ == "__main__":
    unittest.main()
