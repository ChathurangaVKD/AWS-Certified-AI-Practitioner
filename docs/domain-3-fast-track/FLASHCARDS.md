# Domain 3 Flashcards: Applications of Foundation Models

**Flashcard deck** · full guide: [`docs/domain-3-applications-of-foundation-models.md`](../domain-3-applications-of-foundation-models.md) · ultra fast track: [`docs/domain-3-fast-track/ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · **Last verified:** 2026-09-09

A companion active-recall / spaced-repetition deck, not a new source of
material — every card below is a front/back reformat of a fact already
verified in the [Ultra Fast Track](ULTRA-FAST-LEARN.md) cram sheet. This
deck covers the **entire domain** — it is not split by the full guide's
part-1/part-2/part-3 files. Cards are ordered to match the Ultra Fast
Track's own section order, so studying the deck top to bottom reinforces
the domain's structure. One question or term per card, one-to-two-line
answer, no re-explaining.

For app-based spaced repetition (Anki, Quizlet, etc.), import
[`flashcards.tsv`](flashcards.tsv) directly — it's the same 126 cards,
same order, tab-separated with no header row.

## 1. Customization trade-off table

| Front | Back |
|---|---|
| Prompt engineering — changes weights? data required? cost/flexibility? | No weight change; no data beyond the prompt; lowest cost; highest flexibility (edit prompt, redeploy instantly). |
| RAG — changes weights? data required? cost/flexibility? | No weight change; external knowledge source (documents), no labeling; low cost; high flexibility (re-sync data, no retraining). |
| Fine-tuning — changes weights? data required? cost/flexibility? | Yes, changes weights; labeled input/output example pairs; higher cost; lower flexibility (new training job per change), often needs provisioned throughput. |
| Continued pre-training — changes weights? data required? cost/flexibility? | Yes, changes weights; large volume of unlabeled domain-specific text; highest cost; lowest flexibility (heaviest, slowest to iterate). |
| "Frequently changing data" / "reduce hallucination from our own docs" — which customization approach? | RAG, not fine-tuning. |
| Labeled vs. unlabeled data — fine-tuning or continued pre-training? | Labeled pairs → fine-tuning (narrow task/style/format); unlabeled bulk text → continued pre-training (broad domain fluency). |
| "No data available, quick behavior/format tweak" — which approach? | Prompt engineering. |
| Full fine-tuning — parameters updated, resource cost, best fit? | 100% of weights; highest resource cost; max accuracy, ample GPU budget, safety/compliance-critical. |
| LoRA — parameters updated, resource cost, best fit? | <1% (small adapter matrices); low resource cost; resource-constrained, mid-size GPU (24GB+) available. |
| QLoRA — what is it, and best fit? | LoRA on a base model quantized (e.g., 4-bit); lowest GPU memory; GPU memory is the hard training constraint (fits a single 16GB GPU). |
| Instruction tuning — what is it? | An objective, not a parameter strategy — trains on (instruction, response) pairs, layered on any fine-tuning method; improves general instruction-following. |
| "Limited GPU budget, single GPU" — which fine-tuning technique? | QLoRA. |
| "Faster/cheaper, small quality trade-off, no quantization mentioned" — which technique? | LoRA. |
| "Best accuracy, cost/time isn't the constraint" — which technique? | Full fine-tuning. |
| Merged vs. unmerged adapter — serving latency? | Merged (folded into base weights) serves at ~1.0x full-fine-tuning latency; unmerged adds a tax (~1.05-1.15x LoRA, ~1.15-1.3x QLoRA). |
| What are full fine-tuning, LoRA, QLoRA, and instruction tuning all examples of? | Supervised fine-tuning (SFT) — trained against one "correct" labeled target. |
| What are RLHF's three stages? | (1) Start from an SFT baseline policy; (2) train a reward model on human preference rankings; (3) fine-tune the SFT model against the reward model via reinforcement learning (commonly PPO). |
| Does RLHF fix stale or missing knowledge? | No — RLHF only changes how a model responds, never what it knows; use RAG for stale/missing knowledge. |
| LoRA/QLoRA, small-to-mid model (≤13B), one task — recommended minimum labeled examples? | ~100-500. |
| Full fine-tuning, large model (34B+), one task — recommended minimum labeled examples, and the risk if underfed? | ~10,000-100,000+; risks catastrophic forgetting if underfed. |
| Continued pre-training — recommended data volume? | Millions-billions of unlabeled tokens. |
| Fewer than ~50-100 labeled examples per class/task — what does the exam usually want instead of a smaller fine-tune? | Prompt engineering (few-shot) or RAG. |
| What four items make up the fine-tuning data-quality checklist? | Diversity, edge-case coverage, label correctness (inter-annotator agreement), class/category balance. |
| Synthetic vs. real fine-tuning data — safest pattern? | Real data as the foundation, synthetic to fill specific identified gaps — never entirely synthetic for a high-stakes task. |

## 2. Prompt engineering techniques at a glance

| Front | Back |
|---|---|
| Zero-shot — exam keywords? | "no examples," "simplest task." |
| Few-shot — exam keywords? | "example input/output pairs," "consistent structure." |
| Chain-of-thought — exam keywords? | "step by step," "reasoning," "show your work." |
| Prompt templates — exam keywords? | "reusable structure," "placeholders," "Bedrock Prompt Management." |
| Prompt chaining / Prompt Flows — exam keywords? | "sequence of prompts," "visual builder," "output feeds next." |
| System prompts / role prompting — exam keywords? | "persona," "role," "across the conversation." |
| Prompt injection in a list of prompting "techniques" — what is it really? | Not a technique — a security risk; the exam plants it as a distractor in technique lists. |

## 3. Bedrock features checklist

| Front | Back |
|---|---|
| "Explicitly enable a model before calling it" — which Bedrock feature? | Model access. |
| "Take actions / call APIs / multi-step tasks, re-plan based on a tool result" — which feature? | Agents (action groups). |
| "Block harmful, off-topic, or PII content" — which feature? | Guardrails. |
| "Answer from our own documents, no retraining" — which feature? | Knowledge Bases (RAG). |
| "Visual builder, sequence of prompts, output feeds next" — which feature? | Prompt Flows. |
| "Compare model quality objectively/at scale" — which feature? | Automatic model evaluation. |
| "Judge subjective quality like tone/creativity" — which feature? | Human evaluation. |
| "Guaranteed throughput, high/steady/predictable volume, custom model" — which feature? | Provisioned throughput. |
| "Unpredictable/low/spiky volume, pay per use" — which feature? | On-demand. |
| Redact PII (names, SSNs, emails, phone/account numbers) — which Guardrails rule type? | Sensitive information filters. |
| Fixed list of exact strings (competitor names, profanity) — which rule type? | Word filters. |
| Whole subject area regardless of phrasing (e.g., "no medical advice") — which rule type? | Denied topics. |
| Standard harm category (hate, violence, sexual, prompt injection) — which rule type? | Content filters. |
| Model contradicts/invents facts not in the source — which rule type? | Contextual grounding checks. |
| Does Guardrails retrieve knowledge or invoke APIs? | No — Guardrails filters content only; Knowledge Bases retrieves, Agents invoke APIs. |

## 4. Vector databases and embeddings

| Front | Back |
|---|---|
| Amazon OpenSearch (Service/Serverless) — pick for? | Native hybrid (vector + keyword) search in one query, bring your own embedding model; large scale; default vector store for Bedrock Knowledge Bases. |
| Amazon Aurora (PostgreSQL) + pgvector — pick for? | Vectors as a column type queried with SQL; "we already run Aurora/PostgreSQL." |
| Amazon Kendra — pick for? | Fully managed enterprise search, no embedding model to pick, automatic relevance ranking; a Knowledge Base can reuse an existing Kendra GenAI Index as its retriever. |
| Embedding model tiers, in order of preference? | General-purpose (Titan/Cohere) → domain-specific pretrained → fine-tuned on your own data. |
| When should you move past the default general-purpose embedding model? | Only when a scenario calls out a specialized domain AND a retrieval-quality problem traceable to the embedding model itself (not chunking or the vector store). |
| What does reranking fix that pure vector similarity can't? | "Topically close but not the right chunk" results and query/document terminology mismatches. |
| What does hybrid search (vector + keyword) surface that vector similarity alone would miss? | Exact-term matches (SKU codes, names, acronyms). |

## 5. Evaluation-strategy table

| Front | Back |
|---|---|
| Automatic/benchmark evaluation — measures what, speed/cost? | Objective, formula-computable quality (accuracy, F1, BLEU/ROUGE, toxicity); fast, cheap, reproducible at scale. |
| Human evaluation — measures what, speed/cost? | Subjective quality (tone, creativity, nuance, cultural fit); slow, expensive. |
| Business metrics — measures what, and when used? | Real-world outcome impact (CSAT, task completion, cost/interaction, escalation rate); post-launch, ongoing — the only layer tied to org goals. |
| MMLU — measures, direction? | General knowledge/reasoning across subjects; higher is better. |
| ARC — measures, direction? | Science reasoning; higher is better. |
| HumanEval — measures, direction? | Code generation (pass unit tests); higher is better. |
| GSM8K — measures, direction? | Multi-step math word problems; higher is better. |
| Toxicity scoring — measures, direction? | Is this output safe to show a user?; lower is better. |
| BERTScore — measures, direction? | Semantic similarity to a reference despite different wording; higher is better. |
| Perplexity — measures, direction? | LM fluency/confidence, independent of correctness; lower is better. |
| BLEU/ROUGE vs. BERTScore — what's the difference? | BLEU/ROUGE reward exact n-gram overlap and penalize valid paraphrases; BERTScore recognizes a correctly-reworded answer. |
| Recall@k — what does it measure, use when? | Whether a relevant item appears anywhere in the top k; use when any top-k result counts as a win. |
| MRR (Mean Reciprocal Rank) — what does it measure, use when? | How early the first relevant result appears; use when each query has essentially one correct/best answer. |
| MAP (Mean Average Precision) — what does it measure, use when? | Precision averaged across every relevant item's rank; use when multiple relevant, binary-labeled documents exist per query. |
| NDCG@k — what does it measure, use when? | Ranking quality with graded (not binary) relevance; use when relevance comes in degrees and order matters. |

## 6. Infrastructure-scaling bullets

| Front | Back |
|---|---|
| AWS Trainium — purpose? | High-performance, cost-efficient training at scale (EC2 Trn1/Trn2). |
| AWS Inferentia — purpose? | High-throughput, low-latency, cost-efficient inference (EC2 Inf1/Inf2). |
| What SDK programs both Trainium and Inferentia? | AWS Neuron SDK. |
| Amazon SageMaker JumpStart — what does it offer over Bedrock's managed API? | Pretrained FMs + templates, deploy/fine-tune with more hosting control (specific instance type, or a model not on Bedrock). |
| What are the five SageMaker real-time endpoint auto-scaling knobs? | Target metric, target value, scale-out cooldown, scale-in cooldown, MinCapacity/MaxCapacity. |
| Bursty/spiky traffic — cooldown tuning? | Short scale-out cooldown (~60s), long scale-in cooldown (~600-900s) — scale out fast, scale in slow to prevent flapping. |
| "Flapping" (scale out → in → out again quickly) — root cause and fix? | Scale-in cooldown too short — lengthen it. |
| Capacity never scales back down — likely root cause? | Two conflicting target-tracking policies attached — scale-in needs every attached policy to agree. |
| Known daily/weekly traffic peaks — what extra layer should you add beyond reactive scaling? | A scheduled scaling action raising MinCapacity ahead of the known window. |

## 7. Prompt-injection prevention bullets

| Front | Back |
|---|---|
| What is prompt injection? | Malicious user input designed to override the application's intended prompt/system instructions. |
| Is prompt injection a customization technique? | No — it's a security risk to mitigate, never something to intentionally apply. |
| What are the three primary prompt-injection mitigations? | Input validation on user text, Guardrails content filters (harm category "prompt injection"), and clear separation of system instructions from user-supplied content. |
| Do inference parameters (temperature/top-p/top-k/max tokens) stop prompt injection? | No — that's a content-policy problem, not a sampling problem. |

## 8. RAG failure-mode triage

| Front | Back |
|---|---|
| Answer correct but incomplete, cuts off mid-explanation — root cause and fix? | Chunks too small/answer split across a chunk boundary; increase chunk size, add overlap, retrieve more chunks. |
| Retrieved chunks unrelated to the query's topic entirely — root cause and fix? | Embedding model mismatched to the domain; swap to a better-suited embeddings model and re-embed the corpus. |
| Retrieved chunks topically related but not the specific right answer — root cause and fix? | Vector similarity finds "close," not "correct"; add reranking and/or hybrid search. |
| Retrieval returns nothing relevant despite a clearly-worded answer existing — root cause and fix? | Query/document terminology mismatch; rerank a wider candidate set, rewrite the query (e.g., HyDE), index likely question phrasings. |
| Assistant states facts not present in any retrieved chunk — root cause and fix? | Retrieval returned no/thin relevant chunk so the FM fills the gap; verify a covering chunk exists, raise numberOfResults, require cited sources. |
| Request fails/cuts off with a context-length/token-limit error — root cause and fix? | System prompt + chunks + history exceed the context window; retrieve fewer/smaller chunks or use a larger-context model. |
| Does fine-tuning the FM fix any of the six RAG failure modes? | No — all six live in the retrieval half of the pipeline, before the FM ever sees a prompt. |

## Rapid-fire key terms

| Front | Back |
|---|---|
| Modality | Input/output type(s) a model handles (text, image, audio, video); multimodal = more than one. |
| Prompt injection | Malicious input overriding intended prompt instructions; mitigate via input validation + Guardrails content filters. |
| Chunking | Splitting documents into passages before embedding. |
| Embedding | Numeric vector capturing semantic meaning. |
| Vector database | Stores/queries embeddings by similarity (k-NN). |
| Provisioned throughput | Reserved Bedrock capacity (model units) for a commitment period; typically required for custom (fine-tuned) models. |
| On-demand | Pay-per-token Bedrock pricing, no commitment. |
| Action group | The APIs (often via Lambda) a Bedrock Agent invokes. |
| Reranking | Cross-encoder re-scores an initial vector-search candidate set for relevance. |
| Hybrid search | Vector (semantic) search combined with keyword/full-text search in one query. |
| AWS Trainium | Purpose-built AWS chip for cost-efficient training at scale (EC2 Trn1/Trn2). |
| AWS Inferentia | Purpose-built AWS chip for cost-efficient inference (EC2 Inf1/Inf2). |
| Retrieval Augmented Generation (RAG) | Grounds FM answers in retrieved external data at inference time, without retraining. |
| Fine-tuning | Further training an FM's weights on labeled data for a specific task, style, or format. |
| Continued pre-training | Further training an FM on large volumes of unlabeled domain-specific text for broad domain fluency. |
| Amazon Bedrock Knowledge Bases | Bedrock's fully managed RAG feature: automatic ingestion, chunking, embedding, and retrieval. |
| Denied topics (Guardrails) | Semantic block on an entire subject area regardless of phrasing. |
| Content filters (Guardrails) | Built-in ML classifiers per harm category (hate, violence, sexual, prompt injection). |
| Business metric | Outcome-oriented measure (CSAT, conversion rate, cost per interaction) distinct from model-quality metrics. |
| Human evaluation | People scoring FM outputs on subjective criteria (tone, creativity) that automatic metrics can't capture. |
| Benchmark dataset | Standardized dataset used to objectively and reproducibly score and compare model quality. |
| Amazon SageMaker JumpStart | Hub of pretrained FMs and templates deployable/fine-tunable with more hosting control than Bedrock's API. |
| LoRA (Low-Rank Adaptation) | Fine-tuning technique that freezes the base model and trains small low-rank adapter matrices (often <1% of parameters). |
| QLoRA | LoRA on a base model first quantized to a lower precision (e.g., 4-bit); lowest GPU memory of the parameter-efficient options. |
| Instruction tuning | Fine-tuning objective training on (instruction, response) pairs so a model follows instructions generally; layered on full fine-tuning, LoRA, or QLoRA. |
| RLHF (Reinforcement Learning from Human Feedback) | Aligns an SFT model to human preferences via a reward model and reinforcement learning (commonly PPO), layered on top of SFT. |
| Reward model | Model trained on human preference rankings to predict a scalar preference score, used to guide RLHF. |
| Catastrophic forgetting | A fine-tuned model losing previously learned general capability; the risk of full fine-tuning a large model on too little data. |
| Early stopping | Halting training once validation performance stops improving, to avoid overfitting a small fine-tuning dataset. |
| Inter-annotator agreement | Measured consistency between human labelers, used to gauge fine-tuning label correctness. |
| NDCG (Normalized Discounted Cumulative Gain) | Retrieval ranking-quality metric for graded (non-binary) relevance. |
| MAP (Mean Average Precision) | Retrieval metric averaging precision across every relevant item's rank; multiple binary-labeled relevant documents per query. |
| MRR (Mean Reciprocal Rank) | Retrieval metric measuring how early the first relevant result appears; fits queries with one correct/best answer. |
| Recall@k | Retrieval metric measuring whether a relevant item appears anywhere in the top k results. |

## Common exam traps checklist

| Front | Back |
|---|---|
| Does a fine-tuned or continued-pre-trained model typically need on-demand or provisioned throughput under steady high load? | Provisioned throughput — don't pick on-demand for a custom model under steady high load. |
| Does streaming reduce total generation time or cost? | No — streaming only improves perceived latency, not total generation time or cost. |
| Is a raw benchmark score (e.g., "MMLU: 68%") meaningful on its own? | No — always compare it to a baseline (previous model or competing candidate). |
| When should you reuse an existing Kendra GenAI Index instead of building a new vector store? | When one already exists — reuse it as the Knowledge Base's retriever instead of standing up a second OpenSearch/Aurora index for the same content. |

---

[← Back to the full Domain 3 guide](../domain-3-applications-of-foundation-models.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md) · [Interactive cheat sheet →](CHEAT-SHEET.md)
