# AWS Certified AI Practitioner (AIF-C01) Study Guide — Documentation Structure

## Overview

This documentation project is a comprehensive, exam-focused study guide series for the AWS Certified AI Practitioner (AIF-C01) certification. It serves learners preparing for the exam by breaking content into five domain-specific guides, each covering core concepts, AWS services, practice questions, and model answers. The material is designed for self-study and assumes no prior deep ML knowledge, pitching content at exam level rather than graduate-level depth. The guides are maintained automatically by gd-autopilot's discovery-to-review pipeline.

## Structure

The repository organizes material by **exam domain**, not by document type. Each domain is a self-contained, comprehensive guide that can be read independently but assumes the reader has seen Domains 1–2 before tackling 3–5 (per exam structure).

**Entry-point material:** `README.md` is the single index — a brief overview with a table linking the five domains, their exam weights (~20%, ~24%, ~28%, ~14%, ~14%), and file paths. It is purely navigational with no content.

**Topic subdirectories (by domain):** `docs/domain-N-fundamentals-of-*.md` — five markdown files (one per domain), currently 1,042–1,441 lines each (Domain 1: 1,118 lines; Domain 2: 1,344 lines; Domain 3: 1,441 lines; Domain 4: 1,232 lines; Domain 5: 1,042 lines) and following an identical template: domain overview, 5–8 major numbered sections (## 1, ## 2, …), a comparison/reference table, a key terms glossary (15–50 entries), 15–20 practice questions, and full answer key with justifications.

**Self-assessment material:** embedded in each domain file: practice questions (15–20 per domain, ~85 total) with detailed answer explanations ruling out distractors.

**Validation tests:** `tests/test_domain_N_study_guide.py` for Domains 1–4 only — structural checks (required topic headings, AWS services, glossary size, question counts, answer coverage). Domain 5 has no corresponding test file.

**Mermaid flowchart showing reader flow:**
```
README.md (index) → Domain 1 (fundamentals) → Domain 2 (GenAI) → Domain 3 (FM applications) → Domain 4 (responsible AI) → Domain 5 (security/governance)
Tests: D1–D4 have validation tests; D5 lacks test file
```

## Coverage

Five exam domains totaling 100% coverage:

1. **Domain 1 — Fundamentals of AI and ML (~20%):** AI/ML/DL nesting, ML lifecycle (8 stages from business goal to monitoring), learning types (supervised, unsupervised, reinforcement), AWS managed services (SageMaker, Rekognition, Comprehend, Forecast, Personalize, Transcribe, Polly, Translate, Lex, Textract, Fraud Detector), model evaluation metrics (confusion matrix, accuracy, precision, recall, F1, AUC-ROC, RMSE/MAE), overfitting/underfitting, bias–variance trade-off.

2. **Domain 2 — Fundamentals of Generative AI (~24%):** Generative AI definition, tokens, embeddings, vectors, semantic search, vector databases, transformer architecture, self-attention, foundation models, LLMs, multimodal models, LLM lifecycle (6 stages: scope → select → adapt → evaluate → deploy → monitor), GenAI advantages (adaptability, responsiveness, creativity, scalability) and disadvantages (hallucination, interpretability, inaccuracy, nondeterminism, cost), business use cases (content creation, summarization, chatbots, code generation, search), prompt engineering techniques (zero-shot, few-shot, chain-of-thought, negative prompting), inference parameters (temperature, top-p, top-k, max tokens), foundation model selection criteria (cost, modality, latency, context window, fine-tuning support), AWS services (Bedrock, Knowledge Bases, Agents, Guardrails, Model Evaluation, Titan, Provisioned Throughput, Amazon Q Business, Amazon Q Developer, SageMaker JumpStart, PartyRock).

3. **Domain 3 — Applications of Foundation Models (~28%):** FM application design (model selection, cost, latency, modality, customization options), prompt engineering techniques (in depth), RAG and Amazon Bedrock Knowledge Bases, customization spectrum (prompt engineering, RAG, fine-tuning, continued pre-training), Amazon Bedrock features (model access, Agents, Guardrails, Knowledge Bases, Model Evaluation, Provisioned Throughput), vector databases (Amazon OpenSearch, Aurora with pgvector, Amazon Kendra), embeddings, FM performance evaluation (automatic metrics, human evaluation, business metrics), AWS infrastructure (SageMaker, Trainium, Inferentia, Neuron SDK).

4. **Domain 4 — Guidelines for Responsible AI (~14%):** Responsible AI dimensions (fairness, explainability, privacy/security, transparency, veracity/robustness, governance, safety, controllability), bias in training data (sampling, measurement, label, historical, exclusion, aggregation bias), bias detection methods (DPL, disparate impact ratio), AWS tools (SageMaker Clarify, SageMaker Model Cards, AI Service Cards, Guardrails), legal/ethical considerations (IP rights, privacy, toxicity/bias, environmental impact), performance vs. interpretability trade-off.

5. **Domain 5 — Security, Compliance, and Governance for AI Solutions (~14%):** Securing AI systems (IAM roles/policies, least privilege, execution roles, encryption at rest/transit, KMS/CMKs, PrivateLink/VPC endpoints, source citation, data lineage), AWS compliance (AWS Artifact, GDPR, HIPAA/BAA), governance services (CloudTrail, Config, Audit Manager), data governance (data lifecycle, data residency, data monitoring with Macie/GuardDuty), shared responsibility model (AWS "of the cloud," customer "in the cloud").

**Cross-domain support materials:** Beyond the five domain guides, `docs/cross-domain-scenario-questions.md` (182 lines) supplies 12 scenario questions that each require knowledge from two or more domains (e.g., a Domain 3 customization choice that also satisfies a Domain 5 security requirement), tagged by difficulty (beginner/intermediate/advanced) like the domain guides' own questions. It sits alongside the repo's other cross-domain support material: `cross-domain-concept-map.md`, `case-study-ai-system-lifecycle.md`, `exam-preparation-strategy.md`, `full-length-mock-exam.md`, `aws-service-decision-guide.md`, and `master-glossary.md`.

**Structural gaps:** No integrated concept map showing how Domain 1 fundamentals (e.g., model evaluation) flow into Domain 3 applications or Domain 4 responsible AI concerns. No exam preparation guide, no quick-reference cheat sheet, no mock exam.

## Content Health

**Staleness:** All content appears current as of August 2026. AWS service names, capabilities (Bedrock Knowledge Bases, Guardrails, Model Evaluation, Provisioned Throughput), and terminology are accurate and align with public AWS documentation.

**Correctness:** No contradictions detected between domains or against AWS service descriptions. Each section includes an "AWS example" (concrete scenario) and an "Exam tip" (high-yield distractor or pitfall), both well-written and pedagogically sound.

**Quality:** Practice questions are authentic exam style (scenario-based, multiple-choice, clear distractors). Answer explanations are substantive and rule out each wrong answer. Comparison tables provide quick reference (e.g., "AWS managed AI/ML services at a glance" in D1, "AWS generative AI services" in D2).

**Diagrams:** Domain 1 has an ASCII diagram for the AI ⊃ ML ⊃ DL ⊃ GenAI hierarchy (Section 1) and for the 8-stage ML lifecycle loop (Section 2). Domain 2 has an ASCII diagram for the transformer/self-attention pipeline (Section 1). Domain 3 has an ASCII decision-tree diagram for FM customization approaches (Section 4). Domain 5 has an ASCII diagram of shared-responsibility boundaries for Bedrock vs. SageMaker (Section 5).

**Missing examples:** Each section has one "AWS example," but no deep end-to-end case study showing a single company's AI evolution through multiple domains. No code examples (appropriate for exam prep, but limits hands-on learning).

**Missing self-assessment:** No mock exam simulating real exam length/time. No answer analytics or topic-difficulty data.

**Test coverage gaps:** Domain 5 has no `test_domain_5_study_guide.py` file; Domains 1–4 do. Domain 5 glossary heading is "Key terms" instead of "Key terms glossary," creating inconsistency with D1–D4 and would fail any unified test.

## Navigation

**Cross-linking:** README.md links to all five domains via a simple table (minimal prose). Within each domain, sections reference one another via text mentions (not hyperlinks). No breadcrumb or "previous/next" navigation. Each domain file is standalone.

**Discoverability gaps:**
- No master glossary index or keyword-to-domain mapping (e.g., "where is 'prompt injection' explained?").
- No AWS service index or hyperlinked service references across domains.
- No table of contents within each 770+ line domain file.
- No "if you're weak on Domain X, prioritize these sections" guidance.

**Navigation issues:**
- Linear reading required (D1 → D5) but not signaled; learners may jump to D3 and miss D1 prerequisites.
- No progress tracker or completion checkpoint across domains.
- No exam strategy or time-management guidance.
- Difficult to jump between related topics in different domains (e.g., "model evaluation in D1" vs. "FM evaluation in D3").

---

## Additional findings

**Test coverage:** `test_domain_5_study_guide.py` is missing. Domains 1–4 validate: required topic headings, AWS service mentions, evaluation term coverage (D1 only), glossary size (≥15 entries), practice question count (15–20), answer explanations (≥120 chars each, bolded answer letter), sequential numbering. Domain 5 should have the same checks.

**Consistency:** All domains follow the same template (overview → sections → table → glossary → questions → answers), yet only Domains 1–4 are validated structurally. Domain 5's glossary heading divergence ("Key terms" vs. "Key terms glossary") breaks the pattern.

**sonar-project.properties:** Exists but unchecked for correctness by tests; verify it's tuned for documentation (markdown) rather than code.