# Domain 5: Security, Compliance, and Governance for AI Solutions

**Exam weight: ~14%**

## Domain overview

Domain 5 tests whether you can identify the right AWS service or control to
secure an AI/ML workload, prove it meets compliance obligations, and govern
the data that feeds it. Unlike Domain 4 (which focuses on *responsible AI*
concepts like fairness and bias), Domain 5 is about the *mechanics* of
security, audit, and governance: IAM policies, encryption, network
isolation, compliance reporting, audit logging, and the shared
responsibility model.

Expect scenario questions that ask you to pick between look-alike services
(AWS CloudTrail vs. AWS Config vs. AWS Audit Manager is a classic trio), to
identify which party — AWS or the customer — owns a given security task, and
to recognize which AWS feature provides transparency (citations, lineage)
into how a generative AI system produced an answer. This domain matters on
the exam and in practice because generative AI systems introduce new risks
— sensitive data flowing into prompts, model outputs that need to be
traceable, and regulatory obligations (GDPR, HIPAA) that don't disappear
just because a foundation model is involved.

---

## 1. Securing AI systems

### IAM roles and policies for AI services

AWS Identity and Access Management (IAM) controls *who* (or *what*) can call
an AI service and *what* they're allowed to do. For AI workloads this shows
up in two common forms:

- **Identity-based policies** attached to IAM users, groups, or roles that
  grant permissions such as `bedrock:InvokeModel` or
  `sagemaker:CreateTrainingJob`.
- **IAM service roles** that a service assumes on your behalf — for
  example, an Amazon SageMaker execution role that lets a training job read
  training data from Amazon S3 and write model artifacts back, or a Bedrock
  service role that lets Amazon Bedrock Knowledge Bases read from an S3
  data source.

The guiding principle is **least privilege**: grant only the specific
actions and resources a role needs (e.g., scope an S3 permission to a
single bucket/prefix rather than `s3:*` on `*`). Resource-based policies
(such as an S3 bucket policy or a Bedrock model resource policy) can add a
second layer of control, and condition keys can restrict access further
(e.g., by VPC endpoint, source IP, or encryption requirement).

**Example:** A SageMaker notebook needs an execution role scoped to read
only from `s3://company-training-data/project-x/*` and to publish metrics
to Amazon CloudWatch — not broad S3 or CloudWatch access across the
account.

> **Exam tip:** If a question describes a service (SageMaker, Bedrock,
> Comprehend, etc.) that needs to act on other AWS resources, the answer is
> almost always "attach an IAM role with least-privilege permissions to the
> service," not "use the caller's IAM user credentials."

### Data encryption at rest and in transit

- **At rest**: AWS Key Management Service (AWS KMS) integrates with
  SageMaker, Bedrock, and S3 to encrypt training data, model artifacts, and
  logs using AWS managed keys or customer managed keys (CMKs). S3
  server-side encryption (SSE-S3, SSE-KMS) protects data stored for
  training or retrieval-augmented generation (RAG).
- **In transit**: TLS encrypts data moving between clients and AWS AI
  service endpoints (e.g., calls to the Bedrock or SageMaker runtime API),
  and between components inside a VPC when configured.
- Amazon Bedrock encrypts data at rest and in transit by default, and lets
  you supply your own CMK for additional control over prompts, model
  customization jobs, and knowledge base data.
- SageMaker lets you attach a KMS key to notebook instance storage,
  training job output, and endpoints for encryption at rest.

**Example:** A company fine-tuning a foundation model in Bedrock supplies a
customer managed KMS key so it retains full control (including the ability
to revoke access) over the encryption key protecting its fine-tuning
dataset and resulting custom model.

> **Exam tip:** "Encryption at rest" protects stored data (S3, EBS, model
> artifacts); "encryption in transit" protects data moving over the network
> (TLS/HTTPS). A question describing data "moving between a client
> application and an API" is testing in-transit encryption, not at-rest.

### AWS PrivateLink and VPC endpoints for AI services

By default, calls to AWS AI service APIs (SageMaker, Bedrock, Comprehend,
etc.) travel over the public internet (though still encrypted via TLS).
**AWS PrivateLink** lets you create an **interface VPC endpoint** so that
traffic between your VPC and the AI service stays entirely on the AWS
network, never traversing the public internet. This is important for
workloads with strict data-exfiltration or compliance requirements.

**Example:** A healthcare company running inference against Amazon
Comprehend Medical from a private subnet with no internet gateway creates a
VPC endpoint (powered by PrivateLink) for Comprehend Medical so the private
subnet can reach the service without adding a NAT gateway or internet
route.

> **Exam tip:** If a scenario emphasizes "traffic must not traverse the
> public internet" or "resources are in a private subnet with no internet
> access," the answer is a VPC endpoint / AWS PrivateLink — not a NAT
> gateway (NAT gateways still egress to the public internet) and not a VPN.

### Source citation and data lineage

For generative AI, **transparency about where an answer came from** is a
governance requirement, not just a nice-to-have:

- **Amazon Bedrock Knowledge Bases** (used for RAG) can return **citations**
  alongside a generated response, pointing back to the specific source
  document chunks used to ground the answer — improving trust and
  auditability.
- **Amazon SageMaker ML Lineage Tracking** automatically (and manually)
  records the lineage of an ML workflow — which datasets, code, and
  parameters produced a given trained model — so you can trace a deployed
  model back to its origins.
- **Amazon SageMaker Model Cards** document a model's intended use,
  training data, evaluation results, and risk considerations in a single
  structured artifact, supporting governance and audit.

**Example:** A RAG-based customer support chatbot built on Bedrock
Knowledge Bases returns not just an answer but the specific knowledge-base
document and page it drew from, letting a reviewer verify the answer's
accuracy.

> **Exam tip:** "Citations" answer *what source grounded this specific
> generated response* (RAG/Knowledge Bases); "lineage" answers *what
> data/code produced this model* (SageMaker ML Lineage Tracking). Don't mix
> them up on scenario questions.

---

## 2. AWS compliance standards relevant to AI workloads

### AWS Artifact

**AWS Artifact** is a self-service portal for on-demand access to AWS's
compliance reports (e.g., SOC 1/2/3, ISO certifications, PCI DSS) and for
reviewing and accepting agreements such as the AWS Business Associate
Addendum (BAA) for HIPAA-eligible workloads. It's how you obtain *evidence*
that AWS's infrastructure meets a given compliance standard.

**Example:** A compliance officer needs proof that AWS data centers hosting
a company's SageMaker workloads are ISO 27001 certified — they download the
relevant report from AWS Artifact rather than requesting an audit of AWS
directly.

> **Exam tip:** AWS Artifact provides AWS's own compliance *documentation*
> — it does not automatically make your workload compliant. Your
> application, data handling, and configuration choices still have to meet
> the standard; AWS Artifact only proves AWS's side (infrastructure) of the
> shared responsibility model.

### Relevant regulations: GDPR and HIPAA (conceptual)

- **GDPR** (General Data Protection Regulation, EU): governs processing of
  personal data of EU individuals — requiring things like data minimization,
  the right to erasure, and control over where/how data is processed and
  transferred. For AI workloads, this affects decisions like which AWS
  Region hosts training/inference data and how long personal data used in
  prompts or training sets is retained.
- **HIPAA** (Health Insurance Portability and Accountability Act, US):
  governs protected health information (PHI). To use AWS services with
  PHI, an organization must sign a **Business Associate Addendum (BAA)**
  with AWS (available via AWS Artifact) and use only HIPAA-eligible
  services configured appropriately (encryption, access controls, audit
  logging).

The exam does not require legal expertise — it tests whether you know these
regulations exist, roughly what they protect (personal data / health data),
and that **using AWS does not automatically make you compliant**: the
customer is responsible for how they configure and use AWS services to meet
these regulations.

**Example:** A hospital wants to build a clinical-notes summarization tool
using Amazon Bedrock. Before processing any PHI, it must confirm Bedrock is
covered under its AWS BAA and that the workload is architected (encryption,
logging, access control) to meet HIPAA requirements.

> **Exam tip:** Signing a BAA or downloading a report from AWS Artifact is
> a *prerequisite*, not a guarantee — compliance is a shared responsibility.
> A question implying "since we use AWS, we're automatically GDPR/HIPAA
> compliant" describes a wrong answer.

---

## 3. AWS Config, AWS Audit Manager, and AWS CloudTrail for AI governance and audit trails

These three services are frequently confused because they all relate to
"governance," but they answer different questions:

| Service | Answers the question |
|---|---|
| AWS CloudTrail | "Who did what, and when?" (API activity log) |
| AWS Config | "What is my resource's configuration right now, and has it drifted from what's allowed?" |
| AWS Audit Manager | "Can I continuously collect evidence that I meet a compliance framework?" |

- **AWS CloudTrail** logs API calls made across your account, including
  calls to AI services. This creates an audit trail of *who invoked what,
  when, and from where*.
- **AWS Config** continuously records and evaluates the *configuration* of
  your AWS resources against rules you define (or managed rules), flagging
  configuration drift or non-compliant resources.
- **AWS Audit Manager** continuously collects evidence (often pulling from
  CloudTrail and Config) and maps it to the controls of a chosen framework
  (e.g., a custom framework or one aligned to GDPR/HIPAA-style controls),
  streamlining audit preparation.

**Examples:**
- CloudTrail: Logging every `bedrock:InvokeModel` and
  `sagemaker:CreateEndpoint` API call, including the calling principal and
  source IP, to investigate who generated a specific model output.
- Config: A Config rule that checks whether every SageMaker notebook
  instance has encryption enabled, and automatically flags (or triggers
  remediation for) any that don't.
- Audit Manager: Running a continuous assessment that gathers evidence
  (CloudTrail logs, Config rule results, IAM policy snapshots) to
  demonstrate an AI system's controls for an upcoming compliance audit.

> **Exam tip:** The classic exam trap: a scenario says "we need to know
> which user invoked a model" → CloudTrail. "We need to know if our
> SageMaker resources are configured per policy" → Config. "We need to
> continuously assemble audit-ready evidence for a compliance review" →
> Audit Manager. Match the verb (log / evaluate configuration / assemble
> evidence) to the service.

---

## 4. Data governance strategies

Good data governance for AI workloads spans the full lifecycle of the data
that trains and feeds models.

### Data lifecycle

Covers classification (what kind of data is it — public, confidential,
PII?), retention (how long is it kept), and deletion (secure disposal when
no longer needed). AI-specific concerns include how long prompts/outputs
are retained, and whether training data used to fine-tune a model needs to
be deleted or the model retrained if source data is deleted (a "right to
erasure" concern).

**Example:** An S3 Lifecycle policy automatically transitions raw training
data to S3 Glacier after 90 days and expires (deletes) it after the
retention period required by policy, reducing exposure of stale sensitive
data.

### Data residency

Where data physically lives and is processed. AWS Regions let you choose
where training data, fine-tuning data, and inference requests are stored
and processed, which matters for regulations that restrict cross-border
transfer of personal data (a GDPR concern) or that require in-country
processing (data sovereignty).

**Example:** An EU-based company configures its SageMaker training jobs and
Bedrock model access to run exclusively in an EU Region (e.g.,
`eu-central-1`) to keep personal data within the EU.

### Data monitoring

Ongoing visibility into how sensitive data is accessed and used.

- **Amazon Macie** uses machine learning to automatically discover and
  classify sensitive data (like PII) in S3, alerting when sensitive data is
  exposed or accessed unexpectedly — useful for auditing datasets before
  they're used to train or fine-tune a model.
- **CloudTrail and Amazon CloudWatch** together monitor and alert on access
  patterns to AI resources and data stores.

**Example:** Before using a customer-support ticket archive in S3 to
fine-tune a model, a team runs Amazon Macie to scan the bucket and discover
that it contains unredacted credit card numbers, prompting remediation
before training.

> **Exam tip:** Amazon Macie is specifically about *discovering and
> classifying sensitive data* (especially PII) in S3 — if a question is
> about finding PII in a data lake before it's used for training, Macie is
> almost always the intended answer, not CloudTrail or Config.

---

## 5. AWS shared responsibility model applied to AI/ML services

AWS's shared responsibility model splits security duties into:

- **Security *of* the cloud** (AWS's responsibility): the physical
  infrastructure, host operating system, virtualization layer, and the
  managed service software itself (e.g., patching the underlying
  infrastructure that runs Bedrock).
- **Security *in* the cloud** (customer's responsibility): how you
  configure and use the service — IAM permissions, data classification,
  encryption key management choices, network configuration, and the
  content/data you send to the service.

Where the line falls **shifts based on the abstraction level** of the
service:

- **Infrastructure-as-a-service-like components** (e.g., a SageMaker
  notebook instance backed by an EC2 instance you manage more directly):
  the customer has more responsibility — patching within the instance,
  configuring the instance's security group, managing the IAM role
  attached, etc.
- **Fully managed / serverless services** (e.g., Amazon Bedrock,
  SageMaker's fully managed training/hosting infrastructure): AWS takes on
  more of the operational and infrastructure burden, but the customer is
  still always responsible for IAM configuration, data they submit, and
  how outputs are used.

**Example:** For Amazon Bedrock, AWS is responsible for securing and
patching the underlying foundation model hosting infrastructure; the
customer is responsible for controlling which IAM principals can call
Bedrock, what data is sent in prompts, and whether that data should be
encrypted with a customer managed key.

> **Exam tip:** No matter how "managed" an AWS AI service is, the customer
> is **always** responsible for IAM/access configuration and the data they
> put into the service. A question implying "AWS is fully responsible for
> our data's security once it's in a managed AI service" is describing a
> wrong answer.

---

## Comparison table

| Service | Primary purpose | What it answers | Example AI use case |
|---|---|---|---|
| AWS CloudTrail | Logs API activity across the account | "Who called this API, when, and from where?" | Auditing who invoked `bedrock:InvokeModel` for a sensitive prompt |
| AWS Config | Tracks and evaluates resource configuration over time | "Is this resource configured correctly, and did it drift?" | Flagging a SageMaker notebook instance that isn't encrypted |
| AWS Audit Manager | Continuously collects evidence mapped to a compliance framework | "Can I prove, with evidence, that we meet this framework's controls?" | Assembling evidence for an internal review of an AI system's controls |
| AWS Artifact | On-demand access to AWS compliance reports and agreements | "What compliance certifications does AWS's infrastructure hold, and can I get a BAA?" | Downloading an ISO 27001 report or signing a HIPAA BAA before processing PHI in Bedrock |
| Amazon Macie | Discovers and classifies sensitive data in S3 using ML | "Where is sensitive/PII data, and is it exposed?" | Scanning a training data bucket for unredacted PII before fine-tuning |

---

## Key terms

- **IAM role/policy** — An IAM role is an identity that AWS services or
  users can assume; an IAM policy is a JSON document defining permitted or
  denied actions/resources.
- **AWS KMS (Key Management Service)** — Managed service for creating and
  controlling encryption keys used to protect data at rest.
- **Encryption at rest** — Protecting stored data (e.g., in S3, EBS, model
  artifacts) from unauthorized access.
- **Encryption in transit** — Protecting data as it moves across a network,
  typically via TLS.
- **AWS PrivateLink** — Technology enabling private connectivity between
  VPCs and AWS services without traversing the public internet.
- **VPC endpoint** — An interface (via PrivateLink) or gateway that lets
  resources in a VPC privately reach an AWS service.
- **Data lineage** — A record of the data, code, and parameters that
  produced a given model or dataset, enabling traceability.
- **AWS Artifact** — Self-service portal for AWS compliance reports and
  agreements (e.g., BAA).
- **GDPR** — EU regulation governing the processing and protection of
  personal data.
- **HIPAA** — US regulation governing protected health information (PHI).
- **AWS Config** — Service that records and evaluates AWS resource
  configurations against defined rules.
- **AWS Audit Manager** — Service that continuously collects evidence to
  simplify assessing compliance with frameworks.
- **AWS CloudTrail** — Service that logs and monitors API activity across
  an AWS account.
- **Data residency** — Where data is physically stored/processed,
  relevant to legal and regulatory requirements.
- **Data sovereignty** — The principle that data is subject to the laws of
  the country in which it is collected or stored.
- **Amazon Macie** — ML-powered service that discovers and classifies
  sensitive data (e.g., PII) stored in Amazon S3.
- **Shared responsibility model** — The division of security duties between
  AWS ("security of the cloud") and the customer ("security in the
  cloud").

---

## Practice questions

1. A company wants its Amazon SageMaker training job to read data from a
   specific S3 bucket and write model artifacts back to that same bucket,
   with no other AWS access. What should the company do?
   A. Use the account root user's credentials in the training job
   B. Create an IAM role with least-privilege permissions scoped to that S3 bucket and attach it as the SageMaker execution role
   C. Grant `s3:*` permissions on all buckets to the SageMaker service
   D. Disable IAM entirely for the training job

2. A financial services firm must ensure that data sent to Amazon Bedrock
   is encrypted at rest using a key the firm fully controls and can revoke.
   What should they use?
   A. The AWS managed default encryption with no configuration
   B. A customer managed key (CMK) in AWS KMS supplied to Bedrock
   C. TLS termination at a load balancer
   D. S3 bucket versioning

3. Which AWS feature ensures that traffic between a private VPC subnet
   (with no internet gateway) and Amazon SageMaker API endpoints never
   traverses the public internet?
   A. A NAT gateway
   B. An internet gateway
   C. An interface VPC endpoint powered by AWS PrivateLink
   D. A Site-to-Site VPN

4. A company builds a RAG-based chatbot using Amazon Bedrock Knowledge
   Bases and wants each answer to reference the exact source document it
   was generated from. Which capability provides this?
   A. AWS CloudTrail logs
   B. Citations returned by Bedrock Knowledge Bases
   C. AWS Config rules
   D. Amazon Macie findings

5. Which AWS capability lets a data science team trace a deployed
   SageMaker model back to the exact dataset, code, and parameters that
   produced it?
   A. SageMaker ML Lineage Tracking
   B. AWS Artifact
   C. Amazon Comprehend
   D. AWS Audit Manager

6. A compliance team needs to obtain AWS's SOC 2 report to satisfy an
   internal audit of their AI infrastructure provider. Where should they
   go?
   A. AWS CloudTrail
   B. AWS Artifact
   C. AWS Config
   D. Amazon Macie

7. A hospital plans to process protected health information (PHI) using
   Amazon Bedrock. Before doing so, what must they do regarding HIPAA?
   A. Nothing — AWS is automatically HIPAA compliant for all services
   B. Sign an AWS Business Associate Addendum (BAA), available via AWS Artifact, and use eligible services appropriately
   C. Wait for AWS to notify them that HIPAA compliance is enabled
   D. Only use Amazon S3, since HIPAA does not apply to AI services
   
8. (Select TWO) Which statements correctly describe the customer's
   responsibility under the AWS shared responsibility model when using a
   fully managed AI service like Amazon Bedrock?
   A. The customer is responsible for patching the physical servers hosting the foundation models
   B. The customer is responsible for configuring IAM permissions controlling who can invoke the model
   C. The customer is responsible for the data they submit in prompts and how outputs are used
   D. AWS is responsible for all data governance decisions once data is submitted
   E. The customer is responsible for the physical security of the AWS data center

9. A security team wants to know exactly which IAM principal called the
   `bedrock:InvokeModel` API, from which IP address, and at what time.
   Which service provides this?
   A. AWS Config
   B. AWS CloudTrail
   C. AWS Audit Manager
   D. Amazon Macie

10. A governance team wants an automated rule that continuously checks
    whether every SageMaker notebook instance has encryption enabled, and
    flags any that don't. Which service should they use?
    A. AWS CloudTrail
    B. AWS Config
    C. AWS Artifact
    D. Amazon Macie

11. An internal audit team needs to continuously gather evidence — pulling
    from CloudTrail logs and Config rule evaluations — mapped to a
    compliance framework, to prepare for an upcoming external audit.
    Which service is purpose-built for this?
    A. AWS Audit Manager
    B. AWS CloudTrail
    C. AWS Artifact
    D. Amazon Macie

12. Before a team fine-tunes a foundation model using an archive of
    customer support tickets stored in S3, they want to automatically
    discover whether the archive contains unredacted PII such as credit
    card numbers. Which service should they use?
    A. AWS Config
    B. Amazon Macie
    C. AWS CloudTrail
    D. AWS Artifact

13. A company operating in the EU must ensure that personal data used to
    train and run inference on its models never leaves the EU. Which
    strategy directly addresses this requirement?
    A. Enabling S3 versioning
    B. Selecting an EU AWS Region for training and inference and restricting processing to it
    C. Enabling AWS CloudTrail
    D. Using Amazon Macie

14. Which of the following is an example of a data lifecycle governance
    control?
    A. An S3 Lifecycle policy that transitions data to S3 Glacier after 90 days and deletes it after the retention period expires
    B. An IAM policy granting SageMaker access to S3
    C. A VPC endpoint for SageMaker
    D. A Bedrock Knowledge Base citation

15. What is the key difference between "encryption at rest" and
    "encryption in transit"?
    A. There is no difference — they are the same control
    B. Encryption at rest protects stored data; encryption in transit protects data moving over a network
    C. Encryption at rest only applies to Amazon S3
    D. Encryption in transit is optional and never required by AWS AI services

16. A retail company signs up for AWS Artifact and downloads several
    compliance reports for the AWS infrastructure underlying its SageMaker
    workloads. Does this alone make the company's AI application GDPR
    compliant?
    A. Yes, downloading the reports guarantees full compliance
    B. No — compliance is shared; the company must still configure its own application, data handling, and access controls appropriately
    C. Yes, but only for workloads in the us-east-1 Region
    D. No, AWS Artifact reports are irrelevant to compliance

17. (Select TWO) Which of the following are valid uses of AWS PrivateLink /
    VPC endpoints in an AI workload?
    A. Allowing a private subnet to call the SageMaker Runtime API without traversing the public internet
    B. Allowing a private subnet to call the Amazon Bedrock Runtime API without traversing the public internet
    C. Automatically encrypting all data stored in S3
    D. Automatically classifying PII in a dataset
    E. Replacing the need for IAM entirely

18. A machine learning engineer wants to document a deployed model's
    intended use, training data summary, evaluation metrics, and known
    limitations in a single structured artifact for governance purposes.
    Which SageMaker feature is designed for this?
    A. SageMaker Model Cards
    B. SageMaker Ground Truth
    C. SageMaker Studio
    D. SageMaker JumpStart

19. Which statement best describes the difference between AWS Config and
    AWS CloudTrail?
    A. They are interchangeable and serve the same purpose
    B. AWS Config evaluates resource configuration/compliance over time; AWS CloudTrail logs API call activity
    C. AWS Config logs API calls; AWS CloudTrail evaluates resource configuration
    D. Both only apply to Amazon EC2 resources

20. Under the shared responsibility model, who is responsible for ensuring
    that IAM permissions granted to a data science team follow the
    principle of least privilege?
    A. AWS is solely responsible
    B. The customer is responsible, regardless of how managed the AI service is
    C. Responsibility is randomly assigned per Region
    D. No one is responsible for IAM configuration in managed services

---

## Answer key

1. **B** — Least-privilege IAM roles scoped to the exact resource are the standard secure pattern for service access. A (root credentials) and C (wildcard access) violate least privilege; D is not a valid or secure option.
2. **B** — A customer managed KMS key gives the customer control over key policy and revocation. A doesn't meet "fully controls/can revoke"; C only protects data in transit, not at rest; D (versioning) is unrelated to encryption.
3. **C** — An interface VPC endpoint via AWS PrivateLink keeps traffic on the AWS network. A NAT gateway (A) and VPN (D) still ultimately touch the internet path or aren't designed for this; an internet gateway (B) directly exposes the subnet to the internet, the opposite of the goal.
4. **B** — Citations from Bedrock Knowledge Bases link a generated answer back to its source document chunks. CloudTrail (A) logs API calls, not content sources; Config (C) is for resource configuration; Macie (D) finds sensitive data, unrelated to citations.
5. **A** — SageMaker ML Lineage Tracking is purpose-built to trace a model back to the data/code/parameters that produced it. AWS Artifact (B) provides compliance reports; Comprehend (C) is an NLP service; Audit Manager (D) collects compliance evidence, not ML lineage.
6. **B** — AWS Artifact is the self-service portal for AWS's compliance reports like SOC 2. CloudTrail (A) and Config (C) are operational/audit services, not report repositories; Macie (D) finds sensitive data.
7. **B** — HIPAA workloads require a signed BAA (obtained via AWS Artifact) and use of eligible services configured correctly. A and C incorrectly imply automatic compliance; D incorrectly restricts HIPAA-eligible services to only S3.
8. **B, C** — The customer always configures IAM and controls the data/outputs they send/use, even with fully managed services. A and E describe AWS's responsibilities (physical infrastructure/data center security), and D is false — data governance remains a shared/customer responsibility.
9. **B** — AWS CloudTrail logs API-level activity including caller identity, source IP, and timestamp. Config (A) tracks configuration state, not who called an API; Audit Manager (C) aggregates evidence; Macie (D) is for sensitive data discovery.
10. **B** — AWS Config continuously evaluates resource configuration against rules (like "encryption enabled"). CloudTrail (A) logs activity, not configuration state; Artifact (C) provides reports; Macie (D) is for data discovery, not resource configuration.
11. **A** — AWS Audit Manager is designed to continuously collect evidence mapped to a compliance framework, often using CloudTrail/Config as inputs. CloudTrail (B) and Config (C) are underlying data sources, not the framework-mapping/evidence-assembly tool itself; Artifact (D) provides AWS's own reports, not evidence about your account.
12. **B** — Amazon Macie uses ML to discover and classify sensitive data like PII/credit card numbers in S3. Config (A) and CloudTrail (C) don't inspect data content; Artifact (D) provides compliance documents, not data scanning.
13. **B** — Choosing an EU Region and restricting processing to it directly controls data residency. Versioning (A) and CloudTrail (C) don't affect where data is processed; Macie (D) finds sensitive data but doesn't control residency.
14. **A** — Lifecycle policies governing retention/transition/deletion are the definition of data lifecycle management. B and C are access/network controls; D is a RAG transparency feature, not a lifecycle control.
15. **B** — At-rest protects stored data; in-transit protects data moving over a network — they are distinct controls addressing different states of data. A is false (they differ); C is false (at-rest applies broadly, not only S3); D is false (many AWS AI services enforce TLS by default).
16. **B** — Compliance is shared: AWS Artifact proves AWS's infrastructure meets certain standards, but the customer must still configure their own application and data handling correctly. A and C overstate what Artifact guarantees; D understates its relevance (it's a necessary but not sufficient piece of evidence).
17. **A, B** — VPC endpoints/PrivateLink support private connectivity to both SageMaker and Bedrock runtime APIs. C (encryption) and D (PII classification) are unrelated capabilities (KMS and Macie respectively), and E is false — PrivateLink doesn't replace IAM authorization.
18. **A** — SageMaker Model Cards are specifically designed to document intended use, training data, metrics, and limitations in one governance artifact. Ground Truth (B) is for data labeling, Studio (C) is the IDE, and JumpStart (D) is a model/solution hub — none document governance metadata this way.
19. **B** — Config evaluates and tracks configuration/compliance state over time; CloudTrail logs discrete API call events. A is false since they serve different purposes; C reverses their roles; D is false — both apply broadly across many resource/service types, not just EC2.
20. **B** — Under the shared responsibility model, IAM configuration ("security in the cloud") is always the customer's responsibility, no matter how managed the underlying AI service is. A, C, and D all incorrectly remove or obscure the customer's ownership of access configuration.
