# Domain 4 Ultra Fast Track: Guidelines for Responsible AI

**Ultra-condensed cram sheet** · fast track: [`docs/domain-4-fast-track/README.md`](README.md) (796 lines) · full guide: [`docs/domain-4-guidelines-for-responsible-ai.md`](../domain-4-guidelines-for-responsible-ai.md) (2,247 lines) · **Last verified:** 2026-09-09

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
- [6. Legal and ethical considerations](#6-legal-and-ethical-considerations)
- [7. Monitoring checklist](#7-monitoring-checklist)
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

| Tool | Primary use case | Applies to |
|---|---|---|
| **Amazon SageMaker Clarify** | Bias detection (pre-/post-training) + SHAP explainability | Datasets and trained models |
| **Amazon SageMaker Model Cards** | Structured documentation for a model **you** built | Models you build (typically SageMaker) |
| **AI Service Cards** | AWS-published documentation for an **AWS-managed** AI service | Services like Rekognition, Transcribe |
| **Guardrails for Amazon Bedrock** | Runtime safety/privacy filtering on live FM input/output | Foundation models at inference (Bedrock) |
| **Amazon A2I** | Human-in-the-loop review workflows | Predictions from ML models or AWS AI services |

- **Model Card = you fill it in** (a model you built); **AI Service Card =
  AWS publishes it, you read it** (an AWS-managed service).

**Amazon SageMaker Clarify capabilities:**

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

**Guardrails for Amazon Bedrock — 5 capabilities:**

| Capability | Blocks/does | Feeds which dimension |
|---|---|---|
| **Denied topics** | Blocks the model from engaging with specified topics entirely | Controllability |
| **Content filters** | Blocks harmful categories (hate, insults, sexual, violence, misconduct, prompt attacks) at configurable strength | Safety |
| **Word filters** | Blocks specific words/phrases (profanity, competitor names) | Safety |
| **Sensitive information filters** | Detects/redacts or blocks PII in prompts and responses | Privacy and security |
| **Contextual grounding checks** | Verifies a response is grounded in provided source content, reducing hallucination | Veracity and robustness |

**Amazon A2I mechanics:**

- Predictions below the routing threshold invoke `StartHumanLoop` instead
  of an automated action.
- A **flow definition** ties a **worker task template** (the reviewer-facing
  UI) to an activation condition — keep it on the *same* threshold as the
  routing logic so the two never drift apart.
- A **private workforce** (via Amazon Cognito), not public Mechanical
  Turk, is required whenever the review task exposes regulated data
  (e.g., PHI).

## 6. Legal and ethical considerations

| Category | What it covers | AWS mitigation |
|---|---|---|
| **Intellectual property (IP)** | Ownership/liability for AI-generated content; training-data copyright risk | Choose a Bedrock model whose provider offers **IP indemnification** — not a technical control like Guardrails |
| **Data privacy** | GDPR-style obligations; minimize/anonymize/consent; **data residency** | Guardrails sensitive information filters redact PII at inference; **Amazon Macie** classifies sensitive data at rest in S3 |
| **Toxicity** | Hateful, harassing, obscene, or otherwise harmful generated content | Guardrails content filters; careful prompt design; Amazon A2I human review |
| **Environmental impact** | Energy/compute/carbon footprint of training and running FMs | Reuse pretrained FMs (prompting/RAG/fine-tuning) instead of pretraining from scratch; **AWS Customer Carbon Footprint Tool**; **Well-Architected Sustainability Pillar** |

- Keep **toxicity** (harmful content), **data privacy** (personal data),
  and **IP** (ownership/liability) as three separate, non-overlapping
  categories — the exam tests them as distinct answers.
- **IP risk → IP indemnification**, never Guardrails (content
  safety/privacy, not copyright liability).

## 7. Monitoring checklist

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

---

## Rapid-fire key terms

- **Responsible AI** — designing, building, and operating AI systems that
  are fair, explainable, private/secure, transparent, veracious/robust,
  governed, safe, and controllable.
- **Bias (fairness sense)** — systematic, unfair skew in outcomes caused
  by training data/process; **not** the same as statistical bias/variance
  ([Domain 1](../domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off)).
- **SHAP (Shapley Additive exPlanations)** — feature-attribution values
  quantifying each input's contribution to one prediction; an
  *approximation*, not an exact decision trace.
- **Amazon SageMaker Model Cards** — structured documentation of intended
  use, training data, evaluation results, and limitations for a model you
  built.
- **AI Service Cards** — AWS-published documentation of an AWS-managed AI
  service's intended use and limitations.
- **Personally identifiable information (PII)** — data identifying a
  specific individual; a Guardrails sensitive-information-filter target.
- **Amazon Macie** — discovers and classifies sensitive data (including
  PII) stored in Amazon S3.
- **Intellectual property (IP) indemnification** — a contractual
  protection some Bedrock model providers offer, shifting IP-infringement
  legal risk away from the customer.
- **Data residency** — the geographic location where data is
  stored/processed.
- **AWS Customer Carbon Footprint Tool** — reports estimated carbon
  emissions from a customer's AWS usage.
- **Interpretability** — how easily a human can understand how a model
  arrives at its outputs; trades off against raw performance.
- **Black box model** — a model whose internal decision process isn't
  easily understood by humans (typically deep learning/foundation
  models).
- **SageMaker Model Monitor** — watches a deployed model/endpoint for
  bias drift, data drift, and performance drift over time.

For the complete 30+ term glossary with full definitions: [full guide, Key
terms glossary](../domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).

## Common exam traps checklist

- [ ] **Bias vs. variance** — bias is a fairness/training-data problem;
      variance is a model-sensitivity/overfitting problem from
      [Domain 1](../domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off).
      Don't conflate them.
- [ ] **Clarify measures bias both before *and* after training** — a
      *dataset* check pre-model is still a pre-training metric (DPL,
      class imbalance), not disparate impact.
- [ ] **Guardrails filters live inference content**; it does not detect
      training-data bias or generate explanations — that's Clarify's job.
- [ ] **Explainability ≠ transparency** — per-prediction vs. whole-system
      documentation.
- [ ] **A named proxy feature (ZIP code, a correlated ID number) usually
      signals measurement bias**, not a demographic label problem.
- [ ] **Two components (a structured/tabular model + a generative FM) need
      two tools** — Clarify on the structured model, Guardrails on the FM
      — never one tool for both, never one blended metric.
- [ ] **RAG bias has no labeled dataset for Clarify** — look for retrieval
      corpus curation, Guardrails grounding checks, and source citation
      instead.
- [ ] **SHAP is an approximation, not an exact decision trace** — a
      regulation requiring the *actual* decision logic disqualifies
      post-hoc SHAP on a black box; only a natively interpretable model
      satisfies it.
- [ ] **IP risk → IP indemnification**, not Guardrails (that's content
      safety/privacy, not copyright liability).
- [ ] **Model Card = self-authored** (a model you built); **AI Service
      Card = AWS-authored** (a service you're evaluating/adopting).
- [ ] **A confidence threshold for A2I routing is not the same as
      temperature** — temperature is a generative-model sampling
      parameter with no meaning for a classical classifier's predicted
      probability.

---

## Where each row comes from

| This cram sheet | Fast track section |
|---|---|
| 1. Dimensions of responsible AI | [Section 1](README.md#1-core-dimensions-of-responsible-ai) |
| 2. Common bias sources | [Section 2](README.md#2-bias-and-fairness) |
| 3. Fairness metrics by use case / stage | [Section 2](README.md#2-bias-and-fairness) |
| 4. Key trade-offs | [Section 5](README.md#5-performance-vs-interpretability) |
| 5. AWS tools for responsible AI | [Section 3](README.md#3-aws-tools-for-responsible-ai) |
| 6. Legal and ethical considerations | [Section 4](README.md#4-legal-and-ethical-considerations) |
| 7. Monitoring checklist | [Monitoring section](README.md#monitoring-responsible-ai-in-production) |
| Rapid-fire key terms | [Rapid-fire key terms](README.md#rapid-fire-key-terms) |
| Common exam traps checklist | [Common exam traps checklist](README.md#common-exam-traps-checklist) |

For the full tables, decision flowcharts, worked examples, and rapid
self-check this cram sheet intentionally omits, go back to the
[Domain 4 fast track](README.md) or the
[full Domain 4 guide](../domain-4-guidelines-for-responsible-ai.md). For
material spanning multiple domains, see
[`docs/cross-domain-concept-map.md`](../cross-domain-concept-map.md).

[← Back to the Domain 4 fast track](README.md) · [Full Domain 4 guide →](../domain-4-guidelines-for-responsible-ai.md)
