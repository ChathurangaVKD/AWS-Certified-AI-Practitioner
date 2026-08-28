# Cross-Domain Glossary

Every domain guide in this series ends with its own **Key terms** section, scoped to that guide's material. This page merges all of them into one alphabetical, series-wide glossary so you can look up a term without knowing (or guessing) which domain defines it.

Each entry gives a one-line working definition plus a backlink — or, for terms that show up in more than one domain, several backlinks — to the "Key terms" section where the concept is explained in full, with surrounding context and examples.

See also the [cross-domain concept map](cross-domain-concept-map.md) for how Domain 1 fundamentals flow into Domains 3–5, rather than just which terms they share. For the same term set as a compact index with `[D1, D3]`-style domain tags per term, see [`master-glossary.md`](master-glossary.md). For an index organized by AWS service instead of by term -- e.g. every mention of Amazon SageMaker or Amazon Bedrock across all five guides -- see [`aws-service-index.md`](aws-service-index.md).

## Jump to a letter

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [Z](#z)

---

## A

- **Accuracy** [D1] — proportion of all predictions that were correct. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Action group (Bedrock Agents)** [D3] — a defined set of APIs (typically backed by AWS Lambda) that a Bedrock Agent can invoke to take actions. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **AI (Artificial Intelligence)** [D1] — broad field of systems performing tasks that normally require human intelligence. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **AI Service Cards** [D4] — AWS-published documentation describing intended use, limitations, and design considerations of an AWS AI service. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Algorithm** [D1] — the method used to train a model (e.g., XGBoost, k-means). *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Algorithmic Accountability Act** [D5] — Proposed US legislation that would require impact assessments for automated decision systems. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms-glossary).)*
- **Amazon Augmented AI (Amazon A2I)** [D4] — a service for building human-in-the-loop review workflows for ML predictions. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Amazon Bedrock** [D2] — fully managed service offering a choice of foundation models via a single API. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Amazon Bedrock Agents** [D2, D3] — managed capability for FMs to plan and execute multi-step tasks by calling your APIs. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Amazon Bedrock Knowledge Bases** [D2, D3] — managed RAG capability in Bedrock. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Amazon Bedrock model access** [D3] — the requirement to explicitly request access to a specific foundation model in the Bedrock console before use. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Amazon Kendra** [D3] — a fully managed, ML-powered enterprise search service that handles embeddings and relevance internally. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Amazon Macie** [D5] — ML-powered service that discovers and classifies sensitive data in S3. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Amazon OpenSearch Service / Serverless** [D3] — an AWS search and analytics service with a built-in vector engine, supporting hybrid vector + keyword search. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Amazon Q Business** [D2] — pre-built enterprise generative AI assistant grounded in company data and systems. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Amazon Q Developer** [D2] — generative AI coding companion and AWS resource assistant. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Amazon SageMaker** [D3] — AWS's fully managed service for building, training, and deploying ML models. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Amazon SageMaker Clarify** [D4] — AWS tool for detecting bias in datasets and models and generating SHAP-based explainability reports. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Amazon SageMaker JumpStart** [D2, D3] — model hub for deploying/fine-tuning pretrained foundation models within SageMaker. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Amazon SageMaker Model Cards** [D4] — structured documentation of a model's intended use, training data, evaluation results, and limitations. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Amazon Titan Text Embeddings** [D3] — an Amazon Bedrock embeddings model used to generate vector embeddings from text. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **AUC-ROC** [D1] — area under the ROC curve; measures ranking quality across thresholds. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Automatic model evaluation** [D3] — evaluation using built-in or custom metrics computed programmatically against a prompt dataset. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **AWS Artifact** [D5] — Self-service portal for AWS compliance reports and agreements (e.g., BAA). *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **AWS Audit Manager** [D5] — Service that automates evidence collection mapped to compliance frameworks. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **AWS CloudTrail** [D5] — Service that logs AWS API activity for auditing. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **AWS Config** [D5] — Service that records resource configuration history and evaluates compliance rules. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **AWS Customer Carbon Footprint Tool** [D4] — an AWS tool that reports estimated carbon emissions associated with a customer's AWS usage. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **AWS Inferentia** [D3] — AWS's purpose-built ML chip optimized for cost-efficient, high-throughput, low-latency inference (EC2 Inf1/Inf2). *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **AWS KMS (Key Management Service)** [D5] — Managed service for creating and controlling encryption keys. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **AWS Neuron SDK** [D3] — the software development kit used to run ML workloads on Trainium and Inferentia chips. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **AWS PrivateLink** [D5] — Technology providing private connectivity between VPCs and AWS services without traversing the public internet. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **AWS Trainium** [D3] — AWS's purpose-built ML chip optimized for cost-efficient, high-performance model training (EC2 Trn1/Trn2). *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **AWS Well-Architected Framework Sustainability Pillar** [D4] — design principles for minimizing the environmental impact of workloads on AWS. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*

## B

- **BAA (Business Associate Addendum)** [D5] — Agreement required with AWS before processing PHI under HIPAA. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Batch inference** [D1] — predictions computed offline over large datasets at once. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Bedrock model evaluation** [D3] — Bedrock jobs that assess FM quality via automatic (benchmark-based) or human evaluation. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Benchmark dataset** [D3] — a standardized dataset (often public) used to objectively and reproducibly score and compare model quality. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Bias (ML fairness sense)** [D4] — a systematic, unfair skew in a model's predictions caused by problems in training data or the training process. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Bias–variance trade-off** [D1] — balance between error from oversimplified assumptions (bias) and error from sensitivity to training data noise (variance). *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Black box model** [D4] — a model (typically a deep neural network or foundation model) whose internal decision process is not easily understood by humans. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Business metric** [D3] — an outcome-oriented measure (e.g., conversion rate, CSAT, cost per interaction) used to judge an application's real-world impact, distinct from model-quality metrics. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*

## C

- **Chain-of-thought prompting** [D2, D3] — instructing a model to reason step by step before answering. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Chunking** [D3] — splitting documents into smaller passages before embedding, so retrieval returns focused, relevant content. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Class imbalance** [D4] — one class or group is significantly underrepresented in a dataset. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Classification** [D1] — predicting a discrete category/label. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Clustering** [D1] — grouping similar unlabeled data points together. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Confusion matrix** [D1] — table comparing predicted vs. actual classifications (TP/TN/FP/FN). *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Context window** [D2] — the maximum number of tokens a model can consider in a single prompt/response. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Contextual grounding check (Guardrails)** [D4] — a Guardrails check that verifies a response is grounded in provided source content, reducing hallucination. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Continued pre-training** [D2, D3] — further training a foundation model on a large corpus of unlabeled domain data before task-specific fine-tuning. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Controllability** [D4] — the ability for humans to monitor, override, or stop an AI system's behavior. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Cross-validation** [D1] — repeatedly splitting data into train/validation folds to get a more robust performance estimate. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Customer managed key (CMK)** [D5] — A KMS key the customer creates and controls the policy/rotation for, as opposed to an AWS-managed key. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*

## D

- **Data controller / data processor** [D5] — Under GDPR, the controller decides how/why data is processed (usually the customer); the processor processes it on the controller's behalf (AWS). *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Data lineage** [D5] — A traceable record of a dataset's origin and transformations through a pipeline. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Data poisoning** [D5] — An attack where training or fine-tuning data is deliberately corrupted to manipulate a model's behavior. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms-glossary).)*
- **Data residency** [D4, D5] — the geographic location where data is stored and processed, relevant to privacy and regulatory compliance. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary), [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Data sovereignty** [D5] — The principle that data is subject to the laws of the country in which it is located. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Denied topics (Guardrails)** [D4] — a Guardrails configuration that blocks a model from engaging with specified topics. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Difference in proportions of labels (DPL)** [D4] — a pre-training bias metric measuring how differently a positive label appears across groups in the dataset. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Disparate impact** [D4] — a post-training bias metric measuring how differently a model's outcomes fall across groups in practice. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **DL (Deep Learning)** [D1] — subset of ML using multi-layer neural networks to learn representations automatically. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*

## E

- **Embedding** [D2, D3] — a numeric representation of data that captures its semantic meaning. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Encryption at rest** [D5] — Protecting stored data via encryption. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Encryption in transit** [D5] — Protecting data moving across a network, typically via TLS. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **EU AI Act** [D5] — A binding EU regulation that classifies AI systems into risk tiers (unacceptable, high, limited, minimal) and imposes obligations scaled to risk. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms-glossary).)*
- **Execution role** [D5] — An IAM role an AWS service (e.g., SageMaker) assumes to act on a customer's behalf. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Explainability** [D4] — the ability to describe, in human-understandable terms, why a model produced a specific output. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Exploratory data analysis (EDA)** [D1] — analyzing data (distributions, missing values, outliers) before modeling. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*

## F

- **F1 score** [D1] — harmonic mean of precision and recall. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Fairness** [D4] — an AI system treats individuals and groups equitably without systematically disadvantaging protected groups. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Feature** [D1] — an individual measurable input variable used by a model. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Feature engineering** [D1] — creating/transforming input variables to improve model performance. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Feature Store** [D1] — a centralized repository (e.g., SageMaker Feature Store) for storing and reusing curated features consistently between training and inference. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Few-shot prompting** [D2, D3] — including a small number of example input/output pairs in the prompt to demonstrate the desired pattern. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Fine-tuning** [D2, D3] — further training a foundation model on your own labeled data to adapt its weights for a specific task or style. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Foundation model (FM)** [D2] — a large model pretrained on broad data that can be adapted to many downstream tasks via prompting, RAG, or fine-tuning. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Foundation model (FM) application design** [D3] — the process of choosing a model and architecture based on task fit, cost, latency, modality, and customization needs. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*

## G

- **GDPR** [D5] — EU regulation governing processing of personal data. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Generative AI** [D2] — subset of deep learning where models generate new content (text, images, audio, code) rather than only predicting a label. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Governance** [D4] — the policies and processes an organization uses to control the AI lifecycle and maintain accountability. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Guardrails for Amazon Bedrock** [D2, D3, D4] — configurable safety/compliance filters applied to FM inputs and outputs. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary), [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*

## H

- **Hallucination** [D2] — fluent, confident model output that is factually incorrect or fabricated. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **HIPAA** [D5] — US law governing protected health information (PHI). *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Historical bias** [D4] — training data accurately reflects a real world that itself contains pre-existing societal inequities. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Human evaluation (model evaluation)** [D3] — evaluation where people score model outputs on subjective criteria. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Hyperparameter** [D1] — a configuration value set before training (e.g., learning rate, number of epochs). *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*

## I

- **IAM (Identity and Access Management)** [D5] — AWS service for controlling authentication and authorization to AWS resources. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **IAM Access Analyzer** [D5] — An IAM feature that identifies resources (e.g., S3 buckets, Bedrock model resource policies) shared with entities outside your AWS account or organization. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms-glossary).)*
- **In-processing (bias mitigation)** [D4] — mitigating bias by adding fairness constraints during training. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Inference** [D1] — using a trained model to generate predictions on new data. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Intellectual property (IP) indemnification** [D4] — a contractual protection (offered by some Bedrock model providers) that shifts legal risk of IP infringement claims on generated content away from the customer. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Interpretability** [D4] — how easily a human can understand how a model arrives at its outputs; trades off against raw performance for complex models. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **ISO/IEC 42001** [D5] — An international standard for a certifiable AI management system (AIMS), conceptually similar to ISO 27001 for information security. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms-glossary).)*

## L

- **Label bias / human bias** [D4] — bias introduced by human annotators when labeling training data. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Labeled data** [D1] — data where each example has a known, correct output/target. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Large language model (LLM)** [D2] — a foundation model specialized for understanding and generating natural language text. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Least privilege** [D5] — Granting only the minimum permissions needed to perform a task. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*

## M

- **MITRE ATLAS** [D5] — A knowledge base of adversary tactics and techniques against AI systems, modeled on MITRE ATT&CK. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms-glossary).)*
- **ML (Machine Learning)** [D1] — subset of AI where systems learn patterns from data instead of explicit rules. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Modality** [D3] — the type(s) of input/output a model handles (text, image, audio, video); **multimodal** models handle more than one. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Model** [D1] — the trained artifact that maps inputs to outputs. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Model drift / data drift** [D1] — degradation in model performance over time as real-world data distributions change from training data. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Model inversion (attack)** [D5] — An attack where an adversary uses crafted queries against a deployed model to try to reconstruct training data or replicate the model. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms-glossary).)*
- **Multimodal model** [D2] — a model that can accept and/or generate more than one type of content (e.g., text and images). *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*

## N

- **Negative prompting** [D2, D3] — explicitly telling a model what not to include or do. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **NIST AI Risk Management Framework (AI RMF)** [D5] — A voluntary US framework (Govern, Map, Measure, Manage) for managing risk throughout an AI system's lifecycle. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms-glossary).)*
- **Nondeterminism** [D2] — the same prompt can produce different outputs on different runs due to sampling. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*

## O

- **On-demand (Bedrock pricing)** [D3] — pay-per-token inference pricing with no capacity commitment, suited to variable/unpredictable traffic. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Overfitting** [D1] — model fits training data (including noise) too closely and generalizes poorly (high variance). *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **OWASP Top 10 for LLM Applications** [D5] — A prioritized list of the top security risks specific to large language model applications, such as prompt injection and training data poisoning. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms-glossary).)*

## P

- **Parameter** [D1] — a value learned by the model during training (e.g., neural network weight). *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **PartyRock** [D2] — a free, no-code Amazon Bedrock playground for experimenting with foundation models. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **pgvector** [D3] — an open-source PostgreSQL extension for storing and querying vector embeddings in Amazon Aurora or Amazon RDS for PostgreSQL. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **PII (Personally Identifiable Information)** [D4, D5] — data that can identify a specific individual; a key target of privacy protections and Guardrails' sensitive information filters. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary), [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Post-processing (bias mitigation)** [D4] — mitigating bias by adjusting model outputs/thresholds after training, without retraining. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Pre-processing (bias mitigation)** [D4] — mitigating bias by adjusting the training data before training. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Precision** [D1] — proportion of predicted positives that were actually positive. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Prompt** [D2] — the input text given to a foundation model to elicit a desired output. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Prompt chaining** [D3] — breaking a task into a sequence of prompts where each output feeds the next input. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Prompt engineering** [D2, D3] — designing prompts to reliably get better model output without changing model weights. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Prompt injection** [D2, D3] — a security risk where malicious input tries to override a prompt's original instructions. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Prompt template** [D3] — a reusable prompt structure with placeholders for consistent, repeatable prompt construction. *(See: [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Provisioned Throughput** [D2, D3] — reserved Bedrock model capacity for consistent performance at steady, high-volume traffic. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*

## R

- **Real-time inference** [D1] — low-latency predictions served from a persistent endpoint. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Recall (Sensitivity)** [D1] — proportion of actual positives correctly predicted. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Regression** [D1] — predicting a continuous numeric value. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Regularization** [D1] — techniques (L1/L2, dropout) that discourage overly complex models to reduce overfitting. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Reinforcement learning** [D1] — an agent learns via trial-and-error actions in an environment to maximize cumulative reward. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Responsible AI** [D4] — the practice of designing, building, and operating AI systems that are fair, explainable, private and secure, transparent, veracious and robust, well-governed, safe, and controllable. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Retrieval Augmented Generation (RAG)** [D2, D3] — grounding an FM's answers in retrieved external data at inference time, without retraining the model. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*

## S

- **Safety** [D4] — preventing an AI system from causing harm, including generating harmful content. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Sampling bias** [D4] — training data does not represent the real-world population the model will serve. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Self-attention** [D2] — the mechanism that lets a transformer weigh the relevance of every other token when processing each token. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Semantic search** [D2, D3] — search that matches by meaning (via embeddings/vectors) rather than exact keyword match. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **SHAP (Shapley Additive exPlanations)** [D4] — a feature-attribution method that quantifies how much each input feature contributed to a specific prediction. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Shared responsibility model** [D5] — The division of security duties between AWS ("of the cloud") and the customer ("in the cloud"). *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Source citation / attribution** [D5] — Referencing the source documents used to generate an AI response, as provided by Amazon Bedrock Knowledge Bases. *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*
- **Supervised learning** [D1] — learning from labeled data (classification/regression). *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*

## T

- **Temperature** [D2] — an inference parameter controlling randomness; lower values are more deterministic, higher values are more creative/random. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Token** [D2] — the basic unit of text an LLM processes and generates; often a word or part of a word. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Top-p / Top-k** [D2] — inference parameters that restrict next-token sampling to the most probable candidates, controlling output diversity. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Toxicity** [D4] — hateful, harassing, obscene, or otherwise harmful generated content. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Training data** [D1] — historical data (with labels, for supervised learning) used to fit a model. *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Transformer architecture** [D2] — the neural network architecture behind most modern LLMs, built on the self-attention mechanism. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Transparency** [D4] — openly documenting how a system was built, trained, and intended to be used, including its limitations. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*

## U

- **Underfitting** [D1] — model is too simple to capture the pattern in the data (high bias). *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*
- **Unsupervised learning** [D1] — learning structure from unlabeled data (clustering/dimensionality reduction). *(See: [Domain 1](domain-1-fundamentals-of-ai-and-ml.md#key-terms-glossary).)*

## V

- **Variance** [D1, D4] — a model's sensitivity to fluctuations in the training data (distinct from bias; see Domain 1). *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **Vector** [D2] — the numeric array an embedding is stored as; semantically similar items have vectors that are numerically close together. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary).)*
- **Vector database** [D2, D3] — a database optimized for storing and querying embeddings by similarity (e.g., Amazon OpenSearch Service vector engine). *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*
- **Veracity and robustness** [D4] — a system produces accurate, reliable output and degrades gracefully (rather than unpredictably) under unexpected or adversarial input. *(See: [Domain 4](domain-4-guidelines-for-responsible-ai.md#key-terms-glossary).)*
- **VPC endpoint** [D5] — The interface within a VPC that connects to a supported AWS service via PrivateLink (or, for gateway endpoints, S3/DynamoDB). *(See: [Domain 5](domain-5-security-compliance-governance.md#key-terms).)*

## Z

- **Zero-shot prompting** [D2, D3] — asking a model to perform a task with no examples in the prompt. *(See: [Domain 2](domain-2-fundamentals-of-generative-ai.md#key-terms-glossary), [Domain 3](domain-3-applications-of-foundation-models.md#key-terms-glossary).)*