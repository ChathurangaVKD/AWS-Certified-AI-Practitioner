# Domain 5 Cheat Sheet: Security, Compliance, and Governance for AI Solutions

**Interactive quick-scan cheat sheet** · companion to the [Fast Track guide](README.md) and the [Ultra Fast Track cram sheet](ULTRA-FAST-LEARN.md) · full guide: [`docs/domain-5-security-compliance-governance.md`](../domain-5-security-compliance-governance.md)

Built for a 2-3 minute skim right before the exam — jump straight to the
topic you're weakest on, expand only that section, and tick off the
self-check checklist at the end. Domain 5 is roughly **14%** of scored
questions. Every fact here already lives in the [Fast
Track](README.md) and [Ultra Fast Track](ULTRA-FAST-LEARN.md); this is a
reformat for scannability, not new content.

## Table of contents

- [1. Five compliance frameworks side by side](#1-five-compliance-frameworks-side-by-side)
- [2. Encryption options](#2-encryption-options)
- [3. IAM patterns](#3-iam-patterns)
- [4. PrivateLink / VPC isolation](#4-privatelink-vpc-isolation)
- [5. Incident-response steps](#5-incident-response-steps)
- [6. Shared-responsibility model](#6-shared-responsibility-model)
- [Commonly confused pairs](#commonly-confused-pairs)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Self-check checklist](#self-check-checklist)

---

### 1. Five compliance frameworks side by side

<details>
<summary>GDPR, HIPAA, NIST AI RMF, EU AI Act, ISO/IEC 42001 — binding vs. voluntary, encryption/audit/oversight requirements — tap to expand</summary>

| Framework | Type | Covered subject matter |
|---|---|---|
| **GDPR** | **Binding** EU law | Personal data (broad — any PII) |
| **HIPAA** | **Binding** US law | Protected health information (PHI) |
| **NIST AI RMF** | **Voluntary** US framework | AI system risk across its lifecycle |
| **EU AI Act** | **Binding** EU law | AI systems themselves, tiered by risk |
| **ISO/IEC 42001** | **Voluntary** international standard | AI management system (AIMS) processes |
| **Algorithmic Accountability Act** | *Proposed*, not yet binding US legislation | Automated decision systems |

| Framework | Encryption mandate | Audit logging | Human oversight |
|---|---|---|---|
| **GDPR** | Not explicit — "appropriate" measures (Art. 32) | No explicit clause | Art. 22 — right to human review |
| **HIPAA** | "Addressable" under the Security Rule | **Required** — Security Rule mandates it | Not mandated by statute |
| **NIST AI RMF** | Not prescribed | Recommended, not required | Recommended, not mandatory |
| **EU AI Act** | Not direct — Art. 15 accuracy/robustness | **Required** for high-risk systems | **Required** for high-risk systems (Art. 14) |
| **ISO/IEC 42001** | Not prescribed | Required indirectly (Clause 9) | Scoped to the org's own risk assessment |

- **Binding vs. voluntary:** GDPR, HIPAA, EU AI Act = binding law. NIST AI RMF, ISO/IEC 42001 = voluntary. Algorithmic Accountability Act = **proposed**, not "voluntary."
- "PHI" in a scenario → **HIPAA**, regardless of region. "Risk tiers" for an AI system → **EU AI Act**, not GDPR.

</details>

### 2. Encryption options

<details>
<summary>KMS at rest, TLS in transit, CMKs, data vs. model encryption, differential privacy — tap to expand</summary>

| Facet | Key fact |
|---|---|
| At rest | AWS KMS; AWS-managed keys or **customer managed keys (CMKs)** for key-policy control |
| In transit | **TLS/HTTPS by default** for Bedrock and SageMaker API calls |
| CMK usage | Every CMK call is logged to **CloudTrail** — KMS manages the *keys*, CloudTrail logs their *usage* |
| Data encryption vs. model encryption | **Two separate, independent CMKs** — one for training data (confidentiality), one for the fine-tuned model artifact (IP protection) |
| Differential privacy | **Not encryption** — noise injected during training (DP-SGD) bounds what a deployed model's outputs can reveal |

- Don't confuse KMS (manages keys) with CloudTrail (logs key usage) — a frequent distractor pairing.

</details>

### 3. IAM patterns

<details>
<summary>Least-privilege ARNs, execution roles, resource-based policies, Access Analyzer — tap to expand</summary>

- Scope IAM policies to specific **actions on specific resource ARNs** — never `bedrock:*` on `*`.
- An AWS service acting on your behalf assumes an IAM **execution role** — never embed long-term access keys.
- **Resource-based policies** restrict access independently of the caller's identity policy.
- **IAM Access Analyzer** continuously flags resource-based policies shared outside your account/organization.
- **Insecure plugin design** mitigation: least-privilege Lambda role + server-side input validation.
- **Excessive agency** mitigation: scope an agent's execution role to only the narrow actions its task requires; require human approval before high-impact actions.

</details>

### 4. PrivateLink / VPC isolation

<details>
<summary>Interface vs. gateway VPC endpoints — tap to expand</summary>

- An **interface VPC endpoint** (AWS PrivateLink) keeps traffic to Bedrock/SageMaker entirely within the AWS network — no internet/NAT gateway, no public IP.
- Amazon **S3 (and DynamoDB)** instead use a **gateway VPC endpoint** — don't default to "interface" for every service.
- "Must never traverse the public internet" → **VPC endpoint (PrivateLink)** — not a NAT gateway (still public internet), not a VPN (connects networks, not a VPC to a service).

</details>

### 5. Incident-response steps

<details>
<summary>Detect → contain → eradicate → recover → post-incident · MITRE ATLAS, OWASP Top 10 for LLMs — tap to expand</summary>

- [ ] **Detect** — CloudTrail (`InvokeModel`, `CreateTrainingJob`), AWS Config (unencrypted/public drift), Model Monitor/CloudWatch (drift), Guardrails intervention logs.
- [ ] **Contain** — revoke/rotate the affected IAM role or CMK; throttle the endpoint (API Gateway usage plans, Service Quotas).
- [ ] **Eradicate** — roll back via **SageMaker Model Registry** versioning; patch the code that let the incident through; quarantine the offending knowledge-base document.
- [ ] **Recover** — redeploy the vetted model/dataset version; confirm Guardrails are active.
- [ ] **Post-incident** — assemble evidence with **AWS Audit Manager**; update the policy that let it occur.

- Model drift is **degradation**, not an attack — its response is monitoring + scheduled retraining, not containment.
- "Which service shows a bucket became public **three days ago**?" → **AWS Config**, not CloudTrail.
- **Insecure output handling** — an app trusts raw LLM output without validation; mitigate by validating/sanitizing output plus Guardrails.
- **MITRE ATLAS** and **OWASP Top 10 for LLM Applications** — industry frameworks, not AWS services.
- **Amazon Macie** — discovers/classifies sensitive data in S3; primary mitigation for indirect prompt injection and sensitive info disclosure.
- **Titan Image Generator** embeds an invisible, always-on watermark; Bedrock's detection API confirms it later.

</details>

### 6. Shared-responsibility model

<details>
<summary>Bedrock vs. SageMaker split · multi-stage pipeline example — tap to expand</summary>

| | Bedrock (customer) | SageMaker (customer) |
|---|---|---|
| Scope | IAM permissions, data sent to the model, Guardrail config, key choices | IAM permissions, training data pipeline, custom code, VPC config |
| AWS side | Physical infrastructure, host OS, FM hosting & patching | Physical infrastructure, host OS, underlying compute/storage |

| Stage | Customer responsibility | AWS responsibility |
|---|---|---|
| 1. SageMaker Processing (data prep) | Container image/code, IAM role scope, KMS encryption | Physical infrastructure, host OS |
| 2. Bedrock fine-tuning | IAM policy scope, choice of training data | Training compute infrastructure |
| 3. Bedrock Provisioned Throughput | Guardrails config, invoke-access IAM policy | Serving infrastructure, multi-tenant isolation |

- The customer is **always** responsible for their data and access configuration, regardless of how managed the service is.
- The split applies **per stage** — a data leak traced to stage 1 is the customer's fault even if stages 2-3 ran on fully-managed infrastructure.

</details>

---

### Commonly confused pairs

<details>
<summary>7 pairs the exam loves to swap — tap to expand</summary>

| Pair | How to tell them apart |
|---|---|
| **KMS** vs. **CloudTrail** | KMS = manages **keys**; CloudTrail = logs key **usage** |
| **Interface VPC endpoint** vs. **Gateway VPC endpoint** | Interface = most services (Bedrock, SageMaker); Gateway = **S3 and DynamoDB only** |
| **PrivateLink** vs. **NAT gateway** vs. **VPN** | PrivateLink = never touches the internet; NAT gateway = still routes through it; VPN = connects networks, not a VPC to a service |
| **Data encryption** vs. **Model encryption** | Two **separate, independent CMKs** — one for data, one for the model artifact |
| **AWS Config** vs. **AWS CloudTrail** | Config = **configuration history** ("became public 3 days ago"); CloudTrail = **API call audit trail** |
| **Binding** vs. **Voluntary** vs. **Proposed** frameworks | GDPR/HIPAA/EU AI Act = binding; NIST AI RMF/ISO 42001 = voluntary; Algorithmic Accountability Act = proposed (not voluntary) |
| **MITRE ATLAS** vs. **OWASP Top 10 for LLM Applications** | Both are industry frameworks, not AWS services — ATLAS = adversary tactics/techniques; OWASP = prioritized LLM risk checklist |

</details>

### Rapid-fire key terms

<details>
<summary>10 key terms — tap to expand</summary>

| Term | Definition |
|---|---|
| **Customer managed key (CMK)** | A KMS key the customer controls the policy/rotation/auditability of |
| **Interface VPC endpoint** | AWS PrivateLink-powered endpoint keeping traffic off the public internet |
| **Gateway VPC endpoint** | The S3/DynamoDB-specific VPC endpoint type |
| **IAM Access Analyzer** | Flags resource-based policies shared outside the account/organization |
| **Excessive agency** | A Bedrock Agent scoped with more permissions than its task requires |
| **Insecure output handling** | An app trusting/acting on raw LLM output without validation |
| **MITRE ATLAS** | Adversary tactics/techniques knowledge base for AI systems |
| **OWASP Top 10 for LLM Applications** | Prioritized LLM-specific risk checklist |
| **Amazon Macie** | Discovers/classifies sensitive data (PII/PHI) in S3 |
| **AWS Audit Manager** | Assembles evidence (built on CloudTrail + Config) for compliance/risk records |

</details>

---

## Self-check checklist

Tick each fact you can already state cold — anything unchecked is what to
re-read in the [Fast Track](README.md) or [Ultra Fast
Track](ULTRA-FAST-LEARN.md) before the exam.

- [ ] **Binding vs. voluntary:** GDPR, HIPAA, EU AI Act = binding law; NIST AI RMF, ISO/IEC 42001 = voluntary; Algorithmic Accountability Act = **proposed**, not voluntary.
- [ ] "PHI" → **HIPAA** regardless of region; "risk tiers for an AI system" → **EU AI Act**, not GDPR.
- [ ] Don't confuse **KMS** (manages keys) with **CloudTrail** (logs key usage).
- [ ] Data encryption and model encryption use **two separate, independent CMKs** — neither substitutes for the other.
- [ ] "An AWS service needs to call another AWS service on your behalf" → attach an IAM **role**, never embedded access keys or a `*` wildcard.
- [ ] "Must never traverse the public internet" → **VPC endpoint (PrivateLink)** — not a NAT gateway, not a VPN.
- [ ] Amazon **S3 (and DynamoDB)** use a **gateway** VPC endpoint, not an interface endpoint.
- [ ] Model drift is **degradation**, not an attack — respond with monitoring + retraining, not incident containment.
- [ ] "Which service shows a bucket became public **three days ago**?" → **AWS Config**, not CloudTrail.
- [ ] **MITRE ATLAS** and **OWASP Top 10 for LLM Applications** are industry frameworks, not AWS services.
- [ ] The shared-responsibility split applies **per stage** of a pipeline, not once for the whole thing.
- [ ] The customer is **always** responsible for their data and access configuration, no matter how managed the service is.

---

For the full explanations, worked examples, and the compliance-framework
decision matrix this cheat sheet intentionally omits, go back to the
[Domain 5 fast track](README.md), the [Ultra Fast Track](ULTRA-FAST-LEARN.md),
or the [full Domain 5 guide](../domain-5-security-compliance-governance.md).

[← Back to the Domain 5 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md)
