# Cross-Domain Scenario Questions (AIF-C01)

**Last verified:** 2026-09-06 — this page's scenario questions cite AWS
services, model families, and compliance details spanning all five domain
guides, so it goes stale faster than any single domain guide. Re-verify at
least every 60 days, or sooner if a linked domain guide's own
**Last verified** date moves.

> **Difficulty tiers:** Questions 1–25 are 2-domain pairings; questions
> 26–30 are the harder tier, each requiring reasoning across 3+ domains at
> once. Master the 2-domain set before attempting 26–30.

The five domain guides —
[Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md),
[Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md),
[Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md),
[Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), and
[Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md)
— each end with their own practice-question set, but every one of those
questions is scoped to a single domain. The real AIF-C01 exam frequently
does not work that way: a single scenario question can require choosing a
Domain 3 customization method *and* checking that it satisfies a Domain 5
security requirement in the same breath, or picking a Domain 1 learning
type while weighing a Domain 4 fairness concern.

This document collects 30 scenario questions that each require knowledge
from **two or more domains** to answer correctly — you cannot eliminate
every wrong option using only one domain's vocabulary. Questions 1–25 each
pair up exactly two domains, but questions 26–30 go further and each
require reasoning across **three or more domains at once** (one spans all
five), mirroring how the
[end-to-end case study](case-study-ai-system-lifecycle.md) traces a single
AI system through every domain rather than isolating one at a time. See
the [cross-domain concept map](cross-domain-concept-map.md) for the
underlying concept-to-concept connections these questions draw on, and
each domain guide linked above for the full depth on any single concept
referenced here.

Each question is tagged with a difficulty level
(**[Beginner]**/**[Intermediate]**/**[Advanced]**) and each answer names
the two or more domains it draws on, e.g. `*(Domains 3, 5)*` — or three or
more for questions 26–30, e.g. `*(Domains 1, 3, 4, 5)*`.

---

## Practice questions

1. **[Advanced]** A healthcare company is building an Amazon Bedrock-based
   chatbot that must answer patient questions using protected health
   information (PHI) contained in clinical notes stored in Amazon S3.
   Compliance requires that PHI never be baked into a model's weights, and
   access to any specific patient's data must be revocable at any time.
   Which approach best satisfies both requirements?
   A. Fine-tune a foundation model directly on the clinical notes so it "learns" the answers from training
   B. Continue pre-training the foundation model on the full clinical notes corpus
   C. Use Retrieval Augmented Generation (RAG) via Amazon Bedrock Knowledge Bases to retrieve relevant notes at query time, with an execution role scoped to only the necessary S3 prefixes and a HIPAA Business Associate Addendum in place through AWS Artifact
   D. Rely only on prompt engineering with the model's default pretrained knowledge, without incorporating any clinical notes

2. **[Intermediate]** A data science team trained a classical supervised
   learning fraud-detection model in Amazon SageMaker. Before deployment,
   they want to measure whether the model's positive-prediction ("flagged
   as fraud") rate differs significantly between two customer age groups —
   a potential fairness concern. Which AWS capability directly supports
   this, and what does it build on?
   A. Amazon SageMaker Feature Store, because it stores fairness metrics for later retrieval
   B. Amazon SageMaker Clarify, because it computes post-training bias metrics (such as disparate impact) on a model's predictions, extending the standard supervised-learning evaluation step with a fairness lens
   C. Amazon Comprehend, because it detects toxic sentiment in free text
   D. AWS Trusted Advisor, because it flags cost-optimization opportunities

3. **[Intermediate]** A bank needs guaranteed, consistent inference
   throughput for a customer-facing Amazon Bedrock assistant, and its
   security policy requires that all traffic between its VPC and Bedrock
   avoid the public internet entirely. Which combination of capabilities
   satisfies both requirements?
   A. On-demand pricing plus a NAT gateway in a public subnet
   B. Provisioned Throughput for guaranteed, consistent capacity, plus an interface VPC endpoint (AWS PrivateLink) for Bedrock Runtime to keep all traffic off the public internet
   C. Fine-tuning the model plus downloading a report from AWS Artifact
   D. Continued pre-training plus enabling AWS Config

4. **[Intermediate]** A team must choose between (1) training a classical
   SageMaker regression model on structured historical sales data to
   forecast demand, or (2) using a foundation model with RAG over
   unstructured sales reports. The available data is fully
   structured/tabular. Using standard ML lifecycle and evaluation
   vocabulary, which approach — and why — is the better fit?
   A. The foundation model with RAG, because RAG always outperforms classical models regardless of the data's shape
   B. The classical SageMaker model, because structured/tabular data is well suited to a supervised learning model with clear, easily benchmarked evaluation metrics (e.g., RMSE), whereas RAG is designed to ground generation over unstructured documents
   C. Neither; only prompt engineering should be used for numeric forecasting tasks
   D. The foundation model, because it eliminates the need for the ML lifecycle's evaluation stage entirely

5. **[Advanced]** (Select TWO.) A marketing company's Amazon Bedrock-based
   content generator must (1) block generated copy from ever mentioning a
   configured list of competitor brand names, and (2) give internal
   reviewers a documented record of the model's intended use, known
   limitations, and evaluation results for governance sign-off. Which two
   capabilities, together, satisfy both needs?
   A. Guardrails for Amazon Bedrock, using denied topics and word filters to block competitor mentions
   B. Amazon SageMaker Model Cards, to document intended use, training/evaluation details, and known limitations
   C. Amazon Comprehend, to translate the generated copy into other languages
   D. AWS Trusted Advisor, to reduce infrastructure cost
   E. AWS Config, to track EC2 instance configuration drift

6. **[Intermediate]** A copywriting team wants a foundation model to
   generate marketing slogans while explicitly excluding any reference to
   a specific competitor's trademarked product name, reducing both
   IP-infringement and brand-confusion risk. Which prompt engineering
   technique directly supports this, and what responsible-AI concern does
   it help mitigate?
   A. Chain-of-thought prompting, because it improves multi-step reasoning quality
   B. Negative prompting, explicitly instructing the model to avoid the competitor's trademarked name, which helps mitigate intellectual-property and legal risk
   C. Zero-shot prompting, because it requires no worked examples
   D. Increasing the temperature parameter, because it increases creative variety

7. **[Advanced]** (Select TWO.) A financial institution's fraud-detection
   model must be (1) checked for demographic bias in its predictions, and
   (2) able to produce audit-ready evidence — pulled automatically from
   configuration history and API logs — showing an internal risk-framework
   reviewer that the bias check was performed and documented. Which two
   AWS services fulfill these two distinct needs?
   A. Amazon SageMaker Clarify, to compute post-training bias metrics on the model's predictions
   B. AWS Audit Manager, to automatically collect and consolidate that evidence into an audit-ready compliance report
   C. Amazon Polly, to narrate the audit report aloud
   D. AWS Trainium, to accelerate model training
   E. Amazon Forecast, to predict future fraud transaction volume

8. **[Advanced]** A company operating under a strict national
   data-residency law trains a model on Amazon SageMaker. Its auditors
   require both (1) proof of exactly which raw dataset and processing job
   produced the deployed model, and (2) proof that the training data never
   left the required country's borders, even for disaster-recovery
   backups. Which combination of capabilities addresses both requirements?
   A. SageMaker ML Lineage Tracking for the dataset/model provenance graph, combined with restricting storage and processing to the in-country AWS Region and disabling cross-Region replication
   B. Amazon Macie alone, since it automatically discovers PII in S3
   C. SageMaker Feature Store alone, since it stores curated features
   D. AWS CloudTrail alone, since it logs API call activity

9. **[Intermediate]** A company wants a customer support assistant that
   can accept both text and product images from customers, reason over
   very long historical support-ticket threads, and ground its answers in
   the company's current knowledge-base articles instead of relying purely
   on the model's pretrained knowledge. Which two decisions, in order,
   should the team make first?
   A. First select a foundation model that supports multi-modal (text + image) input with a sufficiently large context window; then connect it to Amazon Bedrock Knowledge Bases via RAG to ground responses in current articles
   B. First fine-tune any available text-only model on the ticket threads; modality and context window don't matter
   C. First purchase Provisioned Throughput; RAG and modality support are irrelevant to this use case
   D. First lower the model's temperature to zero; that alone guarantees grounded, accurate answers

10. **[Advanced]** A RAG application embeds customer support transcripts,
    which contain PII, into a vector database for semantic search. The
    security team requires the stored vectors be encrypted with a
    customer-managed KMS key and that the application never traverse the
    public internet to reach the vector store. Which combination of
    choices satisfies both requirements?
    A. Amazon OpenSearch Serverless configured with a customer-managed KMS key for encryption at rest, accessed through an interface VPC endpoint
    B. Amazon Kendra with default AWS-managed encryption, accessed over the public internet
    C. Amazon Aurora with the pgvector extension, with encryption disabled for faster embedding writes
    D. Storing the raw transcripts in an unencrypted, publicly accessible S3 bucket for the model to read at query time

11. **[Intermediate]** A company has 200 labeled examples of support
    tickets sorted into 5 fixed categories, and a separate need to draft
    free-form email responses in the company's voice with no labeled
    examples of ideal replies available. Which pairing of approaches best
    matches each task?
    A. Use a classical supervised learning classifier for the fixed-category ticket classification, and few-shot prompting a foundation model for the open-ended email drafting
    B. Use few-shot prompting for both tasks, since labeled data is never useful
    C. Use a classical supervised learning classifier for both tasks, since foundation models cannot draft free-form text
    D. Use reinforcement learning for the ticket classification, since it requires no labeled data at all

12. **[Intermediate]** A company wants to minimize its AI workload's
    environmental footprint by routing training jobs to whichever AWS
    Region currently has the greenest energy mix, but its training data is
    subject to a legal data-residency requirement restricting it to one
    specific country's Region. Which consideration should take precedence?
    A. Environmental sustainability — the AWS Customer Carbon Footprint Tool's guidance should always override legal requirements
    B. The data-residency legal requirement — the training data and its processing must stay within the mandated Region regardless of that Region's energy mix, since legal and compliance obligations are non-negotiable constraints that sustainability optimizations must operate within
    C. Neither matters as long as the resulting model achieves high accuracy
    D. Sustainability and residency describe the same requirement and can never conflict

13. **[Intermediate]** A bank is deciding whether to fine-tune a foundation
    model on its historical loan-approval decisions to automate approvals,
    or instead use RAG so the model applies the bank's current, written
    underwriting policy at query time. The historical decisions are known
    to reflect past discriminatory lending practices. Which approach best
    avoids perpetuating that historical bias, and why?
    A. Fine-tune on the historical approval decisions, because fine-tuning always produces a more accurate model regardless of data quality
    B. Use RAG to ground responses in the current, vetted underwriting policy document rather than fine-tuning on the historical decisions, since fine-tuning would bake the historical bias directly into the model's weights, whereas RAG only retrieves the current policy text at query time; also run SageMaker Clarify pre-training bias metrics (e.g., difference in proportions of labels) on the historical dataset before deciding whether it's usable at all
    C. Increase the model's temperature so its decisions vary more from case to case, reducing the appearance of bias
    D. Use continued pre-training on the historical decisions instead, since it changes fewer weights than fine-tuning and therefore introduces less bias

14. **[Advanced]** (Select TWO.) A company fine-tunes a foundation model on
    internal résumé data to automate candidate shortlisting. Before
    production rollout, its responsible-AI review board requires (1)
    quantitative evidence that the fine-tuned model's shortlisting rate
    doesn't differ significantly by gender, and (2) a governance document
    capturing the model's intended use, training data source, and known
    limitations for sign-off. Which two actions satisfy these two
    requirements, respectively?
    A. Run Amazon SageMaker Clarify post-training bias metrics (e.g., disparate impact) on the fine-tuned model's shortlisting predictions
    B. Publish an Amazon SageMaker Model Card documenting the model's intended use, fine-tuning data source, and known limitations
    C. Raise the temperature parameter to produce more varied shortlisting decisions
    D. Switch from fine-tuning to Provisioned Throughput, which removes the need for a bias review
    E. Rely on Amazon Comprehend to translate résumés into additional languages

15. **[Beginner]** A content team steers a foundation model's
    customer-service tone with few-shot prompting — providing example Q&A
    pairs directly in the prompt — without any fine-tuning. During review,
    they notice every example pair happens to feature only one gender in
    leadership-role scenarios, nudging the model toward gender-skewed
    language in its outputs. What is the most direct fix, and what
    responsible-AI concept does it address?
    A. Rebalance/diversify the few-shot examples so they no longer skew toward one gender in leadership roles, directly addressing a fairness bias introduced through the prompt's example selection rather than through training data
    B. Fine-tune the model on a larger dataset instead, since prompt-level bias cannot be fixed without retraining
    C. Lower the temperature parameter, since less randomness always means less bias
    D. Switch to Retrieval Augmented Generation, since RAG automatically removes any bias present in a prompt's examples

16. **[Intermediate]** A company's customer-facing Amazon Bedrock assistant
    uses on-demand pricing. Product wants long, creative answers (a high
    max-tokens setting and a moderately high temperature), while Finance is
    worried that a bug or a flood of malicious requests could drive up
    per-token inference cost unpredictably. Which combination of actions
    addresses both the creative-output goal and the cost-governance
    concern?
    A. Tune max tokens and temperature to the desired creative output, and configure request throttling / Service Quotas (and Amazon API Gateway usage plans if the endpoint sits behind API Gateway) to cap request volume, bounding the worst-case inference cost from a traffic spike or malicious client
    B. Set max tokens to the lowest possible value at all times, eliminating cost risk but also eliminating the creative-answer requirement
    C. Rely solely on IAM policies to prevent cost overruns, since IAM controls who can call the endpoint but not how much they can call it
    D. Switch to Provisioned Throughput only; committing to reserved capacity removes any need to tune inference parameters or bound request volume

17. **[Advanced]** (Select TWO.) A regulated firm wants a Bedrock-based
    support chatbot to give detailed, quality answers while keeping its
    monthly bill predictable, since Bedrock on-demand pricing is billed per
    input/output token. An internal web app calls the endpoint through
    Amazon API Gateway. Which two actions best balance those two goals?
    A. Set max tokens (maximum length) no higher than what the use case actually needs, so responses aren't padded with unnecessary tokens the customer is billed for beyond what's useful
    B. Configure Service Quotas and Amazon API Gateway usage plans on the endpoint to bound total request volume, so a traffic spike can't translate into an unpredictable cost spike
    C. Set temperature to its maximum value, since more randomness always produces the most detailed and highest-quality answers
    D. Disable all request logging to reduce operational overhead and therefore reduce billed inference cost
    E. Purchase Provisioned Throughput sized for worst-case traffic, since only reserved capacity — never inference-parameter tuning — can bound cost

18. **[Beginner]** A startup's Bedrock-based FAQ bot sometimes returns
    extremely long, rambling answers, and Finance flags that per-request
    cost — billed per output token — is higher than expected. Which single
    inference parameter should the team adjust first to directly bound
    response length and cost, and which AWS tool gives an account-level
    view of cost-optimization opportunities to confirm the change's
    impact?
    A. Lower max tokens (maximum length) to cap how many tokens a response can contain, directly bounding per-call output-token cost; then use AWS Trusted Advisor's cost-optimization checks to review the resulting cost trend across the account
    B. Lower the temperature parameter, since temperature controls response length rather than randomness
    C. Raise top-k, since a larger candidate pool always produces shorter responses
    D. Rely on Amazon SageMaker Model Cards to automatically shorten model responses

19. **[Intermediate]** A classical SageMaker binary classifier flags loan
    applicants as "high risk" or "low risk." A fairness audit finds the
    model's false positive rate (wrongly flagging an applicant as high
    risk) is significantly higher for one demographic group than others,
    even though the model's overall accuracy looks acceptable. Which
    evaluation approach surfaces a problem that overall accuracy hides,
    and what is the most direct next step?
    A. Trust the single aggregate accuracy score across the whole test set; accuracy alone is sufficient to catch subgroup disparities, so no further action is needed
    B. Break the confusion matrix out per demographic subgroup to compare metrics like false positive rate and recall across groups, then use Amazon SageMaker Clarify's pre- and post-training bias metrics together with a human-led fairness review to decide on a mitigation such as reweighting the training data or adjusting the decision threshold per group
    C. Raise the model's overall classification threshold uniformly; a stricter threshold applied the same way to every group guarantees fairness
    D. Retrain the model with a larger learning rate, since faster convergence during training eliminates subgroup disparities in outcomes

20. **[Intermediate]** A team trains a classical SageMaker image classifier
    on images scraped almost entirely from users in one geographic region,
    then randomly splits that same pool into training, validation, and
    test sets. The model scores well on its held-out test set, but
    performs far worse in production for users from underrepresented
    regions. Why didn't the held-out test score catch this, and what
    should the team check earlier next time?
    A. The train/validation/test split ratio was wrong; switching to a 90/5/5 split would have surfaced the regional performance gap
    B. The model needs more training epochs; the gap is purely a matter of insufficient convergence and has nothing to do with the data
    C. The held-out test set was drawn from the same non-representative data-collection pool as the training data, so a strong test score couldn't reveal a representativeness gap; the team should audit whether the training data reflects the full population the model will actually serve — a fairness consideration, not just a lifecycle checkbox — before ever reaching the evaluation stage
    D. Switching from a classical model to a foundation model with RAG would automatically resolve the regional performance gap

21. **[Advanced]** A credit union's classical SageMaker model approves or
    denies personal loan applications, and regulations require that every
    denied applicant receive a specific, understandable reason for the
    denial. The data science team must choose between a complex
    gradient-boosted ensemble (highest raw accuracy) and a simpler
    logistic regression model (slightly lower accuracy, but each feature's
    contribution is directly readable from its coefficients). What
    consideration is in tension here, and how should it be resolved?
    A. Always pick the highest-accuracy model regardless of interpretability; the regulatory explanation requirement is a legal matter that shouldn't influence model selection
    B. The interpretability-versus-accuracy tradeoff in classical model selection is directly in tension with the transparency and explainability responsible-AI requirement to give denied applicants an understandable reason; the more interpretable logistic regression (or the ensemble paired with a feature-attribution tool like SageMaker Clarify) better satisfies that legal explanation requirement, even at a small accuracy cost
    C. Deploy the gradient-boosted ensemble and simply omit the denial reason, since balancing accuracy against explainability isn't a real requirement
    D. Switch to unsupervised clustering instead, since clustering models never need to produce an explanation for any individual outcome

22. **[Intermediate]** A hospital deploys a classical SageMaker model that
    scores each patient's priority for nurse review. Leadership requires
    that the model never make a final treatment decision autonomously, and
    that any prediction below a set confidence threshold be routed to a
    human for full manual review instead of being auto-actioned. Which
    mechanism enables that confidence-based routing, and what principle
    does the human-review requirement reflect?
    A. The model's predicted-probability (confidence) output can be compared against a chosen threshold to route low-confidence cases to a human reviewer rather than auto-acting on them, directly implementing the human-in-the-loop oversight and controllability principle that keeps a person accountable for high-stakes decisions
    B. Confidence thresholds are a governance-only concept; classical supervised learning models have no notion of prediction confidence to threshold on
    C. Routing low-confidence cases to a human reviewer defeats the purpose of automation and should be avoided for the sake of consistency
    D. Raising the model's temperature parameter allows it to signal low-confidence predictions for human review

23. **[Beginner]** A team wants to rapidly prototype and compare five
    different summarization approaches this week before committing
    engineering time to a full classical SageMaker training pipeline (data
    collection, feature engineering, training, tuning, and evaluation) for
    a separate numeric credit-score-adjustment task. Which approach best
    matches the standard tradeoff between these two paradigms during this
    exploratory phase?
    A. Use prompt engineering against a pretrained foundation model to quickly draft and compare the summarization approaches, since it requires no training-data collection or training cycle; reserve the classical SageMaker training pipeline's data-prep, training, tuning, and evaluation stages for the numeric credit-score task, where a dedicated, benchmarkable model is needed
    B. Skip prototyping entirely and build a full classical training pipeline for the summarization task too, since prompt engineering cannot be used to compare different approaches
    C. Use Retrieval Augmented Generation for the numeric credit-score task, since retrieval improves numeric regression accuracy
    D. Use continued pre-training for both tasks, since it is always the fastest way to prototype any task

24. **[Intermediate]** A team already evaluates a classical SageMaker
    regression model using RMSE and R² computed against a held-out test
    set, per the ML lifecycle's evaluation stage. They now want to
    evaluate a foundation model's summarization quality before choosing it
    for production. Which evaluation approach correctly extends that
    lifecycle stage to a generative task, and why?
    A. Reuse RMSE directly on the generated summary text, since RMSE is metric-agnostic and works equally well on any model output, numeric or textual
    B. Use FM benchmarking suited to open-ended generation — automated metrics like ROUGE or BERTScore against reference summaries, plus human evaluation for coherence and faithfulness — since a summary has no single "correct" numeric value the way a regression target does, but the held-out, pre-deployment evaluation principle from the ML lifecycle still applies
    C. Skip evaluation entirely, since foundation models are pretrained and already validated by their provider before release
    D. Only track training loss, since the ML lifecycle's evaluation stage concerns the training phase only, not deployment readiness

25. **[Advanced]** (Select TWO.) A financial company is building (1) a
    numeric credit-risk score that regulators will audit year over year
    against a well-defined, benchmarkable metric, and (2) a customer-facing
    assistant that summarizes each applicant's file in plain language.
    Which two statements correctly match each task to an ML paradigm and
    its standard lifecycle/evaluation step?
    A. The credit-risk score should be built as a classical supervised learning model whose performance is tracked with a standard, auditable metric such as AUC computed on a held-out test set from the ML lifecycle's evaluation stage
    B. The plain-language summarizer is better served by a foundation model, since generating fluent, varied natural-language summaries is a core foundation-model strength that a classical supervised model isn't designed to produce
    C. Both should be built as foundation models, since AUC can be computed directly on generated summary text
    D. The credit-risk score should be built as a foundation model prompted to output a risk number, since prompting requires no held-out test set at all
    E. The summarizer should be a classical supervised learning model, since natural language generation always requires labeled input-output training pairs

26. **[Advanced]** A genomics research firm wants to build an internal
    Amazon Bedrock-based assistant that answers scientists' questions using
    proprietary, unpublished genomic sequence data stored in Amazon S3.
    Auditors require (1) a verifiable record of exactly which raw dataset
    version and processing job fed the data the assistant draws on, (2)
    that the proprietary sequences never become extractable from the
    model's own weights, and (3) that all storage and processing stay
    within one required AWS Region, with cross-Region replication
    disabled. Which combination of choices satisfies all three
    requirements?
    A. Fine-tune a foundation model directly on the full sequence dataset, and enable multi-Region replication for disaster recovery
    B. Use Retrieval Augmented Generation (RAG) via Amazon Bedrock Knowledge Bases so sequences are retrieved rather than trained into the model's weights; use SageMaker ML Lineage Tracking to record which dataset version and processing job produced the indexed data; and restrict all storage/processing to the required Region with cross-Region replication disabled
    C. Continue pre-training the foundation model on the sequence data, and rely on AWS CloudTrail alone to satisfy the Region-restriction requirement
    D. Use prompt engineering only, with no retrieval or lineage tracking, since a smaller prompt reduces audit scope

27. **[Advanced]** (Select THREE.) An insurance company is building a
    Bedrock-based underwriting assistant that must (1) process both
    scanned paper applications (images) and typed notes (text) in the same
    conversation, (2) demonstrate to regulators that its recommendations
    don't differ significantly by applicant race, and (3) supply auditors
    with automatically compiled evidence that the bias check was actually
    performed. Which three actions together satisfy all three
    requirements?
    A. Select a foundation model that supports multi-modal (text + image) input, so scanned applications and typed notes can be processed in the same request
    B. Run Amazon SageMaker Clarify post-training bias metrics on the assistant's underwriting recommendations, broken out by race, to produce the required fairness evidence
    C. Use AWS Audit Manager to automatically assemble that Clarify evidence, alongside CloudTrail logs, into an audit-ready compliance report for regulators
    D. Raise the temperature parameter, since more randomness reduces the appearance of racial bias in outputs
    E. Rely on Amazon Polly to read underwriting decisions aloud to applicants instead of running any bias check

28. **[Advanced]** A credit union's classical SageMaker model approves or
    denies personal loan applications. Its board now wants to layer in (1)
    a check that the model's false-positive denial rate doesn't differ
    significantly across age groups, (2) a decision to route any
    prediction below a confidence threshold to a human underwriter rather
    than auto-denying it, and (3) a written NIST AI RMF-aligned governance
    record mapping both controls to the Measure and Govern functions ahead
    of a regulatory exam. Which combination of actions covers all three
    requirements?
    A. Skip the subgroup breakdown, since the model's overall accuracy is high; keep auto-denial for every prediction; and treat the NIST AI RMF as an optional reference with no documentation required
    B. Break the confusion matrix out by age group and run SageMaker Clarify post-training bias metrics for the false-positive-rate gap; threshold the model's predicted-probability output to route low-confidence cases to a human underwriter; and map both controls into a NIST AI RMF-aligned governance document covering the Measure and Govern functions
    C. Replace the classical model with a foundation model, since foundation models never need a bias review or human oversight
    D. Raise the overall classification threshold uniformly across all applicants, and skip both the bias breakdown and any written governance mapping, since a stricter threshold alone satisfies regulators

29. **[Advanced]** A media company operating in the EU wants its
    Bedrock-based content-moderation assistant to (1) guarantee
    consistent, low-latency throughput during traffic spikes, (2) block
    generated replies from ever including specific banned slurs or
    competitor names via configurable rules, and (3) keep all inference
    traffic and underlying data within EU AWS Regions to satisfy a
    data-sovereignty requirement. Which combination of choices satisfies
    all three requirements?
    A. On-demand pricing with default public endpoints and no residency controls, since Bedrock inference is inherently Region-agnostic
    B. Provisioned Throughput in an EU Region for guaranteed, low-latency capacity; Guardrails for Amazon Bedrock configured with denied topics/word filters for the banned terms; and an interface VPC endpoint (PrivateLink) restricted to the EU Region, with cross-Region replication disabled, to keep traffic and data in-Region
    C. Fine-tuning the model on the banned-term list, and relying on Amazon Comprehend alone for both the throughput guarantee and residency enforcement
    D. A NAT gateway in a public subnet, since NAT gateways alone satisfy both the throughput and data-sovereignty requirements

30. **[Advanced]** A hospital network is pairing an existing classical
    SageMaker triage-urgency model (trained on structured historical
    patient data) with a new Bedrock-based assistant that explains each
    urgency score to nurses in plain language, grounded in the hospital's
    current clinical guidelines. Before launch, the review board requires:
    (1) proof of exactly which dataset version and processing job produced
    the deployed classical model, (2) that the guideline text be retrieved
    at query time rather than baked into the assistant's weights, (3)
    evidence that the classical model's urgency scores don't differ
    significantly by patient demographic group, and (4) that all patient
    data stay encrypted with a customer-managed key and never traverse the
    public internet. Which combination of choices satisfies all four
    requirements?
    A. SageMaker ML Lineage Tracking for the model's provenance graph; Retrieval Augmented Generation (RAG) via Bedrock Knowledge Bases to ground explanations in the current guidelines instead of fine-tuning on them; SageMaker Clarify post-training bias metrics broken out by demographic group; and a customer-managed KMS key plus an interface VPC endpoint (PrivateLink) for data in transit and at rest
    B. Skip lineage tracking since the model already passed a one-time accuracy check; fine-tune the assistant directly on the guideline text; skip the bias check since urgency scoring is "purely clinical"; and use default AWS-managed encryption over the public internet
    C. Rely on AWS Trusted Advisor alone for provenance, bias, grounding, and encryption, since it provides a single unified dashboard for all four concerns
    D. Replace the classical model with a foundation model to eliminate the need for lineage tracking, bias testing, and encryption entirely

---

## Answer key and explanations

1. **C — Use RAG via Amazon Bedrock Knowledge Bases, with a scoped execution role and a HIPAA BAA.** RAG (Domain 3) keeps PHI out of the model's weights entirely by retrieving it at query time instead of training on it, while an execution role scoped to only the needed S3 prefixes and an executed BAA via AWS Artifact (Domain 5) satisfy the compliance and revocable-access requirements. Fine-tuning (A) and continued pre-training (B) both bake the data into the weights, which is exactly what's prohibited; prompt engineering alone (D) can't ground answers in the clinical notes at all. *(Domains 3, 5)*
2. **B — Amazon SageMaker Clarify.** Clarify computes post-training bias metrics such as disparate impact directly on a model's predictions, layering a fairness check (Domain 4) onto the standard supervised-learning evaluation step from the ML lifecycle (Domain 1). Feature Store (A) only manages features, not fairness metrics; Comprehend (C) analyzes text sentiment, not tabular model predictions; Trusted Advisor (D) checks cost/performance/security posture, not model fairness. *(Domains 1, 4)*
3. **B — Provisioned Throughput plus an interface VPC endpoint for Bedrock Runtime.** Provisioned Throughput (Domain 2) guarantees consistent inference capacity, while an interface VPC endpoint backed by AWS PrivateLink (Domain 5) keeps that traffic off the public internet. A NAT gateway (A) still routes through the public internet; AWS Artifact (C) only provides compliance reports; AWS Config (D) tracks configuration compliance, not throughput or network path. *(Domains 2, 5)*
4. **B — The classical SageMaker model.** Structured/tabular data is exactly the shape classical supervised learning models (Domain 1) are built for, and their quality can be benchmarked directly with standard metrics like RMSE; RAG (Domain 3) is designed to ground generation in unstructured text, which isn't the bottleneck here. Option A overgeneralizes RAG's strengths; C ignores that this is a well-suited classical ML problem; D is false since evaluation remains essential regardless of approach. *(Domains 1, 3)*
5. **A and B — Guardrails for Amazon Bedrock, and Amazon SageMaker Model Cards.** Guardrails' denied topics/word filters (Domain 3) directly block the configured competitor names from appearing in generated output, while Model Cards (Domain 4) give reviewers the documented intended-use, limitations, and evaluation record needed for governance sign-off. Comprehend (C) translates text and doesn't block content; Trusted Advisor (D) and AWS Config (E) address cost and infrastructure configuration, not content filtering or model documentation. *(Domains 3, 4)*
6. **B — Negative prompting.** Explicitly instructing the model to avoid the competitor's trademarked name (Domain 2's prompt engineering) directly mitigates intellectual-property and legal risk (Domain 4). Chain-of-thought (A) targets reasoning quality, not content exclusion; zero-shot prompting (C) just means no examples are given, it doesn't exclude specific content; raising temperature (D) increases variability and would make unwanted mentions *more* likely, not less. *(Domains 2, 4)*
7. **A and B — Amazon SageMaker Clarify, and AWS Audit Manager.** Clarify (Domain 4) computes the post-training bias metrics the fairness check requires, while Audit Manager (Domain 5) automatically assembles evidence from sources like Config and CloudTrail into an audit-ready compliance report for the risk-framework reviewer. Polly (C) is text-to-speech, Trainium (D) accelerates training compute, and Forecast (E) predicts time-series values — none address bias detection or compliance evidence. *(Domains 4, 5)*
8. **A — SageMaker ML Lineage Tracking combined with in-country Region restriction and disabled cross-Region replication.** Lineage Tracking (Domain 1) supplies the dataset-to-model provenance graph auditors need, while restricting storage/processing to the required Region and disabling cross-Region replication (Domain 5) directly enforces data residency, including for backups. Macie (B) only discovers sensitive data content, Feature Store (C) manages curated features, and CloudTrail (D) logs API calls — none alone provide both provenance and residency guarantees. *(Domains 1, 5)*
9. **A — Select a multi-modal, large-context-window foundation model first, then ground it with RAG.** Modality and context-window are foundation model selection criteria (Domain 2) that must be satisfied before the model can even accept images or long ticket threads; RAG via Bedrock Knowledge Bases (Domain 3) then grounds its answers in current articles rather than stale pretrained knowledge. B, C, and D each skip a hard prerequisite (modality/context support, or grounding) that the scenario explicitly requires. *(Domains 2, 3)*
10. **A — Amazon OpenSearch Serverless with a customer-managed KMS key, accessed through an interface VPC endpoint.** OpenSearch Serverless as a vector store (Domain 3) supports customer-managed KMS encryption and PrivateLink-based interface VPC endpoints (Domain 5), satisfying both the encryption and network-isolation requirements simultaneously. Kendra with default encryption over the public internet (B) fails the network-isolation requirement; disabling encryption (C) and using an unencrypted public bucket (D) both directly violate the encryption requirement for PII. *(Domains 3, 5)*
11. **A — Classical supervised learning for the fixed-category task, few-shot prompting for the open-ended task.** With 200 labeled examples mapping to fixed categories, a classical supervised learning classifier (Domain 1) is the well-matched, data-appropriate choice; for the open-ended drafting task with no labeled "ideal reply" examples, few-shot prompting a foundation model (Domain 2) supplies guidance without needing a labeled dataset. B, C, and D each mismatch the technique to the data shape or task type described. *(Domains 1, 2)*
12. **B — The data-residency legal requirement takes precedence.** Environmental sustainability is one of the responsible-AI considerations (Domain 4), but data-residency and sovereignty obligations (Domain 5) are hard legal constraints that any sustainability-driven Region choice must still satisfy — you cannot route training to a "greener" Region if doing so violates a residency requirement. A inverts that priority; C ignores a legal obligation entirely; D falsely claims the two considerations never conflict, when this scenario is exactly a case where they do. *(Domains 4, 5)*
13. **B — Use RAG grounded in the current policy, and check the historical dataset with Clarify before ever fine-tuning on it.** Fine-tuning (Domain 3) directly encodes whatever patterns exist in its training data into the model's weights, so training on decisions that reflect historical bias (Domain 4) would perpetuate that inequity; RAG instead retrieves the current, vetted policy text at query time without altering the model's weights at all. A ignores data quality entirely; raising temperature (C) only adds randomness and does nothing to correct a systematic skew; continued pre-training (D) still trains on the biased data and would bake in the same historical bias as fine-tuning. *(Domains 3, 4)*
14. **A and B — SageMaker Clarify post-training bias metrics, and a SageMaker Model Card.** Clarify's post-training metrics such as disparate impact (Domain 4) give the quantitative evidence of whether the fine-tuned model's outcomes differ by gender, while a Model Card (Domain 4) documents the fine-tuning data source, intended use, and known limitations that governance sign-off requires — both applied to the fine-tuned model produced by the Domain 3 customization decision. Raising temperature (C) doesn't affect fairness; switching to Provisioned Throughput (D) is a pricing/capacity choice, not a bias review; Comprehend (E) translates text and doesn't assess fairness. *(Domains 3, 4)*
15. **A — Rebalance the few-shot examples.** Few-shot prompting (Domain 3) steers the model using the examples placed directly in the prompt, so a skew in *which* examples are chosen introduces the same kind of fairness bias (Domain 4) that skewed training data would — the fix is diversifying those examples, not retraining. B misdiagnoses this as a training-data problem when no fine-tuning occurred; C confuses bias with randomness; D is false — RAG grounds responses in retrieved documents and has no mechanism that would automatically correct a biased set of prompt examples. *(Domains 3, 4)*
16. **A — Tune max tokens/temperature for the desired output, and bound request volume with throttling/Service Quotas.** Max tokens and temperature (Domain 2) are the inference parameters that control response length and creativity, while request throttling, Service Quotas, and API Gateway usage plans (Domain 5) cap how many requests can be made, bounding worst-case inference cost regardless of per-call settings — the two concerns are independent and both need to be addressed. B sacrifices the stated creative-output requirement; C is incomplete, since IAM governs *who* can call the endpoint, not *how much* they can call it; D is false — Provisioned Throughput changes the pricing model but doesn't remove the value of tuning parameters or bounding abusive request volume. See [Domain 3 § Cost governance](domain-3-applications-of-foundation-models.md#cost-governance-bounding-per-request-cost-with-max-tokens-and-provisioned-throughput) and [Domain 5 § Cost governance](domain-5-security-compliance-governance.md#cost-governance-bounding-total-spend-with-service-quotas-and-api-gateway-usage-plans) for the full write-up. *(Domains 2, 5)*
17. **A and B — Right-size max tokens, and bound request volume with Service Quotas/API Gateway usage plans.** Capping max tokens (Domain 2) to what the task actually needs avoids paying for unnecessary output tokens on every call, while Service Quotas and API Gateway usage plans (Domain 5) bound total request volume so a traffic spike can't translate into an unpredictable bill — together they bound both the per-call and aggregate cost. Maximizing temperature (C) targets creativity, not quality, and does nothing for cost; disabling logging (D) has no meaningful effect on per-token billing and would remove auditability; over-provisioning Provisioned Throughput for worst-case traffic (E) is itself an unpredictable, high fixed cost and ignores that parameter tuning still reduces per-call spend. See [Domain 3 § Cost governance](domain-3-applications-of-foundation-models.md#cost-governance-bounding-per-request-cost-with-max-tokens-and-provisioned-throughput) and [Domain 5 § Cost governance](domain-5-security-compliance-governance.md#cost-governance-bounding-total-spend-with-service-quotas-and-api-gateway-usage-plans) for the full write-up. *(Domains 2, 5)*
18. **A — Lower max tokens, then confirm with Trusted Advisor.** Max tokens (Domain 2) is the inference parameter that directly caps how many tokens a response — and therefore its output-token cost — can contain; AWS Trusted Advisor (Domain 5) then gives the account-level cost-optimization view needed to confirm the change actually reduced spend. Temperature (B) controls randomness, not length; a larger top-k (C) widens the candidate pool but doesn't shorten responses; Model Cards (D) document a model, they don't alter its runtime behavior. See [Domain 3 § Cost governance](domain-3-applications-of-foundation-models.md#cost-governance-bounding-per-request-cost-with-max-tokens-and-provisioned-throughput) and [Domain 5 § Cost governance](domain-5-security-compliance-governance.md#cost-governance-bounding-total-spend-with-service-quotas-and-api-gateway-usage-plans) for the full write-up. *(Domains 2, 5)*
19. **B — Break the confusion matrix out per subgroup, then use Clarify plus a human fairness review.** Per-subgroup confusion-matrix metrics such as false positive rate and recall (Domain 1 evaluation) can diverge sharply between groups even when the aggregate accuracy looks fine, since accuracy averages over the whole population; SageMaker Clarify's pre- and post-training bias metrics, combined with a human-led review to choose a mitigation like reweighting the data or a per-group threshold adjustment (Domain 4), is the direct next step once that gap is found. A wrongly trusts an aggregate metric that can hide subgroup disparity by construction; C is false — a uniformly higher threshold shifts the whole population's outcomes but doesn't equalize the *gap* between groups; D confuses a training hyperparameter with a fairness fix. *(Domains 1, 4)*
20. **C — The test set shared the training data's non-representativeness; audit for representativeness earlier.** A held-out test split drawn from the same skewed collection pool (Domain 1's data collection/preparation stage of the ML lifecycle) will still look strong even when the underlying data underrepresents part of the real-world population, because the split doesn't fix a sampling bias baked in before the split ever happened; catching this requires auditing training data for representativeness across the population the model will actually serve, which is a fairness consideration (Domain 4), not something a stronger test score alone would reveal. A misdiagnoses this as a split-ratio problem; B ignores the data issue entirely; D assumes a different model family would fix a data-collection gap on its own, which it would not. *(Domains 1, 4)*
21. **B — The interpretable model (or ensemble plus explainability tooling) better satisfies the legal requirement.** Classical model selection routinely trades interpretability for a small amount of raw accuracy (Domain 1), and that tradeoff is exactly what's in tension with the responsible-AI requirement for transparency and explainability (Domain 4) when denied applicants must receive an understandable reason; resolving it in favor of interpretability (directly, or via a feature-attribution tool like SageMaker Clarify on top of the ensemble) is what actually satisfies the regulation. A ignores a binding legal constraint; C simply doesn't meet the stated requirement; D swaps in a model family that doesn't even produce the classification decision needed, let alone an explanation for it. *(Domains 1, 4)*
22. **A — Threshold the model's confidence output to route low-confidence cases to a human.** A classical supervised model's predicted-probability output (Domain 1) is a natural signal to threshold on, routing anything below the cutoff to a human reviewer instead of auto-actioning it — this is precisely how the human-in-the-loop oversight and controllability principle (Domain 4) is implemented for a high-stakes, no-autonomous-final-decision requirement. B is false — classical classifiers routinely expose a predicted probability that can serve as a confidence score; C rejects the explicit governance requirement in the scenario; D confuses temperature, a generative-model sampling parameter, with a classical model's confidence output. *(Domains 1, 4)*
23. **A — Prototype with prompt engineering against a pretrained foundation model; reserve the classical training pipeline for the numeric task.** A foundation model's pretrained weights (Domain 2) let a team compare several summarization approaches through prompt engineering alone, with no data-collection or training cycle required, while the numeric credit-score-adjustment task still needs the classical SageMaker ML lifecycle's data-prep, training, tuning, and evaluation stages (Domain 1) to produce a dedicated, benchmarkable model. B wastes the exploratory phase by forcing a full training pipeline where none is needed; C misapplies RAG, a grounding technique, to a numeric regression problem; D wrongly treats continued pre-training — itself a multi-stage training job — as a fast prototyping shortcut for either task. *(Domains 1, 2)*
24. **B — Benchmark the foundation model with generation-appropriate metrics (e.g., ROUGE/BERTScore) plus human evaluation, while keeping the lifecycle's held-out-evaluation principle.** A summary has no single correct numeric value, so the classical regression metrics RMSE and R² (Domain 1) don't transfer directly; instead, FM benchmarking (Domain 2) substitutes automated text-similarity metrics and human judgment of coherence and faithfulness, while still honoring the ML lifecycle's requirement to evaluate on held-out data before choosing a model for production. A misapplies a numeric-error metric to text it can't meaningfully score; C skips evaluation entirely, ignoring that a provider's general-purpose validation doesn't guarantee fitness for this specific summarization use case; D conflates training loss with the separate, necessary pre-deployment evaluation step. *(Domains 1, 2)*
25. **A and B — classical model with an auditable metric for the credit score, foundation model for the summarizer.** A regulator-auditable, year-over-year metric like AUC computed on a held-out test set (Domain 1's evaluation stage) is exactly the rigor a classical supervised learning model provides for the credit-risk score, while fluent, varied natural-language summarization (Domain 2) plays to a foundation model's core strength rather than a classical classifier's. C incorrectly claims AUC — a classification metric requiring ground-truth labels and predicted probabilities — can be computed on free-form generated text; D wrongly claims prompting removes the need for held-out evaluation of a regulated numeric score; E incorrectly claims natural-language generation always requires labeled input-output pairs, ignoring prompting and few-shot techniques that need none. *(Domains 1, 2)*
26. **B — RAG plus ML Lineage Tracking plus Region-restricted storage/processing.** RAG via Bedrock Knowledge Bases (Domain 3) keeps the proprietary sequences out of the model's weights by retrieving them at query time instead of training on them; SageMaker ML Lineage Tracking (Domain 1) supplies the dataset-version/processing-job provenance graph auditors need; and restricting all storage and processing to the required Region while disabling cross-Region replication (Domain 5) enforces the residency requirement even for backups. A and C both bake the sequences directly into the weights via fine-tuning or continued pre-training, which is exactly what's prohibited, and neither addresses lineage or residency; D provides no grounding, no provenance record, and no residency control at all. This is the same three-way tension the [end-to-end case study](case-study-ai-system-lifecycle.md) walks through when a system's lifecycle, customization, and security decisions all constrain each other at once. *(Domains 1, 3, 5)*
27. **A, B and C — a multi-modal foundation model, Clarify bias metrics, and Audit Manager evidence.** Selecting a foundation model with multi-modal (text + image) support (Domain 2) is a prerequisite just to process scanned applications alongside typed notes; SageMaker Clarify's post-training bias metrics broken out by race (Domain 4) produce the fairness evidence regulators require; and AWS Audit Manager (Domain 5) automatically assembles that evidence, plus supporting logs, into an audit-ready compliance report. Raising temperature (D) only adds output randomness and does nothing to measure or reduce racial bias; using Polly to read decisions aloud instead of running a bias check (E) skips the requirement entirely rather than satisfying it. *(Domains 2, 4, 5)*
28. **B — subgroup bias metrics, confidence-based human routing, and a NIST AI RMF-mapped governance record.** Breaking the confusion matrix out by age group and running SageMaker Clarify's post-training bias metrics (Domain 1 evaluation extended with a Domain 4 fairness lens) surfaces a false-positive-rate gap that overall accuracy would hide; thresholding the classical model's predicted-probability output to route low-confidence cases to a human underwriter (Domain 4's human-in-the-loop principle, applied to the Domain 1 model output) keeps a person accountable for borderline denials; and mapping both controls into a NIST AI RMF-aligned document covering the Measure and Govern functions (Domain 5) is what an examiner actually expects to see. A and D both skip the bias review and the written governance mapping the board explicitly asked for; C swaps in a different model family without addressing any of the three stated requirements. *(Domains 1, 4, 5)*
29. **B — Provisioned Throughput in-Region, Guardrails for the banned terms, and an in-Region PrivateLink endpoint.** Provisioned Throughput deployed in an EU Region (Domain 2) is what guarantees consistent, low-latency capacity; Guardrails for Amazon Bedrock with denied topics/word filters (Domain 3) blocks the banned slurs and competitor names from ever appearing in generated replies; and an interface VPC endpoint via PrivateLink restricted to the EU Region, with cross-Region replication disabled (Domain 5), keeps both the traffic path and the underlying data inside the EU. A ignores the sovereignty requirement entirely; C's reliance on Comprehend alone addresses neither throughput guarantees nor residency; D's NAT gateway still routes over the public internet and does nothing for guaranteed throughput. *(Domains 2, 3, 5)*
30. **A — Lineage Tracking, RAG grounding, Clarify bias metrics, and customer-managed KMS plus PrivateLink, together.** SageMaker ML Lineage Tracking (Domain 1) gives the review board the dataset-and-processing-job provenance the classical triage model needs; grounding the assistant's plain-language explanations in the current clinical guidelines via RAG (Domain 3) instead of fine-tuning keeps that guideline text out of the model's weights, so it can be updated without retraining; SageMaker Clarify post-training bias metrics broken out by demographic group (Domain 4) supply the fairness evidence for the urgency scores; and a customer-managed KMS key combined with an interface VPC endpoint (Domain 5) satisfies the encryption-at-rest and no-public-internet requirements for patient data. B skips every one of the four controls the board asked for; C substitutes a single dashboard tool that does not itself perform lineage tracking, bias testing, RAG grounding, or encryption; D discards the classical model that is actually in scope without addressing any of the four stated requirements. This question mirrors the [end-to-end case study](case-study-ai-system-lifecycle.md), where one system's lifecycle, customization, fairness, and security decisions all have to hold together simultaneously. *(Domains 1, 3, 4, 5)*

---

[← README](../README.md) · [Cross-domain concept map →](cross-domain-concept-map.md)
