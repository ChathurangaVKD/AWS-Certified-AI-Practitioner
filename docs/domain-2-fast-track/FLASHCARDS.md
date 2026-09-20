# Domain 2 Flashcards: Fundamentals of Generative AI

**Flashcard deck** · fast track: [`docs/domain-2-fast-track/README.md`](README.md) · ultra fast track: [`docs/domain-2-fast-track/ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · **Last verified:** 2026-09-05

A companion active-recall / spaced-repetition deck, not a new source of
material — every card below is a front/back reformat of a fact already
verified in the [Ultra Fast Track](ULTRA-FAST-LEARN.md) cram sheet. Cards
are ordered to match that file's own section order, so studying the deck
top to bottom reinforces the domain's structure. One question or term per
card, one-to-two-line answer, no re-explaining.

For app-based spaced repetition (Anki, Quizlet, etc.), import
[`flashcards.tsv`](flashcards.tsv) directly — it's the same 92 cards, same
order, tab-separated with no header row.

## 1. Transformer mechanics

| Front | Back |
|---|---|
| What are the stages of transformer processing, in order? | Input text → tokenization → embeddings → positional encoding → self-attention (×N layers) → feed-forward network → output (next-token probabilities, one token at a time). |
| What is the defining innovation of the transformer architecture? | Self-attention — each token weighs the relevance of every other token, regardless of distance, at the same computational cost. |
| Embedding vs. vector vs. vector database — what's the difference? | Embedding = the semantic representation; vector = the numeric array it's stored as; vector database = where those arrays are stored/searched (e.g., OpenSearch, Aurora + pgvector, Kendra). |
| General-purpose embedding model sufficient — which model, and cost profile? | A general-purpose model (e.g., Titan Text Embeddings); $, lowest latency, good on broad domains. |
| Poor retrieval quality, domain specialized (legal/medical/financial), fine-tuning not yet justified — which embedding model? | A domain-specific pretrained embedding model; $$, meaningfully better domain accuracy. |
| Large labeled dataset, high-stakes accuracy — which embedding model approach? | Fine-tune an embedding model (e.g., via SageMaker); $$$, highest accuracy, needs retraining as data drifts. |
| Why is jumping straight to fine-tuning an embedding model "to be safe" usually wrong? | It adds training and maintenance cost for accuracy a cheaper option already delivers. |

## 2. Foundation model selection criteria

| Front | Back |
|---|---|
| What are the six foundation model selection factors? | Cost, modality, latency, context window, fine-tuning/customization support, model size/accuracy/licensing. |
| What validates a foundation model's accuracy claim before committing? | Amazon Bedrock Model Evaluation. |
| Nova Micro — modality and use? | Text → text; lowest cost; high-volume, cheap, latency-sensitive text (simple chat, classification). |
| Nova Lite — modality and use? | Text/image/video → text; low cost; lightweight multimodal chat, document Q&A with images. |
| Nova Pro — modality and use? | Text/image/video → text; moderate cost; balanced multimodal RAG, moderate agentic reasoning. |
| Nova Premier — modality and use? | Text/image/video → text; highest cost; most complex multi-step multimodal reasoning, teacher model for distillation. |
| Nova Canvas — modality and use? | Text/image → image; priced per image; studio-quality image generation/editing. |
| Nova Reel — modality and use? | Text/image → video; priced per second; short-form video generation (async). |
| Nova Sonic — modality and use? | Speech → speech; priced per duration; real-time speech-to-speech (voice assistants, IVR). |
| How do Micro/Lite/Pro/Premier relate to Canvas/Reel/Sonic in the Nova family? | Micro/Lite/Pro/Premier climb together in cost/latency/capability; Canvas/Reel/Sonic are separate models picked by output modality, not a pricier rung on the same ladder. |

## 3. Prompt-engineering techniques

| Front | Back |
|---|---|
| Zero-shot prompting — what is it, and does it change model weights? | Ask the model to perform a task with no examples; no weight change. |
| Few-shot prompting — what is it, and does it change model weights? | Include a small number of example input/output pairs; no weight change. |
| Chain-of-thought (CoT) prompting — what is it, and does it change model weights? | Instruct the model to reason step by step before the final answer; no weight change. |
| Negative prompting — what is it, and does it change model weights? | Tell the model what not to include or do (common in image generation); no weight change. |
| Fine-tuning vs. the prompting techniques above — does it change model weights? | Yes — fine-tuning retrains the model's weights on labeled examples; it is not a prompting technique. |
| What four elements make up a well-formed prompt? | Instruction + context + input data + output indicator. |
| What is prompt injection, and how is it mitigated? | Malicious input tries to override a prompt's original instructions; mitigated with input validation + Guardrails for Amazon Bedrock. |
| Multi-step arithmetic/logic task, improve accuracy without retraining — which technique? | Chain-of-thought. |
| Inconsistent format/style across calls — which technique? | Few-shot prompting. |
| Unwanted elements in generated images — which technique? | Negative prompting. |

## 4. Inference parameters

| Front | Back |
|---|---|
| Temperature — what does it control, low vs. high? | Randomness of next-token choice; low = focused/deterministic/repeatable, high = creative/varied/random. |
| Top-p (nucleus sampling) — what does it control, low vs. high? | Cumulative-probability candidate pool; low = narrower pool (safer, less varied), high = wider pool (more diverse). |
| Top-k — what does it control, low vs. high? | Fixed-size candidate pool (k most-likely tokens); low = safer/less varied, high = more diverse. |
| What is the order of operations among temperature, top-p, and top-k? | Temperature reshapes the distribution first, then top-p/top-k prune the candidate pool, then the next token is sampled. |
| Do temperature/top-p/top-k/max-tokens/stop-sequences reduce hallucination or enforce a content policy? | No — only RAG (facts) and Guardrails for Amazon Bedrock (safety) do that. |
| Which inference parameters are the *direct* cost/latency levers? | Max tokens and stop sequences; temperature/top-p/top-k are only indirect levers (fewer retries). |

## 5. RAG architecture

| Front | Back |
|---|---|
| What are the six steps of RAG, in order? | Ingest → chunk + embed → index → query embed → retrieve → augment + generate. |
| Does RAG retrain the model? | No — RAG grounds answers in retrieved data at inference time; it never touches model weights. |
| What is RAG's primary purpose? | Reduce hallucination by grounding output in actual source data. |
| Fabricated/wrong facts vs. wrong tone/format/style — RAG or prompt engineering/fine-tuning? | Fabricated/wrong facts → RAG; wrong tone/format/style → prompt engineering or fine-tuning, not RAG. |
| What AWS feature wires the full RAG pipeline together without custom retrieval code? | Knowledge Bases for Amazon Bedrock. |

## 6. GenAI advantages and disadvantages

| Front | Back |
|---|---|
| What are the four GenAI advantages? | Adaptability, responsiveness, simplicity/creativity, scalability. |
| Hallucination — definition and primary mitigation? | Fluent, confident output that is factually incorrect or fabricated; primary mitigation is RAG. |
| Hallucination vs. inaccuracy — what's the difference? | Hallucination is confidently fabricating specifics; inaccuracy is just being wrong/low quality. |
| Nondeterminism — definition and primary mitigation? | Same prompt → different outputs on different runs; lower temperature/top-p/top-k reduces (doesn't eliminate) it. |
| What does Guardrails for Amazon Bedrock address, and what does it NOT address? | Safety/compliance (harmful content, denied topics, PII redaction) — not factual accuracy. |

## 7. AWS service → use case table

| Front | Back |
|---|---|
| Single API across multiple FMs, fully managed, minimal infra. | Amazon Bedrock. |
| Ground FM answers in our own data without retraining. | Knowledge Bases for Amazon Bedrock (RAG). |
| FM should plan/execute multi-step tasks calling our APIs/Lambda. | Agents for Amazon Bedrock. |
| Block harmful content, denied topics, redact PII. | Guardrails for Amazon Bedrock. |
| Compare FM outputs to pick the best model for a task. | Amazon Bedrock Model Evaluation. |
| Reserved capacity for steady, high-volume, predictable performance. | Provisioned Throughput. |
| Pre-built enterprise assistant grounded in company data/systems out of the box. | Amazon Q Business. |
| Code suggestions, explanations, security scans, AWS resource Q&A. | Amazon Q Developer. |
| Deploy/fine-tune pretrained FMs with deep infra control, mix with SageMaker MLOps. | Amazon SageMaker JumpStart. |
| Free, no-code, quick FM experimentation/prototyping. | PartyRock. |
| Golden rule for choosing among Bedrock, SageMaker JumpStart, Amazon Q, and PartyRock? | The more "out of the box" a scenario needs, the more the answer shifts toward Amazon Q/PartyRock; the more custom/production-grade control it needs, the more it shifts toward Bedrock/SageMaker JumpStart. |

## 8. Foundation model and LLM lifecycle

| Front | Back |
|---|---|
| What are the six stages of the FM/LLM lifecycle, in order? | Scope the use case → select a foundation model → adapt and customize → evaluate the model → deploy and integrate → monitor and iterate. |
| Stage 3 adaptation options, lightest to heaviest touch? | Prompt engineering → RAG → fine-tuning → continued pre-training. |
| "Up-to-date or proprietary company data without retraining" — which adaptation option? | RAG. |
| "Learn a specific tone, format, or specialized labeled task" — which adaptation option? | Fine-tuning. |
| Is full pretraining of a brand-new FM usually the right answer for a business use case? | Almost never — a poor evaluation sends you back to stage 3 (prompt/retrieval/fine-tuning), long before pretraining a new FM. |

## 9. Business use cases

| Front | Back |
|---|---|
| Chatbots/conversational assistants — custom or pre-built AWS option? | Amazon Bedrock (custom) or Amazon Q Business (pre-built). |
| Code generation — which AWS service? | Amazon Q Developer. |
| Semantic search — what does it use, and which AWS services? | Embeddings/vector similarity; Amazon OpenSearch Service + Bedrock Knowledge Bases. |
| "Assistant grounded in enterprise data with minimal setup" — which service is preferred? | Amazon Q Business, over a custom Bedrock build from scratch. |
| What does "data augmentation" mean in a GenAI business-use-case context? | Using generative AI to create synthetic training data for other ML models. |

## Rapid-fire key terms

| Front | Back |
|---|---|
| Generative AI | Subset of deep learning where models generate new content rather than only predicting a label or number. |
| Foundation model (FM) | Large model pretrained on broad data, adaptable to many tasks via prompting, RAG, or fine-tuning. |
| Large language model (LLM) | An FM specialized for natural-language text; a subset of FMs, not a synonym for all FMs. |
| Multimodal model | Accepts and/or generates more than one content type (text, image, audio, video); input and output modalities can differ. |
| Token | The basic unit of text an LLM reads/generates; tokens ≠ words (pricing and context windows are measured in tokens). |
| Embedding | A numeric representation capturing semantic meaning. |
| Vector | The numeric array an embedding is stored as. |
| Vector database | Stores/queries embeddings by similarity. |
| Semantic search | Search by meaning (embeddings/vectors), not exact keyword match. |
| Transformer architecture | The neural network architecture behind most modern LLMs, built on self-attention. |
| Self-attention | Lets each token weigh the relevance of every other token, regardless of distance. |
| Context window | Max tokens (input + often output) a model can consider at once. |
| Zero-shot / few-shot prompting | No examples vs. a few example input/output pairs in the prompt. |
| Chain-of-thought prompting | Step-by-step reasoning before the final answer. |
| Negative prompting | Explicitly stating what to exclude. |
| Temperature / top-p / top-k | Inference parameters controlling randomness/diversity of next-token sampling. |
| Retrieval Augmented Generation (RAG) | Grounds FM answers in retrieved external data at inference time, without retraining. |
| Fine-tuning | Further training an FM's weights on labeled data. |
| Continued pre-training | Further training an FM on a large corpus of unlabeled domain data, before any task-specific fine-tuning. |
| Hallucination | Confident but fabricated/incorrect output. |
| Nondeterminism | Same prompt, different output across runs. |
| Prompt injection | Malicious input overriding prompt instructions. |
| Amazon Bedrock | Managed access to multiple FMs via one API. |
| Amazon Q Business / Amazon Q Developer | Pre-built enterprise assistant / generative AI coding companion. |
| Provisioned Throughput | Reserved Bedrock capacity for steady, high-volume traffic. |
| Data augmentation | Using generative AI to create synthetic training data for other ML models. |

## Common exam traps checklist

| Front | Back |
|---|---|
| Top-p vs. top-k — what's the difference? | Top-p = cumulative-probability threshold; top-k = fixed count of top tokens — don't swap these. |
| What's the trap in listing only GenAI's downsides? | GenAI has four advantages too (adaptability, responsiveness, simplicity/creativity, scalability) — don't recall only the risks. |
| "One company, five initiatives" business-use-case scenario — what's the mapping rule? | Map each initiative to exactly one use case and one AWS service, never more than one of each. |

---

[← Back to the full Domain 2 guide](../domain-2-fundamentals-of-generative-ai.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md) · [Interactive cheat sheet →](CHEAT-SHEET.md)
