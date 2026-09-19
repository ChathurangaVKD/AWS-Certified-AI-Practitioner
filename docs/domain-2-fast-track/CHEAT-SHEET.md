# Domain 2 Cheat Sheet: Fundamentals of Generative AI

**Interactive quick-scan cheat sheet** · companion to the [Fast Track guide](README.md) and the [Ultra Fast Track cram sheet](ULTRA-FAST-LEARN.md) · full guide: [`docs/domain-2-fundamentals-of-generative-ai.md`](../domain-2-fundamentals-of-generative-ai.md)

Built for a 2-3 minute skim right before the exam — jump straight to the
topic you're weakest on, expand only that section, and tick off the
self-check checklist at the end. Domain 2 is the largest single domain on
the exam (**~24%** of scored questions). Every fact here already lives in
the [Fast Track](README.md) and [Ultra Fast Track](ULTRA-FAST-LEARN.md);
this is a reformat for scannability, not new content.

## Table of contents

- [1. Transformer mechanics](#1-transformer-mechanics)
- [2. Foundation model selection criteria](#2-foundation-model-selection-criteria)
- [3. Prompt-engineering techniques](#3-prompt-engineering-techniques)
- [4. Inference parameters](#4-inference-parameters)
- [5. RAG architecture](#5-rag-architecture)
- [6. GenAI advantages and disadvantages](#6-genai-advantages-and-disadvantages)
- [7. AWS service → use case table](#7-aws-service-use-case-table)
- [8. Foundation model and LLM lifecycle](#8-foundation-model-and-llm-lifecycle)
- [9. Business use cases](#9-business-use-cases)
- [Commonly confused pairs](#commonly-confused-pairs)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Self-check checklist](#self-check-checklist)

---

### 1. Transformer mechanics

<details>
<summary>Tokenization → embeddings → self-attention pipeline · embedding-model decision tree — tap to expand</summary>

| Stage | What happens |
|---|---|
| Input text | Raw text the model will process |
| Tokenization | Text split into tokens (**tokens ≠ words**) |
| Embeddings | Each token mapped to a numeric **vector** capturing meaning |
| Positional encoding | Added to embeddings so word order is preserved |
| Self-attention (× N layers) | Each token weighs the relevance of **every other token**, regardless of distance |
| Feed-forward network | Per-token transformation applied after attention |
| Output | Next-token probabilities, generated **one token at a time** |

- **Self-attention** is the defining innovation — a long-range link (e.g., resolving a pronoun several sentences back) costs no more to compute than a link between adjacent tokens.
- **Embedding** = the semantic representation; **vector** = the numeric array; **vector database** = where those arrays are stored/searched (e.g., Amazon OpenSearch Service, Aurora + `pgvector`, Amazon Kendra).

**Choosing an embedding model (work down only as far as needed):**

| Decision point | Choose | Cost |
|---|---|---|
| General-purpose model sufficient? → **Yes** | General-purpose model (e.g., Titan Text Embeddings) | **$** lowest |
| → No (poor retrieval) → domain specialized? → **No** | Larger general model or better chunking/hybrid search | **$$** |
| → **Yes** → fine-tuning justified? → **No** | Domain-specific pretrained embedding model | **$$** |
| → **Yes** — large labeled dataset, high-stakes accuracy | Fine-tune an embedding model (e.g., via SageMaker) | **$$$** highest |

</details>

### 2. Foundation model selection criteria

<details>
<summary>Cost/modality/latency/context-window checklist · Nova family table — tap to expand</summary>

| Factor | Ask yourself |
|---|---|
| Cost | Per-token (on-demand) or **Provisioned Throughput** |
| Modality | Does the model accept/produce the needed input/output types? |
| Latency | Real-time needs a fast (usually smaller) model |
| Context window | Does the input (+ retrieved context) fit without chunking? |
| Fine-tuning support | Can this model/provider be fine-tuned or continued-pre-trained? |
| Model size, accuracy, licensing | Validate with **Amazon Bedrock Model Evaluation**; check licensing |

**Amazon Nova family (pick by modality first, not one ladder):**

| Variant | Modality (in → out) | Use for |
|---|---|---|
| **Nova Micro** | Text → text | High-volume, cheap, latency-sensitive text |
| **Nova Lite** | Text/image/video → text | Lightweight multimodal chat, doc Q&A with images |
| **Nova Pro** | Text/image/video → text | Balanced multimodal RAG, moderate agentic reasoning |
| **Nova Premier** | Text/image/video → text | Complex multi-step multimodal reasoning; distillation teacher |
| **Nova Canvas** | Text/image → image | Studio-quality image generation/editing |
| **Nova Reel** | Text/image → video | Short-form video generation (async) |
| **Nova Sonic** | Speech → speech | Real-time speech-to-speech |

- Weigh **all** stated constraints together — the biggest model isn't automatically correct if latency or cost is called out.

</details>

### 3. Prompt-engineering techniques

<details>
<summary>Zero-shot, few-shot, CoT, negative prompting vs. fine-tuning — tap to expand</summary>

| Technique | What it does | Changes model weights? |
|---|---|---|
| **Zero-shot** | Ask the model to perform a task with **no examples** | No |
| **Few-shot** | Include a **small number of example pairs** | No |
| **Chain-of-thought (CoT)** | Reason **step by step** before the final answer | No |
| **Negative prompting** | Tell the model what **not** to include | No |
| **Fine-tuning** *(contrast)* | Retrains the model's weights on labeled examples | **Yes** |

- A well-formed prompt = **instruction + context + input data + output indicator**.
- **Prompt injection** — malicious input overrides a prompt's instructions; mitigated with input validation + **Guardrails for Amazon Bedrock**.
- Multi-step arithmetic/logic → **chain-of-thought**. Inconsistent format/style → **few-shot**. Unwanted image elements → **negative prompting**.

</details>

### 4. Inference parameters

<details>
<summary>Temperature, top-p, top-k, max tokens, stop sequences — tap to expand</summary>

| Parameter | Low / small value | High / large value |
|---|---|---|
| **Temperature** | More focused, deterministic | More creative, varied |
| **Top-p** (nucleus sampling) | Narrower candidate pool | Wider candidate pool |
| **Top-k** | Small k → safer | Large k → more diverse |
| **Max tokens** | Shorter responses, may truncate | Longer responses allowed |
| **Stop sequences** | A matched string stops generation immediately | — |

- **Order of operations:** temperature reshapes the distribution **first**, then top-p/top-k prune the pool, then the token is sampled.
- None of these parameters reduce **hallucination** or enforce a content policy — only **RAG** (facts) and **Guardrails** (safety) do that.

</details>

### 5. RAG architecture

<details>
<summary>6-step ingest → retrieve → generate pipeline — tap to expand</summary>

| Step | What happens | AWS |
|---|---|---|
| 1. Ingest | Source documents loaded from a data source | Amazon S3, SharePoint, Salesforce |
| 2. Chunk + embed | Documents split into chunks; each converted to a vector | Amazon Titan Text Embeddings |
| 3. Index | Vectors stored for similarity search | Amazon OpenSearch Service, Aurora + `pgvector`, Amazon Kendra |
| 4. Query embed | The user's question is embedded the same way | Same embeddings model |
| 5. Retrieve | Vector store returns the closest chunks | **Knowledge Bases for Amazon Bedrock** |
| 6. Augment + generate | Retrieved chunks + question passed to an LLM | Bedrock FM (e.g., Claude, Titan) |

- **RAG grounds answers in retrieved data at inference time — it does not retrain the model.**
- **Fabricated/wrong facts** → **RAG**. **Wrong tone, format, or style** → prompt engineering or fine-tuning, not RAG.

</details>

### 6. GenAI advantages and disadvantages

<details>
<summary>4 advantages · hallucination vs. inaccuracy vs. nondeterminism — tap to expand</summary>

| Advantage | What it means |
|---|---|
| **Adaptability** | One FM handles many tasks via prompting alone |
| **Responsiveness** | Interactive, real-time conversational responses |
| **Simplicity / creativity** | Produces novel content, not just a label or number |
| **Scalability** | One deployed FM serves many use cases/users |

| Risk | Definition | Primary mitigation |
|---|---|---|
| **Hallucination** | Fluent, confident output that is **factually incorrect or fabricated** | **RAG** |
| **Interpretability (lack of)** | "Black box" — hard to explain *why* | Human review |
| **Inaccuracy** | Simply wrong/outdated/low quality, distinct from confident fabrication | Model evaluation, RAG, fine-tuning |
| **Nondeterminism** | Same prompt → **different outputs on different runs** | Lower **temperature**/top-p/top-k |
| **Cost / compute intensity** | Large FMs and retries can be expensive | Right-size model, cap max tokens |
| **Prompt injection** | Malicious input overrides prompt instructions | **Guardrails for Amazon Bedrock** |

- **Hallucination vs. inaccuracy:** hallucination is *confidently fabricating specifics*; inaccuracy is just *being wrong/low quality*.

</details>

### 7. AWS service → use case table

<details>
<summary>Bedrock, Knowledge Bases, Agents, Guardrails, Q Business, Q Developer — tap to expand</summary>

| If the scenario says... | Use... |
|---|---|
| "single API across multiple FMs, fully managed" | **Amazon Bedrock** |
| "ground FM answers in our own data without retraining" | **Knowledge Bases for Amazon Bedrock** (RAG) |
| "FM should plan/execute multi-step tasks calling our APIs/Lambda" | **Agents for Amazon Bedrock** |
| "block harmful content, denied topics, redact PII" | **Guardrails for Amazon Bedrock** |
| "compare FM outputs to pick the best model" | **Amazon Bedrock Model Evaluation** |
| "reserved capacity for steady, high-volume, predictable performance" | **Provisioned Throughput** |
| "pre-built enterprise assistant grounded in company data out of the box" | **Amazon Q Business** |
| "code suggestions, explanations, security scans" | **Amazon Q Developer** |
| "deploy/fine-tune pretrained FMs with deep infra control" | **Amazon SageMaker JumpStart** |
| "free, no-code, quick FM experimentation" | **PartyRock** |
| "text-to-image generation/editing" | **Amazon Nova Canvas** |
| "text/image-to-video generation" | **Amazon Nova Reel** |
| "real-time, bidirectional speech-to-speech" | **Amazon Nova Sonic** |

- **Golden rule:** the more "out of the box" a scenario needs, the more the answer shifts toward **Amazon Q** or **PartyRock**; the more custom/production-grade, the more it shifts toward **Bedrock** or **SageMaker JumpStart**.

</details>

### 8. Foundation model and LLM lifecycle

<details>
<summary>6-stage lifecycle · stage-3 adaptation options (lightest to heaviest) — tap to expand</summary>

| # | Stage | AWS |
|---|---|---|
| 1 | Scope the use case | — |
| 2 | Select a foundation model | Amazon Bedrock, SageMaker JumpStart |
| 3 | Adapt and customize | Bedrock prompt console; Knowledge Bases; fine-tuning; continued pre-training |
| 4 | Evaluate the model | Amazon Bedrock Model Evaluation |
| 5 | Deploy and integrate | Bedrock API or a SageMaker endpoint |
| 6 | Monitor quality, cost, latency, safety; iterate | CloudWatch metrics; Guardrails |

| Option | Touch |
|---|---|
| Prompt engineering | No training |
| RAG | Ground in own data at inference time, **no weight changes** |
| Fine-tuning | Train weights on **labeled** data |
| Continued pre-training | Train weights on **unlabeled** corpus |

- **Exam tip:** "Up-to-date or proprietary data without retraining" → **RAG**. "Specific tone, format, or labeled task" → **fine-tuning**. Full pretraining of a new FM is almost never the correct answer.

</details>

### 9. Business use cases

<details>
<summary>Content creation, summarization, chatbots, code generation, search — tap to expand</summary>

| Use case | AWS |
|---|---|
| **Content creation** | Amazon Bedrock, Amazon Nova Canvas |
| **Summarization** | Amazon Bedrock |
| **Chatbots / conversational assistants** | Amazon Bedrock (custom) or **Amazon Q Business** (pre-built) |
| **Code generation** | **Amazon Q Developer** |
| **Search** (semantic search) | Amazon OpenSearch Service + Bedrock Knowledge Bases |

- Also exam-relevant: **translation**, **personalization**, **data augmentation** (synthetic training data), **text-to-image/video** generation.
- **"One company, five initiatives"** scenario shape: map each initiative to exactly **one** use case and **one** AWS service.

</details>

---

### Commonly confused pairs

<details>
<summary>10 pairs the exam loves to swap — tap to expand</summary>

| Pair | How to tell them apart |
|---|---|
| **Hallucination** vs. **Inaccuracy** | Hallucination = confidently **fabricated**; Inaccuracy = just **wrong/low quality** |
| **Top-p** vs. **Top-k** | Top-p = **cumulative-probability** threshold; Top-k = **fixed count** of top tokens |
| **RAG** vs. **Fine-tuning** | RAG = grounds facts at inference, **no weight change**; Fine-tuning = retrains weights |
| **Fine-tuning** vs. **Continued pre-training** | Fine-tuning = **labeled** task data; Continued pre-training = **unlabeled** domain corpus |
| **Few-shot** vs. **Chain-of-thought** | Few-shot = example pairs for **format/style**; CoT = step-by-step **reasoning** |
| **Amazon Q Business** vs. **PartyRock** vs. **SageMaker JumpStart** | Q Business = pre-built enterprise assistant; PartyRock = no-code prototyping; JumpStart = deep infra control |
| **Foundation model (FM)** vs. **Large language model (LLM)** | LLM is a **text-specialized subset** of FMs, not a synonym for all FMs |
| **Guardrails** vs. **inference parameters** | Only **Guardrails** enforces a content policy; temperature/top-p/top-k never do |
| **Nova Micro/Lite/Pro/Premier** vs. **Nova Canvas/Reel/Sonic** | First four climb in cost/capability; the latter three are picked by **output modality**, not a pricier rung |
| **Embedding** vs. **Vector** vs. **Vector database** | Embedding = semantic meaning; Vector = the numeric array; Vector database = where it's stored/searched |

</details>

### Rapid-fire key terms

<details>
<summary>26 key terms — tap to expand</summary>

| Term | Definition |
|---|---|
| **Generative AI** | Subset of deep learning where models generate new content |
| **Foundation model (FM)** | Large model pretrained on broad data, adaptable via prompting/RAG/fine-tuning |
| **Large language model (LLM)** | An FM specialized for natural-language text |
| **Multimodal model** | Accepts/generates more than one content type |
| **Token** | The basic unit of text an LLM reads/generates; **tokens ≠ words** |
| **Embedding** | A numeric representation capturing semantic meaning |
| **Vector** | The numeric array an embedding is stored as |
| **Vector database** | Stores/queries embeddings by similarity |
| **Semantic search** | Search by meaning, not exact keyword match |
| **Transformer architecture** | Neural network architecture behind most modern LLMs |
| **Self-attention** | Lets each token weigh the relevance of every other token |
| **Context window** | Max tokens (input + often output) a model can consider at once |
| **Zero-shot / few-shot prompting** | No examples vs. a few example pairs in the prompt |
| **Chain-of-thought prompting** | Step-by-step reasoning before the final answer |
| **Negative prompting** | Explicitly stating what to exclude |
| **Temperature / top-p / top-k** | Inference parameters controlling randomness of next-token sampling |
| **Retrieval Augmented Generation (RAG)** | Grounds FM answers in retrieved data, without retraining |
| **Fine-tuning** | Further training an FM's weights on labeled data |
| **Continued pre-training** | Further training on a large unlabeled corpus |
| **Hallucination** | Confident but fabricated/incorrect output |
| **Nondeterminism** | Same prompt, different output across runs |
| **Prompt injection** | Malicious input overriding prompt instructions |
| **Amazon Bedrock** | Managed access to multiple FMs via one API |
| **Amazon Q Business / Q Developer** | Pre-built enterprise assistant / generative AI coding companion |
| **Provisioned Throughput** | Reserved Bedrock capacity for steady, high-volume traffic |
| **Data augmentation** | Using generative AI to create synthetic training data |

</details>

---

## Self-check checklist

Tick each fact you can already state cold — anything unchecked is what to
re-read in the [Fast Track](README.md) or [Ultra Fast
Track](ULTRA-FAST-LEARN.md) before the exam.

- [ ] **Hallucination** (confidently fabricated specifics) ≠ **inaccuracy** (just wrong/low quality).
- [ ] Lowering **temperature** reduces nondeterminism but does **not** eliminate hallucination risk.
- [ ] **Top-p** = cumulative-probability threshold; **top-k** = fixed count of top tokens.
- [ ] High temperature + narrow top-p/top-k can still be repetitive — the three parameters interact.
- [ ] **Few-shot prompting** changes nothing about model weights; only **fine-tuning** retrains them.
- [ ] Fabricated/wrong **facts** → **RAG**; wrong **tone/format/style** → prompt engineering or fine-tuning.
- [ ] RAG grounds answers in data — it does **not** restore interpretability or guarantee correctness.
- [ ] A scenario with **two or three constraints at once** wants you to weigh all of them, not just pick the biggest model.
- [ ] "No-code, quick experimentation" → **PartyRock**; "pre-built, grounded out of the box" → **Amazon Q Business**; "deep infra control" → **SageMaker JumpStart**.
- [ ] Content-safety questions need **Guardrails for Amazon Bedrock** — inference parameters alone cannot enforce a content policy.
- [ ] GenAI has four **advantages** too (adaptability, responsiveness, simplicity/creativity, scalability) — don't recall only the disadvantages.
- [ ] "Up-to-date/proprietary data without retraining" → **RAG**; "specific tone, format, or labeled task" → **fine-tuning**.
- [ ] On the embedding-model decision tree, jumping straight to fine-tuning "to be safe" wastes cost.
- [ ] A "one company, five initiatives" scenario maps each initiative to exactly one use case and one AWS service.

---

For the full explanations, worked examples, mini-quizzes, and practice
questions this cheat sheet intentionally omits, go back to the [Domain 2
fast track](README.md), the [Ultra Fast Track](ULTRA-FAST-LEARN.md), or
the [full Domain 2 guide](../domain-2-fundamentals-of-generative-ai.md).

[← Back to the Domain 2 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md)
