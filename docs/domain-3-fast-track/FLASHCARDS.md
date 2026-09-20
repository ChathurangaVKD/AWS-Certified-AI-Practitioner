# Domain 3 Flashcards: Applications of Foundation Models

**Spaced-repetition companion deck** · fast track: [`README.md`](README.md) · cram sheet: [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · plain-text import file: [`flashcards.tsv`](flashcards.tsv)

One card per testable concept from the Domain 3 Ultra Fast Track cram sheet, ordered to match that file's own section order so studying this deck reinforces the domain's structure. Front/back only, no prose -- for active recall or spaced repetition. This deck covers the entire domain in one place -- it is not split by fast-track part. `flashcards.tsv` holds the identical cards as a header-less, two-column (front, back) tab-separated file, importable as-is into Anki or Quizlet.

## 1. Customization trade-off table

| Front | Back |
|---|---|
| Customization approach: no weight changes, no data beyond the prompt itself | Prompt engineering -- lowest cost/latency, highest flexibility (edit and redeploy instantly) |
| Customization approach: no weight changes, needs an external knowledge source (documents) | RAG (Amazon Bedrock Knowledge Bases) -- low cost, high flexibility (re-sync a data source, no retraining) |
| Customization approach: changes weights, needs labeled input/output example pairs | Fine-tuning -- higher cost/latency, often needs provisioned throughput |
| Customization approach: changes weights, needs a large volume of unlabeled domain-specific text | Continued pre-training -- highest cost, slowest to iterate |
| Trap: do prompt engineering and RAG ever touch model weights? | No -- only fine-tuning and continued pre-training retrain weights, and both typically require provisioned throughput to serve |
| Trap: "frequently changing data" / "reduce hallucination from our own docs" | RAG, not fine-tuning |
| Trap: labeled pairs vs. unlabeled bulk text | Labeled -> fine-tuning (narrow task/style/format); unlabeled -> continued pre-training (broad domain fluency) |
| Trap: "no data available, quick behavior/format tweak" | Prompt engineering |
| Fine-tuning technique: 100% of weights updated | Full fine-tuning -- highest resource cost, highest quality ceiling |
| Fine-tuning technique: <1% of weights, small adapter matrices injected into layers | LoRA (Low-Rank Adaptation) -- low resource cost, modest quality trade-off |
| Fine-tuning technique: LoRA on a base model quantized (e.g., 4-bit) | QLoRA -- lowest resource cost, fits a single small GPU (16GB), small added loss vs. LoRA |
| Fine-tuning technique: trains on (instruction, response) pairs, layered on any of the above | Instruction tuning -- an objective, not a parameter strategy |
| Decision: safety/compliance-critical, quality floor allows less than ~1 point of degradation | Full fine-tuning |
| Decision: mid-size GPU (24GB+) available, a small quality gap is tolerable | LoRA |
| Decision: only a small GPU (<=16GB) available | QLoRA |
| Trap: merged-adapter serving latency | ~1.0x full-fine-tuning latency (folded into base weights); a QLoRA-merged model must first dequantize, losing its memory savings |
| Trap: unmerged-adapter serving latency | ~1.05-1.15x for LoRA, ~1.15-1.3x for QLoRA served quantized -- QLoRA can't be both low-memory and low-latency at serving time |
| Are full fine-tuning, LoRA, QLoRA, and instruction tuning all a form of SFT? | Yes -- supervised fine-tuning against one "correct" labeled target; RLHF is a distinct step layered on top of SFT |
| RLHF stage 1 | Start from an SFT model as the baseline policy |
| RLHF stage 2 | Train a reward model on human preference rankings/comparisons of multiple outputs for the same prompt |
| RLHF stage 3 | Fine-tune the SFT model against the reward model via reinforcement learning (commonly PPO) |
| Scenario: narrow, well-defined labeled task, no ambiguity about "correct" | SFT alone |
| Scenario: open-ended chat/instruction-following where humans must judge which response is better | SFT, then layer RLHF |
| Trap: stale or missing proprietary/current knowledge | RAG, not RLHF -- RLHF only changes how a model responds, never what it knows |
| Minimum labeled examples: LoRA/QLoRA, small-to-mid model (<=13B), one task | ~100-500 |
| Minimum labeled examples: LoRA/QLoRA, large model (34B+), one task | ~500-1,000 |
| Minimum labeled examples: instruction tuning, any size | ~1,000-10,000+ across many task types |
| Minimum labeled examples: full fine-tuning, small-to-mid model, one task | ~1,000-10,000 |
| Minimum labeled examples: full fine-tuning, large model (34B+), one task | ~10,000-100,000+ -- risks catastrophic forgetting if underfed |
| Minimum data: continued pre-training, any size | Millions-billions of unlabeled tokens |
| Trap: fewer than ~50-100 examples per class/task | Signals the exam wants prompt engineering (few-shot) or RAG instead of fine-tuning, not a smaller fine-tune |
| How to avoid overfitting on a small fine-tuning dataset | Hold out a validation set, use early stopping, prefer LoRA/QLoRA over full fine-tuning |
| Data-quality checklist for a fine-tuning dataset | Diversity, edge-case coverage, label correctness (inter-annotator agreement), class/category balance |
| Synthetic vs. real fine-tuning data -- the safest pattern | Real data as the foundation, synthetic to fill specific identified gaps -- never entirely synthetic for a high-stakes task |

## 2. Prompt engineering techniques at a glance

| Front | Back |
|---|---|
| Prompting technique: instruction only, no examples, lowest cost | Zero-shot |
| Prompting technique: a few example input/output pairs | Few-shot |
| Prompting technique: explicit step-by-step reasoning ask | Chain-of-thought (CoT) |
| Prompting technique: reusable structure with placeholders, authored once | Prompt templates |
| Prompting technique: tell the model what to avoid / not include | Negative prompting |
| Prompting technique: orchestrated sequence, visual builder, output feeds next | Prompt chaining / Prompt Flows |
| Prompting technique: one persistent block defining persona/role across the conversation | System prompts / role prompting |
| Which item in a prompt-technique list is not actually a technique, but a security risk? | Prompt injection (attacker-controlled, N/A cost/complexity) |
| Scenario: multi-step arithmetic/logic task | Chain-of-thought |
| Scenario: inconsistent format/style across calls | Few-shot |
| Scenario: unwanted elements in generated images | Negative prompting |
| Scenario: reusable, versioned prompt used across many calls | Prompt template |
| Trap: a table row reads "N/A" / "not a technique" | That's prompt injection -- the exam likes planting it in a technique list |

## 3. Bedrock features checklist

| Front | Back |
|---|---|
| Scenario: explicitly enable a model before calling it | Model access |
| Scenario: take actions / call APIs / multi-step tasks, re-plan based on a tool result | Agents (action groups) |
| Scenario: block harmful, off-topic, or PII content | Guardrails |
| Scenario: answer from our own documents, no retraining | Knowledge Bases (RAG) |
| Scenario: visual builder, sequence of prompts, output feeds next | Prompt Flows |
| Scenario: compare model quality objectively/at scale | Automatic model evaluation |
| Scenario: judge subjective quality like tone/creativity | Human evaluation |
| Scenario: guaranteed throughput, high/steady/predictable volume, custom model | Provisioned throughput |
| Scenario: unpredictable/low/spiky volume, pay per use | On-demand |
| Guardrails rule type: redact PII (names, SSNs, emails, phone/account numbers) | Sensitive information filters -- deterministic pattern match, no ML needed |
| Guardrails rule type: fixed list of exact strings (competitor names, profanity) | Word filters -- cheapest, lowest-latency, list fully known ahead of time |
| Guardrails rule type: whole subject area regardless of phrasing (e.g., "no medical advice") | Denied topics -- semantic match catches paraphrases a word list would miss |
| Guardrails rule type: standard harm category (hate, violence, sexual, prompt injection) | Content filters -- built-in ML classifiers per harm category |
| Guardrails rule type: model contradicts/invents facts not in the source | Contextual grounding checks -- the only rule type that checks truthfulness vs. a source |
| Trap: does Guardrails retrieve knowledge or invoke APIs? | No -- that's Knowledge Bases / Agents |
| Trap: on-demand vs. provisioned throughput decision | Steady + high + predictable volume (or a custom model) -> provisioned throughput; variable/spiky/low volume -> on-demand |

## 4. Vector databases and embeddings

| Front | Back |
|---|---|
| Vector store: native hybrid (vector + keyword) search in one query, bring your own embedding model | Amazon OpenSearch (Service / Serverless) |
| Vector store: vectors as a SQL column type, bring your own embedding model | Amazon Aurora (PostgreSQL) + pgvector |
| Vector store: fully managed enterprise search, no embedding model to pick, built-in connectors | Amazon Kendra |
| When should a Knowledge Base reuse an existing Kendra GenAI Index as its retriever? | When one already exists, over standing up a second index in OpenSearch/Aurora |
| Embedding model tier: default, zero extra training, cheapest, fastest to ship | General-purpose (Amazon Titan Text Embeddings, Cohere Embed) |
| Embedding model tier: captures domain vocabulary out of the box, no training pipeline | Domain-specific pretrained |
| Embedding model tier: trained on your own labeled query/passage pairs, highest accuracy and cost | Fine-tuned on your own data (typically SageMaker, not a Bedrock-native workflow) |
| Trap: when should you move off the default embedding model? | Only when a scenario calls out a specialized domain AND a retrieval-quality problem traceable to the embedding model (not chunking or the vector store) |
| What does reranking fix that pure vector similarity alone can't? | "Topically close but not the right chunk" results and query/document terminology mismatches |
| What does hybrid search surface that vector similarity alone would miss? | Exact-term matches (SKU codes, names, acronyms) |

## 5. Evaluation-strategy table

| Front | Back |
|---|---|
| Evaluation layer: objective, formula-computable quality (accuracy, F1, BLEU/ROUGE, toxicity) | Automatic/benchmark evaluation -- fast, cheap, reproducible at scale |
| Evaluation layer: subjective quality (tone, creativity, nuance, cultural fit) | Human evaluation -- slow, expensive |
| Evaluation layer: real-world outcome impact (CSAT, task completion, cost/interaction, escalation rate) | Business metrics -- post-launch, the only layer tied to org goals, not model quality |
| Metric for general knowledge/reasoning across subjects | MMLU (higher is better) |
| Metric for science reasoning | ARC (higher is better) |
| Metric for code generation (pass unit tests) | HumanEval (higher is better) |
| Metric for multi-step math word problems | GSM8K (higher is better) |
| Metric for "is this output safe to show a user?" | Toxicity scoring (lower is better) |
| Metric for "does output mean the same as a reference despite different wording?" | BERTScore -- semantic similarity (higher is better) |
| Metric for how fluent/confident the LM is, independent of correctness | Perplexity (lower is better) |
| Trap: is a raw benchmark score meaningful on its own? | No -- compare it to a baseline (previous model, competing candidate) |
| Trap: BLEU/ROUGE vs. BERTScore on a valid paraphrase | BLEU/ROUGE reward exact n-gram overlap and penalize valid paraphrases; BERTScore recognizes a correctly-reworded answer |
| Retrieval metric: whether a relevant item appears anywhere in the top k | Recall@k -- use when any top-k result counts as a win |
| Retrieval metric: how early the first relevant result appears | MRR (Mean Reciprocal Rank) -- use when each query has one correct/best answer |
| Retrieval metric: precision averaged across every relevant item's rank | MAP (Mean Average Precision) -- use when multiple relevant, binary-labeled documents exist per query |
| Retrieval metric: ranking quality with graded (not binary) relevance | NDCG@k -- use when relevance comes in degrees and result order matters |

## 6. Infrastructure-scaling bullets

| Front | Back |
|---|---|
| AWS Trainium (EC2 Trn1/Trn2) | High-performance, cost-efficient training at scale |
| AWS Inferentia (EC2 Inf1/Inf2) | High-throughput, low-latency, cost-efficient inference |
| What SDK programs both Trainium and Inferentia? | AWS Neuron SDK |
| Amazon SageMaker JumpStart | Pretrained FMs + templates, deploy/fine-tune with more hosting control than Bedrock's managed API |
| Auto-scaling knob: request volume or CPU/GPU utilization | Target metric |
| Auto-scaling knob: per-instance threshold that triggers scaling | Target value |
| Auto-scaling knob: wait before adding more capacity | Scale-out (scale-up) cooldown |
| Auto-scaling knob: wait before removing more capacity | Scale-in (scale-down) cooldown |
| Auto-scaling knob: floor/ceiling on instance count | MinCapacity / MaxCapacity |
| Cooldown tuning for steady, predictable traffic | Short scale-out (~60s), moderate scale-in (~180-300s) |
| Cooldown tuning for bursty/spiky traffic | Short scale-out (~60s), long scale-in (~600-900s) -- scale out fast, scale in slow |
| Cooldown tuning for periodic/scheduled known daily/weekly peaks | Layer a scheduled scaling action raising MinCapacity ahead of the known window |
| Trap: flapping (scale out, back in, out again quickly) | Scale-in cooldown too short -- lengthen it |
| Trap: capacity never scales back down | Two conflicting target-tracking policies attached -- scale-in needs every attached policy to agree |
| Trap: throttles/timeouts at the start of a spike, then recovers | Target-tracking threshold too close to real ceiling and/or scale-out cooldown too long |
| Trap: MinCapacity/MaxCapacity sized off one historical peak | Re-baseline off current steady-state, not the highest spike ever seen |

## 7. Prompt-injection prevention bullets

| Front | Back |
|---|---|
| Prompt injection -- definition | Malicious user input designed to override the application's intended prompt/system instructions |
| Is prompt injection a customization technique? | No -- it's a security risk to mitigate, never something to intentionally apply |
| Which Guardrails rule type catches the standard "prompt injection" harm category? | Content filters (built-in ML classifiers) -- not word filters, denied topics, or contextual grounding checks |
| Do inference parameters (temperature/top-p/top-k/max tokens) stop prompt injection? | No -- it's a content-policy problem, not a sampling problem |
| Primary mitigations for prompt injection | Input validation on user-supplied text; Guardrails content filters; clear separation of system instructions from user content |

## 8. RAG failure-mode triage

| Front | Back |
|---|---|
| RAG symptom: answer correct but incomplete, cuts off mid-explanation | Chunks too small / answer split across a chunk boundary -- increase chunk size, add overlap, retrieve more chunks |
| RAG symptom: retrieved chunks unrelated to the query's topic entirely | Embedding model mismatched to the domain -- swap to a better-suited embeddings model, re-embed corpus |
| RAG symptom: retrieved chunks topically related but not the specific right answer | Vector similarity finds "close," not "correct" -- add reranking, add hybrid search |
| RAG symptom: retrieval returns nothing relevant despite a clearly-worded answer existing | Query/document terminology mismatch -- rerank a wider set, rewrite the query before embedding (e.g., HyDE) |
| RAG symptom: assistant states facts not present in any retrieved chunk | Hallucination from thin/no retrieval -- verify a covering chunk exists, raise numberOfResults, require cited sources |
| RAG symptom: request fails/cuts off with a context-length / token-limit error | System prompt + chunks + history exceed the context window -- retrieve fewer/smaller chunks, trim history, use a larger-context model |
| Triage order for a live, underperforming RAG system | Hallucination -> token-limit error -> off-topic chunks (embedding model) -> topically-close-but-wrong (reranking/hybrid) -> correct-but-incomplete (chunking) |
| Trap: does fine-tuning the FM fix any RAG failure mode? | No -- all six failure modes live in the retrieval half of the pipeline, before the FM ever sees a prompt |

## Rapid-fire key terms

| Front | Back |
|---|---|
| Modality | Input/output type(s) a model handles (text, image, audio, video); multimodal = more than one |
| Prompt injection | Malicious input overriding intended prompt instructions; mitigate via input validation + Guardrails content filters |
| Chunking | Splitting documents into passages before embedding |
| Embedding | Numeric vector capturing semantic meaning |
| Vector database | Stores/queries embeddings by similarity (k-NN) |
| Provisioned throughput | Reserved Bedrock capacity (model units) for a commitment period; typically required for custom (fine-tuned) models |
| On-demand | Pay-per-token Bedrock pricing, no commitment |
| Action group | The APIs (often via Lambda) a Bedrock Agent invokes |
| Reranking | Cross-encoder re-scores an initial vector-search candidate set for relevance |
| Hybrid search | Vector (semantic) search combined with keyword/full-text search in one query |
| AWS Trainium | Purpose-built AWS chip for cost-efficient training at scale (EC2 Trn1/Trn2) |
| AWS Inferentia | Purpose-built AWS chip for cost-efficient inference (EC2 Inf1/Inf2) |
| Retrieval Augmented Generation (RAG) | Grounds FM answers in retrieved external data at inference time, without retraining |
| Fine-tuning | Further training an FM's weights on labeled data for a specific task, style, or format |
| Continued pre-training | Further training an FM on large volumes of unlabeled domain-specific text for broad domain fluency |
| Amazon Bedrock Knowledge Bases | Bedrock's fully managed RAG feature: automatic ingestion, chunking, embedding, and retrieval |
| Denied topics (Guardrails) | Semantic block on an entire subject area regardless of phrasing |
| Content filters (Guardrails) | Built-in ML classifiers per harm category (hate, violence, sexual, prompt injection) |
| Business metric | Outcome-oriented measure (CSAT, conversion rate, cost per interaction) distinct from model-quality metrics |
| Human evaluation | People scoring FM outputs on subjective criteria (tone, creativity) that automatic metrics can't capture |
| Benchmark dataset | Standardized dataset used to objectively and reproducibly score and compare model quality |
| Amazon SageMaker JumpStart | Hub of pretrained FMs and templates deployable/fine-tunable with more hosting control than Bedrock's API |
| LoRA (Low-Rank Adaptation) | Fine-tuning technique that freezes the base model and trains small low-rank adapter matrices (often <1% of parameters) |
| QLoRA | LoRA on a base model first quantized to a lower precision (e.g., 4-bit); lowest GPU memory of the parameter-efficient options |
| Instruction tuning | Fine-tuning objective training on (instruction, response) pairs so a model follows instructions generally; layered on full fine-tuning, LoRA, or QLoRA |
| RLHF (Reinforcement Learning from Human Feedback) | Aligns an SFT model to human preferences via a reward model and reinforcement learning (commonly PPO), layered on top of SFT |
| Reward model | Model trained on human preference rankings to predict a scalar preference score, used to guide RLHF |
| Catastrophic forgetting | A fine-tuned model losing previously learned general capability; the risk of full fine-tuning a large model on too little data |
| Early stopping | Halting training once validation performance stops improving, to avoid overfitting a small fine-tuning dataset |
| Inter-annotator agreement | Measured consistency between human labelers, used to gauge fine-tuning label correctness |
| NDCG (Normalized Discounted Cumulative Gain) | Retrieval ranking-quality metric for graded (non-binary) relevance |
| MAP (Mean Average Precision) | Retrieval metric averaging precision across every relevant item's rank; multiple binary-labeled relevant documents per query |
| MRR (Mean Reciprocal Rank) | Retrieval metric measuring how early the first relevant result appears; fits queries with one correct/best answer |
| Recall@k | Retrieval metric measuring whether a relevant item appears anywhere in the top k results |

## Common exam traps

| Front | Back |
|---|---|
| Trap: "frequently changing data" / "ground in our own docs" | RAG, not fine-tuning |
| Trap: does a fine-tuned or continued-pre-trained model under steady high load need on-demand or provisioned throughput? | Almost always needs provisioned throughput -- don't pick on-demand for a custom model under steady high load |
| Trap: does Guardrails retrieve knowledge or invoke APIs? | No -- Guardrails filters content only |
| Trap: does streaming reduce total generation time or cost? | No -- streaming improves perceived latency only |
| Trap: labeled data vs. unlabeled data | Labeled data -> fine-tuning; unlabeled data -> continued pre-training -- the fastest way to tell them apart |
| Trap: prompt injection appears disguised as a "technique" in an answer list | It's always the security-risk distractor, never a real technique to apply |
| Trap: cooldown tuning for bursty traffic | Needs a short scale-out + long scale-in cooldown -- not long on both sides |
| Trap: is a raw benchmark score meaningful without context? | No -- it means nothing without a baseline to compare against; know which direction (higher/lower) is better for that metric |
| Trap: do RAG failure modes (chunking, embedding, retrieval, terminology, hallucination, token overflow) get fixed by fine-tuning the FM? | No -- all of them live before the FM sees a prompt |
| Trap: an existing Kendra GenAI Index already exists for the content | Reuse it as the Knowledge Base's retriever instead of standing up a second OpenSearch/Aurora index |
| Trap: limited GPU budget vs. faster/cheaper vs. best accuracy | "Limited GPU budget, single GPU" -> QLoRA; "faster/cheaper, small quality trade-off, no quantization" -> LoRA; "best accuracy, cost/time not the constraint" -> full fine-tuning |
| Trap: does RLHF fix stale or missing knowledge? | No -- RLHF fixes how a model responds (tone, helpfulness); that's RAG's job, not RLHF's |
| Trap: fewer than ~50-100 labeled examples per class/task | Points to prompt engineering (few-shot) or RAG, not a smaller fine-tune |
| Trap: retrieval-metric picks | One correct/best answer -> MRR; graded relevance and order matters -> NDCG@k; binary, multiple relevant docs, order matters -> MAP; only "somewhere in the top k" matters -> Recall@k |

---

**166 cards total.** For the full explanations behind any card, see the [fast track](README.md), the [Ultra Fast Track cram sheet](ULTRA-FAST-LEARN.md), or the [full Domain 3 guide](../domain-3-applications-of-foundation-models.md).

[← Back to the Domain 3 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md)
