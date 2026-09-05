# Domain 3 Ultra Fast Track: Applications of Foundation Models

**Ultra-condensed cram sheet** · full guide: [`docs/domain-3-applications-of-foundation-models.md`](../domain-3-applications-of-foundation-models.md) (6,845 lines) · **Last verified:** 2026-09-05

Bullets and tables only — no prose, no worked examples, no mini-quizzes.
For the last 15-20 minutes before the exam, once the full guide's own
[Quick-reference cheat sheet](../domain-3-applications-of-foundation-models.md#quick-reference-cheat-sheet)
is already familiar and you just need the highest-yield tables refreshed
one more time. Domain 3 carries the single largest share of scored
questions (**~28%**). Every row below links back to the full guide
section it's drawn from.

## Table of contents

- [1. Six FM customization methods — trade-off table](#1-six-fm-customization-methods--trade-off-table)
- [2. Amazon Bedrock features checklist](#2-amazon-bedrock-features-checklist)
- [3. Vector databases — bullet summary](#3-vector-databases--bullet-summary)
- [4. Evaluation strategy comparison table](#4-evaluation-strategy-comparison-table)
- [5. Infrastructure scaling — bullets](#5-infrastructure-scaling--bullets)
- [6. Prompt-injection prevention — bullets](#6-prompt-injection-prevention--bullets)
- [7. RAG failure-mode triage list](#7-rag-failure-mode-triage-list)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Common exam traps checklist](#common-exam-traps-checklist)
- [Where each row comes from](#where-each-row-comes-from)

---

## 1. Six FM customization methods — trade-off table

| Method | Changes weights? | Data required | Relative training cost/time | Inference latency once deployed | Flexibility to update |
|---|---|---|---|---|---|
| **Prompt engineering** | No | None beyond the prompt itself | None — no training pipeline | Fastest — no retrieval step, no custom model | Highest — edit the prompt anytime, no retraining |
| **RAG** (Bedrock Knowledge Bases) | No | Unlabeled external documents, no labeling needed | None — only an ingest/index pipeline to build | Low-medium — the retrieval step adds runtime latency | High — update the source documents anytime, no retraining |
| **LoRA fine-tuning** | Yes — small low-rank adapter matrices (<1% of weights) | Labeled input/output pairs | Low — ~0.3-0.4x full fine-tuning's time; fits a single mid-size GPU | Same as the base model — served as a custom model, typically via **provisioned throughput** | Medium — retrain the small adapter to change behavior |
| **QLoRA fine-tuning** | Yes — LoRA adapters on a quantized (e.g., 4-bit) frozen base | Labeled input/output pairs | Lowest fine-tuning cost — fits a single small GPU, ~0.4-0.5x training time | Same as the base model — provisioned throughput | Medium — retrain the adapter; small added quality loss from quantization |
| **Full fine-tuning** | Yes — 100% of model weights | Labeled input/output pairs | Highest of the three fine-tuning options — full model copy, most GPU memory/time | Same as the base model — provisioned throughput | Low — a full training run is needed for every update |
| **Continued pre-training** | Yes — 100% of model weights | Large volume of unlabeled domain-specific text | Highest overall — most data- and compute-intensive, weeks or more | Same as the base model — provisioned throughput | Lowest — a large-scale retrain is needed to change domain fluency |

- **Cost/complexity climbs left to right:** prompt engineering → RAG →
  LoRA/QLoRA → full fine-tuning → continued pre-training. Prompt
  engineering and RAG never touch model weights; the other four all
  retrain the model and typically require **provisioned throughput** to
  serve the resulting custom model.
- **Labeled vs. unlabeled is the fastest tell:** fine-tuning (any
  variant) needs **labeled** input/output pairs; continued pre-training
  needs only **unlabeled** domain text.
- "Latest product catalog / frequently changing facts" → **RAG**, not
  fine-tuning. "Exact required format/tone, have labeled examples" →
  **fine-tuning**. "Limited GPU budget, single small GPU" → **QLoRA**.
  "Best possible accuracy, cost isn't the constraint" → **full
  fine-tuning**. "Broader domain vocabulary from unlabeled text" →
  **continued pre-training**.

## 2. Amazon Bedrock features checklist

- [ ] **Model access** — must be explicitly requested per model in the
      Bedrock console before it can be invoked.
- [ ] **Amazon Bedrock Agents** — plans multi-step tasks and invokes
      **action groups** (APIs, typically via AWS Lambda) and Knowledge
      Bases in a reasoning-and-acting loop (plan → invoke tool → observe
      → continue).
- [ ] **Guardrails for Amazon Bedrock** — configurable safety layer with
      five rule types: denied topics, content filters, word filters,
      sensitive information (PII) filters, contextual grounding checks.
- [ ] **Amazon Bedrock Knowledge Bases** — the managed RAG feature:
      automatic ingestion, chunking, embedding, and retrieval over your
      own data via `Retrieve` / `RetrieveAndGenerate`.
- [ ] **Automatic model evaluation** — built-in metrics (accuracy,
      robustness, toxicity) against built-in or custom prompt datasets —
      fast, cheap, objective.
- [ ] **Human evaluation** — a human work team (your own, or
      AWS-managed) scores subjective criteria (tone, style, relevance)
      automatic metrics can't capture.
- [ ] **Provisioned throughput** — dedicated capacity in **model
      units**, 1- or 6-month commitment; required for most custom
      (fine-tuned/continued-pre-trained) models; cost-effective only for
      **high, steady, predictable** volume.
- [ ] **On-demand** — pay per token, no commitment; fits variable,
      spiky, or low-volume traffic.

**Guardrails rule-type lookup:**

| Use case | Rule type | How it matches |
|---|---|---|
| Detect/redact PII (names, SSNs, emails, account numbers) | Sensitive information filters | Built-in PII entity recognizers, or custom regex |
| Block a known fixed list of strings (competitor names, profanity) | Word filters | Exact string/pattern match |
| Block an entire subject area regardless of phrasing (e.g., "no medical advice") | Denied topics | Semantic match against a topic description |
| Standard harmful-content categories (hate, insults, sexual, violence, misconduct, **prompt injection**) | Content filters | Built-in ML classifiers, configurable strength |
| Block claims the supplied source doesn't support (reduce hallucination) | Contextual grounding checks | Compares the response against source content |

- Match the keyword to the feature: "take actions / call APIs" →
  **Agents**; "block harmful/off-topic content" → **Guardrails**;
  "answer from our own documents" → **Knowledge Bases**; "compare model
  quality objectively at scale" → **automatic evaluation**; "judge tone
  or creativity" → **human evaluation**; "guaranteed throughput at high
  steady volume" → **provisioned throughput**; "unpredictable/spiky
  volume, pay per use" → **on-demand**.
- **Guardrails filters content — it does not retrieve knowledge or
  invoke APIs.** Don't confuse it with Knowledge Bases or Agents.

## 3. Vector databases — bullet summary

- **Embedding** — a numeric vector capturing semantic meaning; similar
  meanings land close together in vector space, even with no shared
  words.
- **Vector database** — stores embeddings and runs **similarity search**
  (k-NN, cosine/Euclidean distance) to find vectors closest to a query
  vector — the retrieval half of RAG and the mechanism behind
  **semantic search**.
- **Amazon OpenSearch Service / OpenSearch Serverless** — built-in
  vector engine plus traditional keyword/full-text search in one query
  (**hybrid search**); a common Bedrock Knowledge Bases vector store.
- **Amazon Aurora (PostgreSQL) or Amazon RDS for PostgreSQL +
  `pgvector`** — stores vectors as a column type inside a relational
  database, queried with SQL; fits a team already standardized on
  PostgreSQL. Aurora fits auto-scaling storage/read-replica/high-scale
  needs; RDS fits smaller, steady workloads.
- **Amazon Kendra** — a fully managed, ML-powered **enterprise search**
  service, not a general-purpose vector database — it handles
  embedding, ranking, and relevance internally. Right choice for
  "natural-language search over existing document repos" with zero
  embeddings pipeline to build; Bedrock Knowledge Bases can also use an
  existing **Amazon Kendra GenAI Index** as a retriever.
- **Embeddings models:** Amazon Titan Text Embeddings, Cohere Embed on
  Bedrock — convert raw content into vectors; a domain-specific or
  fine-tuned embedding model is needed when a general-purpose model
  embeds jargon/abbreviations near unrelated concepts.
- **Decision heuristic:** "manage your own embeddings + similarity
  index" → **vector database** (OpenSearch, or Aurora/RDS + pgvector).
  "Search existing enterprise documents in natural language, no
  embeddings pipeline" → **Amazon Kendra**. "Already on RDS/Aurora and
  also need keyword + vector fused in one query" → **OpenSearch**
  regardless of the existing relational database.

## 4. Evaluation strategy comparison table

| Evaluation layer | Measures | Method | Use when |
|---|---|---|---|
| **Business metrics** | Real-world outcome impact (task completion rate, CSAT, cost per interaction, escalation rate) | Track after launch | The question is about whether the app actually moved a business result |
| **Human evaluation** | Subjective quality (tone, creativity, nuance, cultural appropriateness) | Bedrock human evaluation job (own SMEs or AWS-managed work team) | Criteria are hard to compute automatically; quality bar is the priority |
| **Benchmark datasets / automatic evaluation** | Objective, formula-computable quality (accuracy, F1, BLEU/ROUGE) | Amazon Bedrock automatic model evaluation, built-in or custom prompt datasets | Comparing many candidates quickly and cheaply at scale |

**Named benchmarks (recognize the task type, not the internals):**

| Benchmark | Task type | Looks like |
|---|---|---|
| **MMLU** | General knowledge/reasoning across 57 subjects | Multiple-choice academic/professional questions |
| **ARC** | Science reasoning | Grade-school-level science questions requiring reasoning |
| **HumanEval** | Code generation | Programming problems checked by running unit tests |
| **GSM8K** | Math word problems | Multi-step arithmetic requiring chained reasoning |

**Additional automated metrics:**

| Metric | Measures | Better direction |
|---|---|---|
| **Toxicity scoring** | Harmful/hateful/unsafe language | Lower is better (0-1 scale) |
| **Semantic similarity (BERTScore)** | Meaning-match to a reference, allowing different wording | Higher is better |
| **Perplexity** | Language-model fluency/confidence, not correctness | Lower is better |

- Judging subjective quality with **many candidates** and cost/latency
  matters → automatic benchmark to shortlist, then human evaluation on
  finalists. Judging subjective quality with a **small candidate set**
  → human evaluation alone.
- A raw score is meaningless in isolation — **compare against a
  baseline** (previous model, competing candidate, same benchmark/prompt
  template) before calling a number "good."
- No single metric tells the whole story: combine a
  correctness/reasoning metric, a similarity/quality metric, and the
  toxicity metric before shipping a candidate.
- Unlike BLEU/ROUGE (exact n-gram overlap), **BERTScore** recognizes a
  correctly paraphrased answer as a good match.

## 5. Infrastructure scaling — bullets

- **AWS Trainium** — purpose-built chip for **high-performance,
  cost-efficient training** at scale, via EC2 **Trn1/Trn2**.
- **AWS Inferentia** — purpose-built chip for **high-throughput,
  low-latency, cost-efficient inference**, via EC2 **Inf1/Inf2**.
  (Memorize this pairing precisely — it's tested directly.)
- Both chips are programmed via the **AWS Neuron SDK** and stay
  compatible with PyTorch/TensorFlow; both exist to cut cost vs.
  general-purpose GPU instances at scale.
- **Amazon SageMaker JumpStart** — pretrained FMs + solution templates
  deployable/fine-tunable with more hosting control than Bedrock's
  managed API (specific instance type, or a model not on Bedrock).
- **Bedrock on-demand vs. provisioned throughput** is the
  generative-AI-specific version of the Domain 1 real-time/batch
  inference trade-off: **traffic predictability**, **latency
  guarantee**, and **cost model** (pay-per-token vs. flat-rate
  commitment) all point the same direction together.
- **SageMaker real-time endpoint auto-scaling — five knobs:** target
  metric (usually `SageMakerVariantInvocationsPerInstance`, or a
  CPU/GPU-utilization metric), target value (per-instance threshold),
  scale-out cooldown, scale-in cooldown, MinCapacity/MaxCapacity.
- **Core auto-scaling trade-off:** shorter cooldown reacts faster but
  risks **flapping** (repeated scale-out/scale-in); longer cooldown
  avoids flapping but reacts slower.
- **Traffic-shape → cooldown pattern:**
  - Steady/predictable → short cooldown safe on **both** sides.
  - Bursty/spiky → **short** scale-out cooldown (add capacity fast) +
    **long** scale-in cooldown (don't remove it the moment the spike
    dips) — asymmetric, not "longer on both sides."
  - Periodic/scheduled (business hours, nightly batch) → layer a
    **scheduled scaling action** on top of reactive target tracking.
  - Spike too fast for any cooldown → raise MinCapacity as a standing
    buffer, or pre-warm with provisioned concurrency/throughput.
- **Flapping fix:** lengthen the scale-in cooldown, not the scale-out
  one. **Capacity never scales back down:** check for conflicting
  target-tracking policies on the same variant — Application Auto
  Scaling only scales in when *every* attached policy agrees.

## 6. Prompt-injection prevention — bullets

- **Prompt injection** — malicious input tries to override or
  manipulate a prompt's original instructions (a jailbreaking
  technique); it is one of the standard harmful-content categories a
  Bedrock **Guardrails content filter** can screen for, alongside hate,
  insults, sexual content, violence, and misconduct.
- **Guardrails for Amazon Bedrock content filters** — built-in ML
  classifiers score prompt-attack/injection attempts at a configurable
  strength threshold; the primary automated defense.
- **Careful prompt design** — clearly separate trusted system
  instructions from untrusted user input (e.g., delimiters, structured
  templates); never let raw untrusted text be interpreted as an
  instruction.
- **Input validation** — sanitize/inspect user-supplied input before it
  reaches the model, alongside Guardrails, rather than relying on the
  model alone to resist manipulation.
- **Human review (Amazon A2I)** — route sensitive or high-risk
  generations to a human reviewer as a backstop for jailbreaking/prompt
  injection attempts that slip past automated filters.
- **Contextual grounding checks** — a different Guardrails rule type
  (compares output against supplied source content); doesn't stop
  injection itself, but limits the damage by blocking ungrounded claims
  a successful injection tries to produce.
- **What doesn't fix it:** inference parameters (temperature, top-p,
  top-k) and RAG do not defend against prompt injection — Guardrails
  content filters plus input validation plus human review are the
  actual controls.

## 7. RAG failure-mode triage list

| Symptom | Root cause | Fix |
|---|---|---|
| Answer correct but incomplete, cuts off mid-explanation | Chunks too small — a self-contained answer split across a chunk boundary | Increase chunk size, add chunk overlap, retrieve more chunks (raise `numberOfResults`) |
| Retrieved chunks unrelated to the query's topic entirely | Embedding model doesn't understand domain-specific vocabulary/jargon | Swap to a better-suited embeddings model and re-embed the whole corpus; expand jargon/abbreviations in source text |
| Retrieved chunks topically related but not the specific right answer | Pure vector similarity returns the *closest* chunks, not the *correct* ones | Add reranking (re-score candidates for relevance); add hybrid keyword + vector search |
| No relevant chunks at all despite a clearly-worded answer existing | Query/document terminology mismatch — a casual question embeds differently than the formal statement that answers it | Rerank a wider candidate set; rewrite/expand the query before embedding (e.g., HyDE); index likely question phrasings alongside each chunk |
| Assistant states facts not present in any retrieved chunk | **Hallucination** — retrieval returned no/thin relevant chunks, so the FM fills the gap from its own parametric knowledge | Verify a covering chunk exists in the index; raise `numberOfResults`; add an "answer only from context" instruction; require cited sources |
| Request fails or is cut off with a context-length error | **Token-limit overflow** — system prompt + chunks + history exceed the context window | Retrieve fewer/smaller chunks, lower `numberOfResults`, trim history, or move to a larger-context model |

- **Triage order:** retrieval returns nothing relevant → check chunking,
  then embedding model, then index freshness. Retrieval returns
  irrelevant/topically-close results → check reranking and hybrid
  search. Retrieval returns the right chunks but generation is still
  poor → check model capability, temperature, and prompt engineering.
- **Fine-tuning the FM fixes none of these** — all six failure modes
  live in the retrieval half of the pipeline, before the FM ever sees a
  prompt.
- Embeddings models aren't interchangeable after the fact: swapping one
  requires **re-embedding and re-indexing the entire corpus**.

---

## Rapid-fire key terms

- **Foundation model (FM)** — large pretrained model adaptable to many
  tasks via prompting, RAG, or fine-tuning.
- **Prompt engineering** — crafting input (zero/few-shot, chain-of-
  thought, templates) to shape output with no training and no weight
  changes.
- **Retrieval Augmented Generation (RAG)** — grounds FM answers in
  retrieved external data at query time; never changes model weights.
- **Fine-tuning** — retrains a model's weights on a **labeled**
  input/output dataset for a narrow task, style, or format.
- **Continued pre-training** — retrains a model's weights on a large
  **unlabeled** domain-specific corpus to deepen vocabulary/fluency.
- **LoRA (Low-Rank Adaptation)** — freezes base weights, trains small
  low-rank adapter matrices (<1% of parameters).
- **QLoRA (Quantized LoRA)** — LoRA adapters trained on a quantized
  (e.g., 4-bit) frozen base model; lowest GPU-memory footprint.
- **Instruction tuning** — a fine-tuning *objective* (instruction,
  response) pairs, not a parameter strategy; layered on full/LoRA/QLoRA.
- **Provisioned throughput** — reserved Bedrock capacity, in **model
  units**, for a 1- or 6-month commitment; required for most custom
  models.
- **Action group** — the APIs a Bedrock Agent can invoke, typically via
  AWS Lambda.
- **Guardrails for Amazon Bedrock** — configurable safety layer: denied
  topics, content filters, word filters, sensitive information filters,
  contextual grounding checks.
- **Embedding** — a numeric vector capturing semantic meaning.
- **Vector database** — stores/queries embeddings by similarity (k-NN).
- **Semantic search** — search by meaning (embeddings), not exact
  keyword match.
- **Chunking** — splitting documents into pieces before embedding.
- **Reranking** — re-scoring retrieved candidates for relevance before
  generation, beyond raw vector similarity.
- **Hybrid search** — combining vector (semantic) search with
  keyword/lexical search in one query.
- **Hallucination** — a model confidently generating incorrect or
  fabricated information.
- **Prompt injection** — malicious input overriding a prompt's original
  instructions.
- **AWS Trainium / AWS Inferentia** — purpose-built chips for
  cost-efficient training / inference, respectively.
- **Auto-scaling flapping** — repeated scale-out then premature
  scale-in as a metric bounces near the threshold.
- **BERTScore / perplexity / toxicity scoring** — semantic-similarity,
  fluency, and safety metrics used alongside accuracy-style benchmarks.

## Common exam traps checklist

- [ ] "Frequently changing / proprietary data" → **RAG**, not
      fine-tuning. Fine-tuning bakes knowledge into static weights that
      go stale.
- [ ] "Exact required format/tone, have labeled examples" →
      **fine-tuning**, not RAG.
- [ ] Fine-tuning needs **labeled** pairs; continued pre-training needs
      only **unlabeled** text — the fastest way to tell them apart.
- [ ] "Limited GPU budget, single small GPU" → **QLoRA**; "faster/
      cheaper, small quality trade-off, no quantization mentioned" →
      **LoRA**; "best possible accuracy, cost isn't the constraint" →
      **full fine-tuning**.
- [ ] A fine-tuned or continued-pre-trained model almost always needs
      **provisioned throughput** — don't pick on-demand for a custom
      model under steady high load.
- [ ] **Guardrails** filters content; it does **not** retrieve knowledge
      or invoke APIs — don't confuse it with Knowledge Bases or Agents.
- [ ] "Search existing enterprise documents in natural language, no
      embeddings pipeline" → **Amazon Kendra**; "manage your own
      embeddings + similarity index" → **OpenSearch or Aurora/RDS +
      pgvector**.
- [ ] Bursty traffic wants a **short** scale-out cooldown and a **long**
      scale-in cooldown — not a long cooldown on both sides.
- [ ] Hallucination in an otherwise-working RAG system usually means
      retrieval came back empty/thin — fix retrieval coverage and prompt
      instructions, not "fine-tune the model to hallucinate less."
- [ ] Judging **tone/creativity** → human evaluation; judging
      **objective, formula-computable** quality at scale → automatic
      benchmark evaluation; judging **real-world outcome impact** →
      business metrics — don't conflate the three layers.
- [ ] **AWS Trainium → training; AWS Inferentia → inference** — don't
      swap the pairing under pressure.

---

## Where each row comes from

| This cram sheet | Full guide section |
|---|---|
| 1. Six FM customization methods | [Section 4](../domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering) + [Fine-tuning efficiency techniques](../domain-3-applications-of-foundation-models.md#fine-tuning-efficiency-techniques-full-fine-tuning-vs-lora-vs-qlora-vs-instruction-tuning) |
| 2. Amazon Bedrock features checklist | [Section 5](../domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features) + [Guardrails rule-type decision tree](../domain-3-applications-of-foundation-models.md#guardrails-rule-type-decision-tree-matching-the-use-case-to-the-right-filter) |
| 3. Vector databases | [Section 6](../domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval) |
| 4. Evaluation strategy comparison table | [Section 7](../domain-3-applications-of-foundation-models.md#7-evaluating-foundation-model-performance) |
| 5. Infrastructure scaling | [Section 8](../domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads) + [SageMaker endpoint auto-scaling guide](../domain-3-applications-of-foundation-models.md#sagemaker-endpoint-auto-scaling-a-parameter-tuning-decision-guide) |
| 6. Prompt-injection prevention | [Section 5](../domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features) + [Guardrails rule-type decision tree](../domain-3-applications-of-foundation-models.md#guardrails-rule-type-decision-tree-matching-the-use-case-to-the-right-filter) |
| 7. RAG failure-mode triage list | [Troubleshooting a failing RAG system](../domain-3-applications-of-foundation-models.md#worked-example-troubleshooting-a-failing-rag-system) + [Decision tree: diagnosing RAG retrieval failures](../domain-3-applications-of-foundation-models.md#decision-tree-diagnosing-rag-retrieval-failures) |
| Rapid-fire key terms | [Key terms glossary](../domain-3-applications-of-foundation-models.md#key-terms-glossary) |

For the full explanations, worked examples, mini-quizzes, and practice
questions this cram sheet intentionally omits, go back to the
[full Domain 3 guide](../domain-3-applications-of-foundation-models.md).
For material spanning multiple domains, see
[`docs/cross-domain-concept-map.md`](../cross-domain-concept-map.md).

[← Back to the full Domain 3 guide](../domain-3-applications-of-foundation-models.md)
