# Domain 5 Fast Track / Ultra Fast Learn: coverage verification report

**Status:** technical verification complete; the four hop-1 gaps and the
five hop-2 gaps below have both been backfilled · **Verified:**
2026-09-09 · **Hop-1 backfill applied:** 2026-09-09 · **Hop-2 backfill
applied:** 2026-09-09

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
(1,580 lines combined, after the hop-1 and hop-2 backfills described below), and then against
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
| 2 | [§2 AWS compliance standards relevant to AI workloads](../domain-5-security-compliance-governance.md#2-aws-compliance-standards-relevant-to-ai-workloads) (line 1135) — AWS Artifact, the five compliance frameworks ([GDPR](../domain-5-security-compliance-governance.md#gdpr-general-data-protection-regulation-conceptual-level) through [ISO/IEC 42001 and the Algorithmic Accountability Act](../domain-5-security-compliance-governance.md#isoiec-42001-and-the-algorithmic-accountability-act-conceptual-level)), both comparison matrices | [part-1 §§8–11](part-1-security-and-compliance.md#8-aws-artifact-reports-vs-agreements) | [§1](ULTRA-FAST-LEARN.md#1-five-compliance-frameworks-side-by-side) |
| 3 | [§§3–5](../domain-5-security-compliance-governance.md#3-aws-config-aws-audit-manager-and-aws-cloudtrail-for-ai-governance) — AWS Config, AWS Audit Manager, and AWS CloudTrail; data governance strategies; shared responsibility; both cross-cutting worked examples (Meridian Lending SOC 2, Aurora Benefits hallucination drift, and the [multi-region GDPR/HIPAA/NIST AI RMF worked example](../domain-5-security-compliance-governance.md#worked-example-a-multi-region-bedrock-and-sagemaker-deployment-under-gdpr-hipaa-and-the-nist-ai-rmf)) (lines 1654–2853) | [part-2 §§1–4](part-2-governance-and-monitoring.md#1-aws-config-aws-audit-manager-and-aws-cloudtrail) | [§6](ULTRA-FAST-LEARN.md#6-shared-responsibility-model) |

## Result: Fast Track (full guide → Fast Track hop)

**Verified clean, with four narrow exceptions — now backfilled.** Across
all three sections above, essentially every exam-relevant fact, decision
criterion, AWS service, metric, and named constraint in the full guide is
present in the Fast Track, condensed to tables, flowcharts, and shortened
exam tips. In particular: all 10 named security-threat categories with
their specific AWS-service mitigations, IAM Access Analyzer, the KMS
key-rotation behavior and data-vs-model CMK distinction, differential
privacy (DP-SGD, epsilon), Titan Image Generator watermarking, MITRE
ATLAS and the OWASP Top 10 for LLM Applications, AWS Artifact's
Reports-vs-Agreements split, all five compliance frameworks with both
comparison matrices, the full Config/Audit Manager/CloudTrail purpose
distinctions, the Bedrock-vs-SageMaker shared-responsibility split, and
both comparison tables in §§3–5 all survive intact. Four specific, named
facts were originally confirmed absent (via `grep`) from the entire
`domain-5-fast-track/` directory — i.e. dropped from `README.md`,
`part-1`, `part-2`, *and* `ULTRA-FAST-LEARN.md` alike — and have since
been backfilled into `part-1`/`part-2` (still intentionally absent from
`ULTRA-FAST-LEARN.md`'s further-condensed cram sheet, per the hop-2
recommendation below):

1. **GDPR's "right to erasure" and "data minimization"** (full guide line
   1206: "Concepts like the right to erasure and data minimization matter
   for AI training data pipelines... ensuring a person's data can be
   removed from a dataset and any downstream retrained model", reused in
   the Northfield worked example at line 2451). Previously neither term
   appeared anywhere in the Fast Track's GDPR treatment — only data
   controller/processor roles, residency, and Article 22 human-review (a
   distinct right) survived. **Now backfilled** into part-1 §9, alongside
   its exam tip, rapid-fire key terms, rapid self-check, and exam traps
   checklist.
2. **GDPR's "special category" data classification** (full guide line
   2371: `genetic data is a GDPR "special category"`). Previously the
   term "special category" did not appear anywhere in the Fast Track.
   **Now backfilled** into part-1 §9 alongside item 1.
3. **"SOC 2 Type II" as the specific audit type** (full guide lines 1804,
   1845, 1856, the Meridian Lending worked example). Previously the Fast
   Track mentioned "SOC 2" generically, but the Type II designation — the
   actual testable fact — never appeared; there was no standalone
   condensed takeaway for the Meridian Lending worked example the way
   the Aurora Benefits and multi-region worked examples both got. **Now
   backfilled** into part-2 §1 as a condensed Meridian Lending worked
   example and exam tip, matching the Aurora Benefits/multi-region
   treatment.
4. **Aurora Benefits' named hallucination-drift metrics** (full guide line
   2018: the custom CloudWatch metric names `HallucinationRate` and
   `FactualConsistencyScore`, metric namespace `RAGAssistant/Quality`, and
   the specific alarm thresholds — warn at 4%, page at 6%, baseline 2%).
   Previously the Fast Track's condensed version kept the 2%→8% drift
   narrative and "custom CloudWatch metric with alarm thresholds"
   generically, but dropped the named metrics, namespace, and threshold
   values entirely. **Now backfilled** into part-2 §2's condensed Aurora
   Benefits worked example.

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

**Five coverage gaps found — now backfilled.** `ULTRA-FAST-LEARN.md` is
deliberately far more compressed than the two-part Fast Track, and that
additional trim is expected. However, the following were named, testable
AWS services/concepts present in the Fast Track — confirmed absent
entirely from `ULTRA-FAST-LEARN.md`, not merged under a different
heading:

1. **"Insecure output handling"** as a named threat category. Present in
   part-1's threat table (line 231) and rapid-fire terms (line 555).
   `ULTRA-FAST-LEARN.md` §5 "Incident-response steps" named 9 of the 10
   threats but skipped this one. **Now backfilled** into §5's
   threat-category list and as its own one-line bullet with the
   validate/sanitize/parameterize + Guardrails output-filtering
   mitigation.
2. **MITRE ATLAS and OWASP Top 10 for LLM Applications.** A full section
   in part-1 (`## 7. Security frameworks: MITRE ATLAS and OWASP Top 10`,
   lines 317–341, plus rapid-fire terms and mini-quiz entries). Neither
   framework name appeared anywhere in `ULTRA-FAST-LEARN.md`, despite its
   own intro claiming to condense the full guide's Sections 1, 2, and 5.
   **Now backfilled** as a bullet in §5 naming both frameworks and their
   one-line descriptions.
3. **Amazon Macie.** Present in part-1 (prompt-injection/sensitive-
   information-disclosure mitigations, lines 228 and 234) and as its own
   table row, decision callout, and mini-quiz answer in part-2 (lines
   119, 153, 333, 366, 381, 400, 451). Never named in
   `ULTRA-FAST-LEARN.md`. **Now backfilled** as a bullet in §5 naming its
   PII/PHI-discovery role and its threat mitigations.
4. **Titan Image Generator watermarking / provenance detection.**
   Part-1's `## 4. Source citation and data lineage` (line 192) covers
   this as its own "Provenance watermarking" table row (line 198), with a
   dedicated disambiguation callout distinguishing it from the Domain
   2/3 "visible logo" watermark. Both "Titan" and "watermark" as terms
   were absent from `ULTRA-FAST-LEARN.md`. **Now backfilled** as a
   one-line bullet in §5.
5. **Algorithmic Accountability Act.** Named in both part-1 (lines 387,
   444, 589, mini-quiz line 653) and part-2's comparison table (line
   351). `ULTRA-FAST-LEARN.md` §1's "Five compliance frameworks" table
   named only GDPR, HIPAA, NIST AI RMF, EU AI Act, and ISO/IEC 42001 —
   the sixth, proposed regulation was dropped entirely. **Now
   backfilled** as a sixth row in §1's compliance-frameworks table
   (marked *proposed*, not binding), plus a clarifying note in the
   binding-vs-voluntary bullet distinguishing "proposed" from
   "voluntary."

One further partial gap is worth noting in prose, though it does not rise
to a strict test assertion below since it is a 3-of-4 partial match on a
common English word: the NIST AI RMF's four named functions are
**Govern, Map, Measure, Manage** (part-1 lines 383/584, part-2 line 349
name all four); `ULTRA-FAST-LEARN.md` line 42's requirements table names
"Govern," "Measure," and "Manage" but never "Map."

## Recommendation

Both backfills identified by this report are now complete — no
outstanding action items remain from this audit.

**Update, 2026-09-09: the four Hop-1 items have been backfilled.** GDPR's
right-to-erasure/data-minimization concepts and the "special category"
term were added to part-1 §9 (sourced verbatim from full guide line
~1206 and the Northfield worked example at line ~2371); a condensed
Meridian Lending worked example naming **SOC 2 Type II** was added to
part-2 §1, matching the Aurora Benefits and multi-region worked examples'
treatment; and the named `HallucinationRate`/`FactualConsistencyScore`
metrics, the `RAGAssistant/Quality` namespace, and the warn/page/baseline
thresholds were added to part-2 §2's condensed Aurora Benefits takeaway.
Each addition also extended `tests/test_domain_5_fast_track_part_1.py`
and `tests/test_domain_5_fast_track_part_2.py` with assertions for the
newly-covered terms.

**Update, 2026-09-09: the five Hop-2 items have also been backfilled.**
"Insecure output handling," the MITRE ATLAS / OWASP Top 10 for LLM
Applications framework names, Amazon Macie, Titan Image Generator
watermarking, and the Algorithmic Accountability Act were all added to
`ULTRA-FAST-LEARN.md` as condensed bullets/table rows sourced verbatim
from part-1/part-2 (§5's threat/mitigation bullets, and a sixth row in
§1's compliance-frameworks table). `tests/test_domain_5_ultra_fast_learn.py`
was extended with a `TestUltraFastLearnHop2BackfilledConcepts` test class
asserting each newly-covered term, and
`tests/test_domain_5_coverage_verification_report.py`'s Hop-2 assertions
were flipped from "absent from Ultra Fast Learn" to "present in Ultra
Fast Learn," so a future edit cannot silently drop this content again.
`ULTRA-FAST-LEARN.md` grew from 182 to 201 lines, which required updating
the per-domain Fast Track total and repository-wide grand total in
`docs/DOCUMENTATION_STRUCTURE.md` (and the exact-total assertions in
`tests/test_documentation_structure.py` that cross-check them) in
lockstep.
