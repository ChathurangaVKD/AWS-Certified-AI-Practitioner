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
| [The ML development lifecycle](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle) — model training step | [Fine-tuning vs. continued pre-training vs. RAG vs. prompt engineering](domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering) | Fine-tuning and continued pre-training *are* the D1 "model training" lifecycle stage applied to a foundation model instead of a model trained from scratch — same stage, same risk of overfitting on a small custom dataset, new name. |
| [Types of learning](domain-1-fundamentals-of-ai-and-ml.md#3-types-of-learning) — supervised learning | [Fine-tuning vs. continued pre-training vs. RAG vs. prompt engineering](domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering) | Fine-tuning a foundation model on labeled prompt/response pairs is a direct application of **supervised learning** as defined in D1 — the exam expects you to recognize it as such rather than as some unrelated generative-AI-only technique. |
| [AWS managed AI/ML services](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview) — Amazon SageMaker as the general ML platform | [Amazon Bedrock features](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features) and [AWS infrastructure for generative AI workloads](domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads) | D1 introduces SageMaker as the umbrella platform for building models "anywhere on the AI/ML/DL spectrum." D3 is where that spectrum's generative-AI end lives: Bedrock is the fully managed foundation-model path, while SageMaker JumpStart and custom training are the build-it-yourself path — the same platform, applied to foundation models. |
| [Basic AI/ML/DL terminology](domain-1-fundamentals-of-ai-and-ml.md#1-basic-aimldl-terminology-and-concepts) — real-time, batch, asynchronous, and serverless inference | [AWS infrastructure for generative AI workloads](domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads) | The on-demand vs. provisioned-throughput decision for Bedrock inference is the generative-AI-specific version of the D1 inference-type decision (real-time vs. batch vs. serverless): both are trading latency and cost against traffic predictability. |

## Domain 1 → Domain 4: Guidelines for Responsible AI

| Domain 1 fundamental | Flows into (Domain 4) | Why the connection matters |
|---|---|---|
| [Overfitting, underfitting, and the bias–variance trade-off](domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off) | [Identifying bias and fairness issues in training data and model outputs](domain-4-guidelines-for-responsible-ai.md#2-identifying-bias-and-fairness-issues-in-training-data-and-model-outputs) | D4 explicitly warns not to conflate these: statistical **bias** (high-bias/underfitting) and **variance** (high-variance/overfitting) from D1 are properties of a model's fit; responsible-AI **bias** in D4 is a *systematic, unfair skew* toward or against a demographic group. Same word, two different exam concepts, and the exam tests the distinction directly. |
| [Model evaluation basics](domain-1-fundamentals-of-ai-and-ml.md#6-model-evaluation-basics) — accuracy as an incomplete signal | [Balancing model performance and interpretability](domain-4-guidelines-for-responsible-ai.md#5-balancing-model-performance-and-interpretability) | D1 teaches that accuracy alone can be misleading (e.g., 99% accuracy on imbalanced fraud data). D4 extends that same "don't trust a single number" lesson to model *architecture* choice: a highly accurate model can still be the wrong choice if it can't be explained to a regulator, and SHAP-based tools like SageMaker Clarify recover some of that missing signal. |
| [The ML development lifecycle](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle) — data collection and feature engineering | [Identifying bias and fairness issues in training data and model outputs](domain-4-guidelines-for-responsible-ai.md#2-identifying-bias-and-fairness-issues-in-training-data-and-model-outputs) | Nearly every bias category D4 defines (sampling, measurement, label, historical, exclusion, aggregation) originates in the D1 lifecycle's data-collection and feature-engineering stages — bias detection is a targeted check on the same pipeline steps D1 already introduces, not a separate pipeline. |
| [The ML development lifecycle](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle) — hyperparameter tuning / evaluation step | [AWS tools for responsible AI](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai) | Amazon SageMaker Clarify plugs directly into the D1 lifecycle's evaluation step — running pre-training bias metrics on the dataset and post-training bias metrics on model predictions, at exactly the point D1 says you measure model quality on held-out data. |

## Domain 1 → Domain 5: Security, Compliance, and Governance for AI Solutions

| Domain 1 fundamental | Flows into (Domain 5) | Why the connection matters |
|---|---|---|
| [The ML development lifecycle](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle) — data collection and feature engineering | [Source citation and data lineage](domain-5-security-compliance-governance.md#source-citation-and-data-lineage) and [Data encryption at rest and in transit](domain-5-security-compliance-governance.md#data-encryption-at-rest-and-in-transit) | The raw and prepared data D1 describes moving through S3, Data Wrangler, and Feature Store is exactly what D5 requires you to encrypt (at rest and in transit) and trace (via SageMaker ML Lineage Tracking) — the lifecycle stage is the same, D5 adds the security and audit requirements around it. |
| [The ML development lifecycle](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle) — deployment and monitoring steps | [AWS Config, AWS Audit Manager, and AWS CloudTrail for AI governance](domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance) | Once a D1 lifecycle model reaches a SageMaker endpoint, every invocation and configuration change becomes something D5's governance services must account for: CloudTrail logs who called the endpoint, Config tracks whether it stayed compliant (e.g., encrypted), and Audit Manager turns both into audit-ready evidence. |
| [Model evaluation basics](domain-1-fundamentals-of-ai-and-ml.md#6-model-evaluation-basics) — SageMaker Model Monitor tracking metrics for drift | [Data monitoring](domain-5-security-compliance-governance.md#data-monitoring) | D1 introduces SageMaker Model Monitor as the tool that watches evaluation metrics degrade in production. D5 places that same monitoring discipline inside a broader governance context alongside Amazon Macie (sensitive-data discovery) and CloudWatch/GuardDuty (operational and threat monitoring). |
| [AWS managed AI/ML services](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview) — Amazon SageMaker as a general-purpose platform | [AWS shared responsibility model applied to AI/ML services](domain-5-security-compliance-governance.md#5-aws-shared-responsibility-model-applied-to-aiml-services) | D5's shared-responsibility split hinges on *how managed* a service is — and the abstraction spectrum D5 walks through (Bedrock vs. SageMaker JumpStart vs. custom SageMaker training) is the same AI/ML services landscape D1 first introduces conceptually in its managed-services overview. |

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
