# Full-Length Mock Exam: AWS Certified AI Practitioner (AIF-C01)

**Last verified:** 2026-09-11

The five domain guides ([Domain 1](domain-1-fundamentals-of-ai-and-ml.md),
[Domain 2](domain-2-fundamentals-of-generative-ai.md),
[Domain 3](domain-3-applications-of-foundation-models.md),
[Domain 4](domain-4-guidelines-for-responsible-ai.md),
[Domain 5](domain-5-security-compliance-governance.md)) each end with their
own 15–20 domain-siloed practice questions (~85 total). Those are the right
tool for learning one domain at a time, but the real AIF-C01 exam never
groups questions by domain, never tells you which domain a question belongs
to, and runs for a fixed 90-minute block. This page is the missing
rehearsal step: **one 65-question mock exam, mixed across all five domains
in the exam's own weight proportions, timed like the real thing, with a
full answer key at the end.**

See the [exam preparation strategy guide](exam-preparation-strategy.md) for
when to take this in your study plan (every 1-week, 2-week, and 4-week plan
schedules a full timed run of this exam before the final review day) and
for general time-management tactics. See the individual domain guides for
that concept explained in depth if you miss a question here.

## How to take this mock exam

1. **Block off 90 minutes** in one uninterrupted sitting — no notes, no
   searching, no pausing. That is the real per-attempt time limit, whether
   or not you use all of it.
2. **Answer all 65 questions in order**, top to bottom. Do not skip around
   looking for your strong domains — the real exam interleaves domains
   exactly like this document does, and part of what you are rehearsing is
   staying oriented as the subject changes every question or two.
3. **Write down your answer for every question** (a plain numbered list of
   letters is enough) before checking anything. If you are unsure, flag the
   number and make your best guess anyway — on the real exam there is no
   penalty for a wrong answer, so a blank is always worse than a guess.
4. **Questions marked "(Select TWO.)" or "(Select THREE.)" require every
   correct option** — partial credit is not given on the real exam, and
   this mock exam grades them the same way.
5. Only after finishing all 65, turn to the
   [answer key and explanations](#answer-key-and-explanations) below and
   score yourself.

### Domain weighting

This mock exam mirrors the real AIF-C01 domain weights as closely as a
65-question, whole-number split allows:

| # | Domain | Real exam weight | Questions in this mock exam |
|---|--------|:-----------------:|:----------------------------:|
| 1 | [Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md) | ~20% | 13 |
| 2 | [Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md) | ~24% | 16 |
| 3 | [Applications of Foundation Models](domain-3-applications-of-foundation-models.md) | ~28% | 18 |
| 4 | [Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md) | ~14% | 9 |
| 5 | [Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md) | ~14% | 9 |
| | **Total** | **100%** | **65** |

The questions below are **not labeled by domain** — exactly like the real
exam, so you cannot use the label to narrow down the answer. The
[answer key](#answer-key-and-explanations) tags each question's domain so
you can total up your score per domain afterward and see which domain(s)
need the most review, per the
["identify your two weakest domains" step](exam-preparation-strategy.md#5-study-plans)
in the study plans.

### Scoring

The real AIF-C01 exam reports a scaled score from 100–1000, with a passing
score of 700. The scaled conversion is nonlinear and AWS does not publish
the exact formula, but **≈54/65 correct (about 83%)** is the commonly used
rough proxy for a passing score — treat it as an estimate, not a guarantee,
in either direction. Use your per-domain tally to decide where to spend
your remaining study time, not just the overall score.

---

## Mock exam questions

1. A team is deploying a foundation model behind a customer-facing chat
   widget that must respond in well under a second and only ever needs to
   process text, never images or audio. Which factor should the team
   weigh FIRST when narrowing down candidate foundation models?
   A. The number of parameters in the largest available model
   B. Whether the model supports the required modality (text) at all
   C. The vendor's marketing claims about benchmark leaderboard rank
   D. Whether the model was released in the last three months

2. Which statement correctly distinguishes a token from an embedding?
   A. A token and an embedding are two names for the same numeric vector
   B. A token is a chunk of text the model processes; an embedding is a
      numeric vector capturing that chunk's meaning
   C. An embedding is always a whole sentence; a token is always a
      paragraph
   D. Tokens are used only during training, and embeddings are used only
      during inference

3. Which of the following is the best one-sentence description of the
   relationship between artificial intelligence, machine learning, and
   deep learning?
   A. They are three unrelated fields that happen to share vocabulary
   B. Deep learning contains machine learning, which contains AI
   C. AI is the broadest field, machine learning is a subset of AI, and
      deep learning is a subset of machine learning
   D. Machine learning and deep learning are interchangeable terms for
      the same set of techniques

4. A company has built a working proof-of-concept chatbot using prompt
   engineering alone against a general-purpose foundation model, but
   support staff report the bot regularly invents plausible-sounding
   policy details that do not exist in the company's actual documentation.
   Which approach directly addresses this without retraining the model?
   A. Increase the model's temperature setting to make responses more
      creative
   B. Switch to a larger foundation model with more parameters
   C. Connect the chatbot to the company's own documents with
      Retrieval-Augmented Generation (RAG)
   D. Remove the system prompt entirely to simplify the request

5. A company's model repeatedly denies loan applications from a specific
   ZIP code at a much higher rate than its overall denial rate, even
   though ZIP code is not an explicit input feature. Which responsible-AI
   dimension is most directly implicated?
   A. Latency
   B. Fairness
   C. Cost optimization
   D. Model file versioning

6. A data science team needs an AWS service that can call other AWS
   services (such as a Lambda function) on the team's behalf to process a
   nightly batch of encrypted objects in Amazon S3, without the team
   embedding any long-lived access keys in application code. What should
   the team attach to the compute resource performing this work?
   A. A hardcoded IAM access key and secret pair
   B. An IAM role with only the permissions the task requires
   C. The AWS account's root user credentials
   D. A shared password stored in application configuration

7. Which combination correctly matches an AWS generative AI service to
   its primary intended use?
   A. Amazon Q Developer — a no-code sandbox for casually prototyping app
      ideas from natural-language prompts
   B. PartyRock — a coding companion embedded in an IDE that generates
      and explains code
   C. Amazon Q Business — a managed, pre-built assistant that answers
      questions grounded in a company's own enterprise data with minimal
      setup
   D. Amazon Bedrock — a fully no-code website builder for non-technical
      users

8. A retailer with no in-house data science team wants to forecast next
   quarter's inventory needs for thousands of SKUs using historical sales
   data, without writing or training a custom model. Which AWS service is
   the best fit?
   A. Amazon SageMaker
   B. Amazon Forecast
   C. Amazon Rekognition
   D. Amazon Comprehend

9. Which two Amazon Bedrock capabilities should a team combine to build an
   assistant that (1) answers customer questions using the company's own
   product manuals and (2) automatically calls an internal order-status
   API when a customer asks about a specific order? (Select TWO.)
   A. Guardrails
   B. Knowledge Bases
   C. Agents
   D. Model Evaluation
   E. Provisioned Throughput

10. Which of the following best describes "hallucination" in the context
    of generative AI, as distinct from ordinary inaccuracy?
    A. The model refuses to answer any question it considers sensitive
    B. The model confidently generates fabricated information that is
       not grounded in its training data or provided context, presenting
       it as fact
    C. The model runs out of available context window space mid-response
    D. The model consistently produces the exact same output for the
       exact same prompt

11. A company wants its Bedrock-based assistant to automatically detect
    and block user prompts and model responses that contain hate speech
    or requests for personally identifiable information, without writing
    custom filtering logic. Which Bedrock feature is purpose-built for
    this?
    A. Bedrock Agents
    B. Bedrock Knowledge Bases
    C. Bedrock Guardrails
    D. Bedrock Model Evaluation

12. A hospital deploys a diagnostic-support model and, months later, a
    regulator asks the hospital to explain in specific business terms why
    the model recommended against a certain treatment for a particular
    patient. Which responsible-AI dimension does this request test?
    A. Scalability
    B. Explainability
    C. Throughput
    D. Elasticity

13. Which statement correctly distinguishes "encryption in transit" from
    "encryption at rest"?
    A. Encryption in transit protects data stored on a disk; encryption
       at rest protects data moving over a network
    B. Encryption in transit protects data moving over a network (for
       example, via TLS); encryption at rest protects stored data (for
       example, an S3 object encrypted with AWS KMS)
    C. They are two different names for the identical AWS KMS feature
    D. Encryption in transit only applies to on-premises data centers,
       never to the cloud

14. A model achieves 97% accuracy on its training set but only 58%
    accuracy when evaluated on a held-out test set. What does this
    pattern most strongly suggest?
    A. The model is underfitting the training data
    B. The model is overfitting the training data
    C. The training and test sets were identical
    D. The model's hyperparameters cannot be tuned further

15. A company wants a chatbot to reason step-by-step through a
    multi-part math word problem and show its intermediate reasoning
    before giving a final answer, without any additional training data or
    retraining. Which prompt engineering technique directly supports this?
    A. Zero-shot prompting with no examples or instructions
    B. Chain-of-thought prompting
    C. Fine-tuning on a labeled reasoning dataset
    D. Reducing the model's context window

16. A company must keep all traffic between its VPC and Amazon Bedrock off
    the public internet entirely, for a workload handling regulated
    customer data. Which AWS networking feature satisfies this
    requirement?
    A. A NAT gateway
    B. A site-to-site VPN connection
    C. An interface VPC endpoint powered by AWS PrivateLink
    D. A public internet gateway with a security group restriction

17. Which of the following is an example of a hyperparameter rather than a
    parameter learned by the model itself?
    A. The final weight values of a trained neural network
    B. The batch size used during training
    C. The bias term learned by a linear regression model
    D. The coefficients learned by a regression model

18. A company wants to quickly prototype and share a small generative AI
    app idea with non-technical stakeholders, with no code and minimal
    setup, purely to validate a concept before any serious engineering
    investment. Which AWS offering is purpose-built for this?
    A. Amazon SageMaker JumpStart
    B. PartyRock
    C. AWS Trainium
    D. Amazon Bedrock Agents

19. A company already has Retrieval-Augmented Generation in place for
    up-to-date factual answers, but now also needs its assistant to
    consistently respond in a very specific, tightly regulated legal
    phrasing style across thousands of examples of correct phrasing it
    already has on file. Which customization approach best fits this
    additional requirement?
    A. Increasing the temperature parameter
    B. Fine-tuning the model on the company's labeled phrasing examples
    C. Removing RAG entirely and relying on the base model alone
    D. Reducing the model's maximum token limit

20. A company's internal audit function needs to demonstrate, months from
    now, that a specific IAM principal invoked the Bedrock InvokeModel API
    on a particular date and time. Which AWS service is purpose-built to
    answer that question?
    A. Amazon CloudWatch
    B. AWS CloudTrail
    C. AWS Config
    D. Amazon GuardDuty

21. A healthcare company plans to process protected health information
    (PHI) using AWS AI services. Which combination of steps is required
    before doing so?
    A. Enable AWS Shield and stop there
    B. Execute a Business Associate Addendum (BAA) with AWS via AWS
     Artifact, and use only HIPAA-eligible services configured accordingly
    C. Simply encrypt the data in transit; no other agreement is needed
    D. Use only services released in the current calendar year

22. A prompt engineer wants the model to avoid a specific unwanted
    behavior — for example, instructing it not to include any
    disclaimers or apologies in its response. Which technique is this?
    A. Few-shot prompting
    B. Negative prompting
    C. Retrieval-Augmented Generation
    D. Continued pre-training

23. A data scientist is choosing a learning approach for an application
    that must group website visitors into behavioral segments, where no
    predefined segment labels exist anywhere in the collected data. Which
    type of learning fits?
    A. Supervised learning
    B. Reinforcement learning
    C. Unsupervised learning
    D. Semi-supervised learning with a labeled validation set only

24. A team is deciding between Amazon Kendra and building a custom vector
    database on Amazon OpenSearch Service for a new internal search tool.
    The requirement is "let employees search our internal wiki using
    natural-language questions," with no mention of the team wanting to
    manage its own embedding model or similarity index. Which is the
    better fit?
    A. Amazon Kendra, since it provides managed natural-language search
       without requiring the team to manage embeddings
    B. A custom OpenSearch vector database, since it is always cheaper
    C. AWS Trainium, since it is designed for search workloads
    D. Amazon Polly, since it converts search queries to speech

25. Which of the following best explains why a company might choose
    Amazon Q Business over building a custom Bedrock-based application
    from scratch for an internal enterprise search assistant?
    A. Amazon Q Business requires writing and hosting custom RAG
       pipeline code
    B. Amazon Q Business is a managed, pre-built assistant that can be
       connected to enterprise data sources with comparatively little
       custom development
    C. Amazon Q Business cannot be connected to any company data at all
    D. Amazon Q Business only works with image and video inputs

26. A team is building a Bedrock-based application and needs to compare
    two candidate foundation models on a specific, subjective quality
    dimension — persuasiveness of generated marketing copy — using human
    judgment rather than a fixed benchmark score. Which Bedrock capability
    fits this need?
    A. Bedrock Guardrails
    B. Bedrock Model Evaluation using a human-based evaluation job
    C. Bedrock Agents
    D. Bedrock Provisioned Throughput

27. A company documents its own custom fraud-detection model's intended
    use, training data characteristics, and known limitations for internal
    governance review. Which artifact are they producing?
    A. An AWS AI Service Card
    B. A SageMaker Model Card
    C. An AWS Config rule
    D. A Bedrock Guardrail

28. A security team needs to continuously discover and classify sensitive
    data, such as personally identifiable information, stored in Amazon S3
    buckets used by an AI training pipeline. Which AWS service is
    purpose-built for this?
    A. Amazon Macie
    B. Amazon CloudWatch
    C. AWS Config
    D. AWS Audit Manager

29. A confusion matrix for a binary classifier shows TP = 90, FP = 10,
    FN = 30, TN = 870. What is the model's precision (rounded)?
    A. 75%
    B. 90%
    C. 97%
    D. 25%

30. Which inference parameter most directly controls how deterministic or
    creative a foundation model's generated text is, with lower values
    producing more predictable, focused output?
    A. Maximum token limit
    B. Temperature
    C. Context window size
    D. Number of model parameters

31. A company wants its Bedrock application to automatically scale down
    to zero cost during idle periods but still be able to absorb sudden,
    unpredictable traffic spikes without pre-purchasing fixed capacity.
    Which Bedrock throughput option fits best?
    A. Provisioned Throughput
    B. On-demand throughput
    C. Bedrock Agents
    D. Continued pre-training

32. Which of the following AWS managed services is purpose-built to
    extract not just plain text but also structured key-value pairs and
    tables from scanned forms, preserving their layout?
    A. Amazon Comprehend
    B. Amazon Textract
    C. Amazon Transcribe
    D. Amazon Rekognition

33. A team is evaluating a customer-support foundation model application
    and wants a metric tied directly to real business outcomes, such as
    the reduction in average ticket resolution time after the assistant
    was deployed. Which evaluation category does this fall under?
    A. Automatic benchmark metrics
    B. Human evaluation of subjective quality
    C. Business metrics
    D. Model parameter counts

34. A company wants to reduce legal exposure from generated content that
    might infringe third-party copyrights. Which of the following is the
    most directly relevant mitigation to look for?
    A. Bedrock Guardrails content filtering alone
    B. IP indemnification terms offered for certain Bedrock models
    C. Increasing the model's temperature
    D. Reducing the model's context window

35. Which AWS service continuously records the configuration state of
    resources such as S3 buckets and evaluates them against rules (for
    example, "encryption must be enabled") to flag drift over time?
    A. AWS CloudTrail
    B. AWS Config
    C. AWS Audit Manager
    D. Amazon GuardDuty

36. A company needs a single, managed API to access multiple foundation
    models from different providers, without managing the underlying
    infrastructure itself. Which AWS service is designed for exactly
    this?
    A. Amazon Bedrock
    B. AWS Trainium
    C. Amazon SageMaker Ground Truth
    D. Amazon Kendra

37. A company already uses prompt engineering and RAG for its assistant,
    but now wants the assistant to absorb a large volume of unlabeled,
    domain-specific internal documents so the base model itself better
    understands the company's terminology, without needing labeled
    input/output pairs. Which customization technique fits this specific
    requirement?
    A. Fine-tuning, since it always requires labeled pairs
    B. Continued pre-training, which uses unlabeled domain text to
       further train the base model
    C. Negative prompting
    D. Increasing the temperature parameter

38. A team observes that a regression model's predictions are consistently
    far off from actual values on both the training data and the test
    data. Which of the following best describes this pattern?
    A. Overfitting
    B. Underfitting
    C. Data leakage
    D. Perfect generalization

39. Which of the following correctly distinguishes "few-shot prompting"
    from "fine-tuning"?
    A. Few-shot prompting permanently updates the model's weights; fine-
       tuning does not
    B. Few-shot prompting provides examples within the prompt without
       changing the model itself; fine-tuning retrains the model's
       weights on labeled data
    C. They are two names for the identical underlying process
    D. Few-shot prompting can only be used with image models

40. A company building a Retrieval-Augmented Generation pipeline needs a
    store that can hold embeddings and perform fast similarity search
    across millions of document chunks, integrated with its existing
    relational database. Which option best fits?
    A. Amazon Polly
    B. Amazon Aurora with the pgvector extension
    C. AWS Trainium
    D. Amazon Comprehend

41. A company's model consistently produces starkly different loan
    approval rates for two demographic groups that have similar
    creditworthiness in the underlying data. Which SageMaker capability
    is purpose-built to measure this kind of bias, both before and after
    training?
    A. SageMaker Feature Store
    B. SageMaker Clarify
    C. SageMaker Data Wrangler
    D. SageMaker Neo

42. Under GDPR, which of the following is most accurately described as
    the regulation's core focus, at the conceptual level tested on the
    AIF-C01 exam?
    A. It is a US healthcare-specific law governing patient records
    B. It is an EU regulation focused on the protection of personal data
    C. It exclusively governs AWS's internal data center construction
    D. It only applies to organizations with no EU customers

43. A prompt engineer supplies the model with two or three worked
    examples of the desired input/output format directly inside the
    prompt, without any model retraining. Which prompting technique is
    this?
    A. Zero-shot prompting
    B. Few-shot prompting
    C. Continued pre-training
    D. Fine-tuning

44. A robotics team trains an agent to navigate a warehouse by giving it a
    numeric reward after each action it takes, with no fixed labeled
    dataset provided up front. Which type of learning is this?
    A. Supervised learning
    B. Unsupervised learning
    C. Reinforcement learning
    D. Batch learning

45. A team needs to reduce the cost of running inference for a
    high-volume production foundation model workload at scale, using
    AWS's purpose-built inference chips rather than general-purpose GPUs.
    Which AWS chip should they use?
    A. AWS Trainium
    B. AWS Inferentia
    C. AWS Graviton for training
    D. Amazon EC2 M5 instances exclusively

46. Which best describes the "adaptability" advantage commonly cited for
    generative AI models compared to traditional narrow ML models?
    A. Generative models can only ever perform the single task they were
       first trained for
    B. A single foundation model can be applied to many different tasks
       (summarization, drafting, classification) through prompting alone
    C. Generative models never require any prompt engineering
    D. Generative models are always cheaper to run than any traditional
       ML model

47. Which AWS managed service should a company use to build a text-based
    conversational bot that can also incorporate speech recognition, with
    no in-house ML expertise required?
    A. Amazon Comprehend
    B. Amazon Lex
    C. Amazon Translate
    D. Amazon Polly

48. A company wants to know, across a fixed benchmark dataset, how
    accurately a candidate foundation model answers factual questions
    compared to a competing model, using an objective, repeatable score
    rather than a human review panel. Which evaluation approach is this?
    A. Human evaluation
    B. Automatic (benchmark) evaluation metrics
    C. Business metrics
    D. Guardrails filtering

49. Which pairing correctly matches an AWS responsible-AI documentation
    artifact to who authors it?
    A. A SageMaker Model Card is authored by AWS about its own managed
       service, and an AI Service Card is authored by the customer about
       their own custom model
    B. A SageMaker Model Card is authored by the customer about their own
       model, and an AI Service Card is authored by AWS about its own
       managed AI service
    C. Both are always authored jointly by AWS and the customer
    D. Neither artifact is ever shared publicly

50. Which AWS service is purpose-built to assemble evidence from sources
    such as AWS CloudTrail logs and AWS Config data, mapping it to
    prebuilt or custom compliance frameworks (such as GDPR or HIPAA) to
    support an audit?
    A. AWS Audit Manager
    B. Amazon Macie
    C. Amazon GuardDuty
    D. Amazon CloudWatch

51. A company is evaluating foundation models for a use case that must
    process both scanned images and text in a single request. Which
    category of foundation model is required?
    A. A unimodal text-only model
    B. A multimodal model capable of processing more than one input type
    C. A model with the fewest possible parameters
    D. A model that only supports batch (offline) inference

52. Which of the following is the correct order of the customization
    spectrum for foundation models, from least to most resource-intensive
    and from least to most it changes the model's underlying weights?
    A. Fine-tuning → RAG → prompt engineering → continued pre-training
    B. Prompt engineering → RAG → fine-tuning → continued pre-training
    C. Continued pre-training → fine-tuning → RAG → prompt engineering
    D. RAG → continued pre-training → prompt engineering → fine-tuning

53. Which of the following is generally the LEAST effective standalone
    technique for reducing overfitting in a trained model?
    A. Adding L2 regularization
    B. Increasing model complexity further without adding data
    C. Collecting more diverse training data
    D. Using cross-validation with early stopping

54. A company is comparing the cost of fine-tuning a smaller, efficient
    foundation model against repeatedly running full pre-training
    experiments on ever-larger models, partly because of the energy
    consumption and environmental footprint of large-scale AI training.
    Which responsible-AI consideration does this concern reflect?
    A. Encryption at rest
    B. The environmental impact of AI/ML workloads
    C. Provisioned throughput capacity planning
    D. Data residency

55. A company needs its Bedrock-based application to reliably access the
    latest product catalog data on every query, without ever needing to
    retrain or fine-tune the underlying foundation model as the catalog
    changes. Which approach is the best fit?
    A. Fine-tuning refreshed nightly on the full catalog
    B. Retrieval-Augmented Generation against a knowledge base kept in
       sync with the live catalog
    C. Continued pre-training on historical catalog snapshots
    D. Increasing the model's temperature parameter

56. Which of the following best distinguishes "veracity and robustness"
    from "controllability" as responsible-AI dimensions?
    A. Veracity/robustness concerns whether outputs remain reliable and
       trustworthy under varied or adversarial conditions; controllability
       concerns whether a human can direct, limit, or halt the system's
       behavior
    B. They are interchangeable terms describing identical concerns
    C. Controllability only applies to unsupervised learning models
    D. Veracity/robustness only applies to structured tabular data models

57. A financial services company must be able to justify an individual
    credit-decision model's specific prediction to an affected customer
    on request, even though a more complex model would achieve marginally
    higher accuracy in aggregate. Which trade-off does this scenario
    illustrate?
    A. Favoring performance over interpretability whenever any regulation
       applies
    B. Favoring interpretability, even at some accuracy cost, when
       regulatory or legal accountability for individual decisions is
       required
    C. A trade-off between encryption at rest and encryption in transit
    D. A trade-off between Provisioned Throughput and on-demand
       throughput

58. Which AWS service should an e-commerce company with no ML expertise
    use to add real-time, individualized product recommendations to its
    website?
    A. Amazon SageMaker
    B. Amazon Personalize
    C. Amazon Rekognition
    D. Amazon Comprehend

59. A prompt is submitted to a foundation model with no examples and only
    a plain-language instruction, such as "Summarize this article in two
    sentences." Which prompting technique is this?
    A. Few-shot prompting
    B. Zero-shot prompting
    C. Fine-tuning
    D. Continued pre-training

60. A company wants Bedrock to consistently answer employee questions
    using the exact wording found in its internal HR policy PDFs, citing
    the source section, without retraining any model. Which Bedrock
    feature is the most direct fit?
    A. Bedrock Knowledge Bases
    B. Bedrock Agents
    C. Bedrock Guardrails
    D. Bedrock Provisioned Throughput

61. Which of the following statements about the bias–variance trade-off
    is correct?
    A. High bias is associated with overfitting, and high variance with
       underfitting
    B. High bias is associated with underfitting, and high variance with
       overfitting
    C. Bias and variance always move in the same direction
    D. Bias and variance have no relationship to model generalization
       error

62. Which two of the following are commonly cited disadvantages of
    generative AI models compared to traditional deterministic software?
    (Select TWO.)
    A. Hallucination (fabricating plausible but false information)
    B. Guaranteed determinism across identical prompts
    C. Nondeterminism (the same prompt can produce different outputs)
    D. Zero inference cost regardless of model size
    E. Perfect interpretability of every generated token

63. A company managing its own embeddings and similarity index for a
    RAG pipeline, and needing full control over the underlying index
    configuration, is deciding between Amazon Kendra and Amazon
    OpenSearch Service. Which service is the better fit for this specific
    "we manage our own embeddings and index" requirement?
    A. Amazon Kendra
    B. Amazon OpenSearch Service configured as a vector database
    C. Amazon Polly
    D. Amazon Translate

64. A company's Bedrock-based tool must never generate outputs containing
    a customer's raw credit card number, even if a user's prompt tries to
    coax the model into repeating one back. Which Bedrock feature should
    be configured to enforce this at runtime?
    A. Bedrock Knowledge Bases
    B. Bedrock Guardrails, configured with sensitive-information filters
    C. Bedrock Model Evaluation
    D. Bedrock Agents

65. Which sequence correctly reflects the standard large language model
    (LLM) lifecycle, from initial planning through ongoing operation?
    A. Deploy → Scope → Select → Adapt → Evaluate → Monitor
    B. Scope → Select → Adapt → Evaluate → Deploy → Monitor
    C. Evaluate → Scope → Deploy → Select → Adapt → Monitor
    D. Monitor → Evaluate → Adapt → Select → Scope → Deploy

---

## Answer key and explanations

1. **B — Domain 3.** Whether a candidate model even supports the required
   modality (text-only, sub-second latency) must be checked before
   comparing parameter counts, marketing claims, or release recency —
   a model that cannot process the required input type is disqualified
   regardless of how it scores on unrelated dimensions.

2. **B — Domain 2.** A token is a chunk of text (often a word piece) the
   model processes; an embedding is the numeric vector that captures that
   chunk's semantic meaning. A conflates the two into one concept; C
   reverses their granularity; D is not how either is actually used, since
   both appear at training and inference time.

3. **C — Domain 1.** AI is the broadest field, ML is a subset of AI, and
   deep learning is a subset of ML — the standard nesting relationship.
   A denies any relationship; B reverses the hierarchy; D wrongly treats
   ML and deep learning as identical, when deep learning is a specific
   subset of ML techniques.

4. **C — Domain 3.** Connecting the assistant to the company's actual
   documents via RAG grounds responses in real source material and
   directly reduces fabricated ("hallucinated") policy details, without
   any retraining. Raising temperature (A) would make fabrication worse,
   not better; a larger model (B) does not fix ungrounded generation on
   its own; removing the system prompt (D) does not address the root
   cause at all.

5. **B — Domain 4.** A statistically significant outcome disparity
   correlated with a proxy for a protected characteristic (ZIP code
   correlating with demographics) is a fairness concern, even though the
   feature itself was never explicitly used as a model input. Latency,
   cost, and file versioning (A, C, D) are unrelated operational concerns,
   not responsible-AI dimensions.

6. **B — Domain 5.** Attaching an IAM role scoped to least privilege lets
   the compute resource assume temporary, auditable permissions without
   any long-lived credentials in code. Hardcoded keys (A) and root
   credentials (C) violate least privilege and security best practice; a
   shared password (D) is not how AWS service-to-service authorization
   works at all.

7. **C — Domain 2.** Amazon Q Business is the managed, pre-built assistant
   designed to answer questions grounded in a company's enterprise data
   with comparatively little setup. A and B swap Amazon Q Developer (a
   coding companion) and PartyRock (a no-code prototyping sandbox); D
   mischaracterizes Bedrock, which is a managed API for foundation models,
   not a website builder.

8. **B — Domain 1.** Amazon Forecast is the purpose-built, managed
   time-series forecasting service requiring no custom model development,
   directly matching "forecast inventory needs...without writing or
   training a custom model." SageMaker (A) would require building a
   custom model; Rekognition (C) analyzes images/video; Comprehend (D)
   analyzes text, neither of which fits a demand-forecasting use case.

9. **B and C — Domain 3.** Knowledge Bases grounds answers in the
   company's product manuals (retrieval over documents), and Agents is
   the Bedrock capability purpose-built to take actions such as calling
   an internal API on the user's behalf. Guardrails (A) filters content
   rather than retrieving or acting; Model Evaluation (D) compares model
   quality, not runtime behavior; Provisioned Throughput (E) is a
   capacity/throughput option, not a retrieval or action capability.

10. **B — Domain 2.** Hallucination specifically means the model
    confidently presents fabricated information as fact, distinct from
    merely being wrong or low-quality. A describes a refusal, not
    hallucination; C describes a context-window limit; D describes
    determinism, which is a separate concept from factual grounding.

11. **C — Domain 3.** Bedrock Guardrails is purpose-built to filter
    harmful content and sensitive information (such as PII) in both
    prompts and responses without custom filtering code. Agents (A) is
    for taking actions; Knowledge Bases (B) is for retrieval-grounded
    answers; Model Evaluation (D) compares model quality rather than
    filtering runtime content.

12. **B — Domain 4.** A regulator's request for a specific, business-level
    justification of an individual decision is squarely an explainability
    requirement. Scalability, throughput, and elasticity (A, C, D) are
    infrastructure performance concerns unrelated to explaining a model's
    reasoning.

13. **B — Domain 5.** Encryption in transit protects data moving over a
    network (for example, TLS between a client and an API); encryption at
    rest protects stored data (for example, an S3 object encrypted with
    AWS KMS). A reverses the definitions; C incorrectly merges two
    distinct concepts into one KMS feature; D is false, since both apply
    equally in the cloud and on-premises.

14. **B — Domain 1.** A large gap between very high training performance
    and much lower test performance is the textbook symptom of
    overfitting (the model memorized training data rather than learning
    generalizable patterns). Underfitting (A) would show poor performance
    on both sets; C and D do not match this specific symptom pattern.

15. **B — Domain 2.** Chain-of-thought prompting explicitly asks the model
    to show intermediate reasoning steps before a final answer, with no
    retraining or extra labeled data required. Zero-shot prompting (A)
    gives no reasoning scaffold; fine-tuning (C) requires labeled data and
    retraining, which the scenario rules out; reducing the context window
    (D) would hurt, not help, multi-step reasoning.

16. **C — Domain 5.** An interface VPC endpoint powered by AWS PrivateLink
    keeps traffic between the VPC and Bedrock entirely off the public
    internet. A NAT gateway (A) still routes through public address space;
    a VPN (B) connects networks to each other, not a VPC directly to an
    AWS service; a public internet gateway (D) is the opposite of the
    stated requirement regardless of security group rules.

17. **B — Domain 1.** Batch size is set by a person before training begins,
    making it a hyperparameter. Final weights, the bias term, and
    regression coefficients (A, C, D) are all values the model itself
    learns during training, making them parameters, not hyperparameters.

18. **B — Domain 2.** PartyRock is the no-code, quick-prototyping sandbox
    purpose-built for exactly this kind of low-stakes concept validation.
    SageMaker JumpStart (A) targets deeper, more technical customization;
    AWS Trainium (C) is a training chip, not an app-building tool; Bedrock
    Agents (D) is a capability within a more involved Bedrock application,
    not a standalone no-code prototyping tool.

19. **B — Domain 3.** Fine-tuning on labeled examples of the exact desired
    phrasing directly teaches the model a specific style/format at the
    weight level, which RAG (grounding in facts) does not address on its
    own. Raising temperature (A) increases variability, working against
    consistent phrasing; abandoning RAG (C) would reintroduce the original
    factual-grounding problem; reducing the token limit (D) is unrelated
    to phrasing style.

20. **B — Domain 5.** AWS CloudTrail is purpose-built to log "who did what,
    and when" for API activity, including a specific principal invoking a
    specific API at a specific time. CloudWatch (A) focuses on operational
    metrics/logs; Config (C) tracks resource configuration state, not API
    call history; GuardDuty (D) is a threat-detection service, not an
    activity log.

21. **B — Domain 5.** Processing PHI on AWS requires executing a Business
    Associate Addendum (BAA) via AWS Artifact and using only
    HIPAA-eligible services configured appropriately. Enabling Shield
    alone (A) addresses DDoS protection, not HIPAA compliance;
    encryption in transit alone (C) is necessary but not sufficient;
    service release date (D) has no bearing on HIPAA eligibility.

22. **B — Domain 2.** Negative prompting explicitly instructs the model to
    avoid specific unwanted content or behavior in its response. Few-shot
    prompting (A) provides positive examples rather than exclusions; RAG
    (C) grounds answers in retrieved documents; continued pre-training
    (D) retrains the base model on unlabeled text, unrelated to
    instruction-level exclusions.

23. **C — Domain 1.** With no predefined labels anywhere in the data, the
    algorithm must discover structure/groupings on its own — the
    definition of unsupervised learning (clustering). Supervised learning
    (A) requires labeled outcomes; reinforcement learning (B) requires an
    agent/reward loop, not present here; D still requires some labeled
    data, which the scenario rules out.

24. **A — Domain 3.** Amazon Kendra provides managed, natural-language
    search without requiring the team to build or manage its own
    embedding model or similarity index — exactly matching the stated
    requirement. A custom OpenSearch vector database (B) is the right
    tool only when a team wants to manage its own embeddings, the
    opposite of this scenario; Trainium (C) is a training chip, not a
    search tool; Polly (D) performs text-to-speech, unrelated to search.

25. **B — Domain 2.** Amazon Q Business is managed and pre-built, letting a
    company connect enterprise data sources with comparatively little
    custom development compared to building a Bedrock RAG pipeline from
    scratch. A describes the opposite of Q Business's value proposition; C
    and D are factually incorrect claims about what Q Business supports.

26. **B — Domain 3.** Bedrock Model Evaluation supports human-based
    evaluation jobs specifically for subjective quality dimensions like
    persuasiveness that a fixed benchmark score cannot capture. Guardrails
    (A) filters content; Agents (C) executes actions; Provisioned
    Throughput (D) is a capacity option — none of them compare model
    output quality.

27. **B — Domain 4.** A SageMaker Model Card is the artifact a team
    authors about its own custom model's intended use, training data, and
    limitations. An AI Service Card (A) is authored by AWS about its own
    managed service, the reverse of this scenario; a Config rule (C) and
    a Guardrail (D) are unrelated governance/filtering mechanisms, not
    documentation artifacts.

28. **A — Domain 5.** Amazon Macie is purpose-built to continuously
    discover and classify sensitive data such as PII stored in S3.
    CloudWatch (B) handles operational metrics/logs; Config (C) tracks
    resource configuration; Audit Manager (D) assembles audit evidence —
    none of them scan S3 content for sensitive data.

29. **B — Domain 1.** Precision = TP / (TP + FP) = 90 / (90 + 10) = 90/100
    = 90%. Option A (75%) does not correspond to this formula; option C
    (97%) is close to accuracy for this matrix, not precision; option D
    (25%) matches neither precision nor recall for these values.

30. **B — Domain 2.** Temperature directly controls the randomness of
    token selection, with lower values producing more deterministic,
    focused output and higher values producing more varied, creative
    output. Maximum token limit (A) bounds response length; context
    window size (C) bounds total input+output tokens considered; parameter
    count (D) is a fixed model property, not a per-request setting.

31. **B — Domain 3.** On-demand throughput scales with usage and incurs no
    idle cost, fitting spiky, unpredictable traffic without pre-purchased
    capacity. Provisioned Throughput (A) is the opposite fit — it commits
    to reserved capacity, ideal for steady high volume, not idle-to-spike
    patterns; Agents (C) and continued pre-training (D) are unrelated to
    throughput/capacity planning.

32. **B — Domain 1.** Amazon Textract is specifically built to extract
    text, key-value pairs, and tables while preserving layout/structure
    from scanned documents. Comprehend (A) analyzes plain-text meaning
    without layout awareness; Transcribe (C) converts speech to text;
    Rekognition (D) analyzes image/video content, not document structure.

33. **C — Domain 3.** A metric tied directly to a real business outcome
    (ticket resolution time) is a business metric, the only evaluation
    layer connected to actual operational impact rather than model
    output quality alone. Automatic benchmarks (A) and human evaluation
    (B) assess output quality directly, not downstream business impact;
    parameter counts (D) are a static model property, not an evaluation
    metric.

34. **B — Domain 4.** IP indemnification terms, offered for certain
    Bedrock models, are the most directly relevant mitigation for
    copyright-infringement legal exposure. Guardrails (A) addresses
    safety/privacy content filtering, not copyright; temperature (C) and
    context window size (D) are inference settings unrelated to legal
    IP risk.

35. **B — Domain 5.** AWS Config continuously records resource
    configuration state and evaluates it against rules to flag drift or
    non-compliance over time. CloudTrail (A) logs API activity, not
    configuration state; Audit Manager (C) assembles evidence for audits
    using Config/CloudTrail data as inputs, rather than recording
    configuration itself; GuardDuty (D) performs threat detection.

36. **A — Domain 2.** Amazon Bedrock is the managed service providing a
    single API to access multiple foundation models from different
    providers without managing underlying infrastructure. AWS Trainium
    (B) is a training chip; SageMaker Ground Truth (C) is a data-labeling
    tool; Amazon Kendra (D) is an enterprise search service — none provide
    a unified multi-model API.

37. **B — Domain 3.** Continued pre-training uses large volumes of
    unlabeled domain-specific text to further train the base model on
    company terminology, exactly matching "unlabeled...without needing
    labeled input/output pairs." Fine-tuning (A) requires labeled pairs,
    the opposite of this requirement; negative prompting (C) and
    temperature (D) are inference-time settings, not weight-level
    customization.

38. **B — Domain 1.** Poor performance on both training and test data is
    the definition of underfitting (high bias) — the model has not
    learned the underlying pattern well enough on either set. Overfitting
    (A) would show a large gap between strong training performance and
    weak test performance, which is not described here; data leakage (C)
    and perfect generalization (D) do not match this symptom.

39. **B — Domain 2.** Few-shot prompting supplies examples inside the
    prompt without changing the model's weights; fine-tuning retrains the
    model's weights on labeled data. A reverses which technique changes
    the weights; C incorrectly treats them as identical processes; D is
    false, since few-shot prompting works across text, code, and other
    modalities, not only images.

40. **B — Domain 3.** Amazon Aurora with the pgvector extension lets a
    team store embeddings and perform similarity search integrated
    directly with an existing relational database. Polly (A) performs
    text-to-speech; AWS Trainium (C) is a training chip, not a data
    store; Comprehend (D) performs text analytics, not vector storage or
    search.

41. **B — Domain 4.** SageMaker Clarify is purpose-built to measure bias
    both pre-training (on the dataset, such as class imbalance or
    difference in proportions of labels) and post-training (on
    predictions, such as disparate impact). Feature Store (A) manages
    features for training/inference consistency; Data Wrangler (C)
    handles data prep; Neo (D) optimizes models for specific hardware —
    none of them measure bias.

42. **B — Domain 5.** GDPR is the EU's regulation focused on the
    protection of personal data, tested at a conceptual level on the
    exam. A incorrectly describes HIPAA's scope instead; C is not what
    GDPR governs; D is false, since GDPR can apply to organizations
    processing EU residents' data regardless of the organization's own
    location.

43. **B — Domain 2.** Few-shot prompting supplies two or three worked
    examples directly in the prompt, with no retraining, to demonstrate
    the desired format. Zero-shot prompting (A) provides no examples;
    continued pre-training (C) and fine-tuning (D) both retrain the
    model on labeled or unlabeled data, which this scenario does not
    involve.

44. **C — Domain 1.** An agent taking actions and learning from a numeric
    reward signal through trial and error, with no fixed labeled dataset,
    is the defining trait of reinforcement learning. Supervised (A) and
    unsupervised (B) learning both work from static datasets rather than
    a reward loop; "batch learning" (D) is not a standard learning-type
    category tested on the exam.

45. **B — Domain 3.** AWS Inferentia is the purpose-built chip for
    lower-cost inference at scale. AWS Trainium (A) is the corresponding
    chip for training, not inference; Graviton (C) is a general-purpose
    CPU architecture, not a training-specific chip in this context; a
    fixed EC2 instance family alone (D) does not represent AWS's
    purpose-built inference silicon.

46. **B — Domain 2.** Adaptability refers to a single foundation model
    being applicable to many different tasks through prompting alone,
    without retraining for each new task. A describes the opposite,
    narrow-task limitation typical of traditional ML models; C is false,
    since effective prompting still benefits from prompt engineering; D
    is an unsupported cost claim, not what "adaptability" refers to.

47. **B — Domain 1.** Amazon Lex is the managed service purpose-built for
    conversational bots and supports integrating speech recognition, with
    no in-house ML expertise required. Comprehend (A) analyzes text
    meaning rather than building conversational flows; Translate (C)
    converts between languages; Polly (D) converts text to speech, the
    reverse of speech recognition.

48. **B — Domain 3.** Automatic (benchmark) evaluation metrics provide an
    objective, repeatable score against a fixed dataset, ideal for
    comparing factual-answer accuracy across models. Human evaluation (A)
    is subjective and panel-based, not objective/repeatable in the same
    way; business metrics (C) tie to operational outcomes, not benchmark
    scores; Guardrails (D) filters content rather than evaluating quality.

49. **B — Domain 4.** A SageMaker Model Card is authored by the customer
    about their own model; an AI Service Card is authored by AWS about
    its own managed AI service. Option A reverses this authorship
    relationship; C and D make unsupported blanket claims not reflected
    in how either artifact is actually produced or shared.

50. **A — Domain 5.** AWS Audit Manager is purpose-built to assemble
    evidence from sources like CloudTrail and Config and map it to
    compliance frameworks such as GDPR or HIPAA. Macie (B) discovers
    sensitive data; GuardDuty (C) detects threats; CloudWatch (D) handles
    operational metrics/logs — none of them assemble audit-ready
    evidence mapped to frameworks.

51. **B — Domain 2.** A multimodal model is required whenever an
    application must process more than one input type, such as images
    and text together in a single request. A unimodal text-only model
    (A) cannot process images at all; parameter count (C) and batch-only
    inference support (D) are unrelated to modality support.

52. **B — Domain 3.** The customization spectrum runs prompt engineering
    → RAG → fine-tuning → continued pre-training, from least to most
    resource-intensive and from not touching model weights (prompt
    engineering, RAG) to fully retraining them (fine-tuning, continued
    pre-training). A, C, and D all present this ordering out of sequence.

53. **B — Domain 1.** Increasing model complexity further without adding
    data tends to worsen overfitting, not reduce it, making it the least
    effective (and actively counterproductive) option listed.
    Regularization, more diverse data, and cross-validation with early
    stopping (A, C, D) are all standard, effective techniques for
    reducing overfitting.

54. **B — Domain 4.** The energy and resource cost of large-scale AI
    training is the environmental-impact consideration called out
    alongside IP rights, privacy, and toxicity/bias as part of the legal
    and ethical considerations for responsible AI. Encryption at rest (A)
    and provisioned throughput capacity planning (C) are unrelated
    infrastructure/security concerns, not ethical considerations; data
    residency (D) concerns where data is stored, not energy consumption.

55. **B — Domain 3.** RAG against a knowledge base kept in sync with the
    live catalog lets the application reflect current data on every query
    without ever retraining the model. Fine-tuning nightly (A) is
    expensive and always somewhat stale between refresh cycles; continued
    pre-training on historical snapshots (C) does not reflect the latest
    data at query time; temperature (D) has no bearing on data freshness.

56. **A — Domain 4.** Veracity/robustness concerns whether outputs stay
    reliable under varied or adversarial conditions, while
    controllability concerns whether a human can direct, limit, or halt
    the system's behavior — two distinct responsible-AI dimensions. B
    incorrectly treats them as the same concept; C and D impose false
    scope restrictions not part of either dimension's actual definition.

57. **B — Domain 4.** When regulatory or legal accountability for an
    individual decision is required, favoring interpretability — even at
    some accuracy cost — is the standard trade-off, so the affected
    customer's specific prediction can be explained on request. A states
    the opposite priority; C and D describe unrelated trade-offs
    (encryption modes and Bedrock throughput options) that have nothing
    to do with balancing performance against interpretability.

58. **B — Domain 1.** Amazon Personalize is the purpose-built, managed
    recommendation service requiring no in-house ML expertise. SageMaker
    (A) would require building a custom model; Rekognition (C) analyzes
    images/video; Comprehend (D) analyzes text — neither fits a
    recommendations use case.

59. **B — Domain 2.** Zero-shot prompting gives the model a plain-language
    instruction with no worked examples. Few-shot prompting (A) would
    include examples, which are absent here; fine-tuning (C) and
    continued pre-training (D) both involve retraining, not a single
    inference-time instruction.

60. **A — Domain 3.** Bedrock Knowledge Bases is the most direct fit for
    grounding answers in specific source documents and citing the section
    used, without retraining any model. Agents (B) is for taking actions;
    Guardrails (C) filters content rather than retrieving it; Provisioned
    Throughput (D) is a capacity option unrelated to grounding answers in
    documents.

61. **B — Domain 1.** High bias is associated with underfitting (the model
    is too simple to capture the pattern), and high variance is
    associated with overfitting (the model is overly sensitive to
    training data fluctuations). A reverses this relationship; C is false,
    since bias and variance typically trade off against each other; D
    denies their well-established role in generalization error.

62. **A and C — Domain 2.** Hallucination (fabricating plausible but false
    content) and nondeterminism (identical prompts can yield different
    outputs) are both widely cited generative AI disadvantages. B and E
    describe the opposite of actual generative AI behavior (it is
    typically nondeterministic and only partially interpretable); D is an
    unsupported claim, since inference at scale has real, nonzero cost.

63. **B — Domain 3.** Amazon OpenSearch Service configured as a vector
    database is the fit when a team specifically wants to manage its own
    embeddings and index configuration. Amazon Kendra (A) is the better
    fit for the opposite scenario — natural-language search without
    managing embeddings — the reverse of this requirement; Polly (C) and
    Translate (D) are unrelated to vector search entirely.

64. **B — Domain 3.** Bedrock Guardrails, configured with
    sensitive-information filters, is purpose-built to block specific
    categories of sensitive content (such as credit card numbers) from
    appearing in model output, even under adversarial prompting. Knowledge
    Bases (A) retrieves documents; Model Evaluation (C) compares model
    quality; Agents (D) executes actions — none of them filter runtime
    output content.

65. **B — Domain 2.** The standard LLM lifecycle runs scope → select →
    adapt → evaluate → deploy → monitor: define the use case and success
    criteria, select a candidate foundation model, adapt/customize it,
    evaluate its performance, deploy it, then monitor it in production.
    A, C, and D all present these six stages out of their standard order.

---

## After you finish: scoring by domain

Tally your correct answers against the domain tag in each answer above,
then compare to the question counts in the
[domain weighting table](#domain-weighting):

| Domain | Questions in this exam | Your correct count |
|---|:---:|:---:|
| 1 — Fundamentals of AI and ML | 13 | ___ |
| 2 — Fundamentals of Generative AI | 16 | ___ |
| 3 — Applications of Foundation Models | 18 | ___ |
| 4 — Guidelines for Responsible AI | 9 | ___ |
| 5 — Security, Compliance, and Governance | 9 | ___ |
| **Total** | **65** | ___ |

Your two lowest-scoring domains are exactly the domains the
[study plans](exam-preparation-strategy.md#5-study-plans) tell you to
re-review before your next attempt or before exam day — re-read that
domain's guide section by section, focusing on the "Exam tip" callouts,
then retry the questions you missed here once you understand why the
correct answer is correct and every distractor is wrong.
