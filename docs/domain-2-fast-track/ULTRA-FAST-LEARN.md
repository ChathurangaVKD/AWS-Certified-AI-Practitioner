# Domain 2 Ultra Fast Track: Fundamentals of Generative AI

**Ultra-condensed cram sheet** · full guide: [`docs/domain-2-fundamentals-of-generative-ai.md`](../domain-2-fundamentals-of-generative-ai.md) (2,213 lines) · **Last verified:** 2026-09-05

Bullets and tables only — no prose, no worked examples, no mini-quizzes.
For the last 15-20 minutes before the exam, once the full guide's own
[Quick-reference cheat sheet](../domain-2-fundamentals-of-generative-ai.md#quick-reference-cheat-sheet)
is already familiar and you just need the highest-yield tables refreshed
one more time. Domain 2 is the largest single domain on the exam
(**~24%** of scored questions). Every row below links back to the full
guide section it's drawn from.

## Table of contents

- [1. Transformer mechanics](#1-transformer-mechanics)
- [2. Foundation model selection criteria](#2-foundation-model-selection-criteria)
- [3. Prompt-engineering techniques](#3-prompt-engineering-techniques)
- [4. Inference parameters](#4-inference-parameters)
- [5. RAG architecture](#5-rag-architecture)
- [6. Common GenAI risks](#6-common-genai-risks)
- [7. AWS service → use case table](#7-aws-service-use-case-table)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Common exam traps checklist](#common-exam-traps-checklist)
- [Where each row comes from](#where-each-row-comes-from)

---

## 1. Transformer mechanics

| Stage | What happens |
|---|---|
| Input text | Raw text the model will process |
| Tokenization | Text split into tokens (word/sub-word units — **tokens ≠ words**) |
| Embeddings | Each token mapped to a numeric **vector** capturing meaning |
| Positional encoding | Added to embeddings so word order is preserved |
| Self-attention (× N layers) | Each token weighs the relevance of **every other token**, regardless of distance |
| Feed-forward network | Per-token transformation applied after attention |
| Output | Next-token probabilities, generated **one token at a time** |

- **Self-attention** is the defining innovation — it computes a relevance
  weight between *every* pair of tokens directly, so a long-range link
  (e.g., resolving a pronoun several sentences back) costs no more to
  compute than a link between adjacent tokens.
- This is what gives transformers both **long-range context** and
  **efficient parallel training**, unlike older left-to-right recurrent
  architectures.
- **Embedding** = the semantic representation; **vector** = the numeric
  array it's stored as; **vector database** = where those arrays are
  stored/searched (e.g., Amazon OpenSearch Service, Aurora + `pgvector`,
  Amazon Kendra).

## 2. Foundation model selection criteria

| Factor | Ask yourself |
|---|---|
| Cost | Per-token (on-demand) or **Provisioned Throughput** — bigger/more capable models cost more per token |
| Modality | Does the model accept/produce the needed input/output types (text, image, audio, video)? |
| Latency | Real-time/interactive use cases need fast (usually smaller) models; batch/async workloads tolerate more |
| Context window | Is the input (plus any retrieved context) small enough to fit without chunking? |
| Fine-tuning / customization support | Can this model/provider be fine-tuned or continued-pre-trained if needed? |
| Model size, accuracy, licensing | Parameter count as a rough capability/cost proxy; validate accuracy with **Amazon Bedrock Model Evaluation**; check compliance/licensing terms |

**Amazon Nova family (not one ladder — pick by modality first):**

| Variant | Modality (in → out) | Relative cost/latency | Use for |
|---|---|---|---|
| **Nova Micro** | Text → text | Lowest | High-volume, cheap, latency-sensitive text (simple chat, classification) |
| **Nova Lite** | Text/image/video → text | Low | Lightweight multimodal chat, document Q&A with images |
| **Nova Pro** | Text/image/video → text | Moderate | Balanced multimodal RAG, moderate agentic reasoning |
| **Nova Premier** | Text/image/video → text | Highest | Most complex multi-step multimodal reasoning; teacher model for distillation |
| **Nova Canvas** | Text/image → image | Priced per image | Studio-quality image generation/editing |
| **Nova Reel** | Text/image → video | Priced per second | Short-form video generation (async) |
| **Nova Sonic** | Speech → speech | Priced per duration | Real-time speech-to-speech (voice assistants, IVR) |

- Weigh **all** stated constraints together — the biggest, most capable
  model is not automatically correct if latency or cost is called out.
- Micro/Lite/Pro/Premier climb together in cost/latency/capability;
  Canvas/Reel/Sonic are separate models picked by **output modality**,
  not a pricier rung on that same ladder.

## 3. Prompt-engineering techniques

| Technique | What it does | Changes model weights? |
|---|---|---|
| **Zero-shot** | Ask the model to perform a task with **no examples** | No |
| **Few-shot** | Include a **small number of example input/output pairs** to show the desired pattern | No |
| **Chain-of-thought (CoT)** | Instruct the model to reason **step by step** before the final answer | No |
| **Negative prompting** | Tell the model what **not** to include or do (common in image generation) | No |
| **Fine-tuning** *(contrast, not a prompting technique)* | Retrains the model's weights on labeled examples | **Yes** |

- **Prompt template** — reusable prompt structure with placeholders for
  variable content.
- **Prompt injection** — malicious input tries to override a prompt's
  original instructions; mitigated with input validation + **Guardrails
  for Amazon Bedrock**.
- A well-formed prompt combines: **instruction + context + input data +
  output indicator**.
- Multi-step arithmetic/logic task, improve accuracy without retraining →
  **chain-of-thought**. Inconsistent format/style across calls →
  **few-shot**. Unwanted elements in generated images → **negative
  prompting**.

## 4. Inference parameters

| Parameter | Controls | Low / small value | High / large value |
|---|---|---|---|
| **Temperature** | Randomness of next-token choice | More focused, deterministic, repeatable | More creative, varied, random |
| **Top-p** (nucleus sampling) | Cumulative-probability candidate pool | Narrower pool → safer, less varied | Wider pool → more diverse |
| **Top-k** | Fixed-size candidate pool (k most-likely tokens) | Small k → safer, less varied | Large k → more diverse |
| **Max tokens** (maximum length) | Cap on response length | Shorter responses, may truncate | Longer responses allowed |
| **Stop sequences** | Halts generation when matched | A matched string stops generation immediately (no gradient) | — |

- **Order of operations:** temperature reshapes the distribution **first**,
  then top-p/top-k prune the candidate pool, then the next token is
  sampled — they are not independent dials.
- **Exam trap:** low temperature + high top-p/top-k is *still* mostly
  deterministic (little probability mass reaches the wide pool). High
  temperature + low top-p/top-k is *still* narrow/repetitive (the pruning
  step throws away the long tail the temperature flattened in).
- None of temperature/top-p/top-k/max-tokens/stop-sequences reduce
  **hallucination** or enforce a content policy — only **RAG** (facts) and
  **Guardrails for Amazon Bedrock** (safety) do that.
- **Cost/latency lever:** lower temperature → fewer JSON/format validation
  retries and shorter completions → lower effective cost and latency,
  without changing the per-token price. Max tokens and stop sequences are
  the *direct* cost/latency levers; temperature/top-p/top-k are indirect.

## 5. RAG architecture

| Step | What happens | AWS |
|---|---|---|
| 1. Ingest | Source documents (e.g., product catalog, policy docs) loaded from a data source | Amazon S3, SharePoint, Salesforce |
| 2. Chunk + embed | Documents split into chunks; each chunk converted to an embedding vector | Embeddings model (e.g., Amazon Titan Text Embeddings) |
| 3. Index | Vectors stored in a vector store for similarity search | Amazon OpenSearch Service, Aurora + `pgvector`, Amazon Kendra |
| 4. Query embed | The user's question is embedded the same way | Same embeddings model |
| 5. Retrieve | Vector store returns the chunks closest (most similar) to the query vector | Managed by **Knowledge Bases for Amazon Bedrock** |
| 6. Augment + generate | Retrieved chunks + original question passed as a **prompt** to an LLM, which generates a grounded answer | Bedrock FM (e.g., Claude, Titan) |

- **RAG grounds answers in retrieved data at inference time — it does not
  retrain the model.** This is what distinguishes it from fine-tuning.
- **RAG's primary purpose:** reduce **hallucination** by grounding output
  in actual source data — it does not fully restore interpretability or
  guarantee correctness, and it does not by itself reduce nondeterminism.
- **Fabricated/wrong facts** → reach for **RAG**. **Wrong tone, format, or
  style** → reach for **prompt engineering or fine-tuning**, not RAG.
- **Knowledge Bases for Amazon Bedrock** is the managed, no-retrain way to
  wire steps 1-6 together without building custom retrieval code.

## 6. Common GenAI risks

| Risk | Definition | Primary mitigation |
|---|---|---|
| **Hallucination** | Fluent, confident output that is **factually incorrect or fabricated** (e.g., a citation/API that doesn't exist) | **RAG** (ground in real data); lower temperature helps marginally |
| **Interpretability (lack of)** | "Black box" — hard to explain *why* an FM produced a given output | Human review; not something inference parameters fix |
| **Inaccuracy** | Output is simply wrong/outdated/low quality, distinct from confident fabrication | Model evaluation, RAG, fine-tuning on better data |
| **Nondeterminism** | Same prompt → **different outputs on different runs** (sampling from a probability distribution) | Lower **temperature**/top-p/top-k (reduces, doesn't eliminate) |
| **Cost / compute intensity** | Large FMs, long context windows, and retries can be expensive at scale | Right-size model, cap max tokens, lower temperature to cut retries |
| **Prompt injection** | Malicious input overrides/manipulates the original prompt instructions | Input validation + **Guardrails for Amazon Bedrock** |

- **Hallucination vs. inaccuracy:** hallucination is *confidently
  fabricating specifics*; inaccuracy is just *being wrong/low quality* —
  the exam tests this distinction directly.
- **Guardrails for Amazon Bedrock** — configurable safety/compliance
  filters (harmful content, denied topics, PII redaction) applied
  consistently across models; addresses safety, not factual accuracy.

## 7. AWS service → use case table

| If the scenario says... | Use... |
|---|---|
| "single API across multiple FMs, fully managed, minimal infra" | **Amazon Bedrock** |
| "ground FM answers in our own data without retraining" | **Knowledge Bases for Amazon Bedrock** (RAG) |
| "FM should plan/execute multi-step tasks calling our APIs/Lambda" | **Agents for Amazon Bedrock** |
| "block harmful content, denied topics, redact PII" | **Guardrails for Amazon Bedrock** |
| "compare FM outputs to pick the best model for a task" | **Amazon Bedrock Model Evaluation** |
| "reserved capacity for steady, high-volume, predictable performance" | **Provisioned Throughput** |
| "pre-built enterprise assistant grounded in company data/systems out of the box" | **Amazon Q Business** |
| "code suggestions, explanations, security scans, AWS resource Q&A" | **Amazon Q Developer** |
| "deploy/fine-tune pretrained FMs with deep infra control, mix with SageMaker MLOps" | **Amazon SageMaker JumpStart** |
| "free, no-code, quick FM experimentation/prototyping" | **PartyRock** |
| "text-to-image generation/editing" | **Amazon Nova Canvas** |
| "text/image-to-video generation" | **Amazon Nova Reel** |
| "real-time, bidirectional speech-to-speech" | **Amazon Nova Sonic** |

- **Golden rule:** the more "out of the box" a scenario needs, the more
  the answer shifts toward **Amazon Q** or **PartyRock**; the more custom,
  production-grade control it needs, the more it shifts toward **Amazon
  Bedrock** or **SageMaker JumpStart**.

---

## Rapid-fire key terms

- **Generative AI** — subset of deep learning where models generate new
  content rather than only predicting a label or number.
- **Foundation model (FM)** — large model pretrained on broad data,
  adaptable to many tasks via prompting, RAG, or fine-tuning.
- **Large language model (LLM)** — an FM specialized for natural-language
  text; a subset of FMs, not a synonym for all FMs.
- **Multimodal model** — accepts and/or generates more than one content
  type (text, image, audio, video); input and output modalities can
  differ.
- **Token** — the basic unit of text an LLM reads/generates; **tokens ≠
  words** (pricing and context windows are measured in tokens).
- **Embedding** — a numeric representation capturing semantic meaning.
- **Vector** — the numeric array an embedding is stored as.
- **Vector database** — stores/queries embeddings by similarity.
- **Semantic search** — search by meaning (embeddings/vectors), not exact
  keyword match.
- **Transformer architecture** — the neural network architecture behind
  most modern LLMs, built on self-attention.
- **Self-attention** — lets each token weigh the relevance of every other
  token, regardless of distance.
- **Context window** — max tokens (input + often output) a model can
  consider at once.
- **Zero-shot / few-shot prompting** — no examples vs. a few example
  input/output pairs in the prompt.
- **Chain-of-thought prompting** — step-by-step reasoning before the final
  answer.
- **Negative prompting** — explicitly stating what to exclude.
- **Temperature / top-p / top-k** — inference parameters controlling
  randomness/diversity of next-token sampling.
- **Retrieval Augmented Generation (RAG)** — grounds FM answers in
  retrieved external data at inference time, without retraining.
- **Fine-tuning** — further training an FM's weights on labeled data.
- **Hallucination** — confident but fabricated/incorrect output.
- **Nondeterminism** — same prompt, different output across runs.
- **Prompt injection** — malicious input overriding prompt instructions.
- **Amazon Bedrock** — managed access to multiple FMs via one API.
- **Amazon Q Business / Amazon Q Developer** — pre-built enterprise
  assistant / generative AI coding companion.
- **Provisioned Throughput** — reserved Bedrock capacity for steady,
  high-volume traffic.

## Common exam traps checklist

- [ ] **Hallucination** (confidently fabricated specifics) ≠
      **inaccuracy** (just wrong/low quality) — don't conflate them.
- [ ] Lowering **temperature** reduces nondeterminism, but does **not**
      eliminate hallucination risk (that comes from training data/RAG,
      not sampling).
- [ ] **Top-p** = cumulative-probability threshold; **top-k** = fixed
      count of top tokens — don't swap these under pressure.
- [ ] High temperature + narrow top-p/top-k can still be repetitive; low
      temperature + wide top-p/top-k can still be near-deterministic —
      the three parameters interact, they aren't independent.
- [ ] **Few-shot prompting** changes nothing about model weights; only
      **fine-tuning** retrains them.
- [ ] Fabricated/wrong **facts** → **RAG**; wrong **tone/format/style** →
      prompt engineering or fine-tuning, not RAG.
- [ ] RAG grounds answers in data — it does **not** restore
      interpretability or guarantee correctness.
- [ ] A scenario with **two or three constraints at once** (real-time +
      long documents + fixed budget) wants you to weigh **all** of them,
      not just pick the biggest model.
- [ ] "No-code, quick experimentation" → **PartyRock**; "pre-built,
      grounded in enterprise data out of the box" → **Amazon Q Business**;
      "deep infra control / mix with SageMaker" → **SageMaker JumpStart**.
- [ ] Content-safety questions need **Guardrails for Amazon Bedrock** —
      raising/lowering inference parameters alone cannot enforce a
      content policy.

---

## Where each row comes from

| This cram sheet | Full guide section |
|---|---|
| 1. Transformer mechanics | [Section 1](../domain-2-fundamentals-of-generative-ai.md#1-generative-ai-core-concepts) |
| 2. Foundation model selection criteria | [Section 7](../domain-2-fundamentals-of-generative-ai.md#7-foundation-model-selection-criteria) + [Nova comparison](../domain-2-fundamentals-of-generative-ai.md#comparing-amazon-nova-model-variants) |
| 3. Prompt-engineering techniques | [Section 6](../domain-2-fundamentals-of-generative-ai.md#6-prompt-engineering-fundamentals) |
| 4. Inference parameters | [Cost and latency implications subsection](../domain-2-fundamentals-of-generative-ai.md#cost-and-latency-implications-of-temperature-top-p-and-top-k) |
| 5. RAG architecture | [Section 1](../domain-2-fundamentals-of-generative-ai.md#1-generative-ai-core-concepts) + [Section 5](../domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) |
| 6. Common GenAI risks | [Section 3](../domain-2-fundamentals-of-generative-ai.md#3-advantages-and-disadvantages-of-generative-ai) |
| 7. AWS service → use case table | [Comparison table](../domain-2-fundamentals-of-generative-ai.md#comparison-table-aws-generative-ai-services-at-a-glance) |
| Rapid-fire key terms | [Key terms glossary](../domain-2-fundamentals-of-generative-ai.md#key-terms-glossary) |

For the full explanations, worked examples, mini-quizzes, and practice
questions this cram sheet intentionally omits, go back to the
[full Domain 2 guide](../domain-2-fundamentals-of-generative-ai.md). For
material spanning multiple domains, see
[`docs/cross-domain-concept-map.md`](../cross-domain-concept-map.md).

[← Back to the full Domain 2 guide](../domain-2-fundamentals-of-generative-ai.md)
