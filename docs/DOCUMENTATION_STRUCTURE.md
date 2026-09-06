# Documentation Structure

This page is a map of how this repository is actually organized today: what
each file is for, how the five domain guides are put together internally,
what the ten cross-domain support documents add on top of them, and how
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
domain, currently 2,030–6,845 lines each, **16,191 lines total**:

- Domain 1: 2,030 lines
- Domain 2: 2,213 lines
- Domain 3: 6,845 lines
- Domain 4: 2,250 lines
- Domain 5: 2,853 lines

## Fast Track condensed guides (15 files, 7,424 lines total)

Beyond the five full domain guides, each domain also has a condensed
"Fast Track" layer under its own `docs/domain-N-fast-track/` directory.
Together with the full guide and the cram sheet nested inside that same
directory, this forms a three-tier structure for exam prep:

1. **Full guide** (`docs/domain-N-*.md`) — the complete domain guide, with
   every worked example, diagram, and practice question.
2. **Fast Track** (`docs/domain-N-fast-track/`) — a condensed rewrite of
   the same domain's content.
3. **Ultra Fast Learn** (`docs/domain-N-fast-track/ULTRA-FAST-LEARN.md`) —
   a further-condensed cram sheet built from the Fast Track material,
   meant for a final pass in the hours before the exam.

Domains 1, 2, and 4 each organize their Fast Track as a single pair of
files: `domain-N-fast-track/README.md` (the condensed guide itself) plus
`domain-N-fast-track/ULTRA-FAST-LEARN.md` (the cram sheet). Domains 3 and
5 are large enough that their condensed guide content is split into
multiple numbered parts instead of living entirely in one `README.md`:
Domain 3 into `part-1-application-design-and-customization.md`,
`part-2-inference-and-multimodal.md`, and
`part-3-deployment-and-troubleshooting.md`; Domain 5 into
`part-1-security-and-compliance.md` and
`part-2-governance-and-monitoring.md` — each still paired with its own
`ULTRA-FAST-LEARN.md`. Both domains still have a `README.md` in their
Fast Track directory, though, and it is still an integral, load-bearing
part of that domain's Fast Track layer: rather than holding the condensed
guide itself, it is a short landing page (88 lines for Domain 3, 81 for
Domain 5) that explains the split and links out to each part in reading
order, so `README.md` remains the entry point into every domain's Fast
Track layer even where the condensed content itself lives in numbered
parts.

Per domain, the Fast Track layer (condensed guide/parts plus cram sheet
combined) totals:

- Domain 1 Fast Track: 935 lines (`README.md` 743 + `ULTRA-FAST-LEARN.md` 192)
- Domain 2 Fast Track: 1,135 lines (`README.md` 851 + `ULTRA-FAST-LEARN.md` 284)
- Domain 3 Fast Track: 2,909 lines (`README.md` 88 + `part-1` 832 + `part-2` 784 +
  `part-3` 847 + `ULTRA-FAST-LEARN.md` 358)
- Domain 4 Fast Track: 954 lines (`README.md` 796 + `ULTRA-FAST-LEARN.md` 158)
- Domain 5 Fast Track: 1,491 lines (`README.md` 81 + `part-1` 698 + `part-2` 530 +
  `ULTRA-FAST-LEARN.md` 182)

That is 15 files (2 + 2 + 5 + 2 + 4) totaling **7,424 lines** across all
five domains. Every Fast Track guide and Ultra Fast Learn cram sheet
carries the same coverage guarantee: every testable concept the full
domain guide covers is retained somewhere in the condensed layer — only
narrative explanation, extra worked examples, and repetition are cut, not
exam-relevant content.

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
Bedrock Agent executing a multi-step task with tool calling), plus ten
further worked examples that are subsections nested at the "###" or
"####" level inside their enclosing numbered sections rather than
standalone sections: whether a 2-point BLEU/ROUGE improvement is
statistically significant ("### Worked example: is a 2-point BLEU/ROUGE
improvement statistically significant?"); two concrete model-pair
comparisons; the same task worked four different ways; building a
product-knowledge assistant using Kendra's GenAI Index as a Bedrock
Knowledge Base data source; retrieval patterns for a multimodal
product-catalog RAG system combining text and images; when QLoRA's
quality loss becomes unacceptable; when to use Cohere Rerank in a RAG
pipeline; budgeting tokens for a multimodal financial-report RAG
pipeline combining text, tables, and images; picking evaluation
metrics for a scenario; and running a Bedrock Model Evaluation job to
choose between candidate models. Counting standalone sections only,
Domain 3 has eight worked examples; counting the ten nested subsections
too, it has eighteen — more worked examples than any other domain guide.

Domain 4 similarly grew beyond a single worked example: alongside the
closing e-commerce recommendation-engine audit, it now has a second
standalone "## Worked example" section auditing a classical ML
small-business loan-approval classifier for proxy-variable bias, a third
diagnosing retrieval-induced bias and hallucination in a RAG-based HR
assistant, a fourth isolating the Section 5 performance/
interpretability tradeoff itself — a health-insurance prior-authorization
scenario where a regulatory explainability requirement forces the team off
a post-hoc-SHAP-on-a-black-box approach and onto a natively interpretable
model — and a fifth, "## Worked example: pairing a classical ML ranker
scored by SageMaker Clarify with a Bedrock FM protected by Guardrails,"
which contrasts with the nested Section 3 Clarify/Guardrails-layering
subsection described below: instead of layering both tools on one
fine-tuned foundation model across two lifecycle stages, it pairs a
classical ML ranking model (audited with Clarify) with a separate Bedrock
FM (filtered with Guardrails) as two distinct components in one
recommendation system — five standalone "## Worked example" sections in
total for Domain 4, covering bias-detection patterns across a deep
learning ranking model, a classical ML classifier, a foundation-model/RAG
application, a dedicated performance-versus-interpretability tradeoff
walkthrough, and a classical-ML-plus-foundation-model integration pattern.

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

Domain 5 also has an eighth nested "####"-level worked-example
subsection, nested inside the "Data monitoring" subsection right after
its exam tip and before that subsection's mini-quiz: "#### Worked
example: monitoring hallucination rate drift in a production RAG
assistant." It walks Aurora Benefits Co.'s Bedrock RAG assistant through
a hallucination rate that drifts from 2% at launch to 8% three months
later as its knowledge base goes stale, detecting and quantifying that
drift via an LLM-as-judge factual-consistency score published as a
custom CloudWatch metric, setting warning/paging alarm thresholds on it,
and remediating by refreshing and re-embedding the knowledge base rather
than retraining the model — contrasting this generative-AI-specific
monitoring approach with the classical accuracy/precision/recall drift
monitoring described earlier in the same subsection.

Domain 5 also has a ninth nested "####"-level worked-example subsection,
nested inside the "Common security threats to AI systems and how to
mitigate them" subsection right after the indirect-prompt-injection AWS
example and before the model-inversion/extraction AWS example: "#### Worked
example: indirect prompt injection via an untrusted document in a RAG
knowledge base." It walks a customer-support chatbot's Bedrock Knowledge
Base through ingesting an unmoderated customer-forum thread carrying a
hidden injection payload, an unrelated customer's query retrieving that
poisoned document, and the resulting leak — then contrasts Guardrails for
Amazon Bedrock's post-hoc, per-request input/output filtering (the
direct-injection mitigation) with the pre-ingestion data
validation/sanitization of untrusted source documents (plus Amazon Macie
for sensitive-data discovery) that indirect injection additionally
requires.

Domain 5 also has a tenth nested "####"-level worked-example subsection,
nested inside Section 2 ("AWS compliance standards relevant to AI
workloads") right after the "Compliance framework decision matrix"
subsection's exam tip and before Section 2's mini-quiz: "#### Worked
example: filling out a SageMaker Model Card for governance sign-off." It
completes the actual SageMaker Model Card for Domain 4's Meridian
Community Bank loan-approval classifier — model overview, intended use,
training data provenance, evaluation metrics, bias assessment results,
explainability, known limitations, human oversight controls, and
monitoring plan — flags which sections require the risk-governance
committee's formal sign-off versus a read-through, and walks through the
committee meeting where those sections are used to defend the deployment
decision.

Domain 5 also has an eleventh nested "####"-level worked-example
subsection, nested inside the "NIST AI Risk Management Framework (AI RMF)
— conceptual level" subsection right after its exam tip and before the
"GDPR, HIPAA, and the NIST AI RMF" mini-quiz: "#### Worked example:
applying NIST AI RMF to a multi-region Bedrock deployment." It walks
Solstice Mutual's Bedrock claims-summarization assistant, deployed
identically across `us-east-1` and `eu-west-1`, through all four NIST AI
RMF functions in implementation order: Map (SageMaker Model Cards and
Clarify pre-training bias reports inventorying each Region's model and
risks), Measure (a pre-launch Bedrock model evaluation job plus
per-Region Clarify and Model Monitor drift tracking), Manage (per-Region
Guardrails for Amazon Bedrock configurations and a Model-Registry-gated
fine-tuning approval pipeline), and Govern (cross-Region CloudTrail
API-call logging, AWS Config conformance packs, and an AWS Audit Manager
evidence package for board review).

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
Bedrock-Knowledge-Base-data-source, multimodal-product-catalog-retrieval,
and QLoRA-quality-loss-threshold subsections, its
Cohere-Rerank-in-a-RAG-pipeline and multimodal-financial-report-
token-budgeting subsections, and its BLEU/ROUGE-significance and
evaluation-metric-picking subsections;
Domain 4's confidence-threshold/Amazon A2I and Clarify/Guardrails-layering
subsections;
Domain 5's cost-capping, data-encryption-vs-model-encryption,
multi-team quota-sizing, SageMaker-to-Bedrock shared-responsibility, Titan Image Generator
watermarking-provenance, differential-privacy healthcare-training,
cost-optimization-SLA-tradeoffs, hallucination-rate-drift-monitoring,
indirect-prompt-injection-RAG-defense, Model-Card-governance-sign-off, and
NIST-AI-RMF-multi-region-Bedrock-deployment subsections), the five domain
guides mark **47
worked-example sections in total**: 3 in Domain 1, 5 in Domain 2, 18 in
Domain 3, 8 in Domain 4, and 13 in Domain 5, plus further example content
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

**Diagrams:** There are **98 total Mermaid diagrams** across the repository:
55 in the full domain guides and cross-domain materials, plus 43 in the
Fast Track condensed guides.

The 55 full-guide/cross-domain diagrams break down as: Domain 1 has seven,
Domain 2 has five, Domain 3 has twenty-five, Domain 4 has six, and Domain 5
has seven (50 diagrams across the five domain guides), plus
`cross-domain-concept-map.md` adds two more Mermaid diagrams (the "Visual
overview" section's cross-domain flowchart, and the "Inference deployment
pattern comparison" section's decision-tree diagram comparing real-time,
batch, serverless, and provisioned-throughput inference), and
`aws-service-decision-guide.md` adds three further Mermaid diagrams of its
own (the Section 4.1 Bedrock model family selection flow, the Section 6
cost-control flow, and the Section 1 layering-matrix request-path
diagram) — 50 + 2 + 3 = **55 Mermaid diagrams**.

The remaining 43 diagrams live in the Fast Track condensed guides, adapted
for condensed-format presentation and not duplicates of the 55 above: 6 in
Domain 1's Fast Track guide, 8 in Domain 2's, 4 in Domain 3's part 1, 8 in
Domain 3's part 2, 7 in Domain 3's part 3, 4 in Domain 4's, 4 in Domain 5
part 1, and 2 in Domain 5's part 2 (6 + 8 + 4 + 8 + 7 + 4 + 4 + 2 =
**43 Fast Track diagrams**), for a combined grand total of 55 + 43 =
**98 Mermaid diagrams** repository-wide.

**Quick-reference cheat sheets:** each of the five domain guides also
closes with its own `## Quick-reference cheat sheet` section — a
condensed, print-friendly recap of that guide's content for last-minute
review, distinct from the closing `## Worked example`/`## Practice
questions` sections that precede it: Domain 1: line 1524; Domain 2: line 1668;
Domain 3: line 6147; Domain 4: line 1746; Domain 5: line 2496.
Each one is validated by its own `tests/test_domain_N_quick_reference_cheat_sheet.py`
file (heading present, linked from the table of contents, and positioned
between the comparison table and the glossary link). These in-guide
cheat sheets serve the same last-minute-cram purpose as the Ultra Fast
Track cram sheets under `docs/domain-N-fast-track/ULTRA-FAST-LEARN.md` —
the difference is scope: the in-guide cheat sheet condenses its own
domain guide, while an Ultra Fast Track cram sheet is a separate,
standalone file condensing either the full guide or (Domains 1 and 4) an
intermediate Fast Track guide under `docs/domain-N-fast-track/README.md`.

## Cross-domain support documents: aws-service-index.md

**`aws-service-index.md`** indexes **83 services**, grouped under letter sections A, C, G, I, M, P, and S.
That figure counts one `- **Service**` bullet per row: each third-party
foundation model provider named in the domain guides (AI21 Labs,
Anthropic Claude, Cohere, Meta Llama, Mistral AI, Stability AI) counts as
a single row, not as one row per model it offers — so the count is
provider-level, not model-level.

## Cross-domain support documents: the rest

The remaining nine files under `docs/` round out the ten cross-domain
support documents named in the repository layout above. Each one is scoped
to a different way of reusing the five domain guides' content rather than
duplicating it:

**`aws-service-decision-guide.md`** is the inverse of `aws-service-index.md`:
instead of "everywhere this service is mentioned," it answers "which
service is the exam answer for this scenario?" It carries seven numbered
sections — a SageMaker-vs.-Bedrock-vs.-purpose-built-service decision flow,
comparison tables for security/compliance/governance services and for
encryption/privacy options, a Bedrock model reference, a consolidated
service matrix spanning all five domains, and dedicated decision guides for
Amazon API Gateway placement and for Bedrock Prompt Management vs. Prompt
Flows vs. direct prompting — plus the three Mermaid diagrams already
counted above (the Section 1 layering-matrix request-path diagram, the
Section 4.1 Bedrock model family selection flow, and the Section 6
cost-control flow).

**`cross-domain-concept-map.md`** traces how Domain 1 and Domain 2
fundamentals reappear, renamed or extended, in Domains 3–5 (and how Domain
3 decisions in turn feed Domains 4 and 5): six domain-to-domain sections
(D1→D3, D2→D3, D2→D4, D2→D5, D3→D4, D3→D5), a "Commonly confused concept
pairs" quick-reference table, and the two Mermaid diagrams already counted
above (the "Visual overview" cross-domain flowchart and the "Inference
deployment pattern comparison" decision tree).

**`cross-domain-scenario-questions.md`** carries 30 scenario questions,
each requiring concepts from 2 or more domains at once to answer — the
kind of blended scenario the actual exam favors over single-domain recall
— plus a full `## Answer key` explaining which domain each part of the
question draws on. Five of the 30 (questions 26–30) require 3+ domains.

**`case-study-ai-system-lifecycle.md`** follows one fictional company,
Solstice Outdoors, and one system, Trailhead, through all five domains in
the order a real team would build it: a classical ML model (Domain 1),
choosing and prompting a foundation model (Domain 2), designing and
customizing it with RAG and fine-tuning (Domain 3), finding and fixing a
bias problem (Domain 4), and securing and governing it before launch
(Domain 5) — one continuous narrative rather than five isolated worked
examples.

**`exam-preparation-strategy.md`** covers exam format and time management,
domain weights and high-yield focus areas, a recommended reading order,
common exam traps consolidated from every domain guide's "Exam tip"
callouts, 1-week/2-week/4-week study plans — including a dedicated
"Mini-quizzes: formative checks while you study" subsection explaining how
and when to use the 35 embedded mini-quizzes as in-the-moment, formative
self-checks, distinct from the summative domain practice questions,
cross-domain scenario questions, and mock exams covered elsewhere on the
page — and a topic-based review quick reference — the logistics layer
that sits on top of the five domain guides' content rather than teaching
new material itself.

**`full-length-mock-exam.md`** and **`mock-exam.md`** are two separate,
non-overlapping 65-question, 90-minute mock exams (130 mock-exam questions
combined) meant to be taken in sequence: `full-length-mock-exam.md` first,
`mock-exam.md` second as a fresh check once the first exam's questions are
no longer novel. Both follow the same shape — a "How to take this mock
exam" section, the 65 numbered questions, an answer key with explanations,
and a scoring-by-domain breakdown — so a wrong answer on either one points
straight back to the domain guide section it came from.

**`master-glossary.md`** and **`GLOSSARY.md`** are two views of the same
merged term set: `master-glossary.md` groups **157 entries** alphabetically
under "Jump to a letter" navigation, with each entry tagged
`[D#, ...]` for the domain guide(s) that define it, while `GLOSSARY.md`
presents the identical 157-term set as backlinked prose organized the same
way. Both files must be updated together whenever a term is added, renamed,
or retagged, which `tests/test_documentation_structure.py` enforces by
requiring their entry counts to match.

## Practice question and assessment inventory

Beyond the five domain guides' own `## Practice questions` sections (129
questions total, see above), the repository carries several other layers
of self-testing:

- **Subsection mini quizzes (35 in total across the five guides)**: 7 in
  Domain 1, 7 in Domain 2, 8 in Domain 3, 5 in Domain 4, and 8 in Domain 5,
  embedded as short "Mini-quiz" call-outs directly under the subsection
  they test, distinct from each domain's closing `## Practice questions`
  section.
- **Cross-domain scenario questions:** 30 questions in
  `cross-domain-scenario-questions.md`, each spanning 2 or more domains
  (5 of the 30 spanning 3 or more).
- **Mock exams:** 65 questions each in `full-length-mock-exam.md` and
  `mock-exam.md` (130 combined), simulating the real AIF-C01 format and
  timing.

**Total assessment:** 129 domain practice questions + 65 mock-exam questions +
30 scenario questions + 35 embedded mini-quiz questions =
259 total practice items across the repository (this excludes the second
65-question `mock-exam.md`, which is a second, independent practice pool
with a completely different set of questions—meant to be taken as a
follow-up rehearsal after re-studying weak domains from the first exam).

**Test coverage:** Every content claim in this file is enforced by a
matching test, not just asserted in prose:
`tests/test_domain_N_study_guide.py` for all five domains checks each
domain guide's structure — breadcrumb navigation, table of contents,
required section headings, and answer-key alignment — against its own
practice questions, for **129 total** domain practice questions verified
end to end. `tests/test_domain_N_subsection_mini_quizzes.py` and
`tests/test_domain_N_quick_reference_cheat_sheet.py` do the same for each
domain's mini quizzes and cheat sheet, and one dedicated test file exists
per cross-domain document (`test_cross_domain_scenario_questions.py`,
`test_full_length_mock_exam.py`, `test_mock_exam.py`,
`test_case_study_ai_system_lifecycle.py`,
`test_cross_domain_concept_map.py`, `test_aws_service_decision_guide.py`,
`test_aws_service_index.py`, `test_master_glossary.py`, `test_glossary.py`,
`test_exam_preparation_strategy.py`). `tests/test_cross_reference_links.py`
separately checks that every internal link and anchor across every file
resolves. `tests/test_documentation_structure.py` (this file's own test)
then re-derives every line count, worked-example count, diagram count,
question count, and glossary/service-index entry count directly from the
source files and asserts this document states them exactly, so the figures
above can't silently drift stale as the guides grow.

## Navigation

Every domain guide opens with a breadcrumb line (`[← Domain N-1 of 5](...)
· Domain N of 5 · [Domain N+1 of 5 →](...)`) linking to the previous and
next domain guide, plus a `## Table of contents` section linking every
numbered section within that file — checked by
`tests/test_domain_footer_navigation.py` for all five guides. The
cross-domain support documents link back into the domain guides with
inline links to specific sections (e.g.,
`domain-3-applications-of-foundation-models.md#2-rag`), and
`master-glossary.md`/`GLOSSARY.md` entries carry `[D#, ...]` tags naming
which domain guide(s) define each term, so a reader can always jump from a
term, a scenario question, or a mock-exam answer back to the source
material it was drawn from.

## Content health

All five domain guides carry a `**Last verified:**` line stamped with the
date their AWS-service and pricing claims were last re-checked against
current AWS documentation, enforced by
`tests/test_domain_last_verified_date.py`. `DOCUMENTATION_STRUCTURE.md`
itself does not carry a Last verified stamp; instead, its accuracy is
continuously enforced by `tests/test_documentation_structure.py`, which
re-derives every figure in this file from the underlying source files
rather than relying on a point-in-time human check.

## Complete file inventory

The repository's Markdown content is **33 files**: `README.md`; the five
domain guides (`domain-1-fundamentals-of-ai-and-ml.md` through
`domain-5-security-compliance-governance.md`); the 15 Fast Track condensed
guides across the five `docs/domain-N-fast-track/` directories, including
the Domain 3 and Domain 5 `README.md` landing pages (see "Fast Track
condensed guides" above); the ten cross-domain support documents
(`aws-service-index.md`, `aws-service-decision-guide.md`,
`cross-domain-concept-map.md`, `cross-domain-scenario-questions.md`,
`case-study-ai-system-lifecycle.md`, `exam-preparation-strategy.md`,
`full-length-mock-exam.md`, `mock-exam.md`, `master-glossary.md`, and
`GLOSSARY.md`); `study-progress-tracker.md`, a standalone checklist for
tracking progress through the study plan; and this file,
`DOCUMENTATION_STRUCTURE.md`. Every one of the seventeen non-Fast-Track
`docs/` files is reachable from `README.md`'s study plan within two clicks
(either linked directly, or linked from a domain guide's breadcrumb or
glossary that README.md itself links to).

Combined, the ten cross-domain support documents listed above total
**5,426 lines** (`aws-service-index.md`: 159; `aws-service-decision-guide.md`:
793; `cross-domain-concept-map.md`: 281; `cross-domain-scenario-questions.md`:
440; `case-study-ai-system-lifecycle.md`: 279; `exam-preparation-strategy.md`:
594; `full-length-mock-exam.md`: 1,263; `mock-exam.md`: 1,150;
`master-glossary.md`: 238; `GLOSSARY.md`: 229). The 15 Fast Track condensed
guides listed above (see "Fast Track condensed guides" section) add
**7,424 lines**, and `study-progress-tracker.md` adds a further **163
lines**. All thirty-three files together — `README.md`, the five domain
guides, the 15 Fast Track condensed guides, the ten cross-domain support
documents, `study-progress-tracker.md`, and this file — total
**29,967 lines**.

## Cross-linking architecture

The documents above are not independent files that happen to share a
`docs/` directory — they form a deliberate, four-layer cross-linking
system on top of the five domain guides' content:

1. **Glossary layer** (`master-glossary.md` / `GLOSSARY.md`): a flat,
   alphabetical index of every defined term, each tagged with the domain
   guide(s) it originates from. This is the "what does this word mean, and
   where is it explained in full?" entry point.
2. **Service index layer** (`aws-service-index.md`): a flat, alphabetical
   index of every AWS (and third-party model provider) service, each
   listing every domain guide section that mentions it. This is the
   "everywhere is this service discussed?" entry point — the mirror image
   of the glossary layer, organized by AWS service instead of by concept.
3. **Decision guide layer** (`aws-service-decision-guide.md`): a
   consolidated, cross-domain set of decision flows and comparison tables
   that sits above the domain guides' own per-domain tables. This is the
   "given a scenario, which service is the exam answer?" entry point —
   scenario-first rather than term-first or service-first.
4. **Concept map layer** (`cross-domain-concept-map.md`): explicit
   domain-to-domain links tracing how a Domain 1 or 2 fundamental
   reappears, renamed or extended, in Domains 3–5. This is the "why does
   this later domain keep saying 'recall from Domain 1...'?" entry point —
   relationship-first rather than lookup-first.

`cross-domain-scenario-questions.md` and `case-study-ai-system-lifecycle.md`
exercise all four layers at once (a single scenario or case-study phase
routinely needs a glossary term, a service lookup, a decision-guide
comparison, and a concept-map connection to answer fully), and
`exam-preparation-strategy.md` and the two mock exams sit on top of the
whole structure as the final rehearsal layer. A contributor adding new
content should ask, for each of the four layers: does this introduce a
term the glossary doesn't have yet, a service the index doesn't list yet,
a decision the guide doesn't cover yet, or a cross-domain connection the
concept map doesn't trace yet? `tests/test_cross_reference_links.py` then
verifies every link this architecture depends on actually resolves.