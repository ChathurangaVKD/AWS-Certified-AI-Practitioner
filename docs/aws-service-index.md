# AWS Service Index — Cross-Domain Service Reference

[`docs/master-glossary.md`](master-glossary.md) and [`docs/GLOSSARY.md`](GLOSSARY.md) already index every domain guide's key **terms** (concepts like "overfitting" or "prompt injection") alphabetically. They answer "where is term X explained?" — but a term-based index is the wrong shape for a different, common question: *"where does this series mention Amazon SageMaker?"* or *"what does every domain guide say about Amazon Bedrock?"* Answering that from the term glossaries means scanning past dozens of unrelated concepts to find the AWS-service entries mixed in among them.

This page is a **service-centric** index instead: one alphabetical list of every AWS service referenced anywhere across the five domain guides, each tagged with the domain(s) `[D#, ...]` that discuss it and linked straight to the section in each domain where that discussion lives. Use it to jump directly to "all SageMaker coverage" or "all Bedrock capabilities" without re-reading whole domain guides. For the [AWS Service Decision Guide](aws-service-decision-guide.md), see that page instead — it answers "which service is the exam answer for this scenario?" rather than "where is service X discussed?"

The domain tags are:

| Tag | Domain guide |
|-----|--------------|
| `D1` | [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md) |
| `D2` | [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md) |
| `D3` | [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md) |
| `D4` | [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md) |
| `D5` | [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md) |

A service tagged `[D1, D3]` is discussed in both Domain 1 and Domain 3 — follow either link to reach that domain's coverage. A service with only one tag is still included: even single-domain coverage is worth a direct jump-link rather than a full re-read of the guide.

## Jump to a letter

[A](#a) · [G](#g) · [I](#i) · [P](#p)

---

## A

- **AI Service Cards** `[D4]` — AWS-published documentation describing the intended use, limitations, and design considerations of a specific pre-built AWS AI service (e.g., Rekognition, Transcribe). [D4](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai)
- **Amazon Augmented AI (Amazon A2I)** `[D4]` — a human-in-the-loop review workflow builder for low-confidence or high-stakes ML predictions. [D4](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai)
- **Amazon Aurora (PostgreSQL, with pgvector)** `[D3]` — a relational database that stores vector embeddings as a column type via the open-source pgvector extension. [D3](domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval)
- **Amazon Bedrock** `[D2, D3, D4, D5]` — a fully managed service offering a choice of foundation models from Amazon and third parties through a single, unified API. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) · [D3](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features) · [D4](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai) · [D5](domain-5-security-compliance-governance.md#5-aws-shared-responsibility-model-applied-to-aiml-services)
- **Amazon Bedrock Agents** `[D2, D3]` — a managed capability that lets a foundation model plan and execute multi-step tasks by calling your APIs. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) · [D3](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features)
- **Amazon Bedrock Knowledge Bases** `[D2, D3, D5]` — managed RAG that grounds foundation model answers in your own data, with source attribution. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) · [D3](domain-3-applications-of-foundation-models.md#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases) · [D5](domain-5-security-compliance-governance.md#source-citation-and-data-lineage)
- **Amazon Bedrock Model Evaluation** `[D2, D3]` — Bedrock jobs that compare foundation model quality using automatic metrics or human evaluators. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) · [D3](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features)
- **Amazon CloudWatch** `[D5]` — operational metrics/logs monitoring used to detect anomalous invocation patterns and model drift. [D5](domain-5-security-compliance-governance.md#data-monitoring)
- **Amazon Comprehend** `[D1, D5]` — managed NLP for sentiment, entities, key phrases, PII, and topics; Comprehend Medical is HIPAA-eligible. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview) · [D5](domain-5-security-compliance-governance.md#hipaa-health-insurance-portability-and-accountability-act-conceptual-level)
- **Amazon Forecast** `[D1]` — managed time-series forecasting for demand, inventory, and financial metrics. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview)
- **Amazon Fraud Detector** `[D1]` — managed real-time fraud-risk scoring for transaction/account data. [D1](domain-1-fundamentals-of-ai-and-ml.md#comparison-table-aws-managed-aiml-services-at-a-glance)
- **Amazon GuardDuty** `[D5]` — continuous threat and anomaly detection across an AWS account. [D5](domain-5-security-compliance-governance.md#data-monitoring)
- **Amazon Kendra** `[D3]` — a fully managed, ML-powered enterprise search service that handles embeddings and relevance internally. [D3](domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval)
- **Amazon Lex** `[D1]` — builds conversational chatbot/voice-bot interfaces using speech recognition and language understanding; the technology behind Alexa. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview)
- **Amazon Macie** `[D5]` — discovers and classifies sensitive data (e.g., PII) stored in Amazon S3. [D5](domain-5-security-compliance-governance.md#data-monitoring)
- **Amazon OpenSearch Service / Serverless** `[D3]` — a search and analytics service with a built-in vector engine supporting hybrid vector + keyword search. [D3](domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval)
- **Amazon Personalize** `[D1]` — real-time, individualized recommendations and re-ranking that require no ML expertise. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview)
- **Amazon Polly** `[D1]` — text-to-speech that turns text into natural, lifelike speech audio. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview)
- **Amazon Q Business** `[D2]` — a pre-built enterprise generative AI assistant grounded in company data and systems. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities)
- **Amazon Q Developer** `[D2]` — a generative AI coding companion and AWS resource assistant. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities)
- **Amazon Rekognition** `[D1, D4]` — pre-trained and custom computer vision for object/scene detection, facial analysis, and content moderation. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview) · [D4](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai)
- **Amazon SageMaker** `[D1, D2, D3, D4, D5]` — AWS's fully managed, end-to-end platform to build, train, tune, deploy, and monitor custom ML models. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview) · [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) · [D3](domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads) · [D4](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai) · [D5](domain-5-security-compliance-governance.md#1-securing-ai-systems)
- **Amazon SageMaker Clarify** `[D4]` — detects bias in datasets and trained models and generates SHAP-based explainability reports. [D4](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai)
- **Amazon SageMaker JumpStart** `[D2, D3]` — a model hub within SageMaker for deploying and fine-tuning pretrained foundation models with deep infrastructure control. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) · [D3](domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads)
- **Amazon SageMaker Model Cards** `[D4, D5]` — structured, auditable documentation of a model's intended use, training data, evaluation results, and limitations. [D4](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai) · [D5](domain-5-security-compliance-governance.md#source-citation-and-data-lineage)
- **Amazon Textract** `[D1]` — extracts text, handwriting, forms, and tables from scanned documents, preserving structure. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview)
- **Amazon Titan** `[D2, D3, D4]` — Amazon's own family of foundation models available in Bedrock (text, embeddings, image generation). [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) · [D3](domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval) · [D4](domain-4-guidelines-for-responsible-ai.md#4-legal-and-ethical-considerations)
- **Amazon Transcribe** `[D1, D4]` — automatic speech recognition that converts audio/video speech into text. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview) · [D4](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai)
- **Amazon Translate** `[D1]` — neural machine translation between languages. [D1](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview)
- **AWS Artifact** `[D5]` — a self-service portal for AWS's own compliance reports and agreements, including the HIPAA Business Associate Addendum (BAA). [D5](domain-5-security-compliance-governance.md#aws-artifact)
- **AWS Audit Manager** `[D5]` — automates collection of audit-ready evidence mapped to compliance frameworks. [D5](domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance)
- **AWS CloudTrail** `[D5]` — logs AWS API activity (who did what, and when) for security investigation and accountability. [D5](domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance)
- **AWS Config** `[D5]` — records AWS resource configuration history and evaluates it against compliance rules. [D5](domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance)
- **AWS Customer Carbon Footprint Tool** `[D4]` — reports estimated carbon emissions associated with a customer's AWS usage. [D4](domain-4-guidelines-for-responsible-ai.md#4-legal-and-ethical-considerations)
- **AWS Inferentia** `[D3]` — a purpose-built ML chip optimized for cost-efficient, high-throughput, low-latency inference. [D3](domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads)
- **AWS KMS (Key Management Service)** `[D5]` — a managed service for creating and controlling the encryption keys used to protect AI/ML data at rest. [D5](domain-5-security-compliance-governance.md#data-encryption-at-rest-and-in-transit)
- **AWS Neuron SDK** `[D3]` — the SDK used to run ML workloads on Trainium and Inferentia chips. [D3](domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads)
- **AWS PrivateLink** `[D5]` — provides private VPC connectivity to AWS services (like Bedrock and SageMaker) without traversing the public internet. [D5](domain-5-security-compliance-governance.md#aws-privatelink-and-vpc-endpoints-for-ai-services)
- **AWS Trainium** `[D3]` — a purpose-built ML chip optimized for cost-efficient, high-performance model training. [D3](domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads)
- **AWS Well-Architected Framework Sustainability Pillar** `[D4]` — design principles for minimizing the environmental impact of AI/ML workloads. [D4](domain-4-guidelines-for-responsible-ai.md#4-legal-and-ethical-considerations)

## G

- **Guardrails for Amazon Bedrock** `[D2, D3, D4, D5]` — configurable safety/compliance filters (denied topics, content/word filters, PII redaction, contextual grounding checks) applied to foundation model inputs and outputs. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) · [D3](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features) · [D4](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai) · [D5](domain-5-security-compliance-governance.md#common-security-threats-to-ai-systems-and-how-to-mitigate-them)

## I

- **IAM (AWS Identity and Access Management)** `[D5]` — controls who (a user, group, or AWS service) can do what, on which resource, across AI services. [D5](domain-5-security-compliance-governance.md#iam-roles-and-policies-for-ai-services)
- **IAM Access Analyzer** `[D5]` — identifies resources (e.g., S3 buckets, Bedrock model resource policies) shared with entities outside your AWS account. [D5](domain-5-security-compliance-governance.md#iam-roles-and-policies-for-ai-services)

## P

- **PartyRock** `[D2]` — a free, no-code Amazon Bedrock playground for experimenting with foundation models. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities)
- **Provisioned Throughput (Amazon Bedrock)** `[D2, D3]` — reserved Bedrock model capacity for consistent performance at steady, high-volume traffic. [D2](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) · [D3](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features)
