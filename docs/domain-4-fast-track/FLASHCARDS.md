# Domain 4 Flashcards: Guidelines for Responsible AI

**Flashcard deck** · fast track: [`README.md`](README.md) · ultra fast
learn: [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · full guide:
[`docs/domain-4-guidelines-for-responsible-ai.md`](../domain-4-guidelines-for-responsible-ai.md)

One card per testable concept — front/back only, no prose. A reformat of
this domain's already-verified [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md)
content into active-recall/spaced-repetition format; it introduces no new
facts. Cards are ordered to match `ULTRA-FAST-LEARN.md`'s own section
order, so working through the deck top to bottom reinforces the domain's
structure. For app-based spaced repetition (Anki, Quizlet, etc.), import
[`flashcards.tsv`](flashcards.tsv) — the same 78 cards, same order, no
header row, tab-separated `front\tback`.

## 1. Dimensions of responsible AI

| Front | Back |
|---|---|
| Fairness — key question & primary AWS tool? | Equitable treatment across groups/protected characteristics?; SageMaker Clarify (bias metrics). |
| Explainability — key question & primary AWS tool? | Why did the model produce *this* prediction?; SageMaker Clarify (SHAP). |
| Privacy and security — key question & primary AWS tool? | Is personal data protected; is the model protected from misuse?; Guardrails (PII redaction); Amazon Macie. |
| Transparency — key question & primary AWS tool? | Is the whole system's build/training/limits documented?; SageMaker Model Cards / AI Service Cards. |
| Veracity and robustness — key question & primary AWS tool? | Correct and reliable, even under noisy/adversarial input?; Guardrails (contextual grounding). |
| Governance — key question & primary AWS tool? | Policies/processes controlling the AI lifecycle?; Model Cards; ML lineage tracking. |
| Safety — key question & primary AWS tool? | Avoids harmful/dangerous generated content?; Guardrails (content filters). |
| Controllability — key question & primary AWS tool? | Can a human monitor, override, or stop it?; Guardrails (denied topics); Amazon A2I. |
| Which four dimensions of responsible AI drive most scenario questions? | Fairness, explainability, privacy and security, and transparency (the other four — veracity/robustness, governance, safety, controllability — round out the full 8-dimension model). |
| Scenario: explaining one prediction → which dimension? | Explainability. |
| Scenario: whole system's build/training/limits documented → which dimension? | Transparency. |
| Scenario: treats groups equitably → which dimension? | Fairness. |
| Scenario: a human can step in → which dimension? | Controllability. |

## 2. Common bias sources

| Front | Back |
|---|---|
| Sampling bias — definition? | Training data doesn't represent the real-world population. |
| Measurement bias — definition? | A proxy feature (e.g., ZIP code) correlates with a protected characteristic more than the real outcome. |
| Label / human bias — definition? | Annotators inject conscious/unconscious bias while labeling. |
| Historical bias — definition? | Data accurately reflects a real world that is itself inequitable. |
| Exclusion bias — definition? | Relevant data/features dropped, removing signal a group needs. |
| Aggregation bias — definition? | One model applied uniformly to groups that need distinct treatment. |
| Representativeness bias — definition? | A whole deployment segment (region/market) is thin/absent from training data — no group label exists, so standard fairness metrics miss it. |
| Scenario: a named proxy variable in a scenario → which bias, and correct fix? | Measurement bias, fixed by dropping/transforming the feature, not by rebalancing classes. |

## 3. Fairness metrics by use case / stage

| Front | Back |
|---|---|
| Positive label rate differs across groups in the *dataset* → metric, stage, computed by? | Difference in proportions of labels (DPL); pre-training; Clarify — dataset job. |
| A class/group is underrepresented in the dataset → metric, stage, computed by? | Class imbalance; pre-training; Clarify — dataset job. |
| A trained model's outcome rates differ across groups → metric, stage, computed by? | Disparate impact; post-training; Clarify — model job. |
| Accuracy/recall differs materially across groups → metric, stage, computed by? | Accuracy/recall difference; post-training; Clarify — model job. |
| Credit/loan approval — highest-value fairness metric? | Disparate impact + DPL (pre- and post-training). |
| Hiring/resume screening — highest-value fairness metric? | DPL (dataset), disparate impact (predictions). |
| Healthcare triage/diagnosis — highest-value fairness metric? | Accuracy/recall difference across demographic groups. |
| Content moderation — highest-value fairness metric? | Class imbalance (dataset), accuracy difference (predictions). |
| RAG/generative assistant — highest-value fairness metric? | No labeled dataset — audit the retrieval corpus coverage instead. |

## 4. Key trade-offs

| Front | Back |
|---|---|
| Fairness vs. accuracy — typical fix for each side? | Favor fairness: pre-processing rebalance, in-processing fairness constraints, post-processing threshold calibration. Favor accuracy: leave the higher-accuracy model/objective unconstrained. |
| Fairness vs. accuracy — cost of each choice? | Favor fairness: accuracy can drop when a constraint forces equalized outcomes across groups. Favor accuracy: risk of disparate impact on a protected group. |
| Fairness vs. accuracy — when to favor each? | Favor fairness: high-stakes, regulated decisions (credit, hiring, healthcare). Favor accuracy: low-stakes tasks with no protected-group exposure. |
| Explainability vs. latency — added inference-time compute: natively interpretable model vs. post-hoc SHAP? | Natively interpretable: none — the model's logic *is* the explanation. Post-hoc SHAP (SageMaker Clarify): extra computation per explanation (Shapley value estimation). |
| Explainability vs. latency — real-time/low-latency fit: natively interpretable model vs. post-hoc SHAP? | Natively interpretable: best fit — explanation is free. Post-hoc SHAP: often run as an offline/batch job, not synchronously per request. |
| Explainability vs. latency — accuracy tendency: natively interpretable model vs. post-hoc SHAP? | Natively interpretable: often lower on complex tasks. Post-hoc SHAP: often higher — no interpretability constraint on the model. |
| Explainability vs. latency — reflects actual decision logic: natively interpretable model vs. post-hoc SHAP? | Natively interpretable: yes. Post-hoc SHAP: no — an approximation only. |
| Scenario: needs an explanation AND strict real-time latency → which approach? | A natively interpretable model, not synchronous post-hoc SHAP. |
| A regulation requiring the explanation reflect actual decision logic disqualifies what? | Post-hoc SHAP, regardless of latency budget. |

## 5. AWS tools for responsible AI

| Front | Back |
|---|---|
| Amazon SageMaker Clarify — primary use case & applies to? | Bias detection (pre-/post-training) + SHAP explainability; applies to datasets and trained models. |
| SageMaker Model Cards — primary use case & applies to? | Structured documentation of a model *you* built; applies to models you build. |
| AI Service Cards — primary use case & applies to? | AWS-published documentation of an AWS-managed AI service; applies to AWS-managed AI services. |
| Guardrails for Amazon Bedrock — primary use case & applies to? | Runtime safety/privacy filtering; applies to FM inputs/outputs at inference. |
| Amazon A2I — primary use case & applies to? | Human-in-the-loop review of low-confidence/high-stakes predictions; applies to ML/AWS AI service predictions. |
| Guardrails — Denied topics capability? | Blocks the model from engaging with specified topics. |
| Guardrails — Content filters capability? | Blocks harmful categories (hate, insults, sexual, violence, misconduct, prompt attacks). |
| Guardrails — Word filters capability? | Blocks specific words/phrases (profanity, competitor names). |
| Guardrails — Sensitive information filters capability? | Detects/redacts/blocks PII in prompts and responses. |
| Guardrails — Contextual grounding checks capability? | Verifies a response is grounded in source content, reducing hallucination. |
| A2I — what triggers StartHumanLoop, and what wires the activation condition? | A prediction below the routing confidence threshold invokes StartHumanLoop instead of an automated action; the flow definition wires the activation condition and must use the same threshold as the routing logic so the two never drift apart. |
| A2I — worker task template vs. private workforce requirement? | The worker task template defines the reviewer-facing review UI; a private workforce (via Amazon Cognito) is required whenever the review task exposes regulated data (e.g., PHI) — public Mechanical Turk is not. |
| SageMaker Clarify — pre-training vs. post-training bias metrics? | Pre-training: class imbalance, difference in proportions of labels (DPL), computed on the raw dataset. Post-training: disparate impact, accuracy/recall difference, computed on a trained model's predictions. |
| SageMaker Clarify — SHAP-based explainability? | Per-prediction feature-attribution values for a trained model (an approximation, not an exact trace). |
| SageMaker Clarify — bias reports & Model Monitor integration? | Bias reports are generated artifacts summarizing metric results, attachable to a SageMaker Model Card; Clarify integrates with SageMaker Model Monitor to feed ongoing bias-drift monitoring on a deployed endpoint. |
| SageMaker Clarify — applies to what, not what? | Datasets and trained models (typically SageMaker) — not live foundation-model input/output (that's Guardrails' job). |

## 6. Legal and ethical considerations

| Front | Back |
|---|---|
| Intellectual property (IP) — what it covers & AWS mitigation? | Ownership of AI-generated content; liability for content resembling copyrighted training material — mitigated by choosing a Bedrock provider offering IP indemnification. |
| Data privacy — what it covers & AWS mitigation? | GDPR, data residency, minimizing/anonymizing personal data — mitigated by Guardrails sensitive information filters (PII redaction); Amazon Macie. |
| Toxicity — what it covers & AWS mitigation? | Hateful, harassing, obscene, or otherwise harmful generated content — mitigated by Guardrails content filters; Amazon A2I human review. |
| Environmental impact — what it covers & AWS mitigation? | Energy/compute/carbon footprint of training and running FMs — mitigated by reusing pretrained FMs (prompting/RAG/fine-tuning); AWS Customer Carbon Footprint Tool; Well-Architected Sustainability Pillar. |
| IP risk — mitigated by what, and why not Guardrails? | IP indemnification — Guardrails covers content safety/privacy, not copyright liability; toxicity, data privacy, and IP stay three separate, non-overlapping categories. |

## 7. Monitoring checklist

| Front | Back |
|---|---|
| Bias drift — what's tracked & how? | Disparate impact / accuracy-recall difference tracked over time via SageMaker Model Monitor + Clarify. |
| Confidence-threshold drift — what signals it? | A rising share of predictions below an Amazon A2I routing threshold signals population drift. |
| Runtime content/safety drift — what's reviewed? | Guardrails intervention logs (blocked topics, filtered content, redacted PII) reviewed over time. |
| Coverage/representativeness drift — what's checked? | New regions/segments in production traffic checked against training-data coverage. |
| Two-component systems — monitoring rule? | A structured model and a paired FM each get their own independent monitoring stream, never one blended metric. |
| Governance cadence — what's the recurring review? | A recurring (e.g. quarterly) review of the SageMaker Model Card against the latest Clarify/Model Monitor metrics; high-risk flags route through Amazon A2I. |

## Rapid-fire key terms

| Front | Back |
|---|---|
| Responsible AI — definition? | Fair, explainable, private/secure, transparent, veracious/robust, governed, safe, and controllable AI systems. |
| SHAP — definition? | Feature-attribution values quantifying one prediction; an approximation, not an exact decision trace. |
| PII — definition? | Personally identifiable information; a Guardrails sensitive-information-filter target. |
| IP indemnification — definition? | A contractual protection shifting IP-infringement legal risk away from the customer. |
| AWS Customer Carbon Footprint Tool — definition? | Reports estimated carbon emissions from a customer's AWS usage. |
| Amazon Macie — definition? | Discovers/classifies sensitive data (incl. PII) stored in Amazon S3. |

## Commonly confused pairs & numeric traps

| Front | Back |
|---|---|
| Confused pair: bias (fairness) vs. variance? | Fairness/training-data problem (bias, Domain 4) vs. model-sensitivity/overfitting problem (variance, Domain 1) — don't conflate. |
| Confused pair: Guardrails vs. Clarify? | Guardrails filters live inference content; it doesn't detect training-data bias or generate explanations — that's Clarify's job. |
| Confused pair: clean Clarify report vs. representativeness bias? | Representativeness gaps evade standard fairness metrics — a clean Clarify report doesn't rule out a thin/absent segment. |
| Confused pair: two-component systems — which tool for which component? | Tabular model + generative FM need two tools — Clarify on the tabular model, Guardrails on the FM — never blended. |
| Confused pair: SHAP vs. an actual decision trace? | SHAP is an approximation, not an exact decision trace — only a natively interpretable model satisfies an actual-decision-logic requirement. |
| Confused pair: Model Card vs. AI Service Card? | Model Card = self-authored (a model you built); AI Service Card = AWS-authored (an AWS-managed service). |

---

[← Back to the Domain 4 fast track](README.md) · [Ultra Fast Learn →](ULTRA-FAST-LEARN.md) · [Interactive cheat sheet →](CHEAT-SHEET.md)
