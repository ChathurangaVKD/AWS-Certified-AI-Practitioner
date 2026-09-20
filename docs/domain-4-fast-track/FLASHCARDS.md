# Domain 4 Flashcards: Guidelines for Responsible AI

**Spaced-repetition companion deck** · fast track: [`README.md`](README.md) · cram sheet: [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · plain-text import file: [`flashcards.tsv`](flashcards.tsv)

One card per testable concept from the Domain 4 Flashcards: Guidelines for Responsible AI Ultra Fast Track cram sheet, ordered to match that file's own section order so studying this deck reinforces the domain's structure. Front/back only, no prose -- for active recall or spaced repetition. `flashcards.tsv` holds the identical cards as a header-less, two-column (front, back) tab-separated file, importable as-is into Anki or Quizlet.

## 1. Dimensions of responsible AI

| Front | Back |
|---|---|
| Responsible AI dimension: equitable treatment across groups/protected characteristics? | Fairness -- SageMaker Clarify (bias metrics) |
| Responsible AI dimension: why did the model produce this prediction? | Explainability -- SageMaker Clarify (SHAP) |
| Responsible AI dimension: is personal data protected; is the model protected from misuse? | Privacy and security -- Guardrails (PII redaction); Amazon Macie |
| Responsible AI dimension: is the whole system's build/training/limits documented? | Transparency -- SageMaker Model Cards / AI Service Cards |
| Responsible AI dimension: correct and reliable, even under noisy/adversarial input? | Veracity and robustness -- Guardrails (contextual grounding) |
| Responsible AI dimension: policies/processes controlling the AI lifecycle? | Governance -- Model Cards; ML lineage tracking |
| Responsible AI dimension: avoids harmful/dangerous generated content? | Safety -- Guardrails (content filters) |
| Responsible AI dimension: can a human monitor, override, or stop it? | Controllability -- Guardrails (denied topics); Amazon A2I |
| Which four responsible-AI dimensions drive most exam scenario questions? | Fairness, explainability, privacy and security, and transparency |
| Scenario: explain why the model produced one specific prediction | Explainability |
| Scenario: the whole system is documented end to end | Transparency |
| Scenario: groups are treated equitably | Fairness |
| Scenario: a human can step in and override or stop the system | Controllability |

## 2. Common bias sources

| Front | Back |
|---|---|
| Bias type: training data doesn't represent the real-world population | Sampling bias |
| Bias type: a proxy feature (e.g., ZIP code) correlates with a protected characteristic more than the real outcome | Measurement bias |
| Bias type: annotators inject conscious/unconscious bias while labeling | Label / human bias |
| Bias type: data accurately reflects a real world that is itself inequitable | Historical bias |
| Bias type: relevant data/features dropped, removing signal a group needs | Exclusion bias |
| Bias type: one model applied uniformly to groups that need distinct treatment | Aggregation bias |
| Bias type: a whole deployment segment is thin/absent from training data, with no group label | Representativeness bias |
| Trap: a named proxy variable in a scenario | Measurement bias -- fixed by dropping/transforming the feature, not by rebalancing classes |
| Trap: does a clean fairness-metric report rule out representativeness bias? | No -- check per-segment coverage and accuracy separately |

## 3. Fairness metrics by use case / stage

| Front | Back |
|---|---|
| Fairness metric: positive label rate differs across groups in the dataset | Difference in proportions of labels (DPL) -- pre-training, Clarify dataset job |
| Fairness metric: a class/group is underrepresented in the dataset | Class imbalance -- pre-training, Clarify dataset job |
| Fairness metric: a trained model's outcome rates differ across groups | Disparate impact -- post-training, Clarify model job |
| Fairness metric: accuracy/recall differs materially across groups | Accuracy/recall difference -- post-training, Clarify model job |
| Highest-value fairness metric for credit/loan approval | Disparate impact + DPL (pre- and post-training) |
| Highest-value fairness metric for hiring/resume screening | DPL (dataset), disparate impact (predictions) |
| Highest-value fairness metric for healthcare triage/diagnosis | Accuracy/recall difference across demographic groups |
| Highest-value fairness metric for content moderation | Class imbalance (dataset), accuracy difference (predictions) |
| Highest-value fairness check for a RAG/generative assistant | No labeled dataset -- audit retrieval corpus coverage instead |
| If-then: checking labels with no model yet, vs. predictions from a deployed model | No model yet -> DPL/class imbalance; predictions/deployed model -> disparate impact/accuracy-recall difference |

## 4. Key trade-offs

| Front | Back |
|---|---|
| Fairness-vs-accuracy trade-off: typical fix to favor fairness | Pre-processing rebalance, in-processing fairness constraints, post-processing threshold calibration |
| Fairness-vs-accuracy trade-off: typical approach to favor accuracy | Leave the higher-accuracy model/objective unconstrained |
| When should you favor fairness over accuracy? | High-stakes, regulated decisions (credit, hiring, healthcare) |
| When should you favor accuracy over fairness? | Low-stakes tasks with no protected-group exposure |
| Explainability-vs-latency: added inference-time compute for a natively interpretable model | None -- the model's logic is the explanation |
| Explainability-vs-latency: added inference-time compute for post-hoc SHAP | Extra computation per explanation (Shapley value estimation); often run offline/batch |
| Which approach best fits real-time / low-latency explainability needs? | A natively interpretable model -- explanation is free |
| Does post-hoc SHAP reflect the model's actual decision logic? | No -- it is an approximation only; a natively interpretable model does reflect actual logic |
| Trap: a scenario needs an explanation AND strict real-time latency | Pushes toward a natively interpretable model, not synchronous post-hoc SHAP |
| Trap: a regulation requires the explanation reflect actual decision logic | Disqualifies post-hoc SHAP regardless of latency budget |

## 5. AWS tools for responsible AI

| Front | Back |
|---|---|
| AWS tool: bias detection (pre-/post-training) + SHAP explainability | Amazon SageMaker Clarify -- applies to datasets and trained models |
| AWS tool: structured documentation of a model you built | SageMaker Model Cards |
| AWS tool: AWS-published documentation of an AWS-managed AI service | AI Service Cards |
| AWS tool: runtime safety/privacy filtering of FM inputs/outputs | Guardrails for Amazon Bedrock |
| AWS tool: human-in-the-loop review of low-confidence/high-stakes predictions | Amazon A2I |
| Model Card vs. AI Service Card | Model Card = you fill it in (a model you built); AI Service Card = AWS publishes it, you read it (an AWS-managed service) |
| Guardrails capability: blocks the model from engaging with specified topics | Denied topics |
| Guardrails capability: blocks harmful categories (hate, insults, sexual, violence, misconduct, prompt attacks) | Content filters |
| Guardrails capability: blocks specific words/phrases (profanity, competitor names) | Word filters |
| Guardrails capability: detects/redacts/blocks PII in prompts and responses | Sensitive information filters |
| Guardrails capability: verifies a response is grounded in source content, reducing hallucination | Contextual grounding checks |
| A2I: what happens when a prediction falls below the routing confidence threshold? | It invokes StartHumanLoop instead of an automated action |
| A2I: what wires the activation condition, and must match the routing threshold? | The flow definition |
| A2I: what defines the reviewer-facing review UI? | The worker task template |
| A2I: when is a private workforce (via Amazon Cognito) required instead of Mechanical Turk? | Whenever the review task exposes regulated data (e.g., PHI) |
| SageMaker Clarify: pre-training bias metrics | Class imbalance, difference in proportions of labels (DPL) -- computed on the raw dataset |
| SageMaker Clarify: post-training bias metrics | Disparate impact, accuracy/recall difference -- computed on a trained model's predictions |
| SageMaker Clarify: SHAP-based explainability | Per-prediction feature-attribution values for a trained model -- an approximation, not an exact trace |
| SageMaker Clarify: bias reports | Generated artifacts summarizing metric results, attachable to a SageMaker Model Card |
| SageMaker Clarify: integration with SageMaker Model Monitor | Feeds ongoing bias-drift monitoring on a deployed endpoint |
| What does SageMaker Clarify NOT apply to? | Live foundation-model input/output at inference -- that's Guardrails' job |

## 6. Legal and ethical considerations

| Front | Back |
|---|---|
| Legal/ethical category: ownership of AI-generated content; liability for content resembling copyrighted training material | Intellectual property (IP) -- choose a Bedrock provider offering IP indemnification |
| Legal/ethical category: GDPR, data residency, minimizing/anonymizing personal data | Data privacy -- Guardrails sensitive information filters (PII redaction); Amazon Macie |
| Legal/ethical category: hateful, harassing, obscene, or otherwise harmful generated content | Toxicity -- Guardrails content filters; Amazon A2I human review |
| Legal/ethical category: energy/compute/carbon footprint of training and running FMs | Environmental impact -- reuse pretrained FMs; AWS Customer Carbon Footprint Tool; Well-Architected Sustainability Pillar |
| Trap: IP risk mitigation | IP indemnification, not Guardrails (which covers content safety/privacy, not copyright liability) -- keep toxicity, data privacy, and IP separate |

## 7. Monitoring checklist

| Front | Back |
|---|---|
| Monitoring item: bias drift | Disparate impact / accuracy-recall difference tracked over time via SageMaker Model Monitor + Clarify |
| Monitoring item: confidence-threshold drift | A rising share of predictions below an Amazon A2I routing threshold signals population drift |
| Monitoring item: runtime content/safety drift | Guardrails intervention logs (blocked topics, filtered content, redacted PII) reviewed over time |
| Monitoring item: coverage/representativeness drift | New regions/segments in production traffic checked against training-data coverage |
| Monitoring item: two-component systems | A structured model and a paired FM each get their own independent monitoring stream, never one blended metric |
| Monitoring item: governance cadence | Recurring (e.g., quarterly) review of the SageMaker Model Card against the latest Clarify/Model Monitor metrics; high-risk flags route through Amazon A2I |

## Rapid-fire key terms

| Front | Back |
|---|---|
| Responsible AI | Fair, explainable, private/secure, transparent, veracious/robust, governed, safe, and controllable AI systems |
| SHAP | Feature-attribution values quantifying one prediction; an approximation, not an exact decision trace |
| PII | Personally identifiable information; a Guardrails sensitive-information-filter target |
| IP indemnification | A contractual protection shifting IP-infringement legal risk away from the customer |
| AWS Customer Carbon Footprint Tool | Reports estimated carbon emissions from a customer's AWS usage |
| Amazon Macie | Discovers/classifies sensitive data (incl. PII) stored in Amazon S3 |

## Common exam traps

| Front | Back |
|---|---|
| Trap: bias vs. variance | Bias (fairness/training-data problem) vs. variance (model-sensitivity/overfitting problem, Domain 1) -- don't conflate them |
| Trap: what does Guardrails filter, and what doesn't it do? | Guardrails filters live inference content; it doesn't detect training-data bias or generate explanations -- that's Clarify's job |
| Trap: do representativeness gaps show up in standard fairness metrics? | No -- a clean Clarify report doesn't rule out a thin/absent segment |
| Trap: a system with a tabular model plus a generative FM | Needs two tools -- Clarify on the tabular model, Guardrails on the FM -- never blended |
| Trap: is SHAP an exact decision trace? | No -- it's an approximation; only a natively interpretable model satisfies an actual-decision-logic requirement |
| Trap: Model Card vs. AI Service Card authorship | Model Card = self-authored; AI Service Card = AWS-authored |

---

**86 cards total.** For the full explanations behind any card, see the [fast track](README.md), the [Ultra Fast Track cram sheet](ULTRA-FAST-LEARN.md), or the [full Domain 4 guide](../domain-4-guidelines-for-responsible-ai.md).

[← Back to the Domain 4 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md)
