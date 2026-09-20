# Domain 4 Cheat Sheet: Guidelines for Responsible AI

**Interactive quick-scan cheat sheet** · companion to the [Fast Track guide](README.md) and the [Ultra Fast Track cram sheet](ULTRA-FAST-LEARN.md) · full guide: [`docs/domain-4-guidelines-for-responsible-ai.md`](../domain-4-guidelines-for-responsible-ai.md)

Built for a 2-3 minute skim right before the exam — jump straight to the
topic you're weakest on, expand only that section, and tick off the
self-check checklist at the end. Domain 4 is roughly **14%** of scored
questions. Every fact here already lives in the [Fast
Track](README.md) and [Ultra Fast Track](ULTRA-FAST-LEARN.md); this is a
reformat for scannability, not new content.

## Table of contents

- [1. Dimensions of responsible AI](#1-dimensions-of-responsible-ai)
- [2. Common bias sources](#2-common-bias-sources)
- [3. Fairness metrics by use case / stage](#3-fairness-metrics-by-use-case-stage)
- [4. Key trade-offs](#4-key-trade-offs)
- [5. AWS tools for responsible AI](#5-aws-tools-for-responsible-ai)
- [6. Monitoring checklist](#6-monitoring-checklist)
- [7. Legal and ethical considerations](#7-legal-and-ethical-considerations)
- [Commonly confused pairs](#commonly-confused-pairs)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Self-check checklist](#self-check-checklist)

---

### 1. Dimensions of responsible AI

<details>
<summary>8 dimensions · fairness, explainability, privacy, transparency, and 4 more — tap to expand</summary>

| Dimension | Key question | Primary AWS tool |
|---|---|---|
| **Fairness** | Equitable treatment across groups? | SageMaker Clarify (bias metrics) |
| **Explainability** | Why did the model produce *this* prediction? | SageMaker Clarify (SHAP) |
| **Privacy and security** | Is personal data / the model protected? | Guardrails (PII redaction); Amazon Macie |
| **Transparency** | Is the whole system documented? | SageMaker Model Cards / AI Service Cards |
| **Veracity and robustness** | Correct/reliable under adversarial input? | Guardrails (contextual grounding) |
| **Governance** | Policies/processes controlling the AI lifecycle? | Model Cards; ML lineage tracking |
| **Safety** | Avoids harmful generated content? | Guardrails (content filters) |
| **Controllability** | Can a human monitor/override/stop it? | Guardrails (denied topics); Amazon A2I |

- **Highest-tested four:** fairness, explainability, privacy and security, and transparency.
- One prediction → **explainability**; whole system documented → **transparency**; treats groups equitably → **fairness**; a human can step in → **controllability**.

</details>

### 2. Common bias sources

<details>
<summary>Sampling, measurement, label, historical, exclusion, aggregation, representativeness bias — tap to expand</summary>

| Bias type | One-line definition |
|---|---|
| **Sampling bias** | Training data doesn't represent the real-world population |
| **Measurement bias** | A **proxy feature** (e.g., ZIP code) correlates with a protected characteristic |
| **Label / human bias** | Annotators inject conscious/unconscious bias while labeling |
| **Historical bias** | Data accurately reflects a real world that is itself inequitable |
| **Exclusion bias** | Relevant data/features dropped, removing signal a group needs |
| **Aggregation bias** | One model applied uniformly to groups that need distinct treatment |
| **Representativeness bias** | A whole deployment segment is thin/absent from training data — **no group label exists**, so fairness metrics miss it |

- A named **proxy variable** in a scenario → measurement bias, fixed by dropping/transforming the feature.
- A clean fairness-metric report does **not** rule out representativeness bias.

</details>

### 3. Fairness metrics by use case / stage

<details>
<summary>DPL, class imbalance, disparate impact, accuracy/recall difference — tap to expand</summary>

| Question | Metric | Stage |
|---|---|---|
| Positive label rate differs across groups in the *dataset*? | **Difference in proportions of labels (DPL)** | Pre-training |
| A class/group is underrepresented in the dataset? | **Class imbalance** | Pre-training |
| A trained model's outcome rates differ across groups? | **Disparate impact** | Post-training |
| Accuracy/recall differs materially across groups? | **Accuracy/recall difference** | Post-training |

| Use case | Highest-value metric |
|---|---|
| Credit/loan approval | Disparate impact + DPL |
| Hiring/resume screening | DPL (dataset), disparate impact (predictions) |
| Healthcare triage/diagnosis | Accuracy/recall difference |
| RAG/generative assistant | No labeled dataset — audit **retrieval corpus** coverage |

- No model yet, checking labels → **DPL**/class imbalance. Predictions/deployed model → **disparate impact**/accuracy-recall difference.

</details>

### 4. Key trade-offs

<details>
<summary>Fairness vs. accuracy · explainability vs. latency (SHAP vs. natively interpretable) — tap to expand</summary>

| | Favor fairness | Favor accuracy |
|---|---|---|
| Typical fix | Pre/in/post-processing rebalancing | Leave the higher-accuracy model unconstrained |
| Favor when | High-stakes, regulated decisions | Low-stakes, no protected-group exposure |

| | Natively interpretable model | Post-hoc SHAP (Clarify) |
|---|---|---|
| Real-time / low-latency fit | Best fit — explanation is **free** | Often an offline/batch job |
| Reflects actual decision logic? | **Yes** | **No** — an approximation only |

- A regulation requiring the explanation reflect **actual decision logic** disqualifies post-hoc SHAP regardless of latency budget.

</details>

### 5. AWS tools for responsible AI

<details>
<summary>Clarify, Model Cards, AI Service Cards, Guardrails, A2I — tap to expand</summary>

| Tool | Detects / does | Applies to |
|---|---|---|
| **SageMaker Clarify** | Pre/post-training bias metrics + SHAP explainability | Datasets & trained models |
| **SageMaker Model Cards** | **Self-authored** documentation | Models you build |
| **AI Service Cards** | **AWS-authored** documentation | AWS-managed AI services |
| **Guardrails for Amazon Bedrock** | Runtime safety/privacy filtering | FM input/output at inference |
| **Amazon A2I** | Human-in-the-loop review routing | Low-confidence/high-stakes predictions |

**Guardrails — five capabilities:**

| Capability | Blocks / does |
|---|---|
| **Denied topics** | Blocks specified topics |
| **Content filters** | Blocks harmful categories |
| **Word filters** | Blocks specific words/phrases |
| **Sensitive information filters** | Detects/redacts **PII** |
| **Contextual grounding checks** | Verifies a response is grounded in source content |

- `StartHumanLoop` (**Amazon A2I**) routes low-confidence predictions to a human review workflow. **Private workforce** (Cognito) for regulated data; **Mechanical Turk** otherwise.

</details>

### 6. Monitoring checklist

<details>
<summary>Bias drift, confidence-threshold drift, runtime safety drift, coverage drift — tap to expand</summary>

- [ ] **Bias drift** — disparate impact / accuracy-recall difference tracked via SageMaker Model Monitor + Clarify.
- [ ] **Confidence-threshold drift** — rising share of predictions below an A2I routing threshold signals population drift.
- [ ] **Runtime content/safety drift** — Guardrails intervention logs reviewed over time.
- [ ] **Coverage/representativeness drift** — new regions/segments checked against training-data coverage.
- [ ] **Two-component systems** — a structured model and a paired FM each get their own **independent** monitoring stream.
- [ ] **Governance cadence** — recurring review of the Model Card against the latest Clarify/Model Monitor metrics.

</details>

### 7. Legal and ethical considerations

<details>
<summary>IP indemnification, data privacy, toxicity, environmental impact — tap to expand</summary>

| Category | What it covers | AWS mitigation |
|---|---|---|
| **Intellectual property (IP)** | Ownership/liability for AI-generated content | Choose a provider offering **IP indemnification** |
| **Data privacy** | GDPR, data residency, PII | Guardrails sensitive info filters; **Amazon Macie** |
| **Toxicity** | Hateful, harassing, obscene content | Guardrails content filters; A2I human review |
| **Environmental impact** | Energy/compute/carbon footprint | Reuse pretrained FMs; **AWS Customer Carbon Footprint Tool** |

- **IP risk → IP indemnification**, not Guardrails — keep toxicity, data privacy, and IP as three separate categories.

</details>

---

### Commonly confused pairs

<details>
<summary>6 pairs the exam loves to swap — tap to expand</summary>

| Pair | How to tell them apart |
|---|---|
| **Model Card** vs. **AI Service Card** | Model Card = **self-authored** (your model); AI Service Card = **AWS-authored** |
| **Bias** (Domain 4) vs. **Variance** (Domain 1) | Bias = fairness/training-data problem; Variance = model-sensitivity/overfitting problem |
| **SHAP** vs. **natively interpretable model** | SHAP = post-hoc **approximation**; natively interpretable = explanation **is** the decision logic |
| **DPL / class imbalance** vs. **disparate impact / accuracy-recall difference** | Former = **pre-training** (dataset); latter = **post-training** (predictions) |
| **Guardrails** vs. **SageMaker Clarify** | Guardrails filters live **inference** content; Clarify detects training-data **bias** and generates explanations |
| **Measurement bias** vs. **representativeness bias** | Measurement bias = a named **proxy feature**; representativeness bias = a whole segment **missing**, no group label to catch it |

</details>

### Rapid-fire key terms

<details>
<summary>6 key terms — tap to expand</summary>

| Term | Definition |
|---|---|
| **Responsible AI** | Fair, explainable, private/secure, transparent, veracious/robust, governed, safe, and controllable AI |
| **SHAP** | Feature-attribution values quantifying one prediction; an approximation, not an exact trace |
| **PII** | Personally identifiable information; a Guardrails sensitive-information-filter target |
| **IP indemnification** | A contractual protection shifting IP-infringement legal risk from the customer |
| **AWS Customer Carbon Footprint Tool** | Reports estimated carbon emissions from a customer's AWS usage |
| **Amazon Macie** | Discovers/classifies sensitive data (incl. PII) stored in Amazon S3 |

</details>

---

## Self-check checklist

Tick each fact you can already state cold — anything unchecked is what to
re-read in the [Fast Track](README.md) or [Ultra Fast
Track](ULTRA-FAST-LEARN.md) before the exam.

- [ ] **Bias vs. variance** — fairness/training-data problem vs. model-sensitivity/overfitting problem (Domain 1). Don't conflate.
- [ ] **Guardrails filters live inference content**; it doesn't detect training-data bias or generate explanations — that's Clarify's job.
- [ ] **Representativeness gaps evade standard fairness metrics** — a clean Clarify report doesn't rule out a thin/absent segment.
- [ ] **Two components (tabular model + generative FM) need two tools** — Clarify on the tabular model, Guardrails on the FM — never blended.
- [ ] **SHAP is an approximation, not an exact decision trace** — only a natively interpretable model satisfies an actual-decision-logic requirement.
- [ ] **Model Card = self-authored; AI Service Card = AWS-authored.**

---

For the full explanations, worked examples, mini-quizzes, and practice
questions this cheat sheet intentionally omits, go back to the [Domain 4
fast track](README.md), the [Ultra Fast Track](ULTRA-FAST-LEARN.md), or
the [full Domain 4 guide](../domain-4-guidelines-for-responsible-ai.md).

[← Back to the Domain 4 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md)
