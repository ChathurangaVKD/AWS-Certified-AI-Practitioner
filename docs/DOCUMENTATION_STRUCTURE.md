# Documentation Structure

This page is a map of how this repository is actually organized today: what
each file is for, how the five domain guides are put together internally,
what the nine cross-domain support documents add on top of them, and how
all of it cross-links. Read this first if you're a contributor trying to
figure out where something lives or where a new addition should go.

## Repository layout

```
AWS-Certified-AI-Practitioner/
├── README.md                                  study plan + links into every doc below
├── sonar-project.properties                    SonarQube/SonarCloud scanner config
├── docs/
│   ├── DOCUMENTATION_STRUCTURE.md              this file
│   │
│   │   Five domain guides (the exam content itself) ──────────────
│   ├── domain-1-fundamentals-of-ai-and-ml.md
│   ├── domain-2-fundamentals-of-generative-ai.md
│   ├── domain-3-applications-of-foundation-models.md
│   ├── domain-4-guidelines-for-responsible-ai.md
│   ├── domain-5-security-compliance-governance.md
│   │
│   │   Nine cross-domain support documents ────────────────────────
│   ├── aws-service-index.md                    every AWS service, indexed across all 5 guides
│   ├── aws-service-decision-guide.md           "which service is the exam answer here?"
│   ├── cross-domain-concept-map.md             how D1/D2 concepts flow into D3/D4/D5, D3 into D4/D5
│   ├── cross-domain-scenario-questions.md      22 questions spanning 2+ domains
│   ├── case-study-ai-system-lifecycle.md       one company, one system, all 5 domains
│   ├── exam-preparation-strategy.md            reading order, schedules, mock-exam plan
│   ├── full-length-mock-exam.md                65-question, 90-minute mock exam
│   ├── master-glossary.md                      alphabetical term index, `[D#, ...]` tags
│   └── GLOSSARY.md                             the same term set as backlinked prose
│
└── tests/
    ├── test_domain_N_study_guide.py            structural checks, one file per domain
    ├── test_domain_N_quick_reference_cheat_sheet.py
    ├── test_domain_N_subsection_mini_quizzes.py
    ├── test_domain_footer_navigation.py        breadcrumb link checks, all 5 domains
    ├── test_cross_reference_links.py           every internal link/anchor resolves
    ├── test_documentation_structure.py         this file stays in sync with reality
    └── ...                                      one test file per cross-domain doc above
```

## Domain guides: per-domain coverage breakdown

`docs/domain-N-fundamentals-of-*.md` — five markdown files, one per exam
domain, currently 1,792–4,670 lines each, **13,169 lines total**:

- Domain 1: 1,792 lines
- Domain 2: 2,169 lines
- Domain 3: 4,670 lines
- Domain 4: 2,118 lines
- Domain 5: 2,420 lines

All five follow the same template:

- a breadcrumb navigation line (previous domain · position in sequence ·
  next domain) and a `## Table of contents` linking every numbered section
  within the file;
- a domain overview, then 5–8 major numbered sections (`## 1`, `## 2`, …),
  each with an "AWS example" and an "Exam tip";
- a condensed **"## Quick-reference cheat sheet"** section — every domain
  now has one (Domain 3 got it first; Domains 1, 2, 4, and 5 each later
  added their own), sitting between the comparison table and the glossary
  for last-minute review;
- domain-specific supplementary sections beyond the shared template, e.g.
  Domain 2's inference-parameter interaction visual guide and per-domain
  "mini quiz" call-outs embedded under individual subsections;
- a comparison/reference table (e.g., "AWS managed AI/ML services at a
  glance" in D1, "AWS generative AI services" in D2);
- a `## Key terms glossary` (15–50 entries; Domain 5's heading matches the
  same "Key terms glossary" convention used by D1–D4);
- a dedicated `## Worked example` section closing out each domain;
- `## Practice questions` (15–20 per domain, except **24 for Domain 1**,
  **24 for Domain 2**, **28 for Domain 3**, and **32 for Domain 5**
  (Domain 4 has 20), including exactly 2 multiple-response ["select TWO"]
  questions, for **128 domain practice questions in total** across
  the five domain guides) and a full `## Answer key` with justifications
  ruling out each wrong answer.

**Worked examples:** Domains 1, 2, 3, 4, and 5 each close with a dedicated
"## Worked example" section stitching the domain's concepts into one
end-to-end scenario: a loan-default predictor (D1), a generative AI
support assistant (D2), a RAG-based policy-lookup assistant (D3), auditing
and documenting a responsible e-commerce recommendation engine (D4), and a
HIPAA-regulated Bedrock application (D5).

Domain 3 carries far more worked examples than any other domain, so its
count needs its own methodology note: it has eight standalone "## Worked
example" sections in total (implementing RAG for a policy-lookup
assistant — the closing example referenced above — troubleshooting a
failing RAG system, selecting a foundation model under multiple competing
constraints, estimating a context-window token budget, estimating tokens
for long-document summarization, comparing monthly inference costs across
model tiers, comparing fine-tuning against prompt engineering, and a
Bedrock Agent executing a multi-step task with tool calling), plus seven
further worked examples that are subsections nested at the "###" or
"####" level inside their enclosing numbered sections rather than
standalone sections: two concrete model-pair comparisons; the same task
worked four different ways; building a product-knowledge assistant using
Kendra's GenAI Index as a Bedrock Knowledge Base data source; when
QLoRA's quality loss becomes unacceptable; when to use Cohere Rerank in a
RAG pipeline; whether a 2-point BLEU/ROUGE improvement is statistically
significant ("### Worked example: is a 2-point BLEU/ROUGE improvement
statistically significant?"); and picking evaluation metrics for a
scenario. Counting standalone sections only, Domain 3 has eight worked
examples; counting the seven nested subsections too, it has fifteen —
more worked examples than any other domain guide.

Domain 4 similarly grew beyond a single worked example: alongside the
closing e-commerce recommendation-engine audit, it now has a second
standalone "## Worked example" section auditing a classical ML
small-business loan-approval classifier for proxy-variable bias, a third
diagnosing retrieval-induced bias and hallucination in a RAG-based HR
assistant, and a fourth isolating the Section 5 performance/
interpretability tradeoff itself — a health-insurance prior-authorization
scenario where a regulatory explainability requirement forces the team off
a post-hoc-SHAP-on-a-black-box approach and onto a natively interpretable
model — four standalone "## Worked example" sections in total for
Domain 4, covering bias-detection patterns across a deep learning ranking
model, a classical ML classifier, and a foundation-model/RAG application,
plus a dedicated performance-versus-interpretability tradeoff walkthrough.

Domain 4 also has one nested "###"-level worked-example subsection: "###
Worked example: routing low-confidence predictions to human review with
Amazon A2I," nested inside Section 3 ("AWS tools for responsible AI")
right after its exam tip and before that section's mini-quiz. It walks a
hospital's patient-triage classifier through selecting a confidence
threshold with the Domain 1, Section 6 evaluation metrics (AUC-ROC,
precision/recall tradeoff), routing predictions below that threshold to
an Amazon A2I human review workflow, and configuring the A2I flow
definition, worker task template, and private workforce needed to keep
PHI-handling clinical review human-in-the-loop end to end.

Domain 2 also grew beyond a single worked example: alongside the
generative AI support assistant walkthrough referenced above, it now has
a second "## Worked example" section estimating tokens for RAG retrieval
and long-document summarization, a third section selecting and comparing
models for a real-time voice assistant use case, a fourth section tracing
all six Section 2 LLM lifecycle stages end-to-end for an insurance
claims-triage assistant, and a fifth (closing) section — "## Worked
example: Amazon Q Business vs. a custom Bedrock assistant for enterprise
customer support" — comparing per-user Amazon Q Business pricing against
on-demand Bedrock token cost, data-connector breadth, and customization
trade-offs for a 200-agent support team choosing between the two from
scratch — five standalone "## Worked example" sections in total for
Domain 2 as well.
Domain 5 also now has one nested worked-example subsection alongside its
closing HIPAA walkthrough: a "#### Worked example: capping cost under
three different threat models" subsection inside Section 1's cost-
governance material, applying Service Quotas and API Gateway usage plans
to three distinct threat models (malicious abuse, an accidental spike,
and a fixed budget ceiling).

Domain 5 also added a second standalone "## Worked example" section
tracing Northfield Genomics, a company running genetic-risk screening
clinics in both the US and EU, through a single deployment that must
satisfy GDPR, HIPAA, and the NIST AI RMF simultaneously across both
Amazon Bedrock and Amazon SageMaker — showing how a binding, region-
scoped law (GDPR or HIPAA) and a voluntary, global framework (the NIST
AI RMF) layer differently over the same two-service, two-region
architecture. Domain 5 therefore now has two standalone "## Worked
example" sections (the closing HIPAA walkthrough and this new
multi-framework example) plus the one nested cost-capping subsection
described above.

Domain 5 also has a second nested "####"-level worked-example subsection,
alongside the cost-capping one: "#### Worked example: shared
responsibility for a SageMaker-to-Bedrock fine-tuning pipeline," nested
inside Section 5 right after its exam tip and before that section's
mini-quiz. It walks Ferrous Analytics, a fintech company, through a
three-stage pipeline — SageMaker Processing for data prep, a Bedrock
fine-tuning job, and Bedrock Provisioned Throughput serving — assigning
customer-vs-AWS responsibility per stage, then contrasts a data-leak
incident traced back to the customer-owned anonymization code in stage 1
against AWS's own infrastructure responsibilities.

Domain 5 also has a third nested "####"-level worked-example subsection,
alongside the cost-capping and shared-responsibility ones: "#### Worked
example: data encryption vs. model encryption in a multi-region HIPAA
fine-tuning pipeline," nested inside Section 1 right after its exam tip
and before the PrivateLink section. It walks Meridian Health, a
healthcare company running clinics in `us-east-1` and `us-west-2`,
through a SageMaker-to-Bedrock fine-tuning pipeline in each Region,
distinguishing the customer managed KMS key encrypting the training
data at rest (and TLS in transit) from the separate customer managed
KMS key encrypting the resulting fine-tuned model artifact, and
explaining why both are independently required — one guards PHI
confidentiality, the other guards the model as intellectual property.

Domain 5 also has a fourth nested "####"-level worked-example
subsection, nested inside the cost-governance subsection right
after the cost-capping worked example: "#### Worked example: sizing service quotas for a multi-team
Bedrock workload". It walks through inventorying
per-team RPM/TPM demand, comparing it against the Service Quotas
console limit, requesting a sized increase, and setting AWS Budgets
alert thresholds as a proactive spend backstop, contrasting with the
reactive threat-model examples above it.

Domain 5 also has a fifth nested "####"-level worked-example
subsection: "#### Worked example: tracing provenance through a Titan
Image Generator watermarking pipeline," nested inside Section 1's
"Source citation and data lineage" subsection right after its exam
tip. It traces a photo-syndication company's Titan Image Generator G1
v2 pipeline from generation through Titan's built-in invisible
watermark embedding to a newsroom fact-checker's downstream detection
of that watermark, distinguishing this provenance mechanism from the
unrelated negative-prompting technique (covered in Domains 2–3) that
excludes a visible watermark/logo from an image's rendered content.

Domain 5 also has a sixth nested "####"-level worked-example
subsection: "#### Worked example: applying differential privacy to a
healthcare model-training pipeline," nested inside the "Common security
threats to AI systems and how to mitigate them" subsection right after
its exam tip and before that subsection's mini-quiz. It walks Meridian
Health Alliance, a hospital consortium, through applying DP-SGD-style
noise injection during SageMaker training to bound how much any single
patient's record can influence a readmission-risk model, weighing the
resulting privacy-budget/accuracy trade-off, and distinguishing that
training-time protection from the KMS-based encryption-at-rest control
covered earlier in the file.

Domain 5 also has a seventh nested "####"-level worked-example
subsection, nested inside the cost-governance subsection right after the
multi-team quota-sizing worked example: "#### Worked example: cost
optimization tradeoffs for a latency-critical chat workload vs. a batch
analytics pipeline." It contrasts a customer-facing chat assistant held
to a hard per-request latency SLA against an overnight batch
summarization pipeline held only to a completion-window target, showing
how the SLA target flips which combination of on-demand pricing,
Provisioned Throughput, Bedrock batch inference, and response caching
minimizes cost for each.

Domain 1 also has a second nested "###"-level worked-example subsection,
alongside the canary-deployment one: "### Worked example: estimating
training cost for the loan-default predictor: SageMaker managed spot
training vs. on-demand," nested inside Section 2 ("The ML development
lifecycle") right after its exam tip and before the "Production
deployment strategies and model versioning" subsection. It walks the same
bank's loan-default XGBoost model through picking a memory-appropriate
CPU training instance, checkpointing to S3 so Managed Spot Training
interruptions resume instead of restarting, and a full monthly cost
comparison between Managed Spot Training and On-Demand training —
distinguishing a routine, deadline-flexible retrain (Spot) from a
drift-triggered emergency retrain bound to a 24-hour compliance SLA
(On-Demand).

Counting every "## Worked example" heading plus the nested "###"/"####"
worked-example subsections called out above (Domain 1's training-cost-
estimation subsection; Domain 3's model-pair-comparison and
four-techniques-on-one-task subsections, its Kendra-GenAI-Index-as-a-
Bedrock-Knowledge-Base-data-source and QLoRA-quality-loss-threshold
subsections, its Cohere-Rerank-in-a-RAG-pipeline subsection, and its
BLEU/ROUGE-significance and evaluation-metric-picking subsections;
Domain 4's confidence-threshold/Amazon A2I and Clarify/Guardrails-layering
subsections;
Domain 5's cost-capping, data-encryption-vs-model-encryption,
multi-team quota-sizing, SageMaker-to-Bedrock shared-responsibility, Titan Image Generator
watermarking-provenance, differential-privacy healthcare-training, and
cost-optimization-SLA-tradeoffs subsections), the five domain guides mark **39
worked-example sections in total**: 3 in Domain 1, 5 in Domain 2, 15 in
Domain 3, 7 in Domain 4, and 9 in Domain 5, plus further example content
nested at the sub-bullet level within some of those sections.

Every depth gap previously flagged against this documentation is now
filled by one of those worked examples rather than left open: Amazon Q
Business coverage (Domain 2's closing "Amazon Q Business vs. a custom
Bedrock assistant" worked example), LoRA/QLoRA fine-tuning benchmarks
(Domain 3's "when does QLoRA's quality loss become unacceptable?"
subsection), Kendra-plus-Bedrock integration (Domain 3's
Kendra-GenAI-Index-as-a-Bedrock-Knowledge-Base-data-source subsection),
RAG troubleshooting (Domain 3's "troubleshooting a failing RAG system"
worked example), and layering SageMaker Clarify with Bedrock Guardrails
(Domain 4's Clarify/Guardrails-layering subsection).

**Diagrams:** The five domain guides contain 39 Mermaid flowchart diagrams
in total: Domain 1 has seven, Domain 2 has five, Domain 3 has sixteen,
Domain 4 has six, and Domain 5 has five. `cross-domain-concept-map.md`
adds two more Mermaid diagrams (the "Visual overview" section's
cross-domain flowchart, and the "Inference deployment pattern comparison"
section's decision-tree diagram comparing real-time, batch, serverless,
and provisioned-throughput inference), and
`aws-service-decision-guide.md` adds two further Mermaid diagrams of its
own (the Section 4.1 Bedrock model family selection decision flow, and
the Section 6 cost-control decision flow for Amazon API Gateway in front
of Bedrock/SageMaker endpoints), bringing the total to **43 Mermaid
diagrams** (39 in the domain guides + 2 in cross-domain-concept-map.md +
2 in aws-service-decision-guide.md).