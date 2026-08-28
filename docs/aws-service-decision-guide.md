# AWS Service Decision Guide: A Cross-Domain Quick Reference

[Domain 1](domain-1-fundamentals-of-ai-and-ml.md), [Domain 2](domain-2-fundamentals-of-generative-ai.md),
[Domain 3](domain-3-applications-of-foundation-models.md), and
[Domain 5](domain-5-security-compliance-governance.md) each carry their own
comparison table, scoped to that domain's task statements. That's the right
depth for studying a domain in isolation, but the exam (and real-world
architecture decisions) routinely mixes "which AI service?" and "which
security/compliance service?" questions in the same scenario. This page is
a **consolidated quick reference** that sits on top of those domain tables —
it doesn't replace them, it points back to them for the full detail.

Use this page when a scenario gives you a use case and you need to jump
straight to "which AWS service is the exam answer here?" without re-reading
an entire domain guide. If instead you already know the service and want
every place it's discussed across the series (e.g., "everywhere Amazon
Bedrock is mentioned"), see [`aws-service-index.md`](aws-service-index.md) --
an alphabetical, per-service index rather than a decision flow.

---

## 1. Decision flow: SageMaker vs. Bedrock vs. purpose-built AI services

The single most tested decision pattern across Domains 1–3 is **"which AWS
service should I reach for?"** — and it always resolves through the same
three-question flow, regardless of whether the use case is classic ML or
generative AI:

```
START: What are you trying to build?
│
├─ 1. Does the task involve a *foundation model* (generating or reasoning
│     over text, images, code, or other content; chat; summarization;
│     RAG; agents)?
│     │
│     ├─ YES → 2. Do you need a ready-made, fully managed *application*
│     │         rather than a model you integrate yourself?
│     │         │
│     │         ├─ YES → Amazon Q Business (enterprise assistant grounded
│     │         │        in your data), Amazon Q Developer (coding
│     │         │        companion), or PartyRock (no-code prototyping)
│     │         │
│     │         └─ NO  → Amazon Bedrock — choose a foundation model,
│     │                  and layer on Knowledge Bases (RAG), Agents
│     │                  (multi-step task execution), Guardrails (safety
│     │                  filters), and Model Evaluation as needed.
│     │                  Need deep infrastructure control alongside the
│     │                  FM (custom training pipelines, Trainium/
│     │                  Inferentia)? → SageMaker JumpStart instead.
│     │
│     └─ NO  → 3. Does a purpose-built managed AI service already solve
│               this exact use case?
│               │
│               ├─ YES → Use the purpose-built service:
│               │        • Amazon Personalize — recommendations
│               │        • Amazon Forecast — time-series forecasting
│               │        • Amazon Rekognition — image/video analysis
│               │        • Amazon Transcribe — speech-to-text
│               │        • Amazon Comprehend — text/NLP analytics
│               │        • Amazon Polly — text-to-speech
│               │        • Amazon Translate — language translation
│               │        • Amazon Lex — conversational chat/voice bots
│               │        • Amazon Textract — structured document extraction
│               │        • Amazon Fraud Detector — fraud-risk scoring
│               │
│               └─ NO  → Amazon SageMaker — build, train, and deploy a
│                        bespoke model when no managed service covers
│                        the use case, or deep customization is required.
```

> **Exam tip — the rule behind the flow:** at every branch, the more
> "out of the box" and purpose-built a service is for the exact scenario
> described, the more likely it's the correct exam answer. The flow only
> reaches **Amazon Bedrock** (for generative use cases) or **Amazon
> SageMaker** (for everything else) when no purpose-built service already
> covers the ask. Building a custom model or FM integration for a task a
> purpose-built service already handles is a classic exam distractor.

For the full service-by-service detail behind this flow, see:
- [Domain 1 §5 — AWS managed AI/ML services (conceptual overview)](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview)
  and its [comparison table](domain-1-fundamentals-of-ai-and-ml.md#comparison-table-aws-managed-aiml-services-at-a-glance)
- [Domain 2 §5 — AWS generative AI services and capabilities](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities)
  and its [comparison table](domain-2-fundamentals-of-generative-ai.md#comparison-table-aws-generative-ai-services-at-a-glance)
- [Domain 3 §5 — Amazon Bedrock features](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features)
  and the [customization-approach comparison table](domain-3-applications-of-foundation-models.md#comparison-table-customization-approaches-for-foundation-model-applications)

---

## 2. Comparison table: security, compliance, and governance services

Domain 5 scenarios frequently confuse these four services because they all
touch "compliance" — but each answers a different question:

| Service | Category | What it does | Answers the question... | When it's the exam answer |
|---|---|---|---|---|
| **AWS CloudTrail** | Governance — activity logging | Logs every API call (who, what, when) across your account | "Who invoked this model / changed this resource, and when?" | You need a record of a specific API call, e.g. a specific `InvokeModel` or `CreateEndpoint` |
| **AWS Config** | Governance — configuration tracking | Records resource configuration state and evaluates it against compliance rules over time | "Is this resource compliant right now, and when did its configuration change?" | You need to detect that a SageMaker endpoint or S3 bucket drifted out of an encrypted/private configuration |
| **AWS Audit Manager** | Compliance — evidence collection | Automates collecting audit evidence mapped to a named framework (HIPAA, ISO 27001, SOC 2, etc.) | "Can I generate an audit-ready compliance report?" | You need to assemble evidence for an external or internal audit of an AI system |
| **AWS Artifact** | Compliance — AWS's own attestations | On-demand self-service portal for AWS's own compliance reports and agreements (SOC reports, ISO certifications, the HIPAA BAA) | "Where do I get proof of *AWS's* compliance, or sign an agreement with AWS?" | You need to download a SOC 2 report or execute a Business Associate Addendum (BAA) — it does not audit *your* account |

> **Exam tip:** CloudTrail and Config both watch *your* account, but
> CloudTrail is about **events/actions** while Config is about **resource
> state over time**. Audit Manager and Artifact both relate to
> "compliance," but Audit Manager assembles evidence *about your account*
> while Artifact hands you evidence *about AWS itself*.

See the fuller version of this table (which also covers Amazon Macie and
Amazon GuardDuty) at
[Domain 5 — comparison table: governance and monitoring services](domain-5-security-compliance-governance.md#comparison-table-governance-and-monitoring-services).

---

## 3. Comparison table: encryption and privacy options

| Option | Protects | Key concept | When to use it |
|---|---|---|---|
| **AWS KMS (Key Management Service)** | Data at rest (S3, EBS, SageMaker model artifacts, Bedrock fine-tuning data) | AWS-managed keys are simplest; **customer managed keys (CMKs)** give you control over key policy, rotation, and give you a CloudTrail-logged audit trail of every decrypt | You must encrypt sensitive data at rest and control (or prove control over) exactly who can decrypt it |
| **AWS PrivateLink / VPC endpoints** | Data in transit between your VPC and an AWS service | An **interface VPC endpoint** keeps traffic to a supported AWS service on the AWS network backbone — it never traverses the public internet, and needs no internet gateway, NAT gateway, or public IP | A scenario says a workload runs in a private/isolated VPC (no internet access) but still needs to call an AI service like Bedrock or SageMaker |
| **HIPAA eligibility + BAA (via AWS Artifact)** | Protected health information (PHI) | To legally process PHI on AWS, you must execute a **Business Associate Addendum (BAA)** — obtained through AWS Artifact — and use only **HIPAA-eligible services**, configured per AWS's HIPAA guidance (encryption enabled, access controls applied) | The scenario mentions patient data, PHI, or a healthcare workload — think "BAA + HIPAA-eligible services," not just "encrypt it" |

> **Exam tip:** These three are often layered in the same scenario: a
> healthcare company fine-tuning a model on Bedrock with patient data
> needs a **customer-managed KMS key** (control over decryption), a
> **VPC endpoint** (keep the training traffic off the public internet),
> and a **signed BAA** (the legal prerequisite for touching PHI at all) —
> none of the three substitutes for the others.

For the full walkthrough of each concept, see Domain 5:
[Data encryption at rest and in transit](domain-5-security-compliance-governance.md#data-encryption-at-rest-and-in-transit),
[AWS PrivateLink and VPC endpoints for AI services](domain-5-security-compliance-governance.md#aws-privatelink-and-vpc-endpoints-for-ai-services),
[AWS Artifact](domain-5-security-compliance-governance.md#aws-artifact), and
[HIPAA — conceptual level](domain-5-security-compliance-governance.md#hipaa-health-insurance-portability-and-accountability-act-conceptual-level).

---

## How this guide relates to the domain guides

This page is intentionally short: it is a **decision aid**, not a
replacement for the domain guides' depth. If a scenario needs more context
than a single table row gives you — the *why* behind a service choice, a
worked AWS example, or an exam-tip explanation of a common distractor —
follow the links above into the relevant domain section. See also the
[cross-domain concept map](cross-domain-concept-map.md) for how Domain 1
fundamentals flow into the later domains' service and governance choices.
