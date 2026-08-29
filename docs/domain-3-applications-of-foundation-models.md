# Domain 3: Applications of Foundation Models

[← Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md) · **Domain 3 of 5** · [Domain 4: Guidelines for Responsible AI →](domain-4-guidelines-for-responsible-ai.md)

**Last verified:** 2026-08-29

## Table of contents

- [1. Design considerations for foundation model applications](#1-design-considerations-for-foundation-model-applications)
- [2. Prompt engineering techniques](#2-prompt-engineering-techniques)
  - [Comparison table: prompt engineering techniques at a glance](#comparison-table-prompt-engineering-techniques-at-a-glance)
- [3. Retrieval Augmented Generation (RAG) and Amazon Bedrock Knowledge Bases](#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases)
- [4. Fine-tuning vs. continued pre-training vs. RAG vs. prompt engineering](#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering)
- [5. Amazon Bedrock features](#5-amazon-bedrock-features)
- [6. Vector databases and embeddings for search and retrieval](#6-vector-databases-and-embeddings-for-search-and-retrieval)
- [7. Evaluating foundation model performance](#7-evaluating-foundation-model-performance)
- [8. AWS infrastructure for generative AI workloads](#8-aws-infrastructure-for-generative-ai-workloads)
- [Worked example: implementing RAG for an internal policy-lookup assistant](#worked-example-implementing-rag-for-an-internal-policy-lookup-assistant)
- [Worked example: selecting a foundation model under multiple competing constraints](#worked-example-selecting-a-foundation-model-under-multiple-competing-constraints)
- [Comparison table: customization approaches for foundation model applications](#comparison-table-customization-approaches-for-foundation-model-applications)
- [Quick-reference cheat sheet](#quick-reference-cheat-sheet)
- [Key terms glossary](#key-terms-glossary)
- [Practice questions](#practice-questions)
- [Answer key and explanations](#answer-key-and-explanations)

## Domain overview

Domain 3 is the largest domain on the AWS Certified AI Practitioner
(AIF-C01) exam, making up roughly **28% of scored questions**. Where
[Domain 2](domain-2-fundamentals-of-generative-ai.md) tests whether you understand *what* generative AI and foundation
models (FMs) are, Domain 3 tests whether you can reason about how to
**build a real application on top of one** — how to choose a model for a
scenario, how to make it accurate and grounded in your own data, how to
customize its behavior, how to evaluate whether it's actually working, and
which AWS services and infrastructure you'd reach for at each step.

Concretely, this domain covers: design considerations for FM applications
(model selection, cost, latency, modality, customization options); prompt
engineering; Retrieval Augmented Generation (RAG) and **Amazon Bedrock
Knowledge Bases**; the trade-offs between prompt engineering, RAG,
fine-tuning, and continued pre-training; core **Amazon Bedrock** platform
features (model access, Agents, Guardrails, Knowledge Bases, model
evaluation, provisioned throughput); vector databases and embeddings; how
to evaluate FM performance (human evaluation, benchmark datasets, business
metrics); and the AWS infrastructure that powers generative AI workloads
(Amazon SageMaker, and the purpose-built ML chips AWS Trainium and AWS
Inferentia).

Expect heavily scenario-based questions: "a company needs X — which
customization approach / AWS service / chip fits best?" The exam rewards
knowing not just *what* each option does, but *when* to pick it over a
similar-sounding alternative — RAG vs. fine-tuning, Amazon Kendra vs. a
vector database, Trainium vs. Inferentia, on-demand vs. provisioned
throughput. This guide is organized so each of those decision points gets
its own explanation, a concrete AWS example, and an exam tip flagging the
tricky wording the real exam likes to use.

---

## 1. Design considerations for foundation model applications

Before writing a single prompt, an AIF-C01 candidate is expected to know
the factors that go into **choosing and architecting a foundation model
application**. The exam frames this as a set of design considerations you
weigh against each other, since improving one often costs you on another:

- **Model selection** — no single FM is best for every job. Selection
  criteria include: task fit (summarization vs. code generation vs.
  classification), context window size, supported modalities, accuracy on
  your use case, inference cost, latency, and whether the model can be
  customized (fine-tuned) if needed. On **Amazon Bedrock**, you can
  compare and swap foundation models from multiple providers (Amazon,
  Anthropic, AI21 Labs, Cohere, Meta, Mistral AI, Stability AI) behind a
  single unified API without re-architecting your application.
- **Cost** — generative AI inference is typically billed per input/output
  **token** (on-demand) or as a flat rate for reserved capacity
  (**provisioned throughput**, [Section 5](#5-amazon-bedrock-features)). Larger, more capable models
  cost more per token than smaller models. Cost is also driven by prompt
  length (more context = more input tokens) and how many customization
  steps (fine-tuning, continued pre-training) you invest in up front.
- **Latency** — the time to receive a response. Smaller models generally
  respond faster than larger ones; response **streaming** (returning
  tokens as they're generated) improves *perceived* latency for
  user-facing chat applications even when total generation time is
  unchanged. Latency-sensitive use cases (real-time chat, voice
  assistants) generally favor smaller, faster models or provisioned
  throughput to avoid variable on-demand queueing.
- **Modality** — whether the application needs to handle text, images,
  audio, video, or some combination (**multimodal**). Not every FM
  supports every modality — e.g., **Amazon Nova Canvas** and
  Stability AI models on Bedrock handle image generation, while Anthropic
  Claude models on Bedrock support multimodal (text + image) input.
  Choosing a model that doesn't support your required modality is a
  common exam distractor.
### Mini-quiz: check your understanding (Section 1)

Quick formative check before moving on — try each question, then expand
the answer.

1. A team is choosing between two foundation models for a voice assistant
   that must feel conversational and responsive. Which design
   consideration should weigh most heavily?
   A. Latency
   B. Modality
   C. Fine-tuning support
   D. Prompt template versioning

   <details><summary>Show answer</summary>

   **A — Latency.** A "conversational, responsive" voice assistant is a
   latency-sensitive use case, so the team should favor a smaller,
   faster model or provisioned throughput. Modality (B) only matters if
   the required input/output type is in question, which it isn't here;
   fine-tuning support (C) and prompt template versioning (D) are
   customization/tooling concerns, not what drives a real-time feel.

   </details>

2. Which pricing model is generally most cost-effective for a workload
   with unpredictable, spiky traffic?
   A. Provisioned throughput
   B. On-demand
   C. Continued pre-training
   D. Reserved model units regardless of volume

   <details><summary>Show answer</summary>

   **B — On-demand.** On-demand pricing (pay per token, no commitment)
   fits variable or unpredictable traffic best. Provisioned throughput
   (A, D) is cost-effective only for high, steady, predictable volume;
   continued pre-training (C) is a customization technique, not a
   pricing model.

   </details>

3. On Amazon Bedrock, what lets an application swap foundation models
   from different providers without re-architecting the application?
   A. A separate SDK per provider
   B. Amazon Bedrock's single, unified API across providers
   C. Fine-tuning every candidate model first
   D. Amazon Bedrock Agents

   <details><summary>Show answer</summary>

   **B — Amazon Bedrock's single, unified API across providers.**
   Bedrock exposes FMs from Amazon, Anthropic, AI21 Labs, Cohere, Meta,
   Mistral AI, and Stability AI behind one API, so switching models is a
   config change rather than a rewrite. A contradicts how Bedrock works;
   fine-tuning (C) is an optional customization step, not a prerequisite
   for swapping models; Agents (D) orchestrate multi-step tasks, they
   don't provide model-provider abstraction.

   </details>

---

## 2. Prompt engineering techniques

**Prompt engineering** is the practice of crafting the input (prompt) to a
foundation model to reliably get the output you want, without changing the
model's underlying weights. It is the cheapest, fastest customization
option and the exam's most detailed topic within "applications."

Key techniques:

- **Zero-shot prompting** — asking the model to perform a task with only
  an instruction and no examples (e.g., "Classify this review as positive
  or negative: ..."). Works well for simpler tasks a large, well-trained
  FM already generalizes to.
- **Few-shot prompting** — including a small number of example
  input/output pairs in the prompt before the actual task, so the model
  infers the desired pattern, format, or tone. Improves reliability on
  tasks with a specific expected output structure.
- **Chain-of-thought (CoT) prompting** — instructing the model to reason
  step-by-step (e.g., "think through this step by step") before giving a
  final answer, which improves accuracy on multi-step reasoning, math, and
  logic tasks.
- **Prompt templates** — reusable prompt structures with placeholders
  (e.g., `{customer_question}`) that standardize how an application
  constructs prompts, ensuring consistent instructions, tone, and format
  across many requests. **Amazon Bedrock Prompt Management** lets teams
  create, version, and share prompt templates.
- **Negative prompting** — explicitly telling the model what to avoid
  (e.g., "do not include pricing information" or, for image generation,
  "no text, no watermark") to steer output away from undesired content.
- **Prompt chaining / prompt flows** — breaking a complex task into a
  sequence of smaller prompts, where the output of one prompt feeds the
  input of the next. **Amazon Bedrock Prompt Flows** provides a visual
  builder for chaining prompts and other steps (like Knowledge Base
  lookups) into a single workflow.
- **System prompts / role prompting** — setting persistent instructions
  (persona, tone, constraints, guardrails on behavior) that apply across
  an entire conversation, separate from the user's individual turns.
- **Prompt injection** — a security risk, not a technique: a malicious
  user embeds instructions in their input designed to override the
  application's intended prompt/system instructions (e.g., "ignore all
  previous instructions"). Mitigations include input validation and
  **Guardrails for Amazon Bedrock** ([Section 5](#5-amazon-bedrock-features)).

**AWS example:** A retail company builds a support-ticket triage tool on
Amazon Bedrock. They use a **few-shot** prompt with five labeled example
tickets to teach the model their exact category taxonomy, add a
**negative prompt** instructing the model never to promise refunds, and
wrap it all in a versioned **prompt template** managed through Bedrock
Prompt Management so every application call uses a consistent, tested
prompt.

> **Exam tip:** Prompt engineering **never changes the model's weights** —
> it's the only customization option in [Section 4](#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering) that requires no
> training data and no training job, which is why it's always the
> cheapest and fastest to implement. If a scenario needs a multi-step
> reasoning improvement (math, logic) with no extra data or cost, the
> answer is almost always **chain-of-thought prompting**, not fine-tuning.

### Worked examples: the same task, four techniques

Concepts are easier to compare side by side. Below, the identical task —
classify a customer review as **Positive**, **Negative**, or **Neutral** —
is run through four techniques against the exact same input, so you can
see how the prompt changes and how that changes the output.

**Input review (same for all four examples):** "The product arrived two
days late and the box was a little dented, but everything inside works
perfectly and customer support was quick to apologize."

**1. Zero-shot prompting** — only an instruction, no examples.

Prompt:

```
Classify the sentiment of this customer review as Positive, Negative, or Neutral.

Review: "The product arrived two days late and the box was a little dented,
but everything inside works perfectly and customer support was quick to
apologize."
```

Model output:

```
Sentiment: Positive
```

Fast to write and cheap to run, but with no example to anchor it, the
model decides the output format on its own — here a single label, but a
different model or phrasing could just as easily return a full paragraph.

**2. Few-shot prompting** — a couple of labeled examples establish the
exact output format before the real task.

Prompt:

```
Classify each review's sentiment as Positive, Negative, or Neutral.
Respond in the format "Label: <one-sentence reason>".

Review: "Fast shipping and the item matched the description exactly."
Label: Positive: praises shipping speed and accuracy with no complaints.

Review: "Package never arrived and support never responded to my emails."
Label: Negative: describes a failed delivery and unresponsive support.

Review: "The product arrived two days late and the box was a little dented,
but everything inside works perfectly and customer support was quick to
apologize."
Label:
```

Model output:

```
Label: Positive: minor shipping and packaging issues are outweighed by a
fully functional product and a responsive apology from support.
```

The two labeled examples teach the model the exact `Label: <reason>`
format and the level of nuance expected, so the output is now reliably
structured instead of just a bare word.

**3. Chain-of-thought prompting** — the model reasons step-by-step before
committing to a label, which helps on a review with mixed signals like
this one.

Prompt:

```
Classify the sentiment of this review as Positive, Negative, or Neutral.
Think through the positive and negative signals in the review step by
step, then give your final answer on the last line as
"Final sentiment: <label>".

Review: "The product arrived two days late and the box was a little dented,
but everything inside works perfectly and customer support was quick to
apologize."
```

Model output:

```
Step 1 - Negative signals: late arrival, dented box.
Step 2 - Positive signals: product works perfectly, support apologized
quickly and took ownership.
Step 3 - Weighing them: the negative signals are about logistics, not the
product itself, and were promptly addressed; the positive signals are
about the core product and service experience.
Final sentiment: Positive
```

The visible reasoning makes the borderline call auditable — you can see
*why* the model landed on Positive instead of Neutral, which the bare
zero-shot label couldn't show you.

**4. Negative prompting** — an explicit constraint steers the model away
from an unwanted response shape.

Prompt:

```
Classify the sentiment of this review as Positive, Negative, or Neutral.
Do not answer Neutral for a review that describes a fully working product,
even if there is a delivery or packaging complaint. Do not include any
text besides the single word label.

Review: "The product arrived two days late and the box was a little dented,
but everything inside works perfectly and customer support was quick to
apologize."
```

Model output:

```
Positive
```

Without that constraint, a model faced with mixed signals like this one
might hedge and answer "Neutral"; explicitly ruling that out — and ruling
out extra commentary — forces a decisive, single-word answer suited for
automated downstream processing.

Put side by side, the trade-off is clear: zero-shot is cheapest but least
controllable, few-shot locks in format and nuance with a couple of
examples, chain-of-thought spends extra output tokens to make reasoning
on ambiguous cases auditable, and negative prompting is a cheap way to
eliminate one specific failure mode (here, over-using "Neutral" as a
hedge) without restructuring the whole prompt.

#### Mini-quiz: Test your understanding of prompt engineering techniques

Quick self-check before moving on — try to answer before reading the
explanation.

1. A team wants a model to produce consistently formatted output across
   many different application calls, using a reusable structure with
   placeholders like `{customer_name}`. Which technique fits best?
   A. Negative prompting
   B. Prompt template
   C. Fine-tuning
   D. Continued pre-training

   **Answer: B** — Prompt templates are reusable prompt structures with
   placeholders that standardize how an application constructs prompts, so
   every call gets a consistent instruction/format without retraining
   anything.

2. Which of the following is a security risk rather than a legitimate
   prompt engineering technique?
   A. Few-shot prompting
   B. Chain-of-thought prompting
   C. Prompt injection
   D. Prompt chaining

   **Answer: C** — Prompt injection is a malicious user embedding
   instructions designed to override the application's intended
   prompt/system instructions; it's a risk to mitigate (e.g., with
   Guardrails), not a technique to apply.

3. A developer breaks a complex task into a sequence of prompts, where the
   output of one feeds the input of the next, using Amazon Bedrock's
   visual builder for this. Which capability are they using?
   A. Amazon Bedrock Prompt Flows
   B. Amazon Bedrock Guardrails
   C. Amazon Bedrock Agents
   D. Amazon Bedrock model evaluation

   **Answer: A** — Amazon Bedrock Prompt Flows provides a visual builder
   for chaining prompts (and other steps, like Knowledge Base lookups)
   into a single workflow, which is prompt chaining in practice.

### Comparison table: prompt engineering techniques at a glance

Eight techniques were just introduced across four worked examples — the
table below puts all of them side by side against the dimensions the exam
actually tests (cost, complexity, control over output, use-case fit, and
the keywords a question stem tends to use to signal each one), so the
trade-offs can be scanned at a glance instead of re-reading the narrative
above:

| Technique | Cost | Complexity | Control over output | Best use-case fit | Exam keywords |
|---|---|---|---|---|---|
| **Zero-shot prompting** | Lowest — just an instruction, no examples | Lowest — single prompt, no setup | Low — model decides format/structure on its own | Simple tasks a large, well-trained FM already generalizes to | "no examples," "instruction only," "simplest task" |
| **Few-shot prompting** | Low — a few example pairs added to the prompt | Low/medium — must author and maintain good examples | Medium/high — examples anchor the exact output format and tone | Tasks needing a specific, consistent output structure | "example input/output pairs," "learn the format," "consistent structure" |
| **Chain-of-thought (CoT) prompting** | Low — extra output tokens for the reasoning steps | Medium — prompt must explicitly request step-by-step reasoning | High for reasoning tasks — makes the logic auditable | Multi-step reasoning, math, logic, ambiguous/borderline cases | "step by step," "reasoning," "multi-step," "show your work" |
| **Prompt templates** | Lowest — one-time authoring, reused across calls | Low — placeholders defined once, versioned centrally | High for consistency — every call gets the same instructions/format | Standardizing prompts across many application calls | "reusable structure," "placeholders," "{variable}," "Bedrock Prompt Management" |
| **Negative prompting** | Lowest — a short added constraint | Lowest — one or two extra sentences in the prompt | Medium — rules out specific unwanted outputs, doesn't dictate the whole shape | Eliminating one specific failure mode (a hedge answer, unwanted content/text) | "do not include," "avoid," "no text/watermark," "steer away from" |
| **Prompt chaining / Prompt Flows** | Medium — multiple prompt calls per task, more tokens overall | Medium/high — must design and orchestrate the sequence of steps | High — each stage's output is validated/shaped before feeding the next | Complex multi-step tasks that are unreliable as a single prompt | "sequence of prompts," "output feeds the next," "Amazon Bedrock Prompt Flows," "visual builder" |
| **System prompts / role prompting** | Lowest — set once per conversation/application | Low — a single persistent instruction block | High for persona/tone/guardrails across an entire conversation | Enforcing a consistent persona, tone, or behavioral constraint app-wide | "persona," "role," "persistent instructions," "across the conversation" |
| **Prompt injection** | N/A — not a technique, a security risk | N/A — attacker-controlled, not designed by the application | None (from the defender's perspective) — attacker attempts to hijack output | Something to *mitigate*, not apply — via input validation and Guardrails | "ignore previous instructions," "malicious input," "override the system prompt" |

> **Exam tip:** If a table row reads "N/A" or "not a technique," that's
> your cue — the exam likes to plant **prompt injection** in a list of
> techniques and ask which one is actually a *security risk* rather than
> a legitimate customization tool (see question 2 above). For everything
> else, notice that cost and complexity track together (zero-shot,
> negative prompting, and system prompts are all cheap, low-setup ways to
> nudge output) while chain-of-thought and prompt chaining spend more
> tokens/effort in exchange for auditability or multi-step reliability.

---

## 3. Retrieval Augmented Generation (RAG) and Amazon Bedrock Knowledge Bases

**Retrieval Augmented Generation (RAG)** is a technique that retrieves
relevant information from an external knowledge source at query time and
inserts it into the prompt, so the FM generates its response grounded in
that retrieved content instead of relying solely on what it learned during
training. RAG directly addresses two core FM limitations: **stale
knowledge** (the model's training data has a cutoff date) and
**hallucination** (the model confidently generating incorrect
information) — by giving the model authoritative source text to draw
from.

The typical RAG pipeline:

1. **Ingestion** — source documents (PDFs, HTML, text files, etc.,
   typically from **Amazon S3**) are loaded.
2. **Chunking** — documents are split into smaller passages so retrieval
   can return focused, relevant sections rather than entire documents.
3. **Embedding** — each chunk is converted into a numeric vector
   (**embedding**) using an embeddings model (e.g., **Amazon Titan Text
   Embeddings**), capturing its semantic meaning.
4. **Indexing/storage** — the embeddings are stored in a **vector
   database** ([Section 6](#6-vector-databases-and-embeddings-for-search-and-retrieval)) for fast similarity search.
5. **Retrieval** — at query time, the user's question is embedded the same
   way, and the vector store returns the most semantically similar chunks.
6. **Augmentation and generation** — the retrieved chunks are inserted into
   the prompt as context, and the FM generates an answer grounded in that
   context.

**Visual summary — RAG system architecture:** the diagram below traces one
query end-to-end, from source documents being indexed offline through to a
cited answer being returned at query time, and marks which AWS service
typically handles each stage:

```mermaid
graph TD
    subgraph Ingestion["Offline: ingestion & indexing"]
        DOCS["Source documents\n(Amazon S3)"] --> CHUNK["Chunking"]
        CHUNK --> EMBED1["Embedding model\n(Amazon Titan Text Embeddings /\nCohere Embed on Bedrock)"]
        EMBED1 --> STORE["Vector store\n(Amazon OpenSearch Serverless/Service,\nAurora + pgvector, or Amazon Kendra)"]
    end

    subgraph QueryTime["Query time"]
        USER["User question"] --> EMBED2["Embed the question\n(same embeddings model)"]
        EMBED2 --> RETRIEVE["Retrieval:\nsimilarity search against\nthe vector store"]
        STORE -. indexed chunks .-> RETRIEVE
        RETRIEVE --> AUGMENT["Augmentation:\nretrieved chunks inserted\ninto the prompt as context"]
        AUGMENT --> LLM["LLM invocation\n(Amazon Bedrock FM)"]
        LLM --> RESPONSE["Response with citations"]
    end
```

**Amazon Bedrock Knowledge Bases** is the fully managed AWS implementation
of this entire pipeline: point it at a data source (typically an S3
bucket), and it automatically handles ingestion, chunking, embedding
(using a Bedrock embeddings model you choose), and storage/indexing in a
supported vector store (Amazon OpenSearch Serverless by default, or
Amazon OpenSearch Service, Amazon Aurora with the pgvector extension,
Amazon RDS for PostgreSQL, Redis Enterprise Cloud, MongoDB Atlas, or
Pinecone). Your application calls the `Retrieve` or `RetrieveAndGenerate`
API and Bedrock handles the retrieval-plus-prompting for you.

**AWS example:** A software company wants an internal chatbot that
answers employee questions using the company's constantly updated internal
wiki, without retraining a model every time the wiki changes. They set up
an **Amazon Bedrock Knowledge Base** pointed at an S3 bucket synced from
the wiki, using **Amazon OpenSearch Serverless** as the vector store and
**Amazon Titan Text Embeddings** to generate embeddings. When an employee
asks a question, Bedrock retrieves the most relevant wiki passages and
generates a grounded answer citing them — and when the wiki updates, they
simply re-sync the S3 data source instead of retraining anything.

> **Exam tip:** RAG **does not modify the foundation model's weights** —
> it changes what's in the *prompt*, not the model itself. If a scenario's
> goal is "keep responses current with frequently changing data" or
> "reduce hallucination by grounding answers in our own documents,"
> **RAG / Amazon Bedrock Knowledge Bases** is almost always the answer —
> not fine-tuning, which is comparatively slow/expensive to update and
> doesn't inherently reduce hallucination on facts outside the fine-tuning
> data.

#### Mini-quiz: Test your understanding of RAG and Amazon Bedrock Knowledge Bases

Quick self-check before moving on — try to answer before reading the
explanation.

1. Which two foundation model limitations does RAG directly address?
   A. High inference cost and slow latency
   B. Stale knowledge and hallucination
   C. Limited context window and lack of multimodal support
   D. Prompt injection and toxic output

   **Answer: B** — RAG grounds generation in retrieved, authoritative
   source text, which directly counters a model's training-data cutoff
   (stale knowledge) and its tendency to confidently generate incorrect
   information (hallucination).

2. In the RAG pipeline, what is the purpose of the chunking step?
   A. Converting text into numeric vectors
   B. Splitting documents into smaller passages so retrieval can return
      focused, relevant sections
   C. Storing embeddings in a vector database for fast similarity search
   D. Generating the final answer grounded in retrieved context

   **Answer: B** — Chunking splits source documents into smaller passages
   *before* embedding, so retrieval returns focused sections instead of
   entire documents; converting to vectors is embedding (A), storing them
   is indexing (C), and producing the final answer is generation (D).

3. Which Amazon Bedrock Knowledge Bases API call lets an application send a
   user question and receive an answer generated from automatically
   retrieved context in a single call?
   A. Retrieve
   B. RetrieveAndGenerate
   C. InvokeModel
   D. CreateKnowledgeBase

   **Answer: B** — `RetrieveAndGenerate` performs the retrieval-plus-
   prompting-plus-generation steps together; `Retrieve` (A) only returns
   the matching chunks without generating an answer, and the other two
   options aren't Knowledge Bases retrieval/generation calls.

### Vector store decision guide: OpenSearch vs. Aurora + pgvector vs. Amazon Kendra

The RAG pipeline above names three AWS options for the "indexing/storage"
step — **Amazon OpenSearch**, **Amazon Aurora with pgvector**, and
**Amazon Kendra** — and the exam expects you to pick the right one from a
scenario description, not just recognize the names. They aren't
interchangeable: OpenSearch and Aurora/pgvector are vector databases *you*
architect and query, while Kendra is a fully managed enterprise search
service that hides the embeddings/indexing layer entirely. The table below
compares them on the dimensions the exam tests most.

| Dimension | Amazon OpenSearch (Service / Serverless) | Amazon Aurora (PostgreSQL) + pgvector | Amazon Kendra |
|---|---|---|---|
| **Hybrid search support** | Native — a built-in **vector engine** does k-NN vector search alongside traditional keyword/full-text search in the same query. Strongest hybrid-search story of the three. | Possible (combine a SQL `WHERE` filter or Postgres full-text search with a `pgvector` similarity query) but you assemble it yourself — no single built-in "hybrid" query type. | Built in and automatic — Kendra's ranking model blends semantic and keyword relevance internally; you don't configure it. |
| **Embedding model options** | Bring your own — you pick an embeddings model (e.g., **Amazon Titan Text Embeddings**, Cohere Embed) and generate vectors yourself, then index them. Full control over which model, and you can change models later. | Bring your own, same as OpenSearch — embeddings are computed outside the database and stored as a `vector` column type via SQL. | None to choose — Kendra generates and manages relevance signals internally; there's no user-facing "pick an embeddings model" step. |
| **Management overhead** | Moderate (OpenSearch Service — you size and manage a cluster/domain) to low (**OpenSearch Serverless** — AWS autoscales capacity, still your index to design). | Low if the team already operates Aurora/RDS PostgreSQL — it's normal database administration plus enabling and tuning the `pgvector` extension and its index type. | Lowest — fully managed; no cluster, index, or embeddings pipeline to build, size, or patch. Point it at a data source connector and it handles the rest. |
| **Scalability model** | Horizontal — add nodes/shards (OpenSearch Service) or let capacity auto-scale with load (OpenSearch Serverless); built for large, high-throughput vector + text workloads. | Scales with the underlying Aurora database — storage auto-scales, compute scales vertically or via read replicas; vector search performance is bounded by the relational engine and pgvector index. | Scales automatically and transparently with document volume and number of connectors; AWS manages capacity behind the scenes. |
| **Exam keywords that signal this choice** | "hybrid search," "keyword *and* semantic search," "large-scale vector search," "default vector store for Bedrock Knowledge Bases." | "we already run Aurora/PostgreSQL," "query embeddings with SQL," "avoid standing up a separate search service." | "enterprise search," "automatic relevance ranking," "no infrastructure to manage," "connectors to S3/SharePoint/Salesforce," "natural-language search without building a RAG pipeline." |

**Decision tree:** the flowchart below turns the table above into a
sequence of yes/no questions — the fastest way to work an exam scenario
that describes requirements instead of naming a service:

```mermaid
flowchart TD
    START(["Choosing a vector store /\nsearch backend for RAG?"])
    START --> Q1{"Do you need hybrid search —\nkeyword AND vector search in\none query, at large scale?"}
    Q1 -->|"YES"| OS["AMAZON OPENSEARCH\n(Service or Serverless)\nbuilt-in vector engine +\nkeyword search, bring your\nown embedding model"]
    Q1 -->|"NO"| Q2{"Do you already run\nAurora/PostgreSQL and want to\nquery embeddings with SQL?"}
    Q2 -->|"YES"| PGV["AURORA + PGVECTOR\n(bring your own embeddings,\nquery via familiar SQL,\nnormal DB administration)"]
    Q2 -->|"NO"| Q3{"Do you want a fully managed\nservice with built-in connectors\n(S3, SharePoint, Salesforce) and\nno embeddings pipeline to build?"}
    Q3 -->|"YES"| KEN["AMAZON KENDRA\n(managed relevance ranking,\nzero infrastructure to operate)"]
    Q3 -->|"NO"| RECHECK["Re-check requirements —\nyou likely still need OpenSearch\nor Aurora/pgvector with a\ncustom embeddings pipeline"]
```

**Worked scenario — Amazon OpenSearch:** A retail company needs its
product-search RAG assistant to combine exact filtering (SKU codes, brand
names) with semantic similarity over product descriptions, at a scale of
tens of millions of documents and unpredictable traffic spikes during
sales events. The requirement for *both* keyword and vector search in one
query, at large scale, with autoscaling, points to **Amazon OpenSearch
Serverless** with its vector engine.

**Worked scenario — Aurora with pgvector:** A fintech startup already
stores all of its account and transaction metadata in **Amazon Aurora
PostgreSQL** and wants to add semantic search over its compliance
documents so support staff can ask natural-language questions. The team
knows SQL well and doesn't want to operate a second, dedicated search
service just for this one feature. Because the data already lives in
Aurora and the team wants to query embeddings with familiar SQL rather
than adopt new infrastructure, **Aurora PostgreSQL with the pgvector
extension** is the fit.

**Worked scenario — Amazon Kendra:** A company wants employees to search
natural-language questions across documents scattered over S3, SharePoint,
and Salesforce, with automatic relevance ranking, and explicitly does not
want to build or manage an embeddings pipeline or a vector index — "a
company wants automatic relevance ranking without managing
infrastructure." That combination — multiple document-repository
connectors, managed ranking, zero infrastructure — is the signature of
**Amazon Kendra**, not a vector database the team would have to architect
itself.

> **Exam tip:** If a scenario says the team **chooses an embeddings model**
> and **manages a vector index**, it's OpenSearch or Aurora/pgvector — and
> between those two, "we already run PostgreSQL/Aurora" points to
> **pgvector**, while "we need hybrid keyword + vector search at scale"
> points to **OpenSearch**. If the scenario emphasizes **no embeddings
> pipeline to build** and **automatic relevance ranking** over existing
> enterprise repositories, it's **Amazon Kendra**. [Section 6](#6-vector-databases-and-embeddings-for-search-and-retrieval)
> goes deeper on vector databases and embeddings in general.

---

## 4. Fine-tuning vs. continued pre-training vs. RAG vs. prompt engineering

The exam expects you to place these four customization approaches on a
single spectrum and pick the right one for a scenario:

- **Prompt engineering** — no training, no extra data beyond what's in the
  prompt. Cheapest and fastest. Limited by the model's context window and
  by what the base model already "knows." Covered in [Section 2](#2-prompt-engineering-techniques).
- **Retrieval Augmented Generation (RAG)** — no training; augments prompts
  with retrieved external data at query time. Best for grounding responses
  in **frequently changing or proprietary knowledge** without retraining.
  Covered in [Section 3](#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases).
- **Fine-tuning** — further trains a copy of a pretrained FM on a
  smaller, **labeled** dataset of your own input/output examples, updating
  the model's weights so it reliably produces a particular style,
  format, tone, or task behavior. Requires more time, cost, and ML
  expertise than prompting or RAG, and updates require re-running the
  fine-tuning job. On Bedrock, **fine-tuning creates a custom model** that
  typically must be accessed via **provisioned throughput** ([Section 5](#5-amazon-bedrock-features)).
- **Continued pre-training (a.k.a. domain adaptation)** — further trains a
  pretrained FM on a large volume of **unlabeled**, domain-specific text
  using the same self-supervised objective as original pretraining (e.g.,
  predicting the next token). It deepens the model's general knowledge and
  vocabulary of a domain (e.g., legal, medical, or a company's internal
  jargon) rather than teaching it a specific labeled task. It's more
  data- and compute-intensive than fine-tuning and doesn't require labeled
  input/output pairs.

**Visual summary — comparison matrix:** the diagram below lines up all
four approaches side by side across the five dimensions the exam tests
most (cost, complexity, accuracy, speed to implement, and data
requirements), so the trade-offs can be scanned at a glance instead of
re-reading the narrative above:

```mermaid
graph LR
    subgraph PE["Prompt engineering"]
        PE_COST["Cost: Lowest"]
        PE_COMPLEXITY["Complexity: Lowest -\nno training pipeline"]
        PE_ACCURACY["Accuracy: Limited by base\nmodel + context window"]
        PE_SPEED["Speed: Fastest -\nminutes to iterate"]
        PE_DATA["Data: None beyond\nthe prompt itself"]
    end

    subgraph RAG_G["RAG"]
        RAG_COST["Cost: Low"]
        RAG_COMPLEXITY["Complexity: Low/medium -\nretrieval pipeline to build"]
        RAG_ACCURACY["Accuracy: High for current/\nproprietary, grounded facts"]
        RAG_SPEED["Speed: Fast -\nhours to days to stand up"]
        RAG_DATA["Data: Unlabeled external\nknowledge source (documents)"]
    end

    subgraph FT["Fine-tuning"]
        FT_COST["Cost: High"]
        FT_COMPLEXITY["Complexity: High -\ntraining job + ML expertise"]
        FT_ACCURACY["Accuracy: High for the\nspecific trained task/style"]
        FT_SPEED["Speed: Slow -\ndays to weeks per training run"]
        FT_DATA["Data: Labeled\ninput/output example pairs"]
    end

    subgraph CPT["Continued pre-training"]
        CPT_COST["Cost: Highest"]
        CPT_COMPLEXITY["Complexity: Highest -\nlarge-scale self-supervised training"]
        CPT_ACCURACY["Accuracy: Deepens domain\nfluency, not one specific task"]
        CPT_SPEED["Speed: Slowest -\nweeks or more"]
        CPT_DATA["Data: Large volume of\nunlabeled domain-specific text"]
    end

    PE --> RAG_G --> FT --> CPT
```

**How to decide:**

| Need | Best fit |
|---|---|
| Change tone/format/style reliably for a specific task, have labeled examples | Fine-tuning |
| Deepen the model's understanding of domain-specific language/concepts from large unlabeled text | Continued pre-training |
| Ground answers in current, frequently changing, or proprietary knowledge without retraining | RAG |
| Quick behavior adjustment, no training data, lowest cost/fastest to iterate | Prompt engineering |

**Decision tree:** the flowchart below is the fastest way to work an exam
scenario — read the symptom the question describes, follow the matching
branch, and land on the customization approach it implies:

```mermaid
flowchart TD
    START(["Need to customize an FM's behavior?"])
    START --> Q1{"Is it a factuality/context\nproblem — answers must reflect\ncurrent, proprietary, or\nfrequently changing knowledge?"}
    Q1 -->|"YES"| RAG["RAG\n(retrieve external data\nat query time, no retraining)"]
    Q1 -->|"NO"| Q2{"Is it a style/format\nproblem — tone, structure, or\nbehavior fixable with better\ninstructions and no extra data?"}
    Q2 -->|"YES"| PE["PROMPT ENGINEERING\n(zero/few-shot, templates,\nchain-of-thought)"]
    Q2 -->|"NO"| Q3{"Is it narrow-task behavior —\ndo you have LABELED input/output\nexamples to teach one exact\ntask, tone, or format?"}
    Q3 -->|"YES"| FT["FINE-TUNING\n(train on labeled examples;\naccessed via provisioned throughput)"]
    Q3 -->|"NO"| Q4{"Does the model need new domain\nvocabulary from a large volume\nof UNLABELED training data?"}
    Q4 -->|"YES"| CPT["CONTINUED PRE-TRAINING\n(self-supervised training on\nunlabeled domain-specific text)"]
```

**Quick reference (if–then):** the same branches as one-line lookups, for
the fastest possible exam-time recall:

- Data changes frequently or is proprietary, but model weights shouldn't
  change → **RAG**
- Just need better formatting, tone, or output style, with no extra
  training data → **prompt engineering**
- Model needs to reliably perform a new, narrow, proprietary task and you
  have labeled input/output examples for it → **fine-tuning**
- Model needs broader domain vocabulary/fluency from a large body of
  unlabeled text, not one specific task → **continued pre-training**

These are not mutually exclusive — a production application commonly
combines several, e.g., prompt engineering **and** RAG together, or a
fine-tuned model accessed **through** a RAG pipeline.

**AWS example:** A legal-tech company builds a contract-analysis
assistant. They start with **prompt engineering** (fastest to prototype).
They add **Amazon Bedrock Knowledge Bases (RAG)** so the assistant can
cite the specific contract clauses it's answering about. Because outputs
must always follow a strict, firm-specific summary format, they then
**fine-tune** a Bedrock model on hundreds of labeled example
summaries in that exact format. Separately, because the firm's contracts
are dense with specialized legal terminology poorly represented in general
web text, they also evaluate **continued pre-training** on a large corpus
of unlabeled legal documents to improve the base model's grasp of legal
language before fine-tuning on top of it.

> **Exam tip:** The single most common trap: a scenario says "the company
> wants the model to always have access to the latest product catalog" —
> this is **RAG**, not fine-tuning, because fine-tuning bakes knowledge
> into static weights that go stale. Conversely, "the company wants every
> response to follow an exact required format/tone, and has example
> data" is **fine-tuning**. Remember **fine-tuning needs labeled
> input/output pairs; continued pre-training needs only unlabeled
> domain text** — that labeled-vs-unlabeled distinction is exactly what
> the exam tests between these two.

#### Mini-quiz: Test your understanding of customization approach trade-offs

Quick self-check before moving on — try to answer before reading the
explanation.

1. Which customization approach requires **labeled** input/output example
   pairs to update the model's weights toward a specific task or style?
   A. Prompt engineering
   B. RAG
   C. Fine-tuning
   D. None of these change the model's weights

   **Answer: C** — Fine-tuning trains a copy of a pretrained FM on a
   smaller, labeled dataset of input/output examples, updating its weights
   for a specific behavior; prompt engineering and RAG never touch the
   model's weights at all.

2. Which approach trains on a large volume of **unlabeled** domain-specific
   text using the original self-supervised pretraining objective, to
   deepen a model's general domain fluency rather than teach one task?
   A. RAG
   B. Continued pre-training
   C. Prompt engineering
   D. Fine-tuning

   **Answer: B** — Continued pre-training deepens domain knowledge and
   vocabulary using large volumes of unlabeled text, unlike fine-tuning,
   which needs labeled task-specific examples.

3. A company wants a generative AI assistant to always reflect the latest
   version of a product catalog that changes daily, without retraining a
   model every day. Which approach best fits?
   A. Fine-tuning
   B. Continued pre-training
   C. RAG
   D. Prompt engineering alone, with no external data

   **Answer: C** — RAG retrieves current external data at query time
   without any retraining, exactly fitting a frequently changing data
   source; fine-tuning and continued pre-training both bake knowledge into
   static weights that would need daily retraining to stay current.

---

## 5. Amazon Bedrock features

**Amazon Bedrock** is AWS's fully managed service for building generative
AI applications on top of foundation models, without managing any
infrastructure. Its core features, each tested individually on the exam:

- **Model access** — Bedrock provides a single, unified API to access FMs
  from multiple third-party and Amazon providers. Before use, an AWS
  account must explicitly **request model access** in the Bedrock console
  for each model. This lets applications swap FMs with minimal code
  changes.
- **Amazon Bedrock Agents** — orchestrates multi-step tasks by letting an
  FM reason about a user's request, break it into steps, and invoke
  external **action groups** (API calls, backed by AWS Lambda functions)
  and Knowledge Bases to complete the task — for example, checking order
  status via a company API and then answering a follow-up question from a
  Knowledge Base, all within one conversational session. Agents follow a
  reasoning-and-acting loop (plan → invoke a tool → observe the result →
  continue) to complete multi-step goals autonomously.
- **Guardrails for Amazon Bedrock** — a configurable safety layer applied
  to model inputs/outputs: denied topics, content filters, word filters,
  sensitive information (PII) filters, and contextual grounding checks
  (covered in depth in the [Domain 4 study guide](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai), since it's primarily a
  responsible-AI control — but the exam also tests it here as a Bedrock
  platform feature you attach to any model or Agent).
- **Amazon Bedrock Knowledge Bases** — the managed RAG feature described
  in [Section 3](#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases): automatic ingestion, chunking, embedding, and retrieval
  over your own data.
- **Model evaluation** — Bedrock lets you run **evaluation jobs** to
  compare FMs or assess a specific model's quality before choosing it for
  production, in two modes:
  - **Automatic evaluation** — uses built-in metrics (e.g., accuracy,
    robustness, toxicity) computed against built-in or your own
    prompt datasets — fast, low-cost, and objective, but limited to
    metrics that can be computed programmatically.
  - **Human evaluation** — a human work team (your own employees, or an
    AWS-managed team) reviews and scores model outputs on subjective
    criteria (e.g., relevance, style, friendliness) that automatic metrics
    can't capture.
- **Provisioned throughput** — lets you purchase dedicated inference
  capacity (measured in **model units**) for a model, for a 1-month or
  6-month commitment, guaranteeing consistent throughput and latency
  regardless of other customers' demand. It's the pricing/capacity mode
  required to use **custom (fine-tuned or continued-pre-trained)
  models** in most cases, and it's generally cost-effective only for
  **high, consistent, predictable** request volumes — as opposed to
  **on-demand** pricing (pay per token, no commitment), which fits
  variable or unpredictable traffic.

**AWS example:** An airline builds a Bedrock Agent that lets customers
change flight bookings conversationally: the Agent calls the airline's
booking API (via an action group backed by Lambda) to look up a
reservation, consults a **Knowledge Base** for baggage-policy questions,
and has **Guardrails** attached to block requests unrelated to travel.
Before launch, the team runs a Bedrock **automatic model evaluation** job
to compare candidate models on accuracy and toxicity, then a **human
evaluation** job to judge tone quality. At launch, because traffic volume
is high and predictable (peak booking season), they purchase **provisioned
throughput** instead of paying on-demand rates.

> **Exam tip:** Match the keyword to the feature: "the assistant needs to
> take actions / call APIs / complete multi-step tasks" → **Agents**;
> "block harmful or off-topic content" → **Guardrails**; "answer from our
> own documents" → **Knowledge Bases**; "compare model quality
> objectively/at scale" → **automatic evaluation**; "judge subjective
> quality like tone" → **human evaluation**; "guarantee consistent
> throughput for a custom/fine-tuned model at high, steady volume" →
> **provisioned throughput**; "unpredictable/low/spiky volume, pay only
> for what's used" → **on-demand**.

#### Mini-quiz: Test your understanding of Amazon Bedrock features

Quick self-check before moving on — try to answer before reading the
explanation.

1. Which Bedrock feature lets an FM plan a multi-step task and invoke
   external APIs via action groups?
   A. Guardrails for Amazon Bedrock
   B. Amazon Bedrock Agents
   C. Amazon Bedrock model evaluation
   D. Provisioned throughput

   **Answer: B** — Agents orchestrate multi-step tasks by letting an FM
   reason about a request, break it into steps, and invoke external action
   groups (API calls via Lambda) and Knowledge Bases.

2. Which Bedrock capability blocks denied topics and filters sensitive
   information (PII) from a model's inputs and outputs?
   A. Amazon Bedrock Knowledge Bases
   B. Amazon Bedrock Agents
   C. Guardrails for Amazon Bedrock
   D. Model access

   **Answer: C** — Guardrails is the configurable safety layer covering
   denied topics, content filters, word filters, PII filters, and
   contextual grounding checks.

3. A team expects high, steady, predictable request volume for a custom
   fine-tuned model in production and wants guaranteed, consistent
   throughput. Which capacity option should they choose?
   A. On-demand pricing
   B. Provisioned throughput
   C. Automatic model evaluation
   D. Requesting model access

   **Answer: B** — Provisioned throughput purchases dedicated inference
   capacity for a commitment period, guaranteeing consistent
   throughput/latency, and is generally the required and cost-effective
   choice for high, steady, predictable volume on a custom model.

---

## 6. Vector databases and embeddings for search and retrieval

**Embeddings** are numeric vector representations of text (or images,
audio) that capture semantic meaning — pieces of content with similar
meaning end up as vectors that are close together in the vector space,
even if they don't share exact words. Embeddings models (e.g., **Amazon
Titan Text Embeddings**, Cohere Embed on Bedrock) convert raw content into
these vectors.

A **vector database** stores embeddings and efficiently performs
**similarity search** (commonly k-nearest-neighbor / k-NN search using
cosine similarity or Euclidean distance) to find the stored vectors
closest to a query vector — the mechanism that powers **semantic search**
(finding conceptually related content, not just exact keyword matches)
and is the retrieval half of RAG. AWS options tested on the exam:

- **Amazon OpenSearch Service** (and its serverless option, **Amazon
  OpenSearch Serverless**) — a search and analytics service with a
  built-in **vector engine**, supporting k-NN vector search alongside
  traditional keyword/full-text search. A common choice as the vector
  store behind Bedrock Knowledge Bases, and useful when you need both
  vector *and* keyword (hybrid) search.
- **Amazon Aurora (PostgreSQL-compatible) with the pgvector extension** —
  lets you store vector embeddings as a column type directly inside a
  relational **Amazon Aurora** or **Amazon RDS for PostgreSQL** database
  and query them with SQL, using the open-source `pgvector` extension.
  A good fit when a team already runs PostgreSQL and wants vector search
  without adopting a separate, dedicated search service.
- **Amazon Kendra** — an intelligent, ML-powered **enterprise search**
  service, not a general-purpose vector database. Kendra indexes
  documents from many connectors (S3, SharePoint, Salesforce, etc.) and
  handles embedding, ranking, and relevance internally — you don't manage
  embeddings or a vector index yourself. It's the right choice for
  "add natural-language enterprise search over our existing document
  repositories" without building a custom RAG/embeddings pipeline;
  Bedrock Knowledge Bases can also use an existing **Amazon Kendra
  GenAI Index** as a retriever.

**AWS example:** A healthcare software vendor builds a clinical-reference
chatbot. They generate embeddings for medical documents using **Amazon
Titan Text Embeddings** and store them in **Amazon OpenSearch Service**
for low-latency semantic + keyword hybrid search inside a Bedrock
Knowledge Base. A separate internal team, wanting quick natural-language
search across existing SharePoint and S3 document repositories without
building an embeddings pipeline at all, instead deploys **Amazon Kendra**
and points it at those repositories directly.

> **Exam tip:** If a scenario describes managing your own embeddings model
> and choosing a similarity-search index, that's a **vector database**
> (OpenSearch Service, or Aurora/RDS PostgreSQL with **pgvector**). If a
> scenario just wants "search across our existing enterprise documents in
> natural language" with minimal setup and no mention of managing
> embeddings, that's **Amazon Kendra** — a fully managed enterprise search
> service, not a database you architect yourself.

**Decision tree: choosing a vector database or search backend.** The
bullets above describe what each option *is*; the flowchart below turns
the same choice into a sequence of yes/no questions centered on whether
Amazon RDS/Aurora infrastructure already exists, whether the use case
needs vector-only search or hybrid (vector + keyword) search, and
scale/throughput requirements — a visual complement to the table above,
consistent with the customization decision tree in [Section 4](#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering):

```mermaid
flowchart TD
    START(["Choosing a vector database /\nsearch backend?"])
    START --> Q0{"Need natural-language search across\nexisting document repos (S3, SharePoint,\nSalesforce) with NO embeddings\npipeline to build yourself?"}
    Q0 -->|"YES"| KEN["AMAZON KENDRA\n(managed embeddings + ranking,\nzero vector infrastructure)"]
    Q0 -->|"NO"| Q1{"Does Amazon RDS or Aurora\n(PostgreSQL-compatible) infrastructure\nALREADY exist for this application?"}
    Q1 -->|"YES"| Q2{"Is the search VECTOR-ONLY -\nno built-in keyword/full-text\nfused into the same query?"}
    Q2 -->|"YES"| Q3{"High throughput / large scale,\nor already running on Aurora\n(vs. plain RDS)?"}
    Q3 -->|"YES"| AUR["AURORA (PostgreSQL) + PGVECTOR\nauto-scaling storage, read replicas,\nvectors alongside relational data"]
    Q3 -->|"NO"| RDSV["AMAZON RDS FOR POSTGRESQL +\nPGVECTOR\nsmaller/steady workloads, normal\nRDS administration"]
    Q2 -->|"NO - need hybrid search too"| OS1["AMAZON OPENSEARCH\n(Service or Serverless)\nbuilt-in vector engine + keyword\nsearch in one query"]
    Q1 -->|"NO"| Q4{"Need hybrid (vector + keyword)\nsearch, or large-scale/\nhigh-throughput vector search?"}
    Q4 -->|"YES"| OS2["AMAZON OPENSEARCH SERVERLESS\nbuilt-in vector engine, autoscaling,\nhybrid search out of the box"]
    Q4 -->|"NO"| AUR2["AURORA (PostgreSQL) + PGVECTOR\n(new deployment)\nvector-only, moderate scale,\nSQL-native querying"]
```

> **Exam tip:** Amazon RDS and Amazon Aurora both support `pgvector`, and
> the exam distinguishes them by what the application already standardizes
> on: a scenario that says the team already runs **RDS for PostgreSQL**
> points to **RDS + pgvector**, while "needs auto-scaling storage, read
> replicas, or is already on Aurora" points to **Aurora + pgvector**. If
> the scenario adds "and we also need keyword/full-text search fused into
> the same query," that pulls the answer toward **OpenSearch** instead,
> regardless of which relational database is already in place.

#### Mini-quiz: Test your understanding of vector databases and embeddings

Quick self-check before moving on — try to answer before reading the
explanation.

1. What mechanism does a vector database use to find the stored vectors
   closest to a query vector?
   A. Exact keyword matching only
   B. Similarity search (e.g., k-nearest-neighbor / k-NN)
   C. Chain-of-thought reasoning
   D. Prompt templating

   **Answer: B** — Vector databases perform similarity search (commonly
   k-NN using cosine similarity or Euclidean distance) to find vectors
   close to a query vector, which is the mechanism behind semantic search.

2. A team already runs its data in Amazon Aurora PostgreSQL and wants to
   add vector similarity search without adopting a separate dedicated
   search service. Which option fits best?
   A. Amazon Kendra
   B. Amazon Aurora (PostgreSQL-compatible) with the pgvector extension
   C. AWS Trainium
   D. Amazon Bedrock Agents

   **Answer: B** — pgvector lets the team store embeddings as a column
   type directly inside the PostgreSQL database they already operate and
   query them with SQL, avoiding a new dedicated service.

3. Which AWS service handles embedding, ranking, and relevance internally,
   making it the right fit for natural-language search across existing
   enterprise document repositories without building a custom embeddings
   pipeline?
   A. Amazon OpenSearch Service
   B. Amazon Aurora with pgvector
   C. Amazon Kendra
   D. AWS Inferentia

   **Answer: C** — Amazon Kendra is a fully managed enterprise search
   service that indexes documents from connectors like S3 and SharePoint
   and handles embeddings and relevance internally, so no custom pipeline
   is required.

---

## 7. Evaluating foundation model performance

Choosing and shipping a foundation model requires evaluating it, and the
exam expects you to know three complementary evaluation approaches:

- **Human evaluation** — people (either your own subject-matter experts
  or an AWS-managed work team via Bedrock's human evaluation jobs) review
  model outputs and score them against criteria that are hard to automate:
  tone, creativity, helpfulness, cultural appropriateness, or nuanced
  correctness. Slower and more expensive than automatic evaluation, but
  necessary for subjective quality judgments.
- **Benchmark datasets** — standardized, often publicly available datasets
  paired with automatically computable metrics (e.g., accuracy, F1 score,
  BLEU/ROUGE for text similarity) used to score a model objectively and
  reproducibly, and to compare models against each other on a level
  playing field. **Amazon Bedrock automatic model evaluation** runs jobs
  against built-in curated prompt datasets and metrics, or your own
  custom prompt dataset.
- **Business metrics** — ultimately, an FM application must be judged by
  whether it moves outcomes the organization cares about: task completion
  rate, average handling time, customer satisfaction (CSAT) score,
  conversion rate, cost per interaction, or reduction in human escalation
  rate. A model can score well on benchmark metrics yet fail to improve
  the business metric it was built for (or vice versa) — the exam expects
  you to recognize business metrics as the final, outcome-oriented layer
  of evaluation, distinct from (but informed by) model-quality metrics.

**AWS example:** A telecom company evaluates two candidate Bedrock models
for a customer-service assistant. They first run an **automatic model
evaluation** job using a benchmark dataset to compare accuracy and
robustness objectively. The top two candidates then go through a **human
evaluation** job where support agents score sample conversations for tone
and helpfulness. After launch, the company tracks the **business
metric** of average call-deflection rate (how many issues the assistant
resolves without escalation to a human agent) to judge real-world impact —
which is ultimately what determines whether the project is considered
successful, regardless of how well the model scored on benchmarks.

> **Exam tip:** Keep the three layers distinct: **benchmark datasets**
> measure model quality **objectively and automatically**; **human
> evaluation** measures quality **subjectively**, using people;
> **business metrics** measure real-world **outcome impact**, and are the
> only one of the three tied directly to organizational goals rather than
> model output quality itself. A question about "comparing multiple
> models quickly and cheaply at scale" points to benchmark-based automatic
> evaluation; a question about "judging tone or creativity" points to
> human evaluation; a question about "did this actually help the
> business" points to a business metric.

#### Mini-quiz: Test your understanding of evaluating foundation model performance

Quick self-check before moving on — try to answer before reading the
explanation.

1. Which evaluation approach uses standardized datasets paired with
   automatically computable metrics such as accuracy or F1 score?
   A. Human evaluation
   B. Benchmark datasets
   C. Business metrics
   D. Provisioned throughput

   **Answer: B** — Benchmark datasets are standardized, often public
   datasets paired with automatically computable metrics used to score a
   model objectively and reproducibly.

2. Which of the three evaluation layers is tied directly to organizational
   outcomes rather than to model output quality itself?
   A. Benchmark datasets
   B. Human evaluation
   C. Business metrics
   D. Automatic model evaluation

   **Answer: C** — Business metrics (e.g., CSAT, task completion rate,
   cost per interaction) measure real-world outcome impact; a model can
   score well on benchmarks or human evaluation yet still fail to move the
   business metric it was built for.

3. A team wants to judge tone and creativity — criteria that are hard to
   compute automatically. Which evaluation approach fits best?
   A. Benchmark datasets
   B. Human evaluation
   C. Business metrics
   D. Automatic evaluation only

   **Answer: B** — Human evaluation uses people to score outputs on
   subjective criteria like tone and creativity that automatic metrics
   can't capture.

---

## 8. AWS infrastructure for generative AI workloads

Behind Bedrock's managed experience, and for teams building or training
custom models directly, AWS provides infrastructure purpose-built for
generative AI and deep learning workloads:

- **Amazon SageMaker** — AWS's fully managed service for building,
  training, and deploying machine learning models, including foundation
  models. **SageMaker JumpStart** provides a hub of pretrained foundation
  models and pre-built solution templates that can be deployed or
  fine-tuned with a few clicks, for teams that need more control over
  model hosting/customization than Bedrock's fully managed API offers
  (e.g., deploying to a specific instance type, or a model not available
  on Bedrock).
- **AWS Trainium** — a purpose-built AWS silicon (ML chip) optimized for
  **high-performance, cost-efficient training** of deep learning and
  foundation models at scale. Available via Amazon EC2 **Trn1/Trn2**
  instances.
- **AWS Inferentia** — a purpose-built AWS silicon (ML chip) optimized for
  **high-throughput, low-latency, cost-efficient inference**. Available
  via Amazon EC2 **Inf1/Inf2** instances.
- Both chip families are programmed via the **AWS Neuron SDK**, and both
  exist specifically to reduce the cost of large-scale deep learning
  compared to general-purpose GPU instances, while remaining compatible
  with common ML frameworks (PyTorch, TensorFlow).

**AWS example:** An AI startup pretrains a custom foundation model from
scratch on **Amazon EC2 Trn1** instances powered by **AWS Trainium** to
minimize training cost at scale. Once trained, they deploy the model for
production inference on **Amazon EC2 Inf2** instances powered by **AWS
Inferentia2**, achieving low per-request latency and lower cost per
inference than equivalent GPU instances. For experimentation and
fine-tuning of openly available foundation models without managing this
infrastructure directly, a different team at the same company uses
**Amazon SageMaker JumpStart**.

> **Exam tip:** Memorize the mapping precisely, since the exam frequently
> tests it directly: **AWS Trainium → training**, **AWS Inferentia →
> inference**. Both are purpose-built chips (not general-purpose GPUs)
> whose primary selling point is **lower cost at high scale** for deep
> learning workloads specifically — pick Trainium/Inferentia over generic
> EC2 GPU instances when a scenario emphasizes minimizing the cost of
> training or serving large models at scale.

**Decision tree: from the Domain 1 inference-type question to the Domain 3
Bedrock throughput decision.** [The cross-domain concept map](cross-domain-concept-map.md#domain-1-domain-3-applications-of-foundation-models)
notes that Bedrock's on-demand vs. provisioned-throughput choice ([Section
5](#5-amazon-bedrock-features)) is the generative-AI-specific version of the
Domain 1 inference-type decision (real-time, batch, asynchronous, or
serverless inference) -- both trade latency and cost against traffic
predictability. The flowchart below turns that cross-domain link into a
walkable sequence of questions:

```mermaid
flowchart TD
    START(["D1 QUESTION:\nWhat inference type does\nthe workload need?\n(real-time, batch,\nasynchronous, or serverless)"])
    START -->|"Real-time or\nasynchronous\n(a user or system waits\non a live response)"| RT["Needs low-latency,\nsynchronous inference"]
    START -->|"Batch\n(large volume scored\noffline, no one waiting\non an individual request)"| BATCH["Needs high-throughput,\nasynchronous inference"]
    RT --> Q1{"D3 QUESTION:\nIs Bedrock request volume\nhigh, steady, and predictable?"}
    BATCH --> Q1
    Q1 -->|"NO -\nvariable, spiky,\nor low volume"| OD["BEDROCK ON-DEMAND\nTHROUGHPUT\npay per token, no\ncommitment - fits\nunpredictable traffic"]
    Q1 -->|"YES -\nhigh, steady,\npredictable volume"| Q2{"Do you also need a custom\n(fine-tuned) model, or a\nlatency SLA guaranteed\nregardless of other tenants'\ntraffic?"}
    Q2 -->|"YES"| PT["BEDROCK PROVISIONED\nTHROUGHPUT\ndedicated capacity (model\nunits), 1- or 6-month\ncommitment - required for\nmost custom models"]
    Q2 -->|"NO -\nbase model, no hard\nlatency guarantee needed"| OD2["BEDROCK ON-DEMAND\nTHROUGHPUT\nstill the cheaper choice\nunless volume justifies a\ncapacity commitment"]
```

The three deciding factors are the same ones Domain 1 already trades off for
real-time vs. batch inference, just re-applied to Bedrock's pricing model:
**traffic predictability** (steady/high volume vs. variable/spiky),
**latency needs** (a guaranteed, consistent SLA vs. best-effort), and
**cost model** (a flat-rate capacity commitment vs. pay-per-token).

#### Mini-quiz: Test your understanding of AWS infrastructure for generative AI workloads

Quick self-check before moving on — try to answer before reading the
explanation.

1. Which purpose-built AWS chip is optimized specifically for
   high-performance, cost-efficient **training** of deep learning and
   foundation models at scale?
   A. AWS Inferentia
   B. AWS Trainium
   C. AWS Graviton
   D. AWS Nitro

   **Answer: B** — Trainium is purpose-built for high-performance,
   cost-efficient training, available via EC2 Trn1/Trn2 instances.

2. Which purpose-built AWS chip is optimized specifically for
   high-throughput, low-latency, cost-efficient **inference**?
   A. AWS Trainium
   B. AWS Inferentia
   C. AWS Graviton
   D. AWS Nitro

   **Answer: B** — Inferentia is purpose-built for high-throughput,
   low-latency, cost-efficient inference, available via EC2 Inf1/Inf2
   instances; Trainium (A) targets training, not inference.

3. Which AWS service provides a hub of pretrained foundation models and
   pre-built solution templates that can be deployed or fine-tuned with
   more direct control over hosting than Amazon Bedrock's fully managed
   API?
   A. Amazon Bedrock Knowledge Bases
   B. Amazon SageMaker JumpStart
   C. Amazon Kendra
   D. AWS Neuron SDK

   **Answer: B** — SageMaker JumpStart offers pretrained models and
   templates deployable/fine-tunable with more control over hosting (e.g.,
   a specific instance type or a model not available on Bedrock).

---

## Worked example: implementing RAG for an internal policy-lookup assistant

[Section 3](#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases) introduced the RAG pipeline conceptually. This
walkthrough follows one company through every step of actually building
it, including the customization-approach decision from [Section
4](#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering) and the evaluation step from [Section
7](#7-evaluating-foundation-model-performance) — the level of detail AIF-C01 scenario questions expect
you to reason through even though the exam itself is multiple-choice.

**Scenario:** An insurance company's HR team fields the same questions
over and over ("how many vacation days do I have," "what's the parental
leave policy") against a 300-page internal policy handbook that legal
revises every quarter. Employees currently search a shared drive full of
PDFs, and answers are often wrong because employees read an outdated
version.

1. **Rule out the alternatives first.** The team checks the customization
   spectrum from [Section 4](#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering): fine-tuning would require creating
   thousands of labeled question/answer pairs from the handbook *and*
   re-running that training job every quarter when legal revises it —
   too slow and too expensive for a document that changes often. Prompt
   engineering alone can't work either, because the 300-page handbook
   does not fit in a single prompt. That combination of "frequently
   changing source data" and "too large for the context window" is the
   textbook signal for **RAG**.
2. **Ingestion.** The handbook PDFs (and any policy addenda) are uploaded
   to an **Amazon S3** bucket, which becomes the data source for an
   **Amazon Bedrock Knowledge Base**.
3. **Chunking.** The team lets Bedrock's default chunking strategy split
   each PDF into passages of a few hundred tokens with slight overlap
   between consecutive chunks, so a policy detail that falls near a page
   boundary still appears intact in at least one retrievable chunk.
4. **Embedding.** Each chunk is converted to a vector with **Amazon Titan
   Text Embeddings**, chosen because the team is already using other
   Titan models elsewhere and wants one consistent embedding space.
5. **Indexing/storage.** The embeddings are stored in **Amazon OpenSearch
   Serverless**, which the Knowledge Base provisions and manages
   automatically — the team never has to size or patch a search cluster.
6. **Retrieval and augmentation at query time.** An employee asks, "How
   many weeks of parental leave do I get?" The question is embedded with
   the same Titan model, **Amazon OpenSearch Serverless** returns the most
   semantically similar handbook chunks (the parental-leave section, even
   if the employee's wording doesn't match the handbook's exact phrasing),
   and those chunks are inserted into the prompt sent to the FM via
   Bedrock's `RetrieveAndGenerate` API.
7. **Generation with citations.** The FM answers using only the retrieved
   passages as grounding, and the application surfaces which handbook
   section the answer came from — directly addressing the "employees
   trust the wrong answer" problem, since HR can now verify any answer
   against a cited source.
8. **Evaluation before rollout.** Using the criteria from [Section
   7](#7-evaluating-foundation-model-performance), the team checks retrieval quality (are the *right*
   chunks coming back for a test set of real HR questions?) separately
   from generation quality (given the right chunks, does the FM produce a
   correct, well-formed answer?) — because a wrong answer could stem from
   either half of the pipeline, and conflating them makes the failure
   impossible to debug.
9. **Handling the quarterly update.** When legal revises the handbook next
   quarter, the team simply re-uploads the changed PDFs to the same S3
   bucket and re-syncs the Knowledge Base's data source — no retraining,
   no redeployment, and the assistant is answering from the current
   policy within minutes.

> **Exam tip:** If a scenario emphasizes that source data **changes
> frequently** and/or is **too large to fit in a prompt**, and the goal is
> **grounded, current, citable answers**, the answer is **RAG / Amazon
> Bedrock Knowledge Bases** — not fine-tuning (too slow to keep current)
> and not prompt engineering alone (can't fit a 300-page document). Watch
> for distractor scenarios that describe this exact setup but then ask
> "how do you keep it current" with a fine-tuning-flavored answer choice —
> re-syncing the S3 data source is always cheaper and faster.

---

## Worked example: selecting a foundation model under multiple competing constraints

[Section 1](#1-design-considerations-for-foundation-model-applications) and
[Domain 2, Section 7](domain-2-fundamentals-of-generative-ai.md#7-foundation-model-selection-criteria)
each introduce foundation model selection criteria (modality, cost,
latency, context window, fine-tuning support) one at a time. Real exam
scenarios rarely give you just one constraint — they stack four or five at
once and expect you to eliminate candidate models constraint by constraint
until exactly one survives. This walkthrough works through a scenario that
way.

**Scenario:** A media company is adding an AI-assisted support-triage
feature to its live chat widget. The requirements gathered from three
different stakeholders are:

- **Modality:** customers frequently attach a photo of the damaged or
  defective product, so the model must accept **image input alongside
  text** (multimodal).
- **Latency:** the feature sits inside a **live chat widget** — replies
  must feel conversational, not delayed.
- **Cost:** finance has capped inference spend, ruling out the account's
  most expensive, largest frontier-tier model for this feature.
- **Fine-tuning support:** the support team wants to later fine-tune the
  model on thousands of labeled historical transcripts so it reliably
  matches the brand's exact tone and escalation format — the model must be
  a Bedrock model that supports customization, not an on-demand-only
  model.
- **Context window:** when an issue escalates, the assistant must
  summarize the **entire ticket history** for that customer — sometimes
  tens of thousands of tokens of past messages — in a single prompt,
  without chunking it across multiple calls.

Five foundation models are available in the team's Amazon Bedrock model
catalog:

| Model | Modality | Relative cost | Latency | Fine-tuning support | Context window |
|---|---|---|---|---|---|
| **Model A** | Text + image | High (largest, frontier-tier) | High | Yes | 200K tokens |
| **Model B** | Text only | Low | Low | Yes | 8K tokens |
| **Model C** | Text + image | Low | Low | No (on-demand only) | 32K tokens |
| **Model D** | Text + image | Moderate | Moderate | Yes | 4K tokens |
| **Model E** | Text + image | Moderate | Low | Yes | 128K tokens |

Rather than trying to weigh all five constraints against all five models at
once, work through them one constraint at a time, eliminating any model
that fails it, the same way you should on the exam:

1. **Modality eliminates Model B first.** The feature must accept
   image attachments, and Model B is text-only. Modality is usually the
   right constraint to apply first ([Section 1](#1-design-considerations-for-foundation-model-applications) calls this out explicitly),
   because no amount of low cost or low latency makes a model that can't
   even read the required input viable. Remaining: **A, C, D, E**.
2. **Cost eliminates Model A next.** Model A satisfies every other
   requirement — it's multimodal, fine-tunable, and has the largest
   context window of the group — but it's the account's most expensive,
   frontier-tier model, and finance has explicitly capped inference spend
   for this feature. A model that's disqualified on cost stays
   disqualified regardless of how well it scores elsewhere. Remaining:
   **C, D, E**.
3. **Fine-tuning support eliminates Model C.** Model C is cheap and
   low-latency, but it's only available for on-demand inference and
   doesn't support customization — and the support team has a firm
   requirement to fine-tune on labeled transcripts later. Remaining:
   **D, E**.
4. **Context window eliminates Model D.** Both D and E are multimodal,
   moderately priced, and fine-tunable. But D's 4K-token context window
   can't hold a tens-of-thousands-of-token ticket history in one prompt,
   while E's 128K-token window can. Remaining: **E**.
5. **Confirm the survivor against every constraint.** Model E is
   multimodal (✓ modality), low-latency (✓ latency for a live chat
   widget), moderately priced and within budget (✓ cost), fine-tunable
   (✓ customization), and has a 128K-token context window large enough for
   a full escalation history (✓ context window). Because it is the only
   model left standing after each constraint was applied, **Model E** is
   the answer — not because it "wins" on any single dimension, but because
   it's the only one that fails none of them.

**Visual summary — multi-constraint elimination decision tree:** the
diagram below traces the exact same walkthrough as a flowchart, so you can
see all five constraints applied in sequence against all five candidate
models in one picture, instead of re-reading the numbered steps:

```mermaid
flowchart TD
    START(["5 candidate models:\nA, B, C, D, E"])
    START --> Q1{"MODALITY:\nmust accept image + text\n(customers attach photos)"}
    Q1 -->|"Model B is text-only -\nELIMINATED"| R1["Remaining: A, C, D, E"]
    R1 --> Q2{"COST:\nmust stay within finance's\ninference budget"}
    Q2 -->|"Model A is the most\nexpensive, frontier-tier -\nELIMINATED"| R2["Remaining: C, D, E"]
    R2 --> Q3{"FINE-TUNING SUPPORT:\nmust support customization\non labeled transcripts"}
    Q3 -->|"Model C is on-demand\nonly, no fine-tuning -\nELIMINATED"| R3["Remaining: D, E"]
    R3 --> Q4{"CONTEXT WINDOW:\nmust fit a full ticket\nhistory in one prompt"}
    Q4 -->|"Model D's 4K-token window\nis too small - ELIMINATED"| R4["Remaining: E"]
    R4 --> Q5{"LATENCY (confirm):\nmust feel conversational\nin a live chat widget"}
    Q5 -->|"Model E is low-latency -\nCONFIRMED"| SURVIVOR["MODEL E\nonly candidate that fails\nno stated constraint"]
```

Notice what this process avoids: picking Model A because it looks most
capable on paper (it fails cost), or picking Model C because it looks
cheapest and fastest (it fails fine-tuning support). A model that's
excellent on three out of four stated constraints is still the wrong
answer if a scenario states all four as requirements — the exam is testing
whether you'll eliminate on every stated constraint, not just the
most obvious one.

> **Exam tip:** When a scenario lists several requirements at once, don't
> try to mentally rank or average them — **eliminate candidates one
> constraint at a time**, in whatever order the constraints are easiest to
> check (a hard modality or cost cutoff is usually fastest to apply
> first), until only one candidate remains. A distractor answer choice in
> this kind of question is almost always a model that satisfies most, but
> not all, of the stated constraints.

---

## Comparison table: customization approaches for foundation model applications

| Approach | Changes model weights? | Data required | Relative cost/speed | Best for |
|---|---|---|---|---|
| **Prompt engineering** | No | None beyond the prompt itself | Lowest cost, fastest to iterate | Quick behavior/format adjustments; no training data available |
| **RAG (Amazon Bedrock Knowledge Bases)** | No | External knowledge source (documents), no labeling needed | Low cost, fast to set up; retrieval adds some runtime latency | Grounding answers in current, frequently changing, or proprietary data; reducing hallucination |
| **Fine-tuning** | Yes | Labeled input/output example pairs | Higher cost, slower (requires a training job) | Reliable task-specific style/format/behavior; often needs provisioned throughput to serve |
| **Continued pre-training** | Yes | Large volume of unlabeled domain-specific text | Highest cost, slowest, most compute-intensive | Deepening a model's general knowledge/vocabulary of a specialized domain |

> **Exam tip:** This table is the domain's most-tested decision. As
> complexity/cost increases left to right, so does how deeply the model
> itself is changed: prompt engineering and RAG never touch the model's
> weights (the model is used "as-is," just given different input); fine-
> tuning and continued pre-training both retrain the model and typically
> require the resulting custom model to be served via **provisioned
> throughput** on Bedrock.

---

## Quick-reference cheat sheet

A condensed, one-page (print-friendly) recap of this domain's
highest-yield material for last-minute review right before the exam.
Domain 3 carries the largest single share of scored questions
(**~28%**), so this is the single most valuable page-and-a-half in this
guide to re-read the morning of the exam. It restates material covered
in full in [Section 1](#1-design-considerations-for-foundation-model-applications), [Section 3](#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases), [Section 4](#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering), and [Section 5](#5-amazon-bedrock-features) —
it is not a substitute for reading those sections, only a fast recall
aid once you already have.

**FM selection criteria (Section 1) — weigh all six against each other:**

| Factor | Ask yourself |
|---|---|
| Task fit | Does the model handle this task type (summarization, code, classification, chat) well? |
| Context window | Is the input (plus retrieved/RAG context) small enough to fit? |
| Modality | Does the model accept/produce the needed input/output types (text, image, audio, video)? |
| Accuracy | Does it perform well enough on *this* use case, not just on generic benchmarks? |
| Cost | Per-token (on-demand) or reserved-capacity (provisioned throughput) — bigger models cost more per token |
| Latency | Smaller models respond faster; streaming improves *perceived* latency only |
| Customization | Can it be fine-tuned or continued-pre-trained if prompt engineering/RAG isn't enough? |

**RAG architecture (Section 3) — six steps, in order:**

Ingestion (S3) → Chunking → Embedding (e.g., Amazon Titan Text
Embeddings) → Indexing/storage (vector database) → Retrieval (similarity
search on the embedded query) → Augmentation and generation (retrieved
chunks inserted into the prompt, FM generates a grounded answer). Amazon
Bedrock Knowledge Bases automates all six steps for you via the
`Retrieve` / `RetrieveAndGenerate` APIs. **RAG never changes model
weights** — it changes what goes into the prompt.

**Customization spectrum (Section 4) — one-line-per-approach recall:**

- **Prompt engineering** → no data, no training, cheapest/fastest → style/format tweaks.
- **RAG** → external data, no training → current/frequently changing/proprietary facts, less hallucination.
- **Fine-tuning** → labeled data, retrains weights → a specific narrow task/style done reliably.
- **Continued pre-training** → unlabeled data, retrains weights, priciest/slowest → broad domain vocabulary/fluency.

**Bedrock feature set (Section 5) — match the keyword to the feature:**

| If the scenario says... | The feature is... |
|---|---|
| "explicitly enable a model before calling it" | Model access |
| "take actions / call APIs / multi-step tasks" | Agents (action groups) |
| "block harmful, off-topic, or PII content" | Guardrails |
| "answer from our own documents" | Knowledge Bases |
| "compare model quality objectively/at scale" | Automatic model evaluation |
| "judge subjective quality like tone" | Human evaluation |
| "guaranteed throughput, high/steady/predictable volume, custom model" | Provisioned throughput |
| "unpredictable/low/spiky volume, pay per use" | On-demand |

**Key definitions to have cold:** embedding (numeric vector capturing
semantic meaning) · chunking (splitting documents before embedding) ·
vector database (optimized for similarity/k-NN search) · hallucination
(a model confidently generating incorrect information) · provisioned
throughput (reserved capacity, in *model units*, for a commitment
period) · action group (the APIs a Bedrock Agent can invoke, typically
via Lambda).

**Common exam traps:**

- "Frequently changing data" or "reduce hallucination from our own
  documents" → **RAG**, not fine-tuning. Fine-tuning is slow/expensive to
  update and doesn't ground answers in facts outside its training data.
- A **fine-tuned or continued-pre-trained** model almost always needs
  **provisioned throughput** to serve reliably — don't pick on-demand for
  a custom model under steady high load.
- **Guardrails** filters content; it does **not** retrieve knowledge or
  invoke APIs — don't confuse it with Knowledge Bases or Agents.
- **Streaming** improves *perceived* latency (tokens appear sooner); it
  does not reduce total generation time or cost.
- Continued pre-training uses **unlabeled** text for broad domain
  fluency; fine-tuning uses **labeled** input/output pairs for a narrow
  task — the labeled/unlabeled distinction is the fastest way to tell
  the two apart under exam pressure.

---

## Key terms glossary

> Looking for a term from another domain? [`docs/master-glossary.md`](master-glossary.md) indexes every domain's key terms alphabetically with domain tags (e.g. `[D1, D3]`) and links back here.

- **Foundation model (FM) application design** — the process of choosing
  a model and architecture based on task fit, cost, latency, modality, and
  customization needs.
- **Modality** — the type(s) of input/output a model handles (text,
  image, audio, video); **multimodal** models handle more than one.
- **Prompt engineering** — crafting model input to reliably produce a
  desired output, without changing model weights.
- **Zero-shot prompting** — asking a model to perform a task with no
  example demonstrations.
- **Few-shot prompting** — including example input/output pairs in a
  prompt to guide the model's output pattern.
- **Chain-of-thought (CoT) prompting** — instructing a model to reason
  step-by-step before answering, improving multi-step reasoning accuracy.
- **Negative prompting** — explicitly instructing a model what to avoid
  producing.
- **Prompt template** — a reusable prompt structure with placeholders for
  consistent, repeatable prompt construction.
- **Prompt chaining** — breaking a task into a sequence of prompts where
  each output feeds the next input.
- **Prompt injection** — a malicious attempt to override an application's
  intended prompt/system instructions via user input.
- **Retrieval Augmented Generation (RAG)** — retrieving relevant external
  data at query time and inserting it into the prompt to ground a model's
  response, without retraining.
- **Amazon Bedrock Knowledge Bases** — Bedrock's fully managed RAG
  feature: automatic ingestion, chunking, embedding, and retrieval over
  your own data source.
- **Chunking** — splitting documents into smaller passages before
  embedding, so retrieval returns focused, relevant content.
- **Embedding** — a numeric vector representation of text (or other
  content) capturing its semantic meaning.
- **Amazon Titan Text Embeddings** — an Amazon Bedrock embeddings model
  used to generate vector embeddings from text.
- **Vector database** — a data store optimized for similarity search over
  embeddings (e.g., k-NN search).
- **Semantic search** — search based on meaning/similarity rather than
  exact keyword matching, powered by embeddings and vector search.
- **Amazon OpenSearch Service / Serverless** — an AWS search and analytics
  service with a built-in vector engine, supporting hybrid vector +
  keyword search.
- **pgvector** — an open-source PostgreSQL extension for storing and
  querying vector embeddings in Amazon Aurora or Amazon RDS for
  PostgreSQL.
- **Amazon Kendra** — a fully managed, ML-powered enterprise search
  service that handles embeddings and relevance internally.
- **Fine-tuning** — further training a pretrained FM on a smaller labeled
  dataset to change its weights for a specific task, style, or format.
- **Continued pre-training (domain adaptation)** — further training a
  pretrained FM on large volumes of unlabeled domain-specific text using
  the original pretraining objective.
- **Amazon Bedrock model access** — the requirement to explicitly request
  access to a specific foundation model in the Bedrock console before use.
- **Amazon Bedrock Agents** — a Bedrock feature that lets an FM plan and
  execute multi-step tasks by invoking external APIs (action groups) and
  Knowledge Bases.
- **Action group (Bedrock Agents)** — a defined set of APIs (typically
  backed by AWS Lambda) that a Bedrock Agent can invoke to take actions.
- **Guardrails for Amazon Bedrock** — configurable safety filters applied
  to FM inputs/outputs (denied topics, content filters, PII redaction,
  contextual grounding checks).
- **Bedrock model evaluation** — Bedrock jobs that assess FM quality via
  automatic (benchmark-based) or human evaluation.
- **Automatic model evaluation** — evaluation using built-in or custom
  metrics computed programmatically against a prompt dataset.
- **Human evaluation (model evaluation)** — evaluation where people score
  model outputs on subjective criteria.
- **Benchmark dataset** — a standardized dataset (often public) used to
  objectively and reproducibly score and compare model quality.
- **Business metric** — an outcome-oriented measure (e.g., conversion
  rate, CSAT, cost per interaction) used to judge an application's
  real-world impact, distinct from model-quality metrics.
- **Provisioned throughput** — dedicated, reserved inference capacity
  (model units) purchased for a commitment period, guaranteeing
  consistent throughput/latency; typically required to serve custom
  (fine-tuned) models.
- **On-demand (Bedrock pricing)** — pay-per-token inference pricing with
  no capacity commitment, suited to variable/unpredictable traffic.
- **Amazon SageMaker** — AWS's fully managed service for building,
  training, and deploying ML models.
- **Amazon SageMaker JumpStart** — a hub of pretrained foundation models
  and solution templates deployable/fine-tunable within SageMaker.
- **AWS Trainium** — AWS's purpose-built ML chip optimized for
  cost-efficient, high-performance model training (EC2 Trn1/Trn2).
- **AWS Inferentia** — AWS's purpose-built ML chip optimized for
  cost-efficient, high-throughput, low-latency inference (EC2 Inf1/Inf2).
- **AWS Neuron SDK** — the software development kit used to run ML
  workloads on Trainium and Inferentia chips.

---

## Practice questions

1. **[Intermediate]** A company wants its generative AI assistant to always answer using the
   most current version of its product catalog, which changes daily, and
   cannot afford to retrain a model every day. Which approach best fits
   this requirement?
   A. Fine-tuning
   B. Continued pre-training
   C. Retrieval Augmented Generation (RAG) with Amazon Bedrock Knowledge Bases
   D. Increasing the model's temperature parameter

2. **[Beginner]** Which factor should a team prioritize first when a use case requires
   the model to generate both text and images from a single prompt?
   A. Cost per token
   B. Modality support
   C. Provisioned throughput commitment length
   D. Chain-of-thought prompting

3. **[Intermediate]** A developer wants a foundation model to reliably output responses in a
   very specific JSON schema by showing it several example input/output
   pairs directly inside the prompt, without any training job. Which
   prompt engineering technique is this?
   A. Zero-shot prompting
   B. Few-shot prompting
   C. Continued pre-training
   D. Fine-tuning

4. **[Intermediate]** A model is prone to giving a final answer to multi-step math word
   problems without correctly working through the intermediate steps.
   Which prompting technique would most directly help, at no additional
   training cost?
   A. Negative prompting
   B. Chain-of-thought prompting
   C. Provisioned throughput
   D. Continued pre-training

5. **[Beginner]** Which of the following best describes the purpose of Amazon Bedrock
   Knowledge Bases?
   A. It fine-tunes a foundation model's weights on labeled data
   B. It automatically manages ingestion, chunking, embedding, and retrieval of your own data to ground FM responses
   C. It provides dedicated, reserved inference capacity for a model
   D. It filters harmful content from model outputs

6. **[Advanced]** A company wants a foundation model to deeply understand highly
   specialized medical terminology found throughout a large volume of
   unlabeled clinical text, improving its general fluency in that domain
   rather than teaching it one specific task. Which customization approach
   fits best?
   A. Prompt engineering
   B. RAG
   C. Continued pre-training
   D. Provisioned throughput

7. **[Advanced]** Which statement correctly distinguishes fine-tuning from continued
   pre-training?
   A. Fine-tuning requires unlabeled data; continued pre-training requires labeled data
   B. Fine-tuning uses labeled input/output examples to adapt a model to a specific task; continued pre-training uses large volumes of unlabeled domain text to deepen general domain knowledge
   C. They are the same process with different names
   D. Neither approach changes the model's weights

8. **[Intermediate]** A company wants a Bedrock-based assistant to (1) look up a
   customer's order status by calling an internal REST API, and (2)
   answer a follow-up question by retrieving relevant passages from
   internal documentation, all within one conversation. Which two Amazon
   Bedrock capabilities respectively fit these two needs? (Select TWO.)
   A. Amazon Bedrock Agents
   B. Amazon Bedrock Knowledge Bases
   C. Guardrails for Amazon Bedrock
   D. Provisioned throughput
   E. Amazon Bedrock model evaluation

9. **[Beginner]** Before an AWS account can invoke a specific foundation model on Amazon
   Bedrock, what must first be done?
   A. Purchase provisioned throughput for that model
   B. Request and be granted model access for that model in the Bedrock console
   C. Fine-tune the model on custom data
   D. Deploy the model to Amazon SageMaker JumpStart

10. **[Intermediate]** A company expects high, steady, predictable request volume for a
    custom fine-tuned model in production and wants guaranteed, consistent
    throughput. Which Bedrock capacity option should they choose?
    A. On-demand pricing
    B. Provisioned throughput
    C. Automatic model evaluation
    D. Continued pre-training

11. **[Beginner]** A team needs to compare several candidate foundation models on
    accuracy and robustness quickly, cheaply, and objectively before
    narrowing down to finalists. Which approach fits best?
    A. Human evaluation
    B. Automatic model evaluation using benchmark datasets
    C. Business metric tracking
    D. Provisioned throughput

12. **[Intermediate]** After launch, which of the following is a business metric (as
    distinct from a model-quality metric) for a generative AI customer
    support assistant?
    A. BLEU score against a benchmark dataset
    B. Toxicity score from an automatic evaluation job
    C. Customer satisfaction (CSAT) score and call-deflection rate
    D. F1 score on a labeled test set

13. **[Beginner]** Which AWS service should a team use to generate vector embeddings from
    text for use in a semantic search application?
    A. AWS Trainium
    B. Amazon Titan Text Embeddings
    C. AWS Inferentia
    D. Amazon SageMaker JumpStart

14. **[Intermediate]** A team already runs its application data in Amazon Aurora PostgreSQL
    and wants to add vector similarity search without adopting a separate
    dedicated search service. Which option fits best?
    A. Amazon Kendra
    B. Amazon Aurora with the pgvector extension
    C. AWS Trainium
    D. Amazon Bedrock Agents

15. **[Beginner]** A team wants to add natural-language search across its existing
    SharePoint and Amazon S3 document repositories, without building or
    managing an embeddings pipeline themselves. Which AWS service is the
    best fit?
    A. Amazon Kendra
    B. AWS Inferentia
    C. Amazon Aurora with pgvector
    D. AWS Trainium

16. **[Beginner]** Which purpose-built AWS chip is optimized specifically for
    cost-efficient, high-performance training of deep learning and
    foundation models at scale?
    A. AWS Inferentia
    B. AWS Trainium
    C. AWS Graviton
    D. AWS Nitro

17. **[Intermediate]** A company has already trained a large custom model and now needs to
    serve it for production inference with low latency and low
    cost-per-request at high volume. Which AWS infrastructure choice
    is purpose-built for this?
    A. Amazon EC2 instances powered by AWS Trainium
    B. Amazon EC2 instances powered by AWS Inferentia
    C. AWS Neuron SDK alone, without any EC2 instance
    D. Amazon Bedrock Knowledge Bases

18. **[Intermediate]** A company wants to quickly deploy and optionally fine-tune a
    pretrained foundation model with more direct control over hosting than
    Amazon Bedrock's fully managed API provides. Which AWS capability best
    fits this need?
    A. Amazon Bedrock Guardrails
    B. Amazon SageMaker JumpStart
    C. Amazon Kendra
    D. Amazon Bedrock model evaluation

19. **[Advanced]** Which combination of factors is part of "design considerations for
    foundation model applications" as tested on the AIF-C01 exam? (Select
    TWO.)
    A. The modality (text, image, audio) the application must support
    B. The latency requirements of the use case
    C. The specific AWS Region's time zone offset
    D. The font used to render the application's UI
    E. The color palette of the company's marketing website

20. **[Advanced]** A retail company wants a generative AI assistant to consistently
    output product descriptions in the company's exact required tone and
    format, and has hundreds of labeled example descriptions already
    written by their copywriting team. Which customization approach is the
    best fit?
    A. Prompt engineering only
    B. RAG only
    C. Fine-tuning
    D. Increasing the context window

---

## Answer key and explanations

1. **C — Retrieval Augmented Generation (RAG) with Amazon Bedrock
   Knowledge Bases.** RAG retrieves current external data at query time
   without retraining, exactly fitting a daily-changing catalog.
   Fine-tuning (A) and continued pre-training (B) bake knowledge into
   static weights and would require retraining daily; changing temperature
   (D) affects randomness of output, not knowledge freshness.

2. **B — Modality support.** If a model can't process/generate the
   required input/output types, no amount of cost or prompting technique
   makes it viable, so modality must be filtered on first. Cost (A) and
   provisioned throughput (C) are capacity/pricing decisions made after
   narrowing to modality-capable models; chain-of-thought prompting (D)
   is a reasoning technique, unrelated to modality support.

3. **B — Few-shot prompting.** Providing example input/output pairs
   directly in the prompt to shape output format is the definition of
   few-shot prompting. Zero-shot (A) provides no examples; continued
   pre-training (C) and fine-tuning (D) both require a training job and
   change model weights, which the scenario explicitly rules out.

4. **B — Chain-of-thought prompting.** Instructing the model to reason
   step-by-step directly improves multi-step reasoning accuracy at no
   training cost. Negative prompting (A) tells the model what to avoid,
   not how to reason; provisioned throughput (C) is a capacity/pricing
   feature; continued pre-training (D) requires a costly training job the
   scenario doesn't call for.

5. **B — It automatically manages ingestion, chunking, embedding, and
   retrieval of your own data to ground FM responses.** This is Knowledge
   Bases' defining purpose (managed RAG). Fine-tuning weights (A) is a
   separate Bedrock customization feature; reserved capacity (C) describes
   provisioned throughput; content filtering (D) describes Guardrails.

6. **C — Continued pre-training.** Deepening general domain
   understanding from a large volume of unlabeled text, rather than
   teaching one specific task, is exactly what continued pre-training
   does. Prompt engineering (A) doesn't change the model's underlying
   knowledge; RAG (B) retrieves facts at query time rather than deepening
   the model's fluency; provisioned throughput (D) is a capacity feature
   unrelated to customization.

7. **B — Fine-tuning uses labeled input/output examples to adapt a model
   to a specific task; continued pre-training uses large volumes of
   unlabeled domain text to deepen general domain knowledge.** This is the
   precise labeled-vs-unlabeled, task-vs-domain distinction the exam
   tests. A reverses the data requirements; C is false, they are distinct
   processes; D is false, both approaches update model weights.

8. **A and B — Amazon Bedrock Agents, and Amazon Bedrock Knowledge Bases.**
   Agents are purpose-built to plan and execute multi-step tasks,
   including invoking external APIs (action groups) such as an order-status
   lookup; Knowledge Bases retrieves relevant passages from your own
   documentation via RAG to ground a follow-up answer. Guardrails (C)
   filters content, it doesn't call APIs or retrieve documents;
   provisioned throughput (D) is a capacity feature; model evaluation (E)
   assesses model quality, it isn't a runtime orchestration or retrieval
   feature.

9. **B — Request and be granted model access for that model in the
   Bedrock console.** Bedrock requires explicit model access approval per
   model before it can be invoked. Provisioned throughput (A) is an
   optional capacity purchase, not a prerequisite for basic access;
   fine-tuning (C) is an optional customization step; SageMaker JumpStart
   (D) is a separate deployment path, not required for Bedrock access.

10. **B — Provisioned throughput.** High, steady, predictable volume for a
    custom model is exactly the scenario provisioned throughput is
    designed and cost-effective for, and it's typically required to serve
    fine-tuned custom models. On-demand (A) suits variable/unpredictable
    traffic, not steady high volume; automatic model evaluation (C) and
    continued pre-training (D) are unrelated to serving capacity.

11. **B — Automatic model evaluation using benchmark datasets.** Automatic
    evaluation against benchmark datasets is fast, low-cost, and
    objective — ideal for quickly comparing many candidates. Human
    evaluation (A) is slower and more expensive, better suited to
    subjective criteria; business metrics (C) are measured post-launch on
    real usage, not during model comparison; provisioned throughput (D) is
    a capacity feature, not an evaluation method.

12. **C — Customer satisfaction (CSAT) score and call-deflection rate.**
    These are outcome-oriented business metrics reflecting real-world
    impact. BLEU score (A), toxicity score (B), and F1 score (D) are all
    model-quality metrics computed against datasets, not business outcome
    measures.

13. **B — Amazon Titan Text Embeddings.** This is a Bedrock embeddings
    model purpose-built to convert text into vector embeddings for
    semantic search. AWS Trainium (A) and AWS Inferentia (C) are compute
    chips for training/inference generally, not an embeddings model
    themselves; SageMaker JumpStart (D) is a model hub/deployment tool,
    not an embeddings generator itself.

14. **B — Amazon Aurora with the pgvector extension.** This lets the team
    add vector similarity search directly inside the PostgreSQL database
    they already operate, via SQL, without adopting a new dedicated
    service. Amazon Kendra (A) is a separate managed search service, not
    integrated into their existing database; AWS Trainium (C) is a
    training chip, unrelated to vector search; Bedrock Agents (D)
    orchestrates tasks, it isn't a vector store.

15. **A — Amazon Kendra.** Kendra is a fully managed enterprise search
    service that indexes connectors like SharePoint and S3 and handles
    embeddings/relevance internally, requiring no custom embeddings
    pipeline. AWS Inferentia (B) and AWS Trainium (D) are ML chips, not
    search services; Aurora with pgvector (C) still requires the team to
    generate and manage embeddings themselves, which the scenario wants
    to avoid.

16. **B — AWS Trainium.** Trainium is AWS's purpose-built chip optimized
    specifically for cost-efficient, high-performance training at scale.
    AWS Inferentia (A) is optimized for inference, not training; AWS
    Graviton (C) is a general-purpose AWS CPU, not ML-training-specific;
    AWS Nitro (D) is the underlying EC2 virtualization/security system,
    not an ML training chip.

17. **B — Amazon EC2 instances powered by AWS Inferentia.** Inferentia is
    purpose-built for high-throughput, low-latency, cost-efficient
    inference at scale, matching the described serving need. Trainium (A)
    is optimized for training, not inference; the Neuron SDK alone (C)
    is software, not compute infrastructure — it still requires
    Trainium/Inferentia-backed EC2 instances to run on; Bedrock Knowledge
    Bases (D) is a RAG feature, unrelated to chip-level inference
    infrastructure.

18. **B — Amazon SageMaker JumpStart.** JumpStart provides pretrained
    foundation models and templates deployable and fine-tunable with more
    direct control over hosting than Bedrock's fully managed API.
    Guardrails (A) is a safety filter feature within Bedrock; Amazon
    Kendra (C) is an enterprise search service, unrelated to model
    hosting; Bedrock model evaluation (D) assesses model quality, it
    doesn't deploy or host models.

19. **A and B — The modality the application must support, and the
    latency requirements of the use case.** Both are core, exam-defined
    design considerations for FM applications (alongside model selection
    and cost). Region time zone offset (C), UI font (D), and marketing
    website color palette (E) are unrelated to foundation model
    application design.

20. **C — Fine-tuning.** Having hundreds of labeled example
    input/output pairs and needing consistently reproduced tone/format is
    exactly the scenario fine-tuning is designed for. Prompt engineering
    alone (A) is less reliable at scale for a strict required format
    without weight updates; RAG alone (B) grounds facts in external data
    but doesn't teach a consistent output style; increasing the context
    window (D) allows more input text, but doesn't itself teach the model
    a specific tone or format.

---

[← Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md) · **Domain 3 of 5** · [Domain 4: Guidelines for Responsible AI →](domain-4-guidelines-for-responsible-ai.md)
