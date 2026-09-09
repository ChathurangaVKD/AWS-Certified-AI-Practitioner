# Domain 5 Ultra Fast Track: Security, Compliance, and Governance for AI Solutions

**Ultra-condensed cram sheet** · full guide: [`docs/domain-5-security-compliance-governance.md`](../domain-5-security-compliance-governance.md) (2,853 lines) · **Last verified:** 2026-09-05

Bullets and tables only — no prose, no worked examples, no mini-quizzes.
Domain 5 has no separate ~40%-length Fast Track condensation guide yet,
so this cram sheet condenses the full guide's own [Quick-reference cheat
sheet](../domain-5-security-compliance-governance.md#quick-reference-cheat-sheet)
plus Sections 1, 2, and 5 directly down to two pages. For the last 15-20
minutes before the exam, once the full guide is already familiar and you
just need the highest-yield tables refreshed one more time. Domain 5 is
roughly **14%** of scored questions.

## Table of contents

- [1. Five compliance frameworks side by side](#1-five-compliance-frameworks-side-by-side)
- [2. Encryption options](#2-encryption-options)
- [3. IAM patterns](#3-iam-patterns)
- [4. PrivateLink / VPC isolation](#4-privatelink-vpc-isolation)
- [5. Incident-response steps](#5-incident-response-steps)
- [6. Shared-responsibility model](#6-shared-responsibility-model)
- [Where each row comes from](#where-each-row-comes-from)

---

## 1. Five compliance frameworks side by side

| Framework | Type | Geographic scope | Covered subject matter |
|---|---|---|---|
| **GDPR** | Binding EU law | EU/EEA — protects individuals in the EU/EEA regardless of where the company is based | Personal data (broad — any PII) |
| **HIPAA** | Binding US law | United States | Protected health information (PHI) |
| **NIST AI RMF** | Voluntary US framework | US-originated, referenced globally | AI system risk across its lifecycle (process, not a data type) |
| **EU AI Act** | Binding EU law | EU — AI systems placed on the EU market or affecting people in the EU | AI systems themselves, tiered by risk |
| **ISO/IEC 42001** | Voluntary international standard | Global — adoptable by any organization | AI management system (AIMS) processes |
| **Algorithmic Accountability Act** | *Proposed* (not yet binding) US legislation | United States | Automated decision systems — would require algorithmic impact assessments |

**Key requirements side by side:**

| Framework | Encryption mandate | Audit logging | Data residency | Human oversight |
|---|---|---|---|---|
| **GDPR** | Not explicit — Article 32 requires "appropriate" measures only | No explicit clause; accountability principle (Art. 5(2)) requires demonstrating compliance | No blanket rule, but cross-border transfer limits push toward EU/EEA Regions | Article 22 — right to human review of solely-automated decisions with legal/significant effect |
| **HIPAA** | "Addressable" under the Security Rule — must implement or document an equivalent | **Required** — Security Rule mandates PHI access audit controls (45 CFR §164.312(b)) | None — governs access/encryption of PHI, not location | Not mandated by statute; expected operationally for clinical decisions |
| **NIST AI RMF** | Not prescribed — defers to controls like AWS KMS (Manage function) | Recommended (Govern/Measure) for an auditable trail — not required | Not addressed — a process framework | Recommended (Govern/Manage) — not mandatory |
| **EU AI Act** | Not direct — addressed via high-risk "accuracy, robustness, cybersecurity" (Art. 15) | **Required** for high-risk systems — automatic record-keeping (Art. 12) | Not required — focuses on training/validation data governance (Art. 10) | **Required** for high-risk systems — Art. 14 mandates a human can intervene/halt |
| **ISO/IEC 42001** | Not prescribed — org selects controls via its own AI risk assessment | Required indirectly — certifiable AIMS needs monitoring/internal audit (Clause 9) | Not addressed — an organizational management-system standard | Annex A controls on human oversight, scoped to the org's own risk assessment |

- **Binding vs. voluntary:** GDPR, HIPAA, EU AI Act = binding law.
  NIST AI RMF, ISO/IEC 42001 = voluntary. Algorithmic Accountability Act
  = *proposed*, not yet binding — don't confuse "proposed" with
  "voluntary."
- "PHI" in a scenario → **HIPAA**, regardless of region. "Risk tiers" for
  an AI system → **EU AI Act**, not GDPR.
- HIPAA (BAA via AWS Artifact) + HIPAA-eligible services; GDPR (EU Region
  residency + AWS Artifact DPA); EU AI Act (Guardrails + Model Cards +
  Audit Manager); NIST AI RMF (Model Cards + Audit Manager + Config);
  ISO/IEC 42001 (AWS Artifact ISO certifications + Audit Manager).

## 2. Encryption options

| Facet | Key fact |
|---|---|
| At rest | AWS KMS; AWS-managed keys (e.g. `aws/s3`) for convenience, or **customer managed keys (CMKs)** for key-policy control, rotation, and auditability |
| In transit | TLS/HTTPS by default for Bedrock and SageMaker API calls — no extra configuration |
| CMK usage | Every CMK `Encrypt`/`Decrypt`/`GenerateDataKey` call is logged to CloudTrail — KMS manages the *keys*, CloudTrail logs their *usage* |
| SageMaker | Encrypts notebook storage, training/inference storage volumes, and inter-node traffic during distributed training |
| Bedrock | Encrypts data at rest/in transit by default; supports CMKs for custom models and fine-tuning data |
| Data encryption vs. model encryption | Two **separate, independent** CMKs — one for the training-data bucket (PHI/data confidentiality), one for the fine-tuned model artifact (IP protection) — neither substitutes for the other |
| Differential privacy | Not encryption — noise injected during training (DP-SGD) bounds what a *deployed model's outputs* can reveal about a training record; complements, doesn't replace, KMS |

- Don't confuse KMS (manages keys) with CloudTrail (logs key usage) — a
  frequent distractor pairing.

## 3. IAM patterns

- Scope IAM policies to specific **actions on specific resource ARNs** —
  e.g., `bedrock:InvokeModel` on one model ARN, never `bedrock:*` on `*`.
- An AWS service acting on your behalf (a SageMaker training job, a
  Bedrock fine-tuning job) assumes an IAM **execution role** — never
  embed long-term access keys.
- **Resource-based policies** (S3 bucket policy, Bedrock model resource
  policy) restrict access independently of the caller's identity policy.
- **IAM Access Analyzer** continuously flags resource-based policies
  shared with a principal outside your account/organization.
- **Insecure plugin design** mitigation: scope the Lambda/action-group
  IAM role to least privilege; validate inputs (e.g., account ID)
  server-side rather than trusting model-supplied values.
- **Excessive agency** mitigation: scope an agent's execution role/action
  groups to only the narrow actions its task requires; require human
  approval before high-impact actions (delete, terminate, modify).
- "An AWS service needs to call another AWS service on your behalf" →
  attach an IAM **role** — not embedded access keys, not a `*` wildcard.

## 4. PrivateLink / VPC isolation

- An **interface VPC endpoint** (powered by AWS PrivateLink) keeps
  traffic to Bedrock or SageMaker entirely within the AWS network — no
  internet gateway, NAT gateway, or public IP required.
- Amazon S3 (and DynamoDB) instead use a **gateway VPC endpoint** — don't
  default to "interface" for every service.
- Attach a security group and a VPC endpoint policy to restrict which
  principals can use the endpoint.
- "Must never traverse the public internet" / "isolated or air-gapped
  VPC" → **VPC endpoint (PrivateLink)** — not a NAT gateway (still routes
  through the public internet), not a VPN (connects networks, not a VPC
  to an AWS service).
- A SageMaker-to-Bedrock pipeline can route the fine-tuning job itself
  through a PrivateLink VPC endpoint so training data never traverses
  the public internet.

## 5. Incident-response steps

- [ ] **Detect** — AWS CloudTrail (who/what/when on `InvokeModel`,
      `CreateTrainingJob`, etc.), AWS Config (unencrypted/public resource
      drift), SageMaker Model Monitor / Amazon CloudWatch (drift,
      anomalous invocation volume), Guardrails intervention logs
      (blocked topics, filtered content).
- [ ] **Contain** — revoke/rotate the affected IAM role or CMK; disable
      or throttle the compromised endpoint (API Gateway usage plans,
      Service Quotas); tighten the resource-based policy an IAM Access
      Analyzer finding surfaced.
- [ ] **Eradicate** — roll back to a known-good dataset/model version via
      **SageMaker Model Registry** versioning (data poisoning, supply
      chain); patch the anonymization/validation code that let sensitive
      data or a poisoned example through; strip/quarantine the
      offending source document from the knowledge base (indirect
      prompt injection).
- [ ] **Recover** — redeploy the vetted model/dataset version; re-enable
      normal throttle limits; confirm Guardrails (content filters,
      denied topics, PII filters) are active on the restored endpoint.
- [ ] **Post-incident** — assemble evidence with **AWS Audit Manager**
      (built on CloudTrail + Config) for the compliance/risk record;
      update the IAM policy, KMS key policy, or Guardrails configuration
      that let the incident occur; log the root cause against the
      relevant threat category (data poisoning, prompt injection,
      insecure output handling, model inversion/extraction, DoS, supply
      chain, sensitive-info disclosure, insecure plugin design,
      excessive agency, overreliance).

- Model drift is **degradation**, not an attack — its "incident
  response" is monitoring + scheduled retraining, not containment/
  eradication.
- "Which service shows a bucket became public **three days ago**?" →
  AWS Config (configuration history), not CloudTrail.
- **Insecure output handling** — an app trusts/acts on raw LLM output
  (e.g., passes it to SQL) without validation; mitigate by
  validating/sanitizing/parameterizing LLM output before use plus
  Guardrails output filtering.
- **MITRE ATLAS** (adversary tactics/techniques knowledge base for AI
  systems) and **OWASP Top 10 for LLM Applications** (prioritized
  LLM-specific risk checklist, incl. insecure output handling) —
  industry frameworks, not AWS services, for reasoning about these
  threat categories systematically.
- **Amazon Macie** — discovers/classifies sensitive data (PII/PHI) in
  S3; primary mitigation for indirect prompt injection (pre-ingestion
  scanning) and sensitive information disclosure.
- **Titan Image Generator** embeds an invisible, always-on watermark on
  generated images; Bedrock's detection API confirms its presence later
  to prove an image is AI-generated (provenance watermarking).

## 6. Shared-responsibility model

| | Amazon Bedrock (customer) | Amazon Bedrock (AWS) | Amazon SageMaker (customer) | Amazon SageMaker (AWS) |
|---|---|---|---|---|
| Scope | IAM permissions, data sent to/from the model, Guardrail configuration, encryption key choices | Physical infrastructure, host OS/virtualization, FM hosting & patching | IAM permissions, training data pipeline, custom training/inference containers & code, VPC config for jobs | Physical infrastructure, host OS/virtualization, underlying compute/storage infrastructure |
| Abstraction | Thin customer slice — most responsibility is AWS-managed | — | Thicker customer slice — customer takes on more configuration/code | — |

**Multi-stage pipeline example (SageMaker Processing → Bedrock fine-tuning → Bedrock Provisioned Throughput):**

| Stage | Customer responsibility | AWS responsibility |
|---|---|---|
| 1. SageMaker Processing (data prep) | Container image/code, IAM role scope, VPC config, enabling KMS encryption | Physical infrastructure, host OS, patching the SageMaker platform |
| 2. Bedrock fine-tuning | IAM policy scope, choice of training data, PrivateLink usage | Training compute infrastructure, foundation model weights |
| 3. Bedrock Provisioned Throughput (serving) | Guardrails configuration, invoke-access IAM policy, CloudTrail logging | Serving infrastructure, host OS, multi-tenant isolation |

- The customer is **always** responsible for their data and access
  configuration, regardless of how managed the service is.
- A per-pipeline question applies the split **per stage**, not once for
  the whole pipeline — a data leak traced to stage 1's anonymization
  code is the customer's fault even if stages 2-3 ran on fully-managed
  Bedrock infrastructure.

---

## Where each row comes from

| This cram sheet | Full guide section |
|---|---|
| 1. Five compliance frameworks side by side | [Compliance framework decision matrix](../domain-5-security-compliance-governance.md#compliance-framework-decision-matrix), [Compliance framework requirements comparison matrix](../domain-5-security-compliance-governance.md#compliance-framework-requirements-comparison-matrix) |
| 2. Encryption options | [Data encryption at rest and in transit](../domain-5-security-compliance-governance.md#data-encryption-at-rest-and-in-transit), [Quick-reference cheat sheet](../domain-5-security-compliance-governance.md#quick-reference-cheat-sheet) |
| 3. IAM patterns | [IAM roles and policies for AI services](../domain-5-security-compliance-governance.md#iam-roles-and-policies-for-ai-services), [Common security threats](../domain-5-security-compliance-governance.md#common-security-threats-to-ai-systems-and-how-to-mitigate-them) |
| 4. PrivateLink / VPC isolation | [AWS PrivateLink and VPC endpoints for AI services](../domain-5-security-compliance-governance.md#aws-privatelink-and-vpc-endpoints-for-ai-services) |
| 5. Incident-response steps | [Common security threats](../domain-5-security-compliance-governance.md#common-security-threats-to-ai-systems-and-how-to-mitigate-them), [AWS Config, AWS Audit Manager, and AWS CloudTrail](../domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance) |
| 6. Shared-responsibility model | [AWS shared responsibility model applied to AI/ML services](../domain-5-security-compliance-governance.md#5-aws-shared-responsibility-model-applied-to-aiml-services) |

For the full prose, worked examples, mermaid diagrams, and mini-quizzes
this cram sheet intentionally omits, go back to the
[full Domain 5 guide](../domain-5-security-compliance-governance.md). For
material spanning multiple domains, see
[`docs/cross-domain-concept-map.md`](../cross-domain-concept-map.md).

[Full Domain 5 guide →](../domain-5-security-compliance-governance.md)
