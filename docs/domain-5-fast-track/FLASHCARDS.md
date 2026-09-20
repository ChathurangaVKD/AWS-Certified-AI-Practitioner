# Domain 5 Flashcards: Security, Compliance, and Governance for AI Solutions

**Flashcard deck** · full guide: [`docs/domain-5-security-compliance-governance.md`](../domain-5-security-compliance-governance.md) · ultra fast track: [`docs/domain-5-fast-track/ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · **Last verified:** 2026-09-05

A companion active-recall / spaced-repetition deck, not a new source of
material — every card below is a front/back reformat of a fact already
verified in the [Ultra Fast Track](ULTRA-FAST-LEARN.md) cram sheet. This
deck covers the **entire domain** — it is not split by the full guide's
part-1/part-2 files. Cards are ordered to match the Ultra Fast Track's own
section order, so studying the deck top to bottom reinforces the domain's
structure. One question or term per card, one-to-two-line answer, no
re-explaining.

For app-based spaced repetition (Anki, Quizlet, etc.), import
[`flashcards.tsv`](flashcards.tsv) directly — it's the same 53 cards, same
order, tab-separated with no header row.

## 1. Five compliance frameworks side by side

| Front | Back |
|---|---|
| GDPR — type, geographic scope, covered subject matter? | Binding EU law; EU/EEA (protects individuals in the EU/EEA regardless of company location); personal data (broad, any PII). |
| HIPAA — type, geographic scope, covered subject matter? | Binding US law; United States; protected health information (PHI). |
| NIST AI RMF — type, geographic scope, covered subject matter? | Voluntary US framework; US-originated, referenced globally; AI system risk across its lifecycle (a process, not a data type). |
| EU AI Act — type, geographic scope, covered subject matter? | Binding EU law; EU (AI systems placed on the EU market or affecting people in the EU); AI systems themselves, tiered by risk. |
| ISO/IEC 42001 — type, geographic scope, covered subject matter? | Voluntary international standard; global; AI management system (AIMS) processes. |
| Algorithmic Accountability Act — type, geographic scope, covered subject matter? | Proposed (not yet binding) US legislation; United States; automated decision systems (would require algorithmic impact assessments). |
| Binding vs. voluntary — which frameworks are which? | Binding: GDPR, HIPAA, EU AI Act. Voluntary: NIST AI RMF, ISO/IEC 42001. Algorithmic Accountability Act is proposed, not voluntary. |
| "PHI" in a scenario points to which framework? | HIPAA, regardless of region. |
| "Risk tiers" for an AI system points to which framework? | EU AI Act, not GDPR. |
| HIPAA — key AWS compliance mechanism? | BAA via AWS Artifact + HIPAA-eligible services. |
| GDPR — key AWS compliance mechanism? | EU Region residency + AWS Artifact DPA. |
| EU AI Act — key AWS compliance mechanism? | Guardrails + Model Cards + Audit Manager. |
| NIST AI RMF — key AWS compliance mechanism? | Model Cards + Audit Manager + Config. |
| ISO/IEC 42001 — key AWS compliance mechanism? | AWS Artifact ISO certifications + Audit Manager. |
| HIPAA — encryption mandate and audit logging requirement? | Encryption "addressable" (implement or document equivalent); audit logging required (Security Rule, 45 CFR §164.312(b)). |
| GDPR — human oversight requirement? | Article 22 — right to human review of solely-automated decisions with legal/significant effect. |
| EU AI Act — audit logging and human oversight requirement for high-risk systems? | Both required — automatic record-keeping (Art. 12) and a human must be able to intervene/halt (Art. 14). |

## 2. Encryption options

| Front | Back |
|---|---|
| Encryption at rest — AWS service and key choice? | AWS KMS; AWS-managed keys (e.g. aws/s3) for convenience, or customer managed keys (CMKs) for key-policy control, rotation, and auditability. |
| Encryption in transit for Bedrock/SageMaker API calls — what's required? | TLS/HTTPS by default — no extra configuration. |
| Where is every CMK Encrypt/Decrypt/GenerateDataKey call logged? | CloudTrail — KMS manages the keys, CloudTrail logs their usage. |
| What does SageMaker encrypt by default? | Notebook storage, training/inference storage volumes, and inter-node traffic during distributed training. |
| Data encryption vs. model encryption — how many CMKs, and why? | Two separate, independent CMKs — one for the training-data bucket (data confidentiality), one for the fine-tuned model artifact (IP protection); neither substitutes for the other. |
| Differential privacy — is it encryption? | No — noise injected during training (DP-SGD) bounds what a deployed model's outputs can reveal about a training record; complements, doesn't replace, KMS. |
| KMS vs. CloudTrail — a frequent distractor pairing — what's the difference? | KMS manages the keys; CloudTrail logs their usage. |

## 3. IAM patterns

| Front | Back |
|---|---|
| How should IAM policies scope actions on AI services? | Specific actions on specific resource ARNs (e.g., bedrock:InvokeModel on one model ARN), never a wildcard like bedrock:* on *. |
| How does an AWS service (a SageMaker training job, a Bedrock fine-tuning job) act on your behalf? | It assumes an IAM execution role — never embed long-term access keys. |
| What do resource-based policies (S3 bucket policy, Bedrock model resource policy) restrict? | Access independently of the caller's identity policy. |
| What does IAM Access Analyzer continuously flag? | Resource-based policies shared with a principal outside your account/organization. |
| Insecure plugin design — mitigation? | Scope the Lambda/action-group IAM role to least privilege; validate inputs (e.g., account ID) server-side rather than trusting model-supplied values. |
| Excessive agency — mitigation? | Scope an agent's execution role/action groups to only the narrow actions its task requires; require human approval before high-impact actions. |
| "An AWS service needs to call another AWS service on your behalf" — what's the correct IAM pattern? | Attach an IAM role — not embedded access keys, not a wildcard. |

## 4. PrivateLink / VPC isolation

| Front | Back |
|---|---|
| What keeps traffic to Bedrock or SageMaker entirely within the AWS network? | An interface VPC endpoint, powered by AWS PrivateLink — no internet gateway, NAT gateway, or public IP required. |
| Which AWS services use a gateway VPC endpoint instead of an interface endpoint? | Amazon S3 and DynamoDB. |
| What restricts which principals can use a VPC endpoint? | A security group and a VPC endpoint policy attached to it. |
| "Must never traverse the public internet" / "isolated or air-gapped VPC" — which solution? | A VPC endpoint (PrivateLink) — not a NAT gateway (still routes through the public internet), not a VPN (connects networks, not a VPC to an AWS service). |
| How can a SageMaker-to-Bedrock fine-tuning pipeline keep training data off the public internet? | Route the fine-tuning job through a PrivateLink VPC endpoint. |

## 5. Incident-response steps

| Front | Back |
|---|---|
| Incident response — Detect phase tools? | AWS CloudTrail (who/what/when on API calls), AWS Config (unencrypted/public resource drift), SageMaker Model Monitor/CloudWatch (drift, anomalous volume), Guardrails intervention logs. |
| Incident response — Contain phase actions? | Revoke/rotate the affected IAM role or CMK; disable/throttle the compromised endpoint; tighten the resource-based policy an IAM Access Analyzer finding surfaced. |
| Incident response — Eradicate phase actions? | Roll back to a known-good dataset/model version via SageMaker Model Registry versioning; patch the anonymization/validation code; strip/quarantine the offending source document. |
| Incident response — Recover phase actions? | Redeploy the vetted model/dataset version; re-enable normal throttle limits; confirm Guardrails are active on the restored endpoint. |
| Incident response — Post-incident phase actions? | Assemble evidence with AWS Audit Manager; update the IAM/KMS/Guardrails configuration that let the incident occur; log the root cause against the relevant threat category. |
| Is model drift an "incident" requiring containment/eradication? | No — it's degradation, handled by monitoring + scheduled retraining, not incident containment. |
| "Which service shows a bucket became public three days ago?" | AWS Config (configuration history), not CloudTrail. |
| Insecure output handling — what is it, and mitigation? | An app trusts/acts on raw LLM output (e.g., passes it to SQL) without validation; mitigate by validating/sanitizing/parameterizing LLM output plus Guardrails output filtering. |
| MITRE ATLAS and OWASP Top 10 for LLM Applications — what are they? | Industry frameworks (not AWS services) for reasoning systematically about AI-specific threat categories. |
| Amazon Macie — primary mitigation role in incident response? | Discovers/classifies sensitive data (PII/PHI) in S3; primary mitigation for indirect prompt injection (pre-ingestion scanning) and sensitive information disclosure. |
| Titan Image Generator watermarking — what does it do? | Embeds an invisible, always-on watermark on generated images; Bedrock's detection API confirms its presence later to prove an image is AI-generated. |

## 6. Shared-responsibility model

| Front | Back |
|---|---|
| Amazon Bedrock — customer's scope of responsibility? | IAM permissions, data sent to/from the model, Guardrail configuration, encryption key choices. |
| Amazon Bedrock — AWS's scope of responsibility? | Physical infrastructure, host OS/virtualization, FM hosting & patching. |
| Amazon SageMaker — customer's scope of responsibility? | IAM permissions, training data pipeline, custom training/inference containers & code, VPC config for jobs. |
| Bedrock vs. SageMaker — which has the thicker customer responsibility slice? | SageMaker — the customer takes on more configuration/code than with Bedrock's thin customer slice. |
| Is the customer ever responsible for their data and access configuration, regardless of how managed the service is? | Yes — always, no matter how managed the service. |
| A per-pipeline shared-responsibility question (e.g., SageMaker Processing → Bedrock fine-tuning → Bedrock Provisioned Throughput) — applied once or per stage? | Per stage — a data leak traced to stage 1's anonymization code is the customer's fault even if later stages ran on fully-managed Bedrock infrastructure. |

---

[Full Domain 5 guide →](../domain-5-security-compliance-governance.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md) · [Interactive cheat sheet →](CHEAT-SHEET.md)
