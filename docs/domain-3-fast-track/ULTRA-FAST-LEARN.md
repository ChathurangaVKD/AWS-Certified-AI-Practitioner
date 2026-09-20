# Domain 3 Ultra Fast Track: Applications of Foundation Models

**Ultra-condensed cram sheet** · full guide: [`docs/domain-3-applications-of-foundation-models.md`](../domain-3-applications-of-foundation-models.md) (6,957 lines) · **Last verified:** 2026-09-09

Bullets and tables only — no prose, no worked examples, no mini-quizzes.
For the last 15-20 minutes before the exam, once the full guide's own
[Quick-reference cheat sheet](../domain-3-applications-of-foundation-models.md#quick-reference-cheat-sheet)
is already familiar and you just need the highest-yield tables refreshed
one more time. Domain 3 carries the **largest single share of scored
questions (~28%)**. Every row below links back to the full guide section
it's drawn from.

## Table of contents

- [1. Customization trade-off table (the most-tested decision)](#1-customization-trade-off-table-the-most-tested-decision)
- [2. Prompt engineering techniques at a glance](#2-prompt-engineering-techniques-at-a-glance)
- [3. Bedrock features checklist (keyword → feature)](#3-bedrock-features-checklist-keyword-feature)
- [4. Vector databases and embeddings — bullet summary](#4-vector-databases-and-embeddings-bullet-summary)
- [5. Evaluation-strategy table](#5-evaluation-strategy-table)
- [6. Infrastructure-scaling bullets](#6-infrastructure-scaling-bullets)
- [7. Prompt-injection prevention bullets](#7-prompt-injection-prevention-bullets)
- [8. RAG failure-mode triage (compact)](#8-rag-failure-mode-triage-compact)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Common exam traps checklist](#common-exam-traps-checklist)
- [Where each row comes from](#where-each-row-comes-from)

---

## 1. Customization trade-off table (the most-tested decision)

| Approach | Changes model weights? | Data required | Latency | Cost | Flexibility / speed to iterate |
|---|---|---|---|---|---|
| **Prompt engineering** | No | None beyond the prompt itself | Lowest (no extra pipeline step) | Lowest | Highest — edit a prompt and redeploy instantly |
| **RAG** (Amazon Bedrock Knowledge Bases) | No | External knowledge source (documents), no labeling | Low, but retrieval adds a runtime hop vs. prompting alone | Low — no training job, pay for storage/retrieval + tokens | High — re-sync a data source; no retraining to refresh facts |
| **Fine-tuning** | Yes | Labeled input/output example pairs | Higher once served — often needs **provisioned throughput** | Higher — training job + usually reserved capacity | Lower — a new training job per behavior change |
| **Continued pre-training** | Yes | Large volume of **unlabeled** domain-specific text | Highest to produce; serving also often needs provisioned throughput | Highest — most compute-intensive, slowest | Lowest — heaviest, slowest approach to iterate on |

- [ ] As complexity/cost rises left → right, so does **how deeply the
      model is changed**: prompt engineering and RAG never touch
      weights; fine-tuning and continued pre-training both retrain and
      typically require **provisioned throughput** to serve.
- [ ] "Frequently changing data," "reduce hallucination from our own
      docs" → **RAG**, not fine-tuning.
- [ ] "Labeled" pairs → **fine-tuning** (narrow task/style/format).
      "Unlabeled" bulk text → **continued pre-training** (broad domain
      fluency/vocabulary). The labeled/unlabeled split is the fastest
      way to tell the two apart.
- [ ] "No data available, quick behavior/format tweak" → **prompt
      engineering**.

**Fine-tuning efficiency techniques — full fine-tuning vs. LoRA vs.
QLoRA vs. instruction tuning:**

| Technique | Parameters updated | Resource cost | Quality trade-off | Best fit |
|---|---|---|---|---|
| **Full fine-tuning** | 100% of weights | Highest — most GPU memory/time | Highest ceiling | Max accuracy, ample GPU budget, safety/compliance-critical |
| **LoRA** (Low-Rank Adaptation) | <1% (small adapter matrices injected into layers) | Low — much faster/cheaper | Modest, usually acceptable | Resource-constrained, mid-size GPU (24GB+) available |
| **QLoRA** (Quantized LoRA) | Same as LoRA, on a base model quantized (e.g., 4-bit) | Lowest — fits a single small GPU (16GB) | Small added loss vs. LoRA | GPU memory is the hard training constraint |
| **Instruction tuning** | An *objective*, not a parameter strategy — trains on (instruction, response) pairs, layered on any of the above | Depends on the underlying method | Improves general instruction-following | Varied instruction-following, not one fixed task |

- [ ] Decision order: safety/compliance-critical, or the quality floor
      allows less than ~1 point of degradation → **full fine-tuning**.
      Mid-size GPU (24GB+) available and a small quality gap is
      tolerable → **LoRA**. Only a small GPU (≤16GB) → **QLoRA** (accept
      the added quality loss, or escalate the GPU and use LoRA instead).
- [ ] **Merged vs. unmerged serving latency:** a **merged** adapter
      (folded into base weights after training) serves at ~1.0x
      full-fine-tuning latency — a QLoRA-merged model must first
      dequantize, losing its memory savings. An **unmerged** adapter
      (many task adapters sharing one base model) adds a latency tax:
      ~1.05-1.15x for LoRA, ~1.15-1.3x for QLoRA served quantized. QLoRA
      can't be both low-memory and low-latency at serving time — pick
      one.
- [ ] "Limited GPU budget / fine-tune a large model on a single GPU" →
      **QLoRA**. "Faster/cheaper, small quality trade-off, no
      quantization mentioned" → **LoRA**. "Best accuracy, cost/time
      isn't the constraint" → **full fine-tuning**. "Teach general
      instruction-following" (not one narrow task) → **instruction
      tuning**, layered on any of the three above.

**RLHF (Reinforcement Learning from Human Feedback) — aligning a
fine-tuned model to human preferences:**

- [ ] Full fine-tuning, LoRA, QLoRA, and instruction tuning are all
      **supervised fine-tuning (SFT)** — trained against one "correct"
      labeled target. RLHF is a distinct step layered *on top of* SFT.
- [ ] **Three stages:** (1) start from an **SFT** model as the baseline
      policy; (2) train a **reward model** on human preference
      rankings/comparisons of multiple outputs for the same prompt;
      (3) fine-tune the SFT model against the reward model via
      reinforcement learning (commonly **PPO**, Proximal Policy Optimization)
      without drifting so far it loses coherence.
- [ ] Narrow, well-defined labeled task, no ambiguity about "correct" →
      **SFT alone**. Open-ended chat/instruction-following where humans
      must judge *which response is better* (helpfulness, tone,
      honesty) → **SFT, then layer RLHF**. Stale or missing
      proprietary/current knowledge → **RAG**, not RLHF — RLHF only
      changes *how* a model responds, never *what* it knows.

**Curating a fine-tuning dataset — size thresholds, quality checklist,
synthetic vs. real:**

| Technique / model scale | Recommended minimum labeled examples |
|---|---|
| LoRA/QLoRA, small-to-mid model (≤13B), one task | ~100-500 |
| LoRA/QLoRA, large model (34B+), one task | ~500-1,000 |
| Instruction tuning, any size | ~1,000-10,000+ across many task types |
| Full fine-tuning, small-to-mid model, one task | ~1,000-10,000 |
| Full fine-tuning, large model (34B+), one task | ~10,000-100,000+ — risks **catastrophic forgetting** if underfed |
| Continued pre-training, any size | Millions-billions of unlabeled tokens |

- [ ] Fewer than ~50-100 examples per class/task usually signals the
      exam wants **prompt engineering (few-shot)** or **RAG** instead of
      fine-tuning, not a smaller fine-tune.
- [ ] Avoid **overfitting** on a small dataset: hold out a validation
      set and use **early stopping**; prefer LoRA/QLoRA over full
      fine-tuning (training fewer parameters is itself a regularizer).
- [ ] **Data-quality checklist** (size alone isn't sufficient):
      diversity (full range of production phrasings/lengths/formats/
      locales) · edge-case coverage (boundary/adversarial/minority
      cases deliberately included) · label correctness (real
      subject-matter review, measured **inter-annotator agreement**) ·
      class/category balance (corrected via oversampling/undersampling/
      loss weighting, not left as-is).
- [ ] **Synthetic vs. real data:** synthetic = cheap/fast, steerable for
      rare edge cases, but only as accurate as the generating model
      (propagates its errors/bias). Real = the foundation, especially
      for high-stakes behavior, reflects real-world ground truth. Safest
      pattern: real data as the foundation, synthetic to fill specific
      identified gaps — never entirely synthetic for a high-stakes task.

## 2. Prompt engineering techniques at a glance

| Technique | Changes weights? | Cost/complexity | Exam keywords |
|---|---|---|---|
| **Zero-shot** | No | Lowest — instruction only | "no examples," "simplest task" |
| **Few-shot** | No | Low — a few example pairs | "example input/output pairs," "consistent structure" |
| **Chain-of-thought (CoT)** | No | Low/medium — explicit step-by-step ask | "step by step," "reasoning," "show your work" |
| **Prompt templates** | No | Lowest — one-time authoring, reused | "reusable structure," "placeholders," "Bedrock Prompt Management" |
| **Negative prompting** | No | Lowest — one added constraint | "do not include," "avoid," "no watermark" |
| **Prompt chaining / Prompt Flows** | No | Medium/high — orchestrated sequence | "sequence of prompts," "visual builder," "output feeds next" |
| **System prompts / role prompting** | No | Lowest — one persistent block | "persona," "role," "across the conversation" |
| **Prompt injection** *(not a technique — a security risk)* | N/A (attacker-controlled) | N/A | "ignore previous instructions," "override the system prompt" |

- [ ] Multi-step arithmetic/logic → **chain-of-thought**. Inconsistent
      format/style across calls → **few-shot**. Unwanted elements in
      generated images → **negative prompting**. Reusable, versioned
      prompt across many calls → **prompt template**.
- [ ] If a table row reads "N/A"/"not a technique," that's **prompt
      injection** — the exam likes planting it in a technique list.

## 3. Bedrock features checklist (keyword → feature)

| If the scenario says... | The feature is... |
|---|---|
| "explicitly enable a model before calling it" | ☐ Model access |
| "take actions / call APIs / multi-step tasks, re-plan based on a tool result" | ☐ Agents (action groups) |
| "block harmful, off-topic, or PII content" | ☐ Guardrails |
| "answer from our own documents, no retraining" | ☐ Knowledge Bases (RAG) |
| "visual builder, sequence of prompts, output feeds next" | ☐ Prompt Flows |
| "compare model quality objectively/at scale" | ☐ Automatic model evaluation |
| "judge subjective quality like tone/creativity" | ☐ Human evaluation |
| "guaranteed throughput, high/steady/predictable volume, custom model" | ☐ Provisioned throughput |
| "unpredictable/low/spiky volume, pay per use" | ☐ On-demand |

**Guardrails rule type → use case (don't confuse these four):**

| Use case | Rule type | Why |
|---|---|---|
| Redact PII (names, SSNs, emails, phone/account numbers) | ☐ Sensitive information filters | Deterministic pattern match — no ML needed |
| Fixed list of exact strings (competitor names, profanity) | ☐ Word filters | Cheapest, lowest-latency — list fully known ahead of time |
| Whole subject area regardless of phrasing (e.g., "no medical advice") | ☐ Denied topics | Semantic match catches paraphrases a word list would miss |
| Standard harm category (hate, violence, sexual, **prompt injection**) | ☐ Content filters | Built-in ML classifiers per harm category |
| Model contradicts/invents facts not in the source | ☐ Contextual grounding checks | Only rule type that checks truthfulness vs. a source |

- [ ] **Guardrails** filters content — it does **not** retrieve
      knowledge or invoke APIs (that's Knowledge Bases / Agents).
- [ ] **On-demand vs. provisioned throughput** = the Domain 3 version of
      the Domain 1 real-time/batch inference-type decision: steady +
      high + predictable volume (or a custom model) → provisioned
      throughput; variable/spiky/low volume → on-demand.

## 4. Vector databases and embeddings — bullet summary

**Vector store options:**

- **Amazon OpenSearch (Service / Serverless)** — native hybrid
  (vector + keyword) search in one query; bring your own embedding
  model; horizontal/auto scaling. Pick for: "hybrid search," "large
  scale," "default vector store for Bedrock Knowledge Bases."
- **Amazon Aurora (PostgreSQL) + `pgvector`** — vectors as a column
  type, queried with SQL; bring your own embedding model. Pick for:
  "we already run Aurora/PostgreSQL," "query embeddings with SQL."
- **Amazon Kendra** — fully managed enterprise search; no embedding
  model to pick, ranking handled internally; connectors to S3,
  SharePoint, Salesforce. Pick for: "no infrastructure/embeddings
  pipeline to build," "automatic relevance ranking." A Knowledge Base
  can also reuse an existing **Kendra GenAI Index** as its retriever —
  the exam-favored answer when one already exists, over standing up a
  second index in OpenSearch/Aurora.

**Embedding model tiers (pick in this order):**

- ☐ **General-purpose** (Amazon Titan Text Embeddings, Cohere Embed) —
  default; zero extra training, cheapest, fastest to ship; struggles on
  dense specialized jargon (legal/medical/internal).
- ☐ **Domain-specific pretrained** (often third-party/open-source, not
  a Bedrock built-in) — captures domain vocabulary out of the box, no
  training pipeline; extra model to evaluate/license/host.
- ☐ **Fine-tuned on your own data** — trained on your labeled
  query/passage pairs; highest accuracy ceiling, highest cost; **not**
  a Bedrock-native fine-tuning workflow (typically Amazon SageMaker).

- [ ] Default to Titan/Cohere unless a scenario calls out a
      specialized domain **and** a retrieval-quality problem traceable
      to the embedding model (not chunking or the vector store).
- [ ] **Reranking** (cross-encoder re-scores a wider candidate set) fixes
      "topically close but not the right chunk" and query/document
      terminology mismatches — pure vector similarity alone can't.
- [ ] **Hybrid search** (vector + keyword) surfaces exact-term matches
      (SKU codes, names, acronyms) vector similarity alone would miss.

## 5. Evaluation-strategy table

| Layer | Measures | Speed/cost | Use when... |
|---|---|---|---|
| **Automatic/benchmark evaluation** | Objective, formula-computable quality (accuracy, F1, BLEU/ROUGE, toxicity) | Fast, cheap, reproducible at scale | Comparing many candidates quickly; screening before a costlier step |
| **Human evaluation** | Subjective quality (tone, creativity, nuance, cultural fit) | Slow, expensive | Small candidate set where the quality bar is the priority |
| **Business metrics** | Real-world outcome impact (CSAT, task completion, cost/interaction, escalation rate) | Post-launch, ongoing | Judging whether the app actually moved a business result — the only layer tied to org goals, not model quality |

**Metric-to-need matcher (higher/lower-is-better differs — don't mix these up):**

| Need | Metric | Direction |
|---|---|---|
| General knowledge/reasoning across subjects | MMLU | Higher is better |
| Science reasoning | ARC | Higher is better |
| Code generation (pass unit tests) | HumanEval | Higher is better |
| Multi-step math word problems | GSM8K | Higher is better |
| Is this output safe to show a user? | Toxicity scoring | **Lower** is better |
| Does output mean the same as a reference despite different wording? | BERTScore (semantic similarity) | Higher is better |
| How fluent/confident is the LM, independent of correctness? | Perplexity | **Lower** is better |

- [ ] Compare scores to a baseline (previous model, competing
      candidate) — a raw number in isolation ("MMLU: 68%") is close to
      meaningless.
- [ ] BLEU/ROUGE reward exact n-gram overlap and penalize valid
      paraphrases; **BERTScore** recognizes a correctly-reworded answer.
- [ ] No single metric tells the whole story — combine a
      correctness/reasoning metric + a similarity/quality metric +
      toxicity before shipping.
- [ ] Cheap/fast screening of many candidates on subjective criteria →
      automatic benchmark to shortlist, **then** human evaluation on
      finalists.

**Retrieval quality metrics — NDCG, MAP, Recall@k, MRR (ranking
quality, distinct from the automatic/human/business layers above):**

| Metric | What it measures | Use it when |
|---|---|---|
| **Recall@k** | Whether a relevant item appears anywhere in the top *k* | Any top-*k* result counts as a win — rank within the window doesn't matter |
| **MRR** (Mean Reciprocal Rank) | How early the *first* relevant result appears | Each query has essentially **one** correct/best answer |
| **MAP** (Mean Average Precision) | Precision averaged across every relevant item's rank | **Multiple** relevant, binary-labeled documents per query; finding all and ranking them both matter |
| **NDCG@k** | Ranking quality with **graded** (not binary) relevance | Relevance comes in degrees and result order matters (e.g., product search) |

- [ ] Decision order: only care whether a relevant result is somewhere
      in the top *k* → **Recall@k**. Order matters, usually one
      correct/best answer → **MRR**. Order matters, relevance is
      graded → **NDCG@k**. Order matters, binary relevance, multiple
      relevant docs → **MAP**.
- [ ] "Findable somewhere in the top 5" → **Recall@5**. "Single-answer
      FAQ bot's best answer should rank near #1" → **MRR**. "Rank the
      most relevant results highest" on a graded scale → **NDCG@k**.
      "Find all relevant documents, ranked as high as possible," binary
      labels → **MAP**.

## 6. Infrastructure-scaling bullets

**Purpose-built chips (memorize the mapping cold):**

- ☐ **AWS Trainium** (EC2 Trn1/Trn2) → high-performance, cost-efficient
  **training** at scale.
- ☐ **AWS Inferentia** (EC2 Inf1/Inf2) → high-throughput, low-latency,
  cost-efficient **inference**.
- ☐ Both programmed via the **AWS Neuron SDK**; both exist to beat
  general-purpose GPU cost at scale, not raw capability.
- ☐ **Amazon SageMaker JumpStart** — pretrained FMs + templates,
  deploy/fine-tune with more hosting control than Bedrock's managed
  API (specific instance type, or a model not on Bedrock).

**SageMaker real-time endpoint auto-scaling — the five knobs:**

- ☐ Target metric — `SageMakerVariantInvocationsPerInstance` (request
  volume) or CPU/GPU utilization (compute-bound workload).
- ☐ Target value — per-instance threshold that triggers scaling.
- ☐ Scale-out (scale-up) cooldown — wait before adding more capacity.
- ☐ Scale-in (scale-down) cooldown — wait before removing more capacity.
- ☐ MinCapacity / MaxCapacity — floor/ceiling on instance count.

**Cooldown tuning by traffic shape:**

| Traffic shape | Scale-out cooldown | Scale-in cooldown | Notes |
|---|---|---|---|
| Steady, predictable | Short (~60s) | Moderate (~180-300s) | Safe to be responsive on both sides — metric doesn't bounce unpredictably |
| Bursty / spiky | Short (~60s) | **Long (~600-900s)** | Scale out fast, scale in slow — prevents flapping; a longer scale-**in** cooldown does not mean a longer scale-**out** cooldown |
| Periodic / scheduled (known daily/weekly peaks) | — | — | Layer a **scheduled scaling action** raising MinCapacity ahead of the known window; don't rely on reactive scaling alone |
| Spike too large/fast for even a short scale-out cooldown | — | — | Raise MinCapacity as a standing buffer, or pre-warm with provisioned concurrency/throughput |

- [ ] **Flapping** (scale out → back in → out again quickly) = scale-in
      cooldown too short. Lengthen it.
- [ ] Capacity never scales back down = **two conflicting
      target-tracking policies** attached — scale-in needs *every*
      attached policy to agree.
- [ ] Throttles/timeouts at the *start* of a spike, then recovers =
      target-tracking threshold too close to real ceiling and/or
      scale-out cooldown too long — lower the threshold, shorten
      scale-out cooldown.
- [ ] MinCapacity/MaxCapacity sized off one historical peak, sitting at
      MaxCapacity during ordinary traffic = re-baseline off current
      steady-state, not the highest spike ever seen.

## 7. Prompt-injection prevention bullets

- ☐ **Definition:** malicious user input designed to override the
  application's intended prompt/system instructions ("ignore previous
  instructions," "reveal your system prompt").
- ☐ **Not a customization technique** — it's a security risk to
  *mitigate*, never something to intentionally "apply."
- ☐ **Primary mitigations:**
  - Input validation on user-supplied text before it reaches the prompt.
  - **Guardrails for Amazon Bedrock** — the standard harm category
    "prompt injection" is caught by **content filters** (built-in ML
    classifiers), not by word filters, denied topics, or contextual
    grounding checks.
  - Clear separation of system instructions from user-supplied content
    in the prompt structure (system prompts / role prompting).
- ☐ **Don't confuse the fix with the wrong Guardrails rule type:**
  sensitive information filters = PII; word filters = a fixed banned
  string list; denied topics = an entire semantic subject area;
  contextual grounding checks = factual consistency vs. a source. Only
  **content filters** cover the standard harm categories including
  prompt injection.
- ☐ Inference parameters (temperature/top-p/top-k/max tokens) do
  **nothing** to stop prompt injection — that's a content-policy
  problem, not a sampling problem.

## 8. RAG failure-mode triage (compact)

| Symptom | Root cause | Fix |
|---|---|---|
| Answer correct but incomplete, cuts off mid-explanation | Chunks too small / answer split across a chunk boundary | Increase chunk size, add chunk overlap, retrieve more chunks |
| Retrieved chunks unrelated to the query's topic entirely | Embedding model mismatched to the domain (jargon/abbreviations) | Swap to a better-suited embeddings model, re-embed corpus; expand jargon in source text |
| Retrieved chunks topically related but not the specific right answer | Vector similarity finds "close," not "correct" | Add reranking; add hybrid (keyword + vector) search |
| Retrieval returns nothing relevant despite a clearly-worded answer existing | Query/document terminology mismatch (casual question vs. formal statement) | Rerank a wider candidate set; rewrite the query before embedding (e.g., HyDE); index likely question phrasings alongside chunks |
| Assistant states facts not present in any retrieved chunk (hallucination) | Retrieval returned no/thin relevant chunk, so the FM fills the gap from parametric knowledge | Verify a covering chunk exists; raise `numberOfResults`; add "answer only from provided context"; require cited sources |
| Request fails/cuts off with a context-length / token-limit error | System prompt + chunks + history exceed the context window | Retrieve fewer/smaller chunks, lower `numberOfResults`, trim history, or use a larger-context model |

- [ ] Triage order for a live, underperforming RAG system: **hallucination
      → token-limit error → off-topic chunks (embedding model) →
      topically-close-but-wrong (reranking/hybrid) → correct-but-
      incomplete (chunking)**.
- [ ] Fine-tuning the FM fixes **none** of these — all six failure modes
      live in the retrieval half of the pipeline, before the FM ever
      sees a prompt.

---

## Rapid-fire key terms

- **Modality** — input/output type(s) a model handles (text, image,
  audio, video); multimodal = more than one.
- **Prompt injection** — malicious input overriding intended prompt
  instructions; mitigate via input validation + Guardrails content
  filters.
- **Chunking** — splitting documents into passages before embedding.
- **Embedding** — numeric vector capturing semantic meaning.
- **Vector database** — stores/queries embeddings by similarity (k-NN).
- **Provisioned throughput** — reserved Bedrock capacity (model units)
  for a commitment period; typically required for custom (fine-tuned)
  models.
- **On-demand** — pay-per-token Bedrock pricing, no commitment.
- **Action group** — the APIs (often via Lambda) a Bedrock Agent invokes.
- **Reranking** — cross-encoder re-scores an initial vector-search
  candidate set for relevance.
- **Hybrid search** — vector (semantic) search combined with
  keyword/full-text search in one query.
- **AWS Trainium** — purpose-built AWS chip for cost-efficient
  **training** at scale (EC2 Trn1/Trn2).
- **AWS Inferentia** — purpose-built AWS chip for cost-efficient
  **inference** (EC2 Inf1/Inf2).
- **Retrieval Augmented Generation (RAG)** — grounds FM answers in
  retrieved external data at inference time, without retraining.
- **Fine-tuning** — further training an FM's weights on labeled data
  for a specific task, style, or format.
- **Continued pre-training** — further training an FM on large volumes
  of unlabeled domain-specific text for broad domain fluency.
- **Amazon Bedrock Knowledge Bases** — Bedrock's fully managed RAG
  feature: automatic ingestion, chunking, embedding, and retrieval.
- **Denied topics (Guardrails)** — semantic block on an entire subject
  area regardless of phrasing.
- **Content filters (Guardrails)** — built-in ML classifiers per harm
  category (hate, violence, sexual, prompt injection).
- **Business metric** — outcome-oriented measure (CSAT, conversion
  rate, cost per interaction) distinct from model-quality metrics.
- **Human evaluation** — people scoring FM outputs on subjective
  criteria (tone, creativity) that automatic metrics can't capture.
- **Benchmark dataset** — standardized dataset used to objectively and
  reproducibly score and compare model quality.
- **Amazon SageMaker JumpStart** — hub of pretrained FMs and templates
  deployable/fine-tunable with more hosting control than Bedrock's API.
- **LoRA (Low-Rank Adaptation)** — fine-tuning technique that freezes
  the base model and trains small low-rank adapter matrices (often <1%
  of parameters).
- **QLoRA** — LoRA on a base model first quantized to a lower precision
  (e.g., 4-bit); lowest GPU memory of the parameter-efficient options.
- **Instruction tuning** — fine-tuning objective training on
  (instruction, response) pairs so a model follows instructions
  generally; layered on full fine-tuning, LoRA, or QLoRA.
- **RLHF (Reinforcement Learning from Human Feedback)** — aligns an SFT
  model to human preferences via a reward model and reinforcement
  learning (commonly PPO), layered on top of SFT.
- **Reward model** — model trained on human preference rankings to
  predict a scalar preference score, used to guide RLHF.
- **Catastrophic forgetting** — a fine-tuned model losing previously
  learned general capability; the risk of full fine-tuning a large
  model on too little data.
- **Early stopping** — halting training once validation performance
  stops improving, to avoid overfitting a small fine-tuning dataset.
- **Inter-annotator agreement** — measured consistency between human
  labelers, used to gauge fine-tuning label correctness.
- **NDCG (Normalized Discounted Cumulative Gain)** — retrieval
  ranking-quality metric for graded (non-binary) relevance.
- **MAP (Mean Average Precision)** — retrieval metric averaging
  precision across every relevant item's rank; multiple binary-labeled
  relevant documents per query.
- **MRR (Mean Reciprocal Rank)** — retrieval metric measuring how early
  the first relevant result appears; fits queries with one correct/best
  answer.
- **Recall@k** — retrieval metric measuring whether a relevant item
  appears anywhere in the top *k* results.

## Common exam traps checklist

- [ ] "Frequently changing data" / "ground in our own docs" →
      **RAG**, not fine-tuning.
- [ ] A fine-tuned or continued-pre-trained model almost always needs
      **provisioned throughput** — don't pick on-demand for a custom
      model under steady high load.
- [ ] **Guardrails** filters content; it does **not** retrieve knowledge
      or invoke APIs.
- [ ] **Streaming** improves *perceived* latency only — not total
      generation time or cost.
- [ ] Labeled data → fine-tuning; unlabeled data → continued
      pre-training — the fastest way to tell them apart.
- [ ] **Prompt injection** shows up disguised as a "technique" in
      answer lists — it's always the security-risk distractor.
- [ ] Bursty traffic needs a **short scale-out** + **long scale-in**
      cooldown — not long on both sides.
- [ ] A raw benchmark score means nothing without a baseline to compare
      against; know which direction ("higher"/"lower") is better for
      that specific metric.
- [ ] All four+ RAG failure modes (chunking, embedding, retrieval,
      terminology, hallucination, token overflow) live **before** the
      FM sees a prompt — fine-tuning the FM doesn't fix any of them.
- [ ] Reuse an existing **Kendra GenAI Index** as a Knowledge Base's
      retriever when one already exists, instead of standing up a
      second OpenSearch/Aurora index for the same content.
- [ ] "Limited GPU budget, single GPU" → **QLoRA**; "faster/cheaper,
      small quality trade-off, no quantization" → **LoRA**; "best
      accuracy, cost/time not the constraint" → **full fine-tuning**.
- [ ] **RLHF** fixes *how* a model responds (tone, helpfulness) — it
      never fixes stale or missing knowledge; that's **RAG**'s job, not
      RLHF's.
- [ ] Fewer than ~50-100 labeled examples per class/task → **prompt
      engineering (few-shot)** or **RAG**, not a smaller fine-tune.
- [ ] Retrieval-metric picks: one correct/best answer → **MRR**; graded
      relevance and order matters → **NDCG@k**; binary, multiple
      relevant docs, order matters → **MAP**; only "somewhere in the top
      *k*" matters → **Recall@k**.

---

## Where each row comes from

| This cram sheet | Full guide section |
|---|---|
| 1. Customization trade-off table | [Comparison table: customization approaches](../domain-3-applications-of-foundation-models.md#comparison-table-customization-approaches-for-foundation-model-applications) |
| 1a. Fine-tuning efficiency techniques (LoRA/QLoRA/instruction tuning) | [Fine-tuning efficiency techniques](../domain-3-applications-of-foundation-models.md#fine-tuning-efficiency-techniques-full-fine-tuning-vs-lora-vs-qlora-vs-instruction-tuning) |
| 1b. RLHF | [Reinforcement Learning from Human Feedback (RLHF)](../domain-3-applications-of-foundation-models.md#reinforcement-learning-from-human-feedback-rlhf-aligning-fine-tuned-models-to-human-preferences) |
| 1c. Fine-tuning dataset curation | [Curating a fine-tuning dataset](../domain-3-applications-of-foundation-models.md#curating-a-fine-tuning-dataset-size-thresholds-a-quality-checklist-and-synthetic-vs-real-data) |
| 2. Prompt engineering techniques | [Section 2](../domain-3-applications-of-foundation-models.md#2-prompt-engineering-techniques) + [comparison table](../domain-3-applications-of-foundation-models.md#comparison-table-prompt-engineering-techniques-at-a-glance) |
| 3. Bedrock features checklist | [Section 5](../domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features) + [Guardrails rule-type decision tree](../domain-3-applications-of-foundation-models.md#guardrails-rule-type-decision-tree-matching-the-use-case-to-the-right-filter) |
| 4. Vector databases and embeddings | [Vector store decision guide](../domain-3-applications-of-foundation-models.md#vector-store-decision-guide-opensearch-vs-aurora-pgvector-vs-amazon-kendra) + [Section 6](../domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval) + [embedding model selection](../domain-3-applications-of-foundation-models.md#choosing-an-embedding-model-domain-specific-vs-general-vs-fine-tuned) |
| 5. Evaluation-strategy table | [Section 7](../domain-3-applications-of-foundation-models.md#7-evaluating-foundation-model-performance) |
| 5a. Retrieval quality metrics (NDCG/MAP/Recall@k/MRR) | [Retrieval quality metrics](../domain-3-applications-of-foundation-models.md#retrieval-quality-metrics-ndcg-map-recallk-and-mrr-a-selection-decision-guide) |
| 6. Infrastructure-scaling bullets | [Section 8](../domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads) + [SageMaker auto-scaling decision guide](../domain-3-applications-of-foundation-models.md#sagemaker-endpoint-auto-scaling-a-parameter-tuning-decision-guide) |
| 7. Prompt-injection prevention | [Section 2](../domain-3-applications-of-foundation-models.md#2-prompt-engineering-techniques) + [Guardrails rule-type decision tree](../domain-3-applications-of-foundation-models.md#guardrails-rule-type-decision-tree-matching-the-use-case-to-the-right-filter) |
| 8. RAG failure-mode triage | [Worked example: troubleshooting a failing RAG system](../domain-3-applications-of-foundation-models.md#worked-example-troubleshooting-a-failing-rag-system) + [decision tree](../domain-3-applications-of-foundation-models.md#decision-tree-diagnosing-rag-retrieval-failures) |
| Rapid-fire key terms | [Key terms glossary](../domain-3-applications-of-foundation-models.md#key-terms-glossary) |

For the full explanations, worked examples, mini-quizzes, and practice
questions this cram sheet intentionally omits, go back to the
[full Domain 3 guide](../domain-3-applications-of-foundation-models.md).
For material spanning multiple domains, see
[`docs/cross-domain-concept-map.md`](../cross-domain-concept-map.md).

[← Back to the full Domain 3 guide](../domain-3-applications-of-foundation-models.md) · [Interactive cheat sheet →](CHEAT-SHEET.md)
