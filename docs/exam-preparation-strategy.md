# Exam Preparation and Study Strategy Guide

The five domain guides in this series ([Domain 1](domain-1-fundamentals-of-ai-and-ml.md),
[Domain 2](domain-2-fundamentals-of-generative-ai.md),
[Domain 3](domain-3-applications-of-foundation-models.md),
[Domain 4](domain-4-guidelines-for-responsible-ai.md),
[Domain 5](domain-5-security-compliance-governance.md)) each teach their own
material in depth, but none of them tell you *how to plan your study time* or
*what the exam itself looks like on exam day*. This page fills that gap. It
covers:

1. [Exam format and time management](#1-exam-format-and-time-management)
2. [Domain weights and high-yield focus areas](#2-domain-weights-and-high-yield-focus-areas)
3. [Recommended reading order](#3-recommended-reading-order)
4. [Common exam traps, consolidated](#4-common-exam-traps-consolidated-from-every-domains-exam-tip-callouts)
5. [1-week / 2-week / 4-week study plans](#5-study-plans)
6. [Topic-based review quick reference](#6-topic-based-review-quick-reference)

This guide's self-assessment advice spans two layers: the in-domain
[mini-quizzes](#mini-quizzes-formative-checks-while-you-study) you take
*while* reading a domain, and the end-of-domain practice questions,
cross-domain scenario questions, and mock exams covered in Sections 1 and 5
that you take *after*.

This guide does not introduce new exam content — every fact and trap here is
drawn from (and links back to) the five domain guides. Use it as the
"how do I actually prepare" companion to their "what do I need to know."

---

## 1. Exam format and time management

The AWS Certified AI Practitioner (AIF-C01) exam:

- **65 questions** in **90 minutes** — that is roughly **1.4 minutes per
  question** on average, though real pacing is uneven (some questions are a
  one-line definitional lookup, others are multi-paragraph scenarios).
- Of those 65 questions, **50 are scored** and **15 are unscored** (used by
  AWS to evaluate future questions). You are **not told which is which**, so
  treat every question with equal care — there is no way to identify and
  skip the unscored ones.
- Questions come in two formats: **multiple choice** (one correct answer out
  of four options) and **multiple response** (e.g., "select TWO" or "select
  THREE" out of five or six options). Multiple-response questions require
  **every** correct option to be selected — partial credit is not given, so
  don't stop at the first option that sounds right.
- Scoring is a **scaled score from 100–1000**, with a **passing score of
  700**. There is **no penalty for a wrong answer**, so never leave a
  question blank — a guess has better expected value than an omission.
- Delivered via Pearson VUE, either at a testing center or online proctored.

**Time-management tactics:**

- **First pass, no stalling:** Answer every question you're confident about
  immediately. Use the on-screen "flag for review" feature to mark scenario
  questions that need more than ~90 seconds of thought, and move on rather
  than getting stuck early and running out of time for questions you'd have
  answered easily.
- **Budget by question type, not question number:** A short definitional
  question ("which term describes...") should take well under a minute; a
  multi-paragraph business scenario deserves the time you save from the
  quick ones. Don't let a single hard question consume 10% of your total
  time.
- **Watch the instruction line, not just the options:** Misreading "select
  TWO" as "select ONE" (or vice versa) is a self-inflicted error that costs
  a scored question for no conceptual reason — read the instruction on
  every multiple-response item before reading the options.
- **Answer, then reconsider only if time remains:** Second-guessing a
  confident first read is a common source of avoidable score loss. If you
  flagged a question and come back to it, look for the specific keyword the
  scenario emphasizes (see [Section 4](#4-common-exam-traps-consolidated-from-every-domains-exam-tip-callouts))
  rather than re-reading the whole scenario from scratch.
- **Every domain guide's practice questions are timed-practice material:**
  each domain has 15–20 scenario-style practice questions with full answer
  explanations (~85 across the series). Doing them under a rough per-question
  time limit — not untimed — is what builds the pacing habit the real exam
  requires.

### Pacing model by question type

The 1.4-minutes-per-question average above is a *budget*, not a *target* —
no individual question should actually take 1.4 minutes. Instead, classify
each question by complexity as soon as you've read it, and pace against the
target for that type, not the overall average:

| Question type | Target time | What it looks like |
|---|---|---|
| **Definitional** | **~30–45 seconds** | A one- or two-sentence question asking you to name or recognize a term, service, or concept directly (e.g., "Which AWS service provides X?", "What does RAG stand for?"). If you know the answer, select it immediately — dwelling longer doesn't improve accuracy on a recall question. |
| **Single-scenario** | **~1–2 minutes** | A short paragraph describing one business situation with one decision point (e.g., choosing RAG vs. fine-tuning for a single stated goal, or matching one Bedrock feature to one keyword). Read it once, identify the one deciding constraint or keyword, and choose. |
| **Complex / multi-paragraph / multi-domain scenario** | **~2–3 minutes** | Multiple paragraphs, several stated constraints that must be weighed together, or a scenario that requires combining knowledge from two domains at once (see the [cross-domain scenario questions](cross-domain-scenario-questions.md) for practice with this format). These questions deserve the time saved from the two faster categories above — that's what makes the 1.4-minute average work out even though no single question takes 1.4 minutes. |

**Flag-and-move-on vs. work-through-it:**

- **Work through it now** if you can identify the deciding keyword or
  constraint within that question type's target time and you're making
  progress, not re-reading the same sentence. Most single-scenario questions,
  and many complex ones, resolve as soon as you spot the one detail the
  question is actually testing.
- **Flag and move on** if you've spent roughly *double* the target time for
  that question type (e.g., ~1.5 minutes on a definitional question, ~4–5
  minutes on a complex multi-domain scenario) and still can't narrow it to
  two options. Flagging preserves time for later questions you'd answer
  confidently and correctly — a question you're stuck on is not worth
  losing two easy questions' worth of time to.
- **Never leave a flagged question unanswered.** Since there is no penalty
  for a wrong answer (Section 1 above), lock in your best guess on every
  flagged question *before* time is at risk of running out, then use any
  remaining time to revisit flagged questions in order and reconsider them
  with fresh eyes.

### Mini-quizzes: formative checks while you study

Beyond the practice-question sets described above, each of the five domain
guides also embeds **35 short mini-quizzes directly within its sections**
(5–8 per domain), each placed right where the material it tests was just
taught, under a heading like `#### Mini-quiz: Test your understanding of
[topic]`. They are **intentionally left out of every domain guide's table
of contents** — you're meant to run into them naturally as you read a
section, not navigate to them directly.

Use a mini-quiz the moment you reach it: it's a **formative** check on the
paragraph or subsection you just finished, not a substitute for the
**summative** practice material covered elsewhere on this page.

- **Mini-quiz (35 total, embedded in-section):** "Did I understand what I
  just read?" Take it immediately after the subsection it follows, before
  moving on to the next topic.
- **Domain practice questions (end of each domain guide):** "Can I apply
  this domain's material, under exam-style conditions, once the whole
  domain is behind me?" Take these after finishing the entire domain, not
  after a single subsection — see [Section 1 above](#1-exam-format-and-time-management).
- **Cross-domain scenario questions and the two mock exams:** "Can I
  combine material from multiple domains the way the real exam does?"
  Save these for after all five domains are done — see
  [Section 5](#5-study-plans).

If you get a mini-quiz question wrong, re-read the subsection right then —
correcting a gap while it's still the topic on screen is far cheaper than
waiting to discover the same gap later in a domain's practice questions or,
worse, on the mock exam.

---

## 2. Domain weights and high-yield focus areas

| # | Domain | Exam weight | Study priority |
|---|--------|:-----------:|-----------------|
| 3 | [Applications of Foundation Models](domain-3-applications-of-foundation-models.md) | **~28%** | **Highest** — largest single slice of the exam |
| 2 | [Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md) | **~24%** | **Second** |
| 1 | [Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md) | ~20% | Third |
| 4 | [Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md) | ~14% | Fourth (tied) |
| 5 | [Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md) | ~14% | Fourth (tied) |

**Domains 2 and 3 together are more than half the exam (~52%).** If your
review time is limited, weight your re-reading and practice-question time
toward Domain 3 first and Domain 2 second — not evenly across all five
domains — even though (see [Section 3](#3-recommended-reading-order)) you
should still have *learned* Domains 1–2 before Domain 3 in the first place.
Weight-based prioritization is for your final review pass, not for the
order in which you first learn the material.

### High-yield focus areas per domain

Each domain guide flags its single most-tested decision directly in an
"Exam tip" on its comparison table. These are the topics to make sure you
can answer without hesitation:

- **Domain 1 (~20%):** the rule that a **purpose-built managed AI service
  beats a custom SageMaker model** whenever one exists for the described use
  case (see the [comparison table](domain-1-fundamentals-of-ai-and-ml.md#comparison-table-aws-managed-aiml-services-at-a-glance));
  distinguishing supervised vs. unsupervised vs. reinforcement learning from
  a one-sentence scenario; reading a confusion matrix and knowing when
  accuracy is the *wrong* metric (class imbalance).
- **Domain 2 (~24%):** choosing **RAG vs. fine-tuning vs. full pretraining**
  from a scenario's stated goal; matching a scenario to the right AWS
  generative AI service (PartyRock vs. Bedrock vs. Amazon Q Business vs.
  Amazon Q Developer vs. SageMaker JumpStart — see the
  [comparison table](domain-2-fundamentals-of-generative-ai.md#comparison-table-aws-generative-ai-services-at-a-glance));
  inference parameters (temperature, top-p, top-k) and their effect on
  determinism/creativity.
- **Domain 3 (~28%, the single highest-weighted domain):** the full
  **prompt engineering → RAG → fine-tuning → continued pre-training**
  customization spectrum, explicitly called out as "the domain's
  most-tested decision" (see the
  [comparison table](domain-3-applications-of-foundation-models.md#comparison-table-customization-approaches-for-foundation-model-applications));
  matching an Amazon Bedrock feature (Agents, Guardrails, Knowledge Bases,
  Model Evaluation, provisioned throughput) to a keyword in the scenario;
  the Trainium (training) vs. Inferentia (inference) chip mapping.
- **Domain 4 (~14%):** naming the specific responsible-AI dimension a
  scenario describes (fairness, explainability, transparency,
  controllability, veracity/robustness — see the
  [comparison table](domain-4-guidelines-for-responsible-ai.md#comparison-table-aws-responsible-ai-tools-at-a-glance));
  Model Cards (self-authored) vs. AI Service Cards (AWS-authored); balancing
  performance vs. interpretability under regulatory pressure.
- **Domain 5 (~14%):** the one-line distinction between **CloudTrail**
  (API activity), **Config** (resource configuration/compliance state), and
  **Audit Manager** (audit evidence collection); when a VPC endpoint
  (PrivateLink) is required vs. a NAT gateway or VPN; the shared
  responsibility model as abstraction increases (Bedrock > SageMaker
  JumpStart > SageMaker custom training).

For a cross-domain view of how these high-yield areas connect to each
other — not just within one domain — see the
[cross-domain concept map](cross-domain-concept-map.md) and the
[AWS service decision guide](aws-service-decision-guide.md).

---

## 3. Recommended reading order

**Read the domains in numeric order: Domain 1 → Domain 2 → Domain 3 →
Domain 4 → Domain 5.** This is not arbitrary — it mirrors the exam's own
task-statement structure, and each domain's guide is written assuming the
vocabulary and mental models from the earlier domains are already familiar:

1. **[Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md)**
   is the prerequisite for everything else. Its ML lifecycle, learning
   types, and model-evaluation vocabulary reappear — renamed or specialized
   — in every later domain (see the
   [cross-domain concept map](cross-domain-concept-map.md) for the specific
   throughlines).
2. **[Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md)**
   builds directly on Domain 1's "types of learning" and "model evaluation"
   concepts to introduce foundation models, tokens, embeddings, and the LLM
   lifecycle.
3. **[Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md)**
   assumes you already know *what* a foundation model and embedding are
   (Domain 2) and *what* fine-tuning means as a form of supervised learning
   (Domain 1) before it teaches you to *apply* those concepts — RAG,
   customization trade-offs, Bedrock features, and FM evaluation all build
   on prior material rather than re-explaining it.
4. **[Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md)**
   depends on Domain 1's bias–variance vocabulary (to avoid confusing
   statistical bias with fairness bias) and on Domain 1/3's model-evaluation
   and customization vocabulary (to reason about the performance vs.
   interpretability trade-off).
5. **[Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md)**
   assumes familiarity with the AWS services introduced in Domains 1–3
   (SageMaker, Bedrock) before layering security, compliance, and governance
   controls on top of them.

**Do not start at Domain 3** just because it carries the most exam weight.
A learner who jumps straight to Domain 3 without Domains 1–2 will
repeatedly hit terms (embeddings, supervised learning, foundation models)
that Domain 3 assumes are already understood, and will spend more total
time backfilling gaps than if the domains had been read in order the first
time. Weight-based prioritization (Section 2) is a tool for your *review*
and *cram* passes once you've completed a first pass in reading order — see
the [1-week plan](#1-week-plan-time-constrained-review) below for how the
two strategies combine when time is short.

---

## 4. Common exam traps (consolidated from every domain's "Exam tip" callouts)

Every numbered section across all five domain guides ends with an "Exam
tip" — a specific, high-yield distractor or pitfall the exam is known to
test. This section consolidates all of them into one list, organized by
domain, so you can do a final pass over every trap without re-reading all
five guides. Follow each link back to the full explanation if a trap
doesn't immediately make sense on its own.

### Domain 1 traps

- The **AI ⊃ ML ⊃ DL ⊃ Generative AI** nesting relationship is tested with
  reversed distractors (e.g., "ML is a type of deep learning"); also know
  **parameter** (learned) vs. **hyperparameter** (configured by a person).
  ([§1](domain-1-fundamentals-of-ai-and-ml.md#1-basic-aimldl-terminology-and-concepts))
- Memorize the ML lifecycle order: **collect → explore → prepare/feature-engineer
  → train → evaluate/tune → deploy → monitor.** Feature Store exists
  specifically to prevent training/serving skew.
  ([§2](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle))
- Data with **no labels** → **unsupervised**, even if the goal sounds like
  "prediction." Reinforcement learning = *agent + environment + reward*, not
  just "no labels."
  ([§3](domain-1-fundamentals-of-ai-and-ml.md#3-types-of-learning))
- Match the scenario's **verb** to the AWS service: "detect fraud" → Fraud
  Detector; "recommend" → Personalize; "predict demand" → Forecast; "read a
  scanned form" → Textract (not Comprehend, which analyzes plain-text
  meaning, not layout).
  ([§4](domain-1-fundamentals-of-ai-and-ml.md#4-common-use-cases-for-aiml))
- "No ML expertise, wants X" → a **purpose-built managed AI service**, not
  SageMaker. SageMaker is the answer only for custom models or uncovered use
  cases.
  ([§5](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview),
  [comparison table](domain-1-fundamentals-of-ai-and-ml.md#comparison-table-aws-managed-aiml-services-at-a-glance))
- **Class imbalance** (fraud, disease detection) → precision/recall/F1/AUC-ROC,
  almost never plain accuracy. Raising the classification threshold
  increases precision and decreases recall.
  ([§6](domain-1-fundamentals-of-ai-and-ml.md#6-model-evaluation-basics))
- "Great on training, bad on test/production" → **overfitting/high
  variance**. "Bad on both" → **underfitting/high bias.**
  ([§7](domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off))

### Domain 2 traps

- Distinguish **embedding** (semantic representation) from **vector**
  (the numeric array) from **vector database** (where vectors are stored).
  Tokens ≠ words — pricing and context windows are measured in tokens.
  ([§1](domain-2-fundamentals-of-generative-ai.md#1-generative-ai-core-concepts))
- **Up-to-date/proprietary data without retraining** → RAG. **Specific
  tone/format/specialized labeled task** → fine-tuning. Full pretraining of
  a new foundation model is almost never the right business-scenario
  answer.
  ([§2](domain-2-fundamentals-of-generative-ai.md#2-llm-lifecycle-basics))
- **Hallucination** (confidently fabricating facts) ≠ general **inaccuracy**
  (just wrong/low quality). Lower temperature reduces but doesn't eliminate
  hallucination/nondeterminism.
  ([§3](domain-2-fundamentals-of-generative-ai.md#3-advantages-and-disadvantages-of-generative-ai))
- Assistant grounded in **enterprise data with minimal setup** → **Amazon Q
  Business**, not a custom Bedrock build from scratch.
  ([§4](domain-2-fundamentals-of-generative-ai.md#4-business-use-cases-for-generative-ai))
- "No-code, quick experimentation" → PartyRock; "managed, single API across
  FMs" → Bedrock; "pre-built enterprise assistant" → Amazon Q Business;
  "coding companion" → Amazon Q Developer; "deep customization + SageMaker
  pipelines" → SageMaker JumpStart.
  ([§5](domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities),
  [comparison table](domain-2-fundamentals-of-generative-ai.md#comparison-table-aws-generative-ai-services-at-a-glance))
- **Few-shot** (examples in the prompt) changes nothing about the model
  itself, unlike **fine-tuning** (retrains weights). Multi-step reasoning
  without retraining → **chain-of-thought prompting**.
  ([§6](domain-2-fundamentals-of-generative-ai.md#6-prompt-engineering-fundamentals))
- Weigh **all** stated constraints (latency, cost, modality) together — the
  biggest/most capable model is not automatically the right answer.
  ([§7](domain-2-fundamentals-of-generative-ai.md#7-foundation-model-selection-criteria))

### Domain 3 traps

- "Real-time/responsive/conversational" → favor latency (smaller model or
  provisioned throughput). "Cost-sensitive/spiky traffic" → on-demand.
  Always filter by **modality** first — a cheap model that can't process
  the required input type is never the answer.
  ([§1](domain-3-applications-of-foundation-models.md#1-design-considerations-for-foundation-model-applications))
- Prompt engineering **never changes model weights** — it's the cheapest,
  fastest customization option. Multi-step reasoning with no extra data or
  cost → chain-of-thought, not fine-tuning.
  ([§2](domain-3-applications-of-foundation-models.md#2-prompt-engineering-techniques))
- RAG **does not modify model weights** — it changes the prompt. "Keep
  responses current" or "reduce hallucination via our own documents" → RAG
  / Knowledge Bases, not fine-tuning.
  ([§3](domain-3-applications-of-foundation-models.md#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases))
- "Always access the latest catalog/data" → **RAG**, not fine-tuning
  (fine-tuning bakes in static, staling knowledge). Fine-tuning needs
  **labeled** pairs; continued pre-training needs only **unlabeled** domain
  text.
  ([§4](domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering))
- Match the keyword to the Bedrock feature: "take actions/call APIs" →
  Agents; "block harmful content" → Guardrails; "answer from our documents"
  → Knowledge Bases; "compare models at scale" → automatic evaluation;
  "judge subjective quality" → human evaluation; "steady high volume" →
  provisioned throughput; "spiky/unpredictable volume" → on-demand.
  ([§5](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features))
- Managing your own embeddings model + similarity index → **vector
  database** (OpenSearch, Aurora/RDS pgvector). "Search our documents in
  natural language," no mention of managing embeddings → **Amazon Kendra**.
  ([§6](domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval))
- Keep three evaluation layers distinct: **benchmark datasets** (objective/
  automatic), **human evaluation** (subjective), **business metrics**
  (real-world outcome — the only one tied to business goals).
  ([§7](domain-3-applications-of-foundation-models.md#7-evaluating-foundation-model-performance))
- **AWS Trainium → training. AWS Inferentia → inference.** Purpose-built
  chips for lower cost at scale, not general-purpose GPUs.
  ([§8](domain-3-applications-of-foundation-models.md#8-aws-infrastructure-for-generative-ai-workloads))
- The customization-spectrum table (prompt engineering → RAG → fine-tuning
  → continued pre-training) is this domain's **single most-tested
  decision** — know which two never touch model weights and which two
  retrain it.
  ([comparison table](domain-3-applications-of-foundation-models.md#comparison-table-customization-approaches-for-foundation-model-applications))

### Domain 4 traps

- Map each scenario phrase to its specific responsible-AI dimension: "why
  did the model say that?" → explainability; "documented/disclosed?" →
  transparency; "equally fair across groups?" → fairness; "human can stop
  it?" → controllability; "trustworthy under stress?" → veracity/robustness.
  ([§1](domain-4-guidelines-for-responsible-ai.md#1-core-dimensions-of-responsible-ai))
- **Bias** (systematic, unfair skew — responsible AI) ≠ **variance**
  (sensitivity to data fluctuations — Domain 1's overfitting concept).
  SageMaker Clarify measures bias **both** pre-training (on the dataset)
  and post-training (on predictions).
  ([§2](domain-4-guidelines-for-responsible-ai.md#2-identifying-bias-and-fairness-issues-in-training-data-and-model-outputs))
- **Model Card** = you document your own model. **AI Service Card** = AWS
  documents its own managed service and you just read it. Clarify = bias
  detection/explainability; Guardrails = runtime content/safety filtering.
  ([§3](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai))
- Reducing legal risk from **copyright infringement** → look for **IP
  indemnification** on Bedrock, not Guardrails (which covers safety/privacy,
  not copyright). Keep toxicity, privacy, and IP as separate categories.
  ([§4](domain-4-guidelines-for-responsible-ai.md#4-legal-and-ethical-considerations))
- **Regulatory/legal accountability** → favor interpretability, even at some
  accuracy cost. **Maximum accuracy, low individual stakes** → favor
  performance; SHAP/Clarify adds partial transparency, it doesn't replace
  choosing a simpler model.
  ([§5](domain-4-guidelines-for-responsible-ai.md#5-balancing-model-performance-and-interpretability))

### Domain 5 traps

- A service calling another AWS service on your behalf → **attach an IAM
  role**, never "embed an access key."
  ([§1](domain-5-security-compliance-governance.md#1-securing-ai-systems))
- "Encryption at rest" = data on disk (S3/EBS/KMS). "Encryption in transit"
  = data moving over the network (TLS/HTTPS). KMS manages *keys*; CloudTrail
  *logs* key usage — don't confuse the two.
  ([§1](domain-5-security-compliance-governance.md#1-securing-ai-systems))
- Data must never traverse the public internet / isolated VPC → **VPC
  endpoint (PrivateLink)**, not a NAT gateway (still public-routed) or a VPN
  (connects networks, not a VPC to a service).
  ([§1](domain-5-security-compliance-governance.md#1-securing-ai-systems))
- **Source citation** = end-user trust in generated output (RAG citing
  documents). **Data lineage** = tracing a dataset/model's history for
  governance. Don't conflate the two.
  ([§1](domain-5-security-compliance-governance.md#1-securing-ai-systems))
- **HIPAA** is US healthcare-specific; **GDPR** is EU personal-data general
  regulation — both tested at a conceptual level only. PHI → BAA +
  HIPAA-eligible services.
  ([§2](domain-5-security-compliance-governance.md#2-aws-compliance-standards-relevant-to-ai-workloads))
- **CloudTrail** = API activity log. **Config** = resource
  configuration/compliance state over time. **Audit Manager** = automated
  evidence collection for audits. "Which service shows a bucket became
  public 3 days ago" → Config, not CloudTrail.
  ([§3](domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance))
- **Discovering sensitive data (PII/PHI)** → Amazon Macie. **Operational
  metrics/logs** → CloudWatch. **Threat detection** → GuardDuty. Commonly
  offered as distractors for each other.
  ([§4](domain-5-security-compliance-governance.md#4-data-governance-strategies))
- The more "managed" the AI service (Bedrock > SageMaker JumpStart >
  SageMaker custom training), the less infrastructure security you handle —
  but **you are always responsible for your own data and access
  configuration**, regardless of how managed the service is.
  ([§5](domain-5-security-compliance-governance.md#5-aws-shared-responsibility-model-applied-to-aiml-services))

---

## 5. Study plans

All three plans below cover the same ground — all five domains, the
[AWS service decision guide](aws-service-decision-guide.md), the
[GLOSSARY.md](GLOSSARY.md), the
[cross-domain concept map](cross-domain-concept-map.md), and every domain's
practice questions — at increasing levels of compression. Pick the plan
that matches your available time, and use [Section 1](#1-exam-format-and-time-management)'s
pacing advice on every practice-question pass.

### 4-week plan (thorough, prerequisite-ordered)

Best if you're new to AI/ML concepts and want to build understanding before
compressing for review.

| Week | Focus | Activities |
|---|---|---|
| 1 | [Domain 1](domain-1-fundamentals-of-ai-and-ml.md) (~20%) | Days 1–4: read all 7 sections and the comparison table, taking notes on each "Exam tip." Days 5–6: work all practice questions untimed, then re-attempt missed ones. Day 7: read the [cross-domain concept map](cross-domain-concept-map.md)'s Domain 1 rows to preview where this material resurfaces later. |
| 2 | [Domain 2](domain-2-fundamentals-of-generative-ai.md) (~24%) | Days 1–4: read all 7 sections and the comparison table. Days 5–6: practice questions, review explanations for every wrong answer. Day 7: cross-reference Domain 1 terms that reappear (tokens, supervised learning as fine-tuning) using [GLOSSARY.md](GLOSSARY.md). |
| 3 | [Domain 3](domain-3-applications-of-foundation-models.md) (~28%, highest weight) | Days 1–5: read all 8 sections and the comparison table — this domain gets the most days of any single domain. Day 6: practice questions. Day 7: read the [AWS service decision guide](aws-service-decision-guide.md)'s decision flow and the Domain 1→3 rows of the concept map. |
| 4 | [Domain 4](domain-4-guidelines-for-responsible-ai.md) + [Domain 5](domain-5-security-compliance-governance.md) (~14% each) + full review | Days 1–2: Domain 4 (read + practice questions). Days 3–4: Domain 5 (read + practice questions). Day 5: full read of [GLOSSARY.md](GLOSSARY.md), [aws-service-decision-guide.md](aws-service-decision-guide.md), and [Section 4](#4-common-exam-traps-consolidated-from-every-domains-exam-tip-callouts) above. Day 6: take the [full-length mock exam](full-length-mock-exam.md) (65 questions weighted and mixed across all five domains, 90 minutes). Day 7: review every missed mock question and re-read the matching domain section it came from. |

### 2-week plan (condensed, still prerequisite-ordered)

Best if you already have some AI/ML background and mainly need the
exam-specific framing and AWS service mappings.

| Day | Focus |
|---|---|
| 1 | [Domain 1](domain-1-fundamentals-of-ai-and-ml.md): full read + comparison table. |
| 2 | [Domain 2](domain-2-fundamentals-of-generative-ai.md) sections 1–4. |
| 3 | [Domain 2](domain-2-fundamentals-of-generative-ai.md) sections 5–7 + comparison table + practice questions. |
| 4 | [Domain 3](domain-3-applications-of-foundation-models.md) sections 1–3 (design considerations, prompt engineering, RAG). |
| 5 | [Domain 3](domain-3-applications-of-foundation-models.md) sections 4–6 (customization spectrum, Bedrock features, vector databases). |
| 6 | [Domain 3](domain-3-applications-of-foundation-models.md) sections 7–8 + comparison table + practice questions. |
| 7 | [Domain 4](domain-4-guidelines-for-responsible-ai.md): full read + comparison table + practice questions. |
| 8 | [Domain 5](domain-5-security-compliance-governance.md): full read + comparison table + practice questions. |
| 9 | [AWS service decision guide](aws-service-decision-guide.md), [GLOSSARY.md](GLOSSARY.md), and [cross-domain concept map](cross-domain-concept-map.md) — consolidate cross-domain connections. |
| 10 | Untimed pass over all ~85 practice questions across all five domains; re-read the explanation for every question you got wrong or were unsure about. |
| 11 | Re-review Domains 2 and 3 only (52% of the exam combined) using [Section 2](#2-domain-weights-and-high-yield-focus-areas)'s high-yield list — this is a weighted review pass, not a full re-read. |
| 12 | Take the [full-length mock exam](full-length-mock-exam.md): 65 questions, 90 minutes, weighted and mixed across all five domains. Score it against the 700/1000 passing bar (≈ 54/65 as a rough proxy, since the real scale is nonlinear). Then work through the [cross-domain scenario questions](cross-domain-scenario-questions.md) to practice combining two domains' knowledge in a single question. |
| 13 | Review every missed mock question against [Section 4](#4-common-exam-traps-consolidated-from-every-domains-exam-tip-callouts) — most missed questions map directly onto one of the consolidated traps. |
| 14 | Light final review only: skim [Section 4](#4-common-exam-traps-consolidated-from-every-domains-exam-tip-callouts) and the glossary terms you've flagged as weak. Avoid cramming new material the day before the exam. |

### 1-week plan (time-constrained review)

**This plan assumes you already have general AI/ML/cloud familiarity** and
need exam-specific review, not first-time learning. If you are learning
this material for the first time, use the 4-week or 2-week plan instead —
compressing to a week only works because it skips building foundational
understanding from scratch, and Domain 3 (day 1 below) assumes you already
recognize the Domain 1/2 vocabulary it builds on.

This plan is intentionally **weight-ordered rather than prerequisite-ordered**
(see [Section 3](#3-recommended-reading-order)) to maximize expected score
per hour studied when time is the binding constraint:

| Day | Focus |
|---|---|
| 1 | [Domain 3](domain-3-applications-of-foundation-models.md) (~28%, highest weight) — full read + comparison table + practice questions. |
| 2 | [Domain 2](domain-2-fundamentals-of-generative-ai.md) (~24%) — full read + comparison table + practice questions. |
| 3 | [Domain 1](domain-1-fundamentals-of-ai-and-ml.md) (~20%) — full read + comparison table + practice questions. |
| 4 | [Domain 4](domain-4-guidelines-for-responsible-ai.md) and [Domain 5](domain-5-security-compliance-governance.md) (~14% each) — full read + comparison tables + practice questions for both. |
| 5 | [AWS service decision guide](aws-service-decision-guide.md) + [GLOSSARY.md](GLOSSARY.md) skim + [Section 4](#4-common-exam-traps-consolidated-from-every-domains-exam-tip-callouts) in full. |
| 6 | Take the [full-length mock exam](full-length-mock-exam.md): 65 questions, 90 minutes, weighted and mixed across all five domains. Score it and identify your two weakest domains. Also work through the [cross-domain scenario questions](cross-domain-scenario-questions.md) for practice combining domains in one question. |
| 7 | Re-review only your two weakest domains from Day 6, plus a final skim of [Section 4](#4-common-exam-traps-consolidated-from-every-domains-exam-tip-callouts). Keep the day before the exam light — recognition review, not new material. |

---

## 6. Topic-based review quick reference

The [full-length mock exam](full-length-mock-exam.md)'s
[score-band remediation tables](full-length-mock-exam.md#score-band-remediation-by-domain)
are *domain*-shaped: they take your weakest domain's score and point you at
specific sections within that one domain's guide. That works well when an
entire domain is weak, but not every review gap is domain-shaped — a missed
mock-exam question or practice question often traces back to one narrow
*topic* that cuts across several domains at once, not a whole domain. If
you already know the specific concept you're shaky on (not just which
domain it lives in), this section gets you there faster than re-reading a
domain guide end to end.

Each table below covers one high-leverage, cross-domain topic and links to
where it's covered in every domain guide that addresses it, plus the
matching entry in the [cross-domain concept map](cross-domain-concept-map.md),
which explains *why* the topic connects across domains rather than just
that it does.

### Cost governance

Bounding what an AI workload actually costs — per request and in total —
comes up from Domain 1's build-vs-buy service choice through Domain 3 and
Domain 5's dedicated cost-control mechanics.

| Guide | Section |
|---|---|
| Domain 1 | [§5 AWS managed AI/ML services (conceptual overview)](domain-1-fundamentals-of-ai-and-ml.md#5-aws-managed-aiml-services-conceptual-overview) — choosing a purpose-built managed service over a custom SageMaker model is a build-vs-buy cost decision before it's anything else |
| Domain 2 | [§7 Foundation model selection criteria](domain-2-fundamentals-of-generative-ai.md#7-foundation-model-selection-criteria) — cost is one of the selection criteria weighed alongside latency and context window |
| Domain 3 | [Cost governance: bounding per-request cost with max tokens and provisioned throughput](domain-3-applications-of-foundation-models.md#cost-governance-bounding-per-request-cost-with-max-tokens-and-provisioned-throughput) |
| Domain 4 | [§4 Legal and ethical considerations](domain-4-guidelines-for-responsible-ai.md#4-legal-and-ethical-considerations) — the environmental-impact bullet covers the compute/resource cost of training and running foundation models |
| Domain 5 | [Cost governance: bounding total spend with Service Quotas and API Gateway usage plans](domain-5-security-compliance-governance.md#cost-governance-bounding-total-spend-with-service-quotas-and-api-gateway-usage-plans) |
| Cross-domain concept map | [Domain 2 → Domain 3: Applications of Foundation Models](cross-domain-concept-map.md#domain-2-domain-3-applications-of-foundation-models) — traces how Domain 2's cost/latency selection criteria become Domain 3's application-design decisions |

### Bias and fairness

The exam tests a specific distinction here: *statistical* bias (a model-fit
property) versus *fairness* bias (a systematic, unfair skew toward or
against a demographic group) — and where each kind of bias can enter a
system.

| Guide | Section |
|---|---|
| Domain 1 | [§7 Overfitting, underfitting, and the bias–variance trade-off](domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off) — the *statistical* bias definition that fairness bias is commonly confused with |
| Domain 2 | [§3 Advantages and disadvantages of generative AI](domain-2-fundamentals-of-generative-ai.md#3-advantages-and-disadvantages-of-generative-ai) — hallucination, the generative-AI failure mode Domain 4 teaches you to distinguish from fairness-driven output skew |
| Domain 3 | [§3 Retrieval Augmented Generation (RAG) and Amazon Bedrock Knowledge Bases](domain-3-applications-of-foundation-models.md#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases) — a RAG knowledge base's documents are a second source of bias on top of the base model's training data |
| Domain 4 | [§2 Identifying bias and fairness issues in training data and model outputs](domain-4-guidelines-for-responsible-ai.md#2-identifying-bias-and-fairness-issues-in-training-data-and-model-outputs) (primary coverage) |
| Domain 5 | [Common security threats to AI systems and how to mitigate them](domain-5-security-compliance-governance.md#common-security-threats-to-ai-systems-and-how-to-mitigate-them) — training-data poisoning as a deliberate attack that biases a model |
| Cross-domain concept map | [Commonly confused concept pairs (quick reference)](cross-domain-concept-map.md#commonly-confused-concept-pairs-quick-reference) — the statistical-bias-vs-fairness-bias row |

### RAG (Retrieval-Augmented Generation) concepts

RAG spans a design decision (Domain 3), a responsible-AI risk (Domain 4),
and a governance/traceability requirement (Domain 5) — all attached to the
same retrieval corpus.

| Guide | Section |
|---|---|
| Domain 1 | [§2 The ML development lifecycle](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle) — the data collection/preparation discipline that curating a RAG retrieval corpus borrows from |
| Domain 2 | [§1 Generative AI core concepts](domain-2-fundamentals-of-generative-ai.md#1-generative-ai-core-concepts) — tokens and embeddings, the building blocks RAG retrieval operates on |
| Domain 3 | [§3 Retrieval Augmented Generation (RAG) and Amazon Bedrock Knowledge Bases](domain-3-applications-of-foundation-models.md#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases) (primary coverage) and [§6 Vector databases and embeddings for search and retrieval](domain-3-applications-of-foundation-models.md#6-vector-databases-and-embeddings-for-search-and-retrieval) |
| Domain 4 | [Worked example: diagnosing retrieval-induced bias and hallucination in a RAG-based HR assistant](domain-4-guidelines-for-responsible-ai.md#worked-example-diagnosing-retrieval-induced-bias-and-hallucination-in-a-rag-based-hr-assistant) |
| Domain 5 | [Source citation and data lineage](domain-5-security-compliance-governance.md#source-citation-and-data-lineage) |
| Cross-domain concept map | [Domain 3 → Domain 5: Security, Compliance, and Governance](cross-domain-concept-map.md#domain-3-domain-5-security-compliance-and-governance) — RAG's source citation reframed as a data-lineage and governance requirement, not just a UX nicety |

### Model evaluation and performance measurement

The same underlying question — "how good is this model, and how do you
know?" — starts as classical model evaluation in Domain 1 and gets
extended, not replaced, all the way through Domain 5's audit evidence.

| Guide | Section |
|---|---|
| Domain 1 | [§6 Model evaluation basics](domain-1-fundamentals-of-ai-and-ml.md#6-model-evaluation-basics) (primary coverage — accuracy, precision, recall, F1, AUC-ROC) |
| Domain 2 | [§7 Foundation model selection criteria](domain-2-fundamentals-of-generative-ai.md#7-foundation-model-selection-criteria) — comparing models against each other on cost, latency, and context window is an evaluative judgment that precedes evaluating a deployed model's output |
| Domain 3 | [§7 Evaluating foundation model performance](domain-3-applications-of-foundation-models.md#7-evaluating-foundation-model-performance) (primary coverage) |
| Domain 4 | [§5 Balancing model performance and interpretability](domain-4-guidelines-for-responsible-ai.md#5-balancing-model-performance-and-interpretability) — weighing performance against interpretability assumes you can already measure the performance side |
| Domain 5 | [§3 AWS Config, AWS Audit Manager, and AWS CloudTrail for AI governance](domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance) — Audit Manager collects evaluation evidence for compliance reporting |
| Cross-domain concept map | [Domain 1 → Domain 3: Applications of Foundation Models](cross-domain-concept-map.md#domain-1-domain-3-applications-of-foundation-models) — the row tracing Domain 1's classification metrics into Domain 3's FM evaluation framework |
