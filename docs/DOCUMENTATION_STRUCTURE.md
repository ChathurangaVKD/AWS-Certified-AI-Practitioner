# AWS Certified AI Practitioner (AIF-C01) Study Guide — Documentation Structure

## Overview

This documentation project is a comprehensive, exam-focused study guide series for the AWS Certified AI Practitioner (AIF-C01) certification. It serves learners preparing for the exam by breaking content into five domain-specific guides, each covering core concepts, AWS services, practice questions, and model answers. The material is designed for self-study and assumes no prior deep ML knowledge, pitching content at exam level rather than graduate-level depth. The guides are maintained automatically by gd-autopilot's discovery-to-review pipeline.

## Structure

The repository organizes material by **exam domain**, not by document type. Each domain is a self-contained, comprehensive guide that can be read independently but assumes the reader has seen Domains 1–2 before tackling 3–5 (per exam structure).

**Entry-point material:** `README.md` is the single index — a brief overview with a table linking the five domains, their exam weights (~20%, ~24%, ~28%, ~14%, ~14%), and file paths. It is purely navigational with no content.

**Topic subdirectories (by domain):** `docs/domain-N-fundamentals-of-*.md` — five markdown files (one per domain), currently 1,118–1,766 lines each (Domain 1: 1,118 lines; Domain 2: 1,380 lines; Domain 3: 1,766 lines; Domain 4: 1,232 lines; Domain 5: 1,164 lines) and following an identical template: domain overview, 5–8 major numbered sections (## 1, ## 2, …), a comparison/reference table, a key terms glossary (15–50 entries), 15–20 practice questions (26 for Domain 5), and full answer key with justifications. Domain 3 also carries a condensed "Quick-reference cheat sheet" section (between the comparison table and the glossary) for last-minute exam review, distilling FM selection criteria, RAG architecture, the customization spectrum, and the Bedrock feature set into one page — the other four domains do not yet have an equivalent section.

**Self-assessment material:** embedded in each domain file: practice questions (15–20 per domain for Domains 1–4, 26 for Domain 5; 106 total) with detailed answer explanations ruling out distractors. Domain 5 is currently the only domain with multiple-response ("select TWO") questions — Q3 and Q14; every other domain uses single-answer multiple choice.

**Validation tests:** `tests/test_domain_N_study_guide.py` for all five domains — structural checks (required topic headings, AWS services, glossary size, question counts, answer coverage).

**Mermaid flowchart showing reader flow:**
```
README.md (index) → Domain 1 (fundamentals) → Domain 2 (GenAI) → Domain 3 (FM applications) → Domain 4 (responsible AI) → Domain 5 (security/governance)
Tests: D1–D5 all have validation tests
```

## Coverage

Five exam domains totaling 100% coverage:

1. **Domain 1 — Fundamentals of AI and ML (~20%):** AI/ML/DL nesting, ML lifecycle (8 stages from business goal to monitoring), learning types (supervised, unsupervised, reinforcement), AWS managed services (SageMaker, Rekognition, Comprehend, Forecast, Personalize, Transcribe, Polly, Translate, Lex, Textract, Fraud Detector), model evaluation metrics (confusion matrix, accuracy, precision, recall, F1, AUC-ROC, RMSE/MAE), overfitting/underfitting, bias–variance trade-off.

2. **Domain 2 — Fundamentals of Generative AI (~24%):** Generative AI definition, tokens, embeddings, vectors, semantic search, vector databases, transformer architecture, self-attention, foundation models, LLMs, multimodal models, LLM lifecycle (6 stages: scope → select → adapt → evaluate → deploy → monitor), GenAI advantages (adaptability, responsiveness, creativity, scalability) and disadvantages (hallucination, interpretability, inaccuracy, nondeterminism, cost), business use cases (content creation, summarization, chatbots, code generation, search), prompt engineering techniques (zero-shot, few-shot, chain-of-thought, negative prompting), inference parameters (temperature, top-p, top-k, max tokens), foundation model selection criteria (cost, modality, latency, context window, fine-tuning support), AWS services (Bedrock, Knowledge Bases, Agents, Guardrails, Model Evaluation, Titan, Provisioned Throughput, Amazon Q Business, Amazon Q Developer, SageMaker JumpStart, PartyRock).

3. **Domain 3 — Applications of Foundation Models (~28%):** FM application design (model selection, cost, latency, modality, customization options), prompt engineering techniques (in depth), RAG and Amazon Bedrock Knowledge Bases, customization spectrum (prompt engineering, RAG, fine-tuning, continued pre-training), Amazon Bedrock features (model access, Agents, Guardrails, Knowledge Bases, Model Evaluation, Provisioned Throughput), vector databases (Amazon OpenSearch, Aurora with pgvector, Amazon Kendra), embeddings, FM performance evaluation (automatic metrics, human evaluation, business metrics), AWS infrastructure (SageMaker, Trainium, Inferentia, Neuron SDK).

4. **Domain 4 — Guidelines for Responsible AI (~14%):** Responsible AI dimensions (fairness, explainability, privacy/security, transparency, veracity/robustness, governance, safety, controllability), bias in training data (sampling, measurement, label, historical, exclusion, aggregation bias), bias detection methods (DPL, disparate impact ratio), AWS tools (SageMaker Clarify, SageMaker Model Cards, AI Service Cards, Guardrails), legal/ethical considerations (IP rights, privacy, toxicity/bias, environmental impact), performance vs. interpretability trade-off.

5. **Domain 5 — Security, Compliance, and Governance for AI Solutions (~14%):** Securing AI systems (IAM roles/policies, least privilege, execution roles, encryption at rest/transit, KMS/CMKs, PrivateLink/VPC endpoints, source citation, data lineage), AWS compliance (AWS Artifact, GDPR, HIPAA/BAA), governance services (CloudTrail, Config, Audit Manager), data governance (data lifecycle, data residency, data monitoring with Macie/GuardDuty), shared responsibility model (AWS "of the cloud," customer "in the cloud").
**Cross-domain support materials:** Beyond the five domain guides, `docs/cross-domain-scenario-questions.md` (182 lines) supplies 12 scenario questions that each require knowledge from two or more domains (e.g., a Domain 3 customization choice that also satisfies a Domain 5 security requirement), tagged by difficulty (beginner/intermediate/advanced) like the domain guides' own questions. It sits alongside the repo's other cross-domain support material: `cross-domain-concept-map.md` (traces how Domain 1 fundamentals flow into Domains 3–5), `case-study-ai-system-lifecycle.md` (a single company's AI system followed through all five domains), `exam-preparation-strategy.md`, `full-length-mock-exam.md` (65 questions, weighted across all five domains), `aws-service-decision-guide.md`, `master-glossary.md`, `GLOSSARY.md`, and `aws-service-index.md`.

**Structural coverage:** `cross-domain-concept-map.md` shows how Domain 1 fundamentals (e.g., model evaluation) flow into Domain 3 applications and Domain 4 responsible AI concerns. `exam-preparation-strategy.md` provides an exam preparation guide with a day-by-day study plan, and `full-length-mock-exam.md` provides a full 65-question mock exam. `aws-service-decision-guide.md` serves as the quick-reference cheat sheet for choosing between similar AWS services.

## Content Health

**Staleness:** All content appears current as of August 2026. AWS service names, capabilities (Bedrock Knowledge Bases, Guardrails, Model Evaluation, Provisioned Throughput), and terminology are accurate and align with public AWS documentation.

**Correctness:** No contradictions detected between domains or against AWS service descriptions. Each section includes an "AWS example" (concrete scenario) and an "Exam tip" (high-yield distractor or pitfall), both well-written and pedagogically sound.

**Quality:** Practice questions are authentic exam style (scenario-based, multiple-choice, clear distractors). Answer explanations are substantive and rule out each wrong answer. Comparison tables provide quick reference (e.g., "AWS managed AI/ML services at a glance" in D1, "AWS generative AI services" in D2).

**Diagrams:** All 13 flowchart-style diagrams across the guide are Mermaid flowcharts, not ASCII art: Domain 1 has one (the 8-stage ML lifecycle loop, Section 2); Domain 2 has three (including the transformer/self-attention pipeline, Section 1); Domain 3 has three (including the FM-customization decision tree, Section 4); Domain 4 has three (including the bias detection/mitigation workflow, Section 2); Domain 5 has three (covering the KMS key lifecycle and data-security/encryption architecture, Section 1). Two domains also carry separate plain-text ASCII notations for readers without Mermaid rendering, which are not among the 13 flowcharts: Domain 1's AI ⊃ ML ⊃ DL ⊃ GenAI nesting notation (Section 1) and Domain 5's shared-responsibility boundary diagram for Bedrock vs. SageMaker (Section 5).

**Worked examples:** Domains 1, 2, 3, 4, and 5 each close with a dedicated "## Worked example" section stitching the domain's concepts into one end-to-end scenario: a loan-default predictor (D1), a generative AI support assistant (D2), a RAG-based policy-lookup assistant (D3), auditing and documenting a responsible e-commerce recommendation engine (D4), and a HIPAA-regulated Bedrock application (D5).

**Missing examples:** Each section has one "AWS example," and `case-study-ai-system-lifecycle.md` now provides a deep end-to-end case study (Solstice Outdoors' AI shopping assistant) showing a single company's AI evolution through all five domains. No code examples (appropriate for exam prep, but limits hands-on learning).

**Self-assessment:** `full-length-mock-exam.md` provides a 65-question mock exam simulating real exam length and time (90 minutes), weighted across all five domains, with a scoring guide for identifying weak domains from the results. No automated answer analytics or topic-difficulty data beyond that self-scoring guidance.

**Test coverage:** All five domains have a corresponding `test_domain_N_study_guide.py` file with consistent structural checks. Domain 5's glossary heading is "Key terms glossary," matching the convention used by D1–D4.

## Navigation

**Cross-linking:** README.md links to all five domains via a simple table (minimal prose). Each domain guide opens with a breadcrumb line (e.g. `[← Domain 1: Fundamentals of AI and ML] · **Domain 2 of 5** · [Domain 3: Applications of Foundation Models →]`) that links to the previous and next domain and signals its position in the five-domain sequence, and each domain file also carries its own `## Table of contents` section linking to every numbered section within it.

**Discoverability:**
- `master-glossary.md` and `GLOSSARY.md` provide a master glossary index / keyword-to-domain mapping (e.g., "where is 'prompt injection' explained?"), each entry tagged with the domain(s) that define or use the term and linked to the relevant section.
- `aws-service-index.md` provides a service-centric index — every AWS service referenced anywhere across the five guides, tagged by domain and linked to the discussing section — and `aws-service-decision-guide.md` complements it by answering "which service is the exam answer for this scenario?"
- Each domain file has its own table of contents.
- `exam-preparation-strategy.md` includes day-by-day guidance to take the mock exam, identify your two weakest domains, and prioritize re-review of those domains before the exam.

**Navigation:**
- Linear reading order (D1 → D5) is signaled by each domain's breadcrumb (e.g. "Domain 3 of 5"), reducing the risk of learners jumping to D3 and missing D1 prerequisites.
- `exam-preparation-strategy.md` provides a full exam strategy and time-management guidance (Section 1: exam format and time management, plus a day-by-day study plan).
- `cross-domain-concept-map.md` and `master-glossary.md` make it straightforward to jump between related topics in different domains (e.g., "model evaluation in D1" vs. "FM evaluation in D3").

---

## Additional findings

**Test coverage:** `test_domain_5_study_guide.py` exists alongside the other four domain test files. Domains 1–5 validate: required topic headings, AWS service mentions, evaluation term coverage (D1 only), glossary size (≥15 entries), practice question count (15–20 for Domains 1–4; 15–26 for Domain 5), answer explanations (≥120 chars each, bolded answer letter), sequential numbering.

**Consistency:** All domains follow the same template (overview → sections → table → glossary → questions → answers) and all five are validated structurally by their respective test files. Domain 5's glossary heading is "Key terms glossary," matching the convention used by D1–D4.

**sonar-project.properties:** Exists but unchecked for correctness by tests; verify it's tuned for documentation (markdown) rather than code.