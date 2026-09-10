# Domain 4 Ultra Fast Track: Guidelines for Responsible AI

**Ultra-condensed cram sheet** · fast track: [`docs/domain-4-fast-track/README.md`](README.md) (796 lines) · full guide: [`docs/domain-4-guidelines-for-responsible-ai.md`](../domain-4-guidelines-for-responsible-ai.md) (2,247 lines) · **Last verified:** 2026-09-05

Bullets and tables only — no prose, no worked examples, no mini-quizzes.
For the last 15-20 minutes before the exam, once the fast track guide is
already familiar and you just need the highest-yield tables refreshed one
more time. Domain 4 is roughly **14%** of scored questions.

## Table of contents

- [1. Dimensions of responsible AI](#1-dimensions-of-responsible-ai)
- [2. Common bias sources](#2-common-bias-sources)
- [3. Fairness metrics by use case / stage](#3-fairness-metrics-by-use-case-stage)
- [4. Key trade-offs](#4-key-trade-offs)
- [5. AWS tools for responsible AI](#5-aws-tools-for-responsible-ai)
- [6. Monitoring checklist](#6-monitoring-checklist)
- [7. Legal and ethical considerations](#7-legal-and-ethical-considerations)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Common exam traps checklist](#common-exam-traps-checklist)
- [Where each row comes from](#where-each-row-comes-from)

---

## 1. Dimensions of responsible AI

| Dimension | Key question | Primary AWS tool |
|---|---|---|
| **Fairness** | Equitable treatment across groups/protected characteristics? | SageMaker Clarify (bias metrics) |
| **Explainability** | Why did the model produce *this* prediction? | SageMaker Clarify (SHAP) |
| **Privacy and security** | Is personal data protected; is the model protected from misuse? | Guardrails (PII redaction); Amazon Macie |
| **Transparency** | Is the whole system's build/training/limits documented? | SageMaker Model Cards / AI Service Cards |
| **Veracity and robustness** | Correct and reliable, even under noisy/adversarial input? | Guardrails (contextual grounding) |
| **Governance** | Policies/processes controlling the AI lifecycle? | Model Cards; ML lineage tracking |
| **Safety** | Avoids harmful/dangerous generated content? | Guardrails (content filters) |
| **Controllability** | Can a human monitor, override, or stop it? | Guardrails (denied topics); Amazon A2I |

- **Highest-tested four:** fairness, explainability, privacy and security,
  and transparency drive most scenario questions — the other four
  (veracity/robustness, governance, safety, controllability) round out the
  full 8-dimension model.
- One prediction → **explainability**; whole system documented → **transparency**.
  Treats groups equitably → **fairness**; a human can step in → **controllability**.

## 2. Common bias sources

| Bias type | One-line definition |
|---|---|
| **Sampling bias** | Training data doesn't represent the real-world population |
| **Measurement bias** | A proxy feature (e.g., ZIP code) correlates with a protected characteristic more than the real outcome |
| **Label / human bias** | Annotators inject conscious/unconscious bias while labeling |
| **Historical bias** | Data accurately reflects a real world that is itself inequitable |
| **Exclusion bias** | Relevant data/features dropped, removing signal a group needs |
| **Aggregation bias** | One model applied uniformly to groups that need distinct treatment |
| **Representativeness bias** | A whole deployment segment (region/market) is thin/absent from training data — no group label exists, so standard fairness metrics miss it |

- A named **proxy variable** in a scenario → measurement bias, fixed by
  dropping/transforming the feature, not by rebalancing classes.
- A clean fairness-metric report does **not** rule out representativeness
  bias — check per-segment coverage and accuracy separately.

## 3. Fairness metrics by use case / stage

| Question | Metric | Stage | Computed by |
|---|---|---|---|
| Positive label rate differs across groups in the *dataset*? | **Difference in proportions of labels (DPL)** | Pre-training | Clarify — dataset job |
| A class/group is underrepresented in the dataset? | **Class imbalance** | Pre-training | Clarify — dataset job |
| A trained model's outcome rates differ across groups? | **Disparate impact** | Post-training | Clarify — model job |
| Accuracy/recall differs materially across groups? | **Accuracy/recall difference** | Post-training | Clarify — model job |

**By use case:**

| Use case | Highest-value metric |
|---|---|
| Credit/loan approval | Disparate impact + DPL (pre- and post-training) |
| Hiring/resume screening | DPL (dataset), disparate impact (predictions) |
| Healthcare triage/diagnosis | Accuracy/recall difference across demographic groups |
| Content moderation | Class imbalance (dataset), accuracy difference (predictions) |
| RAG/generative assistant | No labeled dataset — audit **retrieval corpus** coverage instead |

- No model yet, checking labels → **DPL**/class imbalance. Predictions,
  an endpoint, or a deployed model → **disparate impact**/accuracy-recall
  difference.

## 4. Key trade-offs

**Fairness vs. accuracy:**

| | Favor fairness | Favor accuracy |
|---|---|---|
| Typical fix | Pre-processing rebalance, in-processing fairness constraints, post-processing threshold calibration | Leave the higher-accuracy model/objective unconstrained |
| Cost | Accuracy can drop when a constraint forces equalized outcomes across groups | Risk of disparate impact on a protected group |
| Favor when | High-stakes, regulated decisions (credit, hiring, healthcare) | Low-stakes tasks with no protected-group exposure |

**Explainability vs. latency:**

| | Natively interpretable model | Post-hoc SHAP (SageMaker Clarify) |
|---|---|---|
| Added inference-time compute | None — the model's logic *is* the explanation | Extra computation per explanation (Shapley value estimation) |
| Real-time / low-latency fit | Best fit — explanation is free | Often run as an offline/batch job, not synchronously per request |
| Accuracy | Often lower on complex tasks | Often higher — no interpretability constraint on the model |
| Reflects actual decision logic? | Yes | No — an approximation only |

- A scenario requiring an explanation **and** strict real-time latency
  pushes toward a **natively interpretable model**, not synchronous
  post-hoc SHAP.
- A regulation requiring the explanation reflect **actual decision
  logic** disqualifies post-hoc SHAP regardless of latency budget.

## 5. AWS tools for responsible AI

| Tool | Detects / does | Applies to |
|---|---|---|
| **SageMaker Clarify** | Pre/post-training bias metrics + SHAP explainability | Datasets & trained models |
| **SageMaker Model Cards** | Self-authored documentation — intended use, training data, limits | Models you build |
| **AI Service Cards** | AWS-authored documentation of a managed AI service | AWS-managed AI services |
| **Guardrails for Amazon Bedrock** | Runtime safety/privacy filtering | FM input/output at inference |
| **Amazon A2I** | Human-in-the-loop review routing | Low-confidence/high-stakes predictions |

- **Model Card = you fill it in** (self-authored, your model).
  **AI Service Card = AWS publishes it** (AWS-managed service).

**Guardrails — five capabilities:**

| Capability | Blocks / does |
|---|---|
| **Denied topics** | Blocks the model from engaging with specified topics |
| **Content filters** | Blocks harmful categories at configurable strength |
| **Word filters** | Blocks specific words/phrases |
| **Sensitive information filters** | Detects/redacts or blocks **PII** |
| **Contextual grounding checks** | Verifies a response is grounded in source content |

- `StartHumanLoop` (**Amazon A2I**) routes a low-confidence prediction to
  a human review workflow: a **flow definition** (activation condition)
  plus a **worker task template** (reviewer-facing UI) plus a workforce.
- **Private workforce** (Amazon Cognito) required for regulated data
  (e.g. PHI); public **Mechanical Turk** otherwise.

**SageMaker Clarify capabilities:**

- **Pre-training bias metrics** — class imbalance, difference in
  proportions of labels (DPL), computed on the raw dataset.
- **Post-training bias metrics** — disparate impact, accuracy/recall
  difference, computed on a trained model's predictions.
- **SHAP-based explainability** — per-prediction feature-attribution
  values for a trained model (an approximation, not an exact trace).
- **Bias reports** — generated artifacts summarizing metric results,
  attachable to a SageMaker Model Card.
- **Integration with SageMaker Model Monitor** — feeds ongoing bias-drift
  monitoring on a deployed endpoint.
- **Applies to** datasets and trained models (typically SageMaker) — not
  live foundation-model input/output (that's Guardrails' job).

## 6. Monitoring checklist

- [ ] **Bias drift** — disparate impact / accuracy-recall difference
      tracked over time via SageMaker Model Monitor + Clarify.
- [ ] **Confidence-threshold drift** — rising share of predictions below
      an Amazon A2I routing threshold signals population drift.
- [ ] **Runtime content/safety drift** — Guardrails intervention logs
      (blocked topics, filtered content, redacted PII) reviewed over time.
- [ ] **Coverage/representativeness drift** — new regions/segments in
      production traffic checked against training-data coverage.
- [ ] **Two-component systems** — a structured model and a paired FM each
      get their own independent monitoring stream, never one blended metric.
- [ ] **Governance cadence** — recurring (e.g. quarterly) review of the
      SageMaker Model Card against the latest Clarify/Model Monitor
      metrics; high-risk flags route through Amazon A2I.

## 7. Legal and ethical considerations

| Category | What it covers | AWS mitigation |
|---|---|---|
| **Intellectual property (IP)** | Ownership of AI-generated content; liability for content resembling copyrighted training material | Choose a Bedrock provider offering **IP indemnification** |
| **Data privacy** | **GDPR**, **data residency**, minimizing/anonymizing personal data | Guardrails sensitive information filters (PII redaction); **Amazon Macie** |
| **Toxicity** | Hateful, harassing, obscene, or otherwise harmful generated content | Guardrails content filters; Amazon A2I human review |
| **Environmental impact** | Energy/compute/carbon footprint of training and running FMs | Reuse pretrained FMs (prompting/RAG/fine-tuning); **AWS Customer Carbon Footprint Tool**; **Well-Architected Sustainability Pillar** |

- **IP risk → IP indemnification**, not Guardrails (content
  safety/privacy, not copyright liability) — keep **toxicity**, **data
  privacy**, and **IP** as three separate, non-overlapping categories.

---

## Rapid-fire key terms

- **Responsible AI** — fair, explainable, private/secure, transparent,
  veracious/robust, governed, safe, and controllable AI systems.
- **SHAP** — feature-attribution values quantifying one prediction; an
  approximation, not an exact decision trace.
- **PII** — personally identifiable information; a Guardrails
  sensitive-information-filter target.
- **IP indemnification** — a contractual protection shifting
  IP-infringement legal risk away from the customer.
- **AWS Customer Carbon Footprint Tool** — reports estimated carbon
  emissions from a customer's AWS usage.
- **Amazon Macie** — discovers/classifies sensitive data (incl. PII)
  stored in Amazon S3.

## Common exam traps checklist

- [ ] **Bias vs. variance** — fairness/training-data problem vs.
      model-sensitivity/overfitting problem (Domain 1). Don't conflate.
- [ ] **Guardrails filters live inference content**; it doesn't detect
      training-data bias or generate explanations — that's Clarify's job.
- [ ] **Representativeness gaps evade standard fairness metrics** — a
      clean Clarify report doesn't rule out a thin/absent segment.
- [ ] **Two components (tabular model + generative FM) need two tools** —
      Clarify on the tabular model, Guardrails on the FM — never blended.
- [ ] **SHAP is an approximation, not an exact decision trace** — only a
      natively interpretable model satisfies an actual-decision-logic requirement.
- [ ] **Model Card = self-authored; AI Service Card = AWS-authored.**

---

## Where each row comes from

| This cram sheet | Fast track section |
|---|---|
| 1. Dimensions of responsible AI | [Section 1](README.md#1-core-dimensions-of-responsible-ai) |
| 2. Common bias sources | [Section 2](README.md#2-bias-and-fairness) |
| 3. Fairness metrics by use case / stage | [Section 2](README.md#2-bias-and-fairness) |
| 4. Key trade-offs | [Section 5](README.md#5-performance-vs-interpretability) |
| 5. AWS tools for responsible AI | [Section 3](README.md#3-aws-tools-for-responsible-ai) |
| 6. Monitoring checklist | [Monitoring section](README.md#monitoring-responsible-ai-in-production) |
| 7. Legal and ethical considerations | [Section 4](README.md#4-legal-and-ethical-considerations) |
| Rapid-fire key terms | [Rapid-fire key terms](README.md#rapid-fire-key-terms) |
| Common exam traps checklist | [Common exam traps checklist](README.md#common-exam-traps-checklist) |

For the full tables, decision flowcharts, worked examples, and rapid
self-check this cram sheet intentionally omits, go back to the
[Domain 4 fast track](README.md) or the
[full Domain 4 guide](../domain-4-guidelines-for-responsible-ai.md). For
material spanning multiple domains, see
[`docs/cross-domain-concept-map.md`](../cross-domain-concept-map.md).

[← Back to the Domain 4 fast track](README.md) · [Full Domain 4 guide →](../domain-4-guidelines-for-responsible-ai.md)
