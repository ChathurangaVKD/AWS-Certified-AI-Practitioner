# Full-Length Mock Exam (AIF-C01)

This is a single, full-length mock exam for the AWS Certified AI
Practitioner (AIF-C01) certification. The five domain guides
([Domain 1](domain-1-fundamentals-of-ai-and-ml.md),
[Domain 2](domain-2-fundamentals-of-generative-ai.md),
[Domain 3](domain-3-applications-of-foundation-models.md),
[Domain 4](domain-4-guidelines-for-responsible-ai.md),
[Domain 5](domain-5-security-compliance-governance.md)) each end with
15–20 domain-siloed practice questions (~85 total) for learning one domain
at a time. This exam is different: it draws **65 questions from across all
five domains, mixed together in a single unordered sequence** — the way
the real exam actually presents them — at the **same domain-weight
distribution as the real exam**, so you can rehearse the real exam's
length, pacing, and domain mix in one sitting rather than one domain at a
time.

Every question here is reused verbatim from a domain guide's practice
question set (see the source citation under each answer), so this exam
does not introduce new exam content. What it adds is the *mix*: a single
65-question, 90-minute rehearsal that mirrors the real exam's structure
instead of testing one domain in isolation.

For guidance on *how* to prepare before attempting this exam, see the
[exam preparation and study strategy guide](exam-preparation-strategy.md) —
in particular its
[exam format and time-management section](exam-preparation-strategy.md#1-exam-format-and-time-management)
and its study plans, each of which schedules a full timed mock exam like
this one near the end of the plan.

## 1. How to take this exam

1. **Set a timer for 90 minutes** and answer all 65 questions in the
   [Mock exam questions](#4-mock-exam-questions) section below **before**
   looking at the [answer key](#5-answer-key-and-explanations). Treat it
   like exam day: no notes, no domain guides open, no pausing the timer.
2. **Answer every question — there is no penalty for a wrong answer** on
   the real exam, so never leave one blank. If you're unsure, flag it
   mentally, make your best guess, and move on rather than stalling.
3. **Watch the instruction line on every question.** Most are standard
   multiple choice (choose one), but a few are multiple response, marked
   "(Select TWO.)" or "(Multiple response — select TWO)" — every correct
   option must be selected for credit, partial credit is not given.
4. **Score yourself** using [Section 6](#6-scoring-this-exam) once you've
   finished, then read every explanation in the
   [answer key](#5-answer-key-and-explanations) — not just for the
   questions you missed — since a right answer for the wrong reason won't
   hold up against the real exam's distractors.

## 2. Timing guidance and pacing checkpoints

The real AIF-C01 exam is **65 questions in 90 minutes** (≈1.4 minutes per
question on average). This mock exam uses the same limits. Pacing is
never perfectly even in practice — some questions are a one-line
definitional lookup, others are multi-paragraph scenarios — so use these
checkpoints to catch yourself running badly behind, not as a rigid
per-question clock:

| Checkpoint | Questions completed | Elapsed time target |
|---|---|---|
| 25% | Question 17 of 65 | ~23 minutes |
| 50% | Question 33 of 65 | ~45 minutes |
| 75% | Question 49 of 65 | ~68 minutes |
| 100% | Question 65 of 65 | 90 minutes |

If you're significantly behind a checkpoint (for example, still on
question 20 at the 45-minute mark), stop deliberating on hard questions —
make your best guess, flag it mentally, and keep moving so you reach every
question at least once before time runs out.

## 3. Domain weight distribution in this exam

This exam draws its 65 questions from the five domain guides' practice
question sets at (as closely as 65 questions allows) the same domain-weight
distribution as the real AIF-C01 exam:

| # | Domain | Real exam weight | Questions in this mock exam | Share of this exam |
|---|--------|:-----------:|:---:|:---:|
| 1 | [Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md) | ~20% | 13 | 20.0% |
| 2 | [Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md) | ~24% | 16 | 24.6% |
| 3 | [Applications of Foundation Models](domain-3-applications-of-foundation-models.md) | ~28% | 18 | 27.7% |
| 4 | [Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md) | ~14% | 9 | 13.8% |
| 5 | [Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md) | ~14% | 9 | 13.8% |
| | **Total** | **100%** | **65** | **100%** |

Unlike the domain guides, **the questions below are not grouped by
domain** — they're interleaved in a fixed mixed order, matching how the
real exam presents questions from all five domains without signaling which
domain each one belongs to. The domain each question comes from is only
revealed in the [answer key](#5-answer-key-and-explanations), so that
reviewing a missed question also tells you which domain guide to revisit.

---

## 4. Mock exam questions

*(65 questions. Do not consult the answer key until you have answered
every question below.)*

### Questions 1–33 (first half — target ~45 minutes)

1. A company wants its generative AI assistant to always answer using the
   most current version of its product catalog, which changes daily, and
   cannot afford to retrain a model every day. Which approach best fits
   this requirement?
   A. Fine-tuning
   B. Continued pre-training
   C. Retrieval Augmented Generation (RAG) with Amazon Bedrock Knowledge Bases
   D. Increasing the model's temperature parameter

2. A developer notices that the same prompt sent to a foundation model
   twice produces two noticeably different responses. Which concept best
   explains this behavior?
   A. Hallucination
   B. Nondeterminism
   C. Overfitting
   D. Fine-tuning

3. A company wants to group its customers into segments based on purchasing
   behavior, but it has no predefined categories or labels. Which type of
   machine learning should it use?
   A. Supervised learning
   B. Unsupervised learning
   C. Reinforcement learning
   D. Semi-supervised learning

4. Which factor should a team prioritize first when a use case requires
   the model to generate both text and images from a single prompt?
   A. Cost per token
   B. Modality support
   C. Provisioned throughput commitment length
   D. Chain-of-thought prompting

5. A hiring-decision model performs well overall but is later found to
   reject qualified candidates from one demographic group at a
   significantly higher rate than others. Which responsible AI dimension
   does this problem most directly violate?
   A. Governance
   B. Fairness
   C. Controllability
   D. Environmental sustainability

6. A company wants its SageMaker training jobs, running in a private VPC subnet with no internet gateway, to read training data from S3 without traversing the public internet. What should they configure?
   A. An internet gateway with a restrictive security group
   B. A gateway VPC endpoint for Amazon S3
   C. A NAT gateway
   D. A site-to-site VPN connection

7. Which AWS service provides access to a choice of foundation models from
   Amazon and third-party providers through a single, unified API without
   managing any underlying infrastructure?
   A. Amazon SageMaker JumpStart
   B. Amazon Q Developer
   C. Amazon Bedrock
   D. Amazon Comprehend

8. Which of the following best describes the relationship between AI, ML,
   and deep learning?
   A. Deep learning is a broader field that contains machine learning, which contains AI
   B. AI, ML, and deep learning are unrelated, independently developed fields
   C. AI is the broadest field; ML is a subset of AI; deep learning is a subset of ML
   D. ML and deep learning are the same technique with different names

9. A developer wants a foundation model to reliably output responses in a
   very specific JSON schema by showing it several example input/output
   pairs directly inside the prompt, without any training job. Which
   prompt engineering technique is this?
   A. Zero-shot prompting
   B. Few-shot prompting
   C. Continued pre-training
   D. Fine-tuning

10. A company wants its support chatbot to answer questions using its own,
   frequently changing internal documentation, without retraining the
   underlying model. Which approach best fits this need?
   A. Full pretraining of a new foundation model
   B. Fine-tuning on internal documentation
   C. Retrieval Augmented Generation (RAG)
   D. Increasing the temperature parameter

11. A model is prone to giving a final answer to multi-step math word
   problems without correctly working through the intermediate steps.
   Which prompting technique would most directly help, at no additional
   training cost?
   A. Negative prompting
   B. Chain-of-thought prompting
   C. Provisioned throughput
   D. Continued pre-training

12. Which AWS service should a data science team use to measure whether a
   training dataset shows a significant difference in the proportion of
   positive labels across two demographic groups, before a model is even
   trained?
   A. Guardrails for Amazon Bedrock
   B. Amazon SageMaker Clarify
   C. Amazon A2I
   D. AI Service Cards

13. Which AWS service should a compliance team use to download AWS's SOC 2 report and execute a HIPAA Business Associate Addendum?
   A. AWS Audit Manager
   B. AWS Config
   C. AWS Artifact
   D. AWS CloudTrail

14. A data scientist notices a model achieves 98% accuracy on training data
   but only 61% accuracy on the test data. What is the most likely problem?
   A. Underfitting
   B. Overfitting
   C. Data leakage prevention
   D. Insufficient hyperparameters

15. In the transformer architecture, which mechanism allows a model to weigh
   the relevance of every other token in the input when processing a given
   token, regardless of distance between them?
   A. Convolution
   B. Self-attention
   C. Gradient descent
   D. Regularization

16. Which of the following best describes the purpose of Amazon Bedrock
   Knowledge Bases?
   A. It fine-tunes a foundation model's weights on labeled data
   B. It automatically manages ingestion, chunking, embedding, and retrieval of your own data to ground FM responses
   C. It provides dedicated, reserved inference capacity for a model
   D. It filters harmful content from model outputs

17. Which AWS service should a company with no in-house ML expertise use to
   add real-time, individualized product recommendations to its e-commerce site?
   A. Amazon SageMaker
   B. Amazon Personalize
   C. Amazon Forecast
   D. Amazon Comprehend

18. A prompt engineer wants to improve a model's accuracy on a multi-step
   arithmetic word problem without fine-tuning or adding examples. Which
   prompting technique is most appropriate?
   A. Zero-shot prompting
   B. Negative prompting
   C. Chain-of-thought prompting
   D. Top-k sampling

19. A company wants a foundation model to deeply understand highly
   specialized medical terminology found throughout a large volume of
   unlabeled clinical text, improving its general fluency in that domain
   rather than teaching it one specific task. Which customization approach
   fits best?
   A. Prompt engineering
   B. RAG
   C. Continued pre-training
   D. Provisioned throughput

20. A company wants to document, for internal governance purposes, the
   intended use, training data description, evaluation metrics, and known
   limitations of a custom model it trained on Amazon SageMaker. Which
   AWS capability is designed for exactly this?
   A. AI Service Cards
   B. Guardrails for Amazon Bedrock
   C. Amazon SageMaker Model Cards
   D. Amazon Macie

21. A security team needs to know exactly which IAM principal called `bedrock:InvokeModel` on a specific model at 3:14 AM last Tuesday. Which service provides this?
   A. AWS Config
   B. AWS CloudTrail
   C. AWS Audit Manager
   D. Amazon CloudWatch

22. A company wants non-technical employees to quickly and freely
   experiment with foundation models and prototype a simple app for an
   internal hackathon, with no coding and no infrastructure setup. Which
   AWS offering best fits?
   A. Amazon SageMaker JumpStart
   B. PartyRock
   C. Amazon Bedrock Agents
   D. Amazon Q Developer

23. A hospital is building a diagnostic model to detect a rare disease that
   occurs in 1% of patients. Which evaluation metric is LEAST appropriate
   on its own for this use case?
   A. Recall
   B. Precision
   C. Accuracy
   D. F1 score

24. Which statement correctly distinguishes fine-tuning from continued
   pre-training?
   A. Fine-tuning requires unlabeled data; continued pre-training requires labeled data
   B. Fine-tuning uses labeled input/output examples to adapt a model to a specific task; continued pre-training uses large volumes of unlabeled domain text to deepen general domain knowledge
   C. They are the same process with different names
   D. Neither approach changes the model's weights

25. Which inference parameter, when lowered, makes a foundation model's
   output more focused and deterministic?
   A. Maximum length
   B. Top-k
   C. Temperature
   D. Context window

26. A company wants a Bedrock-based assistant to look up a customer's order
   status by calling an internal REST API and then answer a follow-up
   question using internal documentation, all within one conversation.
   Which Amazon Bedrock feature is designed for this?
   A. Guardrails for Amazon Bedrock
   B. Amazon Bedrock Agents
   C. Provisioned throughput
   D. Amazon Bedrock model evaluation

27. A generative AI chatbot occasionally generates confident but
   fabricated answers not supported by the source documents it was given.
   Which Guardrails for Amazon Bedrock capability most directly addresses
   this?
   A. Denied topics
   B. Word filters
   C. Contextual grounding checks
   D. Content filters for violence

28. A retail company wants to automatically discover whether any documents in their S3-based product-review dataset contain customer PII before using them to fine-tune a model. Which service should they use?
   A. Amazon GuardDuty
   B. AWS Config
   C. Amazon Macie
   D. AWS Trusted Advisor

29. In the standard ML development lifecycle, which step comes immediately
   after model training and before deployment?
   A. Data collection
   B. Exploratory data analysis
   C. Evaluation and hyperparameter tuning
   D. Monitoring

30. A marketing team wants to generate product images but wants to exclude
   any watermark, logo, or text from appearing in the generated images.
   Which prompting technique should they use?
   A. Few-shot prompting
   B. Negative prompting
   C. Chain-of-thought prompting
   D. Zero-shot prompting

31. A company expects high, steady, predictable request volume for a
    custom fine-tuned model in production and wants guaranteed, consistent
    throughput. Which Bedrock capacity option should they choose?
    A. On-demand pricing
    B. Provisioned throughput
    C. Automatic model evaluation
    D. Continued pre-training

32. Which AWS service is purpose-built to extract text, key-value pairs, and
   tables (preserving structure) from scanned documents?
   A. Amazon Comprehend
   B. Amazon Rekognition
   C. Amazon Textract
   D. Amazon Transcribe

33. A team needs to compare several candidate foundation models on
    accuracy and robustness quickly, cheaply, and objectively before
    narrowing down to finalists. Which approach fits best?
    A. Human evaluation
    B. Automatic model evaluation using benchmark datasets
    C. Business metric tracking
    D. Provisioned throughput

---

### Questions 34–65 (second half — target ~45 minutes)

34. Which of the following best distinguishes bias from variance in a
   machine learning model?
   A. Bias is a model's sensitivity to small fluctuations in training data; variance is a systematic unfair skew
   B. Bias is a systematic, often unfair skew from data or training issues; variance is a model's sensitivity to fluctuations in the training data
   C. Bias and variance both refer exclusively to fairness across demographic groups
   D. Bias and variance are two names for the same concept

35. Which statement about encryption at rest vs. in transit for Amazon Bedrock is correct?
   A. Bedrock only encrypts data in transit; data at rest is unencrypted by default
   B. Bedrock encrypts data both at rest and in transit by default, and supports customer-managed KMS keys for custom models
   C. Encryption at rest must be manually enabled by opening a support ticket
   D. Bedrock does not support customer-managed encryption keys under any circumstance

36. Which AWS service is purpose-built to give employees a ready-made,
    generative-AI assistant that answers questions grounded in company data
    from systems like SharePoint and Salesforce, with minimal setup and
    built-in access controls?
    A. Amazon Bedrock
    B. Amazon SageMaker JumpStart
    C. Amazon Q Business
    D. PartyRock

37. After launch, which of the following is a business metric (as
    distinct from a model-quality metric) for a generative AI customer
    support assistant?
    A. BLEU score against a benchmark dataset
    B. Toxicity score from an automatic evaluation job
    C. Customer satisfaction (CSAT) score and call-deflection rate
    D. F1 score on a labeled test set

38. Which of the following is a hyperparameter rather than a parameter?
   A. A neural network's learned weight values
   B. The learning rate used during training
   C. The bias term learned by a linear regression model
   D. The coefficients learned by a regression model

39. What is the primary difference between few-shot prompting and
    fine-tuning?
    A. Few-shot prompting permanently updates the model's weights; fine-tuning does not
    B. Few-shot prompting only works with negative prompts; fine-tuning does not
    C. Few-shot prompting supplies examples within a single prompt and changes nothing about the model; fine-tuning retrains the model's weights on labeled data
    D. There is no meaningful difference; both terms describe the same process

40. A bank discovers that its loan approval model reflects discriminatory
   patterns present in decades of past lending decisions, even though the
   data was collected accurately. Which type of bias does this describe?
   A. Sampling bias
   B. Historical bias
   C. Measurement bias
   D. Aggregation bias

41. A financial institution must produce a consolidated, audit-ready report showing evidence of compliance with an internal risk framework for its AI-powered fraud detection system, pulling from configuration history and API logs automatically. Which service is purpose-built for this?
   A. AWS Config
   B. AWS CloudTrail
   C. AWS Audit Manager
   D. Amazon Macie

42. Which AWS service should a team use to generate vector embeddings from
    text for use in a semantic search application?
    A. AWS Trainium
    B. Amazon Titan Text Embeddings
    C. AWS Inferentia
    D. Amazon SageMaker JumpStart

43. Which combination of AWS generative AI concepts would a company use to
    let employees search internal documents by meaning rather than exact
    keyword match? (Select TWO.)
    A. Embeddings model to convert documents into vectors
    B. A vector database to store and query the vectors by similarity
    C. Amazon Forecast to predict document access patterns
    D. Fine-tuning a classification model to label documents as spam
    E. Amazon Polly to convert documents to speech

44. Which SageMaker capability is specifically designed to store and share
    curated features consistently between model training and real-time
    inference to avoid training/serving skew?
    A. SageMaker Data Wrangler
    B. SageMaker Feature Store
    C. SageMaker Clarify
    D. SageMaker Model Monitor

45. A team already runs its application data in Amazon Aurora PostgreSQL
    and wants to add vector similarity search without adopting a separate
    dedicated search service. Which option fits best?
    A. Amazon Kendra
    B. Amazon Aurora with the pgvector extension
    C. AWS Trainium
    D. Amazon Bedrock Agents

46. A company wants a coding assistant that can suggest code completions,
    explain code, run security scans, and answer natural-language questions
    about their AWS account resources. Which AWS service is the best fit?
    A. Amazon Q Business
    B. Amazon Q Developer
    C. Amazon Comprehend
    D. Amazon Textract

47. A model classifying loan applications as "approve" or "reject" has the
    following confusion matrix on test data: TP = 180, FP = 20, FN = 60,
    TN = 740. What is the recall of the model (rounded)?
    A. 90%
    B. 75%
    C. 25%
    D. 96%

48. A media company is concerned that images generated by a foundation
   model on Amazon Bedrock could expose it to copyright infringement
   claims. Which consideration would most directly reduce this specific
   legal risk?
   A. Enabling Guardrails content filters for violence
   B. Choosing a Bedrock model whose provider offers IP indemnification
   C. Lowering the model's temperature parameter
   D. Adding a SageMaker Model Card

49. In a GDPR context, when a company uses Amazon Bedrock to process personal data of EU customers, which role does AWS typically play?
    A. Data controller
    B. Data subject
    C. Data processor
    D. Supervisory authority

50. A team wants to add natural-language search across its existing
    SharePoint and Amazon S3 document repositories, without building or
    managing an embeddings pipeline themselves. Which AWS service is the
    best fit?
    A. Amazon Kendra
    B. AWS Inferentia
    C. Amazon Aurora with pgvector
    D. AWS Trainium

51. Which statement about foundation models is correct?
    A. A foundation model must be trained from scratch for every new task
    B. A foundation model is pretrained on broad data and can be adapted to many downstream tasks
    C. A foundation model can only process text input and text output
    D. A foundation model cannot be customized in any way after pretraining

52. Which purpose-built AWS chip is optimized specifically for
    cost-efficient, high-performance training of deep learning and
    foundation models at scale?
    A. AWS Inferentia
    B. AWS Trainium
    C. AWS Graviton
    D. AWS Nitro

53. Which technique is generally the LEAST effective way to reduce overfitting?
    A. Adding regularization (e.g., L2 penalty)
    B. Collecting more diverse training data
    C. Increasing model complexity further
    D. Using cross-validation and early stopping

54. Which of the following best describes what a "token" is in the context
    of a large language model?
    A. A security credential used to authenticate API calls to the model
    B. The basic unit of text, such as a word or part of a word, that the model processes and generates
    C. A single parameter learned during model pretraining
    D. A unit of measurement for GPU memory usage

55. A financial institution is choosing between a simple, interpretable
    scoring model and a complex deep learning model for a credit
    underwriting decision that must be explained to regulators and
    rejected applicants. Which factor should weigh most heavily in favor
    of the simpler model?
    A. The simpler model always has lower training cost
    B. The simpler model requires less training data
    C. The simpler model is easier to interpret and explain to regulators and affected individuals, which is required for this high-stakes, regulated decision
    D. The simpler model has no risk of bias

56. Which service provides continuous, ML-driven threat detection for suspicious or malicious activity in an AWS account hosting AI workloads?
    A. Amazon Macie
    B. Amazon GuardDuty
    C. AWS Config
    D. AWS Audit Manager

57. A company wants to quickly deploy and optionally fine-tune a
    pretrained foundation model with more direct control over hosting than
    Amazon Bedrock's fully managed API provides. Which AWS capability best
    fits this need?
    A. Amazon Bedrock Guardrails
    B. Amazon SageMaker JumpStart
    C. Amazon Kendra
    D. Amazon Bedrock model evaluation

58. A team is building a completely custom fraud model using a proprietary
    algorithm and unique internal features that no managed AWS AI service
    supports out of the box. Which AWS service should they use?
    A. Amazon Fraud Detector
    B. Amazon SageMaker
    C. Amazon Comprehend
    D. Amazon Personalize

59. Which of the following is the best example of using generative AI for
    "summarization" as a business use case?
    A. Automatically flagging fraudulent transactions in real time
    B. Condensing a 40-page customer contract into a one-paragraph summary for a reviewer
    C. Predicting next quarter's inventory demand
    D. Translating a product listing into five languages

60. Which combination of factors is part of "design considerations for
    foundation model applications" as tested on the AIF-C01 exam? (Select
    TWO.)
    A. The modality (text, image, audio) the application must support
    B. The latency requirements of the use case
    C. The specific AWS Region's time zone offset
    D. The font used to render the application's UI
    E. The color palette of the company's marketing website

61. During exploratory data analysis, a data scientist discovers a dataset
    is missing 40% of values in one column and contains several extreme
    outliers in another. In the ML lifecycle, which stage should address
    these issues before training begins?
    A. Model monitoring
    B. Data preparation / feature engineering
    C. Model deployment
    D. Hyperparameter tuning

62. A company deploys a chatbot built on a foundation model and later finds
    it occasionally states incorrect, fabricated facts with high
    confidence, such as citing a policy clause that does not exist. Which
    concept describes this specific behavior?
    A. Nondeterminism
    B. Overfitting
    C. Hallucination
    D. Underfitting

---

63. Which combination of concerns falls under "legal and ethical
    considerations" for generative AI on the AIF-C01 exam? (Select TWO.)
    A. Intellectual property risk from training on or generating content similar to copyrighted material
    B. Data privacy obligations around personal data used in training or prompts
    C. Choosing the number of attention heads in a transformer
    D. Selecting the AWS Region with the lowest network latency
    E. Configuring a VPC subnet's CIDR block

64. Which statement correctly distinguishes AWS Config from AWS CloudTrail?
    A. Config logs API calls; CloudTrail tracks resource configuration compliance over time
    B. Config tracks resource configuration state and compliance rules over time; CloudTrail logs API call activity
    C. They are interchangeable and provide identical functionality
    D. Config is only for networking resources; CloudTrail is only for IAM resources

65. A retail company wants a generative AI assistant to consistently
    output product descriptions in the company's exact required tone and
    format, and has hundreds of labeled example descriptions already
    written by their copywriting team. Which customization approach is the
    best fit?
    A. Prompt engineering only
    B. RAG only
    C. Fine-tuning
    D. Increasing the context window

---

---

## 5. Answer key and explanations

*(Each answer notes the correct option(s), why they're correct and the
distractors aren't, and the domain guide the question was originally drawn
from — follow that link to restudy the underlying material.)*

1. **C — Retrieval Augmented Generation (RAG) with Amazon Bedrock
   Knowledge Bases.** RAG retrieves current external data at query time
   without retraining, exactly fitting a daily-changing catalog.
   Fine-tuning (A) and continued pre-training (B) bake knowledge into
   static weights and would require retraining daily; changing temperature
   (D) affects randomness of output, not knowledge freshness.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q1.)*

2. **B — Nondeterminism.** Generative models sample from a probability
   distribution over possible next tokens, so identical prompts can yield
   different outputs across runs. Hallucination (A) refers to fabricated
   facts, not run-to-run variation; overfitting (C) and fine-tuning (D) are
   unrelated training concepts, not response-to-response behavior.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q1.)*

3. **B — Unsupervised learning.** No labels/categories exist, so the
   algorithm must find structure on its own (clustering). Supervised (A)
   requires labeled outcomes; reinforcement (C) requires an agent/reward
   loop, not present here; semi-supervised (D) requires at least some
   labeled data.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q1.)*

4. **B — Modality support.** If a model can't process/generate the
   required input/output types, no amount of cost or prompting technique
   makes it viable, so modality must be filtered on first. Cost (A) and
   provisioned throughput (C) are capacity/pricing decisions made after
   narrowing to modality-capable models; chain-of-thought prompting (D)
   is a reasoning technique, unrelated to modality support.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q2.)*

5. **B — Fairness.** A model that systematically disadvantages a
   demographic group in its outcomes is a fairness problem by definition.
   Governance (A) concerns oversight processes, not the outcome itself;
   controllability (C) concerns human ability to intervene; environmental
   sustainability (D) concerns resource/energy impact, unrelated to
   discriminatory outcomes.
   *(Source: [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), original Q1.)*

6. **B.** A gateway VPC endpoint for S3 keeps S3 traffic within the AWS network without needing internet access. (A) and (C) both require internet connectivity the private subnet lacks by design; (D) a VPN connects networks, it doesn't provide S3 access.
   *(Source: [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md), original Q1.)*

7. **C — Amazon Bedrock.** It is specifically the fully managed service
   offering a choice of FMs from Amazon and third parties via one unified
   API with no infrastructure to manage. SageMaker JumpStart (A) requires
   deploying models onto managed infrastructure you control; Q Developer
   (B) is a coding assistant, not a general multi-model API; Comprehend (D)
   is a traditional NLP service, not a foundation model access layer.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q2.)*

8. **C — AI is the broadest field; ML is a subset of AI; deep learning is a
   subset of ML.** This is the standard nesting relationship. A reverses
   the hierarchy; B is false since the fields are directly related by
   subset; D incorrectly equates ML and deep learning, which differ in
   technique and data requirements.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q2.)*

9. **B — Few-shot prompting.** Providing example input/output pairs
   directly in the prompt to shape output format is the definition of
   few-shot prompting. Zero-shot (A) provides no examples; continued
   pre-training (C) and fine-tuning (D) both require a training job and
   change model weights, which the scenario explicitly rules out.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q3.)*

10. **C — Retrieval Augmented Generation (RAG).** RAG grounds model outputs
   in externally retrieved, current data at inference time without
   changing model weights, ideal for frequently changing documentation.
   Full pretraining (A) is extremely costly and unnecessary; fine-tuning
   (B) would need to be repeated every time the documentation changes;
   raising temperature (D) increases randomness and has nothing to do with
   grounding answers in data.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q3.)*

11. **B — Chain-of-thought prompting.** Instructing the model to reason
   step-by-step directly improves multi-step reasoning accuracy at no
   training cost. Negative prompting (A) tells the model what to avoid,
   not how to reason; provisioned throughput (C) is a capacity/pricing
   feature; continued pre-training (D) requires a costly training job the
   scenario doesn't call for.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q4.)*

12. **B — Amazon SageMaker Clarify.** Clarify computes pre-training bias
   metrics, including difference in proportions of labels, directly on a
   dataset before any model is trained. Guardrails (A) operates at
   inference time on a deployed generative model, not on a training
   dataset; A2I (C) routes predictions to human reviewers, it doesn't
   measure dataset bias; AI Service Cards (D) are documentation, not a
   measurement tool.
   *(Source: [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), original Q2.)*

13. **C.** AWS Artifact is the self-service portal for AWS's compliance reports and agreements, including the HIPAA BAA. Audit Manager (A) builds evidence for *your* account's compliance, not AWS's own certifications; Config (B) tracks resource configuration; CloudTrail (D) logs API activity.
   *(Source: [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md), original Q2.)*

14. **B — Overfitting.** Very high training performance with much lower
   test performance is the textbook symptom of overfitting (high
   variance), where the model memorized training data. Underfitting (A)
   would show poor performance on *both* sets. C and D are not real
   diagnoses matching these symptoms.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q3.)*

15. **B — Self-attention.** This is the transformer's defining mechanism,
   allowing every token to attend to every other token regardless of
   distance. Convolution (A) is used in CNNs for vision, not transformers;
   gradient descent (C) is a general optimization method, not an attention
   mechanism; regularization (D) reduces overfitting and is unrelated to
   attention.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q4.)*

16. **B — It automatically manages ingestion, chunking, embedding, and
   retrieval of your own data to ground FM responses.** This is Knowledge
   Bases' defining purpose (managed RAG). Fine-tuning weights (A) is a
   separate Bedrock customization feature; reserved capacity (C) describes
   provisioned throughput; content filtering (D) describes Guardrails.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q5.)*

17. **B — Amazon Personalize.** It is a purpose-built, managed
   recommendation service requiring no ML expertise. SageMaker (A) would
   require building a custom model; Forecast (C) is for time-series
   prediction, not recommendations; Comprehend (D) is for text analytics.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q4.)*

18. **C — Chain-of-thought prompting.** Instructing the model to reason step
   by step measurably improves performance on multi-step reasoning tasks
   like arithmetic word problems. Zero-shot (A) provides no reasoning
   scaffold; negative prompting (B) tells the model what to avoid, not how
   to reason; top-k (D) is an inference sampling parameter, not a
   reasoning technique.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q5.)*

19. **C — Continued pre-training.** Deepening general domain
   understanding from a large volume of unlabeled text, rather than
   teaching one specific task, is exactly what continued pre-training
   does. Prompt engineering (A) doesn't change the model's underlying
   knowledge; RAG (B) retrieves facts at query time rather than deepening
   the model's fluency; provisioned throughput (D) is a capacity feature
   unrelated to customization.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q6.)*

20. **C — Amazon SageMaker Model Cards.** Model Cards are purpose-built to
   record intended use, training data, evaluation results, and
   limitations for a model an organization trained. AI Service Cards (A)
   document AWS-managed services, not your own custom model; Guardrails
   (B) filters live inference content, it doesn't document a model; Macie
   (D) discovers and classifies sensitive data, unrelated to model
   documentation.
   *(Source: [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), original Q3.)*

21. **B.** AWS CloudTrail records the identity, action, resource, and timestamp of every API call, exactly answering "who did what, when." Config (A) tracks configuration state, not individual API calls; Audit Manager (C) aggregates evidence rather than providing a raw call-level log; CloudWatch (D) is for metrics/operational logs, not identity-level API auditing.
   *(Source: [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md), original Q4.)*

22. **B — PartyRock.** It is a free, no-code Amazon Bedrock playground built
   specifically for rapid, hands-on experimentation and prototyping with no
   infrastructure setup. SageMaker JumpStart (A) requires more
   infrastructure and ML familiarity; Bedrock Agents (C) requires defining
   APIs/actions and is not no-code; Q Developer (D) is a coding assistant,
   not a general app-prototyping playground.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q7.)*

23. **C — Accuracy.** With only 1% positive cases, a model predicting
   "negative" for everyone would still score ~99% accuracy while being
   clinically useless — the accuracy paradox on imbalanced data. Recall,
   precision, and F1 (A, B, D) are all more informative for rare-event
   detection.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q5.)*

24. **B — Fine-tuning uses labeled input/output examples to adapt a model
   to a specific task; continued pre-training uses large volumes of
   unlabeled domain text to deepen general domain knowledge.** This is the
   precise labeled-vs-unlabeled, task-vs-domain distinction the exam
   tests. A reverses the data requirements; C is false, they are distinct
   processes; D is false, both approaches update model weights.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q7.)*

25. **C — Temperature.** Lower temperature makes the probability
   distribution over next tokens more peaked, producing more focused,
   deterministic output. Maximum length (A) caps response size, not
   randomness; top-k (B) restricts candidate tokens but temperature is the
   parameter most directly described as controlling randomness/focus;
   context window (D) limits how much input/output the model can consider,
   not the randomness of generation.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q8.)*

26. **B — Amazon Bedrock Agents.** Agents are purpose-built to plan and
   execute multi-step tasks, including invoking external APIs (action
   groups) and consulting Knowledge Bases within one interaction.
   Guardrails (A) filters content, it doesn't call APIs or orchestrate
   steps; provisioned throughput (C) is a capacity feature; model
   evaluation (D) assesses model quality, it isn't a runtime orchestration
   feature.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q8.)*

27. **C — Contextual grounding checks.** This Guardrails feature verifies
   that a response is grounded in the provided source content, directly
   reducing hallucinated/fabricated answers. Denied topics (A) block
   entire subject areas, not ungrounded facts within an allowed topic;
   word filters (B) block specific words/phrases; content filters for
   violence (D) address harmful content categories, not factual grounding.
   *(Source: [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), original Q5.)*

28. **C.** Amazon Macie uses ML to discover and classify sensitive data like PII in S3. GuardDuty (A) detects threats, not sensitive data content; Config (B) tracks resource configuration; Trusted Advisor (D) gives cost/performance/security best-practice checks, not content-level PII discovery.
   *(Source: [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md), original Q5.)*

29. **C — Evaluation and hyperparameter tuning.** The standard lifecycle
   order is train → evaluate/tune → deploy → monitor. Data collection (A)
   and EDA (B) happen before training; monitoring (D) happens after
   deployment.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q6.)*

30. **B — Negative prompting.** Explicitly stating what to exclude (no
   watermark, logo, or text) is the definition of negative prompting, most
   common in image generation. Few-shot (A) would require example
   image/prompt pairs, not exclusions; chain-of-thought (C) is for
   reasoning tasks, not image constraints; zero-shot (D) simply means no
   examples are given, which doesn't describe exclusion instructions.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q9.)*

31. **B — Provisioned throughput.** High, steady, predictable volume for a
    custom model is exactly the scenario provisioned throughput is
    designed and cost-effective for, and it's typically required to serve
    fine-tuned custom models. On-demand (A) suits variable/unpredictable
    traffic, not steady high volume; automatic model evaluation (C) and
    continued pre-training (D) are unrelated to serving capacity.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q10.)*

32. **C — Amazon Textract.** It is specifically built to extract text,
   forms, and tables with structural/layout awareness from scanned
   documents. Comprehend (A) analyzes plain text meaning, not document
   layout; Rekognition (B) is for images/video content, not structured
   document data; Transcribe (D) converts speech, not scanned documents.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q7.)*

33. **B — Automatic model evaluation using benchmark datasets.** Automatic
    evaluation against benchmark datasets is fast, low-cost, and
    objective — ideal for quickly comparing many candidates. Human
    evaluation (A) is slower and more expensive, better suited to
    subjective criteria; business metrics (C) are measured post-launch on
    real usage, not during model comparison; provisioned throughput (D) is
    a capacity feature, not an evaluation method.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q11.)*

34. **B — Bias is a systematic, often unfair skew from data or training
   issues; variance is a model's sensitivity to fluctuations in the
   training data.** This is the precise definitional distinction the exam
   tests. A reverses the definitions; C incorrectly limits both terms to
   fairness only, when variance is a general ML concept unrelated to
   demographics; D is false since they describe different phenomena.
   *(Source: [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), original Q6.)*

35. **B.** Bedrock encrypts data at rest and in transit by default and supports customer-managed KMS keys for custom models/fine-tuning data. (A), (C), and (D) all misstate Bedrock's default and configurable encryption behavior.
   *(Source: [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md), original Q6.)*

36. **C — Amazon Q Business.** It is purpose-built as a ready-made
    enterprise assistant that connects to systems like SharePoint and
    Salesforce with minimal setup and respects existing access controls.
    Bedrock (A) requires building a custom application; SageMaker
    JumpStart (B) is for deploying/customizing models, not a turnkey
    assistant; PartyRock (D) is for no-code experimentation, not
    enterprise data integration with access controls.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q10.)*

37. **C — Customer satisfaction (CSAT) score and call-deflection rate.**
    These are outcome-oriented business metrics reflecting real-world
    impact. BLEU score (A), toxicity score (B), and F1 score (D) are all
    model-quality metrics computed against datasets, not business outcome
    measures.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q12.)*

38. **B — The learning rate used during training.** Hyperparameters are
   set by a person before training begins. A, C, and D are all values the
   model itself learns during training (parameters).
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q9.)*

39. **C — Few-shot prompting supplies examples within a single prompt and
    changes nothing about the model; fine-tuning retrains the model's
    weights on labeled data.** This is the core distinction tested
    repeatedly on the exam. A reverses the two techniques' effects; B
    conflates unrelated prompting techniques; D is false since the two
    approaches have fundamentally different costs, durability, and
    mechanisms.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q12.)*

40. **B — Historical bias.** The data was collected accurately but
   reflects real-world, pre-existing societal inequities embedded in past
   decisions. Sampling bias (A) refers to unrepresentative data
   collection, not accurately-collected-but-inequitable outcomes;
   measurement bias (C) refers to systematically different data
   collection/labeling methods across groups; aggregation bias (D) refers
   to applying one model uniformly where subgroup differences matter.
   *(Source: [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), original Q7.)*

41. **C.** AWS Audit Manager is purpose-built to automatically collect evidence (including from Config and CloudTrail) and map it to a compliance framework for audit-ready reporting. Config (A) and CloudTrail (B) are underlying data sources, not the consolidated reporting tool; Macie (D) is for sensitive-data discovery.
   *(Source: [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md), original Q9.)*

42. **B — Amazon Titan Text Embeddings.** This is a Bedrock embeddings
    model purpose-built to convert text into vector embeddings for
    semantic search. AWS Trainium (A) and AWS Inferentia (C) are compute
    chips for training/inference generally, not an embeddings model
    themselves; SageMaker JumpStart (D) is a model hub/deployment tool,
    not an embeddings generator itself.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q13.)*

43. **A and B — An embeddings model to convert documents into vectors, and
    a vector database to store and query the vectors by similarity.**
    Semantic search requires generating embeddings and then searching them
    by vector similarity. Forecast (C) predicts time-series values, not
    search relevance; fine-tuning a spam classifier (D) solves a different
    problem (labeling, not retrieval); Polly (E) converts text to speech
    and has nothing to do with search.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q13.)*

44. **B — SageMaker Feature Store.** It is purpose-built as a centralized,
    versioned feature repository shared between training and inference.
    Data Wrangler (A) is for data prep/EDA; Clarify (C) is for bias and
    explainability; Model Monitor (D) tracks live model/data quality
    post-deployment.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q11.)*

45. **B — Amazon Aurora with the pgvector extension.** This lets the team
    add vector similarity search directly inside the PostgreSQL database
    they already operate, via SQL, without adopting a new dedicated
    service. Amazon Kendra (A) is a separate managed search service, not
    integrated into their existing database; AWS Trainium (C) is a
    training chip, unrelated to vector search; Bedrock Agents (D)
    orchestrates tasks, it isn't a vector store.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q14.)*

46. **B — Amazon Q Developer.** It is purpose-built for code suggestions,
    code explanation, security scanning, and natural-language Q&A about a
    user's AWS resources. Q Business (A) is a general enterprise assistant
    over company data/systems, not a coding-specific tool; Comprehend (C)
    performs text analytics, not code assistance; Textract (D) extracts
    data from scanned documents, unrelated to coding.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q14.)*

47. **B — 75%.** Recall = TP / (TP + FN) = 180 / (180 + 60) = 180/240 =
    0.75 = 75%. Option A (90%) is actually the model's *precision*
    (180/200) — a common distractor; accuracy would be (180+740)/1000 =
    92%, and option C/D do not match any of these standard formulas.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q12.)*

48. **B — Choosing a Bedrock model whose provider offers IP
   indemnification.** This directly and contractually addresses copyright
   infringement legal risk on generated content. Content filters for
   violence (A) address harmful content, not copyright; lowering
   temperature (C) reduces randomness but doesn't address legal
   copyright exposure; a Model Card (D) documents the model, it provides
   no legal protection.
   *(Source: [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), original Q9.)*

49. **C.** AWS acts as the data processor, processing personal data on the customer's behalf, while the customer (as data controller) decides the purpose and means of processing. (A) is the customer's role, not AWS's; (B) and (D) don't describe AWS's role under GDPR.
   *(Source: [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md), original Q10.)*

50. **A — Amazon Kendra.** Kendra is a fully managed enterprise search
    service that indexes connectors like SharePoint and S3 and handles
    embeddings/relevance internally, requiring no custom embeddings
    pipeline. AWS Inferentia (B) and AWS Trainium (D) are ML chips, not
    search services; Aurora with pgvector (C) still requires the team to
    generate and manage embeddings themselves, which the scenario wants
    to avoid.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q15.)*

51. **B — A foundation model is pretrained on broad data and can be
    adapted to many downstream tasks.** This is the defining
    characteristic of a foundation model. A contradicts the entire point of
    foundation models (avoiding training from scratch per task); C is
    false since multimodal foundation models exist; D is false since FMs
    can be customized via prompting, RAG, or fine-tuning.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q15.)*

52. **B — AWS Trainium.** Trainium is AWS's purpose-built chip optimized
    specifically for cost-efficient, high-performance training at scale.
    AWS Inferentia (A) is optimized for inference, not training; AWS
    Graviton (C) is a general-purpose AWS CPU, not ML-training-specific;
    AWS Nitro (D) is the underlying EC2 virtualization/security system,
    not an ML training chip.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q16.)*

53. **C — Increasing model complexity further.** Adding complexity
    increases the model's capacity to memorize noise, making overfitting
    *worse*, not better. A, B, and D are all standard, effective
    overfitting remedies.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q14.)*

54. **B — The basic unit of text, such as a word or part of a word, that
    the model processes and generates.** This is the standard definition of
    a token in LLM context. A describes an authentication credential, an
    unrelated concept that happens to share the word "token"; C describes
    a model parameter, not an input/output unit; D is unrelated to
    tokenization.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q17.)*

55. **C — The simpler model is easier to interpret and explain to
    regulators and affected individuals, which is required for this
    high-stakes, regulated decision.** This captures the correct
    performance/interpretability tradeoff reasoning for regulated,
    high-stakes decisions. A and B are not reliably true in general and
    aren't the deciding factor described in the scenario; D is false —
    simpler models can still be biased.
   *(Source: [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), original Q11.)*

56. **B.** Amazon GuardDuty performs continuous, ML-driven threat detection across an account. Macie (A) focuses specifically on sensitive-data discovery, not general threat detection; Config (C) tracks configuration compliance; Audit Manager (D) aggregates audit evidence.
   *(Source: [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md), original Q15.)*

57. **B — Amazon SageMaker JumpStart.** JumpStart provides pretrained
    foundation models and templates deployable and fine-tunable with more
    direct control over hosting than Bedrock's fully managed API.
    Guardrails (A) is a safety filter feature within Bedrock; Amazon
    Kendra (C) is an enterprise search service, unrelated to model
    hosting; Bedrock model evaluation (D) assesses model quality, it
    doesn't deploy or host models.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q18.)*

58. **B — Amazon SageMaker.** When the use case requires a fully custom
    algorithm and proprietary features not supported by any purpose-built
    managed AI service, SageMaker provides the flexibility to build,
    train, and deploy that custom model. Fraud Detector (A), Comprehend
    (C), and Personalize (D) are purpose-built services with fixed
    capabilities that don't support arbitrary custom algorithms/features.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q17.)*

59. **B — Condensing a 40-page customer contract into a one-paragraph
    summary for a reviewer.** This directly matches the summarization use
    case: compressing long content into a shorter form. Fraud detection
    (A) is a classification use case; demand prediction (C) is a
    forecasting use case; translation (D) is a distinct use case from
    summarization.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q19.)*

60. **A and B — The modality the application must support, and the
    latency requirements of the use case.** Both are core, exam-defined
    design considerations for FM applications (alongside model selection
    and cost). Region time zone offset (C), UI font (D), and marketing
    website color palette (E) are unrelated to foundation model
    application design.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q19.)*

61. **B — Data preparation / feature engineering.** Handling missing
    values and outliers is core data cleaning/preparation work that must
    happen before training, typically alongside or right after EDA.
    Monitoring (A) and deployment (C) happen after a model already
    exists; hyperparameter tuning (D) operates on the training process,
    not on fixing raw data quality issues.
   *(Source: [Domain 1: Fundamentals of AI and ML](domain-1-fundamentals-of-ai-and-ml.md), original Q19.)*

62. **C — Hallucination.** Confidently stating specific fabricated facts
    (like a nonexistent policy clause) is the textbook definition of
    hallucination. Nondeterminism (A) refers to output varying across
    runs, not fabricated content itself; overfitting (B) and underfitting
    (D) are traditional ML training diagnoses that don't describe a
    deployed generative model fabricating facts at inference time.
   *(Source: [Domain 2: Fundamentals of Generative AI](domain-2-fundamentals-of-generative-ai.md), original Q20.)*

63. **A and B — Intellectual property risk from training on or generating
    content similar to copyrighted material, and data privacy obligations
    around personal data used in training or prompts.** These are the
    legal/ethical considerations the exam associates with this domain.
    Attention heads (C) is a model architecture detail from Domain 2;
    Region selection for latency (D) and VPC subnet configuration (E) are
    infrastructure/networking concerns, not legal or ethical
    considerations.
   *(Source: [Domain 4: Guidelines for Responsible AI](domain-4-guidelines-for-responsible-ai.md), original Q14.)*

64. **B.** Config tracks resource configuration state and evaluates compliance rules over time; CloudTrail logs the underlying API call activity. (A) reverses the definitions; (C) and (D) misstate their scope and purpose.
   *(Source: [Domain 5: Security, Compliance, and Governance for AI Solutions](domain-5-security-compliance-governance.md), original Q19.)*

65. **C — Fine-tuning.** Having hundreds of labeled example
    input/output pairs and needing consistently reproduced tone/format is
    exactly the scenario fine-tuning is designed for. Prompt engineering
    alone (A) is less reliable at scale for a strict required format
    without weight updates; RAG alone (B) grounds facts in external data
    but doesn't teach a consistent output style; increasing the context
    window (D) allows more input text, but doesn't itself teach the model
    a specific tone or format.
   *(Source: [Domain 3: Applications of Foundation Models](domain-3-applications-of-foundation-models.md), original Q20.)*

---

## 6. Scoring this exam

The real AIF-C01 exam uses a **scaled score from 100–1000, with a passing
score of 700** — the scaling is nonlinear and AWS does not publish the
exact conversion, so no raw-score-to-scaled-score formula is exact.
[Section 1 of the exam preparation guide](exam-preparation-strategy.md#1-exam-format-and-time-management)
uses **≈54/65 correct (≈83%) as a rough proxy** for a passing performance,
and that's the bar to use here too:

- **58–65 correct (~89–100%):** Comfortably above the passing proxy. Do a
  light final review of any missed questions and the
  [consolidated exam traps](exam-preparation-strategy.md#4-common-exam-traps-consolidated-from-every-domains-exam-tip-callouts)
  before exam day.
- **54–57 correct (~83–88%):** Around the passing proxy. Identify which
  one or two domains contributed the most misses (use the domain citation
  in each answer) and re-read those domain guides' comparison table and
  "Exam tip" callouts before your next attempt.
- **Below 54 correct (<83%):** Below the passing proxy. Rather than
  retaking this exact mock exam again immediately, re-read the domain
  guide(s) behind your weakest area, work that domain's own 15–20
  practice questions untimed, and then retake this mock exam once you can
  explain *why* each wrong answer is wrong.

Because this mock exam reuses 65 of the ~85 total practice questions
across the series, memorizing its specific answers is not equivalent to
knowing the material — use it to rehearse pacing and domain mix, and use
each domain guide's own practice questions (and a full re-read of any weak
domain) to actually close knowledge gaps.
