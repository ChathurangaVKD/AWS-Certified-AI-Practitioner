"""Structural validation for the bias-metric/tool-selection Mermaid
flowchart added to docs/domain-4-guidelines-for-responsible-ai.md.

The gap this covers: Domain 4's "Comparison table: AWS responsible AI
tools at a glance" and the prose "Decision framework: choosing a bias
metric and layering tools for high-stakes AI" section that follows it
explain, in words only, (1) when to check DPL vs. Disparate Impact, (2)
when a high-stakes use case should favor an interpretable model plus
SHAP, and (3) when Amazon A2I human review should be layered on top --
but neither included a diagram tying those three decisions together, so
readers had to infer the decision path from a static table and paragraphs
of prose (flagged by the documentation scan as a missing diagram). This
test guards the new Mermaid flowchart added immediately after the
comparison table (and its "Exam tip" callout), before the "Decision
framework" heading, covering all three decision points end to end.

Mirrors the conventions established in
tests/test_domain_4_bias_metric_decision_framework.py and
tests/test_domain_3_embedding_model_selection_diagram.py.

Run with:
    python3 -m unittest tests/test_domain_4_bias_metric_tool_selection_flowchart.py -v
"""

import re
import unittest
from pathlib import Path

DOC_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "domain-4-guidelines-for-responsible-ai.md"
)

COMPARISON_HEADING = "## Comparison table: AWS responsible AI tools at a glance"
FRAMEWORK_HEADING = (
    "## Decision framework: choosing a bias metric and layering tools "
    "for high-stakes AI"
)


def _read_doc():
    return DOC_PATH.read_text(encoding="utf-8")


class TestDomain4BiasMetricToolSelectionFlowchart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _read_doc()
        comparison_idx = cls.text.index(COMPARISON_HEADING)
        framework_idx = cls.text.index(FRAMEWORK_HEADING)
        cls.between = cls.text[comparison_idx:framework_idx]
        fences = re.findall(r"```mermaid\n(.*?)```", cls.between, re.S)
        cls.diagrams = fences

    def test_flowchart_is_placed_between_comparison_table_and_decision_framework(
        self,
    ):
        self.assertTrue(
            self.diagrams,
            "expected a ```mermaid fenced diagram between the comparison "
            "table and the 'Decision framework' heading",
        )

    def test_flowchart_uses_mermaid_flowchart_syntax(self):
        diagram = "\n".join(self.diagrams)
        self.assertRegex(
            diagram,
            r"flowchart\s+\w+|graph\s+\w+",
            "diagram should use Mermaid flowchart/graph syntax",
        )

    def test_flowchart_branches_on_training_data_vs_predictions_to_dpl_vs_disparate_impact(
        self,
    ):
        diagram = "\n".join(self.diagrams)
        self.assertRegex(
            diagram,
            r"(?i)training data",
            "diagram missing a training-data audit branch",
        )
        self.assertRegex(
            diagram,
            r"(?i)predictions",
            "diagram missing a model-predictions audit branch",
        )
        self.assertIn("DPL", diagram)
        self.assertRegex(diagram, r"(?i)disparate impact")

    def test_flowchart_branches_on_high_stakes_to_interpretable_model_and_shap(self):
        diagram = "\n".join(self.diagrams)
        self.assertRegex(diagram, r"(?i)high-stakes")
        self.assertRegex(diagram, r"(?i)interpretable model")
        self.assertIn("SHAP", diagram)

    def test_flowchart_branches_on_human_review_to_a2i(self):
        diagram = "\n".join(self.diagrams)
        self.assertRegex(diagram, r"(?i)human review")
        self.assertRegex(diagram, r"(?i)Amazon A2I")

    def test_flowchart_mentions_model_card_documentation_endpoint(self):
        # The three decisions should still terminate in the existing
        # documentation practice (Model Cards) established earlier in the
        # doc, so the diagram doesn't dead-end without a record of what
        # was decided.
        diagram = "\n".join(self.diagrams)
        self.assertRegex(diagram, r"(?i)model card")

    def test_flowchart_poses_branching_decision_questions(self):
        diagram = "\n".join(self.diagrams)
        self.assertIn("?", diagram)
        # Mermaid decision nodes use curly braces; there should be at
        # least the three decision points described in the task: data vs.
        # predictions, high-stakes or not, and human review required or
        # not.
        decision_nodes = re.findall(r"\{[^{}]+\}", diagram)
        self.assertGreaterEqual(
            len(decision_nodes),
            2,
            "expected at least two Mermaid decision ({...}) nodes beyond "
            "the initial data-vs-predictions branch",
        )


if __name__ == "__main__":
    unittest.main()
