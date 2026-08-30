# Cross-Domain Scenario Questions (AIF-C01)

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

This document collects 18 scenario questions that each require knowledge
from **two or more domains** to answer correctly — you cannot eliminate
every wrong option using only one domain's vocabulary. See the
[cross-domain concept map](cross-domain-concept-map.md) for the underlying
concept-to-concept connections these questions draw on, and each domain
guide linked above for the full depth on any single concept referenced
here.

Each question is tagged with a difficulty level
(**[Beginner]**/**[Intermediate]**/**[Advanced]**) and each answer names
the two or more domains it draws on, e.g. `*(Domains 3, 5)*`.

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
16. **A — Tune max tokens/temperature for the desired output, and bound request volume with throttling/Service Quotas.** Max tokens and temperature (Domain 2) are the inference parameters that control response length and creativity, while request throttling, Service Quotas, and API Gateway usage plans (Domain 5) cap how many requests can be made, bounding worst-case inference cost regardless of per-call settings — the two concerns are independent and both need to be addressed. B sacrifices the stated creative-output requirement; C is incomplete, since IAM governs *who* can call the endpoint, not *how much* they can call it; D is false — Provisioned Throughput changes the pricing model but doesn't remove the value of tuning parameters or bounding abusive request volume. *(Domains 2, 5)*
17. **A and B — Right-size max tokens, and bound request volume with Service Quotas/API Gateway usage plans.** Capping max tokens (Domain 2) to what the task actually needs avoids paying for unnecessary output tokens on every call, while Service Quotas and API Gateway usage plans (Domain 5) bound total request volume so a traffic spike can't translate into an unpredictable bill — together they bound both the per-call and aggregate cost. Maximizing temperature (C) targets creativity, not quality, and does nothing for cost; disabling logging (D) has no meaningful effect on per-token billing and would remove auditability; over-provisioning Provisioned Throughput for worst-case traffic (E) is itself an unpredictable, high fixed cost and ignores that parameter tuning still reduces per-call spend. *(Domains 2, 5)*
18. **A — Lower max tokens, then confirm with Trusted Advisor.** Max tokens (Domain 2) is the inference parameter that directly caps how many tokens a response — and therefore its output-token cost — can contain; AWS Trusted Advisor (Domain 5) then gives the account-level cost-optimization view needed to confirm the change actually reduced spend. Temperature (B) controls randomness, not length; a larger top-k (C) widens the candidate pool but doesn't shorten responses; Model Cards (D) document a model, they don't alter its runtime behavior. *(Domains 2, 5)*

---

[← README](../README.md) · [Cross-domain concept map →](cross-domain-concept-map.md)
