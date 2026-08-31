# Cross-Domain Concept Map: From Domain 1 Fundamentals to Domains 3–5

The five domain guides in this series are written to stand alone — each one
covers its own exam task statements in full. But the AIF-C01 exam does not
test domains in isolation, and neither does real-world practice: the
vocabulary and mental models built in
[**Domain 1: Fundamentals of AI and ML**](domain-1-fundamentals-of-ai-and-ml.md)
(how a model is trained, how you measure whether it's any good, why it
fails) are the exact same concepts that reappear — renamed, specialized, or
extended — once you get to foundation models, responsible AI, and
governance.

This page is a map, not a new topic: every row links back to material that
is already covered in depth in its home domain document. Use it when a
Domain 3–5 guide says "recall from Domain 1..." and you want the direct
link, or when you want to see at a glance how the fundamentals you just
studied in Domain 1 pay off three domains later.

> **How to read this map:** each entry names a Domain 1 concept, the
> downstream concept it flows into, and *why* the connection exists — not
> just that the two topics share a word. Follow the links to jump straight
> to the relevant section in either document.

---

## At a glance

- Model evaluation metrics (D1) → FM performance evaluation (D3)
- ML lifecycle: training/fine-tuning step (D1) → fine-tuning vs. RAG vs. prompt engineering (D3)
- Types of learning: supervised learning (D1) → fine-tuning as supervised adaptation (D3)
- AWS managed AI/ML services: Amazon SageMaker (D1) → Bedrock vs. SageMaker infrastructure choices (D3)
- Inference types: real-time/batch/serverless (D1) → on-demand vs. provisioned throughput (D3)
- Bias–variance trade-off (D1) → bias detection and fairness (D4)
- Model evaluation vs. interpretability (D1) → balancing performance and interpretability (D4)
- ML lifecycle: data collection/preparation (D1) → sources of bias in training data (D4)
- ML lifecycle: hyperparameter tuning/evaluation (D1) → AWS tools for responsible AI (D4)
- ML lifecycle: deployment/monitoring (D1) → governance and audit services (D5)
- ML lifecycle: data collection/preparation (D1) → data lineage, encryption, and residency (D5)
- AWS managed AI/ML services: Amazon SageMaker (D1) → shared responsibility model (D5)
- Model monitoring for drift (D1) → data governance and monitoring strategies (D5)

---

## Domain 1 → Domain 3: Applications of Foundation Models

| Domain 1 fundamental | Flows into (Domain 3) | Why the connection matters |
|---|---|---|
| [Model evaluation basics](domain-1-fundamentals-of-ai-and-ml.md#6-model-evaluation-basics) — accuracy, precision, recall, F1, AUC-ROC | [Evaluating foundation model performance](domain-3-applications-of-foundation-models.md#7-evaluating-foundation-model-performance) | FM evaluation doesn't replace classical model evaluation, it builds on it: **benchmark datasets** score an FM with the same objective, automatable mindset as D1's classification metrics, before layering on human evaluation and business metrics that D1 doesn't need for a simple classifier. |
## Commonly confused concept pairs (quick reference)

The concepts above don't just *relate* across domains — a handful of them
share a name, an acronym, or a superficial similarity with a completely
different concept in another domain, and the exam exploits exactly that
overlap. This table is a single side-by-side lookup for the pairs that
learners most often mix up, pulled from across all five domain guides. Use
it as a last-minute review pass right before the exam.

| Term A vs. Term B | One-line distinction | Source sections |
|---|---|---|
| Statistical bias (bias–variance trade-off) vs. fairness bias | Statistical bias is a *model-fit* property — systematic underfitting error measured against ground truth; fairness bias is a *systematic, unfair skew* in a model's outputs toward or against a demographic group. Same word, two different exam concepts. | [Domain 1 §7](domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off), [Domain 4 §2](domain-4-guidelines-for-responsible-ai.md#2-identifying-bias-and-fairness-issues-in-training-data-and-model-outputs) |
| Precision vs. recall | Precision = of everything flagged positive, what fraction was actually positive (few false alarms); recall = of everything actually positive, what fraction was caught (few missed cases). Prioritize precision when false positives are costly, recall when false negatives are costly. | [Domain 1 §6](domain-1-fundamentals-of-ai-and-ml.md#6-model-evaluation-basics) |
| Fine-tuning vs. continued pre-training | Fine-tuning adapts a foundation model on a smaller set of *labeled* task-specific prompt/response pairs (supervised learning); continued pre-training further trains it on a large corpus of *unlabeled* domain data (e.g., legal or medical text) to adapt vocabulary before any task-specific fine-tuning happens. | [Domain 1 §2](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle), [Domain 3 §4](domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering) |
| CloudTrail vs. Config vs. Audit Manager | CloudTrail logs *who did what, and when* (API call/event history); AWS Config tracks *whether a resource's configuration stays compliant* with a rule over time; Audit Manager continuously collects evidence from both (and more) into audit-ready reports. | [Domain 5 §3](domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance) |
| Model Cards vs. AI Service Cards | A SageMaker Model Card documents a model *your organization built* — intended use, training data, evaluation results, known limitations; an AI Service Card is AWS-published documentation describing an *AWS-managed AI service* (e.g., Rekognition, Transcribe) that you consume as-is. | [Domain 4 §3](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai) |
| On-demand vs. provisioned throughput | On-demand is pay-per-token pricing with no commitment — fits variable, spiky, or low-volume traffic; provisioned throughput is a flat-rate, dedicated-capacity commitment (1- or 6-month) — required for most custom/fine-tuned models and needed when traffic is high, steady, and predictable. | [Domain 2 §2](domain-2-fundamentals-of-generative-ai.md#2-llm-lifecycle-basics), [Domain 3 §5](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features) |
| Real-time vs. batch vs. serverless inference | Real-time inference is a low-latency, persistent endpoint for a live request; batch inference scores a large volume offline with no one waiting on an individual result; serverless inference auto-scales to zero and suits intermittent, unpredictable traffic. | [Domain 1 §1](domain-1-fundamentals-of-ai-and-ml.md#1-basic-aimldl-terminology-and-concepts), [Domain 3 §8](domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads) |

---

## Why this matters for the exam

AIF-C01 scenario questions frequently combine concepts across domains in a
single item — for example, a question about **fine-tuning a foundation
model on customer data** can simultaneously test D1 (is this
supervised learning? will it overfit on a small dataset?), D3 (is
fine-tuning the right customization option compared to RAG?), D4 (does the
training data introduce bias?), and D5 (is the training data encrypted, and
who is responsible for securing it?). Studying each domain guide in
isolation covers the vocabulary; this map is meant to help you practice
recognizing when a single scenario is really asking about more than one
domain at once.