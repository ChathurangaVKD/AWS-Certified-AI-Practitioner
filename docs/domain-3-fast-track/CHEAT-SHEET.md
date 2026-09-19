# Domain 3 Cheat Sheet: Applications of Foundation Models

**Interactive quick-scan cheat sheet** · companion to the [Fast Track guide](README.md) and the [Ultra Fast Track cram sheet](ULTRA-FAST-LEARN.md) · full guide: [`docs/domain-3-applications-of-foundation-models.md`](../domain-3-applications-of-foundation-models.md)

Built for a 2-3 minute skim right before the exam — jump straight to the
topic you're weakest on, expand only that section, and tick off the
self-check checklist at the end. Domain 3 carries the **largest single
share of scored questions (~28%)**. Every fact here already lives in the
[Fast Track](README.md) and [Ultra Fast Track](ULTRA-FAST-LEARN.md); this
is a reformat for scannability, not new content.

## Table of contents

- [1. Customization trade-off table](#1-customization-trade-off-table-the-most-tested-decision)
- [2. Prompt engineering techniques at a glance](#2-prompt-engineering-techniques-at-a-glance)
- [3. Bedrock features checklist](#3-bedrock-features-checklist-keyword-feature)
- [4. Vector databases and embeddings](#4-vector-databases-and-embeddings-bullet-summary)
- [5. Evaluation-strategy table](#5-evaluation-strategy-table)
- [6. Infrastructure-scaling bullets](#6-infrastructure-scaling-bullets)
- [7. Prompt-injection prevention bullets](#7-prompt-injection-prevention-bullets)
- [8. RAG failure-mode triage](#8-rag-failure-mode-triage-compact)
- [Commonly confused pairs](#commonly-confused-pairs)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Self-check checklist](#self-check-checklist)

---

### 1. Customization trade-off table (the most-tested decision)

<details>
<summary>Prompt engineering vs. RAG vs. fine-tuning vs. continued pre-training · LoRA/QLoRA · RLHF · dataset size thresholds — tap to expand</summary>

| Approach | Changes weights? | Data required | Cost |
|---|---|---|---|
| **Prompt engineering** | No | None beyond the prompt itself | Lowest |
| **RAG** (Bedrock Knowledge Bases) | No | External knowledge source, no labeling | Low — no training job |
| **Fine-tuning** | Yes | **Labeled** input/output pairs | Higher — training job + usually provisioned throughput |
| **Continued pre-training** | Yes | Large volume of **unlabeled** domain text | Highest — most compute-intensive |

- "Frequently changing data," "reduce hallucination from our own docs" → **RAG**, not fine-tuning.
- **Labeled** pairs → fine-tuning. **Unlabeled** bulk text → continued pre-training — the fastest way to tell them apart.

**Fine-tuning efficiency techniques:**

| Technique | Parameters updated | Best fit |
|---|---|---|
| **Full fine-tuning** | 100% of weights | Max accuracy, safety/compliance-critical |
| **LoRA** (Low-Rank Adaptation) | **<1%** (small adapter matrices) | Mid-size GPU (**24GB+**) available |
| **QLoRA** (Quantized LoRA) | Same as LoRA, on a **4-bit** quantized base | Only a small GPU (**≤16GB**) |
| **Instruction tuning** | An *objective*, not a strategy — trains on (instruction, response) pairs | Varied instruction-following, layered on any of the above |

- **Merged** adapter serves at **~1.0x** full-fine-tuning latency; **unmerged** adds **~1.05-1.15x** (LoRA) or **~1.15-1.3x** (QLoRA) — QLoRA can't be both low-memory and low-latency at serving time.

**RLHF (layered on top of SFT):**

- Full fine-tuning, LoRA, QLoRA, and instruction tuning are all **supervised fine-tuning (SFT)**.
- **Three stages:** (1) SFT baseline policy; (2) train a **reward model** on human preference rankings; (3) fine-tune against the reward model via RL (commonly **PPO**).
- Open-ended chat needing human judgment of "which response is better" → **SFT, then layer RLHF**. Stale/missing knowledge → **RAG**, not RLHF — RLHF never changes *what* a model knows.

**Fine-tuning dataset size thresholds:**

| Technique / model scale | Recommended minimum labeled examples |
|---|---|
| LoRA/QLoRA, small-to-mid model (≤13B) | **~100-500** |
| LoRA/QLoRA, large model (34B+) | **~500-1,000** |
| Instruction tuning, any size | **~1,000-10,000+** |
| Full fine-tuning, small-to-mid model | **~1,000-10,000** |
| Full fine-tuning, large model (34B+) | **~10,000-100,000+** — risks **catastrophic forgetting** if underfed |
| Continued pre-training, any size | **Millions-billions** of unlabeled tokens |

- Fewer than **~50-100** examples per class/task usually signals **prompt engineering (few-shot)** or **RAG** instead of fine-tuning.
- **Data-quality checklist:** diversity · edge-case coverage · label correctness (**inter-annotator agreement**) · class/category balance.
- Safest pattern: **real data as the foundation**, synthetic only to fill specific gaps — never entirely synthetic for a high-stakes task.

</details>

### 2. Prompt engineering techniques at a glance

<details>
<summary>Zero-shot, few-shot, CoT, templates, negative prompting, chaining — tap to expand</summary>

| Technique | Changes weights? | Exam keywords |
|---|---|---|
| **Zero-shot** | No | "no examples," "simplest task" |
| **Few-shot** | No | "example input/output pairs," "consistent structure" |
| **Chain-of-thought (CoT)** | No | "step by step," "reasoning," "show your work" |
| **Prompt templates** | No | "reusable structure," "placeholders" |
| **Negative prompting** | No | "do not include," "avoid," "no watermark" |
| **Prompt chaining / Prompt Flows** | No | "sequence of prompts," "visual builder" |
| **System prompts / role prompting** | No | "persona," "role," "across the conversation" |
| **Prompt injection** *(not a technique — a security risk)* | N/A (attacker-controlled) | "ignore previous instructions" |

- If a table row reads "N/A"/"not a technique," that's **prompt injection** — the exam likes planting it in a technique list.

</details>

### 3. Bedrock features checklist (keyword → feature)

<details>
<summary>Agents, Guardrails, Knowledge Bases, Prompt Flows · Guardrails rule-type table — tap to expand</summary>

| If the scenario says... | The feature is... |
|---|---|
| "explicitly enable a model before calling it" | Model access |
| "take actions / call APIs / multi-step tasks" | **Agents** (action groups) |
| "block harmful, off-topic, or PII content" | **Guardrails** |
| "answer from our own documents, no retraining" | **Knowledge Bases** (RAG) |
| "visual builder, sequence of prompts" | **Prompt Flows** |
| "compare model quality objectively/at scale" | Automatic model evaluation |
| "judge subjective quality like tone/creativity" | Human evaluation |
| "guaranteed throughput, high/steady/predictable volume" | **Provisioned throughput** |
| "unpredictable/low/spiky volume, pay per use" | **On-demand** |

**Guardrails rule type → use case:**

| Use case | Rule type |
|---|---|
| Redact PII (names, SSNs, emails) | **Sensitive information filters** |
| Fixed list of exact strings | **Word filters** |
| Whole subject area regardless of phrasing | **Denied topics** |
| Standard harm category (hate, violence, **prompt injection**) | **Content filters** |
| Model contradicts/invents facts not in the source | **Contextual grounding checks** |

- **Guardrails** filters content — it does **not** retrieve knowledge or invoke APIs.

</details>

### 4. Vector databases and embeddings — bullet summary

<details>
<summary>OpenSearch vs. Aurora pgvector vs. Kendra · embedding model tiers — tap to expand</summary>

| Vector store | Pick for... |
|---|---|
| **Amazon OpenSearch (Service/Serverless)** | Native hybrid (vector + keyword) search, large scale, default for Bedrock Knowledge Bases |
| **Amazon Aurora (PostgreSQL) + `pgvector`** | "We already run Aurora/PostgreSQL," query embeddings with SQL |
| **Amazon Kendra** | No infra/embeddings pipeline to build, automatic relevance ranking; a Knowledge Base can reuse an existing **Kendra GenAI Index** |

**Embedding model tiers (pick in this order):**

1. **General-purpose** (Amazon Titan Text Embeddings, Cohere Embed) — default, cheapest.
2. **Domain-specific pretrained** — captures domain vocabulary, no training pipeline.
3. **Fine-tuned on your own data** — highest accuracy ceiling, highest cost.

- **Reranking** (cross-encoder) fixes "topically close but not the right chunk."
- **Hybrid search** (vector + keyword) surfaces exact-term matches (SKU codes, acronyms).

</details>

### 5. Evaluation-strategy table

<details>
<summary>Automatic vs. human vs. business metrics · MMLU/HumanEval/GSM8K · Recall@k/MRR/MAP/NDCG — tap to expand</summary>

| Layer | Measures | Use when... |
|---|---|---|
| **Automatic/benchmark evaluation** | Objective, formula-computable quality | Comparing many candidates quickly |
| **Human evaluation** | Subjective quality (tone, creativity) | Small candidate set, quality bar is the priority |
| **Business metrics** | Real-world outcome impact (CSAT, cost/interaction) | Post-launch, ongoing |

| Need | Metric | Direction |
|---|---|---|
| General knowledge/reasoning | MMLU | Higher is better |
| Code generation | HumanEval | Higher is better |
| Multi-step math | GSM8K | Higher is better |
| Is this output safe? | Toxicity scoring | **Lower** is better |
| Semantic similarity to a reference | BERTScore | Higher is better |
| Fluency independent of correctness | Perplexity | **Lower** is better |

**Retrieval quality metrics:**

| Metric | Use it when |
|---|---|
| **Recall@k** | Any top-*k* result counts as a win |
| **MRR** (Mean Reciprocal Rank) | Each query has essentially **one** correct/best answer |
| **MAP** (Mean Average Precision) | **Multiple** relevant, binary-labeled documents per query |
| **NDCG@k** | Relevance comes in **degrees** and result order matters |

- Compare scores to a **baseline** — a raw number in isolation is close to meaningless.
- BLEU/ROUGE penalize valid paraphrases; **BERTScore** recognizes a correctly-reworded answer.

</details>

### 6. Infrastructure-scaling bullets

<details>
<summary>Trainium vs. Inferentia · auto-scaling cooldown tuning by traffic shape — tap to expand</summary>

- **AWS Trainium** (EC2 Trn1/Trn2) → high-performance, cost-efficient **training** at scale.
- **AWS Inferentia** (EC2 Inf1/Inf2) → high-throughput, low-latency, cost-efficient **inference**.
- Both programmed via the **AWS Neuron SDK**.
- **Amazon SageMaker JumpStart** — pretrained FMs + templates, more hosting control than Bedrock's API.

**Auto-scaling cooldown tuning by traffic shape:**

| Traffic shape | Scale-out cooldown | Scale-in cooldown |
|---|---|---|
| Steady, predictable | Short (**~60s**) | Moderate (**~180-300s**) |
| Bursty / spiky | Short (**~60s**) | **Long (~600-900s)** |
| Periodic / scheduled | Layer a **scheduled scaling action** ahead of the known window | — |

- **Flapping** (scale out → in → out again quickly) = scale-in cooldown **too short**.
- Capacity never scales back down = **two conflicting target-tracking policies** attached.

</details>

### 7. Prompt-injection prevention bullets

<details>
<summary>Definition, mitigations, correct Guardrails rule type — tap to expand</summary>

- **Definition:** malicious user input designed to override the application's intended prompt/system instructions.
- **Not a customization technique** — it's a security risk to *mitigate*.
- **Primary mitigations:** input validation on user text; **Guardrails content filters** (the built-in ML classifier that catches prompt injection — not word filters, denied topics, or contextual grounding checks); clear separation of system instructions from user content.
- Inference parameters (temperature/top-p/top-k/max tokens) do **nothing** to stop prompt injection.

</details>

### 8. RAG failure-mode triage (compact)

<details>
<summary>6 symptoms → root cause → fix — tap to expand</summary>

| Symptom | Root cause | Fix |
|---|---|---|
| Answer correct but incomplete | Chunks too small / split across a boundary | Increase chunk size, add overlap |
| Retrieved chunks unrelated to topic | Embedding model mismatched to domain | Swap embeddings model, re-embed corpus |
| Chunks topically related but not the right answer | Vector similarity finds "close," not "correct" | Add reranking; add hybrid search |
| Retrieval returns nothing despite a clear answer existing | Query/document terminology mismatch | Rerank a wider set; rewrite the query (e.g., HyDE) |
| Assistant states facts not in any retrieved chunk | Retrieval returned no/thin relevant chunk | Verify a covering chunk exists; raise `numberOfResults`; require cited sources |
| Request fails with a context-length error | System prompt + chunks + history exceed the context window | Retrieve fewer/smaller chunks, trim history |

- Fine-tuning the FM fixes **none** of these — all six failure modes live in the retrieval half of the pipeline.

</details>

---

### Commonly confused pairs

<details>
<summary>9 pairs the exam loves to swap — tap to expand</summary>

| Pair | How to tell them apart |
|---|---|
| **Fine-tuning** vs. **Continued pre-training** | Fine-tuning = **labeled** pairs, narrow task; Continued pre-training = **unlabeled** bulk text, broad fluency |
| **LoRA** vs. **QLoRA** | LoRA = adapter matrices on a full-precision base; QLoRA = same, on a **4-bit quantized** base for the smallest GPU |
| **RLHF** vs. **SFT** | SFT trains against one "correct" labeled target; RLHF layers **reward-model-guided RL** on top of an SFT baseline |
| **RLHF** vs. **RAG** | RLHF fixes **how** a model responds; RAG fixes **what** it knows — RLHF never fixes stale/missing knowledge |
| **Recall@k** vs. **MRR** vs. **MAP** vs. **NDCG@k** | Recall@k = anywhere in top-*k*; MRR = one best answer, how early; MAP = multiple binary-relevant docs; NDCG@k = graded relevance |
| **On-demand** vs. **Provisioned throughput** | On-demand = pay-per-token, variable volume; Provisioned throughput = reserved capacity, steady/custom-model volume |
| **AWS Trainium** vs. **AWS Inferentia** | Trainium = **training** at scale; Inferentia = **inference** — cost-efficiency chips, not raw capability |
| **Guardrails** vs. **Knowledge Bases** vs. **Agents** | Guardrails filters content; Knowledge Bases retrieves (RAG); Agents take actions/call APIs |
| **Merged** vs. **unmerged** adapter | Merged = folded into base weights, ~1.0x latency; Unmerged = shared base across task adapters, adds a latency tax |

</details>

### Rapid-fire key terms

<details>
<summary>30 key terms — tap to expand</summary>

| Term | Definition |
|---|---|
| **Modality** | Input/output type(s) a model handles; multimodal = more than one |
| **Prompt injection** | Malicious input overriding intended prompt instructions |
| **Chunking** | Splitting documents into passages before embedding |
| **Embedding** | Numeric vector capturing semantic meaning |
| **Vector database** | Stores/queries embeddings by similarity (k-NN) |
| **Provisioned throughput** | Reserved Bedrock capacity (model units) for a commitment period |
| **On-demand** | Pay-per-token Bedrock pricing, no commitment |
| **Action group** | The APIs (often via Lambda) a Bedrock Agent invokes |
| **Reranking** | Cross-encoder re-scores an initial vector-search candidate set |
| **Hybrid search** | Vector (semantic) search combined with keyword search |
| **AWS Trainium** | Purpose-built chip for cost-efficient **training** (EC2 Trn1/Trn2) |
| **AWS Inferentia** | Purpose-built chip for cost-efficient **inference** (EC2 Inf1/Inf2) |
| **Retrieval Augmented Generation (RAG)** | Grounds FM answers in retrieved data, without retraining |
| **Fine-tuning** | Further training an FM's weights on labeled data |
| **Continued pre-training** | Further training on unlabeled domain-specific text |
| **Amazon Bedrock Knowledge Bases** | Bedrock's fully managed RAG feature |
| **Denied topics (Guardrails)** | Semantic block on an entire subject area |
| **Content filters (Guardrails)** | Built-in ML classifiers per harm category |
| **Business metric** | Outcome-oriented measure distinct from model-quality metrics |
| **Human evaluation** | People scoring FM outputs on subjective criteria |
| **Benchmark dataset** | Standardized dataset used to objectively score model quality |
| **Amazon SageMaker JumpStart** | Pretrained FM hub with more hosting control than Bedrock's API |
| **LoRA** | Fine-tuning technique training small low-rank adapter matrices (**<1%** of parameters) |
| **QLoRA** | LoRA on a base model quantized (e.g., **4-bit**) — lowest GPU memory |
| **Instruction tuning** | Objective training on (instruction, response) pairs |
| **RLHF** | Aligns an SFT model to human preferences via a reward model + RL (commonly PPO) |
| **Reward model** | Model trained on human preference rankings to predict a preference score |
| **Catastrophic forgetting** | A fine-tuned model losing previously learned general capability |
| **Early stopping** | Halting training once validation performance stops improving |
| **Inter-annotator agreement** | Measured consistency between human labelers |

</details>

---

## Self-check checklist

Tick each fact you can already state cold — anything unchecked is what to
re-read in the [Fast Track](README.md) or [Ultra Fast
Track](ULTRA-FAST-LEARN.md) before the exam.

- [ ] "Frequently changing data" / "ground in our own docs" → **RAG**, not fine-tuning.
- [ ] A fine-tuned or continued-pre-trained model almost always needs **provisioned throughput**.
- [ ] **Guardrails** filters content; it does **not** retrieve knowledge or invoke APIs.
- [ ] **Streaming** improves *perceived* latency only — not total generation time or cost.
- [ ] Labeled data → fine-tuning; unlabeled data → continued pre-training.
- [ ] **Prompt injection** shows up disguised as a "technique" in answer lists — it's always the security-risk distractor.
- [ ] Bursty traffic needs a **short scale-out** + **long scale-in** cooldown — not long on both sides.
- [ ] A raw benchmark score means nothing without a baseline; know which direction ("higher"/"lower") is better.
- [ ] All RAG failure modes live **before** the FM sees a prompt — fine-tuning the FM doesn't fix any of them.
- [ ] Reuse an existing **Kendra GenAI Index** as a Knowledge Base's retriever when one already exists.
- [ ] "Limited GPU budget, single GPU" → **QLoRA**; "faster/cheaper, small quality trade-off" → **LoRA**; "best accuracy, cost/time not the constraint" → **full fine-tuning**.
- [ ] **RLHF** fixes *how* a model responds — it never fixes stale or missing knowledge; that's **RAG**'s job.
- [ ] Fewer than **~50-100** labeled examples per class/task → prompt engineering or RAG, not a smaller fine-tune.
- [ ] Retrieval-metric picks: one correct/best answer → **MRR**; graded relevance → **NDCG@k**; binary, multiple relevant docs → **MAP**; only "somewhere in the top *k*" → **Recall@k**.

---

For the full explanations, worked examples, mini-quizzes, and practice
questions this cheat sheet intentionally omits, go back to the [Domain 3
fast track](README.md), the [Ultra Fast Track](ULTRA-FAST-LEARN.md), or
the [full Domain 3 guide](../domain-3-applications-of-foundation-models.md).

[← Back to the Domain 3 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md)
