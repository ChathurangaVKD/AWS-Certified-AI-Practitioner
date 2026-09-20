# Domain 5 Fast Track: Security, Compliance, and Governance for AI Solutions

**Condensed guide, split into 2 parts** · full guide: [`docs/domain-5-security-compliance-governance.md`](../domain-5-security-compliance-governance.md) (2,853 lines) · **Last verified:** 2026-09-06

## Why this fast track is split into two parts

Domain 5's full study guide runs 2,853 lines and covers five sections plus
two cross-cutting worked examples — long enough that a single condensed guide
covering all of it would be harder to navigate than two focused halves, so
the Fast Track splits it into two parts along the guide's natural seam
between securing/complying with a system and governing/monitoring it
afterward:

| Part | Covers | Full guide sections |
|---|---|---|
| [Part 1: AI System Security & Compliance Frameworks](part-1-security-and-compliance.md) | Securing AI systems (IAM, encryption, network isolation, PrivateLink, source citation/lineage, the security-threat catalog, cost governance, MITRE ATLAS/OWASP) and AWS compliance standards (AWS Artifact and all five compliance frameworks — GDPR, HIPAA, NIST AI RMF, EU AI Act, ISO/IEC 42001) | Sections 1-2 |
| [Part 2: Governance, Audit, Data Governance & Shared Responsibility](part-2-governance-and-monitoring.md) | AWS Config, AWS Audit Manager, and AWS CloudTrail for AI governance; data governance strategies; the AWS shared responsibility model applied to AI/ML services; and the domain's two cross-cutting worked examples | Sections 3-5 |

Each part keeps **every testable concept** from its scope — every IAM/
encryption/network control, every named security threat and mitigation, both
security frameworks, every compliance framework's scope/type/requirements,
the one-line distinction between CloudTrail/Config/Audit Manager, every
data-governance control, and the full Bedrock-vs-SageMaker shared-
responsibility split — while trimming worked-example narration down to
one-line takeaways with a link back to the full step-by-step walkthrough.

Domain 5 makes up roughly **14% of scored questions** on the AWS Certified AI
Practitioner (AIF-C01) exam. For the last 15-20 minutes before the exam, once
both parts are already familiar and you just need the highest-yield tables
refreshed one more time, see [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) — a
bullets-and-tables-only cram sheet built on top of both parts. For an even
faster, interactive scan of the same verified facts — jump links,
collapsible sections per topic, and a self-check checklist — see
[`CHEAT-SHEET.md`](CHEAT-SHEET.md). For active-recall / spaced-repetition
practice on the same verified facts — importable as-is into Anki or
Quizlet — see [`FLASHCARDS.md`](FLASHCARDS.md) (and its
[`flashcards.tsv`](flashcards.tsv) companion); this deck covers the
**entire domain**, not split by part.

## How to use this fast track

Read this fast track the day before the exam, or any time you already know
the material and just need the tables refreshed; read the [full
guide](../domain-5-security-compliance-governance.md) first if any of these
terms are new to you. Read [Part
1](part-1-security-and-compliance.md) first — it covers securing AI systems
and the five compliance frameworks — since several of [Part
2](part-2-governance-and-monitoring.md)'s worked examples and exam traps
assume that material. Each part also links back to the full guide
independently, so you can jump straight to one part if you only need to
review that topic cluster. For the final cram before the exam, drop down to
[`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) once both parts are familiar.

## Table of contents

- [Part 1: AI System Security & Compliance Frameworks](part-1-security-and-compliance.md) — Sections 1-2
- [Part 2: Governance, Audit, Data Governance & Shared Responsibility](part-2-governance-and-monitoring.md) — Sections 3-5
- [ULTRA-FAST-LEARN.md](ULTRA-FAST-LEARN.md) — bullets-and-tables-only cram sheet for the last 15-20 minutes before the exam
- [CHEAT-SHEET.md](CHEAT-SHEET.md) — interactive quick-scan cheat sheet: jump links, collapsible sections, and a self-check checklist
- [FLASHCARDS.md](FLASHCARDS.md) / [flashcards.tsv](flashcards.tsv) — active-recall flashcard deck (Anki/Quizlet-importable), covering the entire domain, not split by part

## Where each section comes from

Combined index of both parts' own front-matter tables, for jumping straight
to the full prose, mini-quiz, and worked example behind any condensed table
in either part:

| Part | This fast track | Full guide section | Approx. full-guide lines |
|---|---|---|---|
| 1 | 1. IAM roles and policies | [IAM roles and policies](../domain-5-security-compliance-governance.md#iam-roles-and-policies-for-ai-services) | 58–92 |
| 1 | 2. Data and model encryption | [Data encryption at rest and in transit](../domain-5-security-compliance-governance.md#data-encryption-at-rest-and-in-transit) + worked example | 93–238 |
| 1 | 3. AWS PrivateLink and VPC endpoints | [PrivateLink and VPC endpoints](../domain-5-security-compliance-governance.md#aws-privatelink-and-vpc-endpoints-for-ai-services) | 175–292 |
| 1 | 4. Source citation and data lineage | [Source citation and data lineage](../domain-5-security-compliance-governance.md#source-citation-and-data-lineage) + worked example | 293–360 |
| 1 | 5. Security threats and mitigations | [Common security threats](../domain-5-security-compliance-governance.md#common-security-threats-to-ai-systems-and-how-to-mitigate-them) + 2 worked examples | 361–665 |
| 1 | 6. Cost governance | [Cost governance](../domain-5-security-compliance-governance.md#cost-governance-bounding-total-spend-with-service-quotas-and-api-gateway-usage-plans) + 3 worked examples | 666–1016 |
| 1 | 7. Security frameworks | [MITRE ATLAS and OWASP Top 10](../domain-5-security-compliance-governance.md#security-frameworks-for-ai-systems-mitre-atlas-and-owasp-top-10-for-llm-applications) | 1017–1134 |
| 1 | 8. AWS Artifact | [AWS Artifact](../domain-5-security-compliance-governance.md#aws-artifact) + BAA/DPA decision guide | 1137–1197 |
| 1 | 9. The five compliance frameworks | [GDPR](../domain-5-security-compliance-governance.md#gdpr-general-data-protection-regulation-conceptual-level) through [ISO/IEC 42001](../domain-5-security-compliance-governance.md#isoiec-42001-and-the-algorithmic-accountability-act-conceptual-level) | 1198–1412 |
| 1 | 10. Compliance decision matrix | [Compliance framework decision matrix](../domain-5-security-compliance-governance.md#compliance-framework-decision-matrix) | 1413–1453 |
| 1 | 11. Requirements comparison matrix | [Requirements comparison matrix](../domain-5-security-compliance-governance.md#compliance-framework-requirements-comparison-matrix) + worked example | 1454–1608 |
| 2 | 1. AWS Config, Audit Manager, and CloudTrail | [Section 3](../domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance) + worked example | 1654–1871 |
| 2 | 2. Data governance strategies | [Section 4](../domain-5-security-compliance-governance.md#4-data-governance-strategies) + worked example | 1873–2067 |
| 2 | 3. AWS shared responsibility model | [Section 5](../domain-5-security-compliance-governance.md#5-aws-shared-responsibility-model-applied-to-aiml-services) + worked example | 2069–2265 |
| 2 | 4. Two cross-cutting worked examples, condensed | [HIPAA lifecycle worked example](../domain-5-security-compliance-governance.md#worked-example-securing-and-governing-a-hipaa-regulated-bedrock-application-across-its-lifecycle) + [multi-region worked example](../domain-5-security-compliance-governance.md#worked-example-a-multi-region-bedrock-and-sagemaker-deployment-under-gdpr-hipaa-and-the-nist-ai-rmf) | 2267–2467 |
| 2 | Comparison table: governance and monitoring services | [Full guide table](../domain-5-security-compliance-governance.md#comparison-table-governance-and-monitoring-services) | 2470–2481 |
| 2 | Comparison table: regulations at a glance | [Full guide table](../domain-5-security-compliance-governance.md#comparison-table-governance-and-compliance-regulations-at-a-glance) | 2483–2492 |

---

[← Back to the full Domain 5 guide](../domain-5-security-compliance-governance.md) · [Part 1: AI System Security & Compliance Frameworks →](part-1-security-and-compliance.md)
