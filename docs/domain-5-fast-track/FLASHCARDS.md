# Domain 5 Flashcards: Security, Compliance, and Governance for AI Solutions

**Spaced-repetition companion deck** · fast track: [`README.md`](README.md) · cram sheet: [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · plain-text import file: [`flashcards.tsv`](flashcards.tsv)

One card per testable concept from the Domain 5 Ultra Fast Track cram sheet, ordered to match that file's own section order so studying this deck reinforces the domain's structure. Front/back only, no prose -- for active recall or spaced repetition. This deck covers the entire domain in one place -- it is not split by fast-track part. `flashcards.tsv` holds the identical cards as a header-less, two-column (front, back) tab-separated file, importable as-is into Anki or Quizlet.

## 1. Five compliance frameworks side by side

| Front | Back |
|---|---|
| GDPR: type and geographic scope | Binding EU law -- EU/EEA, protects individuals in the EU/EEA regardless of where the company is based |
| GDPR: covered subject matter | Personal data (broad -- any PII) |
| HIPAA: type and geographic scope | Binding US law -- United States |
| HIPAA: covered subject matter | Protected health information (PHI) |
| NIST AI RMF: type and geographic scope | Voluntary US framework -- US-originated, referenced globally |
| NIST AI RMF: covered subject matter | AI system risk across its lifecycle (a process, not a data type) |
| EU AI Act: type and geographic scope | Binding EU law -- AI systems placed on the EU market or affecting people in the EU |
| EU AI Act: covered subject matter | AI systems themselves, tiered by risk |
| ISO/IEC 42001: type and geographic scope | Voluntary international standard -- global, adoptable by any organization |
| ISO/IEC 42001: covered subject matter | AI management system (AIMS) processes |
| Algorithmic Accountability Act: status | Proposed (not yet binding) US legislation |
| Algorithmic Accountability Act: covered subject matter | Automated decision systems -- would require algorithmic impact assessments |
| GDPR encryption mandate | Not explicit -- Article 32 requires only "appropriate" measures |
| HIPAA audit logging requirement | Required -- Security Rule mandates PHI access audit controls (45 CFR Sec. 164.312(b)) |
| EU AI Act audit logging requirement | Required for high-risk systems -- automatic record-keeping (Art. 12) |
| EU AI Act human oversight requirement | Required for high-risk systems -- Art. 14 mandates a human can intervene/halt |
| GDPR human oversight requirement | Article 22 -- right to human review of solely-automated decisions with legal/significant effect |
| Trap: binding vs. voluntary vs. proposed frameworks | GDPR, HIPAA, EU AI Act = binding law; NIST AI RMF, ISO/IEC 42001 = voluntary; Algorithmic Accountability Act = proposed, not yet binding -- don't confuse "proposed" with "voluntary" |
| Trap: "PHI" appears in a scenario | HIPAA applies, regardless of region |
| Trap: "risk tiers" for an AI system appear in a scenario | EU AI Act, not GDPR |
| HIPAA -- matching AWS mechanism | BAA via AWS Artifact + HIPAA-eligible services |
| GDPR -- matching AWS mechanism | EU Region residency + AWS Artifact DPA |
| EU AI Act -- matching AWS mechanism | Guardrails + Model Cards + Audit Manager |
| NIST AI RMF -- matching AWS mechanism | Model Cards + Audit Manager + Config |
| ISO/IEC 42001 -- matching AWS mechanism | AWS Artifact ISO certifications + Audit Manager |

## 2. Encryption options

| Front | Back |
|---|---|
| Encryption at rest | AWS KMS -- AWS-managed keys (e.g. aws/s3) for convenience, or customer managed keys (CMKs) for key-policy control, rotation, and auditability |
| Encryption in transit | TLS/HTTPS by default for Bedrock and SageMaker API calls -- no extra configuration |
| CMK usage logging | Every CMK Encrypt/Decrypt/GenerateDataKey call is logged to CloudTrail -- KMS manages the keys, CloudTrail logs their usage |
| What does SageMaker encrypt by default? | Notebook storage, training/inference storage volumes, and inter-node traffic during distributed training |
| What does Bedrock encrypt by default? | Data at rest/in transit by default; supports CMKs for custom models and fine-tuning data |
| Data encryption vs. model encryption | Two separate, independent CMKs -- one for the training-data bucket, one for the fine-tuned model artifact -- neither substitutes for the other |
| Differential privacy | Not encryption -- noise injected during training (DP-SGD) bounds what a deployed model's outputs can reveal about a training record; complements, doesn't replace, KMS |
| Trap: KMS vs. CloudTrail | KMS manages keys; CloudTrail logs key usage -- a frequent distractor pairing |

## 3. IAM patterns

| Front | Back |
|---|---|
| IAM policy scoping best practice | Scope to specific actions on specific resource ARNs -- e.g., bedrock:InvokeModel on one model ARN, never bedrock:* on * |
| What does an AWS service acting on your behalf (a SageMaker training job, a Bedrock fine-tuning job) assume? | An IAM execution role -- never embed long-term access keys |
| Resource-based policies | Restrict access independently of the caller's identity policy (S3 bucket policy, Bedrock model resource policy) |
| IAM Access Analyzer | Continuously flags resource-based policies shared with a principal outside your account/organization |
| Insecure plugin design -- mitigation | Scope the Lambda/action-group IAM role to least privilege; validate inputs server-side rather than trusting model-supplied values |
| Excessive agency -- mitigation | Scope an agent's execution role/action groups to only the narrow actions its task requires; require human approval before high-impact actions |
| Scenario: an AWS service needs to call another AWS service on your behalf | Attach an IAM role -- not embedded access keys, not a * wildcard |

## 4. PrivateLink / VPC isolation

| Front | Back |
|---|---|
| Interface VPC endpoint (AWS PrivateLink) | Keeps traffic to Bedrock or SageMaker entirely within the AWS network -- no internet gateway, NAT gateway, or public IP required |
| Which endpoint type do Amazon S3 and DynamoDB use? | A gateway VPC endpoint -- don't default to "interface" for every service |
| What restricts which principals can use a VPC endpoint? | A security group and a VPC endpoint policy |
| Scenario: "must never traverse the public internet" / "isolated or air-gapped VPC" | VPC endpoint (PrivateLink) -- not a NAT gateway (still routes through the public internet), not a VPN (connects networks, not a VPC to an AWS service) |
| SageMaker-to-Bedrock pipeline: keeping training data off the public internet | Route the fine-tuning job through a PrivateLink VPC endpoint |

## 5. Incident-response steps

| Front | Back |
|---|---|
| Incident response -- Detect phase | AWS CloudTrail (who/what/when on API calls), AWS Config (unencrypted/public resource drift), SageMaker Model Monitor/CloudWatch (drift, anomalous invocation volume), Guardrails intervention logs |
| Incident response -- Contain phase | Revoke/rotate the affected IAM role or CMK; disable/throttle the compromised endpoint; tighten the resource-based policy an Access Analyzer finding surfaced |
| Incident response -- Eradicate phase | Roll back to a known-good dataset/model version via SageMaker Model Registry versioning; patch the anonymization/validation code; strip/quarantine the offending source document |
| Incident response -- Recover phase | Redeploy the vetted model/dataset version; re-enable normal throttle limits; confirm Guardrails are active on the restored endpoint |
| Incident response -- Post-incident phase | Assemble evidence with AWS Audit Manager; update the IAM policy, KMS key policy, or Guardrails configuration that let the incident occur; log the root cause against the relevant threat category |
| Trap: is model drift an attack? | No -- it's degradation; its "incident response" is monitoring + scheduled retraining, not containment/eradication |
| Trap: "which service shows a bucket became public three days ago?" | AWS Config (configuration history), not CloudTrail |
| Insecure output handling | An app trusts/acts on raw LLM output (e.g., passes it to SQL) without validation; mitigate by validating/sanitizing/parameterizing LLM output plus Guardrails output filtering |
| MITRE ATLAS | Adversary tactics/techniques knowledge base for AI systems -- an industry framework, not an AWS service |
| OWASP Top 10 for LLM Applications | Prioritized LLM-specific risk checklist, including insecure output handling -- an industry framework, not an AWS service |
| Amazon Macie's role in incident response | Discovers/classifies sensitive data (PII/PHI) in S3; primary mitigation for indirect prompt injection (pre-ingestion scanning) and sensitive information disclosure |
| Titan Image Generator watermarking | Embeds an invisible, always-on watermark on generated images; Bedrock's detection API confirms its presence later to prove an image is AI-generated |

## 6. Shared-responsibility model

| Front | Back |
|---|---|
| Amazon Bedrock -- customer responsibility | IAM permissions, data sent to/from the model, Guardrail configuration, encryption key choices |
| Amazon Bedrock -- AWS responsibility | Physical infrastructure, host OS/virtualization, FM hosting and patching |
| Amazon SageMaker -- customer responsibility | IAM permissions, training data pipeline, custom training/inference containers and code, VPC config for jobs |
| Amazon SageMaker -- AWS responsibility | Physical infrastructure, host OS/virtualization, underlying compute/storage infrastructure |
| Bedrock vs. SageMaker -- customer abstraction level | Bedrock is a thin customer slice (most responsibility is AWS-managed); SageMaker is a thicker customer slice (customer takes on more configuration/code) |
| Multi-stage pipeline stage 1 (SageMaker Processing) -- customer responsibility | Container image/code, IAM role scope, VPC config, enabling KMS encryption |
| Multi-stage pipeline stage 2 (Bedrock fine-tuning) -- customer responsibility | IAM policy scope, choice of training data, PrivateLink usage |
| Multi-stage pipeline stage 3 (Bedrock Provisioned Throughput) -- customer responsibility | Guardrails configuration, invoke-access IAM policy, CloudTrail logging |
| Trap: who is always responsible for data and access configuration? | The customer -- always, regardless of how managed the service is |
| Trap: does the shared-responsibility split apply once per pipeline or per stage? | Per stage -- a data leak traced to one stage's code is the customer's fault even if other stages ran on fully-managed infrastructure |

---

**67 cards total.** For the full explanations behind any card, see the [fast track](README.md), the [Ultra Fast Track cram sheet](ULTRA-FAST-LEARN.md), or the [full Domain 5 guide](../domain-5-security-compliance-governance.md).

[← Back to the Domain 5 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md)
