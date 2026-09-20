# Domain 3 Fast Track: Applications of Foundation Models

**Condensed guide, split into 3 parts** · full guide: [`docs/domain-3-applications-of-foundation-models.md`](../domain-3-applications-of-foundation-models.md) (6,957 lines) · **Last verified:** 2026-09-06

## Why this fast track is split into three parts

Domain 3 (Applications of Foundation Models) is the exam's heaviest-weighted
domain — roughly **28% of scored questions** — and its full study guide runs
6,957 lines across 25 Mermaid diagrams and dozens of worked examples. That is
too long for a single condensed guide to stay easy to navigate end to end, so
the Fast Track splits it into three parts, one per major topic cluster:

| Part | Covers | Full guide sections |
|---|---|---|
| [Part 1: FM Application Design & Customization Methods](part-1-application-design-and-customization.md) | Design considerations for FM applications, multi-model routing and fallback strategies, prompt engineering techniques, RAG fundamentals, and all six customization methods (prompt engineering, RAG, fine-tuning, LoRA/QLoRA, RLHF, and continued pre-training) | Sections 1-4 |
| [Part 2: Inference Architecture & Multi-Modal Applications](part-2-inference-and-multimodal.md) | Amazon Bedrock's inference architecture (model access, Agents, Prompt Flows, Guardrails and prompt-injection prevention, cost governance, capacity decisions), vector databases and embeddings, multi-modal application patterns, and evaluating foundation model performance | Sections 5-7 |
| [Part 3: Production Deployment & Troubleshooting](part-3-deployment-and-troubleshooting.md) | AWS infrastructure for generative AI workloads, auto-scaling, inference failure triage, resilience patterns, and RAG-specific troubleshooting | Section 8 onward |

Each part keeps **every testable decision point** from its scope as compact
tables and decision trees instead of full worked-example narration, and every
section links back to the corresponding section of the full guide for the
complete scenario, worked examples, and mini-quizzes.

For the last 15-20 minutes before the exam, once all three parts are already
familiar and you just need the highest-yield tables refreshed one more time,
see [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) — a bullets-and-tables-only
cram sheet built on top of all three parts. For an even faster, interactive
scan of the same verified facts — jump links, collapsible sections per
topic, and a self-check checklist — see [`CHEAT-SHEET.md`](CHEAT-SHEET.md).
For active-recall/spaced-repetition practice (Anki, Quizlet, or similar),
see [`FLASHCARDS.md`](FLASHCARDS.md) — one deck covering all three parts,
plus a matching `flashcards.tsv` for direct import.

## How to use this fast track

Read this fast track the day before the exam, or any time you already know
the material and just need the tables refreshed; read the [full
guide](../domain-3-applications-of-foundation-models.md) first if any of
these terms are new to you. Work through the three parts in numeric order —
[Part 1](part-1-application-design-and-customization.md)'s customization
decision framework is assumed by [Part 2](part-2-inference-and-multimodal.md)'s
inference-architecture and evaluation material, which in turn underpins
[Part 3](part-3-deployment-and-troubleshooting.md)'s production-deployment
and troubleshooting content — though each part also links back to the full
guide independently, so you can jump straight to one part if you only need to
review that topic cluster. For the final cram before the exam, drop down to
[`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) once all three parts are
familiar.

## Table of contents

- [Part 1: FM Application Design & Customization Methods](part-1-application-design-and-customization.md) — Sections 1-4
- [Part 2: Inference Architecture & Multi-Modal Applications](part-2-inference-and-multimodal.md) — Sections 5-7
- [Part 3: Production Deployment & Troubleshooting](part-3-deployment-and-troubleshooting.md) — Section 8 onward
- [ULTRA-FAST-LEARN.md](ULTRA-FAST-LEARN.md) — bullets-and-tables-only cram sheet for the last 15-20 minutes before the exam
- [CHEAT-SHEET.md](CHEAT-SHEET.md) — interactive quick-scan cheat sheet: jump links, collapsible sections, and a self-check checklist
- [FLASHCARDS.md](FLASHCARDS.md) — active-recall/spaced-repetition flashcard deck (plus `flashcards.tsv` for Anki/Quizlet import)

## Where each section comes from

Combined index of all three parts' own front-matter tables, for jumping
straight to the full prose, worked examples, and mini-quizzes behind any
condensed table in any part:

| Part | This fast track | Full guide section | Approx. full-guide lines |
|---|---|---|---|
| 1 | 1. Design considerations for FM applications | [Section 1](../domain-3-applications-of-foundation-models.md#1-design-considerations-for-foundation-model-applications) | 98-353 |
| 1 | 2. Multi-model routing and fallback strategies | [Multi-model routing and fallback strategies](../domain-3-applications-of-foundation-models.md#multi-model-routing-and-fallback-strategies-routing-requests-to-the-right-model-at-request-time) | 354-682 |
| 1 | 3. Prompt engineering techniques | [Section 2](../domain-3-applications-of-foundation-models.md#2-prompt-engineering-techniques) | 684-945 |
| 1 | 4. RAG and Amazon Bedrock Knowledge Bases | [Section 3](../domain-3-applications-of-foundation-models.md#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases) | 947-1068 |
| 1 | 5. Customization decision framework | [Section 4](../domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering) | 1564-1705 |
| 1 | 6. Fine-tuning efficiency techniques | [Fine-tuning efficiency techniques](../domain-3-applications-of-foundation-models.md#fine-tuning-efficiency-techniques-full-fine-tuning-vs-lora-vs-qlora-vs-instruction-tuning) | 1706-2011 |
| 1 | 7. RLHF | [Reinforcement Learning from Human Feedback (RLHF)](../domain-3-applications-of-foundation-models.md#reinforcement-learning-from-human-feedback-rlhf-aligning-fine-tuned-models-to-human-preferences) | 2053-2129 |
| 1 | 8. Curating a fine-tuning dataset | [Curating a fine-tuning dataset](../domain-3-applications-of-foundation-models.md#curating-a-fine-tuning-dataset-size-thresholds-a-quality-checklist-and-synthetic-vs-real-data) | 2130-2284 |
| 2 | 1. Bedrock inference architecture: model access and orchestration | [Section 5](../domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features) | 2285-2502 |
| 2 | 2. Guardrails and prompt injection prevention | [Guardrails rule-type decision tree](../domain-3-applications-of-foundation-models.md#guardrails-rule-type-decision-tree-matching-the-use-case-to-the-right-filter) | 2355-2447 |
| 2 | 3. Cost governance and capacity decision guide | [Cost governance](../domain-3-applications-of-foundation-models.md#cost-governance-bounding-per-request-cost-with-max-tokens-and-provisioned-throughput) | 2503-2882 |
| 2 | 4. Vector databases and embeddings: choosing a backend | [Section 6](../domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval) and [Kendra GenAI Index worked example](../domain-3-applications-of-foundation-models.md#worked-example-building-a-product-knowledge-assistant-using-kendras-genai-index-as-a-bedrock-knowledge-base-data-source) | 2931-3018, 1208-1405 |
| 2 | 5. Choosing an embedding model | [Choosing an embedding model](../domain-3-applications-of-foundation-models.md#choosing-an-embedding-model-domain-specific-vs-general-vs-fine-tuned) | 3019-3101 |
| 2 | 6. Reranking and hybrid search | [Reranking and hybrid search](../domain-3-applications-of-foundation-models.md#reranking-and-hybrid-search-sharpening-vector-only-results) | 3102-3371 |
| 2 | 7. Multi-modal application patterns | [Multi-modal retrieval worked example](../domain-3-applications-of-foundation-models.md#worked-example-retrieval-patterns-for-a-multimodal-product-catalog-rag-system-text-images) and [token-budget worked example](../domain-3-applications-of-foundation-models.md#worked-example-budgeting-tokens-for-a-multimodal-financial-report-rag-pipeline-text-tables-images) | 1404-1562, 3372-3512 |
| 2 | 8. Retrieval quality metrics | [Retrieval quality metrics](../domain-3-applications-of-foundation-models.md#retrieval-quality-metrics-ndcg-map-recallk-and-mrr-a-selection-decision-guide) | 3513-3738 |
| 2 | 9. Evaluating foundation model performance | [Section 7](../domain-3-applications-of-foundation-models.md#7-evaluating-foundation-model-performance) | 3739-4223 |
| 3 | 1. AWS infrastructure for generative AI | [Section 8](../domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads) | 4224-4267 |
| 3 | 2. Bedrock throughput decision flow | [Section 8](../domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads) | 4268-4300 |
| 3 | 3. Auto-scaling decision guide | [SageMaker endpoint auto-scaling](../domain-3-applications-of-foundation-models.md#sagemaker-endpoint-auto-scaling-a-parameter-tuning-decision-guide) | 4301-4409 |
| 3 | 4. Inference failure triage (4 scenarios) | [Inference failures and recovery strategies](../domain-3-applications-of-foundation-models.md#inference-failures-and-recovery-strategies) | 4452-4878 |
| 3 | 5. Resilience patterns | [Inference error handling and resilience patterns](../domain-3-applications-of-foundation-models.md#inference-error-handling-and-resilience-patterns) | 4881-5113 |
| 3 | 6. RAG troubleshooting (4 failure modes) | [Worked example: troubleshooting a failing RAG system](../domain-3-applications-of-foundation-models.md#worked-example-troubleshooting-a-failing-rag-system) | 5190-5386 |
| 3 | 7. RAG symptom decision tree | [Decision tree: diagnosing RAG retrieval failures](../domain-3-applications-of-foundation-models.md#decision-tree-diagnosing-rag-retrieval-failures) | 5387-5421 |
| 3 | 8. Debugging method (stage isolation) | [Debugging method: isolating the broken pipeline stage](../domain-3-applications-of-foundation-models.md#debugging-method-isolating-the-broken-pipeline-stage) | 5423-5494 |

---

[← Back to the full Domain 3 guide](../domain-3-applications-of-foundation-models.md) · [Part 1: FM Application Design & Customization Methods →](part-1-application-design-and-customization.md)
