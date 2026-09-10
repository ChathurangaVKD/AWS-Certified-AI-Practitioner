# Domain 1 Fast Track / Ultra Fast Learn: coverage verification report

**Status:** technical verification complete · **Verified:** 2026-09-09

## What this report is

`docs/DOCUMENTATION_STRUCTURE.md` states a coverage guarantee for every
domain's condensed layer: "every testable concept the full domain guide
covers is retained somewhere in the condensed layer — only narrative
explanation, extra worked examples, and repetition are cut, not
exam-relevant content." For Domain 1 specifically, that guarantee had not
been technically verified — it was flagged as a claim requiring spot-check
against the source material. This report is that spot-check: a
line-by-line comparison of four major sections of
[`docs/domain-1-fundamentals-of-ai-and-ml.md`](../domain-1-fundamentals-of-ai-and-ml.md)
(2,030 lines) against
[`docs/domain-1-fast-track/README.md`](README.md) (743 lines) and
[`docs/domain-1-fast-track/ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md)
(192 lines), confirming whether every exam-relevant fact, decision
criterion, AWS service, metric, and concept survives both condensation
hops.

This is a correctness audit, not new content authoring: it documents what
was checked, what verified clean, and where a real gap was found. It does
not itself change `README.md` or `ULTRA-FAST-LEARN.md`.

## Sections spot-checked

| # | Full guide section | Fast Track section | Ultra Fast Learn section |
|---|---|---|---|
| 1 | [§2 The ML development lifecycle](../domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle) (line 178) — incl. the Managed Spot Training worked example (line 329) and the production deployment strategies subsection (line 500) | [§2](README.md#2-the-ml-development-lifecycle) (line 136) | [§1](ULTRA-FAST-LEARN.md#1-the-8-stage-ml-development-lifecycle) (line 27) |
| 2 | [§4 Common use cases for AI/ML](../domain-1-fundamentals-of-ai-and-ml.md#4-common-use-cases-for-aiml) (line 789) | [§4](README.md#4-common-use-cases-for-aiml) (line 285) | folded into [§3](ULTRA-FAST-LEARN.md#3-aws-aiml-services-compact-decision-table) (line 61) |
| 3 | [§5 AWS managed AI/ML services](../domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview) (line 898), incl. the SageMaker Ground Truth subsection and its labeling-alternatives decision table (line 989–1087) | [§5](README.md#5-aws-managed-aiml-services) (line 314) | [§3](ULTRA-FAST-LEARN.md#3-aws-aiml-services-compact-decision-table) (line 61) |
| 4 | [§6 Model evaluation basics](../domain-1-fundamentals-of-ai-and-ml.md#6-model-evaluation-basics) (line 1090) | [§6](README.md#6-model-evaluation-basics) (line 369) | [§4](ULTRA-FAST-LEARN.md#4-classification-evaluation-metrics) (line 80) |

## Result: Fast Track (full guide → Fast Track hop)

**Verified clean — no gaps found.** For all four sections above, every
exam-relevant fact, decision criterion, AWS service, metric, and named
constraint in the full guide is present in the Fast Track, condensed to
tables and shortened exam tips but with no testable content dropped.
Specifically confirmed:

- The full 8-stage lifecycle, its loop-back triggers, SageMaker Autopilot's
  capabilities and its three named blockers (custom loss function,
  domain-specific feature engineering, novel architecture).
- **Managed Spot Training vs. On-Demand**: the ~90% savings figure, the
  2-minute interruption notice, the checkpointing requirement
  (`checkpoint_s3_uri`) and what happens without it (job restarts from 0%),
  the billing-only-for-compute-consumed rule, and the deciding factor
  (fixed deadline/compliance SLA → On-Demand) — all retained in Fast Track
  §2's "Managed Spot Training vs. On-Demand training" table.
- **Production deployment strategies and SageMaker Model Registry**: all
  four rollout patterns (canary, blue/green, A/B testing, shadow
  deployment) distinguished by intent, plus the Model Registry
  register → approve → deploy flow and its distinction from Model Monitor
  and Model Cards — all retained in Fast Track §2.
- All ten common-use-case → AWS-service mappings from §4, folded into Fast
  Track §4's scenario-verb table.
- The full **Ground Truth vs. alternatives** decision surface: Ground
  Truth, manual labeling, Data Wrangler, standalone active learning, weak
  supervision, and synthetic data generation, each with its deciding
  constraint — all retained in Fast Track §5's two comparison tables.
- All six evaluation metrics (accuracy, precision, recall, F1, AUC-ROC,
  RMSE/MAE), the scenario → metric table, the accuracy-paradox exam trap,
  and the threshold/precision/recall trade-off direction — all retained in
  Fast Track §6.

## Result: Ultra Fast Learn (Fast Track → Ultra Fast Learn hop)

**Three coverage gaps found.** `ULTRA-FAST-LEARN.md` is deliberately far
more compressed than the Fast Track (192 lines vs. 743), and its own intro
says it omits "decision flowcharts, condensed worked example, and rapid
self-check" by design — that trim is expected and consistent with the
guarantee (narrative and worked examples are the parts allowed to go).
However, three items that are *decision criteria and named AWS
services/concepts*, not narrative, are missing entirely rather than
condensed:

1. **Managed Spot Training vs. On-Demand training is entirely absent.**
   `ULTRA-FAST-LEARN.md` §1's lifecycle table names "Managed Spot Training"
   as a tool for stage 5 (line 35) but nowhere states the decision
   criterion the exam actually tests: checkpointing is required to resume
   instead of restarting from 0%, and a fixed-deadline/compliance-SLA
   retrain should use On-Demand instead of Spot. Grepping the file for
   `spot|checkpoint` outside that one table cell returns nothing.

2. **Production deployment strategies and SageMaker Model Registry are
   entirely absent.** None of canary, blue/green, A/B testing, shadow
   deployment, or SageMaker Model Registry appears anywhere in
   `ULTRA-FAST-LEARN.md`. This is a named, exam-tip-flagged decision surface
   in both the full guide (line 500–648, with its own worked example at
   line 586) and the Fast Track (line 208–242), but the Ultra Fast Learn
   cram sheet's lifecycle section stops at stage 8 (Monitoring) and never
   mentions it.

3. **The Ground Truth vs. active learning vs. weak supervision vs.
   synthetic data decision table is entirely absent.** `ULTRA-FAST-LEARN.md`
   §3 (line 76) has exactly one row for Ground Truth ("human-in-the-loop
   labeling to produce training data"), but the deciding exam
   detail — which of these four/five options a scenario is describing,
   based on whether the scenario names a tight **labeling budget**,
   expressible *rules*, *scarce/rare* data, or a large genuinely
   *unlabeled pool* — is present in both the full guide (line 1040–1087)
   and the Fast Track (line 346–361) and does not appear in the Ultra Fast
   Learn cram sheet at all.

Corroborating evidence: `tests/test_domain_1_ultra_fast_learn.py`
(`TestUltraFastLearnContent`) enumerates the concepts the cram sheet is
expected to cover — the 8 lifecycle stages, the 3 learning types, 11 AWS
services, 7 evaluation metrics, bias-variance terms, and ensemble
methods — and that checklist itself does not mention Model Registry,
canary/blue-green/A-B/shadow deployment, Managed Spot Training's
checkpointing rule, or the Ground Truth-alternatives table. The existing
test suite does not catch this gap because it was never written to check
for these three items in the first place.

## Recommendation

Backfill `ULTRA-FAST-LEARN.md` with three condensed additions (tables only,
no prose/worked examples, consistent with the file's existing format),
sourced verbatim from Fast Track §2 and §5 (no new facts to author):

1. A "Managed Spot Training vs. On-Demand" table under the lifecycle
   section (cost / risk / checkpointing requirement / billing / best-for).
2. A "Production deployment strategies & Model Registry" table (canary,
   blue/green, A/B testing, shadow deployment by intent, plus the
   Model Registry register → approve → deploy flow).
3. A "Ground Truth vs. alternatives" table (Ground Truth, manual labeling,
   Data Wrangler, active learning, weak supervision, synthetic data, each
   with its deciding constraint).

Each addition should also extend the "Common exam traps checklist" and
`TestUltraFastLearnContent` in `tests/test_domain_1_ultra_fast_learn.py`
with assertions for the newly-covered terms, so a future edit cannot
silently drop this content again. This backfill is scoped as follow-up
work rather than folded into this report, since `ULTRA-FAST-LEARN.md`'s
stated line count is cross-checked by exact-total assertions in
`tests/test_documentation_structure.py` (per-domain Fast Track totals and
the repository-wide grand total) that must be updated in lockstep with any
line-count change to that file.
