Domain 5 also has a third nested "####"-level worked-example subsection,
alongside the cost-capping and shared-responsibility ones: "#### Worked
example: data encryption vs. model encryption in a multi-region HIPAA
fine-tuning pipeline," nested inside Section 1 right after its exam tip
and before the PrivateLink section. It walks Meridian Health, a
healthcare company running clinics in `us-east-1` and `us-west-2`,
through a SageMaker-to-Bedrock fine-tuning pipeline in each Region,
distinguishing the customer managed KMS key encrypting the training
data at rest (and TLS in transit) from the separate customer managed
KMS key encrypting the resulting fine-tuned model artifact, and
explaining why both are independently required — one guards PHI
confidentiality, the other guards the model as intellectual property.

Domain 5 also has a fourth nested "####"-level worked-example
subsection, nested inside the cost-governance subsection right
after the cost-capping worked example: "#### Worked example: sizing service quotas for a multi-team
Bedrock workload". It walks through inventorying
per-team RPM/TPM demand, comparing it against the Service Quotas
console limit, requesting a sized increase, and setting AWS Budgets
alert thresholds as a proactive spend backstop, contrasting with the
reactive threat-model examples above it.

Domain 5 also has a fifth nested "####"-level worked-example
subsection: "#### Worked example: tracing provenance through a Titan
Image Generator watermarking pipeline," nested inside Section 1's
"Source citation and data lineage" subsection right after its exam
tip. It traces a photo-syndication company's Titan Image Generator G1
v2 pipeline from generation through Titan's built-in invisible
watermark embedding to a newsroom fact-checker's downstream detection
of that watermark, distinguishing this provenance mechanism from the
unrelated negative-prompting technique (covered in Domains 2–3) that
excludes a visible watermark/logo from an image's rendered content.

Domain 5 also has a sixth nested "####"-level worked-example
subsection: "#### Worked example: applying differential privacy to a
healthcare model-training pipeline," nested inside the "Common security
threats to AI systems and how to mitigate them" subsection right after
its exam tip and before that subsection's mini-quiz. It walks Meridian
Health Alliance, a hospital consortium, through applying DP-SGD-style
noise injection during SageMaker training to bound how much any single
patient's record can influence a readmission-risk model, weighing the
resulting privacy-budget/accuracy trade-off, and distinguishing that
training-time protection from the KMS-based encryption-at-rest control
covered earlier in the file.

Counting every "## Worked example" heading plus the nested "###"/"####"
worked-example subsections called out above (Domain 3's
BLEU/ROUGE-significance and model-pair-comparison subsections, and its
four-techniques-on-one-task walkthrough; Domain 4's confidence-threshold/
Amazon A2I subsection; Domain 5's cost-capping, data-encryption-vs-model-encryption,
multi-team quota-sizing, SageMaker-to-Bedrock shared-responsibility, Titan Image Generator
watermarking-provenance, and differential-privacy healthcare-training
subsections), the five domain guides mark **30
worked-example sections in total**: 2 in Domain 1, 4 in Domain 2, 10 in
Domain 3, 6 in Domain 4, and 8 in Domain 5, plus further example content
nested at the sub-bullet level within some of those sections.