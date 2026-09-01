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
domain, currently 1,319–2,510 lines each:

- Domain 1: 1,319 lines
- Domain 2: 1,701 lines
- Domain 3: 2,510 lines
- Domain 4: 1,362 lines
- Domain 5: 1,418 lines

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
- `## Practice questions` (15–20 per domain, except **26 for Domain 5**,
  including exactly 2 multiple-response ["select TWO"] questions, for
  **106 domain practice questions in total** across the five domain
  guides) and a full `## Answer key` with justifications ruling out each
  wrong answer.

**Worked examples:** Domains 1, 2, 3, 4, and 5 each close with a dedicated
"## Worked example" section stitching the domain's concepts into one
end-to-end scenario: a loan-default predictor (D1), a generative AI
support assistant (D2), a RAG-based policy-lookup assistant (D3), auditing
and documenting a responsible e-commerce recommendation engine (D4), and a
HIPAA-regulated Bedrock application (D5).

**Diagrams:** All 24 flowchart-style diagrams across the guide are Mermaid flowchart
diagrams, not ASCII art: Domain 1 has six (the 8-stage ML lifecycle loop,
Section 2; decision trees for learning-type selection (Section 3),
use-case-to-service mapping (Section 4), purpose-built-vs-SageMaker
(Section 5), and metric selection (Section 6); and the
bias-variance trade-off spectrum, Section 7);
Domain 2 has four (including the transformer/self-attention
pipeline, Section 1); Domain 3 has eight (including the FM-customization
decision tree, Section 4, the vector store decision tree, Section 3, the
evaluation-approach (metric-selection) decision tree, Section 7, and
the D1-to-D3 inference-type decision tree, Section 8);
Domain 4 has three (including the bias
detection/mitigation workflow, Section 2); Domain 5 has three (covering the
KMS key lifecycle and data-security/encryption architecture, Section 1).
Two domains also carry separate plain-text ASCII notations for readers
without Mermaid rendering, which are not among the 21 flowcharts: Domain
1's AI ⊃ ML ⊃ DL ⊃ GenAI nesting notation (Section 1) and Domain 5's
shared-responsibility boundary diagram for Bedrock vs. SageMaker (Section
5).

**Test coverage:** `tests/test_domain_N_study_guide.py` for all five domains
validates required topic headings, AWS service mentions,
evaluation term coverage (D1), glossary size (≥15 entries), practice
question count (15–20 per domain, **26 for Domain 5**, **106 total**),
answer explanations (≥120 chars each, bolded answer letter), and sequential
numbering. Separate test files cover each domain's quick-reference cheat
sheet, its subsection mini quizzes (32 in total: 7 each for Domains 1 and
2, 8 for Domain 3, and 5 each for Domains 4 and 5), and its footer
breadcrumb navigation.

## Cross-domain support documents

Nine files in `docs/` exist to tie the five domain guides together instead
of duplicating material inside them:

- **`aws-service-index.md`** — a service-centric index: every AWS service
  referenced anywhere across the five guides, alphabetical, tagged by
  domain(s) `[D#, ...]` and linked to the discussing section. Currently
  indexes **79 services**, spanning letter sections A, C, G, I, M, P, and S
  (only the letters that have at least one referenced service), and
  includes standalone entries for every actively-referenced service, including Amazon API Gateway,
  Amazon Bedrock Prompt Management, Amazon Bedrock Prompt Flows, Amazon
  MSK, Amazon SageMaker Autopilot, Amazon SageMaker Model Monitor, and
  Amazon SageMaker RL (`tests/test_aws_service_index.py` guards all seven
  against regressing). Answers "where does this series mention Amazon
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
  features) in turn flow into Domain 4 and Domain 5.
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
  domains.
- **`master-glossary.md`** and **`GLOSSARY.md`** — two views of the same
  merged, alphabetical term set spanning all five domains' "Key terms"
  sections, **155 entries** each: `master-glossary.md` as a compact index
  with `[D#, ...]` domain tags per term, `GLOSSARY.md` as full backlinked
  prose entries. Both answer "where is 'prompt injection' explained?"
  without knowing which domain defines it.

**Total assessment:** 106 domain practice questions (across the five
domain guides) + 65 mock-exam questions + 22 scenario questions +
32 embedded mini-quiz questions (across the five domain guides'
subsections) = 225 total practice items across the repository.

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
2026-08-30` line near the top, kept in sync across the series;
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
