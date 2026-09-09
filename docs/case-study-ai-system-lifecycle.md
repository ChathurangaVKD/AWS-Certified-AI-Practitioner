# Case Study: Solstice Outdoors Builds an AI Shopping Assistant

**Last verified:** 2026-09-06 — this case study traces AWS services across
all five domains as Trailhead moves through its lifecycle. Re-verify at
least every 90 days, or sooner if a linked domain guide's own
**Last verified** date moves.

Every domain guide in this series illustrates its concepts with a one-off
**AWS example** — a company, a scenario, a paragraph, then on to the next
topic. That's useful for isolating a single concept, but it hides something
the exam (and real projects) test constantly: a single AI system moves
through *all five domains* over its lifetime, and decisions made in one
domain directly constrain the options available in the next.

This case study follows one fictional company, **Solstice Outdoors** (a
mid-size outdoor-gear retailer), building one system — **Trailhead**, a
customer-facing shopping and support assistant — from a classic ML model
through a deployed, governed generative AI product. Each phase below maps to
one exam domain, in the order Solstice actually built the system, and links
back to the full explanation of every concept it uses in its home domain
guide. Read it after you've studied the five domain guides individually, as
a way to see the pieces assembled into one coherent story.

> **How to read this case study:** each phase is a decision point Solstice
> faced, not just a feature description. Where the exam tests "what would
> you do here, and why," this case study shows the reasoning, not just the
> outcome.

---

## The system, end to end

| Phase | Domain | What Solstice built | Key AWS services |
|---|---|---|---|
| 1 | [Domain 1](domain-1-fundamentals-of-ai-and-ml.md) — ML fundamentals and lifecycle | A classical **return-prediction model** to flag orders likely to be returned | Amazon SageMaker, S3 |
| 2 | [Domain 2](domain-2-fundamentals-of-generative-ai.md) — Evaluating generative AI | A **build vs. buy vs. foundation-model** decision and FM shortlist for a chatbot | Amazon Bedrock, PartyRock |
| 3 | [Domain 3](domain-3-applications-of-foundation-models.md) — Designing and customizing an FM application | **Trailhead**: a RAG + agentic chatbot over the product catalog and order system | Bedrock Knowledge Bases, Bedrock Agents, OpenSearch Serverless |
| 4 | [Domain 4](domain-4-guidelines-for-responsible-ai.md) — Bias and responsible AI | Bias testing and guardrails after Trailhead under-recommended a product line | SageMaker Clarify, Bedrock Guardrails |
| 5 | [Domain 5](domain-5-security-compliance-governance.md) — Security, compliance, and governance | Locking down and auditing Trailhead ahead of a public launch | IAM, KMS, PrivateLink, CloudTrail, Audit Manager |

---

## Phase 1 (Domain 1): a classical ML model, before anyone says "generative AI"

Before Solstice touches a foundation model, it has an ordinary ML problem:
too many orders come back as returns, and the fulfillment team wants a
model that flags high-return-risk orders at checkout so it can suggest a
better fit (size, material) before the order ships.

This is a textbook run through the
[ML development lifecycle](domain-1-fundamentals-of-ai-and-ml.md#2-the-ml-development-lifecycle):
Solstice defines the business goal (reduce return rate), collects and
prepares two years of order, product, and return history in S3, engineers
features (item category, size-chart mismatches, customer's past return
rate), trains a model in Amazon SageMaker, and evaluates it before
deploying it as a real-time SageMaker endpoint called during checkout.

Two Domain 1 decisions turn out to matter much later:

- **Types of learning.** Return/no-return is a labeled outcome in the
  historical data, so this is
  [supervised learning](domain-1-fundamentals-of-ai-and-ml.md#3-types-of-learning) —
  specifically binary classification. Solstice's data science lead flags
  this explicitly in the design doc, because the team will need to make the
  same supervised-vs-unsupervised-vs-reinforcement call again in Phase 3
  when deciding how to customize a foundation model.
- **Model evaluation basics.** Only 8% of orders are actually returned, so
  training accuracy alone is misleading — a model that always predicts "no
  return" would score 92%. Solstice evaluates on
  [precision, recall, F1, and AUC-ROC](domain-1-fundamentals-of-ai-and-ml.md#6-model-evaluation-basics)
  instead, and tunes the classification threshold to favor **recall**
  (catch more true return risks) at the cost of some false positives,
  since a false "this might not fit" nudge is cheap and a missed return is
  expensive.

The first version of the model badly overfits: it memorizes quirks of one
regional warehouse's return patterns and performs far worse on other
regions' held-out data — a textbook high-variance problem from
[overfitting, underfitting, and the bias–variance trade-off](domain-1-fundamentals-of-ai-and-ml.md#7-overfitting-underfitting-and-the-biasvariance-trade-off).
The fix is more training data across regions and regularization, not a
bigger model.

**Why this matters later:** the return-prediction model isn't just a side
project — its labeled, cleaned order/product history in S3 becomes the raw
material Trailhead's knowledge base retrieves from in Phase 3, and the
lifecycle discipline (define goal → prepare data → train → evaluate →
deploy → monitor) is the same discipline Solstice reuses, renamed, for
every phase after this one.

## Phase 2 (Domain 2): deciding generative AI is the right tool, and picking a model

Customer support tickets ("does this jacket run small?", "where's my
order?") are growing faster than the support team, and a simple FAQ bot
already frustrates customers by not understanding free-form questions.
Solstice's product manager wants a chatbot — but Domain 2 is where the team
first has to justify *why generative AI*, not just reach for it.

The team walks through the
[advantages and disadvantages of generative AI](domain-2-fundamentals-of-generative-ai.md#3-advantages-and-disadvantages-of-generative-ai)
honestly: an LLM can handle open-ended, natural-language questions the old
rules-based bot can't, but it also introduces
[hallucination risk](domain-2-fundamentals-of-generative-ai.md#3-advantages-and-disadvantages-of-generative-ai)
(making up a return policy that doesn't exist) that the return-prediction
model in Phase 1 never had to worry about. They decide the upside is worth it *if*
the bot's factual claims are grounded in real Solstice data — a
requirement that shapes every choice in Phase 3.

Two more Domain 2 concepts drive the next decision:

- **LLM lifecycle basics.** The team maps out the
  [LLM lifecycle](domain-2-fundamentals-of-generative-ai.md#2-llm-lifecycle-basics)
  from data selection through pre-training, fine-tuning, and evaluation —
  and immediately rules out pre-training their own model. Training a
  foundation model from scratch requires far more data and compute than a
  gear retailer has any reason to spend on; the exam-tested lesson (almost
  no organization pretrains its own FM) applies directly.
- **Foundation model selection criteria.** Comparing candidate Bedrock
  models on
  [selection criteria](domain-2-fundamentals-of-generative-ai.md#7-foundation-model-selection-criteria) —
  context window (needs to hold a multi-turn conversation plus retrieved
  product docs), latency (customers won't wait 10 seconds for a chat
  reply), cost per token, and modality (text-only is enough; Solstice
  doesn't need image generation) — narrows the shortlist to a small,
  fast, text-focused model for the primary chat flow.

Before committing engineering time, a couple of Solstice's product team
prototype prompts for the "does this run small?" use case in **PartyRock**,
using
[prompt engineering fundamentals](domain-2-fundamentals-of-generative-ai.md#6-prompt-engineering-fundamentals) —
zero-shot vs. few-shot phrasing, instructions vs. context — to see whether
a well-crafted prompt alone gets close enough before any custom
infrastructure is built.

**Why this matters later:** the "must be grounded in real data" requirement
from this phase is exactly what makes Retrieval Augmented Generation the
right customization choice in Phase 3, and the "no pre-training, no
in-house model" decision is what keeps Solstice inside Bedrock instead of
standing up SageMaker training jobs for the FM itself.

## Phase 3 (Domain 3): designing and customizing Trailhead

With a model shortlisted and the grounding requirement set, Solstice builds
**Trailhead**: a chatbot that answers product-fit questions, looks up order
status, and explains the return policy — using Solstice's own data, not
just the model's general knowledge.

The core design decision is
[fine-tuning vs. continued pre-training vs. RAG vs. prompt engineering](domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering).
Fine-tuning is rejected: Solstice's product catalog and return policy
change weekly, and re-fine-tuning a model every week to keep it current is
slow and expensive. Instead, the team builds
[Retrieval Augmented Generation over an Amazon Bedrock Knowledge Base](domain-3-applications-of-foundation-models.md#3-retrieval-augmented-generation-rag-and-amazon-bedrock-knowledge-bases):
product descriptions, size charts, and policy documents are chunked,
embedded, indexed in OpenSearch Serverless, and retrieved at query time, so
Trailhead's answers stay current without retraining anything. This is a
direct payoff of the Phase 1 lifecycle work — the same cleaned product and
order data that trained the return-prediction model is what gets indexed
into the knowledge base.

For "where's my order?" questions, retrieval alone isn't enough — Trailhead
needs to take an action (look up a specific order by ID), so the team adds
a
[Bedrock Agent](domain-3-applications-of-foundation-models.md#worked-example-a-bedrock-agent-executing-a-multi-step-task-with-tool-calling)
that calls an internal order-status API, following the same
[Amazon Bedrock feature set](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features)
used for the knowledge base. Before launch, Trailhead is scored with the
same rigor Phase 1 applied to the return model, just with FM-specific
methods layered on top:
[evaluating foundation model performance](domain-3-applications-of-foundation-models.md#7-evaluating-foundation-model-performance)
combines benchmark-style regression tests (does it still cite the correct
return window?) with human evaluation of tone and helpfulness, since no
single automated metric like accuracy captures "was this a good answer."

**Why this matters later:** grounding answers in retrieved product and
customer data means Trailhead can now surface biased or unfair patterns
that were latent in that data all along — which is exactly what Phase 4
catches.

## Phase 4 (Domain 4): Trailhead has a bias problem

A month after launch, a merchandising analyst notices Trailhead rarely
recommends Solstice's plus-size and adaptive-fit product line, even when a
customer's question is a near-perfect match for it. This is a responsible-AI
incident, not a retrieval bug — the underlying data (past orders,
merchandising copy, review volume) simply contains far fewer examples of
that product line, so retrieval and generation both under-surface it.

The team is careful not to conflate this with the Phase 1 bias–variance
discussion — Domain 4 draws that line explicitly:
[identifying bias and fairness issues in training data and model outputs](domain-4-guidelines-for-responsible-ai.md#2-identifying-bias-and-fairness-issues-in-training-data-and-model-outputs)
covers *systematic, unfair skew toward or against a group*, a completely
different concept from the statistical high-bias/high-variance properties
of a model fit from Phase 1, even though both use the word "bias."

Solstice runs
**Amazon SageMaker Clarify** — one of the
[AWS tools for responsible AI](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai) —
against the underlying order and catalog data to quantify the
under-representation, confirming a **sampling bias** in the training and
retrieval corpus rather than a model defect. The fix spans two layers: the
merchandising team backfills more content and reviews for the affected
product line (fixing the data), and the engineering team adds a
[Bedrock Guardrail](domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai)
to Trailhead so its recommendation prompts explicitly
require considering the full catalog rather than only the
highest-frequency items (fixing the application). This reflects the
[core dimensions of responsible AI](domain-4-guidelines-for-responsible-ai.md#1-core-dimensions-of-responsible-ai) —
fairness and robustness — that AWS expects a deployed system to be
evaluated against on an ongoing basis, not just at launch.

The incident also forces a
[performance vs. interpretability](domain-4-guidelines-for-responsible-ai.md#5-balancing-model-performance-and-interpretability)
conversation: leadership initially wants to swap in a larger, more capable
foundation model to "just do better," but the team pushes back — a bigger
model makes the retrieval-and-generation pipeline *harder* to audit for
exactly this kind of skew, while the guardrail-plus-data fix is both
effective and explainable to the merchandising team and, eventually, to
auditors in Phase 5.

**Why this matters later:** an incident like this is exactly what Domain
5's monitoring and audit trail exist to catch earlier next time — Phase 5
is where Solstice builds the logging and review process that would have
surfaced this bias before a customer-facing complaint did.

## Phase 5 (Domain 5): securing and governing Trailhead before a public launch

Trailhead has been running in a limited beta; before Solstice opens it to
all customers, security and legal review the deployment end to end. This
phase is where every earlier decision gets locked down and made
accountable.

- **Access control.** Following
  [IAM roles and policies for AI services](domain-5-security-compliance-governance.md#iam-roles-and-policies-for-ai-services),
  the Bedrock Agent's execution role is scoped to only the specific
  order-status API and knowledge base it needs — not blanket access to
  every Solstice data store, so a compromised agent role can't reach
  unrelated systems like payroll or supplier contracts.
- **Encryption.** Customer order history and the embedded knowledge base
  are encrypted at rest with AWS KMS customer-managed keys and in transit
  with TLS, per
  [data encryption at rest and in transit](domain-5-security-compliance-governance.md#data-encryption-at-rest-and-in-transit) —
  the same S3 order data from Phase 1 now carries a stricter encryption
  requirement because it's reachable through a public-facing chatbot.
- **Network isolation.** Trailhead's backend calls to Bedrock and
  OpenSearch Serverless are routed over
  [AWS PrivateLink and VPC endpoints](domain-5-security-compliance-governance.md#aws-privatelink-and-vpc-endpoints-for-ai-services)
  rather than the public internet, keeping customer conversation data off
  the open internet path entirely.
- **Audit trail.** Solstice enables
  [AWS CloudTrail, AWS Config, and AWS Audit Manager for AI governance](domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance),
  so every Bedrock invocation, IAM policy change, and knowledge-base sync
  is logged and reviewable — the exact capability that would have
  produced an earlier, automatic signal for the Phase 4 bias incident
  instead of waiting for a manual catch.
- **Data residency.** Because Solstice now serves EU customers,
  [data residency](domain-5-security-compliance-governance.md#data-residency)
  requirements mean EU customer conversation logs and order data are kept
  in an EU AWS Region rather than the US region the original
  return-prediction model was trained in.
- **Shared responsibility.** Legal asks "if a customer sues over a bad
  Trailhead answer, is that AWS's fault or ours?" The
  [AWS shared responsibility model applied to AI/ML services](domain-5-security-compliance-governance.md#5-aws-shared-responsibility-model-applied-to-aiml-services)
  answers this directly: AWS secures the underlying Bedrock and
  SageMaker infrastructure, but Solstice is responsible for the data it
  feeds in, the guardrails and prompts it configures, and how it acts on
  Trailhead's output — the answer doesn't change because Trailhead is
  generative AI rather than the classical model from Phase 1.

With logging, encryption, access control, and a documented shared-
responsibility boundary in place, Solstice launches Trailhead publicly —
and feeds its production monitoring data (via
[data monitoring](domain-5-security-compliance-governance.md#data-monitoring))
back into the next round of Phase 1-style evaluation and Phase 4-style
bias checks, closing the loop.

---

## Why this matters for the exam

AIF-C01 scenario questions rarely stay inside one domain, and Solstice's
story shows why: the *same* dataset that trains a Domain 1 classifier
becomes a Domain 3 knowledge base; the *same* word ("bias") means a
statistical property in Domain 1 and a fairness problem in Domain 4; the
*same* IAM and encryption controls in Domain 5 apply whether the workload
is a SageMaker endpoint or a Bedrock agent. When a practice question
describes a company's AI system without naming a domain, ask which phase
of this story it resembles — that's usually the fastest way to identify
which domain's mental model the question is really testing.
