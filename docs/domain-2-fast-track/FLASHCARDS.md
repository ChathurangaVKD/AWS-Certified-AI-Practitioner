# Domain 2 Flashcards: Fundamentals of Generative AI

**Spaced-repetition companion deck** · fast track: [`README.md`](README.md) · cram sheet: [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · plain-text import file: [`flashcards.tsv`](flashcards.tsv)

One card per testable concept from the Domain 2 Ultra Fast Track cram sheet, ordered to match that file's own section order so studying this deck reinforces the domain's structure. Front/back only, no prose -- for active recall or spaced repetition. `flashcards.tsv` holds the identical cards as a header-less, two-column (front, back) tab-separated file, importable as-is into Anki or Quizlet.

## 1. Transformer mechanics

| Front | Back |
|---|---|
| Transformer stage: raw text the model will process | Input text |
| Transformer stage: text split into word/sub-word units | Tokenization (tokens != words) |
| Transformer stage: each token mapped to a numeric vector capturing meaning | Embeddings |
| Transformer stage: added to embeddings so word order is preserved | Positional encoding |
| Transformer stage: each token weighs the relevance of every other token, regardless of distance | Self-attention (x N layers) |
| Transformer stage: per-token transformation applied after attention | Feed-forward network |
| Transformer stage: next-token probabilities, generated one token at a time | Output |
| What is the defining innovation of the transformer architecture? | Self-attention -- computes a relevance weight between every pair of tokens directly, so long-range links cost no more than adjacent-token links |
| Embedding vs. vector vs. vector database -- distinguish them | Embedding = the semantic representation; vector = the numeric array it's stored as; vector database = where those arrays are stored/searched |
| Embedding-model decision: is a general-purpose model sufficient? | Yes -> use a general-purpose model (e.g., Titan Text Embeddings) -- lowest cost/latency |
| Embedding-model decision: poor retrieval quality but not domain-specialized | Try a larger general model or better chunking/hybrid search first |
| Embedding-model decision: domain-specialized, but fine-tuning not justified by data volume/accuracy bar | Use a domain-specific pretrained embedding model |
| Embedding-model decision: large labeled dataset + high-stakes accuracy | Fine-tune an embedding model (e.g., via SageMaker) -- highest accuracy, needs retraining as data drifts |
| Trap: jumping straight to embedding fine-tuning "to be safe" | Usually just adds training/maintenance cost for accuracy a cheaper option already delivers |

## 2. Foundation model selection criteria

| Front | Back |
|---|---|
| FM selection factor: cost | Per-token (on-demand) or Provisioned Throughput; bigger/more capable models cost more per token |
| FM selection factor: modality | Does the model accept/produce the needed input/output types (text, image, audio, video)? |
| FM selection factor: latency | Real-time/interactive use cases need a fast (usually smaller) model; batch/async tolerates more |
| FM selection factor: context window | Is the input plus any retrieved context small enough to fit without chunking? |
| FM selection factor: fine-tuning / customization support | Can this model/provider be fine-tuned or continued-pre-trained if needed? |
| FM selection factor: model size, accuracy, licensing | Parameter count as a rough capability/cost proxy; validate accuracy with Amazon Bedrock Model Evaluation; check compliance/licensing |
| Amazon Nova Micro | Text -> text, lowest cost; high-volume, cheap, latency-sensitive text (simple chat, classification) |
| Amazon Nova Lite | Text/image/video -> text, low cost; lightweight multimodal chat, document Q&A with images |
| Amazon Nova Pro | Text/image/video -> text, moderate cost; balanced multimodal RAG, moderate agentic reasoning |
| Amazon Nova Premier | Text/image/video -> text, highest cost; complex multi-step multimodal reasoning, teacher model for distillation |
| Amazon Nova Canvas | Text/image -> image, priced per image; studio-quality image generation/editing |
| Amazon Nova Reel | Text/image -> video, priced per second; short-form video generation (async) |
| Amazon Nova Sonic | Speech -> speech, priced per duration; real-time speech-to-speech (voice assistants, IVR) |
| Trap: Nova Micro/Lite/Pro/Premier vs. Canvas/Reel/Sonic | Micro-Premier climb together in cost/capability on one ladder; Canvas/Reel/Sonic are separate models picked by output modality, not a pricier rung on that ladder |

## 3. Prompt-engineering techniques

| Front | Back |
|---|---|
| Prompting technique: no examples given | Zero-shot |
| Prompting technique: a small number of example input/output pairs | Few-shot |
| Prompting technique: reason step by step before the final answer | Chain-of-thought (CoT) |
| Prompting technique: tell the model what not to include or do | Negative prompting (common in image generation) |
| Which prompting/customization technique actually changes model weights? | Only fine-tuning -- zero-shot, few-shot, CoT, and negative prompting do not |
| What are the four parts of a well-formed prompt? | Instruction + context + input data + output indicator |
| Scenario: multi-step arithmetic/logic task, improve accuracy without retraining | Chain-of-thought |
| Scenario: inconsistent format/style across calls | Few-shot |
| Scenario: unwanted elements in generated images | Negative prompting |
| What mitigates prompt injection? | Input validation + Guardrails for Amazon Bedrock |

## 4. Inference parameters

| Front | Back |
|---|---|
| Inference parameter: randomness of next-token choice | Temperature |
| Inference parameter: cumulative-probability candidate pool | Top-p (nucleus sampling) |
| Inference parameter: fixed-size candidate pool of k most-likely tokens | Top-k |
| Inference parameter: cap on response length | Max tokens (maximum length) |
| Inference parameter: halts generation when a matched string appears | Stop sequences |
| Order of operations for temperature, top-p, and top-k | Temperature reshapes the distribution first, then top-p/top-k prune the candidate pool, then the next token is sampled |
| Trap: low temperature + high top-p/top-k | Still mostly deterministic -- little probability mass reaches the wide pool |
| Trap: high temperature + low top-p/top-k | Still narrow/repetitive -- the pruning step throws away the long tail temperature flattened in |
| Do temperature/top-p/top-k/max-tokens/stop-sequences reduce hallucination or enforce a content policy? | No -- only RAG (facts) and Guardrails for Amazon Bedrock (safety) do that |
| Which inference parameters are the direct cost/latency levers? | Max tokens and stop sequences; temperature/top-p/top-k affect cost/latency only indirectly (fewer retries, shorter completions) |

## 5. RAG architecture

| Front | Back |
|---|---|
| RAG step 1: ingest | Source documents loaded from a data source (Amazon S3, SharePoint, Salesforce) |
| RAG step 2: chunk + embed | Documents split into chunks; each chunk converted to an embedding vector |
| RAG step 3: index | Vectors stored in a vector store (Amazon OpenSearch Service, Aurora + pgvector, Amazon Kendra) |
| RAG step 4: query embed | The user's question is embedded with the same embeddings model |
| RAG step 5: retrieve | Vector store returns the chunks closest to the query vector, managed by Knowledge Bases for Amazon Bedrock |
| RAG step 6: augment + generate | Retrieved chunks + original question passed as a prompt to an LLM, which generates a grounded answer |
| Does RAG retrain the model? | No -- it grounds answers in retrieved data at inference time only |
| RAG's primary purpose | Reduce hallucination by grounding output in actual source data |
| Scenario: fabricated/wrong facts | Reach for RAG |
| Scenario: wrong tone, format, or style | Reach for prompt engineering or fine-tuning, not RAG |
| What is Knowledge Bases for Amazon Bedrock? | The managed, no-retrain way to wire the full RAG pipeline together without custom retrieval code |

## 6. GenAI advantages and disadvantages

| Front | Back |
|---|---|
| GenAI advantage: one FM handles many tasks via prompting alone | Adaptability |
| GenAI advantage: interactive, real-time conversational responses | Responsiveness |
| GenAI advantage: produces novel content/ideas instead of just a label or number | Simplicity / creativity |
| GenAI advantage: one deployed FM serves many use cases/users | Scalability |
| Risk: fluent, confident output that is factually incorrect or fabricated | Hallucination -- primary mitigation is RAG |
| Risk: black box, hard to explain why an FM produced a given output | Lack of interpretability -- mitigated by human review |
| Risk: output is simply wrong/outdated/low quality (not confident fabrication) | Inaccuracy -- mitigated by model evaluation, RAG, fine-tuning on better data |
| Risk: same prompt, different outputs on different runs | Nondeterminism -- mitigated by lowering temperature/top-p/top-k |
| Risk: large FMs, long context windows, retries can be expensive at scale | Cost / compute intensity -- right-size model, cap max tokens, lower temperature to cut retries |
| Risk: malicious input overrides/manipulates the original prompt instructions | Prompt injection -- mitigated by input validation + Guardrails for Amazon Bedrock |
| Trap: hallucination vs. inaccuracy | Hallucination is confidently fabricating specifics; inaccuracy is just being wrong/low quality |
| What does Guardrails for Amazon Bedrock address? | Safety/compliance (harmful content, denied topics, PII redaction) -- not factual accuracy |

## 7. AWS service -> use case table

| Front | Back |
|---|---|
| Scenario: single API across multiple FMs, fully managed, minimal infra | Amazon Bedrock |
| Scenario: ground FM answers in our own data without retraining | Knowledge Bases for Amazon Bedrock (RAG) |
| Scenario: FM should plan/execute multi-step tasks calling our APIs/Lambda | Agents for Amazon Bedrock |
| Scenario: block harmful content, denied topics, redact PII | Guardrails for Amazon Bedrock |
| Scenario: compare FM outputs to pick the best model for a task | Amazon Bedrock Model Evaluation |
| Scenario: reserved capacity for steady, high-volume, predictable performance | Provisioned Throughput |
| Scenario: pre-built enterprise assistant grounded in company data/systems out of the box | Amazon Q Business |
| Scenario: code suggestions, explanations, security scans, AWS resource Q&A | Amazon Q Developer |
| Scenario: deploy/fine-tune pretrained FMs with deep infra control, mix with SageMaker MLOps | Amazon SageMaker JumpStart |
| Scenario: free, no-code, quick FM experimentation/prototyping | PartyRock |
| Scenario: text-to-image generation/editing | Amazon Nova Canvas |
| Scenario: text/image-to-video generation | Amazon Nova Reel |
| Scenario: real-time, bidirectional speech-to-speech | Amazon Nova Sonic |
| Golden rule: more "out of the box" vs. more custom/production-grade control | Out-of-the-box shifts toward Amazon Q or PartyRock; custom/production-grade control shifts toward Amazon Bedrock or SageMaker JumpStart |

## 8. Foundation model and LLM lifecycle

| Front | Back |
|---|---|
| FM/LLM lifecycle stage 1 | Scope the use case -- define the problem; confirm generative AI is even the right fit |
| FM/LLM lifecycle stage 2 | Select a foundation model -- Amazon Bedrock, SageMaker JumpStart |
| FM/LLM lifecycle stage 3 | Adapt and customize -- Bedrock prompt console; Knowledge Bases; Bedrock custom models/JumpStart fine-tuning; Bedrock continued pre-training |
| FM/LLM lifecycle stage 4 | Evaluate the model -- Amazon Bedrock Model Evaluation |
| FM/LLM lifecycle stage 5 | Deploy and integrate -- Bedrock API (on-demand/Provisioned Throughput) or a SageMaker endpoint |
| FM/LLM lifecycle stage 6 | Monitor quality, cost, latency, safety; iterate -- CloudWatch metrics; Guardrails for Amazon Bedrock |
| Stage 3 adaptation option: no training, lightest touch | Prompt engineering (Bedrock prompt console) |
| Stage 3 adaptation option: ground in own data at inference time, no weight changes | RAG (Knowledge Bases for Amazon Bedrock) |
| Stage 3 adaptation option: train weights on labeled data | Fine-tuning (Bedrock custom models / SageMaker JumpStart fine-tuning) |
| Stage 3 adaptation option: train weights on unlabeled corpus, heaviest touch | Continued pre-training (Amazon Bedrock continued pre-training) |
| Where does a poor model evaluation (stage 4) send you back to? | Stage 3 -- a different prompt, retrieval strategy, or fine-tuning; not full pretraining of a new FM |
| Trap: up-to-date/proprietary company data without retraining vs. a specific tone/format/labeled task | RAG vs. fine-tuning, respectively; full pretraining of a new FM is almost never the correct exam answer |
| Few-shot prompting vs. fine-tuning -- which changes model weights? | Few-shot changes no weights; fine-tuning retrains them |

## 9. Business use cases

| Front | Back |
|---|---|
| Business use case: draft marketing copy, product descriptions, emails, images from a prompt | Content creation (Amazon Bedrock, Amazon Nova Canvas) |
| Business use case: condense long documents/transcripts/tickets into short summaries | Summarization (Amazon Bedrock) |
| Business use case: natural-language help, often RAG-grounded in company data | Chatbots / conversational assistants (Amazon Bedrock custom, or Amazon Q Business pre-built) |
| Business use case: generate, explain, complete, refactor code from natural language | Code generation (Amazon Q Developer) |
| Business use case: find results by meaning via embeddings/vector similarity | Search / semantic search (Amazon OpenSearch Service + Bedrock Knowledge Bases) |
| Scenario: assistant grounded in enterprise data with minimal setup | Prefer the purpose-built Amazon Q Business over a custom Bedrock build from scratch |
| Trap: "one company, five initiatives" scenario shape | Map each stated initiative to exactly one use case and one AWS service, never more than one of each |

## Rapid-fire key terms

| Front | Back |
|---|---|
| Generative AI | Subset of deep learning where models generate new content rather than only predicting a label or number |
| Foundation model (FM) | Large model pretrained on broad data, adaptable to many tasks via prompting, RAG, or fine-tuning |
| Large language model (LLM) | An FM specialized for natural-language text; a subset of FMs, not a synonym for all FMs |
| Multimodal model | Accepts and/or generates more than one content type (text, image, audio, video); input and output modalities can differ |
| Token | The basic unit of text an LLM reads/generates; tokens != words (pricing and context windows are measured in tokens) |
| Embedding | A numeric representation capturing semantic meaning |
| Vector | The numeric array an embedding is stored as |
| Vector database | Stores/queries embeddings by similarity |
| Semantic search | Search by meaning (embeddings/vectors), not exact keyword match |
| Transformer architecture | The neural network architecture behind most modern LLMs, built on self-attention |
| Self-attention | Lets each token weigh the relevance of every other token, regardless of distance |
| Context window | Max tokens (input + often output) a model can consider at once |
| Zero-shot / few-shot prompting | No examples vs. a few example input/output pairs in the prompt |
| Chain-of-thought prompting | Step-by-step reasoning before the final answer |
| Negative prompting | Explicitly stating what to exclude |
| Temperature / top-p / top-k | Inference parameters controlling randomness/diversity of next-token sampling |
| Retrieval Augmented Generation (RAG) | Grounds FM answers in retrieved external data at inference time, without retraining |
| Fine-tuning | Further training an FM's weights on labeled data |
| Continued pre-training | Further training an FM on a large corpus of unlabeled domain data, before any task-specific fine-tuning |
| Hallucination | Confident but fabricated/incorrect output |
| Nondeterminism | Same prompt, different output across runs |
| Prompt injection | Malicious input overriding prompt instructions |
| Amazon Bedrock | Managed access to multiple FMs via one API |
| Amazon Q Business / Amazon Q Developer | Pre-built enterprise assistant / generative AI coding companion |
| Provisioned Throughput | Reserved Bedrock capacity for steady, high-volume traffic |
| Data augmentation | Using generative AI to create synthetic training data for other ML models |

## Common exam traps

| Front | Back |
|---|---|
| Trap: hallucination vs. inaccuracy | Confidently fabricated specifics (hallucination) vs. just wrong/low quality (inaccuracy) -- don't conflate them |
| Trap: does lowering temperature eliminate hallucination risk? | No -- it reduces nondeterminism, but hallucination risk comes from training data/RAG, not sampling |
| Trap: top-p vs. top-k | Top-p = cumulative-probability threshold; top-k = fixed count of top tokens -- don't swap these |
| Trap: do temperature/top-p/top-k act independently? | No -- high temperature + narrow top-p/top-k can still be repetitive; low temperature + wide top-p/top-k can still be near-deterministic |
| Trap: does few-shot prompting change model weights? | No -- only fine-tuning retrains them |
| Trap: fabricated/wrong facts vs. wrong tone/format/style | Facts -> RAG; tone/format/style -> prompt engineering or fine-tuning, not RAG |
| Trap: does RAG restore interpretability or guarantee correctness? | No -- it only grounds answers in data |
| Trap: a scenario with two or three constraints at once (real-time + long documents + fixed budget) | Weigh all of them together, not just pick the biggest model |
| Trap: no-code quick experimentation vs. pre-built enterprise-grounded vs. deep infra control | PartyRock vs. Amazon Q Business vs. SageMaker JumpStart, respectively |
| Trap: can inference parameters alone enforce a content policy? | No -- content-safety questions need Guardrails for Amazon Bedrock |
| Trap: does GenAI have advantages, not just disadvantages? | Yes -- adaptability, responsiveness, simplicity/creativity, scalability; don't recall only the disadvantages side |
| Trap: up-to-date/proprietary data without retraining vs. specific tone/format/labeled task | RAG vs. fine-tuning; full pretraining of a new FM is almost never the correct exam answer |
| Trap: the embedding-model decision tree | Jumping straight to fine-tuning "to be safe" wastes cost -- work down only as far as a cheaper option's accuracy actually falls short |
| Trap: a "one company, five initiatives" business-use-case scenario | Maps each initiative to exactly one use case and one AWS service, never more than one of each |

---

**145 cards total.** For the full explanations behind any card, see the [fast track](README.md), the [Ultra Fast Track cram sheet](ULTRA-FAST-LEARN.md), or the [full Domain 2 guide](../domain-2-fundamentals-of-generative-ai.md).

[← Back to the Domain 2 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md)
