# Domain 5 Fast Track / Ultra Fast Learn: coverage verification report

**Status:** technical verification complete · **Verified:** 2026-09-09

## What this report is

`docs/DOCUMENTATION_STRUCTURE.md` states a coverage guarantee for every
domain's condensed layer: "every testable concept the full domain guide
covers is retained somewhere in the condensed layer — only narrative
explanation, extra worked examples, and repetition are cut, not
exam-relevant content." For Domain 5 specifically, that guarantee had not
been technically verified — it was flagged in the Content Health
assessment as a claim requiring spot-check against the source material.
This report is that spot-check, covering both condensation hops: the full
guide down to the two-part Fast Track, and the Fast Track down to the
further-condensed `ULTRA-FAST-LEARN.md` cram sheet.

Three major sections of
[`docs/domain-5-security-compliance-governance.md`](../domain-5-security-compliance-governance.md)
(2,853 lines) were compared line-by-line against
[`docs/domain-5-fast-track/README.md`](README.md),
[`part-1-security-and-compliance.md`](part-1-security-and-compliance.md),
and [`part-2-governance-and-monitoring.md`](part-2-governance-and-monitoring.md)
(1,491 lines combined), and then against
[`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md), confirming whether every
exam-relevant fact, decision criterion, AWS service, metric, and concept
survives both condensation hops.

This is a correctness audit, not new content authoring: it documents what
was checked, what verified clean, and where a real gap was found. It does
not itself change `README.md`, `part-1-security-and-compliance.md`,
`part-2-governance-and-monitoring.md`, or `ULTRA-FAST-LEARN.md`.

## Sections spot-checked

| # | Full guide section | Fast Track section | Ultra Fast Learn section |
|---|---|---|---|
| 1 | [§1 Securing AI systems](../domain-5-security-compliance-governance.md#1-securing-ai-systems) (line 56) — IAM, encryption, PrivateLink, source citation/lineage, the [security-threat catalog](../domain-5-security-compliance-governance.md#common-security-threats-to-ai-systems-and-how-to-mitigate-them) (line 361), cost governance, and [MITRE ATLAS/OWASP](../domain-5-security-compliance-governance.md#security-frameworks-for-ai-systems-mitre-atlas-and-owasp-top-10-for-llm-applications) (line 1017) | [part-1 §§1–7](part-1-security-and-compliance.md#1-iam-roles-and-policies-for-ai-services) | [§§2–5](ULTRA-FAST-LEARN.md#3-iam-patterns) |
| 2 | [§2 AWS compliance standards relevant to AI workloads](../domain-5-security-compliance-governance.md#2-aws-compliance-standards-relevant-to-ai-workloads) (line 1135) — AWS Artifact, the five compliance frameworks ([GDPR](../domain-5-security-compliance-governance.md#gdpr-general-data-protection-regulation--conceptual-level) through [ISO/IEC 42001 and the Algorithmic Accountability Act](../domain-5-security-compliance-governance.md#isoiec-42001-and-the-algorithmic-accountability-act--conceptual-level)), both comparison matrices | [part-1 §§8–11](part-1-security-and-compliance.md#8-aws-artifact-reports-vs-agreements) | [§1](ULTRA-FAST-LEARN.md#1-five-compliance-frameworks-side-by-side) |
| 3 | [§§3–5](../domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance) — AWS Config, AWS Audit Manager, and AWS CloudTrail; data governance strategies; shared responsibility; both cross-cutting worked examples (Meridian Lending SOC 2, Aurora Benefits hallucination drift, and the [multi-region GDPR/HIPAA/NIST AI RMF worked example](../domain-5-security-compliance-governance.md#worked-example-a-multi-region-bedrock-and-sagemaker-deployment-under-gdpr-hipaa-and-the-nist-ai-rmf)) (lines 1654–2853) | [part-2 §§1–4](part-2-governance-and-monitoring.md#1-aws-config-aws-audit-manager-and-aws-cloudtrail) | [§6](ULTRA-FAST-LEARN.md#6-shared-responsibility-model) |

## Result: Fast Track (full guide → Fast Track hop)

**Verified clean, with four narrow exceptions.** Across all three sections
above, essentially every exam-relevant fact, decision criterion, AWS
service, metric, and named constraint in the full guide is present in the
Fast Track, condensed to tables, flowcharts, and shortened exam tips. In
particular: all 10 named security-threat categories with their specific
AWS-service mitigations, IAM Access Analyzer, the KMS key-rotation
behavior and data-vs-model CMK distinction, differential privacy
(DP-SGD, epsilon), Titan Image Generator watermarking, MITRE ATLAS and the
OWASP Top 10 for LLM Applications, AWS Artifact's Reports-vs-Agreements
split, all five compliance frameworks with both comparison matrices, the
full Config/Audit Manager/CloudTrail purpose distinctions, the
Bedrock-vs-SageMaker shared-responsibility split, and both comparison
tables in §§3–5 all survive intact. However, four specific, named facts
were confirmed absent (via `grep`) from the entire `domain-5-fast-track/`
directory — i.e. dropped from `README.md`, `part-1`, `part-2`, *and*
`ULTRA-FAST-LEARN.md` alike:

1. **GDPR's "right to erasure" and "data minimization"** (full guide line
   1206: "Concepts like the right to erasure and data minimization matter
   for AI training data pipelines... ensuring a person's data can be
   removed from a dataset and any downstream retrained model", reused in
   the Northfield worked example at line 2451). Neither term appears
   anywhere in the Fast Track's GDPR treatment — only data
   controller/processor roles, residency, and Article 22 human-review (a
   distinct right) survive.
2. **GDPR's "special category" data classification** (full guide line
   2371: `genetic data is a GDPR "special category"`). The term "special
   category" does not appear anywhere in the Fast Track.
3. **"SOC 2 Type II" as the specific audit type** (full guide lines 1804,
   1845, 1856, the Meridian Lending worked example). The Fast Track
   mentions "SOC 2" generically, but the Type I vs. Type II distinction —
   the actual testable fact — never appears; there is no standalone
   condensed takeaway for the Meridian Lending worked example the way
   the Aurora Benefits and multi-region worked examples both got.
4. **Aurora Benefits' named hallucination-drift metrics** (full guide line
   2018: the custom CloudWatch metric names `HallucinationRate` and
   `FactualConsistencyScore`, metric namespace `RAGAssistant/Quality`, and
   the specific alarm thresholds — warn at 4%, page at 6%, baseline 2%).
   The Fast Track's condensed version keeps the 2%→8% drift narrative and
   "custom CloudWatch metric with alarm thresholds" generically, but drops
   the named metrics, namespace, and threshold values entirely.

A few lower-materiality service names were also observed dropped from
worked-example asides that the Fast Track condenses to one-line
takeaways — **AWS Trusted Advisor**, **AWS Budgets**, **Amazon SNS**, and
**Amazon ElastiCache** (each named once in a full-guide cost-governance or
latency worked example), plus the AWS Artifact agreement-acceptance
mechanics (accepting from the Organizations management account;
verifying via the Agreements page's Active status/acceptance date). These
are single throwaway details inside examples rather than standalone
testable facts, so they are noted here for completeness but not encoded
as pinned test assertions below.

## Result: Ultra Fast Learn (Fast Track → Ultra Fast Learn hop)

**Five coverage gaps found.** `ULTRA-FAST-LEARN.md` is deliberately far
more compressed than the two-part Fast Track, and that additional trim is
expected. However, the following are named, testable AWS
services/concepts present in the Fast Track — confirmed absent entirely
from `ULTRA-FAST-LEARN.md`, not merged under a different heading:

1. **"Insecure output handling"** as a named threat category. Present in
   part-1's threat table (line 231) and rapid-fire terms (line 555).
   `ULTRA-FAST-LEARN.md` §5 "Incident-response steps" (lines 107–140) is
   the file's threat-category list and names 9 of the 10 threats but
   skips this one.
2. **MITRE ATLAS and OWASP Top 10 for LLM Applications.** A full section
   in part-1 (`## 7. Security frameworks: MITRE ATLAS and OWASP Top 10`,
   lines 317–341, plus rapid-fire terms and mini-quiz entries). Neither
   framework name appears anywhere in `ULTRA-FAST-LEARN.md`, despite its
   own intro claiming to condense the full guide's Sections 1, 2, and 5.
3. **Amazon Macie.** Present in part-1 (prompt-injection/sensitive-
   information-disclosure mitigations, lines 228 and 234) and as its own
   table row, decision callout, and mini-quiz answer in part-2 (lines
   119, 153, 333, 366, 381, 400, 451). Never named in
   `ULTRA-FAST-LEARN.md`.
4. **Titan Image Generator watermarking / provenance detection.**
   Part-1's `## 4. Source citation and data lineage` (line 192) covers
   this as its own "Provenance watermarking" table row (line 198), with a
   dedicated disambiguation callout distinguishing it from the Domain
   2/3 "visible logo" watermark. Both "Titan" and "watermark" as terms
   are absent from `ULTRA-FAST-LEARN.md`.
5. **Algorithmic Accountability Act.** Named in both part-1 (lines 387,
   444, 589, mini-quiz line 653) and part-2's comparison table (line
   351). `ULTRA-FAST-LEARN.md` §1's "Five compliance frameworks" table
   names only GDPR, HIPAA, NIST AI RMF, EU AI Act, and ISO/IEC 42001 —
   the sixth, proposed regulation is dropped entirely.

One further partial gap is worth noting in prose, though it does not rise
to a strict test assertion below since it is a 3-of-4 partial match on a
common English word: the NIST AI RMF's four named functions are
**Govern, Map, Measure, Manage** (part-1 lines 383/584, part-2 line 349
name all four); `ULTRA-FAST-LEARN.md` line 42's requirements table names
"Govern," "Measure," and "Manage" but never "Map."

## Recommendation

Backfill the five Hop-2 items into `ULTRA-FAST-LEARN.md` (condensed
bullets/table rows only, sourced verbatim from part-1/part-2, no new
facts to author): add "insecure output handling" to §5's threat list; add
a short MITRE ATLAS / OWASP Top 10 row or bullet (§1 or a new section);
name Amazon Macie alongside the existing PrivateLink/incident-response
services it already covers; add a one-line Titan Image Generator
watermarking bullet; and add the Algorithmic Accountability Act as a
sixth row (or footnote) in §1's compliance-frameworks table.

Separately, backfill the four Hop-1 items into `part-1-security-and-
compliance.md` / `part-2-governance-and-monitoring.md` (sourced verbatim
from the full guide): GDPR's right-to-erasure/data-minimization concepts
in §9; the "special category" term in the same section; "Type II" added
to the existing SOC 2 mentions, or a one-line Meridian Lending takeaway
matching the Aurora Benefits and multi-region worked examples' treatment;
and the named `HallucinationRate`/`FactualConsistencyScore` metrics and
thresholds in part-2's condensed Aurora Benefits takeaway.

Each addition should also extend `tests/test_domain_5_ultra_fast_learn.py`
and/or `tests/test_domain_5_fast_track_part_1.py` /
`test_domain_5_fast_track_part_2.py` with assertions for the newly-covered
terms, so a future edit cannot silently drop this content again. This
backfill is scoped as follow-up work rather than folded into this report,
since `ULTRA-FAST-LEARN.md`'s stated line count is cross-checked by
exact-total assertions in `tests/test_documentation_structure.py`
(per-domain Fast Track totals and the repository-wide grand total) that
must be updated in lockstep with any line-count change to that file.
