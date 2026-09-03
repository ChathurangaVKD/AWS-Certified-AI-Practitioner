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
domain, currently 1,583–3,502 lines each:

- Domain 1: 1,583 lines
- Domain 2: 1,993 lines
- Domain 3: 3,502 lines
- Domain 4: 1,879 lines
- Domain 5: 2,119 lines

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
  **24 for Domain 2**, and **26 for Domain 5** (Domain 3 and Domain 4 each
  have 20), including exactly 2 multiple-response ["select TWO"]
  questions, for **114 domain practice questions in total** across
  the five domain guides) and a full `## Answer key` with justifications
  ruling out each wrong answer.

**Worked examples:** Domains 1, 2, 3, 4, and 5 each close with a dedicated
"## Worked example" section stitching the domain's concepts into one
end-to-end scenario: a loan-default predictor (D1), a generative AI
support assistant (D2), a RAG-based policy-lookup assistant (D3), auditing
and documenting a responsible e-commerce recommendation engine (D4), and a
HIPAA-regulated Bedrock application (D5).

Domain 3 carries more worked examples than any other domain, so its count
needs its own methodology note: it has seven standalone "## Worked
example" sections in total (implementing RAG for a policy-lookup
assistant — the closing example referenced above — troubleshooting a
failing RAG system, selecting a foundation model under multiple competing
constraints, estimating a context-window token budget, estimating tokens
for long-document summarization, comparing monthly inference costs across
model tiers, and comparing fine-tuning against prompt engineering), plus
one additional worked example that is a subsection nested inside Section 7
rather than a standalone section ("### Worked example: is a 2-point
BLEU/ROUGE improvement statistically significant?"). Counting standalone
sections only, Domain 3 has seven worked examples; counting the nested
Section-7 subsection too, it has eight.

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
models for a real-time voice assistant use case, and a fourth (closing)
section tracing all six Section 2 LLM lifecycle stages end-to-end for an
insurance claims-triage assistant — four standalone "## Worked example"
sections in total for Domain 2 as well.
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

Domain 5 also has a third nested "####"-level worked-example
subsection: "#### Worked example: tracing provenance through a Titan
Image Generator watermarking pipeline," nested inside Section 1's
"Source citation and data lineage" subsection right after its exam
tip. It traces a photo-syndication company's Titan Image Generator G1
v2 pipeline from generation through Titan's built-in invisible
watermark embedding to a newsroom fact-checker's downstream detection
of that watermark, distinguishing this provenance mechanism from the
unrelated negative-prompting technique (covered in Domains 2–3) that
excludes a visible watermark/logo from an image's rendered content.

Counting every "## Worked example" heading plus the nested "###"/"####"
worked-example subsections called out above (Domain 3's
BLEU/ROUGE-significance and model-pair-comparison subsections, and its
four-techniques-on-one-task walkthrough; Domain 4's confidence-threshold/
Amazon A2I subsection; Domain 5's cost-capping, SageMaker-to-Bedrock
shared-responsibility, and Titan Image Generator watermarking-provenance
subsections), the five domain guides mark **27
worked-example sections in total**: 2 in Domain 1, 4 in Domain 2, 10 in
Domain 3, 6 in Domain 4, and 5 in Domain 5, plus further example content
nested at the sub-bullet level within some of those sections.

**Diagrams:** The five domain guides contain 35 Mermaid flowchart diagrams
in total: Domain 1 has seven (the 8-stage ML lifecycle loop,
Section 2; decision trees for learning-type selection (Section 3),
use-case-to-service mapping (Section 4), purpose-built-vs-SageMaker
(Section 5), and metric selection (Section 6); and the
bias-variance trade-off spectrum, Section 7);
Domain 2 has five (including the transformer/self-attention
pipeline, Section 1); Domain 3 has fourteen (including the
FM-customization and fine-tuning-efficiency trees, Section 4, the vector
store, embedding-model-selection, and reranking trees, Section 6, and
the RAG retrieval-failure and pipeline-stage-isolation trees);
Domain 4 has four (including the bias
detection/mitigation workflow, Section 2); Domain 5 has five (covering the
KMS key lifecycle and encryption architecture, Section 1, a compliance
decision matrix, Section 2, and a data-governance lifecycle diagram,
Section 4).
`cross-domain-concept-map.md` adds one more Mermaid diagram in its "Visual
overview" section, and `aws-service-decision-guide.md` adds two further
Mermaid diagrams of its own (the Section 4.1 Bedrock model family
selection decision flow, and the Section 6 cost-control decision flow for
Amazon API Gateway in front of Bedrock/SageMaker endpoints), bringing the
total to **38 Mermaid diagrams**. On top of those, 3 ASCII diagrams are
provided in plain text for readers without Mermaid rendering, duplicating
diagrams that already exist as Mermaid above rather than adding new
content: Domain 1's ML lifecycle diagram (Section 2), Domain 5's
data-governance lifecycle diagram (Section 4), and Domain 5's
shared-responsibility diagram (Section 5). In total: 35 Mermaid diagrams
in the domain guides + 1 in cross-domain-concept-map.md + 2 in
aws-service-decision-guide.md = 38 total Mermaid diagrams + 3 ASCII
diagrams = **41 total diagrams**.

**Test coverage:** `tests/test_domain_N_study_guide.py` for all five domains
validates required topic headings, AWS service mentions,
evaluation term coverage (D1), glossary size (≥15 entries), practice
question count (15–20 per domain, **24 for Domain 1**, **24 for Domain 2**,
**26 for Domain 5**, **114 total**),
answer explanations (≥120 chars each, bolded answer letter), and sequential
numbering. Separate test files cover each domain's quick-reference cheat
sheet, its subsection mini quizzes (35 in total: 7 each for Domains 1 and
2, 8 for Domain 3, 5 for Domain 4, and 8 for Domain 5), and its footer
breadcrumb navigation.

## Cross-domain support documents

Nine files in `docs/` exist to tie the five domain guides together instead
of duplicating material inside them:

- **`aws-service-index.md`** — a service-centric index: every AWS service
  referenced anywhere across the five guides, alphabetical, tagged by
  domain(s) `[D#, ...]` and linked to the discussing section. Currently
  indexes **82 services**, spanning letter sections A, C, G, I, M, P, and S
  (only the letters that have at least one referenced service), and
  includes standalone entries for every actively-referenced service, including Amazon API Gateway,
  Amazon Bedrock Prompt Management, Amazon Bedrock Prompt Flows, Amazon
  MSK, Amazon SageMaker Autopilot, Amazon SageMaker Model Monitor, and
  Amazon SageMaker RL (`tests/test_aws_service_index.py` guards all seven
  against regressing). A completeness audit against the [AWS Service
  Decision Guide](aws-service-decision-guide.md)'s consolidated service
  matrix and Bedrock model reference table added three more previously
  missing entries (Amazon Nova Sonic, Amazon Titan Text Embeddings, AWS
  Service Quotas) and documented, in the index's own completeness note,
  why several decision-guide-only Bedrock catalog model names are
  intentionally excluded. Answers "where does this series mention Amazon
  SageMaker?"
- **`aws-service-decision-guide.md`** — a consolidated quick reference
  sitting on top of each domain's own comparison table: a decision flow
  for SageMaker vs. Bedrock vs. purpose-built AI services, plus
  cross-domain comparison tables for security/compliance/governance
  services and encryption/privacy options. Answers "which service is the
  exam answer for this scenario?"
- **`cross-domain-concept-map.md`** — maps how Domain 1 fundamentals
  (e.g., model evaluation, the ML lifecycle, bias–variance) and Domain 2
  fundamentals (e.g., model selection criteria, prompt engineering) flow
  into Domain 3 foundation-model applications, Domain 4 responsible-AI
  concerns, and Domain 5 security/governance requirements — plus how
  Domain 3 application decisions (RAG, customization approach, Bedrock
  features) in turn flow into Domain 4 and Domain 5. Its `## Visual
  overview` section redraws that same prerequisite/dependency
  information as a Mermaid flowchart, so it is not text-and-tables-only.
- **`cross-domain-scenario-questions.md`** — 22 scenario questions that
  each require knowledge from two or more domains to answer (e.g., a
  Domain 3 customization method that also has to satisfy a Domain 5
  security requirement), tagged Beginner/Intermediate/Advanced like the
  domain guides' own questions.
- **`case-study-ai-system-lifecycle.md`** — a single deep end-to-end case
  study (Solstice Outdoors' "Trailhead" AI shopping assistant) tracing one
  company's AI system through all five domains over its lifetime, from a
  classical ML model through a deployed, governed generative AI product.
- **`exam-preparation-strategy.md`** — exam format and time-management
  guidance plus a day-by-day study plan (1-week/2-week/4-week schedules),
  including guidance to take the mock exam, identify your two weakest
  domains, and prioritize re-review before the exam.
- **`full-length-mock-exam.md`** — a 65-question, 90-minute mock exam
  weighted across all five domains in the real exam's proportions
  (~20%/24%/28%/14%/14%), mixed in exam-like order rather than grouped by
  domain, with a full answer key and a scoring guide for spotting weak
  domains. Five of the 65 questions (~8%) are multiple-response ("select
  TWO") items, matching the real exam's ~7-8% mix of multiple-response
  questions.
- **`master-glossary.md`** and **`GLOSSARY.md`** — two views of the same
  merged, alphabetical term set spanning all five domains' "Key terms"
  sections, **156 entries** each: `master-glossary.md` as a compact index
  with `[D#, ...]` domain tags per term, `GLOSSARY.md` as full backlinked
  prose entries. Both answer "where is 'prompt injection' explained?"
  without knowing which domain defines it.

**Total assessment:** 114 domain practice questions (across the five
domain guides) + 65 mock-exam questions + 22 scenario questions +
35 embedded mini-quiz questions (across the five domain guides'
subsections) = 236 total practice items across the repository.

## Navigation

**Cross-linking:** README.md links to all five domains via a table plus
prose pointers into every cross-domain support document above. Each domain
guide opens with a **breadcrumb** line (e.g. `[← Domain 1: Fundamentals of
AI and ML] · **Domain 2 of 5** · [Domain 3: Applications of Foundation
Models →]`) linking to the previous and next domain and signaling its
position in the five-domain sequence, and each domain file also carries
its own `## Table of contents` section linking to every numbered section
within it. `tests/test_domain_footer_navigation.py` and
`tests/test_cross_reference_links.py` guard, respectively, that every
domain guide's breadcrumb is present and that every internal link across
the guides (breadcrumbs, TOCs, glossary backlinks, and in-prose
cross-references) actually resolves to a real file and heading anchor.

**Discoverability:**
- `master-glossary.md` and `GLOSSARY.md` provide a master glossary index /
  keyword-to-domain mapping, each entry tagged with the domain(s) that
  define or use the term and linked to the relevant section.
- `aws-service-index.md` provides a service-centric index — every AWS
  service referenced anywhere across the five guides, tagged by domain and
  linked to the discussing section — and `aws-service-decision-guide.md`
  complements it by answering "which service is the exam answer for this
  scenario?"
- Each domain file has its own table of contents.
- `exam-preparation-strategy.md` includes day-by-day guidance to take the
  mock exam, identify your two weakest domains, and prioritize re-review
  of those domains before the exam.

**Navigation:**
- Linear reading order (D1 → D5) is signaled by each domain's breadcrumb
  (e.g. "Domain 3 of 5"), reducing the risk of learners jumping to D3 and
  missing D1 prerequisites.
- `exam-preparation-strategy.md` provides a full exam strategy and
  time-management guidance (Section 1: exam format and time management,
  plus a day-by-day study plan).
- `cross-domain-concept-map.md` and `master-glossary.md` make it
  straightforward to jump between related topics in different domains
  (e.g., "model evaluation in D1" vs. "FM evaluation in D3").
- `cross-domain-scenario-questions.md` sits alongside
  `cross-domain-concept-map.md`, `case-study-ai-system-lifecycle.md`,
  `exam-preparation-strategy.md`, `full-length-mock-exam.md`, and
  `aws-service-decision-guide.md` as the repo's cross-domain support
  material — the concept map explains *why* two domains connect, the
  scenario questions test whether you can *apply* that connection, the
  case study shows it playing out across a single system's lifetime, the
  mock exam and prep strategy rehearse it under exam conditions, and the
  decision guide resolves the AWS-service choice a cross-domain scenario
  usually turns on.

## Content health

**Staleness:** Content is kept current as AWS service names, capabilities
(Bedrock Knowledge Bases, Guardrails, Model Evaluation, Provisioned
Throughput), and terminology evolve, and is checked against public AWS
documentation. All five domain guides carry a `**Last verified:**
2026-09-02` line near the top, kept in sync across the series;
`tests/test_domain_last_verified_date.py` guards that every domain guide
keeps one and that the dates agree.

**Correctness:** No contradictions between domains or against AWS service
descriptions. Each section includes an "AWS example" (concrete scenario)
and an "Exam tip" (high-yield distractor or pitfall).

**Quality:** Practice questions are authentic exam style (scenario-based,
multiple-choice, clear distractors). Answer explanations are substantive
and rule out each wrong answer.

**Test coverage:** Beyond the per-domain and per-cross-domain-doc test
files, `tests/test_sonar_config.py` checks that `sonar-project.properties`
stays tuned for a documentation (markdown) repository rather than code,
and `tests/test_readme_study_plan.py` checks README.md's study-plan
guidance and links stay accurate.

**Consistency:** All five domains follow the same template (breadcrumb →
TOC → overview → numbered sections → comparison table → quick-reference
cheat sheet → glossary → worked example → practice questions → answer
key) and are validated structurally by their respective test files.