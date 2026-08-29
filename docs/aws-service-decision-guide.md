# AWS Service Decision Guide: A Cross-Domain Quick Reference

[Domain 1](domain-1-fundamentals-of-ai-and-ml.md), [Domain 2](domain-2-fundamentals-of-generative-ai.md),
[Domain 3](domain-3-applications-of-foundation-models.md), and
[Domain 5](domain-5-security-compliance-governance.md) each carry their own
comparison table, scoped to that domain's task statements. That's the right
depth for studying a domain in isolation, but the exam (and real-world
architecture decisions) routinely mixes "which AI service?" and "which
security/compliance service?" questions in the same scenario. This page is
a **consolidated quick reference** that sits on top of those domain tables —
it doesn't replace them, it points back to them for the full detail.

Use this page when a scenario gives you a use case and you need to jump
straight to "which AWS service is the exam answer here?" without re-reading
an entire domain guide. If instead you already know the service and want
every place it's discussed across the series (e.g., "everywhere Amazon
Bedrock is mentioned"), see [`aws-service-index.md`](aws-service-index.md) --
an alphabetical, per-service index rather than a decision flow.

---

## 1. Decision flow: SageMaker vs. Bedrock vs. purpose-built AI services

The single most tested decision pattern across Domains 1–3 is **"which AWS
service should I reach for?"** — and it always resolves through the same
three-question flow, regardless of whether the use case is classic ML or
generative AI:

```
START: What are you trying to build?
│
├─ 1. Does the task involve a *foundation model* (generating or reasoning
│     over text, images, code, or other content; chat; summarization;
│     RAG; agents)?
│     │
│     ├─ YES → 2. Do you need a ready-made, fully managed *application*
│     │         rather than a model you integrate yourself?
│     │         │
│     │         ├─ YES → Amazon Q Business (enterprise assistant grounded
│     │         │        in your data), Amazon Q Developer (coding
│     │         │        companion), or PartyRock (no-code prototyping)
│     │         │
│     │         └─ NO  → Amazon Bedrock — choose a foundation model,
│     │                  and layer on Knowledge Bases (RAG), Agents
│     │                  (multi-step task execution), Guardrails (safety
│     │                  filters), and Model Evaluation as needed.
│     │                  Need deep infrastructure control alongside the
│     │                  FM (custom training pipelines, Trainium/
│     │                  Inferentia)? → SageMaker JumpStart instead.
│     │
│     └─ NO  → 3. Does a purpose-built managed AI service already solve
│               this exact use case?
│               │
│               ├─ YES → Use the purpose-built service:
│               │        • Amazon Personalize — recommendations
│               │        • Amazon Forecast — time-series forecasting
│               │        • Amazon Rekognition — image/video analysis
│               │        • Amazon Transcribe — speech-to-text
│               │        • Amazon Comprehend — text/NLP analytics
│               │        • Amazon Polly — text-to-speech
│               │        • Amazon Translate — language translation
│               │        • Amazon Lex — conversational chat/voice bots
│               │        • Amazon Textract — structured document extraction
│               │        • Amazon Fraud Detector — fraud-risk scoring
│               │
│               └─ NO  → Amazon SageMaker — build, train, and deploy a
│                        bespoke model when no managed service covers
│                        the use case, or deep customization is required.
```

> **Exam tip — the rule behind the flow:** at every branch, the more
> "out of the box" and purpose-built a service is for the exact scenario
> described, the more likely it's the correct exam answer. The flow only
> reaches **Amazon Bedrock** (for generative use cases) or **Amazon
> SageMaker** (for everything else) when no purpose-built service already
> covers the ask. Building a custom model or FM integration for a task a
> purpose-built service already handles is a classic exam distractor.

For the full service-by-service detail behind this flow, see:
- [Domain 1 §5 — AWS managed AI/ML services (conceptual overview)](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview)
  and its [comparison table](domain-1-fundamentals-of-ai-and-ml.md#comparison-table-aws-managed-aiml-services-at-a-glance)
- [Domain 2 §5 — AWS generative AI services and capabilities](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities)
  and its [comparison table](domain-2-fundamentals-of-generative-ai.md#comparison-table-aws-generative-ai-services-at-a-glance)
- [Domain 3 §5 — Amazon Bedrock features](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features)
  and the [customization-approach comparison table](domain-3-applications-of-foundation-models.md#comparison-table-customization-approaches-for-foundation-model-applications)

---

## 2. Comparison table: security, compliance, and governance services

Domain 5 scenarios frequently confuse these four services because they all
touch "compliance" — but each answers a different question:

| Service | Category | What it does | Answers the question... | When it's the exam answer |
|---|---|---|---|---|
| **AWS CloudTrail** | Governance — activity logging | Logs every API call (who, what, when) across your account | "Who invoked this model / changed this resource, and when?" | You need a record of a specific API call, e.g. a specific `InvokeModel` or `CreateEndpoint` |
| **AWS Config** | Governance — configuration tracking | Records resource configuration state and evaluates it against compliance rules over time | "Is this resource compliant right now, and when did its configuration change?" | You need to detect that a SageMaker endpoint or S3 bucket drifted out of an encrypted/private configuration |
| **AWS Audit Manager** | Compliance — evidence collection | Automates collecting audit evidence mapped to a named framework (HIPAA, ISO 27001, SOC 2, etc.) | "Can I generate an audit-ready compliance report?" | You need to assemble evidence for an external or internal audit of an AI system |
| **AWS Artifact** | Compliance — AWS's own attestations | On-demand self-service portal for AWS's own compliance reports and agreements (SOC reports, ISO certifications, the HIPAA BAA) | "Where do I get proof of *AWS's* compliance, or sign an agreement with AWS?" | You need to download a SOC 2 report or execute a Business Associate Addendum (BAA) — it does not audit *your* account |

> **Exam tip:** CloudTrail and Config both watch *your* account, but
> CloudTrail is about **events/actions** while Config is about **resource
> state over time**. Audit Manager and Artifact both relate to
> "compliance," but Audit Manager assembles evidence *about your account*
> while Artifact hands you evidence *about AWS itself*.

See the fuller version of this table (which also covers Amazon Macie and
Amazon GuardDuty) at
[Domain 5 — comparison table: governance and monitoring services](domain-5-security-compliance-governance.md#comparison-table-governance-and-monitoring-services).

---

## 3. Comparison table: encryption and privacy options

| Option | Protects | Key concept | When to use it |
|---|---|---|---|
| **AWS KMS (Key Management Service)** | Data at rest (S3, EBS, SageMaker model artifacts, Bedrock fine-tuning data) | AWS-managed keys are simplest; **customer managed keys (CMKs)** give you control over key policy, rotation, and give you a CloudTrail-logged audit trail of every decrypt | You must encrypt sensitive data at rest and control (or prove control over) exactly who can decrypt it |
| **AWS PrivateLink / VPC endpoints** | Data in transit between your VPC and an AWS service | An **interface VPC endpoint** keeps traffic to a supported AWS service on the AWS network backbone — it never traverses the public internet, and needs no internet gateway, NAT gateway, or public IP | A scenario says a workload runs in a private/isolated VPC (no internet access) but still needs to call an AI service like Bedrock or SageMaker |
| **HIPAA eligibility + BAA (via AWS Artifact)** | Protected health information (PHI) | To legally process PHI on AWS, you must execute a **Business Associate Addendum (BAA)** — obtained through AWS Artifact — and use only **HIPAA-eligible services**, configured per AWS's HIPAA guidance (encryption enabled, access controls applied) | The scenario mentions patient data, PHI, or a healthcare workload — think "BAA + HIPAA-eligible services," not just "encrypt it" |

> **Exam tip:** These three are often layered in the same scenario: a
> healthcare company fine-tuning a model on Bedrock with patient data
> needs a **customer-managed KMS key** (control over decryption), a
> **VPC endpoint** (keep the training traffic off the public internet),
> and a **signed BAA** (the legal prerequisite for touching PHI at all) —
> none of the three substitutes for the others.

For the full walkthrough of each concept, see Domain 5:
[Data encryption at rest and in transit](domain-5-security-compliance-governance.md#data-encryption-at-rest-and-in-transit),
[AWS PrivateLink and VPC endpoints for AI services](domain-5-security-compliance-governance.md#aws-privatelink-and-vpc-endpoints-for-ai-services),
[AWS Artifact](domain-5-security-compliance-governance.md#aws-artifact), and
[HIPAA — conceptual level](domain-5-security-compliance-governance.md#hipaa-health-insurance-portability-and-accountability-act-conceptual-level).

---

## 4. Bedrock model reference: capabilities and use-case fit

The domain guides mention Titan, Claude, Llama, Nova, and other Bedrock
models throughout, but scattered mentions aren't a substitute for a single
place to compare them. Use this table when a scenario names a use case
(or a required modality) and you need to reason about *which family* of
model fits — not the exact model version, which changes too often to be
exam-testable.

> **Staleness warning:** Amazon Bedrock's model catalog changes
> frequently — AWS adds new model versions and deprecates old ones on an
> ongoing basis. The exam tests **model-family capabilities and
> selection criteria** (context window trade-offs, which modality a
> family supports, when multimodal beats text-only), not specific
> version numbers. Always verify exact model names/versions against the
> [Bedrock model catalog](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.md)
> before relying on this table outside exam prep.
>
> **Last verified:** 2026-08-29, against the official Bedrock model
> catalog above. Changes found and applied in that pass: **Titan Text**
> (Lite/Express/Premier) has been retired from the catalog — Amazon's
> current text-generation line is **Nova**; Titan's embeddings and image
> lines continue under newer versions (**Titan Text Embeddings V2**,
> **Titan Image Generator G1 v2**), and **Titan Multimodal Embeddings**
> and **Nova Sonic** (real-time speech-to-speech) were added as
> current-generation models missing from the prior table; AI21's
> **Jurassic** line and Cohere's original (non-R) **Command** models are
> no longer listed; and Stability AI's Bedrock offering is now the
> task-specific **Stable Image** line rather than general Stable
> Diffusion checkpoints. The next reviewer should update this date and
> summary after re-checking against the catalog link above.

| Model family | Provider | Modalities | Context window (relative) | Best-fit use case | Exam-style cue |
|---|---|---|---|---|---|
| **Amazon Titan Text** (Lite/Express/Premier) — *retired, see Nova* | Amazon | Text in → text out | Small → large across tiers | No longer offered for new use as of Aug 2026 — retired in favor of Amazon **Nova**'s text tiers. Kept here because older exam material may still name it | "Cost-effective," "Amazon-native" text-generation cues now point to **Nova**, not Titan Text |
| **Amazon Titan Text Embeddings V2** | Amazon | Text in → vector out | N/A (embeddings, not generation) | Converting chunked documents/queries into vectors for RAG / semantic search | "Embeddings," "semantic search," "vector database" |
| **Amazon Titan Multimodal Embeddings** | Amazon | Text and/or image in → vector out | N/A (embeddings, not generation) | Embedding images and text into the same vector space for multimodal search (e.g., "find images similar to this description") | "Multimodal search," "embed images and text together" |
| **Amazon Titan Image Generator G1 v2** | Amazon | Text/image in → image out | N/A | Image generation and editing with built-in invisible watermarking for provenance | "Generate an image," "watermark," "responsible image generation" |
| **Amazon Nova** (Micro/Lite/Pro/Premier) | Amazon | Text; Lite/Pro/Premier add image and video understanding | Micro smallest/fastest → Premier largest/most capable | Latency- and cost-sensitive text tasks (Micro) up to complex multimodal reasoning (Premier); Amazon's current general-purpose text family, superseding Titan Text | "Fast and low-cost," "understand video," "tiered by speed vs. capability" |
| **Amazon Nova Canvas** | Amazon | Text/image in → image out | N/A | Studio-quality image generation and editing (inpainting, outpainting, background removal) | "Image generation," "edit an existing image" |
| **Amazon Nova Reel** | Amazon | Text/image in → video out | N/A | Short-form video generation from a text or image prompt | "Generate a video" |
| **Amazon Nova Sonic** | Amazon | Speech in → speech/text out (real-time, bidirectional) | N/A | Real-time, low-latency speech-to-speech conversational applications (voice assistants/agents) | "Real-time voice conversation," "speech-to-speech," not just transcription |
| **Anthropic Claude** | Anthropic | Text, and multimodal text+image input | Large (tens of thousands of tokens+) | Complex reasoning, long-document analysis, agentic tool use, careful instruction-following | "Long document," "reasoning," "agents," "analyze an image and answer questions about it" |
| **Meta Llama** | Meta | Text in → text out for the 3.x line; **Llama 4** (Scout/Maverick) adds native multimodal text+image input | Mid → large depending on version | Open-weight model needs — fine-tuning control, on-prem/portability considerations, cost-efficient general text tasks; multimodal open-weight needs point to Llama 4 | "Open source," "open-weight," "fine-tune and control the weights" |
| **AI21 Labs Jamba** | AI21 Labs | Text in → text out | Large, efficient long-context handling | Long-context summarization and text generation with efficient inference | "Long context," "efficient at scale" — the older **Jurassic** line has been retired; Jamba is AI21's only current Bedrock family |
| **Cohere Command R / Command R+ / Embed / Rerank** | Cohere | Command R/R+: text in → text out, RAG- and tool-use-optimized; Embed: text → vector; Rerank: reorders search results | Mid-large (Command R/R+) | Enterprise text generation and RAG-oriented tool use (Command R/R+), embeddings (Embed), improving RAG retrieval relevance (Rerank) | "Improve search relevance," "rerank retrieved documents" — plain **Command** (non-R) has been retired in favor of Command R/R+ |
| **Mistral AI models** | Mistral AI | Text in → text out for the core line; newer additions add vision (**Pixtral**) and audio (**Voxtral**) input | Small (efficient) → large | Cost-efficient, low-latency text generation; some models support function calling; Pixtral/Voxtral cover multimodal needs in the same family | "Low latency," "function calling," "efficient" |
| **Stability AI (Stable Image)** | Stability AI | Text/image in → image out | N/A | High-control, style-flexible image generation and editing (upscaling, inpainting, outpainting, background removal, style transfer) | "Image generation," "fine-grained style control" — current Bedrock catalog exposes this as the task-specific **Stable Image** line rather than general Stable Diffusion checkpoints |

> **Exam tip — pick the *capability*, not the brand name.** Exam
> scenarios rarely ask "which company makes this model?" They describe a
> requirement — "must generate an image," "must reason over a 200-page
> document," "must run fine-tuning on open weights," "must support video
> understanding" — and the correct answer is whichever **family**
> natively supports that modality or trait. Choosing a text-only model
> (e.g., Meta Llama's 3.x line) for an image-generation scenario, or a
> small/fast model (e.g., Nova Micro) for a task that needs deep
> multi-step reasoning, is a classic distractor pattern.

> **Exam tip — modality mismatch is the #1 trap.** Not every Bedrock
> model supports every modality. Before matching a model to a scenario,
> confirm it: (1) accepts the required **input** modality (text, image,
> or both), (2) produces the required **output** modality (text, image,
> video, embeddings), and (3) if long input is described (a large
> document, a long conversation history), favor a model family known for
> large context windows (Claude, AI21) over one optimized for speed/cost
> (Nova Micro).

For the underlying Bedrock feature set these models plug into (Knowledge
Bases, Agents, Guardrails, Model Evaluation, Provisioned Throughput), see
[Domain 3 §5 — Amazon Bedrock features](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features).
For where each model family is mentioned elsewhere across the series, see
[`aws-service-index.md`](aws-service-index.md).

---

## 5. Consolidated service matrix: all services across domains

Sections 1–4 above are decision aids scoped to a single question each
(which compute/model service, which governance service, which encryption
option, which Bedrock model family). This section is different: it's a
**single flat matrix covering every one of the 45+ AWS services**
referenced anywhere across the five domain guides — the same population of
services [`aws-service-index.md`](aws-service-index.md) lists
alphabetically with jump-links, but reshaped here into one multi-dimensional
table you can scan for "which domain(s) is this tested in, how much does
that domain count on the exam, when do I actually reach for it, and what's
the trap." Use the service index when you know the service and want every
place it's discussed; use this matrix when you want the whole landscape in
one scroll, or want to sanity-check a service you're unsure you've fully
placed.

> **How to read "Exam weight relevance":** each domain's share of the exam
> is fixed — Domain 1 ~20%, Domain 2 ~24%, Domain 3 ~28%, Domain 4 ~14%,
> Domain 5 ~14% (see the [domain weighting table in
> README.md](../README.md#exam-domains)). A service tagged with more than
> one domain isn't "more heavily weighted" by itself — it just means it can
> legitimately show up in scenario questions scored under either domain's
> percentage, so confusing it with a same-domain neighbor costs you twice.

| Service | Domain(s) | Exam weight relevance | When to use it | Common point of confusion |
|---|---|---|---|---|
| **AI Service Cards** | D4 | ~14% | Look up the documented intended use, limitations, and design considerations of a specific pre-built AWS AI service before deploying it | Confused with **SageMaker Model Cards** — Service Cards are AWS-authored docs about a managed service (e.g., Rekognition); Model Cards are documentation *you* author about *your own* trained model |
| **Amazon Augmented AI (Amazon A2I)** | D4 | ~14% | Insert a human reviewer into the loop for low-confidence or high-stakes ML predictions | Confused with SageMaker Ground Truth (labeling *training* data) — A2I reviews *inference-time* predictions, not training labels |
| **Amazon Aurora (PostgreSQL, with pgvector)** | D3 | ~28% | Store vector embeddings as a column type inside a relational database you already run, via the pgvector extension | Confused with Amazon OpenSearch and Amazon Kendra as "the RAG vector store" — Aurora/pgvector is the right pick specifically when you need embeddings *alongside* existing relational data and SQL joins, not a dedicated search engine |
| **Amazon Bedrock** | D2, D3, D4, D5 | ~24% + ~28% | Access a choice of foundation models from Amazon and third parties through one unified API, and layer on Knowledge Bases, Agents, Guardrails, and Model Evaluation | Confused with Amazon SageMaker — Bedrock is for consuming/customizing *existing* foundation models; SageMaker is for building/training a *bespoke* model or when deep infrastructure control is required |
| **Amazon Bedrock Agents** | D2, D3 | ~24% + ~28% | Let a foundation model plan and execute multi-step tasks by calling your own APIs | Confused with Bedrock Knowledge Bases — Agents take *action*; Knowledge Bases *retrieve information* (RAG). A scenario needing both grounded answers and task execution needs both together |
| **Amazon Bedrock Knowledge Bases** | D2, D3, D5 | ~24% + ~28% | Ground a foundation model's answers in your own data (RAG) with source attribution, without managing the retrieval pipeline yourself | Confused with a raw vector database (OpenSearch/Aurora/Kendra) — Knowledge Bases is the managed *orchestration layer* on top of one of those stores, not a replacement for picking one |
| **Amazon Bedrock Model Evaluation** | D2, D3 | ~24% + ~28% | Compare foundation model quality using automatic metrics or human evaluators before committing to a model choice | Confused with SageMaker Clarify — Model Evaluation compares *FM output quality/fit*; Clarify measures *bias and explainability*, mostly for traditional ML models |
| **Amazon CloudWatch** | D5 | ~14% | Monitor operational metrics/logs to detect anomalous invocation patterns or model drift in near-real time | Confused with AWS CloudTrail — CloudWatch answers "is something behaving abnormally *right now*"; CloudTrail answers "who called what API, and when" |
| **Amazon Comprehend** | D1, D5 | ~20% + ~14% | Run managed NLP for sentiment, entities, key phrases, PII detection, or topic modeling; use Comprehend Medical for HIPAA-eligible clinical text | Confused with Amazon Textract — Comprehend analyzes/understands text that's already digitized; Textract extracts text/structure *out of* scanned documents in the first place |
| **Amazon Forecast** | D1 | ~20% | Generate time-series forecasts (demand, inventory, financial metrics) without building a custom model | Confused with Amazon Fraud Detector as "another prediction service" — Forecast predicts *future numeric trends over time*; Fraud Detector scores *risk of a single transaction/event* |
| **Amazon Fraud Detector** | D1 | ~20% | Get real-time fraud-risk scores for transactions or account activity using a managed model | Confused with Amazon GuardDuty — Fraud Detector scores *business transaction risk* (an ML/AI service, Domain 1); GuardDuty detects *account/infrastructure security threats* (a security service, Domain 5) |
| **Amazon GuardDuty** | D5 | ~14% | Continuously detect threats and anomalies across an AWS account's infrastructure and API activity | Confused with Amazon Macie — GuardDuty watches for *threats/intrusions*; Macie watches for *sensitive data exposure* in S3 specifically |
| **Amazon Kendra** | D3 | ~28% | Stand up enterprise search where the service manages embeddings and relevance ranking internally, with minimal tuning | Confused with Amazon OpenSearch Service — Kendra is fully managed and opinionated (less control, faster to stand up); OpenSearch gives you direct control over the vector engine and hybrid search tuning |
| **Amazon Lex** | D1 | ~20% | Build a conversational chatbot or voice-bot interface with built-in speech recognition and language understanding | Confused with Amazon Q Business — Lex builds a *custom* conversational interface you design intents for; Q Business is a pre-built enterprise assistant grounded in your existing company data |
| **Amazon Macie** | D5 | ~14% | Discover and classify sensitive data (e.g., PII) already stored in Amazon S3 | Confused with Amazon Comprehend PII detection — Macie scans *data at rest in S3 buckets*; Comprehend's PII feature analyzes *text passed to it*, regardless of where it's stored |
| **Amazon OpenSearch Service / Serverless** | D3 | ~28% | Run vector search with a built-in vector engine, especially when you need hybrid vector + keyword search and want direct control over indexing | Confused with Amazon Kendra — OpenSearch is infrastructure you configure; Kendra is a managed search product. Also confused with Aurora/pgvector — OpenSearch is purpose-built for search/analytics, not a general relational store |
| **Amazon Personalize** | D1 | ~20% | Add real-time, individualized recommendations or re-ranking without needing in-house ML expertise | Confused with Bedrock Agents for "personalized responses" — Personalize is a purpose-built recommendation engine (classic ML, Domain 1); it does not involve a foundation model |
| **Amazon Polly** | D1 | ~20% | Convert text into natural, lifelike speech audio | Confused with Amazon Transcribe — Polly goes *text → speech*; Transcribe goes *speech → text*. Easy to swap under exam time pressure |
| **Amazon Q Business** | D2 | ~24% | Deploy a pre-built enterprise generative AI assistant grounded in company data and systems with minimal setup | Confused with Bedrock Knowledge Bases — Q Business is a ready-made *application*; Knowledge Bases is a *building block* you assemble into your own application on top of Bedrock |
| **Amazon Q Developer** | D2 | ~24% | Get a generative AI coding companion and AWS resource assistant integrated into an IDE or the console | Confused with Amazon Q Business — Developer targets *building software and AWS resources*; Business targets *enterprise knowledge work* grounded in company documents |
| **Amazon Rekognition** | D1, D4 | ~20% + ~14% | Run pre-trained or custom computer vision for object/scene detection, facial analysis, or content moderation | Confused with SageMaker for "any vision task" — Rekognition is purpose-built and should win whenever the use case is a standard vision task; only reach for SageMaker when Rekognition's built-in capabilities don't fit |
| **Amazon SageMaker** | D1, D2, D3, D4, D5 | ~20% + ~24% + ~28% + ~14% + ~14% | Build, train, tune, deploy, and monitor a bespoke ML model when no managed/purpose-built service covers the use case, or when deep customization is required | Confused with Bedrock across every domain it touches — the reflex fix is "does a purpose-built or Bedrock option already cover this?" before defaulting to SageMaker |
| **Amazon SageMaker Clarify** | D4 | ~14% | Detect bias in a dataset or trained model and generate SHAP-based explainability reports | Confused with Amazon A2I — Clarify is an automated *analysis* tool run against data/models; A2I inserts a *human* into the review loop. They're complementary, not substitutes |
| **Amazon SageMaker JumpStart** | D2, D3 | ~24% + ~28% | Deploy or fine-tune a pretrained foundation model when you need deep infrastructure control alongside the model (custom training pipelines, Trainium/Inferentia) | Confused with Bedrock — JumpStart is chosen specifically *because* Bedrock's managed abstraction isn't enough; if the scenario doesn't mention needing that infra control, Bedrock is the simpler correct answer |
| **Amazon SageMaker Model Cards** | D4, D5 | ~14% + ~14% | Produce structured, auditable documentation of a model's intended use, training data, evaluation results, and limitations | Confused with AWS Audit Manager — Model Cards document *a specific model*; Audit Manager assembles *account-wide evidence* against a compliance framework, which may include Model Cards as one input |
| **Amazon Textract** | D1 | ~20% | Extract text, handwriting, forms, and tables from scanned documents while preserving structure | Confused with Amazon Comprehend — Textract's job ends once text/structure is extracted; understanding/analyzing that text (sentiment, entities) is Comprehend's job |
| **Amazon Titan** | D2, D3, D4 | ~24% + ~28% + ~14% | Use Amazon's own foundation model family in Bedrock for text generation or embeddings at low cost | Confused with claiming image-generation capability — that moved to **Amazon Nova Canvas**; Titan today is text and embeddings only |
| **Amazon Transcribe** | D1, D4 | ~20% + ~14% | Convert audio/video speech into text via automatic speech recognition | Confused with Amazon Polly (see Polly's row) and with Amazon Comprehend — Transcribe only produces a text transcript, it does not analyze the transcript's content |
| **Amazon Translate** | D1 | ~20% | Perform neural machine translation between languages | Confused with treating it as a generative/Bedrock capability — Translate is a purpose-built managed service (Domain 1), not a foundation-model use case |
| **AWS Artifact** | D5 | ~14% | Download AWS's own compliance reports (SOC, ISO) or execute a Business Associate Addendum (BAA) for HIPAA | Confused with AWS Audit Manager — Artifact hands you evidence *about AWS itself*; Audit Manager assembles evidence *about your account*. See section 2 above |
| **AWS Audit Manager** | D5 | ~14% | Automate collection of audit-ready evidence mapped to a named compliance framework (HIPAA, ISO 27001, SOC 2) | See AWS Artifact's row — the two are the most frequently confused pair in Domain 5's compliance content |
| **AWS CloudTrail** | D5 | ~14% | Get a record of a specific API call — who invoked it and when (e.g., a specific `InvokeModel` call) | Confused with AWS Config (see section 2 above) — CloudTrail is events/actions, Config is resource state over time |
| **AWS Config** | D5 | ~14% | Detect that a resource (e.g., a SageMaker endpoint or S3 bucket) drifted out of a compliant configuration, and see its configuration history | See AWS CloudTrail's row |
| **AWS Customer Carbon Footprint Tool** | D4 | ~14% | Report estimated carbon emissions associated with your AWS usage | Confused with the Well-Architected Sustainability Pillar — the Footprint Tool *measures* emissions; the Sustainability Pillar *prescribes design principles* to reduce them |
| **AWS Inferentia** | D3 | ~28% | Run inference at high throughput and low cost on a purpose-built ML chip | Confused with AWS Trainium — Inferentia is for **inference**, Trainium is for **training**. The names are the mnemonic, but under time pressure they get swapped |
| **AWS KMS (Key Management Service)** | D5 | ~14% | Encrypt sensitive data at rest and control exactly who can decrypt it, ideally with a customer-managed key (CMK) for audit-logged access control | Confused with AWS PrivateLink — KMS protects data *at rest*; PrivateLink protects data *in transit*. A scenario needing both encryption and network isolation needs both services together |
| **AWS Neuron SDK** | D3 | ~28% | Compile and run ML workloads on Trainium and Inferentia chips | Confused with treating Trainium/Inferentia as usable "out of the box" without it — Neuron SDK is the software layer that makes the chips usable, not a separate hardware choice |
| **AWS PrivateLink** | D5 | ~14% | Keep traffic between your VPC and an AWS service like Bedrock or SageMaker off the public internet via an interface VPC endpoint | See AWS KMS's row; also confused with a VPN or Direct Connect — PrivateLink connects your VPC directly to an AWS *service*, not to another network |
| **AWS Trainium** | D3 | ~28% | Train models cost-efficiently at high performance on a purpose-built ML chip | See AWS Inferentia's row |
| **AWS Well-Architected Framework Sustainability Pillar** | D4 | ~14% | Apply design principles to minimize the environmental impact of an AI/ML workload's architecture | See AWS Customer Carbon Footprint Tool's row |
| **Guardrails for Amazon Bedrock** | D2, D3, D4, D5 | ~24% + ~28% + ~14% + ~14% | Apply configurable safety/compliance filters (denied topics, content filters, PII redaction, contextual grounding checks) to foundation model inputs and outputs | Confused with IAM — Guardrails filters *content*; IAM controls *who can call the API at all*. Both are commonly needed together in a responsible-AI scenario |
| **IAM (AWS Identity and Access Management)** | D5 | ~14% | Control which user, group, or service can do what, on which AI resource | Confused with IAM Access Analyzer — IAM sets the policies; Access Analyzer *audits* those policies for unintended external sharing |
| **IAM Access Analyzer** | D5 | ~14% | Identify resources (e.g., S3 buckets, Bedrock model resource policies) that are shared with entities outside your AWS account | See IAM's row |
| **PartyRock** | D2 | ~24% | Prototype with foundation models in a free, no-code Bedrock playground | Confused with Amazon Bedrock itself — PartyRock is a *no-code experimentation front-end*; production applications still integrate against Bedrock's API directly |
| **Provisioned Throughput (Amazon Bedrock)** | D2, D3 | ~24% + ~28% | Reserve Bedrock model capacity for consistent performance under steady, high-volume traffic | Confused with on-demand Bedrock pricing as "always cheaper" — Provisioned Throughput is a deliberate trade of flexibility for guaranteed capacity/latency, and is the exam answer specifically when traffic is described as steady and high-volume |

> **Exam tip:** a service appearing in multiple domains is the matrix's
> biggest signal, not noise — it means the *same* service can be the
> correct answer to differently-framed scenario questions. Amazon Bedrock,
> Amazon SageMaker, and Guardrails for Amazon Bedrock are the three
> services with the widest domain spread; make sure you can articulate
> what changes about *how* each is tested from one domain to the next
> (e.g., Bedrock-as-a-generative-AI-service in Domain 2 vs.
> Bedrock-under-the-shared-responsibility-model in Domain 5).

For the full definition and every per-domain jump-link behind each row
above, see [`aws-service-index.md`](aws-service-index.md).

---

## How this guide relates to the domain guides

This page is intentionally short: it is a **decision aid**, not a
replacement for the domain guides' depth. If a scenario needs more context
than a single table row gives you — the *why* behind a service choice, a
worked AWS example, or an exam-tip explanation of a common distractor —
follow the links above into the relevant domain section. See also the
[cross-domain concept map](cross-domain-concept-map.md) for how Domain 1
fundamentals flow into the later domains' service and governance choices.
